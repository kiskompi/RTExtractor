# -*- coding: utf-8 -*-
"""
1. Tanulóhalmaz létrehozása:
    1. Felhasználói interakcióval (Selenium WebIDE) használatával csoportosítja
    a linkeket. Ebből megtanulja az osztályozás szabályait, hogy aztán
    interakció nélkül tudja kezelni a többi letöltött oldalt.
        * tényleg kell a Selenium a tanuláshoz (vagy csak a végrehajtáshoz)?
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

from enum import Enum
from splinter import Browser
from lxml.html import fromstring
from bs4 import BeautifulSoup
import re

import element.py

class RTClassifier:
    """
    This class is responsible for the classification of the HTML elements and for
    acting the accordingly to these elements.
    Fields
    ------
    _section_reveals : list
        The list of links with the crawlerClass type: REVEAL 
    _outer_links : list
        The list of links with the crawlerClass type: section_reveal
    _inner_links : list
        The list of links with the crawlerClass type: section_reveal
    _url : list
    """
    def __init__(self, crawl_target: str, url: str):
        self._section_reveals = []
        self._outer_links = []
        self._inner_links = []
        self._url = url

        try:
            if crawl_target == "INNER":
                self.target = "INNER"
            elif crawl_target == "OUTER":
                self.target = "OUTER"
            else:
                raise AttributeError("Bad value for RTClassifier::crawl_target! " +
                                     "You should use either \"INNER\" or \"OUTER~")
        except AttributeError as ex:
            print("Exception caught: " + repr(ex))
        self.target = crawl_target

    def import_learning_set(self, file):
        """
        Imports the learning set and returns it to a vector of objects. Gets the HTML code of the
        element and the crawler class. Result is a vector in
        element[HTMLclass[], HTMLtag, crawlerClass]
        """
        with open(file) as data_file:
            data = json.load(data_file)
            elem = Element.json2element(data)
            elem.print()

    def classify(self, elem: Element):
        """
        A felhasználói interakció alapján megtanult csoportosítással a bejárt oldal
        linkjeit, amiket az process_html() függvény adott neki egy vektorba
        rakva osztályokba rendezi:
        * SectionRevealButton,
        * OuterPageHyperlink,
        * SamePageHyperlink

        BERAKJA A DÖNTÉSI FÁBA AZ IGÉNYELT FORMÁTUMBAN
        """
        # TODO
        return NotImplemented

    def reveal_all(self, browser: Browser):
        """
        SectionReveaLButton osztályú linkjeit egy vektorban megkapja, majd sorban meghívja őket.
        """
        for rev in self.section_reveals:
            # splinter vagy selenium click on this type of elements
            print(rev)
            filtered = []
            for hclass in rev.html_class:
                # finds the elements which have ALL of the HTML classes listed in Element.html_class
                filtered = browser.find_by_css(hclass)

            for filtered_rev in filtered:
                browser.click(filtered_rev)

    def scroll_down(self, browser: Browser):
        """
        Amikor a SectionReveal linkek elfogytak, az oldal aljára görget.
        * Ha nem töltődik be új tartalom: 3-as ponthoz.
        * Ha betöltődik, akkor újra vektorba rendezi a inkeket, de csak azokat a SectionReveaLButton
        típusúakat járja be, amik az előző vektorban nem voltak benne. Ezután vissza a 2-es ponthoz
        (újra legörget). X (kb. 5) legörgetés után abbahagyja, mert túl nagy lenne a memóriaigény.
        """
        prior = 0
        for _ in range(0, 10):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            current = len(browser.execute_script("return document.documentElement.outerHTML;"))
            if current == prior:
                return
            prior = current

    def crawl(self, browser: Browser):
        """
        5.  Miután a legörgetést abbahagyhja, rámegy egy TraditionalHyperlinkButton típusú linkre,
        ami ugyanerre a beállítástül függően SamePage vagy OuterPage URL-osztályra mutat (pl.
        facebookról csak facebookra vagy csak kívülre).
        """
        # TODO
        # melyik linkre menjen rá?
        return NotImplemented

    def html2element(self, code: str) -> str:
        """
        creates a json entry from the code of an  HTML element
        """
        soup = BeautifulSoup(code, "lxml")
        # tag = soup.name vagy REGEX
        # [a-zA-Z0-9]*
        # crawl_class  UNDEFINED
        matches = re.match(r'^<\w+', code)
        tag = matches.group(1)
        print(soup.name)
        html_classes = soup.contents[0].get('class') # a klasszok vektora
        elem = Element(self.url, tag, html_classes, "")
        return elem

    def process_html(self, browser: Browser):
        """
        listázza az elemeket, classzifikálja (vagy elhagyja) őket, és berakja a megfelelő array-be
        """
        elements = fromstring(browser.html)
        for i in elements:
            self.classify(self.html2element(i))

    def run(self):
        """
        runs the simulation via selenium or splinter API
        """
        browser = Browser("chrome")
        browser.visit(self.url)
        self.process_html(browser)
        self.reveal_all(browser)
        self.scroll_down(browser)
        self.crawl(browser)

# import_learning_set("learningset.json")

CLSSFR = RTClassifier("INNER", "https://twitter.com/search?data_id=tweet%3A842698283604557824&f=tweets&vertical=default&q=Trump&src=tren")
CLSSFR.run()
