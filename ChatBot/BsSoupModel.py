from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from urllib.request import urlopen, Request


class BsSoupModel:
    headers = {
        "User - Agent": "Mozilla /5.0 (WindowsNT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}

    def get_page_soup(self, baseUrl):
        uClinet = uReq(baseUrl)
        page_html = uClinet.read()
        uClinet.close()
        page_soup = bs(page_html, "html.parser")
        return page_soup

    def get_page_soup_header(self, baseUrl, url_val):
        headers = {
            "User - Agent": "Mozilla /5.0 (WindowsNT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
        req = Request(url=baseUrl + url_val, headers=headers)
        html = urlopen(req).read()

    def get_rating_avg(self, rating_result_list):
        '''
        :param rating_result_list: Rating list from page soup
        :return:final avegare of all rating on the page
        '''
        try:
            final_rating = 0.0
            for eachRating in rating_result_list:
                final_rating += float(eachRating.contents[0])

            final_rating = final_rating / len(rating_result_list)
        except ValueError as e:
            raise e.__str__();
        return format(final_rating, ".1f")
