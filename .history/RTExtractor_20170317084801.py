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

import json
from enum import Enum
from lxml.html import fromstring

class CrawlerClass(Enum):
    """
    enum representing the types of links
    """
    REVEAL = 1
    INNER = 2
    OUTER = 3

    @classmethod
    def str2cc(cls, par: str):
        """
        gets a string, returns the corresponding enum value
        """
        try:
            if par == "SectionReveal":
                return cls.REVEAL
            elif par == "OuterPageLink":
                return cls.OUTER
            elif par == "InnerPageLink":
                return cls.INNER
            else:
                raise AttributeError("Bad value for CrawlerClass!")
        except AttributeError as ex:
            print("Exception caught: " + repr(ex))

class Element:
    """
    a structure consisting of the HTML tag, HTML classes and the crawlerclass
    """

    def __init__(self, url: str, tag: str, html_class: list, crawler_class: CrawlerClass):
        self.url = url
        self.tag = tag
        self.html_class = html_class
        self.crawler_class = crawler_class

    @classmethod
    def json2element(cls, json_element):
        """
        Converts a json entry to Elements. Returns this element.
        """
        # data["url"], data["tag"], data["code"], data["class"]
        url = json_element["url"]
        tag = json_element["tag"]
        htelem = fromstring(str(json_element["code"]), create_parent=False)
        html_class = []

        for _ in range(0, len(htelem.classes)):
            html_class.append(htelem.classes.pop())

        html_class = html_class[1:]
        crawler_class = json_element["crawler_class"]

        return cls(url, tag, html_class, crawler_class)

    def print(self):
        """
        print
        """
        print("URL: "+self.url+"\ntag: "+self.tag
              +"\nclass: "+self.crawler_class)
        for i in self.html_class:
            print("HTML class: "+i)

class RTClassifier:
    """
    The classifier itself
    """
    def __init__(self):
        self.section_reveals = []
        self.outer_links = []
        self.inner_links = []

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

    def classify(self, elem: Element) -> str:
        """
        A felhasználói interakció alapján megtanult csoportosítással a bejárt oldal
        linkjeit, amiket az process_html() függvény adott neki egy vektorba
        rakva osztályokba rendezi:
        * SectionRevealButton,
        * OuterPageHyperlink,
        * SamePageHyperlink
        A visszatérési érték a learning set
        """
        return NotImplemented

    def reveal_all(self):
        """
        SectionReveaLButton osztályú linkjeit egy vektorban megkapja, majd sorban meghívja őket.
        """
        return NotImplemented

    def scroll_down(self):
        """
        Amikor a SectionReveal linkek elfogytak, az oldal aljára görget.
        * Ha nem töltődik be új tartalom: 3-as ponthoz.
        * Ha betöltődik, akkor újra vektorba rendezi a inkeket, de csak azokat a SectionReveaLButton
        típusúakat járja be, amik az előző vektorban nem voltak benne. Ezután vissza a 2-es ponthoz
        (újra legörget). X (kb. 5) legörgetés után abbahagyja, mert túl nagy lenne a memóriaigény.
        """
        return NotImplemented

    def crawl(self):
        """
        5.  Miután a legörgetést abbahagyhja, rámegy egy TraditionalHyperlinkButton típusú linkre,
        ami ugyanerre a beállítástül függően SamePage vagy OuterPage URL-osztályra mutat (pl.
        facebookról csak facebookra vagy csak kívülre).
        """
        return NotImplemented

    @classmethod
    def html2json(cls, code) -> str:
        """
        creates a json entry from the code of an  HTML element
        """
        print(code)
        return NotImplemented

    def process_html(self, document):
        """
        listázza az elemeket, classzifikálja (vagy elhagyja) őket, és berakja a megfelelő array-be
        """
        elements = fromstring(document)
        for i in elements:
            self.classify(Element.json2element(self.html2json(i)))

    def run(self):
        """
        runs the simulation via selenium or splinter API
        """
        return NotImplemented

# import_learning_set("learningset.json")