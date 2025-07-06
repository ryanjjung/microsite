# Renderer

A `microsite.render.RenderEngine` provides a common way for us to parse over a set of file paths and do different things with them.


## Markdown Renderer

A `microsite.render.markdown.MarkdownRenderEngine` looks for Markdown files and renders them into HTML files using a specified template and stylesheet.


### Configuration Variables

The Markdown render engine can be configured with the following options:

- `extensions`: List of Markdown extensions to enable when rendering Markdown into HTML. A full list of options can be [found here](https://github.com/Python-Markdown/markdown/blob/4669a09894d4a35cd5f5d2106b0da95e48d1a3f9/docs/extensions/index.md#officially-supported-extensions). Defaults to using no extensions.
- `html_template`: Path to a custom Jinja2 template you wish to use when rendering **all** Markdown files for this project. Defaults to using the `markdown.html.j2` template found in this project.
- `pretty_html`: When True, renders HTML with line spacing and indentation. When False, renders all HTML into a single line with minimal whitespace. The "False" option results in smaller files and theoretically faster page loads, while the True option makes for easier reading and debugging later. Defaults to False.
- `rewrite_md_extensions`: When True, Markdown files discovered with a `*.md` file extension are written in the output folder with `*.html` extensions instead. When False, the `*.md` extension is preserved. This can impact how web servers present the file. Preserving the `*.md` extensions can cause files to be served as plaintext instead of being interpreted by the browser as a real website. For this reason, this defaults to True. You should almost never set this to False unless you know what you're doing.
- `rewrite_md_urls`: When True, each HTML page is reviewed before being saved. Any links pointing to another project file using the `*.md` extension will have those extensions replaced with `*.html`. This is typically used in conjunction with `rewrite_md_extensions` to preserve the validity of links after rendering. You usually want this set to True, which is the default, although if you disable `rewrite_md_extensions` you may wish to disable this as well.
- `stylesheet`: Path to the stylesheet to embed with every page. Defaults to the `plain-white.css` stylesheet included in this project.
- `stylesheet_target_name`: Name to give the stylesheet file when it's copied into the output directory. This defaults to `style.css`, which is typically fine. Change this value if you have some other file in the root directory of your project called `style.css` which would otherwise be overwritten during rendering.   
- `title` - The value to use as the `<title>` text for each page rendered.

A completely default configuration for your project file looks like this:

```toml
[render.engine.markdown]
extensions = []
html_template = "microsite/render/templates/markdown.html.j2"
pretty_html = true
rewrite_md_extensions = true
rewrite_md_urls = true
stylesheet = "microsite/render/styles/plain-white.css"
stylesheet_target_name = "style.css"
```


### Page Indexing

One special option needs some extra attention: the `index` option. This is a table of metadata about your source files. You define indices by naming a config table after them. For example:

```toml
[render.engine.markdown.index."page2.md"]
title = "Page 2!"
```

Each `index` entry has the following options:

- `title` - Override the `<title>` text for this page.


### Jinja Templates

This project uses a Jinja2 template to combine the various Markdown documents into proper web pages. This template relies upon the following variables which are populated by the rendering engine automatically:

- `title`: The title of the page being rendered.
- `stylesheet`: The path to the stylesheet to embed.
- `html`: The HTML content to embed.

If you choose to use a custom template, you should make use of these variables.

