from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import time

def init_browser():
    """start chrome browser
    """
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def visit_browser(url:str):
    """use splinter to visit browser
    """
    browser = init_browser()
    try:
        browser.visit(url)
        time.sleep(2)
        html = browser.html
        soup = bs(html, "html5lib")
    except:
        print("Error in visiting the page----")
    
    return soup


def scrape_cards_info(html_str:str, name:str, html_tag:str, html_class:str, order_num:int):
    """scrape homecard information
    """
    if name in ["beds","baths","area"]:
        try:
            output = html_str.find(html_tag,html_class).find_all("div","stats")[order_num].text
        except:
            print(f"error in finding {name} variable-------")
            output = ""
    elif name in ["link"]:
        output = html_str.a["href"]
    elif name in ["price"]:
        try:
            output = html_str.find(html_tag, html_class).text
        except:
            output = ""
            print(f"error in finding {name} variable------")
    else:
        try:
            output = html_str.find(html_tag,html_class).span.text
        except:
            output = ""
            print(f"error in finding {name} variable------")
    return output

def scraper():
    """scrape redfin hourse information
    """
    # define url and visit
    main_url = "https://www.redfin.com/county/321/CA/Los-Angeles-County"
    soup = visit_browser(main_url)

    # find out number of pages
    last_page = int(soup.find_all("div","PagingControls")[0].find_all("a")[-1].text)
    homecard_list = []
    for i in range(last_page):
        url = f"https://www.redfin.com/county/321/CA/Los-Angeles-County/Page-{i+1}"
        # visit each page
        soup = visit_browser(url)
        # find out number of cards
        homecards = soup.find_all("div","bottomV2")
        
        # loop thought each homecard
        for homecard in homecards:
            sub_dict= {}
            # store values into sub_dict
            sub_dict["beds"] = scrape_cards_info(homecard, "beds","div","HomeStatsV2",0)
            sub_dict["baths"] = scrape_cards_info(homecard, "baths","div","HomeStatsV2",1)
            sub_dict["area"] = scrape_cards_info(homecard, "area","div","HomeStatsV2",2)
            sub_dict["price"] = scrape_cards_info(homecard, "price","span","homecardV2Price",1)
            sub_dict["address"] = scrape_cards_info(homecard, "address","div","homeAddressV2",1)
            sub_dict["link"] = "https://www.redfin.com"+scrape_cards_info(homecard, "link","","",1)

            # append dict to list
            homecard_list.append(sub_dict)
    
    data = pd.DataFrame(columns = ["beds","baths","area","price","address", "link"], data = homecard_list)

    return data


