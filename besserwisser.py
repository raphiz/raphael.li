import os
import logging
from contextlib import contextmanager
from collections import defaultdict
from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib.parse import urldefrag
from urllib.parse import urljoin

from ghost import Ghost


default_config = {
    'screenshots_dir': '.screenshots',
    'internal_acceptable_status_codes': [200, 301],
    'external_acceptable_status_codes': [200, 301],
    'follow_links': []
}

logger = logging.getLogger(__name__)


# TODO: propper logging!
class Besserwisser(object):
    def __init__(self, base_url, hooks=[], clients=[], config={}, env={}):
        self.base_url = base_url
        self.hooks = hooks
        self.clients = clients

        self.config = default_config.copy()
        self.config.update(config)
        self.config['follow_links'].append(urlparse(base_url).netloc)
        self.env = env
        # self.reporter = Reporter()

    def run(self):
        try:
            self._start()
            for client in self.clients:
                logger.debug('Running client {0}'.format(client.name))

                client.queue.add(self.base_url)
                while len(client.queue) > 0:
                    url = client.queue.pop()
                    try:
                        # TODO: for external links, fetch "basic" page
                        # TODO: consistent response object!
                        # TODO: make these abstractions - internal vs. external directly in the
                        # ghost client...
                        # response = urllib.request.urlopen('http://python.org/')
                        # html = response.getheader('a')

                        if self._is_internal(url):
                            logger.info('Fetching {0}'.format(url))
                            page, extra_resouces = client.fetch(url)
                            self._process_page(client, page)

                            # Also process all extra resources if it's an internal page

                            for resource in extra_resouces:
                                if resource.url not in client.visited:
                                    self._process_page(client, resource)
                    except TimeoutError:
                        logger.warning('Timeout for url {0}'.format(url))
        finally:
            self._stop()

    def _start(self):
        logger.debug('Starting clients...')
        for client in self.clients:
            logger.debug('Starting client {0}'.format(client.name))
            client.start()
            client.visited = set()
            client.queue = set()

    def _process_page(self, client, page):
        logger.debug('Processing Page {0}'.format(page.url))
        # TODO: assert status! (internal vs external!)
        if page.url in client.queue:
            client.queue.remove(page.url)
        client.visited.add(page.url)

        # TODO: screenshots!

        if self._is_internal(page.url):
            # TODO: check internal status code
            if page.headers['Content-Type'] == 'text/html':
                logger.debug('Extracting links from {0}'.format(page.url))
                parser = LinkHTMLParser(page.url)
                for link in parser.all_links(page.content):
                    if link not in client.visited and link not in client.queue:
                        client.queue.add(link)
            else:
                logger.debug('Skipping link extraction (no HTML) for {0} '.format(page.url))
        else:
            logger.debug('Skipping link extraction (external page) for {0} '.format(page.url))
            # TODO: check external status code

        self.call_hooks(page)

    def _is_internal(self, url):
        return urlparse(url).netloc in self.config['follow_links']

    def _stop(self):
        logger.debug('Stopping clients...')
        for client in self.clients:
            logger.debug('Stopping client {0}'.format(client.name))
            client.stop()

    def call_hooks(self, page):
        for hook in self.hooks:
            hook(self, page)

    def report(self):
        self.reporter.summary()
        return self.reporter


# TODO: try selenium....
class GhostClient(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.ghost = Ghost()
        self.params = kwargs
        self.session = None

    def start(self):
        self.session = self.ghost.start(**self.params)

    def fetch(self, url):
        # TODO: evtl. set_viewport_size
        return self.session.open(url)

    def stop(self):
        if self.session:
            self.session.exit()
        self.ghost.exit()


class Reporter(object):

    def __init__(self):
        self.test_results = defaultdict(int)

    def info(self, msg):
        print(msg)

    def skip(self, msg):
        print('\033[93m{0}\033[0m'.format(msg))
        self.test_results['skipped'] += 1

    def warning(self, msg):
        print('\033[93m{0}\033[0m'.format(msg))
        self.test_results['warning'] += 1

    def success(self, msg):
        print('\033[92m{0}\033[0m'.format(msg))
        self.test_results['success'] += 1

    def error(self, msg):
        print('\033[91m{0}\033[0m'.format(msg))
        self.test_results['error'] += 1

    def summary(self):
        print('\n\n{success} passed, {skipped} skipped, {warning} warnings, {error} errors'
              .format(**self.test_results))


class LinkHTMLParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.urls = set()

    def all_links(self, content):
        self.feed(content)
        return self.urls

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            url = None
            for attr_name, attr_value in attrs:
                if attr_name == 'href':
                    url, _ = urldefrag(urljoin(self.base_url, attr_value))
                    self.urls.add(url)
