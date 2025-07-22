.. _publish-engines:

Publishing Engines
==================


.. _tbp-s3website:

tbp_s3website
-------------

This engine uses some services provided by Amazon Web Services (AWS). One of those is the Simple
Storage Service (S3), which is just an online file store. The engine uploads your website files to
an S3 bucket and then makes the files public. It applies a website configuration that allows for
a default file to serve if no file is specifically requested.

The second service is called Route53. This is AWS's DNS service. DNS (Domain Name Service) is a
service that turns friendly domain names (like ``microsite.info``) into the actual addresses of the
servers presenting the content on those domains. After registering a domain name, you will need to
update the NS record to point to AWS's DNS servers.

We also use a service called CloudFront. This is a content delivery network (CDN) which acts as a
gateway to your content. It pushes copies of your files to servers all over the world so they can be
served as quickly as possible to users based on their geographical region. It can also be configured
to use your custom domain name and to secure all traffic using TLS.
