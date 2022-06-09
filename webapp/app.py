import os
import talisker.requests

from canonicalwebteam.flask_base.app import FlaskBase
from flask import render_template, make_response, send_from_directory

from canonicalwebteam.templatefinder import TemplateFinder
from canonicalwebteam.discourse import (
    DiscourseAPI,
    Docs,
    DocParser,
)
from canonicalwebteam.search import build_search_view

DISCOURSE_API_KEY = os.getenv("DISCOURSE_API_KEY")
DISCOURSE_API_USERNAME = os.getenv("DISCOURSE_API_USERNAME")

# Rename your project below
app = FlaskBase(
    __name__,
    "mir-server.io",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
)

session = talisker.requests.get_session()
discourse_api = DiscourseAPI(
    base_url="https://discourse.ubuntu.com/",
    session=session,
    api_key=DISCOURSE_API_KEY,
    api_username=DISCOURSE_API_USERNAME,
)

DISCOURSE_API_KEY = os.getenv("DISCOURSE_API_KEY")
DISCOURSE_API_USERNAME = os.getenv("DISCOURSE_API_USERNAME")


# Old docs
# ===
@app.route("/doc/<path:path>")
def doc(path):
    return send_from_directory(f"{os.getcwd()}/doc", path)


# New docs
# ===
url_prefix = "/docs"
docs_app = Docs(
    parser=DocParser(
        api=discourse_api,
        index_topic_id=27559,
        url_prefix="/docs",
    ),
    document_template="docs/document.html",
    url_prefix="/docs",
    blueprint_name="mir-server-docs",
)
docs_app.init_app(app)


app.add_url_rule(
    "/docs/search",
    "docs-search",
    build_search_view(
        session=session,
        site="mir-server.io",
        template_path="docs/search.html",
    ),
)


@app.route("/sitemap.xml")
def sitemap_index():
    xml_sitemap = render_template("sitemap/sitemap-index.xml")
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response


@app.route("/sitemap-links.xml")
def sitemap_links():
    xml_sitemap = render_template("sitemap/sitemap-links.xml")
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response


template_finder_view = TemplateFinder.as_view("template_finder")
app.add_url_rule("/", view_func=template_finder_view)
app.add_url_rule("/<path:subpath>", view_func=template_finder_view)
