"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Michal Szotkowski
email: michal.szotkowski@molnlycke.com
"""

import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse
import io
import re

def get_arguments():
    """
    Zpracování argumentů příkazového řádku.
    Ověří, že URL má správný formát a že název souboru má příponu '.csv'.
    """
    parser = argparse.ArgumentParser(description='Zpracování volebních výsledků.')
    parser.add_argument('url', type=str, help='URL adresa stránky s volebními výsledky')
    parser.add_argument('soubor', type=str, help='Název souboru pro uložení výsledků')

    args = parser.parse_args()
    
    # Regulární výraz pro ověření URL
    url_pattern = re.compile(r"https://www\.volby\.cz/pls/ps2017nss/ps32\?xjazyk=CZ&xkraj=\d+&xnumnuts=\d+")
    if not url_pattern.match(args.url):
        print("Chyba: URL musí odpovídat formátu 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=<číslo>&xnumnuts=<číslo>'.")
        sys.exit(1)

    # Ověření přípony souboru
    if not args.soubor.endswith('.csv'):
        print("Chyba: Název souboru musí mít příponu '.csv'.")
        sys.exit(1)
        
    return args

def fetch_page(url):
    """
    Načtení HTML stránky z dané URL.
    Vrací text HTML stránky.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Chyba při načítání stránky: {e}")
        sys.exit(1)
    return response.text

def parse_main_page(html):
    """
    Analyzuje hlavní stránku a vrací seznam odkazů na stránky s výsledky pro jednotlivé obce.
    """
    soup = BeautifulSoup(html, 'html.parser')
    odkazy = []
    for link in soup.find_all('a', href=True):
        # Pouze odkazy s šestimístným číslem
        if link.text.isdigit() and len(link.text) == 6:
            full_url = "https://www.volby.cz/pls/ps2017nss/" + link['href']
            odkazy.append((link.text, full_url))
    return odkazy

def parse_obec_page(html, kod_obce, strany, sloupce):
    """
    Analyzuje stránku obce a vrací data pro danou obec.
    Pokud je to první odkaz, nastaví názvy sloupců pro strany z druhé a třetí tabulky.
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Najdeme název obce z třetího <h3>
    h3_elements = soup.find_all('h3')
    if len(h3_elements) >= 3:
        obec_nazev = h3_elements[2].text.replace('Obec: ', '').strip()
    else:
        obec_nazev = "Neznámá obec"

    tabulky = soup.find_all('table')
    if len(tabulky) < 3:
        print(f"Chyba: Očekávané tabulky nebyly nalezeny na stránce pro obec {obec_nazev}.")
        return None

    tabulka1 = tabulky[0]

    radek_data = [kod_obce, obec_nazev]
    for radek in tabulka1.find_all('tr'):
        bunky = radek.find_all('td')
        if len(bunky) > 0:
            volici = bunky[3].text
            obalky = bunky[4].text
            platne = bunky[7].text
            radek_data.extend([volici, obalky, platne])

    # Pokud je to první odkaz, nastavíme názvy sloupců pro strany z druhé a třetí tabulky
    if not strany:
        for tabulka in tabulky[1:3]:
            for radek in tabulka.find_all('tr'):
                bunky = radek.find_all('td')
                if len(bunky) > 1:
                    strana = bunky[1].text.strip()
                    if len(strana) > 1 and strana not in strany:
                        strany.append(strana)
                        sloupce.append(strana)

    # Přidáme data z druhé a třetí tabulky
    for tabulka in tabulky[1:3]:
        for radek in tabulka.find_all('tr'):
            bunky = radek.find_all('td')
            if len(bunky) > 2:
                strana = bunky[1].text.strip()
                hlasy = bunky[2].text.strip()
                if len(strana) > 1:
                    radek_data.append(hlasy)

    return radek_data

def save_to_csv(seznam, sloupce, soubor):
    """
    Uloží data do CSV souboru s UTF-8 BOM a správným oddělovačem.
    """
    df = pd.DataFrame(seznam, columns=sloupce)
    with io.open(soubor, 'w', encoding='utf-8-sig', newline='') as f:
        df.to_csv(f, index=False, sep=';')

def main():
    """
    Hlavní funkce, která koordinuje celý proces:
    - Získání argumentů
    - Načtení hlavní stránky
    - Analýza hlavní stránky a získání odkazů na jednotlivé obce
    - Načtení a analýza stránek jednotlivých obcí
    - Uložení výsledků do CSV souboru
    """
    args = get_arguments()
    url = args.url
    soubor = args.soubor

    print(f"Stahuji data z vybraného URL: {url}")

    html = fetch_page(url)
    odkazy = parse_main_page(html)

    seznam = []
    sloupce = ['kód obce', 'název obce', 'voliči v seznamu', 'vydané obálky', 'platné hlasy']
    strany = []

    for kod_obce, odkaz in odkazy:
        obec_html = fetch_page(odkaz)
        radek_data = parse_obec_page(obec_html, kod_obce, strany, sloupce)
        if radek_data:
            seznam.append(radek_data)

    print(f"Ukládám do souboru: {soubor}")
    save_to_csv(seznam, sloupce, soubor)
    print("Hotovo.")

if __name__ == "__main__":
    main()