# -*- coding: utf-8 -*-

from enum import Enum
import re
from typing import List

from lxml.html import fromstring


class CrawlerClass(Enum):
    """
    This class is an enumeration representing the classes which are the output
    of the decision tree.
    """
    REVEAL = 1
    INNER = 2
    OUTER = 3
    UNDET = 0

    @classmethod
    def str2cc(cls, par: str):
        """
        This function converts a string to a CrawlerClass enumeration value.
        Parameters
        ----------
        par : str
            The string which is hardcoded to the application. An unexpected
            value results in an AttributeError.
        Returns
        -------
        CrawlerClass
            Returns a copy of the CrawlerClass class.
        """
        try:
            if par == "SectionReveal":
                return cls.REVEAL
            elif par == "OuterPageLink":
                return cls.OUTER
            elif par == "InnerPageLink":
                return cls.INNER
            elif par == "UNDET" or par == "":
                return cls.UNDET
            else:
                raise AttributeError("Bad value for CrawlerClass!")
        except AttributeError as ex:
            print("Exception caught: " + repr(ex))


class CrawlElement:
    """
    A structure consisting of the HTML tag, HTML attributes and their values
    and the crawler class.
    Fields
    ------
        data:: _url
            The URL address where the HTML code fragment comes from.
        data:: _tag
            The type of the HTML element, such as ***div, span*** or ***a***
        data:: _attributes
            The standard and non-standard HTML attributes of the element. The keys are the names of
            the attributes, the values are, well, the values
        data:: _class
            The class of the element determined either by the gold
            standard or the decision tree
    """

    def __init__(self, url: str, name: str, attributes: dict, crawler_class: CrawlerClass):
        self._url = url
        self._tag = name
        self.crawl_class = crawler_class
        self._attributes = attributes

    @classmethod
    def json2element(cls, json_element):
        """
        Converts a json entry to Element. Basically a secondary constructor
        
        Parameters
        ----------
        json_element : dict
            The json element with key-value pairs where the ***key*** is the 
            name of the element and the ***value*** is the corresponding
            value.

        Returns
        -------
        Element
            Returns an element with the corresponding values.
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
        Prints the URL, the attribute-value pairs and the HTML class of
        the Element to the terminal
        """
        print("URL: " + self._url + "\ntag: " + self._tag
              + "\nclass: " + self._class.name)

    @classmethod
    def extract_name(cls, code: str) -> str:
        """
        This function gets an HTML code fragment like this:
        nonStandardAttr="value1 value2 value3"
        And returns the name of the attribute (in this case ***nonStandardAttr***)
        Parameters
        ----------
        code : str
            The HTML fragment, mined from the code of the element
        Returns
        -------
        str
            The name of the HTML attribute, such as ***div, span, a***
        """
        values = re.match(r'([\w]+)\s?=', code)
        values = values.group(1)

        return values

    @classmethod
    def extract_values(cls, code: str) -> List[str]:
        """
        This function gets an HTML code fragment like this:
        nonStandardAttr="value1 value2 value3"
        And returns the vector of the values of the attribute
        (in this case ***[value1, value2, value3]***)
        Parameters
        ----------
        code : str
            The HTML fragment, mined from the code of the element
        Returns
        -------
        str
            The name of the HTML attribute, Eg. the CSS selector classes and the href value
        """
        #
        values = re.match(r'\"\s?([\w\W\s]+)\s?\"', code)
        values = values.group(1)

        return values.split(" ")

    @classmethod
    def extract_attribute_list(cls, code: str) -> List[str]:
        """
        Extracts all of the code fragments containing attributes.
        :param code: An HTML code fragment of a single element, which contains zero or more HTML attributes.
        :return: A list of the extracted attribute code fragments. Each piece looks like this: Attr="value1
        value2 value3"
        """
        # \s([a-zA-Z]+=\"[\w\W]*\")
        return re.match(r'\s([a-zA-Z]+=\"[\w\W]*\")', code).group(1).split(" ")

    @classmethod
    def extract_tag(cls, code: str) -> str:
        # <([a-zA-Z0-9]).*>
        return re.match(r'<([a-zA-Z0-9]).*>', code).group(1)
