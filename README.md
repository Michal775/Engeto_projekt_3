# Engeto_projekt_3

Tento projekt je třetím projektem do Engeto Online Python Akademie.

## Popis projektu

Program stahuje volební výsledky z daného URL a ukládá je do CSV souboru.

## Instalace knihoven

Knihovny, které jsou použity v kódu jsou uložené v souboru `requirements.txt`. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:

    
    pip install -r requirements.txt
    

## Spuštění projektu

Spuštění souboru `Projekt_3.py` v rámci přík. řádku požaduje dva povinné argumenty.

    
    python Projekt_3.py <odkaz-uzemniho-celku> <vysledny-soubor>
    

Následně se vám stáhnou výsledky jako soubor s příponou `.csv`

## Ukázka projektu

Výsledky hlasování pro okres Ostrava:

  1. argument: `https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8106`
  2. argument: `vysledky_ostrava.csv`

Spuštění programu:

    python Projekt_3.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8106" "vysledky_ostrava.csv"

Průběh stahování:

    Stahuji data z vybraného URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8106
    Ukládám do souboru: vysledky_ostrava.csv
    Hotovo.

Částečný výstup:

    kód obce;název obce;voliči v seznamu;vydané obálky;platné hlasy;...
    569119;Čavisov;419;318;316;29;0;0;22;0;16;34;4;2;2;0;0;36;0;0;5;103;0;0;27;0;1;2;0;29;4
    506711;Dolní Lhota;1 202;904;899;95;2;0;69;0;31;41;9;3;2;1;1;90;0;0;25;356;0;2;65;0;6;7;0;91;3

