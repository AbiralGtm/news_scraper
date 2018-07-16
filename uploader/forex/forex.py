from bs4 import BeautifulSoup

from Firestore.Store import Store
from Util.Utility import Utility


class ForeignExchangeRate(object):
    def __init__(self):
        self.url = "https://www.nrb.org.np/fxmexchangerate.php"

    def get_data(self):
        content = Utility.get_source(self.url)
        soup = BeautifulSoup(content, 'html.parser')
        all_tr = soup.find_all('tr', {'bordercolor': ["#FFFFFF", "#999999"]})
        all_list = []
        for tr in all_tr:
            all_td = tr.find_all('td')
            try:
                int(all_td[1].text.strip())
                currency = all_td[0].text.strip().replace("\n", "").split(' ')
                result = {
                    'currency': currency[0] + " " + currency[-1],
                    'unit': int(all_td[1].text.strip()),
                    'buying': float(all_td[2].text.strip()),
                    'selling': float(all_td[3].text.strip())
                }
                all_list.append(result)
            except:
                print("")

        indian_currency = ForeignExchangeRate.get_data_indian_currency(soup)
        all_list.append(indian_currency)
        return all_list

    @staticmethod
    def get_data_indian_currency(soup):
        table = soup.find('table', {'width': "100%", 'align': "center"})
        first_tr = table.find('tr')
        nested_table = first_tr.find('table')
        all_tr = nested_table.find_all('tr')
        all_td = all_tr[-1].find_all('td')
        currency = all_td[0].text.strip().replace("\n", "").split(' ')
        result = {
            'currency': currency[0] + " " + currency[-1],
            'unit': int(all_td[1].text.strip()),
            'buying': float(all_td[2].text.strip()),
            'selling': float(all_td[3].text.strip())
        }

        return result

    def put_to_database(self):
        store = Store()
        data = self.get_data()
        store.put_forex_to_db(data)


