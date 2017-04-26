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

import splinter
import json

class Element:
    """
    a structure consisting of the HTML tag, HTML classes and the crawlerclass
    """
    def __init__(self, tag, HTMLclass, crawlerClass):
        self.tag = tag
        self.html_class = HTMLclass
        self.crawler_class = crawlerClass

    def json2element(self, json_file):
        """
        Converts a json entry to Elements. Returns this element.
        """
        
def import_learning_set():
    """
    Imports the learning set and returns it to a vector of objects. Gets the HTML code of the
    element and the crawler class. Result is a vector in element[HTMLclass[], HTMLtag, crawlerClass]
    """
    pass

def define_crawler_class():
    """
    A felhasználói interakció alapján megtanult csoportosítással a bejárt oldal
    linkjeit, amiket az import_learning_set() függvény adott neki egy vektorba
    rakva osztályokba rendezi:
    * SectionRevealButton,
    * OuterPageHyperlink,
    * SamePageHyperlink
    """
    pass

def reveal_sections():
    """
    SectionReveaLButton osztályú linkjeit egy vektorban megkapja, majd sorban meghívja őket.
    """
    pass

def scroll_down():
    """
    Amikor a SectionReveal linkek elfogytak, az oldal aljára görget.
    * Ha nem töltődik be új tartalom: 3-as ponthoz.
    * Ha betöltődik, akkor újra vektorba rendezi a inkeket, de csak azokat a SectionReveaLButton
    típusúakat járja be, amik az előző vektorban nem voltak benne. Ezután vissza a 2-es ponthoz
    (újra legörget). X (kb. 5) legörgetés után abbahagyja, mert túl nagy lenne a memóriaigény.
    """
    pass

def crawl():
    """
    5.  Miután a legörgetést abbahagyhja, rámegy egy TraditionalHyperlinkButton típusú linkre, ami
    ugyanerre az URL-osztályra mutat (pl facebookról csak facebookra).
    """
    pass
