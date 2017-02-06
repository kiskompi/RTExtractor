import splinter
import justext
import difflib


def difference(old_page_source: str, new_page_source: str) -> str:
    """This function differentiates the two strings given as parameters.

    """
    # TODO
    old_page_source = old_page_source.splitlines(True)
    new_page_source = new_page_source.splitlines(True)

    diff = difflib.unified_diff(old_page_source, new_page_source)

    return ''.join(diff)


def get_refreshment() -> str:
    """This function issues a new HTTP request by clicking on the "refresh" button saved by the get_refresh_button()
    function. """
    # TODO
    pass


def get_refresh_button():
    """This function saves the DOM elements of the page responsible for getting the new data, marked manually by the
    user. """
    # TODO
    pass


def run_extraction(urladdr: str):
    executable_path = {'executable_path': 'lib/chromedriver'}

    # chrome_options = selenium.webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("headless", headless)
    browser = splinter.Browser('chrome', **executable_path)
    browser.visit(urladdr)
    paragraphs = justext.justext(browser.html, justext.get_stoplist('English'))

    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            print(paragraph.text)

    results = [paragraphs]
    try:
        while True:
            new_paragraphs = get_refreshment()

            # ez a rész ideiglenesen justextet használ, ez még változhat - mivel a runtime generated oldalak legtöbbször
            # single page felépítésűek, ezért nem lehet "oldalanként" tanítani a Goldminert
            diff = difference(paragraphs, new_paragraphs)
            for paragraph in diff:
                if not paragraph.is_boilerplate:
                    print(paragraph.text)
            results.append(diff)
    except KeyboardInterrupt:
        pass


    f = open('results.txt')
    f.write(results)

run_extraction("https://twitter.com/hashtag/boycottbudwiser")
