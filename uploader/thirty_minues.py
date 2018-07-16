#!/home/newsapp/khabarSanjal/my_env/bin/python

from Nagarik.NagarikLatest import NagarikLatest
from NayaPatrika.naya_patrika import NayaPatrika
from Rashifal.daily import DailyRashifal

# nagarik
# rashifal daily


names = [u'nagarik', u'republica', u'shukrabar']
urls = [u"http://nagarikplus.nagariknews.com/epaper/src/",
        u"http://e.myrepublica.com/epaper/src/",
        u"http://nagarikplus.nagariknews.com/epaper/src/shukrabar.php"]
image_prefixs = [u"http://nagarikplus.nagariknews.com/images/flippingbook/",
                 u"http://e.myrepublica.com/images/flippingbook/",
                 u"http://nagarikplus.nagariknews.com/images/flippingbook/"]

types = [u"daily", u"daily", u"weekly"]


def run_nagarik():
    for i in range(0, len(names)):
        nl = NagarikLatest(names[i], urls[i], image_prefixs[i], types[i])
        print "Nagraik epapers crawled"
        nl.get_data()


def run_rahifal_daily():
    dr = DailyRashifal("http://www.astrosage.com/nepali/rashifal/")
    print "rashifal daily crawled"
    dr.put_to_database()

def run_naya_patrika():
    naya_patrika = NayaPatrika()
    naya_patrika.get_latest()

if __name__ == '__main__':
    run_nagarik()
    run_rahifal_daily()
    run_naya_patrika()
