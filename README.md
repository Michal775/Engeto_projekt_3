# Engeto_projekt_3: Zpracování volebních výsledků

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
