# microsite

Tools for building a small web.


## Usage

MicroSite is a tool of simplicity. Use it to reduce the difficulty of publishing static content on the web.


**Build Your Content with Markdown**

Use simple [Markdown](https://daringfireball.net/projects/markdown/syntax) syntax to create your content in a separate directory. See our [sample site](sample-site/) for some examples.

**Render the Content into HTML**

Use MicroSite's command line tool to convert your Markdown into HTML.

```
# python -m microsite sample-project.toml render
Logging configured.
Target directory already exists. Deleting it now to ensure a clean build.
Creating target directory sample-output/
Rendering sample-site/page2.md to sample-output/page2.html
Rewriting URLs in links...
Rendering sample-site/index.md to sample-output/index.html
Rewriting URLs in links...
Rendering sample-site/dir/page3.md to sample-output/dir/page3.html
Rewriting URLs in links...
Copying unrendered file microsite.svg
```

Open the output in your web browser:

```
firefox sample-output/index.html
```

![Sample Site](sample-site-screenshot.png)

## To Do

Lots of stuff to do! Someday this tool will offer ways of publishing your static content to the internet on a variety of platforms.