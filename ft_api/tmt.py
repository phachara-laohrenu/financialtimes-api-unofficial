import requests
import pandas as pd
from bs4 import BeautifulSoup


# page = requests.get('https://markets.ft.com/data/search?query=ubs+equity+fund+china+opportunity&country=&assetClass=')
# soup = BeautifulSoup(page.content, 'html.parser')
# soup = soup.find(class_='o-forms__select mod-ui-form__select--event mod-search-app__country')
# soup = soup.findAll('option')

# result_dicts = []
# for result in soup:
#   print(result.text.lower())

a = 'as '
if not a or a.isspace():
  print('hi')
