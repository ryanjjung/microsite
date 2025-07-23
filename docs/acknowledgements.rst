.. _acknowledgements:

Acknowledgements
================

Microsite stands on the shoulders of giants. Here is a listing of various technologies we use to
make this work.

- `Python <https://www.python.org/>`_: The programming language Python is the real engine underneath
  Microsite. It's how we integrate all the other technology into one program.
- `Amazon Web Services <https://aws.amazon.com/>`_: AWS provides a variety of services for a ton of
  different needs. We make use of services like S3, CloudFront, Route53, and Certificate Manager.
- `HyperText Markup Language <https://developer.mozilla.org/en-US/docs/Web/HTML>`: HTML defines the
  structure of every web page on the Internet.
- `Cascading Style Sheets <https://developer.mozilla.org/en-US/docs/Web/CSS>`_: CSS describes how
  web pages look by describing the visual properties of HTML elements.
- `Markdown <https://daringfireball.net/projects/markdown/syntax>`_: A very simple markup language
  that provides an entry point for producing HTML. This helps minimize the complexity of producing
  valid web pages. We convert it to HTML during the rendering process.
- `Sphinx <https://www.sphinx-doc.org/en/master/index.html>`_: We build our documentation using the
  Sphinx tool and the
  `Restructured Text <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#rst-primer>`_
  markup language.
- `Jinja <https://jinja.palletsprojects.com/en/stable/>`_: Jinja is the templating engine that lets
  us programmatically insert your content into a larger web page structure. It ensures that your
  pages are all consistently arranged and styled.
- `Pulumi <https://www.pulumi.com/>`_: Pulumi is an "infrastructure as code" tool. It allows us to
  design cloud-hosted systems in code and then manage them by comparing an ideal state (the code
  we write) to the real state (how the cloud services describe themselves) and then make changes
  to consolidate any differences.
- `tb_pulumi <https://github.com/thunderbird/pulumi/>`_: `Thunderbird <https://www.thunderbird.net/>`_
  maintains this library which extends Pulumi's base capabilities and provides some of the more
  complex infrastructure patterns we need to make your website work.
- `git <https://git-scm.com/>`_: git is the version control software we use to manage changes to Microsite.
- `Github <https://github.com/>`_: Github is a web platform that we use to converse about the code,
  report bugs, request new features, and organize work on the code.
