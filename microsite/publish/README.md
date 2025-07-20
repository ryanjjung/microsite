# Publisher

A `microsite.publish.PublishEngine` provides a common way for us to deploy static files which are already prepared and ready for publication to a site.

All publishers require these options:

- `source`: The directory containing the files to deploy. This is usually the output of a previous render step.

An example config:

```toml
[publish]
source = "sample-output/"
```

## Pulumi and tb_pulumi Publishers

These publish engines use the Pulumi infrastructure-as-code tool to build sites. All Pulumi publishers support the following options:

- `project_name`: A computer-friendly term for the site, like `"microsite"`. Site visitors will never see this.
- `project_description`: A user-friendly description for the site, like `"Sample site for MicroSite!"` Site visitors will never see this.
- `aws_region`: The AWS region you want to build your resources in.
- `pulumi_state_backend`: How you want Pulumi to store its state files. Must be either `"cloud"` or `"s3"`. If "cloud", you must also provide a `pulumi_access_token_file`. If "s3", you must provide a `pulumi_state_s3_bucket`.
- `pulumi_access_token_file`: Path to a file containing your Pulumi Cloud API token. Ignored if the `pulumi_state_backend` is not "cloud".
- `pulumi_passphrase_file`: Path to a file containing the secret passphrase used to encrypt secrets and state in Pulumi.
- `pulumi_log`: File to save Pulumi's standard output in.
- `pulumi_error_log`: File to save Pulumi's error output in.
- `pulumi_stack_name`: Name of the "stack" (an instance of your site) to use. This is an advanced feature that you should only alter if you have some knowledge of Pulumi itself.
- `pulumi_state_s3_bucket`: The S3 bucket in which Pulumi should store its state files. Ignored if `pulumi_state_backend` is not "s3".
- `pulumi_work_dir`: Path to the directory to use as a working environment. If this is not provided, a randomly named directory will be created.
- `persist_work_dir`: When True, the working directory will not be deleted between publish runs. If this is ignored, behavior will depend on whether a `work_dir` was specified. If this tool is told to build a temporary working directory, this will default to False and the directory will be deleted after the run. If a `work_dir` was specified, it will be left alone after the run unless this is explicitly set to False.


## tb_pulumi S3Website Publisher

A `microsite.publish.s3.TbPulumiS3Website` uses the [tb_pulumi](https://thunderbird.github.io/pulumi/index.html) library to syncronize your website's files to an [AWS S3](https://aws.amazon.com/s3/) bucket and set a website config on it, allowing your files to be served to the Internet.

This supports all of the config options for other Pulumi publishers. It also supports the following options:

- `publish_bucket`: The S3 bucket the site should be deployed to. Do not create this bucket, as it will be managed by this tool.
- `index_document`: If a site visitor requests a URL that ends in a slash (`/`), this file will be served from that directory. This is usually `index.html`. It must return a file that really exists or the server will return a `404 Not Found` error.
- `acm_certificate_arn`: The ARN of the AWS Certificate Manager certificate to secure site communication with.
- `domain`: The top-level domain you will publish under.
- `subdomain`: The subdomain to publish under. For example, if your domain is `foobar.com` and your subdomain is `fizzbuzz`, your content will be published at `fizzbuzz.foobar.com`.
- `route53_zone_id`: The zone ID of the Route53 hosted zone to build DNS records in.

An example config:

```toml
[publish.targets.s3website-prod]
engine = "tbp_s3website"
project_name = "microsite"
project_description = "MicroSite Sample Site"
aws_region = 'us-east-1'
pulumi_state_backend = "s3"  # or "cloud"
pulumi_access_token_file = ""  # Ignored when pulumi_state_backend is not "cloud"
pulumi_passphrase_file = "sample-site.pulumi.pass"
pulumi_log = "pulumi.log"
pulumi_error_log = "pulumi.err"
pulumi_stack_name = "prod"
pulumi_state_s3_bucket = "microsite-sample-site-pulumi"
pulumi_work_dir = "tbpulumi-s3website-prod"
persist_work_dir = false
publish_bucket = "microsite-sample-site"
index_document = "index.html"
acm_certificate_arn = "arn:aws:acm:...."
domain = "yourdomain.com"
subdomain = "www"
route53_zone_id = "Z0123456789ABCDEF"
```
