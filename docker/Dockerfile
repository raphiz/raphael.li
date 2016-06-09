FROM ruby:2.3

RUN apt-get update
RUN apt-get install -y node

# Install lftp for deployment
RUN apt-get install lftp

# Install addons
RUN gem install jekyll
RUN gem install jekyll-assets
RUN gem install jekyll-sitemap
RUN gem install redcarpet
RUN gem install rouge
RUN gem install uglifier
RUN gem install therubyracer

# Working directory
RUN mkdir /src
WORKDIR /src

# Create new user jekyll - to prevent user id issues
RUN groupadd -g 1000 jekyll
RUN useradd --home /src -u 1000 -g 1000 -M jekyll
