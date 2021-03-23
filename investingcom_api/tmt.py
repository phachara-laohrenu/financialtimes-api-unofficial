import requests
import pandas as pd
headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
}
data = {
  'search_text': 'ubs equity china oppor'
}
response = requests.post('https://www.investing.com/search/service/searchTopBar', headers=headers, data=data)
search = response.json()
print(search['quotes'])
print(pd.DataFrame(search['quotes']))