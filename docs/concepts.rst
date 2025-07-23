.. _concepts:

Concepts
========

A website can be a lot of things. In its simplest form, it can be a handful of files written in
specialized languages that are interpreted by a web browser as web pages. Sometimes it's an
application that generates web pages on the fly based on inputs it receives over the course of an
interactive session, like an online shop or a blogging platform. Microsite's capabilities can be
stretched with the use of additional technologies, but its ideal usage is more like the first
option.

Regardless, websites are presented to the world through the use of web servers. A server is just a
computer that presents an application to a network. In the old days, you might have run a data
center or rented out physical servers inside a data center if you wanted to run Internet-connected
services. These days, we can rent servers "in the cloud," specifying exactly what resources we need
and paying for only what we use.

Putting a website online is also known as "hosting" the website on a server. There are thousands of
ways to host a website which grow in complexity with a website's needs. Some websites rely on other
services like databases to keep track of user data or memory caches to keep commonly accessed data
in a very fast online data store. Some rely on a lot of servers all running the same software.

Microsite tries to keep the hosting model simple and inexpensive wherever possible, and this is not
hard to do when the goal is to present relatively small amounts of static content.


Object Stores
^^^^^^^^^^^^^

An object store is an online place to store arbitrary files. Many of these exist with different
feature sets. Microsite uses AWS's Simple Storage Service (S3) to upload your website's files to the
Internet. S3 differs in some ways from other object stores like Dropbox whose aim is to help people
share files with one another. Relevant here is the way it can publicize content and present it with
a basic website configuration.


Content Delivery Networks
^^^^^^^^^^^^^^^^^^^^^^^^^

A Content Delivery Network (CDN) is a series of servers distributed geographically across the globe.
When you upload your files into a CDN, they are copied to all of these "edge" servers. When a user
visits the URL the CDN presents this content through, their request is routed to the physically
closest server, which improves the response time of the website.

Microsite uses CloudFront, which is the name of AWS's CDN, to present the S3 website through edge
servers. This content is presented through your domain name.


Domain Name Service
^^^^^^^^^^^^^^^^^^^

A Domain Name Service (DNS) is a service that translates user-friendly domain names like
`samplesite.microsite.info` into the network addresses that actually serve your content. Without
this, the Internet would be a very difficult system to work with.

In a DNS server, you set up "records" which help aim traffic at the right places. These records all
have a type. There are many types, but in setting up your Microsite you will have to set NS (Name
Server) records after you have registered your domain to tell the world that AWS will be your
primary DNS server.

Microsite also sets up a CNAME record to point your subdomain to the CloudFront distribution. A
CNAME is like an alias referring not to a specific network address (that's what an "A" record does),
but to another domain name.
