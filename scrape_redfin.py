from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import time
import re
import ast
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import datetime
matplotlib.use('Agg')

def init_browser():
    """start chrome browser
    """
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=True)


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
            sub_dict["time"] = datetime.datetime.utcnow()
            try:
                sub_dict["city"] = ast.literal_eval(homecard.find_all("script")[0].text)[0]["address"]["addressLocality"].strip()
            except:
                sub_dict["city"] = "No Information Available"
            # append dict to list
            homecard_list.append(sub_dict)
    

    return homecard_list

def data_cleaner(list_of_dict)->pd.core.frame.DataFrame:
    """takes input from scraper function convert list of dict into dataframe and clean up.
    """
    dataframe = pd.DataFrame(columns = ["beds","baths","area","price","address", "link","city","time"], data = list_of_dict)

    # clean up data
    dataframe["beds"] = [re.split("\s", bed)[0] if re.split("\s", bed)[0].isnumeric() else "" for bed in dataframe["beds"]]
    dataframe["baths"] = [re.split("\s", bed)[0] if re.split("\s", bed)[0].isnumeric() else "" for bed in dataframe["baths"]]
    dataframe["price"] = [int(p.replace("$","").replace(",","")) for p in dataframe["price"]]
    # dataframe["area"] = [re.split("\s", a)[0].replace(",","") for a in dataframe["area"]]
    dataframe = dataframe.sort_values("city",ascending = False)

    return dataframe
     
        


def summary(dataframe)->dict:
    """summarize dataframe from scraper function
    """
    summary_info = {}
    summary_info["avg_price"] = "${:,.0f}".format(round(dataframe["price"].describe()[1],0)) # average price
    summary_info["median_price"] =  "${:,.0f}".format(round(dataframe["price"].describe()[5],0)) # median price
    summary_info["max_price"] =  "${:,.0f}".format(round(dataframe["price"].describe()[-1],0)) # max price
    summary_info["html_table"] = dataframe.to_html(index=False)
    
    return summary_info



def plot_data(dataframe)->None:
    """export a png plot
    """
    pt = dataframe.groupby("city").agg(price = ("price","median")).sort_values("price", ascending = False).reset_index()
    plt.figure(figsize= (20,25))
    plt.title("Median House Price In LA County Area", fontsize = 30)
    plot = sns.barplot(x = "price", y = "city", data = pt)
    plot_figure = plot.get_figure()
    plot_figure.savefig("static/plot.png")
    
    return None


    
    
    