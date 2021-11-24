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

  output = ('\n'.join((lambda parsed: (lambda old_romaji: (lambda hiragana: (lambda new_romaji:
                                                                             
    hiragana+f"\t[{old_romaji}{' / '+new_romaji if new_romaji != old_romaji else ''}]; {parsed[2]}"
                                                                             
  )(romaji.hiragana_to_romaji(hiragana)))(romaji.romaji_to_hiragana(old_romaji)))(parsed[1]))(re.split(' \(|\) : ', phrase, 2)) for phrase in phrases))

  print(output)
  pyperclip.copy(output)
  print('Copied to clipboard!')


if __name__ == '__main__': main()
