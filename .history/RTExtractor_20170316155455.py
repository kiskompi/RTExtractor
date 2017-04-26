# -*- coding: utf-8 -*-
""" 
A felhasználói interakció alapján megtanult csoportosítással a bejárt oldal linkjeit osztályokba rendezi: 
    * SectionRevealButton, 
    * OuterPageHyperlink, 
    * SamePageHyperlink
3. SectionReveaLButton osztályú linkjeit vektorokba rakja, majd sorban meghívja őket.
4. Amikor a SectionReveal linkek elfogytak, az oldal aljára görget. 
    * Ha nem töltődik be új tartalom: 3-as ponthoz.
    * Ha betöltődik, akkor újra vektorba rendezi a inkeket, de csak azokat a SectionReveaLButton típusúakat járja be, amik az előző vektorban nem voltak benne. Ezután vissza a 2-es ponthoz (újra legörget). X (kb. 5) legörgetés után abbahagyja, mert túl nagy lenne a memóriaigény.
5.  Miután a legörgetést abbahagyhja, rámegy egy TraditionalHyperlinkButton típusú linkre, ami ugyanerre az URL-osztályra mutat (pl facebookról csak facebookra).

"""

import splinter

