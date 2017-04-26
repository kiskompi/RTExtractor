class CrawlerClass(Enum):
    """
    enum representing the types of links
    """
    REVEAL = 1
    INNER = 2
    OUTER = 3
    UNDET = 0

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
            elif par == "UNDET" or par == "":
                return cls.UNDET
            else:
                raise AttributeError("Bad value for CrawlerClass!")
        except AttributeError as ex:
            print("Exception caught: " + repr(ex))

class HTMLAttribute:
    """
    This class contains a standard or nonstandard HTML tag, with all of its values
    Fields:
    * name: az HTML attribute neve
    * values[]: a tag-hez tartozó értékek (a kódban whitespace-szel elválasztva)
    """
    
    def __init__(self, code: str):
        """
        \param code: \type str Az a html kódrészlet, amelyből a TagValueTuple előáll
        """
        # TODO
        pass

    def extract(code: str)

    
class Element:
    """
    a structure consisting of the HTML tag, HTML tags and their values and the crawlerclass
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
