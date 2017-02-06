#Bevezetés:
Az internet terjedésével egyre fontosabbá válik az a törekvés, hogy az ott fellelhető információ ne csak a felhasználók, hanem különböző szoftverek által is feldolgozható legyen. Ebből a célból jött létre a 2000-es évek elején a szemantikus web koncepciója, majd emiatt születtek meg a különböző tartalomkinyerési technológiák. A különböző célokra specializált tartalomkinyerő programok célja az, hogy a feladatuk szempontjából releváns információkat a lényegtelen információktól (ún. boilerplate) megtisztítva bányásszák ki a weboldalakból. Ilyen feladat lehet pl. a nyelvészeti célú felhasználás, illetve az információ kis méretű eszközökön jobban megjeleníthetővé tétele és a látássérültek számára készült képernyőolvasó programok által könnyebben feldolgozható formátumba történő alakítása.

A modern tartalomkinyerő rendszerek egyik legnagyobb kihívása, hogy képesek legyenek kibányászni az internet egyre nagyobb hányadát elfoglaló dinamikusan, futási időben generált weblapok releváns tartalmait. Ebbőn a szempontból a web rohamtempóban fejlődve maga mögött hagyta a webbányászatot, mivel annak csúcstechnológiát jelentő épviselői sem képesek ezen adatok teljes mértékű feldolgozására.

Jelen dolgozat célja, hogy röviden bemutassa a dinamikusan generált weblapok működésének alapjait, ismertesse atartalomkinyerés kihívásait ezen a területeén, és végül prezentáljon egy lehetséges megoldást a probléma kezelésére. Ilyen módon szűkíthető lenne a tartalomgenerálás- és kinyerés között utóbbi évtizedben kialakult technológiai rés.

#Specifikáció:
Futásidőben generált weblapról automatikusan frissülő szöveggyőjteményt összeállító program.
##A futás menete:
1. Először text inputból vagy user interactionból megszerzi a DOM-elem nevét, amire kattintva a frissítést végzi.
2. Ezután betölti a weblapot, és kinyeri a betöltött oldal tartalmát.
3. Az eltárolt DOM elemre kattintva (ha az nem létezik akkor folyamatosan monitorozva és amint létrejött rákattintva) elindítja az új lekérést. Ez a MAIN LOOP
4. Az eredeti lekérés és az új lekérések tartalmát egyenként szűri, differenciálja és a differenciát elmenti egy fájlba.

#Részfeladatok:
* Elmenteni a felhasználó klikkelését, ami megmutatja, melyik link lenyomásával lehet az új adatot behozni.
* Képes legyen ezt az inputot megváltoztatni.
* Az inputot (a DOM-elemet, ami aktiválja az adatlekérést) szerkeszthető formában tárolni.
* Az outputot olvasható formában tárolni.
* Gépi tanuló API, aminek segítségével az algoritmus felhasználói beavatkozás nélkül tanulhatja a weblap működését.

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

#Kinda docu:
```python
def get_user_action():
    """This function captures the click of the user on the web page and stores it in a file."""
```
```
def change_user_action():
    """This function changes the file by a new interaction, or manual rewriting.
    Can call get_user_action()"""
```
```
def difference(old_page_source: list, new_page_source: list) -> str:
    """This function differentiates the two strings given as parameters.
```
```
def get_refreshment(browser: splinter.Browser) -> list:
    """This function issues a new HTTP request by clicking on the
    "refresh" button saved by the get_refresh_button() function.
```
```
def get_refresh_button():
    """This function saves the DOM elements of the page responsible
    for getting the new data, marked manually by the
    user. Calls get_user_action() or gets it from text input"""
```
```
def run_extraction(urladdr: str):
    """The main function, containing the initial GET request, the
    main loop and the output"""
```