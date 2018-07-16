import requests
from fake_useragent import UserAgent


class Utility():
    @staticmethod
    def get_source(site):
        ua = UserAgent()
        headers = {
            'User-Agent': str(ua.random)}
        return requests.get(site, headers=headers).content

    @staticmethod
    def get_mnth_from_mnth_name(mnth_name):

        return {
            'Jan': "01",
            'Feb': "02",
            'Mar': "03",
            'Apr': "04",
            'May': "05",
            'Jun': "06",
            'Jul': "07",
            'Aug': "08",
            'Sep': "09",
            'Oct': "10",
            'Nov': "11",
            'Dec': "12"
        }[mnth_name]
