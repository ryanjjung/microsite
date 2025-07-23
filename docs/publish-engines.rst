.. _publish-engines:

Publishing Engines
==================

A publishing engine is a method of deploying the website content you've created to an online server.

All publishing engines require one setting in the project file:

- ``source``: Directory containing the content to be published.

Your project file should have a section in it that looks like this:

.. code-block:: toml

    [publish]
    source = "path/to/your/files"


.. _pulumi-publish-engines:

Pulumi Publishing Engines
^^^^^^^^^^^^^^^^^^^^^^^^^

`Pulumi <https://www.pulumi.com>`_ is a tool that we use to maintain online cloud infrastructure. It
is one of a class of software called "infrastructure as code" tools. It is particularly useful here
because it allows us to set up a working Pulumi environment, programmatically generate a Pulumi
program, and then automate the tool to build cloud infrastructure in the background, all completely
transparent to the Microsite user.

All Pulumi publishing engines support the following options:

- ``project_name``: A computer-friendly term for the site, like ``"microsite"``. Site visitors will
  never see this; it is for internal naming purposes only.
- ``project_description``: A user-friendly description for the site, like ``"Sample site for
  MicroSite!"`` Site visitors will never see this; it is for Pulumi's internal usage only.
- ``aws_region``: The AWS region you want to build your resources in. A region is a geographical
  area in which AWS operates multiple data centers. Each one has a name like ``us-east-1``
  (Virginia, USA) or ``eu-central-1`` (Frankfurt, Germany) which you can use for this option. All of
  your resources will live in this region.
- ``pulumi_state_backend``: Pulumi tracks the resources it builds in a file stored in a remote
  location. These is called "state files". This setting determines how Pulumi will store its state
  files. Must be either ``"cloud"`` or ``"s3"``. If ``cloud``, you must also provide a
  ``pulumi_access_token_file`` setting. If ``"s3"``, you must provide a ``pulumi_state_s3_bucket``.
- ``pulumi_access_token_file``: Path to a file containing your Pulumi Cloud API token. You can
  obtain such a token through the Pulumi Cloud website. Always treat this value as a secret. Do not
  share it with anyone or publicize it in any way. This setting is ignored if the
  ``pulumi_state_backend`` is not ``"cloud"``.
- ``pulumi_passphrase_file``: Pulumi keeps some configuration settings in a file of its own. If any
  secrets are ever committed to that file, it encrypts the data first using a secret passphrase.
  This setting is the path to a file containing the secret passphrase used to encrypt Pulumi's
  secrets. Always treat this value as a secret. Do not share it with anyone or publicize it in any
  way.
- ``pulumi_log``: File to save Pulumi's standard output in. Defaults to ``pulumi.log``.
- ``pulumi_error_log``: File to save Pulumi's error output in. Defaults to ``pulumi.err``.
- ``pulumi_stack_name``: In Pulumi, you define the cloud resources you need and their properties and
  relationships. Then you can create multiple isolated instances of those resources by specifying
  that they belong to a different "stack". While this can allow more sophisticated system designs,
  we don't rely on them in Microsite. This setting is the name of the "stack" to use when building
  the systems. This is an advanced setting that you should rarely alter, and probably only if you
  have a working knowledge of Pulumi.
- ``pulumi_state_s3_bucket``: The S3 bucket in which Pulumi should store its state files. Ignored if
  ``pulumi_state_backend`` is not ``"s3"``.
- ``pulumi_work_dir``: Path to the directory to use as a Pulumi working environment. If this is not
  provided, a randomly named directory will be created.
- ``persist_work_dir``: When ``true``, the working directory will not be deleted between publish
  runs. If this is ignored, behavior will depend on whether a ``work_dir`` was specified. If
  ``pulumi_work_dir`` is not specified, this will default to ``false`` and the working directory
  will be deleted after Microsite is done running. If a ``work_dir`` was specified, it will be left
  alone after the run unless this is explicitly set to ``false``. This setting is useful for
  debugging problems with a Pulumi execution. Under most circumstances, and unless you have a
  working knowledge of Pulumi, this should probably be set to ``false``.


.. _tbp-publish-engines:

Thunderbird Pulumi Publishing Engines
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Thunderbird <https://www.thunderbird.net>`_ maintains a library (tb_pulumi) that extends the basic
capabilities of Pulumi and offers some common infrastructure patterns. This is handy for our use
case because the underlying patterns we use are somewhat complicated. Using this code simplifies
Microsite's task considerably.

A tb_pulumi publishing engine does not take any additional configuration options above the basic
Pulumi publishing engine described above. It does perform additional run-time checks to make sure
that its working environment is valid.


.. _tbp-s3website:

tb_pulumi S3 Website
^^^^^^^^^^^^^^^^^^^^

This publishing engine hosts your files on AWS using the following services:

- **Route53:** Route53 is the name of AWS's Domain Name Service (DNS). DNS is a service that turns
  friendly domain names (like ``microsite.info``) into the actual addresses of the servers
  presenting the content on those domains. You will use it to point your domain to the web server.
- **Simple Storage Service (S3):** This is an online "object store" where you can upload any kind of
  file. An S3 "bucket" is an online directory of files. By default, these keep your files private,
  but we enable public read access to them to make them available to the Internet.
- **Amazon Certificate Manager (ACM):** Internet users should expect that the traffic passing between
  their browser and the online server is made private by using an encryption layer called Transport
  Layer Security (TLS). This technology relies upon a chain of trust to validate "certificates" that
  ensure the remote server is legitimate and that communication can proceed securely. You will need
  to create a certificate for your domain to secure traffic to your site.
- **CloudFront:** CloudFront is a content delivery network (CDN) which acts as a gateway to your
  content. It pushes copies of your files to servers all over the world so they can be served as
  quickly as possible to users based on their geographical region. It can also be configured to use
  your custom domain name and to secure all traffic by using the certificate from ACM.

All of the options available for Pulumi publishing engines are available for this engine as well.
This engine additionally supports the following configuration options:

- ``publish_bucket``: The S3 bucket the site should be deployed to. Do not create this bucket
  yourself, as it will be managed by this tool.
- ``index_document``: If a site visitor requests a URL that ends in a slash (`/`), the file
  specified here will be served from that directory. This is usually ``index.html``. It must return
  a file that really exists or the server will return a ``404 Not Found`` error.
- ``acm_certificate_arn``: The ARN of the AWS Certificate Manager certificate to secure site
  communication with. An ARN is a unique identifer for a resource in AWS. You can copy this value
  out of the web console.
- ``domain``: The top-level domain you will publish under (such as ``microsite.info``.
- ``subdomain``: The subdomain to publish under. For example, if your domain is ``microsite.info``
  and your subdomain is ``samplesite``, your content will be published at
  ``samplesite.microsite.info``.
- ``route53_zone_id``: The zone ID of the Route53 hosted zone to build DNS records in. This can be
  taken from the Route53 web console.
