from besserwisser import Besserwisser, GhostClient
import logging

# By default:
# - Visits all local pages:
#       verify status code (can be configured (301, 200 by default))
#       verify  status codes for external links  (can be configured (301, 200 by default))
#       take a screenshot and compare it (for local pages only!)
#
# Configurable: "clients": with different resolutions / user agents / custom headers usw.
#   -> By default a "firefox" client with 1024x768 resolution
#

# Hooks - can be registered on http status codes, urls usw. (-> extension FW?)
# - Check HTTP redirects
# - Check HSTS headers
# - Check if external pages are linked https (if possible)


def main():
    setup_logging()
    besserwisser = Besserwisser(
        'http://raphael.li',
        hooks=[
            # htst_checker,
            # redirect_checker,
            # link_to_https_if_possible
        ],
        clients=[
            GhostClient('web', display=True, viewport_size=(1024, 768), user_agent='Mozilla/5.0 (Windows NT 6.2; WOW64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'),
            # GhostClient(width=360, height=640, user_agent='Mozilla/5.0 (Windows NT 6.2; WOW64) '
            #             'CHROME MOBILE'),
        ],
        config={
            'follow_links': ['www.raphael.li']
        },
        env={'name': 'ads'}
    )

    besserwisser.run()
    # besserwisser.report()


def htst_checker(besserwisser, response):
    # print("it works")
    return
    if response.url == 'http://raphael.li':
        # verify, HTST is not set
        pass

    if (response.url == 'https://www.raphael.li' or
       response.url.starswith('https://www.raphael.li')):
        #    Verify, HTST is set properly
        pass


def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(message)s')
    logger = logging.getLogger(__name__)
    logger.propagate = False


def redirect_checker(besserwisser, response):
    # TODO: check if the request is ....
    pass


def link_to_https_if_possible(besserwisser, response):
    # TODO:
    pass

if __name__ == '__main__':
    main()
