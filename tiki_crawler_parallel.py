import selenium
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import threading
from queue import Queue

# ===============================Initial=======================================
n=6
global title_li, link_li
title_li, link_li = [], []

# ===============================Define Logic==================================

def openMultiBrowsers(n):
    drivers = []
    for i in range(n):
        options = webdriver.ChromeOptions() 
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--log-level=3")
        chromedriver_path = "D:\Python\Scripts\chromedriver.exe"
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options = options)
        drivers.append(driver)
    return drivers

def loadMultiPages(driver, n):
    # for driver in drivers:
    driver.maximize_window()
    driver.get("https://tiki.vn/nha-sach-tiki/c8322?page={}".format(n))
    sleep(6)

def loadMultiBrowsers(drivers_rx, n):
    for driver in drivers_rx:
        t = threading.Thread(target=loadMultiPages, args = (driver, n,))
        t.start()

def getData(driver):
    try:
        elems = driver.find_elements(By.CSS_SELECTOR , ".jXFjHV [href]")        
        print("Page is ready!")
    except:
        print("Please, Retry")
    for i in elems:
        title_li.append(i.text) 
        link_li.append(i.get_attribute('href'))
    sleep(3)
    driver.close()
    print("Crawl Done!!! Close browers:\n ", driver)
    print("----------------")
    return title_li, link_li

def runInParallel(func, drivers_rx):
    for driver in drivers_rx:  
        que = Queue()
        print("-------Running parallel---------")
        t1 = threading.Thread(target=lambda q, arg1: q.put(func(arg1)), args=(que, driver))
        t1.start()
    try:    
        ouput = que.get()
    except:
        ouput = [] 

    return ouput

# ===========================Run/Execute=======================================

drivers_r1 = openMultiBrowsers(n)
loadMultiBrowsers(drivers_r1, n)  
sleep(10)

# ===== GET link/title

title_link2 = runInParallel(getData, drivers_r1)

#return values
titles = title_link2[0]
links = title_link2[1]

#save to...
df_final = pd.DataFrame({'title': titles, 'link': links})
df_final.to_csv('titleLinkTiki_{}Pages.csv'.format(n))
len(df_final)

# =============================================================================
# CONNECT TO SQL SERVER BY PYTHON
# =============================================================================
    
import pandas as pd
import pyodbc


conn = pyodbc.connect('Driver={SQL Server};'
                    'Server=localhost;'
                    'Database=Tiki;'
                    'UID=sa;'
                    'PWD=221045')

# df = pd.read_sql_query('SELECT * FROM dbo.sales', conn)

df_final.to_sql('titleLinkTiki_{}Pages'.format(n), conn, if_exists='append')
