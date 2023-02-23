import time
import requests
from bs4 import BeautifulSoup as bs
from sqlalchemy import create_engine
import pandas as pd
import sqlite3
from selenium import webdriver



options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(r'C:\Users\bootbyt\PycharmProjects\chromedriver_win32\chromedriver.exe', options=options)

# get the start time
st = time.time()


def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Check if dataframe is empty
    if df.empty:
        print("No new city")
        return False

        # Primary Key Check
    if pd.Series(df['Offices']).is_unique:
        pass
    else:
        raise Exception("Primary Key check is violated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found")
    return True


if __name__ == "__main__":
    # SCRAPING DATA FOR DB_TABLE_TECHO


    driver.get('https://justjoin.it/brands')
    source_code = driver.page_source
    webpage = bs(source_code, features="html.parser")
    brands_list = webpage.find('div', attrs={'class': 'MuiGrid-container'})
    brands = brands_list.select('div', attrs={'class': 'MuiGrid-item'})
    offices = []
    for brand in brands:
        brand_link = brand.find('a', href=True)
        if brand_link not in brand:
            continue
        #brand link open Brand Stor
        brand_link = ('https://justjoin.it' + brand_link['href'])
        #brand_link = 'https://justjoin.it/brands/story/future-mind'
        brand_r = requests.get(brand_link)
        brand_webpage = bs(brand_r.text, features="html.parser")
        try:
            div_offers = brand_webpage.body.find('div', {'id': "offices"})
            offices_block = div_offers.find('ul', {'class': 'MuiList-root'})
            for offices_list in offices_block:
                office = offices_list.find('span').text
                #print(office)
                offices.append(office)
            #if offices_block == None:
            #    continue

        except AttributeError:
            continue

    offices_dict = {'Offices': offices}



    offices_df = pd.DataFrame(offices_dict, columns=['Offices'])
    offices_df = offices_df.drop_duplicates()

    # Validate
    if check_if_valid_data(offices_df):
        print("Data valid, proceed to Load stage")

    # Load

    engine = create_engine('sqlite:///justjoin.sqlite', echo=True)
    conn = sqlite3.connect('justjoin.sqlite')
    cursor = conn.cursor()

    sql_query = """
        CREATE TABLE IF NOT EXISTS offices(
            Offices VARCHAR(100) PRIMARY KEY
        )
        """

    cursor.execute(sql_query)
    print("Opened database successfully")

    try:
        offices_df.to_sql("offices", engine, index=False, if_exists='append')
    except :
        print("Data already exists in the database")

    conn.close()
    print("Close database successfully")

#get the end time
et = time.time()
#get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')
