module.exports = function (eleventyConfig) {
  eleventyConfig.setUseGitIgnore(false);
  // Copy to _site as it contains jQuery dep
  eleventyConfig.addPassthroughCopy("doc/");
};
