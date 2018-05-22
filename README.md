# Django Basic REST API

A basic Django 1.11 REST API that includes an advanced project layout and routes for authentication.

## Introduction

For a lack of a documentation, some brief words of introduction. All the provided commands are only tested on Mac (but will probably also work for Linux).

### About this project

If you, like me, work with Django in your job, you probably create a lot of projects. I created this repository for my own convenience, because I wanted to _set up APIs for mobile apps and React apps very fast_. Feel free to use this repository to work fast (or even learn from it if you are newer to Django). If you want to help me and improve this repository, I would greatly appreciate pull requests and suggestions :) Thank you for your advice in advance! Best way too reach me for questions, advice or suggestions is through [Twitter](https://twitter.com/Geromekevin).

### What is included?

This repository provides a _basic Rest API_ that includes a _custom User model,_ _basic authentication routes_ and a _Facebook social authentication_ out of the box utilising various great packages like [djangorestframework](http://www.django-rest-framework.org/), [django-allauth](https://github.com/pennersr/django-allauth), [django-authtools](https://github.com/fusionbox/django-authtools), [django-model-utils](https://github.com/jazzband/django-model-utils) and [django-rest-auth](https://github.com/Tivix/django-rest-auth). Please read through their respective repositories for trouble shooting and learning.
It also follows the _project layout_ from the book ["Two Scoops of Django 1.11"](https://www.twoscoopspress.com/products/two-scoops-of-django-1-11), which makes it _easy to collaborate_. (Make sure to check that book out if you are a beginner in Django and want to take your Django skills to the next level! At this point a _big thank you to Audrey and Daniel Roy Greenfeld_ for their amazing work.)
Furthermore this project comes _staging and production settings tailored to AWS Elastic Beanstalk_, which makes it easy to host this project fast.
At the end of this README I will also provide some quick tips and tricks to help you host on AWS Elastic Beanstalk, which may help you, if you have never hosted there before. Let me know I was missing something so I can add it, or make a pull request with your additional instructions.
Additionally it has a _preconfigured .gitignore._
Last but not least it includes a handy _Makefile_ which was inspired by [this](https://github.com/kaleissin/django-makefile) old repository I found.

## Getting Started

Follow these instructions to set up this server on your local machine.

### Prerequisites

Make sure you have postgesql installed and know how to start a new database. Start a database, take note of the name, the user, the password, the host and the port to set your environment variables.
This project uses [redis-cache](https://niwinz.github.io/django-redis/latest/) for it's cache, so make sure you also have a redis instance running.
You will also need python3 with pip and should use virtualenv.

The recommended directory layout looks like this:

```
~/projects/myproject_project/
~/.envs/myproject/# virtualenv
```

which means for this repository to do it like this:

```
~/projects/DjangoBasicRESTAPI_project/
~/.envs/myproject/
```

When you are in `~/.envs/myproject/` you can start a virtual environment like this:

```
virtualenv -p python3 .
```

Following this structure, clone this github repository into `DjangoBasicRESTAPI_project`. Inside `DjangoBasicRESTAPI_project` (the `<repository_root>`), you will then have this layout:

```
<DjangoBasicRESTAPI_project>/
├── config/
│   ├── settings/
│   │   ├── aws/
│   │   │   ├── __init__.py
│   │   │   ├── conf.py
│   │   │   └── utils.py
│   │   ├── base.py
│   │   ├── local.py
│   │   ├── production.py
│   │   └── staging.py
│   ├── __init__.py
│   ├── urls.py
│   ├── api_urls.py
│   └── wsgi.py
├── <myproject>/
│   ├── accounts/  # App
│   ├── core/ # App
│   ├── media/ # Development only!
│   ├── static/
│   └── templates/
├── <requirements>/
├── .gitignore
├── Makefile
├── README.rst
├── manage.py
└── requirements.txt
```

If you chose this layout, you can activate your virtual environment from within `DjangoBasicRESTAPI_project` by typing:

```
source ~/.envs/DjangoBasicRESTAPI_project/bin/activate
```

### Installing:

After activating your virtual environment, install all the dependencies by running:

```
pip install -r requirements/local.txt
```

Note that the _awsebcli_ will automatically get installed!
Next set all the required environment variables for local development like this.

```
export SOME_SECRET_KEY=y0ur-sup3r-s3cr3t-k3y-l0l
export POSTGRES_NAME=y0ur-sup3r-s3cr3t-k3y-l0l
export POSTGRES_USERNAME=y0ur-sup3r-s3cr3t-k3y-l0l
export POSTGRES_PASSWORD=y0ur-sup3r-s3cr3t-k3y-l0l
export POSTGRES_HOST=y0ur-sup3r-s3cr3t-k3y-l0l
export POSTGRES_PORT=y0ur-sup3r-s3cr3t-k3y-l0l
```

If you are done setting the environment variables migrate to the database:

```
python manage.py migrate
```

Lastly create a super user:

```
python manage.py createsuperuser
```

## Working through the rest of the Todos

The code is marked with TODO comments. Go through them and insert your values for the respective code blocks.

## Setting up a social auth for Facebook

First go to your admin and create a new [site](https://docs.djangoproject.com/en/1.11/ref/contrib/sites/). Click on `sites` and add a new one and using `localhost:8000` for the inputs.
Next to https://developers.facebook.com/ and create an application. Take note of your `client ID` and your `client secret`. Go back to your admin and create a new `Social app`. Choose `Facebook` for the provider, and your `client ID` and your `client secret` and your `localhost:8000` site.
For testing, in `myproject/accounts/api/tests/test_views.py` set `test_facebook=True` and set your `client ID` and your `client secret` as environment variables and obtain a `access_token` from using the [Access Token Tool](https://developers.facebook.com/tools/accesstoken/). Set `self.access_token` in `myproject/accounts/api/tests/test_views.py` and run the tests (view below). Done.

## Running the tests and using the Makefile

To run tests simply type:

```
make test
```

To see how you configured your environment type:

```
make showenv
```

Note that this only works if you kept this projects structure. Otherwise modify the Makefile to your own needs.
You can see the coverage by using:

```
coverage report
```

## Tips for hosting on AWS using Elastic Beanstalk

Here are some tips I wished the docs would point out more clearly, which helped me host with AWS. These tips are probably not complete as I might have forgotten some steps. I just typed down all the struggles I remembered and how I fixed them. So if you go through this and
The basic action you will have to take first is to set up an AWS account. If you've done that, go to `Services` at the top of the navbar and look for _IAM_. Click on IAM and go through the first five security steps:

1.  Delete your root access keys
2.  Activate MFA on your root account
3.  Create individual IAM users
4.  Use groups to assign permissions
5.  Apply an IAM password policy

### Generating a ssh-key

You want to generate an [EC2 key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) and after you downloaded it. It is recommend to put it in a hidden folder: `~/.ssh/id_rsa`. You will also need to own it by running `chmod 400 ~/.ssh/id_rsa`.

### General hosting

Use `eb init` and `eb create` to host on AWS. Choose the ssh key generated earlier. I will not provide more details here, since these commands are super well documented. Make sure to read to take the time to read through [awsebcli documentation](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html).
You will need to set the follwoing environment variables (for production replace `staging` with `production`):

```
eb setenv DJANGO_SECRET_KEY=y0ur-sup3r-s3cr3t-k3y-l0l
eb setenv DJANGO_SETTINGS_MODULE=config.settings.staging
```

### Creating and adding a relational database to an environment on Elastic Beanstalk

In the browser click on Services and then on Elastic Beanstalk. Click on your application, and then on the environment for which you want to add a database. Click on configuration, then on database. Choose `postgres` for the engine and the latest available version for the engine version. Choose your instance class and storage size. Configure your username and password. For retention I recommend `Create snapshot`. For Availability choose Low. Then hit save. The creation of the database will take a few minutes. After the creation the database should work right away with the provided settings.

Using

```
eb ssh
```

you can connect to your instance. After connecting you will need to activate your virtual environment:

```
source /opt/python/run/venv/bin/activate
```

Next in this terminal set all your environment variables using the export syntax.

```
eb setenv DJANGO_SECRET_KEY=y0ur-sup3r-s3cr3t-k3y-l0l
eb setenv DJANGO_SETTINGS_MODULE=config.settings.staging
```

Afterwards navigate to your application:

```
cd /opt/python/bundle/<app-version>/app
```

and `python manage.py migrate`.

### Using Redis for cache

First generate an `ACCESS_KEY_ID` and a `SECRET_ACCESS_KEY`. In IAM click on users and choose the user you created for step 3. Click on Security credentials and then create an access key. Store it somewhere save and remember the values!
Next create a Redis instance using Amazon Elasticache. For instructions see [the docs](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/GettingStarted.html). They are quite good for this. Then set the following environment variables:

```
eb setenv ACCESS_KEY_ID=y0ur-sup3r-s3cr3t-k3y-l0l
eb setenv REDIS_LOCATION=y0ur-sup3r-s3cr3t-k3y-l0l
eb setenv SECRET_ACCESS_KEY=y0ur-sup3r-s3cr3t-k3y-l0l
```

Now you need to assign a Redis security group to an EC2 instance. This one was especially tricky to figure out, but once you know how to do it, it's easy.

1.  Click Services than choose Elasticache.
2.  Click on Redis.
3.  Look for the Redis instance that you want to access and click on the arrow to the right of it's name.
4.  In the drop down menu, note and remember the security group name.
5.  Click again on Services and choose EC2.
6.  Under network & security click on security groups.
7.  Click on the group with the Group ID of the security group of the Redis instance and add click on inbound and then edit.
8.  Add a custom TCP rule on port 6379 with access from anywhere.
9.  Click on EC2 Dashboard, choose your instance and right click on it.
10. Click network and then change security groups and assign the new security group.

No Django using the `REDIS_LOCATION` environment variable should be able to access the Redis instance.

### Creating an S3 bucket for static files

If you want to host your static files on AWS, keep the settings provided here, and make sure to set the environments variables:

```
eb setenv ACCESS_KEY_ID=y0ur-sup3r-s3cr3t-k3y-l0l
eb setenv SECRET_ACCESS_KEY=y0ur-sup3r-s3cr3t-k3y-l0l
eb setenv BUCKET_NAME=y0ur-sup3r-s3cr3t-k3y-l0l
```

For the actual creation of the bucket I can recommend [this tutorial](https://www.codingforentrepreneurs.com/blog/create-a-blank-django-project/) by Justin Mitchel / Coding For Entrepreneurs. Just the settings part of this tutorial are a little outdated.
After you created the bucket, connect to your instance using `eb ssh.` Repeat the steps to activate your virtual env and set all your secret keys. Then from within the `/opt/python/bundle/<app-version>/app` folder run:

```
python manage.py collectstatic
```
