Getting Started with Microsite
==============================


Microsite simplifies the process of putting content online. Still, the more you know about how the
web works, the more this tool will make sense and the more you'll be able to make of it. This page
will get you up and running, but if you'd like a better understanding of what's going on here, you
may wish to check out the :ref:`concepts` page.


Setting Up
----------

Today, Microsite is a command-line tool. Someday this will change (we hope), but for now you'll have
to deal with it. (Sorry.)

.. warning::

    The commands in this section have been tested on a computer running Linux. We expect they should
    work as-is on a Mac as well, though this has not been tested. We would expect them to fail on
    Windows, though. If you test this process on these platforms and find any bugs, please
    `file an issue <https://github.com/ryanjjung/microsite/issues/new>`_.


Install Python 3.13 or later
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Various methods of doing this are described on
`Python's website <https://www.python.org/downloads/>`_.


Install the virtualenv tool
^^^^^^^^^^^^^^^^^^^^^^^^^^^

virtualenv is a tool used for creating Python sandboxes. We'll use this to prevent Microsite from
interfering with other Python-based software on your system.

.. code-block:: bash

    python -m ensurepip
    python -m pip install virtualenv


Install git
^^^^^^^^^^^

`git <https://git-scm.com/downloads>`_ is the version control system we manage changes to Microsite
code with. You'll need to install it to get a copy of the code.


Get a copy of the code
^^^^^^^^^^^^^^^^^^^^^^

The code that is Microsite is managed on a popular website for developing software publicly called
`Github <https://github.com/ryanjjung/microsite>`_. To get a copy of it, clone the code with git:

.. code-block:: bash

    # "git clone" creates a folder called "microsite" with the code in it
    git clone https://github.com/ryanjjung/microsite.git
    cd microsite  # This switches to the code directory
    ls -lah  # This lists out the files in the directory


Create a virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This step creates an empty sandbox environment for us to use and then installs all the other
libraries Microsite needs to run.

.. code-block:: bash

    python -m virtualenv ./venv/  # Build the sandbox
    source ./venv/bin/activate  # Activate the sandbox, we're "in" it now
    python -m pip install .  # Install all of our dependencies

When you're done, you can leave the sandbox with:

.. code-block:: bash

    deactivate

And if you need to reactivate it, you don't have to create it again. You can just run:

.. code-block:: bash

    cd microsite  # Go back to where the code lives
    source ./venv/bin/activate  # Activate the environment

And if something goes wrong, you can always delete the sandbox entirely:

.. code-block:: bash

    rm -rf ./venv

And then recreate it following the first set of steps.


Gathering Materials
-------------------

Out of the box, you can use Microsite's rendering process to produce web content without any
outside requirements. However, to publish a website online, you'll need to get a few other things
set up.


Get a Domain Name
^^^^^^^^^^^^^^^^^

Regardless of what publishing engine you use, you'll need to own a domain name. There are many
domain name registars who can help you find and purchase a domain name. Domain names range in price,
but generally shorter domain names are more expensive, and so are domains on popular top-level
domains like ``.com`` or ``.net``. Domains must be purchased on a subscription basis, though most
registrars will offer bulk rates for purchasing multiple years of registration ahead of time.

Microsite makes no endorsements of any domain registars, though the domain ``microsite.info`` is
registered through `Porkbun <https://porkbun.com>`_.


Choose a Publishing Engine
^^^^^^^^^^^^^^^^^^^^^^^^^^

A publishing engine is a method of publishing static content to the Internet. Theoretically, there
are thousands of ways to accomplish this. The publishing engine model allows us to grow the number
of publishing methods we support over time.

.. note::

    Today, we only support one method of publication, the :ref:`tbp-s3website`.

Specific publishing engines will have additional requirements. You should select a publishing engine
and read about its requirements on the :ref:`publish-engines` page.


Create Some Content
^^^^^^^^^^^^^^^^^^^

Web pages use a markup language called `HTML <https://developer.mozilla.org/en-US/docs/Web/HTML>`_
to describe the structure and content of the page. They also use
`Cascading Style Sheets <https://developer.mozilla.org/en-US/docs/Web/CSS>`_ to apply style to that
content, making it appear in different colors, use different fonts, align certain elements just so,
etc.

This is a lot to learn, so instead Microsite uses a much simpler markup language called
`Markdown <https://daringfireball.net/projects/markdown/syntax>`_. Markdown reduces the complexity
of HTML into simple textual cues that you're probably already somewhat familiar with. Many social
media sites use a form of Markdown to format messages.

You write the Markdown and Microsite will convert it to HTML and insert it into the fuller context
of a website with page structure and style to produce complete web pages.


Write a Project File
^^^^^^^^^^^^^^^^^^^^

A project file describes the configuration for your project's rendering and publishing needs. The
easiest way to create one is to copy the ``sample-project.toml`` file from this repo and then
customize it to your needs. Each rendering and publishing engine supports a different set of
options, which you can read about in the :ref:`render-engines` and :ref:`publish-engines` pages.


Render and Publish
^^^^^^^^^^^^^^^^^^

Specifying your project file, render your content:

.. code-block:: sh

    python -m microsite projectfile.toml render

You can review the content before publishing it. Open it in your favorite browser:

.. code-block:: sh

    firefox output_dir/index.html

You can then publish the content:

.. code-block:: sh

    python -m microsite projectfile.toml publish

The first time you run this, the site will be built from the ground up. This can take some time, so
be patient. When it's done, your site will be live. Generally, future updates to an existing site
are much faster.

If you need to bring the site offline, you can destroy it just as easily:

.. code-block:: sh

    python -m microsite projectfile.toml publish -x


Exploring More
^^^^^^^^^^^^^^

This code contains a sample site, which you can use to test this software. Read the
`sample project file <https://github.com/ryanjjung/microsite/blob/main/sample-project.toml>`_ and
find the settings you find there in this documentation. You will need to substitute your own values
for some of the settings. How to obtain those values is the subject of the :ref:`render-engines` and
:ref:`publish-engines` pages, which will also tell you how to customize things like the structure of
your pages and the style applied to them. If it's outside reading about the underlying technologies
you seek, then you may want to scan through our :ref:`acknowledgements` page. The :ref:`concepts`
page provides a little more focused reading on relevant topics.