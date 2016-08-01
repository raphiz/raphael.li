# Fetch all pages...
# If local: Follow all links
# if remote:
#  -> Check status code 200
#  -> Check weather it's SSL - if not, try to connect.
# local links should not be absolute (eg. not http://raphael.li)

import os
from urllib.parse import urlparse
from urllib.parse import urljoin
from ghost import Ghost
from ghost.bindings import QImage
from PIL import Image, ImageChops, ImageDraw
from html.parser import HTMLParser


# The height is not important - for screenshots only
# TODO: Add support for multiple resolutions
resolutions = [(1024, 768)]  # , (800, 600), (350, 350)]
test_results = {'warning': 0, 'success': 0, 'error': 0}
screenshots_dir = '.screenshots'


def main():
    domain = 'raphael.li'
    production = True
    if os.getenv('LOCAL_TEST', 'FALSE') == 'TRUE':
        domain = 'localhost:4000'
        production = False

    ghost = Ghost()
    with ghost.start(ignore_ssl_errors=False) as session:

        # Request index
        page, extra_resources = session.open("http://"+domain)
        #
        # # Verify the redirects
        # if production:
        #     test('https redirect', extra_resources[0].headers['Location'] == 'https://raphael.li/')
        #     test('www redirect', extra_resources[1].headers['Location'] ==
        #          'https://www.raphael.li/')
        #     test('HSTS header', page.headers['Strict-Transport-Security'] ==
        #          'max-age=31536000; includeSubDomains; preload')
        #
        # test('status codes external resources', check_external_resouces, extra_resources)
        # screenshot(session, page.url)

        # TODO: validator


def check_external_resouces(extra_resources):

    for current in extra_resources:
        if current.http_status not in [200, 301]:
            print(current.url)
            return ('External resource {0} has invalid Status code: {1}!'
                    .format(current.url, current.http_status))
    return True


def test(name, test, *args):
    if not isinstance(test, bool):
        test = test(*args)
        if isinstance(test, str):
            error_detail = test
            test = False
    if test:
        success('Check: {0} - OK!'.format(name))
    else:
        error('Check: {0} - Failed: {1}'.format(name, error_detail))


def screenshot(session, url):
    approved_path = os.path.join(screenshots_dir, 'approved') + os.path.sep
    new_path = os.path.join(screenshots_dir, 'new') + os.path.sep
    diff_path = os.path.join(screenshots_dir, 'new') + os.path.sep
    path = urlparse(url).path.replace('/', '_')
    if not os.path.exists(approved_path):
        os.makedirs(approved_path)
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    if not os.path.exists(diff_path):
        os.makedirs(diff_path)

    for resolution in resolutions:
        session.set_viewport_size(*resolution)
        file_name = '{0}_{1}x{2}.png'.format(path, *resolution)
        image = session.capture_to(new_path + file_name)

        if not os.path.exists(approved_path + file_name):
            warning('No screenshot for {0} with resolution {1}'.format(url, resolution))
            continue

        # Compare new with approved screenshot
        approved = QImage()
        approved.load(approved_path + file_name)
        new = QImage()
        new.load(new_path + file_name)
        if new == approved:
            success('Check: Screenshot {0} with resolution {1} - OK!'.format(
                  url, resolution))
            continue
        try:
            diff = black_or_b(
                Image.open(approved_path + file_name),
                Image.open(new_path + file_name))

            diff.save(diff_path + file_name)
            error('Check: Screenshot {0} with resolution {1} - Failed: has changed! ({2}{3})'
                  .format(url, resolution, diff_path, file_name))
        except ValueError:
            error('Check: Screenshot {0} with resolution {1} - Failed: Image size does not match!'
                  .format(url, resolution))


def new_gray(size, color):
    img = Image.new('L', size)
    dr = ImageDraw.Draw(img)
    dr.rectangle((0, 0) + size, color)
    return img


def black_or_b(a, b, opacity=0.85):
    diff = ImageChops.difference(a, b)
    diff = diff.convert('L')
    # Hack: there is no threshold in PILL,
    # so we add the difference with itself to do
    # a poor man's thresholding of the mask:
    # (the values for equal pixels-  0 - don't add up)
    thresholded_diff = diff
    for repeat in range(3):
        thresholded_diff = ImageChops.add(thresholded_diff, thresholded_diff)
    h, w = size = diff.size
    mask = new_gray(size, int(255 * (opacity)))
    shade = new_gray(size, 0)
    new = a.copy()
    new.paste(shade, mask=mask)
    # To have the original image show partially
    # on the final result, simply put "diff" instead of thresholded_diff bellow
    new.paste(b, mask=thresholded_diff)
    return new

if __name__ == '__main__':
    main()
