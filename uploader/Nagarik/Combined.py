from Nagarik.NagarikLatest import NagarikLatest

names = [u'nagarik', u'republica', u'shukrabar']
urls = [u"http://nagarikplus.nagariknews.com/epaper/src/",
        u"http://e.myrepublica.com/epaper/src/",
        u"http://nagarikplus.nagariknews.com/epaper/src/shukrabar.php"]
image_prefixs = [u"http://nagarikplus.nagariknews.com/images/flippingbook/",
                 u"http://e.myrepublica.com/images/flippingbook/",
                 u"http://nagarikplus.nagariknews.com/images/flippingbook/"]

types = [u"daily", u"daily", u"weekly"]


def run():
    for i in range(0, len(names)):
        nl = NagarikLatest(names[i], urls[i], image_prefixs[i], types[i])
        nl.get_data()

run()
