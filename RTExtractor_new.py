# -*- coding: utf-8 -*-
"""
1. Tanulóhalmaz létrehozása:
    1.A Gold Standard alapján csoportosítja a linkeket. Ebből megtanulja az osztályozás
    szabályait, hogy aztán interakció nélkül tudja kezelni a többi letöltött oldalt.
        * elég egyelőre az Inspect tool a böngészőben, és kézzel megcsinálni a fájlt?
        * Inspect tool-> copy element -> bemásolni egy saját programba,
        ami összeállítja a fájlt 2 adat alapján:
            1. element forráskód
            2. user által megadott osztály
    2. lehet hardcoded néhány feature (pl. URL domain része), azok alapján továbbtanulni
2. A felhasználói interakció alapján megtanult csoportosítással a bejárt oldal
linkjeit osztályokba rendezi:
    * SectionRevealButton,
    * OuterPageHyperlink,
    * SamePageHyperlink
3. SectionReveaLButton osztályú linkjeit vektorokba rakja, majd sorban meghívja őket.
4. Amikor a SectionReveal linkek elfogytak, az oldal aljára görget.
    * Ha nem töltődik be új tartalom: 3-as ponthoz.
    * Ha betöltődik, akkor újra vektorba rendezi a inkeket, de csak azokat a SectionReveaLButton
    típusúakat járja be, amik az előző vektorban nem voltak benne. Ezután vissza a 2-es ponthoz
    (újra legörget). X (kb. 5) legörgetés után abbahagyja, mert túl nagy lenne a memóriaigény.
5.  Miután a legörgetést abbahagyhja, rámegy egy TraditionalHyperlinkButton típusú linkre, ami
ugyanerre az URL-osztályra mutat (pl facebookról csak facebookra).
"""

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
    """
    def __init__(self, crawl_target: str, url: str, extractor):
        self._section_reveals = []
        self._outer_links = []
        self._inner_links = []
        self._clicked = []
        self._url = url
        self._extractor = extractor

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
    def is_stale(cls, elem) -> bool:
        try:
            elem.click()
            return False
        except (StaleElementReferenceException, ElementNotVisibleException):
            return True

    def reveal_all(self, browser: Browser, reveal_count: int):
        """
        Clicks on all of the links in the _section_reveals vector.
        Parameters
        ----------
        :param browser : Browser
            The Splinter Browser object which controls the browser which
            executes the called actions.
        :param reveal_count : int
            Maximises the number of the revealed links
        """
        print("REVEAL ALL")
        for revealer in self._section_reveals:
            # splinter or selenium click on this type of elements
            css_attrs = "." + ".".join((revealer['class'])).replace(" ", ".")

            for i in range(1, reveal_count):
                try:
                    elem_ls = browser.find_by_css(css_attrs)
                    if len(elem_ls) <= i:
                        continue
                    else:
                        if not self.is_stale(elem_ls[i]) and elem_ls[i] not in self._clicked:
                            print("Elem visible: {} - {}".format(elem_ls[i], elem_ls[i].visible))
                            inv = False
                            while not inv:
                                # it has to be here redundantly because slow JS can hide the elements
                                # before clicking but after last check
                                if elem_ls[i].visible:
                                    elem_ls[i].click()
                                    self._clicked.append(elem_ls[i])
                                    print("Element clicked")
                                inv = True
                except StaleElementReferenceException:
                    print("StaleElementReference")
                    continue

            # print(self._section_reveals.pop(0))
            # for elem in elem_ls:
            #    elem.click()
            #    print(elem)

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

    def place_in_vector(self, tag, tag_type):
        if tag_type == "REVEAL":
            self._section_reveals.append(tag)
        elif tag_type == "INNER":
            self._inner_links.append(tag)
        elif tag_type == "OUTER":
            self._outer_links.append(tag)

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
            if not isinstance(tag, NavigableString):
                if tag.has_attr('class'):
                    self.place_in_vector(tag, self.classify(tag['class']))

    @classmethod
    def print_paragraphs(cls, paragraphs):
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
                    self.reveal_all(browser, reveal)
                    self.print_paragraphs(self._extractor(browser.html, extr_param))
                    self.process_html(browser)
            else:
                self.reveal_all(browser, reveal)
                self.print_paragraphs(self._extractor(browser.html, extr_param))
                self.process_html(browser)
            # self.crawl(browser)
            print("Finished, quitting!")
            browser.quit()

# import_learning_set("learningset.json")

CLSSFR = RTClassifier("CLOSED",
                      'https://twitter.com/search?data_id=tweet%3A842698283604557824&f=tweets&vertical=default&q'
                      '=Trump&src=tren',
                      justext.justext)
param = justext.get_stoplist("English")
CLSSFR.run("firefox", scroll=5, reveal=10, repeat=False, extr_param=param)
