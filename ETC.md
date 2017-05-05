# == EXPERIMANTAL ==

# Észrevételek:
1. nem csak a classokat, hanem minden taget érdemes kibányászni a non-standard HTML miatt
2.

# Program működése:
1. Tanulóhalmaz létrehozása:
    1. A felhasználó manuálisan csoportosítja a releváns HTML elemeket. Ebből megtanulja az osztályozás szabályait, hogy aztán interakció nélkül tudja kezelni a többi letöltött oldalt.
        * tényleg kell a Selenium a tanuláshoz (vagy csak a végrehajtáshoz)?
    2. lehet hardcoded néhány feature (pl. URL domain része), azok alapján továbbtanulni
2. A felhasználói interakció alapján megtanult csoportosítással a bejárt oldal linkjeit osztályokba rendezi: 
    * SectionRevealButton, 
    * OuterPageHyperlink, 
    * SamePageHyperlink
3. SectionReveaLButton osztályú linkjeit vektorokba rakja, majd sorban meghívja őket.
4. Amikor a SectionReveal linkek elfogytak, az oldal aljára görget. 
    * Ha nem töltődik be új tartalom: 3-as ponthoz.
    * Ha betöltődik, akkor újra vektorba rendezi a inkeket, de csak azokat a SectionReveaLButton típusúakat járja be, amik az előző vektorban nem voltak benne. Ezután vissza a 2-es ponthoz (újra legörget). X (kb. 5) legörgetés után abbahagyja, mert túl nagy lenne a memóriaigény.
5.  Miután a legörgetést abbahagyhja, rámegy egy TraditionalHyperlinkButton típusú linkre, ami ugyanerre az URL-osztályra mutat (pl facebookról csak facebookra).

# Implementáció folyamata:
Mindig működő kis modulokat kell létrehozni, azokat egyemnként tesztelni:
1. Tanulóhalmaz létrehozása Selenium WebIDE segítségével - ez interaktív a user szempontjából.
    1. végigtakkintgatni felvétel módban
    2. ha lehet, Seleniummal Pop Up ablakot generáltatni, ebbe a link katergóriát bevihetővé tenni (sok manuális munka).
    3. a Selenium output fájlját könnyen feldolgozható és felhasználóbarát formára átírni (pl. YAML, LINK / URL, HTML\_CLASSES, GROUP\_TYPE)
2. Döntési fa létrehozása
    1. implementáció
    2. tanítás
    3. validáció
3. Crawler vagy Crawler API implementálása
4. Extractor API implementálása




== LEGACY ==
#Specifikáció:
Futásidőben generált weblapról automatikusan frissülő szöveggyőjteményt összeállító program.
##A futás menete:
1. Először text inputból vagy user interactionból megszerzi a DOM-elem nevét, amire kattintva a frissítést végzi.
2. Ezután betölti a weblapot, és kinyeri a betöltött oldal tartalmát.
3. Az eltárolt DOM elemre kattintva (ha az nem létezik akkor folyamatosan monitorozva és amint létrejött rákattintva) elindítja az új lekérést. Ez a MAIN LOOP
4. Az eredeti lekérés és az új lekérések tartalmát egyenként szűri, differenciálja és a differenciát elmenti egy fájlba.

#Felmerülő problémák:
1. A jelenlegi rendszerek (pl. Justext) nem alkalmazhatóak, mert a user contentet is boilerplatenek címkézik (nagy code/content ratio, kevés szöveg, kevés stopworddel). Ezt meg kell oldani egy átalakított, vagy új algoritmussal, ami:
    * Nem nézi a szöveg hosszát, vagy ha igen, rövidebbet is elfogad.
    * Nem nézi a code/content ratio-t (FONTOS).
    * STOPWORDöket csak osztályozásra/priorizálásra használja, nem bináris döntésre.
2. Az oldalak más-más módon kérik le az új adatot, ez csak oldalankénti tanulással, vagy felhasználói interakcióval deríthető ki, hogy működik.
    * A Twitter egy linkkel
    * Sok oldal (pl. Facebook) görgetéssel, vagy frissítéssel hozza le az új tartalmat.

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
    
    
    
    run_extraction("https://twitter.com/hashtag/notmysuperbowlchamps?f=tweets&vertical=default&src=tren")
