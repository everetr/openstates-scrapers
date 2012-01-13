import datetime as dt
import lxml.html

from urlparse import urlparse

from billy.scrape.bills import BillScraper, Bill
from billy.scrape.votes import Vote

HI_URL_BASE = "http://capitol.hawaii.gov/"


def create_bill_report_url( chamber, year ):
    cname = { "upper" : "s", "lower" : "h" }[chamber]
    return HI_URL_BASE + "report.aspx?type=intro" + cname + "b&year=" + year

class HIBillScraper(BillScraper):
    
    state = 'hi'

    def scrape_bill( self, url ):
        with self.urlopen(url) as bill_html: 
            bill_page = lxml.html.fromstring(bill_html)

    def scrape_report_page(self, url):
        with self.urlopen(url) as list_html: 
            list_page = lxml.html.fromstring(list_html)
            bills = [ HI_URL_BASE + bill.attrib['href'] for bill in \
                list_page.xpath("//a[@class='report']") ]
            for bill in bills:
                self.scrape_bill( bill )

    def scrape(self, chamber, session):
        session_urlslug = \
            self.metadata['session_details'][session]['_scraped_name']
        self.scrape_report_page( \
            create_bill_report_url( chamber, session_urlslug ) )
