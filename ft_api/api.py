import os
import json

import requests
import pandas as pd
import getpass
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime

#from finnomena_api.keys import keys

class fintimesAPI:
    def __init__(self):
        #self.keys = keys
        pass

    def get_fund_list(self):
        pass

    def search(self, search, country=None, asset_class=None):
        """
        A function to perform searching


        """
        
        # --------------------------------------------------------------------------------------
        # Check
        # --------------------------------------------------------------------------------------

        # check search
        if not search or search.isspace():
            raise ValueError("Please provide a name, partial name or symbol to search.")

        url = 'https://markets.ft.com/data/search'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        countries = soup.find(class_='o-forms__select mod-ui-form__select--event mod-search-app__country')
        countries = [country.text.lower() for country in countries.findAll('option')[1:]]

        sec_types = soup.find(class_='o-forms__select mod-ui-form__select--event mod-search-app__type')
        sec_types = [sec_type.text.lower() for sec_type in sec_types.findAll('option')[1:]]

        # Check if input country is valid
        if (country is not None) and (country not in countries):
            raise ValueError('Input country is not valid, please check the spelling. Available countries are: ' + \
                ', '.join(countries))
        # Check if input asset_class is valid
        if (asset_class is not None) and (asset_class not in sec_types):
            raise ValueError('Input asset_class is not valid, please check the spelling. Available asset classes are: ' + \
                ', '.join(sec_types))

        # --------------------------------------------------------------------------------------
        # Start searching
        # --------------------------------------------------------------------------------------
    
        payload = {
            'query': search,
            'country': country,
            'assetClass': asset_class
        }

        page = requests.get(url, params=payload)
        soup = BeautifulSoup(page.content, 'html.parser')
        search = soup.find(class_='mod-ui-table mod-ui-table--freeze-pane')

        if search is None:
            return None

        search = search.find('tbody')
        search = search.findAll('tr')

        result_dicts = []
        for result in search:
            atts = result.findAll(class_='mod-ui-table__cell--text')
            sec_name = atts[0].text
            isin = atts[1].text

            result_dicts.append({'sec_name':sec_name, 'isin':isin})

        return result_dicts
    
    def get_fund_summary(self, isin):

        url = 'https://markets.ft.com/data/funds/tearsheet/summary'
        payload = {'s': isin}
        page = requests.get(url, params=payload)
        soup = BeautifulSoup(page.content, 'html.parser')
        profile = soup.find(class_='mod-ui-table mod-ui-table--two-column mod-profile-and-investment-app__table--profile')
        atts = {}
        for att in profile.findAll('tr'):
            key = att.find('th').text
            value = att.find('td').text
            atts[key] = value
        
        return atts
    
    def select_fund(self, fund_list, n=1, income_treatment='accumulation', currency='usd',launch_date='oldest'):
        currency = currency.upper()
        income_treatment = income_treatment.capitalize()

        for i, fund in enumerate(fund_list):
            summary = self.get_fund_summary(fund['isin'])
            summary = {k: summary[k] for k in ['Income treatment', 'Launch date', 'Price currency']}
            d = datetime.strptime(summary['Launch date'], '%d %b %Y')
            summary['Launch date'] = d.strftime('%Y-%m-%d')
            fund_list[i] = {**fund, **summary}
        
        df = pd.DataFrame(fund_list)
        
        selection = df.loc[(df['Income treatment']==income_treatment) & (df['Price currency']==currency)]
        if launch_date == 'oldest':
            ascending = True
        elif launch_date == 'newest':
            ascending = False
        selection = selection.sort_values(by='Launch date', ascending=ascending)

        selection = selection.iloc[:n]
        selection = selection.to_dict('records')

        return selection
    
    def search_select_fund(self, search, country=None, asset_class=None,n=1, income_treatment='accumulation', currency='usd',launch_date='oldest'):
        fund_list = self.search(search)
        selection = self.select_fund(fund_list)
        return selection
    
    def get_fund_historical(self, isin):
        

        

    

api = fintimesAPI()
#print(api.search("ubs equity china opportunity"))
#print(api.search("ubs equity fund china opportunity"))
#print(api.get_fund_summary('LU2000522420:EUR'))
df = api.select_fund(api.search("ubs equity fund china opportunity"))
print(df)

            
