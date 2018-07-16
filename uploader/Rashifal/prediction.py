from bs4 import BeautifulSoup

from Firestore.Store import Store
from Util.Utility import Utility


class RashifalPrediction:
    def __init__(self):
        pass

    def get_url(self):
        store = Store()
        url = store.get_rashifal_url()['rashifal_prediction']
        return url

    def get_content(self):
        content = Utility.get_source(self.get_url())
        soup = BeautifulSoup(content, 'html.parser')
        main_soup = soup.find('div', {'class': 'ui-content bg-light-gray'})
        all_divs = main_soup.find_all('div', {'class': 'card-view-content'})[1:]
        final_result = []
        for div in all_divs:
            title = div.h2.text.strip()
            desc = div.p.text.strip()
            result = {'title': title,
                      'desc': desc
                      }
            final_result.append(result)
        return final_result

    def put_to_database(self):
        contents = self.get_content()
        store = Store()
        store.put_yearly_rashifal(contents, u"prediction")

