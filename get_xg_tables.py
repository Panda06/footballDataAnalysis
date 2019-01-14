import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from os import path


options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
base_url = "https://understat.com/league/EPL/201"
soups = []

for year in "45678":
    driver.get(base_url + year)
    soup = bs(driver.page_source, "lxml")
    soups.append(soup)

headers = soups[0].find('div', attrs={'class':'chemp jTable'}).find('table').find_all('th',attrs={'class':'sort'})
 
headers
columns = []

for header in headers:
    columns.append(header.get_text(strip=True))

for soup in soups:
    rows = []
    table = soup.find("div", attrs={"class":"chemp jTable"}).table.tbody
    for row in table.find_all("tr"):
        current_row = []
        for item in row.find_all("td"):
            current_row.append(item.get_text(strip=True))
        rows.append(current_row)
    title = str(soup.title)
    index = title.find("201")
    season = title[index:index+4]
    pd.DataFrame(data=rows, columns=columns).to_csv(path.join("xg_data", season + ".csv", index=None))