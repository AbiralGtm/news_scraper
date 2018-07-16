from bs4 import BeautifulSoup

from Firestore.Store import Store
from Util.Utility import Utility


class DailyRashifal:
    def __init__(self, url):
        self.main_url = url

    def get_data(self):
        req = Utility.get_source(self.main_url)
        soup = BeautifulSoup(req, 'html.parser')
        date_str = DailyRashifal.get_date(soup)
        links = self.all_links()
        datas = []
        for link in links:
            content = Utility.get_source(link[0])
            soup = BeautifulSoup(content, 'html.parser')
            data = DailyRashifal.get_data_item(soup)
            data['name'] = link[1]
            data['date'] = date_str
            datas.append(data)
        return datas

    @staticmethod
    def get_data_item(soup):
        # find div with ui-box ui-margin-tb
        main = soup.find('div', {'class': 'ui-box ui-margin-tb'})
        title = main.find('div', {'class': 'ui-sign-heading'}).text.strip()
        desc = main.find('div', {'class': 'ui-large-content text-justify'}).text.strip()
        starts_div = main.find_all('div', {'class': 'col-sm-4'})
        starts_info = []
        for star_div in starts_div:
            topic = star_div.b.text.strip().replace(":", "")
            no_of_stars = DailyRashifal.get_stars(star_div)
            result = {'title': topic,
                      'no_of_stars': no_of_stars}
            starts_info.append(result)
        return {'title': title,
                'desc': desc,
                'starts': starts_info}

    @staticmethod
    def get_stars(div):
        all_starts = div.find_all('img', {'src': '/images/rating/star2.gif'})
        starts = len(all_starts)
        return starts

    @staticmethod
    def get_date(soup):
        content = soup.find('div', {'class': 'contents'})
        div = content.find("div", {'align': 'center'})
        date_str = div.b.text.strip()
        return date_str

    def all_links(self):
        return [("http://www.astrosage.com/nepali/rashifal/mesh-rashifal.asp", u"mesh"),
                ("http://www.astrosage.com/nepali/rashifal/vrishabha-rashifal.asp", u"vrishabha"),
                ("http://www.astrosage.com/nepali/rashifal/mithun-rashifal.asp", u"mithun"),
                ("http://www.astrosage.com/nepali/rashifal/karkat-rashifal.asp", u"karkat"),
                ("http://www.astrosage.com/nepali/rashifal/simha-rashifal.asp", u"simha"),
                ("http://www.astrosage.com/nepali/rashifal/kanya-rashifal.asp", u"kanya"),
                ("http://www.astrosage.com/nepali/rashifal/tula-rashifal.asp", u"tula"),
                ("http://www.astrosage.com/nepali/rashifal/vrishchika-rashifal.asp", u"vrishchika"),
                ("http://www.astrosage.com/nepali/rashifal/dhanu-rashifal.asp", u"dhanu"),
                ("http://www.astrosage.com/nepali/rashifal/makara-rashifal.asp", u"makara"),
                ("http://www.astrosage.com/nepali/rashifal/kumbha-rashifal.asp", u"kumbha"),
                ("http://www.astrosage.com/nepali/rashifal/meen-rashifal.asp", u"meen")]

    def put_to_database(self):
        store = Store()
        data = self.get_data()
        store.put_daily_rashifal(data)

