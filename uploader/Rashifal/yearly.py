from bs4 import BeautifulSoup

from Firestore.Store import Store
from Util.Utility import Utility


class YearlyRashifal(object):
    def __init__(self):
        pass

    def get_url(self):
        store = Store()
        url = store.get_rashifal_url()['rashifal_yearly']
        return url

    def get_content(self):
        content = Utility.get_source(self.get_url())
        soup = BeautifulSoup(content, 'html.parser')
        # print content
        soup = soup.find('div', {'class': 'contents'})
        all_h_p = soup.find_all(['h2', 'p'])
        return YearlyRashifal.get_data(all_h_p)

    @staticmethod
    def get_data(list_of_h_p):
        h2_index = []
        for h_p in list_of_h_p:
            if h_p.name == "h2":
                h2_index.append(list_of_h_p.index(h_p))
        list_of_result = []
        for i, index_of_h2 in enumerate(h2_index):
            title = list_of_h_p[index_of_h2].text.strip()
            desc = []
            if i is not len(h2_index) - 1:
                for j in range(index_of_h2 + 1, h2_index[i + 1]):
                    desc.append(list_of_h_p[j].text.strip())
            else:
                for j in range(index_of_h2 + 1, len(list_of_h_p)):
                    desc.append(list_of_h_p[j].text.strip())

            result = {'title': title,
                      'desc': desc,
                      'order': i}
            list_of_result.append(result)
        return list_of_result

    def put_to_database(self):
        contents = self.get_content()
        store = Store()
        store.put_yearly_rashifal(contents, u'yearly')

