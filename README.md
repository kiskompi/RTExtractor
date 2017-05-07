# Bevezetés:

Az internet terjedésével egyre fontosabbá válik az a törekvés, hogy az ott fellelhető információ ne csak a felhasználók, hanem különböző szoftverek által is feldolgozható legyen. Ebből a célból jött létre a 2000-es évek elején a szemantikus web koncepciója, majd emiatt születtek meg a különböző tartalomkinyerési technológiák. A különböző célokra specializált tartalomkinyerő programok célja az, hogy a feladatuk szempontjából releváns információkat a lényegtelen információktól (ún. boilerplate) megtisztítva bányásszák ki a weboldalakból. Ilyen feladat lehet pl. a nyelvészeti célú felhasználás, illetve az információ kis méretű eszközökön jobban megjeleníthetővé tétele és a látássérültek számára készült képernyőolvasó programok által könnyebben feldolgozható formátumba történő alakítása.

A modern tartalomkinyerő rendszerek egyik legnagyobb kihívása, hogy képesek legyenek kibányászni az internet egyre nagyobb hányadát elfoglaló dinamikusan, futási időben generált weblapok releváns tartalmait. Ebbőn a szempontból a web rohamtempóban fejlődve maga mögött hagyta a webbányászatot, mivel annak csúcstechnológiát jelentő épviselői sem képesek ezen adatok teljes mértékű feldolgozására.

Jelen dolgozat célja, hogy röviden bemutassa a dinamikusan generált weblapok működésének alapjait, ismertesse atartalomkinyerés kihívásait ezen a területeén, és végül prezentáljon egy lehetséges megoldást a probléma kezelésére. Ilyen módon szűkíthető lenne a tartalomgenerálás- és kinyerés között utóbbi évtizedben kialakult technológiai rés.


# Működés:

## Összefoglaló:
A program egy betanított döntési fa segítségével osztályozza egy megadott oldal elemeit. Az osztályozás alapján bejárja azokat a linkeket, melyek az oldalon új adatokat jelenítenek meg, valamint megpróbál az oldal aljára görgetéssel új adatot előhozni. A megadott számú, vagy összes talált ilyen "Revealer" link bejárása után egy paraméter alapján az oldalon talált, ugyanerre vagy más weblapra mutató linkek valamelyikén folytatja a kinyerést.  

# Program működése:
1. Tanulóhalmaz létrehozása:
    1. Felhasználó által adott tanulóhalmaz vagy referencia alapján csoportosítja a linkeket. Ebből megtanulja az osztályozás szabályait, hogy aztán interakció nélkül tudja kezelni a többi letöltött oldalt.
        * ez a referencia halmaz egyelőre a Firefox Inspection Tool-jával állítható össze. Így kell kibányászni a megfelelő elemek CSS class attribútumát.
        * a tanulóhalmaznak 2 dolgot kell tartalmaznia: az elem CSS class attribútumát és a felhasználó által megállapított osztályát.
2. A felhasználói interakció alapján megtanult csoportosítással a bejárt oldal linkjeit osztályokba rendezi: 
    * Revealer: az ugyanezen oldalon további adatokat letöltő linkek 
    * Outer: a jelenlegi weboldalról kifelé mutató linkek. 
    * Inner: a jelenlegi weboldalon belül új lapot megnyitó linkek
    * Closer: az oldal egyes részeit elérhetetlenné tevő (pl. megnyitott galéria) HTML-blokkokat bezáró oldalelemek
3. A Revealer osztályú linkjeit vektorokba rakja, majd sorban meghívja őket.
4. Amikor a Revealer linkek elfogytak, az oldal aljára görget. 
    * Ha nem töltődik be új tartalom: 3-as ponthoz.
    * Ha betöltődik, akkor újra vektorba rendezi a inkeket, de csak azokat a SectionReveaLButton típusúakat járja be, amik az előző vektorban nem voltak benne. Ezután vissza a 2-es ponthoz (újra legörget). X (kb. 5) legörgetés után abbahagyja, mert túl nagy lenne a memóriaigény.
5.  Miután a legörgetést abbahagyhja, rámegy egy Inner vagy Outer típusú linkre

## A modulok:
1. Tanulóhalmaz - ebbe jön a felhasználói input.
2. Klasszifikátor - a szkriptfájlban lévő DOM elemeket absztrahálja annyira, hogy a weboldal bármelyik hasonló típusú elemére felismerje a böngésző.
3. Végrehajtó - ami a szkriptet a Python Selenium API-val végrehajtatja.

## Lehetséges további absztrakciók az interkcióra képes dolgokra:
1. LanguageSelectionButton:
2. NextPageButton

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

