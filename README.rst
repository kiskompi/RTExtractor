#Bevezetés:
Az internet terjedésével egyre fontosabbá válik az a törekvés, hogy az ott fellelhető információ ne csak a felhasználók, hanem különböző szoftverek által is feldolgozható legyen. Ebből a célból jött létre a 2000-es évek elején a szemantikus web koncepciója, majd emiatt születtek meg a különböző tartalomkinyerési technológiák. A különböző célokra specializált tartalomkinyerő programok célja az, hogy a feladatuk szempontjából releváns információkat a lényegtelen információktól (ún. boilerplate) megtisztítva bányásszák ki a weboldalakból. Ilyen feladat lehet pl. a nyelvészeti célú felhasználás, illetve az információ kis méretű eszközökön jobban megjeleníthetővé tétele és a látássérültek számára készült képernyőolvasó programok által könnyebben feldolgozható formátumba történő alakítása.

A modern tartalomkinyerő rendszerek egyik legnagyobb kihívása, hogy képesek legyenek kibányászni az internet egyre nagyobb hányadát elfoglaló dinamikusan, futási időben generált weblapok releváns tartalmait. Ebbőn a szempontból a web rohamtempóban fejlődve maga mögött hagyta a webbányászatot, mivel annak csúcstechnológiát jelentő épviselői sem képesek ezen adatok teljes mértékű feldolgozására.

Jelen dolgozat célja, hogy röviden bemutassa a dinamikusan generált weblapok működésének alapjait, ismertesse atartalomkinyerés kihívásait ezen a területeén, és végül prezentáljon egy lehetséges megoldást a probléma kezelésére. Ilyen módon szűkíthető lenne a tartalomgenerálás- és kinyerés között utóbbi évtizedben kialakult technológiai rés.

#Specifikáció:
Futásidőben generált weblapról automatikusan frissülő szöveggyőjteményt összeállító program.

#Részfeladatok:
* Elmenteni a felhasználó klikkelését, ami megmutatja, melyik link lenyomásával lehet az új adatot behozni.
* Képes legyen ezt az inputot megváltoztatni.
* Az inputot (a DOM-elemet, ami aktiválja az adatlekérést) szerkeszthető formában tárolni.
* Az outputot olvasható formában tárolni.
* Gépi tanuló API, aminek segítségével az algoritmus felhasználói beavatkozás nélkül tanulhatja a weblap működését.

##Példa Usecase:
1) Gép valami gépitanulással eldönti, hogy mit kell kattintani és mit nem.
2) Ember hasonlóan...
3) Kettőt összehasonlítva mérjük a gépi tanulás "erejét" az adott feladatra...

##Példa Usecase2:
1) Gép eldönti, hogy hova kell kattintani...
2) Ember átnézi és neki nem tetszik, ekkor belejavít...

##Példa Usecase3:
1) Ember valami minta alapján generáltat valami utasítás listát, hogy ide kell kattintani. (Kvázi Első usecase 2.-pont csak itt az ember is automatizáltan csinálná a dolgokat)
2) A program eszerint működik.