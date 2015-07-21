---
layout: post
title: Deploy your webapp with wercker's docker based stack
tags: docker
---

Since [Wercker](https://wercker.com/) introduced their [docker-based stack](http://blog.wercker.com/2015/04/02/Introducing-our-docker-stack.html) (also called "ewok"), deployment isn't as straigt forward as it used to be. 

I would like to share with you a strategy that I have developed for this website. I don't want to claim that this is the only or THE best way to deploy apps. Wercker might also add support for deployment steps to the ewok stack in the near future. This article describes how I deploy this static generated website over FTP. However, it should be pretty straigt-forward to adapt it to any kind of deployment you want.

I assume you have basic knowledge on what Wercker is and what it is good for. If you are not yet familiar with the differece between the old and the new wercker stack, checkout [their documentation](http://devcenter.wercker.com/docs/faq/migration-tips-v2.html).

In my particular case, I had a [static website](https://github.com/raphiz/raphael.li/) generated with [Jekyll](http://jekyllrb.com/). I used docker for development already with a very simple Dockerfile:

```docker
FROM ruby

RUN apt-get update
RUN apt-get install -y node python-pygments
RUN gem install jekyll rdiscount kramdown

# Install addons
RUN gem install jekyll-assets
RUN gem install jekyll-less
RUN gem install therubyracer
RUN gem install uglifier
RUN gem install jekyll-sitemap


# Working directory
RUN mkdir /src
WORKDIR /src

# Create new user jekyll - to prevent user id issues
RUN groupadd -g 1000 jekyll
```

I did also have wercker already set up for continuous deployment.

To get started, we have to write a script, that performs the deployment for us.
I prepared a script that deploys a jekyll generated site to a FTP target

<script src="https://gist.github.com/raphiz/a4d01ae4ca0d23d652f7.js"></script>

This deployment script requires `lftp`, so it must be installed in the docker container that we are using by adding the following line to our `DOCKERFILE`

```docker
# Install lftp for deployment
RUN apt-get update
RUN apt-get install lftp
```

Next, commit all the changes and push them to Github (or Bitbucket). 

TODO: add to wercker cfg.

That's all we have to do in the code itself. What

