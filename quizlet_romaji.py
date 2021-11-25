import requests
from bs4 import BeautifulSoup
import pyperclip
import re

import romaji


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
URL = 'https://learnjapanesedaily.com/most-common-japanese-words.html/{}'


def fetch_from_page(page):

  response = requests.get(URL.format(page), headers={'user-agent': USER_AGENT}, timeout=5)
  soup = BeautifulSoup(response.text, 'html.parser')

  main_box = soup.find('div', 'entry-content')

  phrases = [re.sub(r'(?<![0-9])\. .*|\n', ' ', phrase.text).rstrip(' ') for phrase in main_box.find_all('p') if re.search(r'^[0-9]+\. ', phrase.text)]
  return phrases


def main():

  n = int(input('Enter number of phrases (up to 1000)\n'))

  phrases = [phrase for page in range(1, 1+n//60) for phrase in fetch_from_page(page)]+(fetch_from_page(-(n//-60))[:n%60] if n%60 != 0 else [])

  output = ('\n'.join(

    (lambda number, old_kana, old_romaji, definition:

      (
        (lambda hiragana:
        (lambda new_romaji:
          f"{hiragana}\t[{old_romaji}{' / '+new_romaji if new_romaji != old_romaji else ''}]; {definition}"
        )(romaji.hiragana_to_romaji(hiragana))
        )(romaji.romaji_to_hiragana(old_romaji))
      )

      if not re.search(r'[ァ-ヴー]+', old_kana) else

      (
        (lambda new_romaji:
          f"{old_kana}\t[{new_romaji+' / ' if new_romaji != old_romaji else ''}{old_romaji}]; {definition}"
        )(re.sub(r'([aiueo])-', r'\1\1', old_romaji))
      )

    )(*re.split('\. | \(|\) : ', phrase, 3)) for phrase in phrases)
  )

  print(output)
  pyperclip.copy(output)
  print('Copied to clipboard!')
  

if __name__ == '__main__': main()
