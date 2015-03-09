FROM grahamc/jekyll

# Install assets plugin
RUN gem install jekyll-assets
RUN gem install jekyll-less
RUN gem install therubyracer
RUN gem install uglifier
RUN gem install jekyll-sitemap

# Add and use new user jekyll (working as root is not ideal...)
RUN useradd --home /src -u 1000 -M jekyll
USER jekyll
