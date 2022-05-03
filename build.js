let esbuild = require("esbuild");
const path = require("path");

// Refer to https://github.com/canonical-web-and-design/ubuntu.com/blob/main/build.js
// If new js custom libraries added
let entries = {};

const isDev = process && process.env && process.env.NODE_ENV === "development";

// if CAPTCHA_TESTING_API_KEY doesn't exist then we are on demo / staging / production and use the real API key
const captchaKey =
  (process && process.env && process.env.CAPTCHA_TESTING_API_KEY) ||
  "6LfYBloUAAAAAINm0KzbEv6TP0boLsTEzpdrB8if";

for (const [key, value] of Object.entries(entries)) {
  const options = {
    entryPoints: [value],
    bundle: true,
    minify: isDev ? false : true,
    nodePaths: [path.resolve(__dirname, "./static/js/src")],
    sourcemap: isDev ? false : true,
    outfile: "static/js/dist/" + key + ".js",
    target: ["chrome90", "firefox88", "safari14", "edge90"],
    define: {
      "process.env.NODE_ENV":
        // Explicitly check for 'development' so that this defaults to
        // 'production' in all other cases.
        isDev ? '"development"' : '"production"',
      "process.env.CAPTCHA_TESTING_API_KEY": `"${captchaKey}"`,
    },
  };

  esbuild
    .build(options)
    .then((result) => {
      console.log("Built " + key + ".js");
    })
    // Fail the build if there are errors.
    .catch(() => process.exit(1));
}
