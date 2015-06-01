FROM ruby

RUN apt-get update
RUN apt-get install -y node python-pygments
RUN gem install jekyll rdiscount kramdown

# Install lftp for deployment
RUN apt-get install lftp

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
RUN useradd --home /src -u 1000 -g 1000 -M jekyll
