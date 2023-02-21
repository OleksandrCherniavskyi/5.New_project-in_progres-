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
        print("No new Technologies")
        return False

        # Primary Key Check
    if pd.Series(df['Technologies']).is_unique:
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
    tech = []
    for brand in brands:
        brand_link = brand.find('a', href=True)
        if brand_link not in brand:
            continue
        # brand link open Brand Stor
        brand_link = ('https://justjoin.it' + brand_link['href'])
        brand_r = requests.get(brand_link)
        brand_webpage = bs(brand_r.text, features="html.parser")
        try:
            div_offers = brand_webpage.body.find('div', {'id': "offers"})
            positions_list = div_offers.find('div')
            for position in positions_list:
                link_offers = position.find('a', href=True)
                p_webpage = ('https://justjoin.it' + link_offers['href'])
                p_technology_block = position.find_all('div')[-1]
                tech_more = p_technology_block.find_all('span')


                def Technology():
                    technology = []
                    for tech_one in tech_more:
                        text_tech = tech_one.text
                        technology.append(text_tech)
                    return technology
                technology = Technology()
                tech.extend(technology)
        except AttributeError:
            continue

    tech_dict = {'Technologies': tech}



    tech_df = pd.DataFrame(tech_dict, columns=['Technologies'])
    tech_df = tech_df.drop_duplicates()

    # Validate
    if check_if_valid_data(tech_df):
        print("Data valid, proceed to Load stage")

    # Load

    engine = create_engine('sqlite:///justjoin.sqlite', echo=True)
    conn = sqlite3.connect('justjoin.sqlite')
    cursor = conn.cursor()

    sql_query = """
        CREATE TABLE IF NOT EXISTS tech(
            Technologies VARCHAR(100) PRIMARY KEY
        )
        """

    cursor.execute(sql_query)
    print("Opened database successfully")

    try:
        tech_df.to_sql("tech", engine, index=False, if_exists='append')
    except :
        print("Data already exists in the database")

    conn.close()
    print("Close database successfully")

#get the end time
et = time.time()
#get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')
