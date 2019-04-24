from get_url import simple_get
from bs4 import BeautifulSoup

our_house = 'https://www.zoopla.co.uk/for-sale/details/50903990?search_identifier=d6fe9eeab3ebd7bf77f86a076cd6c39f'

def get_int_from_string(s):
    '''
    This will return a single integer from a string
    '''
    return int(''.join(filter(str.isdigit,s)))


def get_house_views(Zoopla_url):
    '''
    For a given house URL on zoopla will return the number of page hits in the last 30 days
    and the number of page views since the house was listed.
    '''
    house = simple_get(Zoopla_url)
    house_html = BeautifulSoup(house,'html.parser')

    views = house_html.find_all("span",class_="dp-view-count__value")

    last_30_days = get_int_from_string(views[0].text)
    since_listed = get_int_from_string(views[1].text)

    return last_30_days,since_listed

