# syntax=docker/dockerfile:experimental

# Build stage: Install yarn dependencies
# ===
FROM node:16 AS yarn-dependencies
WORKDIR /srv
ADD package.json yarn.lock .
RUN --mount=type=cache,target=/usr/local/share/.cache/yarn yarn install

# Build stage: Run "yarn run build-js"
# ===
FROM yarn-dependencies AS build-js
WORKDIR /srv
ADD src . 
RUN yarn run build-js

# Build stage: Run "yarn run build-css"
# ===
FROM yarn-dependencies AS build-css
WORKDIR /srv
COPY src/sass src/sass
RUN yarn run build-css

# Build stage: Run "yarn run build-site"
# ===
FROM yarn-dependencies AS build-site
WORKDIR /srv
COPY src/ src/
COPY .eleventy.js .eleventy.js
COPY --from=build-css /srv/src/css src/css
COPY --from=build-js /srv/src/js src/js
RUN yarn run build-site

# Build the production image
# ===
FROM ubuntu:focal

# Set up environment
ENV LANG C.UTF-8
WORKDIR /srv

# Install nginx
RUN apt-get update && apt-get install --no-install-recommends --yes nginx

# Import code, build assets and mirror list
RUN rm -rf package.json yarn.lock webpack.config.js nginx.conf
COPY --from=build-site /srv/_site .
COPY doc doc

ARG BUILD_ID
ADD nginx.conf /etc/nginx/sites-enabled/default
RUN sed -i "s/~BUILD_ID~/${BUILD_ID}/" /etc/nginx/sites-enabled/default

STOPSIGNAL SIGTERM

CMD ["nginx", "-g", "daemon off;"]
