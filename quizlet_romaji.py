import requests
from bs4 import BeautifulSoup
import pyperclip

import romaji


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
URL = 'https://learnjapanesedaily.com/most-common-japanese-words.html/{}'


def fetch_from_page(page):

  response = requests.get(URL.format(page), headers={'user-agent': USER_AGENT}, timeout=5)
  soup = BeautifulSoup(response.text, 'html.parser')

  main_box = soup.find('div', 'entry-content')

  phrases = [definition.text for definition in main_box.find_all('p') if 'text-align:' not in str(definition)][1+int(page==1):]
  return phrases


def main():

  n = int(input('Enter number of phrases\n'))

  phrases = [phrase for page in range(1, 1+n//60) for phrase in fetch_from_page(page)]+(fetch_from_page(-(n//-60))[:n%60] if n%60 != 0 else [])

  pyperclip.copy('\n'.join((lambda parsed: romaji.romaji_to_hiragana(parsed[2][1:-1])+'\t['+romaji.hiragana_to_romaji(romaji.romaji_to_hiragana(parsed[2][1:-1]))+'] '+parsed[4])(phrase.split(' ', 4)) for phrase in phrases))



if __name__ == '__main__': main()
