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

def get_similar_properties(Zoopla_url):
    house = simple_get(Zoopla_url)
    house_html = BeautifulSoup(house,'html.parser')

    similar_properties = house_html.find_all("a",class_="ui-property-card__link",href=True)

    return similar_properties

def get_address(Zoopla_url):
    house = simple_get(Zoopla_url)
    house_html = BeautifulSoup(house,'html.parser')

    return house_html.find_all("h2",class_="ui-property-summary__address")[0].text

def get_houses_in_postcode_segment(postcode):
    zoopla_url = "https://www.zoopla.co.uk/for-sale/property/{}/?page_size=100".format(postcode)
    #print(zoopla_url)
    houses = BeautifulSoup(simple_get(zoopla_url),'html.parser')
    house_links = houses.find_all("h2",class_="listing-results-attr")
    
    totalviews = 0
    c = 0
    
    for link in house_links:
        url = (link.find('a',href=True)['href'])
        l = "https://www.zoopla.co.uk{}".format(url)
        last_30,all_views = get_house_views(l)
        address = get_address(l)
        #print("{a} has had {v} views in the last 30 days".format(a=address,v=last_30))
        totalviews += last_30
        c = c + 1
    if c > 0:
        avg_views = totalviews / c
    else:
        avg_views = 0
    #print("the average views in the last 30 days for {postcode} is: {a}".format(postcode=postcode, a=avg_views))
    return avg_views

        



if __name__ =="__main__":
    s = get_similar_properties(our_house)
    our_views_30,our_total_views = get_house_views(our_house)
    print("For our house there have been {} views in the last 30 days".format(our_views_30))
    print("here are the house views for zoopla's similar properties in the last 30 days...")
    Total_views_30 = 0
    for similar in s:
        other =  (similar["href"])
        address = get_address(other)
        last_30,all_views = get_house_views(other)
        print("{a} has had {b} views".format(a=address,b=last_30))
        Total_views_30 += last_30
    avg = Total_views_30 / len(s)
    print("the average views for the other houses in the last 30 days is {}".format(avg))
    print("now look at our postcode area of LS13...this may take a minute")
    print("the average views in LS13 in the last 30 days is:{}".format(get_houses_in_postcode_segment("LS13")))


    



