import os
import json

import requests
import pandas as pd
import getpass
import numpy as np
from bs4 import BeautifulSoup

#from finnomena_api.keys import keys

class finnomenaAPI:
    def __init__(self):
        #self.keys = keys
        pass

    def get_fund_list(self):
        pass

    def search(self, search):
        """
        A function to perform searching


        """
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        }
        data = {
        'search_text': search
        }
        response = requests.post('https://www.investing.com/search/service/searchTopBar', headers=headers, data=data)

        if not response.ok:
            raise Exception("Oops... something wrong during search")

        search = response.json()
        if len(search) == 0:
            raise ValueError("search is empty")

        if search['total']['quotes'] == 0:
            return None
        
        quotes = search['quotes']
        df = pd.DataFrame(quotes)

        return df
            


    # def get_fund_info(self, sec_name):
    #     """
    #     A function to get basic information of a given fund. The informations are:
    #     1. the code name of the fund
    #     2. fund's ID in morningstar.com
    #     3. it's feeder fund (if any)
    #     4. the fees (e.g. purchase fee, redemption fee, management fee, etc)

    #     **This function does NOT require logging in.**

    #     Args:
    #         sec_name (str): the fund's code name (e.g. KT-WTAI-A, TMBCOF)
        
    #     Returns:
    #         info (dict): dictionary containing the fund's information

    #     """
    #     sec_name = str(sec_name)

    #     info = {}
    #     fund_url = self.keys['url']['fund'] + '/' + sec_name
    #     page = requests.get(fund_url)

    #     soup = BeautifulSoup(page.content, 'html.parser')

    #     sec_name_found = soup.find(id='sec-name')
    #     if sec_name_found is None:
    #         raise ValueError("Cannot find fund with name '" + sec_name_found + "'. Check the list of available funds by method get_fund_list() or make sure fund's code name is spelled correctly")
    #     sec_name_found = sec_name_found.text

    #     feeder_fund = soup.find(class_='feeder-fund')
    #     if feeder_fund is None:
    #         feeder_fund = None
    #     else:
    #         feeder_fund = feeder_fund.text

    #     mstar_id = soup.find(id='sec-id').text

    #     info['security_name'] = sec_name_found
    #     info['morningstar_id'] = mstar_id
    #     info['feeder_fund'] = feeder_fund
    #     # ----------------------------------------------------------------
    #     payload = {'fund':mstar_id}
    #     other_info = requests.get('https://www.finnomena.com/fn3/api/fund/nav/latest', params=payload).json()
    #     info['nav_date'] = other_info['nav_date']
    #     info['current_price'] = other_info['value']
    #     info['total_amount'] = other_info['amount']
    #     info['d_change'] = other_info['d_change']
    #     # ----------------------------------------------------------------

    #     fee_url = 'https://www.finnomena.com/fn3/api/fund/public/' + mstar_id + '/fee'
    #     fees_list = requests.get(fee_url).json()['fees']

    #     fees = {v:None for v in self.keys['fees_dict'].values()}
    #     for i in fees_list:
    #         if i['feetypedesc'] in self.keys['fees_dict']:

    #             try:
    #                 amount = float(i['actualvalue'])
    #             except:
    #                 amount = np.nan

    #             fees[self.keys['fees_dict'][i['feetypedesc']]] = amount
    #     # ----------------------------------------------------------------

    #     info = {**info, **fees}

    #     return info

    # def get_fund_price(self, sec_name: str, time_range = 'MAX'):
    #     """
    #     A function to get historical price of a given fund.

    #     **This function does NOT require logging in.**

    #     Args:
    #         sec_name (str): the fund's code name (e.g. KT-WTAI-A, TMBCOF)
    #         time_range (str, optional): time frame to get the fund's price. 
    #                                     E.g. setting time_range = '1Y' will return the price of the fund since a year ago until today. 
    #                                     If not given, it will return all of the available data (price since inception)
        
    #     Returns:
    #         price (pandas.Dataframe): a dataframe of fund's price in timeseries 

    #     """
    #     sec_name = str(sec_name)
    #     time_range = str(time_range)

    #     info = self.get_fund_info(sec_name)
    #     mstar_id = info['morningstar_id']

    #     # Validate time_range (available options are 1D, 7D, 1M, 3M, 6M, 1Y, 3Y, 5Y, 10Y and MAX)
    #     time_range_option = ['1D', '7D', '1M', '3M', '6M', '1Y', '3Y', '5Y', '10Y', 'MAX']
    #     if time_range not in time_range_option:
    #         raise ValueError('time_range is not valid. The options are ' + ', '.join(time_range_option))

    #     payload = {'range':  time_range,
    #                'fund': mstar_id}
    #     url = self.keys['url']['fund_timeseries_price']
    #     temp_data = requests.get(url, params=payload).json()

    #     data = {'date':[], 'price':[]}
    #     for i in temp_data:
    #         data['date'].append(i['nav_date'])
    #         data['price'].append(i['value'])
        
    #     price = pd.DataFrame(data)

    #     return price

    

api = finnomenaAPI()
print(api.search("ubs equity china opportunity"))

            
