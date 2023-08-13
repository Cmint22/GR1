import numpy as np
from selenium import webdriver
from time import sleep
import random 
import csv
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd

# Declare browser
options = webdriver.ChromeOptions() 
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--log-level=3")
chromedriver_path = "D:\Python\Scripts\chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options = options)


# Open URL
driver.get("https://tiki.vn/nha-sach-tiki/c8322")
sleep(random.randint(5,10))


# ================================ GET link/title
elems = driver.find_elements(By.CSS_SELECTOR , ".jXFjHV [href]")
links = [elem.get_attribute('href') for elem in elems]
elems_title = driver.find_elements(By.CSS_SELECTOR , ".bqaPbq .name")
title = [elem.text for elem in elems_title]

# ================================ GET price
elems_price = driver.find_elements(By.CSS_SELECTOR , ".bqaPbq .price-discount .price-discount__price")
len(elems_price)
price = [elem_price.text for elem_price in elems_price]

df1 = pd.DataFrame(list(zip(title, price, links)), columns = ['title', 'price', 'links'])
df1['index_']= np.arange(1, len(df1) + 1)

# ================================ GET discount
elems_discount = driver.find_elements(By.CSS_SELECTOR , ".bqaPbq .price-discount__discount")
discount = [elem.text for elem in elems_discount]

discount_list, discount_idx = [], []
for i in range(1, len(title)+1):
    try:
        discount = driver.find_element("xpath", "/html/body/div[2]/div[1]/main/div[2]/div[1]/div[2]/div/div[2]/div[{}]/div/a/span/div[2]/div[1]/div[3]/div[1]/div[2]".format(i))
        discount_list.append(discount.text)
        print(i)
        discount_idx.append(i)
    except NoSuchElementException:
        print("No Such Element Exception " + str(i))
df2 = pd.DataFrame(list(zip(discount_idx , discount_list)), columns = ['discount_idx', 'discount_list'])

df3 = df1.merge(df2, how='left', left_on='index_', right_on='discount_idx')

# ================================GET rating/sales
elems_rating = driver.find_elements(By.CSS_SELECTOR , ".eMNcac .fsYaBc")
rating = [elem.text for elem in elems_rating]

elems_sales = driver.find_elements(By.CSS_SELECTOR , ".eMNcac .quantity.has-border")
len(elems_sales)
sales = [elem.text for elem in elems_sales]

rating_list, rating_idx, sales_list = [], [], []
for i in range(1, len(title)+1):
    try:
        rating = driver.find_element("xpath", "/html/body/div[2]/div[1]/main/div[2]/div[1]/div[2]/div/div[2]/div[{}]/div/a/span/div[2]/div[1]/div[2]/div[2]/div".format(i))
        rating_list.append(rating.text)
        sales = driver.find_element("xpath", "/html/body/div[2]/div[1]/main/div[2]/div[1]/div[2]/div/div[2]/div[{}]/div/a/span/div[2]/div[1]/div[2]/div[2]/span".format(i))
        sales_list.append(sales.text)
        print(i)
        rating_idx.append(i)
    except NoSuchElementException:
        print("No Such Element Exception" + str(i))

df4 = pd.DataFrame(list(zip(rating_idx, rating_list, sales_list)), columns = ['rating_idx', 'rating_list', 'sales_list'])

df5 = pd.merge(df3, df4, how='left', left_on='discount_idx', right_on='rating_idx')

print(df5)
df5.to_csv(r'C:\Users\HI\.vscode\Code dạo\GR1\book.csv')
# ================================ GET more infor of each item  
# list1 = []
# list1 = [1,2,3,4] + list1     

driver.get(links[0])

sleep(random.randint(1,3))
elems_name = driver.find_elements(By.CSS_SELECTOR , ".review-comment__user-name")
name_comment = [elem.text for elem in elems_name]

elems_content = driver.find_elements(By.CSS_SELECTOR , ".review-comment__content")
content_comment = [elem.text for elem in elems_content]

elems_skuInfo= driver.find_elements(By.CSS_SELECTOR , ".review-comment__title")
skuInfo_comment = [elem.text for elem in elems_skuInfo]

elems_likeCount = driver.find_elements(By.CSS_SELECTOR , ".review-comment__thank")
like_count = [elem.text for elem in elems_likeCount]

df6 = pd.DataFrame(list(zip(name_comment , content_comment, skuInfo_comment, like_count)), 
                    columns = ['name_comment', 'content_comment','skuInfo_comment', 'like_count'])
# df6['link_item'] = links[0]
df6.insert(0, "link_item", links[0])
print(df6)

sleep(random.randint(1,3))
# ================================ next pagination

next_pagination_cmt = driver.find_element(By.CSS_SELECTOR, ".loVmKB .btn.next")
next_pagination_cmt.click()
sleep(random.randint(1,3))
#close_btn = driver.find_element("xpath", "/html/body/div[7]/div[2]/div")
#close_btn.click()

# ================================
count = 1
name_comment, content_comment, skuInfo_comment, like_count = [], [], [], []
while True:
    try:
        print("Crawl Page " + str(count))
        elems_name = driver.find_elements(By.CSS_SELECTOR , ".review-comment__user-name")
        name_comment = [elem.text for elem in elems_name] + name_comment
        
        elems_content = driver.find_elements(By.CSS_SELECTOR , ".review-comment__content")
        content_comment = [elem.text for elem in elems_content] + content_comment
        
        elems_skuInfo= driver.find_elements(By.CSS_SELECTOR , ".review-comment__title")
        skuInfo_comment = [elem.text for elem in elems_skuInfo] + skuInfo_comment
        
        elems_likeCount = driver.find_elements(By.CSS_SELECTOR , ".review-comment__thank")
        like_count = [elem.text for elem in elems_likeCount] + like_count

        sleep(random.randint(1,3))
        next_pagination_cmt = driver.find_element(By.CSS_SELECTOR, ".hyphpd .loVmKB .btn.next")
        next_pagination_cmt.click()
        print("Clicked on button next page!")
        sleep(random.randint(1,3))
        
        count += 1
    except ElementNotInteractableException:
        print("Element Not Interactable Exception!")
        break
    except NoSuchElementException:
        print("Element No Such Element Exception!")
        break

df6 = pd.DataFrame(list(zip(name_comment , content_comment, skuInfo_comment, like_count)), 
                    columns = ['name_comment', 'content_comment','skuInfo_comment', 'like_count'])
# df6['link_item'] = links[0]
df6.insert(0, "link_item", links[0])    
print(df6)


# =============================================================================


# ============================GET INFOMATION OF ALL ITEMS
def getDetailItems(link):
    driver.get(link)
    count = 1
    name_comment, content_comment, skuInfo_comment, like_count = [], [], [], []
    while True:
        try:
            print("Crawl Page " + str(count))
            elems_name = driver.find_elements(By.CSS_SELECTOR, ".review-comment__user-name")
            name_comment = [elem.text for elem in elems_name] + name_comment

            elems_content = driver.find_elements(By.CSS_SELECTOR, ".dOzoKz .review-comment__content")
            content_comment = [elem.text for elem in elems_content] + content_comment

            elems_skuInfo = driver.find_elements(By.CSS_SELECTOR, ".dOzoKz .review-comment__title")
            skuInfo_comment = [elem.text for elem in elems_skuInfo] + skuInfo_comment

            elems_likeCount = driver.find_elements(By.CSS_SELECTOR, ".dOzoKz .review-comment__thank")
            like_count = [elem.text for elem in elems_likeCount] + like_count

            sleep(random.randint(1,3))
            next_pagination_cmt = driver.find_element(By.CSS_SELECTOR, ".hyphpd .loVmKB .btn.next")
            next_pagination_cmt.click()
            print("Clicked on button next page!")
            sleep(random.randint(1,3))

            count += 1
        except ElementNotInteractableException:
            print("Element Not Interactable Exception!")
            break
        except NoSuchElementException:
            print("Element No Such Element Exception!")
            break

    df6 = pd.DataFrame(list(zip(name_comment, content_comment, skuInfo_comment, like_count)),
                        columns=['name_comment', 'content_comment', 'skuInfo_comment', 'like_count'])
    # df6['link_item'] = links[0]
    df6.insert(0, "link_item", link)
    return df6

print(df6)
df6.to_csv(r'C:\Users\HI\.vscode\Code dạo\GR1\comment.csv')

df_list = []
for link in links:
    df = getDetailItems(link)
    df_list.append(df)
# Close browser
driver.close()    

df.to_csv(r'C:\Users\HI\.vscode\Code dạo\GR1\data.csv')