# -*- coding: utf-8 -*-
"""
A program egy betanított döntési fa segítségével osztályozza egy megadott oldal elemeit.
Az osztályozás alapján bejárja azokat a linkeket, melyek az oldalon új adatokat jelenítenek
meg, valamint megpróbál az oldal aljára görgetéssel új adatot előhozni. A megadott számú,
vagy összes talált ilyen "Revealer" link bejárása után egy paraméter alapján az oldalon
talált, ugyanerre vagy más weblapra mutató linkek valamelyikén folytatja a kinyerést.
"""
import timeit

import splinter
from selenium.webdriver.common.keys import Keys
from splinter import Browser
import random
from bs4 import BeautifulSoup
from bs4 import NavigableString
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotVisibleException

import element
import dectree
import json
import justext


class RTClassifier:
    """
    This class is responsible for the classification of the HTML elements and for
    acting the accordingly to these elements.
    Fields
    ------
    _section_reveals : list
        The list of links with the crawlerClass type: crawlerClass.REVEAL
    _outer_links : list
        The list of links with the crawlerClass type: crawlerClass.OUTER
    _inner_links : list
        The list of links with the crawlerClass type: crawlerClass.INNER
    _url : str
        The URL of the homepage of the crawling. If the RTClassifier has
        the _target: CLOSED it will not click on links with other than this
        URL.
    _extractor
    _extract_time

    """
    def __init__(self, crawl_target: str, extract_contly: bool, url: str, extractor):
        self._section_reveals = []
        self._outer_links = []
        self._inner_links = []
        self._clicked = []
        self._closers = []
        self._url = url
        self._extractor = extractor
        self._extract_contly = extract_contly

        try:
            if crawl_target == "CLOSED" or crawl_target == "OPEN":
                self._target = crawl_target
            else:
                raise AttributeError("Bad value for RTClassifier::crawl_target! " +
                                     "You should use either \"CLOSED\" or \"OPEN~")
        except AttributeError as ex:
            print("Exception caught: " + repr(ex))
        self.target = crawl_target

    @classmethod
    def import_learning_set(cls, file):
        """
        Imports the learning set and converts it to a vector of objects.
        :param file : str
            The filename of the file which stores the learning set.
        :returns A vector of CrawlElement type objects
        """
        with open(file) as data_file:
            data = json.load(data_file)
            # FIXME
            elem = element.CrawlElement.json2element(data)
            elem.print()

    @classmethod
    def classify(cls, html_classes: list):
        """
        In this method the decision tree classifies a single HTML element to one of
        the four crawlerClass values. It also appends the classified element to the
        appropriate filed vector:
        * SectionRevealButton,
        * OuterPageHyperlink,
        * SamePageHyperlink

        This is where the decision tree is being used.
        :param html_classes : CrawlElement
            The element which will be classified by the function.
        """

        #   if dectree.DecTree().classify(html_classes) != "MISC":
        #       print(dectree.DecTree().classify("{} : classes {}".format(html_classes, html_classes)))

        return dectree.DecTree().classify(html_classes)

    @classmethod
    def find_by_css(cls, browser: Browser, css: str) -> list:
        """
        This function looks for a set of HTML elements based on their CSS classes.
        :param browser: The Splinter browser instance in which the page is opened.
        :param css: The css query to find the elements.
        :return: The list of the elements.
        """
        try:
            return browser.find_by_css(css)
        except splinter.exceptions.ElementDoesNotExist:
            print("Does not exist")

    @classmethod
    def is_stale(cls, elem) -> bool:
        """
        Checks whether the element is enabled (connected to the DOM and clickable) or not.
        :param elem: the element to check
        :return: True if clickable, False if not
        """
        try:
            # elem.click()
            elem.is_enabled()
            return True
        except (StaleElementReferenceException, ElementNotVisibleException):
            return False

    def click_on(self, elem) -> bool:
        """
        Clicks on the element and returns whether the click was successful or not.
        :param elem: The element to click on
        :return: True if successful, False if not
        """
        try:
            if elem not in self._clicked and elem.is_displayed():
                elem.click()
                return True
        except StaleElementReferenceException or ElementNotVisibleException:
            print("ElementInaccessible")
            return False

    @classmethod
    def js_click_on(cls, elem, browser: Browser) -> bool:
        """
        Clicks on the element via executing a Javascript query and returns whether the click was successful or not.
        :param elem: The element to click on
        :param browser: The Splinter Browser instance which will execute the query
        :return: True if successful, False if not
        """
        try:
            clss = elem.get_attribute("class")

            script_fh = "document.getElementsByClassName('"
            script_sh = "')[" + elem.get_attribute("class") + "].click()"
            script = script_fh + clss + script_sh
            script = ''.join([line.strip("\n") for line in script])

            print(script)
            browser.execute_script(script)
            return True
        except StaleElementReferenceException:
            return False

    def reveal_all(self, browser: Browser, reveal_count: int, extr_param=None):
        """
        Clicks on all of the links in the _section_reveals vector.
        Parameters
        ----------
        :param browser : Browser
            The Splinter Browser object which controls the browser which
            executes the called actions.
        :param reveal_count : int
            Maximises the number of the revealed links
        :param extr_param necessary parameters for the extractor, if needed
        """
        print("REVEAL ALL ", len(self._section_reveals))
        if reveal_count > len(self._section_reveals):
            reveal_count = len(self._section_reveals)

        browser.driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)

        for revealer in self._section_reveals:
            # splinter or selenium click on this type of elements
            revealer_css = "." + ".".join((revealer['class'])).replace(" ", ".")
            # print(revealer_css)

            revealer_css = revealer_css[:-1]
            reveal_ls = browser.driver.find_elements_by_css_selector(revealer_css)
            clicked = 0
            print("Section revealers: ", len(self._section_reveals))
            print("SR found: ", len(reveal_ls))

            # this function iterates through the elements found by css class
            for revealer_act in reveal_ls:
                    if self.is_stale(revealer_act):
                        # self.js_click_on(revealer_act)

                        if self.click_on(revealer_act):
                            clicked += 1
                            self._clicked.append(revealer_act)
                            print("Element clicked")
                            print("Clicked so far: ", clicked)
                            if clicked >= reveal_count:
                                print("Limit reached, reveal stopped")
                                return
                            else:
                                continue

                        # extr = "return $('" + revealer_css + " *:not(:has(\"*\"))')[0];"
                        # extr = ''.join([line.strip("\n") for line in extr])
                        # print(extr)
                        # text = browser.execute_script(extr)

                        # print(text)

                        # print("Section closers: ", len(self._closers))

                        # script_fh = "document.getElementsByClassName('"
                        # script_sh = "')[" + str(j) + "].click()"
                        # script = script_fh + closer_css + script_sh
                        # script = ''.join([line.strip("\n") for line in script])
                        # print(script)
                        # browser.execute_script(script)

                        if self._extract_contly:
                            self.print_paragraphs(self._extractor(browser.html, extr_param))
                            print("Extracting done")

                        for k in self._closers:
                            closer_css = "." + ".".join((k['class'])).replace(" ", ".")
                            closer_ls = browser.driver.find_elements_by_css_selector(closer_css)

                            for closer in closer_ls:
                                if self.click_on(closer):
                                    print("Closer clicked")
                                else:
                                    continue

    @classmethod
    def scroll_down(cls, browser: Browser, scrollnum: int):
        """
        This function scrolls to the bottom of the page. If this action results in getting more
        data then it scrolls again until no more data is loaded or the number of scrolls reaches
        an upper threshold. When new data is loaded it reruns the classification on the newly
        loaded elements. It finds these elements by differentiating between the previous and the
        current document source code.
        Parameters
        ----------
            :param browser : Browser
                The Splinter Browser object which controls the browser which
                executes the called actions.
            :param scrollnum : int
                Maximises the number of the scroll downs
        """
        prior = 0
        for _ in range(0, scrollnum):
            # noinspection PyAssignmentToLoopOrWithParameter
            for _ in range(0, scrollnum):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            current = len(browser.html)
            if current == prior:
                return
            prior = current

    def crawl(self, browser: Browser):
        """
        This function clicks on an element of the _inner_links or the _outer_links vector.
        If the RTClassifier has the _target set to "CLOSED" it only clicks on elements of
        the _inner_links vector.
        Parameters
        ----------
        :param browser : Browser
            The Splinter Browser object which controls the browser which
            executes the called actions.
        """

        if self._target == "CLOSED":
            for cl in random.choice(self._inner_links)['class']:
                if browser.is_element_present_by_css(cl):
                    browser.find_by_css(cl)[0].click()
        elif self._target == "OPEN":
            for cl in random.choice(self._inner_links)['class']:
                if browser.is_element_present_by_css(cl):
                    browser.find_by_css(cl)[0].click()
            # browser.find_by_css(random.choice(self._inner_links + self._outer_links)['class'][-1])[0].click()

    def place_in_vector(self, elem, elem_type):
        """
        Places the received element in one of the class vectors based on the type of these elements.
        :param elem: the HTML element which will be placed in these vectors
        :param elem_type: the type of the HTML element, the result of the classification
        """
        if elem_type == "REVEAL":
            # print("reveal: ", tag["class"])
            self._section_reveals.append(elem)
        elif elem_type == "INNER":
            # print("inner", tag["class"])
            self._inner_links.append(elem)
        elif elem_type == "OUTER":
            # print("outer", tag["class"])
            self._outer_links.append(elem)
        elif elem_type == "CLOSE":
            # print("closer", tag["class"])
            self._closers.append(elem)

    def process_html(self, browser: Browser):
        """
        Iterates through the HTML elements in the page. Calls the classify function for every
        element (which puts them in the right vector).
        Parameters
        ----------
        :param browser : Browser
            The Splinter Browser object which controls the browser which
            executes the called actions.
        """

        # elements = element.fromstring(browser.html)
        soup = BeautifulSoup(browser.html, "lxml")

        for tag in soup.find("body").descendants:
            if not isinstance(tag, NavigableString) and tag.has_attr('class'):
                    self.place_in_vector(tag, self.classify(tag['class']))

    @classmethod
    def print_paragraphs(cls, paragraphs):
        """
        This function handles the result of the data extractor algorithm.
        :param paragraphs: The result of the extraction
        """
        depend = open("results.txt", "a")
        for paragraph in paragraphs:
           if not paragraph.is_boilerplate:
               print("PARAGRAPH\n============\n"+paragraph.text, end="", file=depend)

    def run(self, browser_str, scroll: int = -1, reveal: int = -1, repeat: bool = True, extr_param=None):
        """
        This function calls the actions for every elements of the vectors of RTClassifier.
        It runs the browsing simulation via selenium or splinter API.
        Parameters
        ----------
        :param extr_param: additional parameters to the extractor algorithm (above the HTML source)
        :param repeat: determines whether the crawling runs in an infinite loop or not
        :param reveal: the maximum number of the revealed links. If not given there is no limit
        :param scroll:  the maximum number of the scroll downs.  If not given there is no limit
        :param browser_str: the name of the browser used to start the Splinter simulation
        """
        try:
            if browser_str == "chrome" or browser_str == "firefox" or browser_str == "zope.testbrowser":
                browser = Browser(browser_str)
            else:
                raise AttributeError("Browser not supported!")
        except AttributeError as ex:
            print("Exception caught: " + repr(ex))
            exit(1)
        else:
            browser.visit(self._url)
            self.scroll_down(browser, scroll)
            self.process_html(browser)
            if repeat:
                while True:
                    self.reveal_all(browser, reveal, extr_param)
                    self.print_paragraphs(self._extractor(browser.html, extr_param))
                    self.process_html(browser)
            else:
                self.reveal_all(browser, reveal, extr_param)
                self.print_paragraphs(self._extractor(browser.html, extr_param))
            self.crawl(browser)
            print("Finished, quitting!")
            browser.quit()


def nofunc(param1, param2):
    """
    The only function of this method is to be a placeholder for testing the framework without data extractors.
    :param param1: placeholder parameter
    :param param2: placeholder parameter
    :return:
    """
    pass


def execute():
    """
    It has to exist to make the time measurement possible via timeit
    :return:
    """
    CLSSFR = RTClassifier("CLOSED",
                          True,
                          'https://twitter.com/search?data_id=tweet%3A842698283604557824&f=tweets&vertical=default&q'
                          '=Trump&src=tren',
                          justext.justext)
    CLSSFR.run("firefox", scroll=5, reveal=10, repeat=False)

# Time measurement
# print(timeit.timeit("execute()", "from __main__ import execute", number=10))

execute()