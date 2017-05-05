# Bevezetés:

Az internet terjedésével egyre fontosabbá válik az a törekvés, hogy az ott fellelhető információ ne csak a felhasználók, hanem különböző szoftverek által is feldolgozható legyen. Ebből a célból jött létre a 2000-es évek elején a szemantikus web koncepciója, majd emiatt születtek meg a különböző tartalomkinyerési technológiák. A különböző célokra specializált tartalomkinyerő programok célja az, hogy a feladatuk szempontjából releváns információkat a lényegtelen információktól (ún. boilerplate) megtisztítva bányásszák ki a weboldalakból. Ilyen feladat lehet pl. a nyelvészeti célú felhasználás, illetve az információ kis méretű eszközökön jobban megjeleníthetővé tétele és a látássérültek számára készült képernyőolvasó programok által könnyebben feldolgozható formátumba történő alakítása.

A modern tartalomkinyerő rendszerek egyik legnagyobb kihívása, hogy képesek legyenek kibányászni az internet egyre nagyobb hányadát elfoglaló dinamikusan, futási időben generált weblapok releváns tartalmait. Ebbőn a szempontból a web rohamtempóban fejlődve maga mögött hagyta a webbányászatot, mivel annak csúcstechnológiát jelentő épviselői sem képesek ezen adatok teljes mértékű feldolgozására.

Jelen dolgozat célja, hogy röviden bemutassa a dinamikusan generált weblapok működésének alapjait, ismertesse atartalomkinyerés kihívásait ezen a területeén, és végül prezentáljon egy lehetséges megoldást a probléma kezelésére. Ilyen módon szűkíthető lenne a tartalomgenerálás- és kinyerés között utóbbi évtizedben kialakult technológiai rés.


# Részfeladatok:

- [x] Elmenteni a felhasználó klikkelését, ami megmutatja, melyik link lenyomásával lehet az új adatot behozni. - LearnigSetApp
- [ ] Képes legyen ezt az inputot megváltoztatni. - szabványos Json formátum használata az LSApp kimenetében.
- [ ] Az outputot olvasható formában tárolni. - az osztályozott linkek és feature-eik
- [ ] Monitorozza az oldalt, automatikus változásokat keresve. Ha az addig láthatatlan, user által adott GET link megjelenik, rákattint (így nem kell az egész oldalt újratölteni).
- [ ] Gépi tanuló API, aminek segítségével az algoritmus felhasználói beavatkozás nélkül tanulhatja a weblap működését.

# Működés:

## Összefoglaló:
A program a Selenium WebIDE szkriptfájljaiból nyeri az inputot. Ezt lekezelve hajtja végre az utasításokat, absztrahálva, hogy ne csak a konkrét elemeket, hanem az ugyanabba az osztályba kerülő elemeket is kezelni tudja. Ehhez kell egy klasszifikátor.

A klasszifikátor működjön úgy, hogy megnézi a klikkelt elemek classait, majd a hasonlóan viselkedőkét (pl amelyik nem töltött be új URL-t) egy csoportba gyűjti a viselkedésének megfelelően. Emellett mindenképp megpróbál lemenni az oldal aljára, akkor is, ha nincs ilyen interakció. Az alulra görgetést viszont nem csinálja a végtelenségig, mert elfogy a memória.


# Program működése:
1. Tanulóhalmaz létrehozása:
    1. Felhasználói interakcióval (Selenium WebIDE) használatával csoportosítja a linkeket. Ebből megtanulja az osztályozás szabályait, hogy aztán interakció nélkül tudja kezelni a többi letöltött oldalt.
        * tényleg kell a Selenium a tanuláshoz (vagy csak a végrehajtáshoz)?
        * elég egyelőre az Inspect tool a böngészőben, és kézzel megcsinálni a fájlt?
        * Inspect tool-> copy element -> bemásolni egy saját programba, ami összeállítja a fájlt 2 adat alapján:
            1. element forráskód
            2. user által megadott osztály
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

Csak a void linkek feldolgozásához kell seleniumot használni, a többi mehet URL alapján.

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


## Tehát:
1. Tanulóhalmaz - ebbe jön a felhasználói input, elmenti a szkriptfájlját.
2. Klasszifikátor - a szkriptfájlban lévő DOM elemeket absztrahálja annyira, hogy a weboldal bármelyik hasonló típusú elemére felismerje a böngésző.
3. Végrehajtó - ami a szkriptet a Python Selenium API-val végrehajtatja.

## Lehetséges absztrakciók az interkcióra képes dolgokra:
### SectionRevealButton
    * pl. fb more comment, twitter new posts, Index Mindeközben új hír gombok, ez új szekciót nyit ki ugyanezen az oldalon
### LanguageSelectionButton:
    * ha a gomb megnyomásával a tartalom nem, de a tartalom nyelve megváltozik. pl. euronews
### OuterPageHyperlink:
    * sima link
### SamePageHyperlink:
    * ugyanennek az oldalnak egy másik aloldalára mutató link

## Speciális esetek
Olyan esetek, amikkel nem, vagy máshogy kell foglalkozni. Azért kerültek be, mert lehet relevanciájuk, de nem feltétlen részei a dolgozathoz csatolt program problémahalmazának.
### PopUpSection
    - olyan, felhasználói interakciót igénylő oldalrész, ami blokkolja az oldal tartalmainak elérését. Kódszinten nem probléma, de a felhasználói interakció ami ezt kiiktatja értéktelen a crawlernek, ezért kiszűrendő. (interakció-boilerplate). lehet, hogy csak meg kéne mondani a felhasználóknak, hogy amikor ilyenre kattintsanak, addig állítsák le a felvételt, mert ronthatja a pontosságot/hatékonyságot/sebességet.
### ScrollDownLoader
    - ha lefele görget, akkor új tartalom jön be

Tehát: ismerje meg azokat a linkeket, melyek nem más URL-re irányítanak, hanem ezen az oldalon jelenítenek meg további tartalmakat. 
Ismerje fel azokat a lehetőségeket, melykor az oldal aljára görgetve új adatok töltődnek be. A felhasználói interakciókor a felugró div-ek még bezavarhatnak, de az automatizált crawling futásakor ez már nem szabad.

## Output:
Egy Json fájlba menti ki az tanulás eredményét, hogy újrafelhasználható legyen, kb. így:


## Új link tíus hozzáadása

Erre csak a forráskód módosításával van lehetőség. A következő részekre az element.py megfelelő kódsoraihoz új sorok beszúrásával lehet új típust felvenni:
```python
10 class CrawlerClass(Enum):
11    """
12    This class is an enumeration representing the classes which are the output
13    of the decision tree.
14    """
15    REVEAL = 1
16    INNER = 2
17    OUTER = 3
18    UNDET = 0
19    # Ide az új típust beszúrni 
```
```python
34    try:
35	if par == "SectionReveal":
36            return cls.REVEAL
37        elif par == "OuterPageLink":
38            return cls.OUTER
39        elif par == "InnerPageLink":
40            return cls.INNER
41        elif par == "UNDET" or par == "":
42            return cls.UNDET
43        else:
44            raise AttributeError("Bad value for CrawlerClass!")
45        # Ide az új típus és az annak megfelelő str ellenőrzésének beszúrása
```

Amit meg kell nézni: van-e bit.ly vagy goo.gl visszafejtő vagy valami hasonló.
## Python libraryk:
    - scikit-learn
    - Pandas

# Implementációs fázisok
##Példa Usecase:
1. Gép valami gépitanulással eldönti, hogy mit kell kattintani és mit nem.
2. Ember hasonlóan...
3. Kettőt összehasonlítva mérjük a gépi tanulás "erejét" az adott feladatra...

##Példa Usecase2:
1. Gép eldönti, hogy hova kell kattintani...
2. Ember átnézi és neki nem tetszik, ekkor belejavít...

##Példa Usecase3:
1. Ember valami minta alapján generáltat valami utasítás listát, hogy ide kell kattintani. (Kvázi Első usecase 2.-pont csak itt az ember is automatizáltan csinálná a dolgokat)
2. A program eszerint működik.

##További lehetőségek:

1. "Trollszűrő"
2. youtube commentek
3. euronews-szerű nyelvválasztó linkek osztályozása
4. kommentszekciók mutatása

