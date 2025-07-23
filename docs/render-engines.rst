.. _render-engines:

Rendering Engines
=================

Microsite uses libraries called rendering engines to convert your content into web pages. You can
enable multiple engines (in the future, when multiple engines exist). Each engine marks files it manipulates so
that unmodified files can be copied over directly at the end of the process.

Some configuration options apply to the rendering process as a whole. The following options should
appear in your project file under the ``[render]`` header:

- ``source``: The directory in which the files to be converted into web pages live.
- ``target``: The directory in which the converted web page files should be created.
- ``delete_target_dir``: When set to ``true``, this causes the target directory to be completely
  deleted and recreated at the beginning of the rendering process, ensuring a clean build. This
  defaults to ``true`` since it ensures a clean build.
- ``engines``: A list of rendering engines to enable.

A typical "render" section of a project file looks like this:

.. code-block:: toml

    [render]
    source = "sample-site/"
    target = "sample-output/"
    delete_target_dir = true
    engines = ["markdown"]

Each rendering engine will support its own specific options as well.


Markdown Rendering Engine
^^^^^^^^^^^^^^^^^^^^^^^^^

The Markdown rendering engine looks for files in the source directory whose filenames end in ``.md``.
These files are rendered into HTML, and those HTML snippets placed into the larger template of each
web page.

The input files have ``*.md`` filenames, and links to other documents are typically written as links
to other ``*.md`` files. When rendered, the output files will all have ``*.html`` extensions, which
would cause all of those ``*.md`` links to break. To preserve link functionality both before and
after rendering, this module can convert ``*.md`` links into ``*.html`` links.

Set off this engine's configuration options inside a ``[render.engine.markdown]`` section. It
supports the following options:

- ``extensions``: List of Markdown extensions to enable when rendering Markdown into HTML. A full
  list of options can be found in the `Python-Markdown documentation
  <https://github.com/Python-Markdown/markdown/blob/HEAD/docs/extensions/index.md#officially-supported-extensions>`_.
  Defaults to using no extensions.
- ``html_template``: Path to a custom Jinja2 template you wish to use when rendering **all**
  Markdown files for this project. Defaults to using the ``markdown.html.j2`` template found in this
  project. Use this if you want to change the overall layout of your page.
- ``pretty_html``: When ``true``, renders HTML with added line spacing and indentation to improve
  human readability of the output. When ``false``, renders all HTML into a single line with minimal
  whitespace. The ``false`` option results in smaller files and theoretically faster page loads,
  while the ``true`` option makes for easier debugging. Defaults to ``false``.
- ``rewrite_md_extensions``: When ``true``, Markdown files discovered with a ``*.md`` file extension are
  written in the output folder with ``*.html`` extensions instead. When ``false``, the ``*.md``
  extension is preserved. This can impact how web servers detect the file type and thus how they
  represent the file type to browsers using the ``Content-Type`` header. Preserving the ``*.md``
  extensions can cause files to be served as plaintext (mimetype ``text/plain``) instead of being
  interpreted by the browser as a real website (``text/html``). For this reason, this defaults to
  ``true``. You should almost never set this to ``false`` unless you know what you're doing.
- ``rewrite_md_urls``: When ``true``, each HTML page is reviewed before being saved. Any links
  pointing to another project file using the ``*.md`` extension will have those extensions replaced
  with ``*.html``. This is typically used in conjunction with ``rewrite_md_extensions`` to preserve
  the validity of links after rendering. You usually want this set to ``true``, which is the
  default, although if you disable ``rewrite_md_extensions`` you may wish to disable this as well.
- ``stylesheet``: Path to the stylesheet to embed with every page. Defaults to the
  ``plain-white.css`` stylesheet included in this project.
- ``stylesheet_target_name``: Name to give the stylesheet file when it's copied into the output
  directory. This defaults to ``style.css``, which is typically fine. Change this value if you have
  some other file in the root directory of your project called ``style.css`` which would otherwise
  be overwritten during rendering.   
- ``title`` - The value to use as the default title text (appearing in the browser's title bar or
  tab) for each page rendered. This can be overridden using the ``index`` settings described below.

Here's an example of a Markdown rendering engine config from our sample site's project file:

.. code-block:: toml

    [render.engine.markdown]
    extensions = ["tables", "md_in_html"]
    html_template = "microsite/render/templates/markdown.html.j2"
    pretty_html = true
    rewrite_md_extensions = true
    rewrite_md_urls = true
    stylesheet = "microsite/render/styles/plain-white.css"
    stylesheet_target_name = "style.css"
    title = "Microsite Sample Site"


Page Indexing
^^^^^^^^^^^^^

One special option needs some extra attention: the `index` option. This is a table of metadata about
your source files. You define indices by naming a config table after them. For example:

.. code-block:: toml

    [render.engine.markdown.index."page2.md"]
    title = "Page 2!"

Each `index` entry has the following options:

- ``title`` - Override the ``<title>`` text for this page.


Jinja Templates
^^^^^^^^^^^^^^^

This project uses a Jinja2 template to combine the various Markdown documents into proper web pages.
This template relies upon the following variables which are populated by the rendering engine
automatically:

- ``title``: The title of the page being rendered.
- ``stylesheet``: The path to the stylesheet to embed.
- ``html``: The HTML content to embed.

If you choose to create a custom template, you should make use of these variables.