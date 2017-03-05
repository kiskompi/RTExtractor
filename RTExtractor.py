# -*- coding: utf-8 -*-
""" TODO PLACEHOLDER module docstring """
import splinter
import justext
import difflib


def get_user_action():
    """
    This function captures the click of the user on the web page and stores it in a file.
    """


def change_user_action():
    """
    This function changes the file by a new interaction, or manual rewriting.
    """


def difference(old_page_source: list, new_page_source: list) -> str:
    """
    This function differentiates the two strings given as parameters.
    :type old_page_source: list
    :type new_page_source: list
    """
    # TODO
    old_clear = ""
    new_clear = ""

    for paragraph in old_page_source:
        if not paragraph.is_boilerplate:
            old_clear += str(paragraph.text)

    for paragraph in new_page_source:
        if not paragraph.is_boilerplate:
            new_clear += str(paragraph.text)

    diff = difflib.unified_diff(old_clear, new_clear)

    return ''.join(diff)


def refresh(browser: splinter.Browser) -> str:
    """
    This function issues a new HTTP request by clicking on the "refresh" button
    saved by the get_refresh_button() function.
    :rtype: str
    :type browser: splinter.Browser
    """
    # TODO
    browser.reload()
    return browser.html


def run_extraction(urladdr: str):
    """
    The main function, containing the initial GET request, the main loop and the output
    """
    executable_path = {'executable_path': 'lib/chromedriver'}

    # chrome_options = selenium.webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("headless", headless)
    browser = splinter.Browser('chrome', **executable_path)
    browser.visit(urladdr)

    paragraphs = justext.justext(browser.html, justext.get_stoplist('English'))

    results_str = ""

    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            print(paragraph.text)
            results_str += paragraph.text
        else:
            print("BOILERPLATE:\n", paragraph.text)
    file = open('results.txt', 'w')
    results_str += str(browser.html)
    file.write(results_str)
    try:
        while True:
            new_paragraphs = justext.justext(refresh(browser), justext.get_stoplist('English'))

            # ez a rész ideiglenesen justextet használ, ez még változhat - mivel a runtime
            # generated oldalak legtöbbször
            # single page felépítésűek, ezért nem lehet "oldalanként" tanítani a Goldminert
            diff = difference(paragraphs, new_paragraphs)

            results_str += str(diff)
            # if diff != "" or diff is not None:
            file.write(diff)

    except KeyboardInterrupt:
        pass


run_extraction("https://twitter.com/hashtag/notmysuperbowlchamps?f=tweets&vertical=default&src=tren")
