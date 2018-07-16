import re

from bs4 import BeautifulSoup

from Util.Utility import Utility


class Rashifal(object):
    def __init__(self):
        self.daily_url = "http://nepalipatro.com.np/rashifal/index/type/daily"
        self.monthly_url = "http://nepalipatro.com.np/rashifal/index/type/monthly"
        self.weekly_url = "http://nepalipatro.com.np/rashifal/index/type/weekly"
        self.yearly_url = "http://nepalipatro.com.np/rashifal/index/type/yearly"


    @staticmethod
    def get_soup(url):
        content = Utility.get_source(url)
        return BeautifulSoup(content, 'html.parser')

    """
    sample rashifal item
    heading:""
    name : ""
    image_url: ""
    content: ""
    """

    def get_rashifals(self, soup):
        # row horoscope
        all_divs = soup.find_all('div', {'class': re.compile("panel-material")})
        print(len(all_divs))
        rashifals = []
        for div in all_divs:
            heading = div.find('div', {'class': 'panel-heading'}).text
            content_soup = div.find('div', {'class': 'panel-body'})
            content = content_soup.text
            text_to_replace = "नेपाली पात्रो"
            if text_to_replace in content:
                content = content.replace(text_to_replace, "")
                content = content.replace("()","")
            name = content_soup.img['alt']
            image_url = "http://nepalipatro.com.np" + content_soup.img['src']
            rashifal = {'name': name.strip(),
                        'heading': heading.strip(),
                        'content': content.strip(),
                        'image_url': image_url}
            rashifals.append(rashifal)
        return rashifals

    def get_date(self, soup ,type):
        if type == "daily":
            pass
        else:
            pass



r = Rashifal()
soup = r.get_soup(r.daily_url)
print(r.get_rashifals(soup)[0])




