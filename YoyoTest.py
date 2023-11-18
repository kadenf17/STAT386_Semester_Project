import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://shop.yoyoexpert.com/collections/1a-string-trick-yo-yos?view=listall"


response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
   
link_elements = soup.select("a[href]")

for link_element in link_elements:
    ur = link_element["href"]
    if "/collections/1a-string-trick-yo-yos?page=" not in ur:
        print(ur)

# /collections/1a-string-trick-yo-yos?page=10&view=listall

'''
product = {}

print(url)
print(soup.select_one(".product-title").text.strip())
print(soup.select_one(".hidden-xs.prices span.price").text.strip())
print(soup.select_one(".product-vendor").text.strip())

table = soup.find("table")

table_data = {}
for row in table.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) == 2:
        key = cells[0].text.strip().replace(":", "")
        value = cells[1].text.strip()
        table_data[key] = value

# Convert the table data to a DataFrame
df = pd.DataFrame([table_data])

# Save the DataFrame to a CSV file
df.to_csv("table_data.csv", index=False)
'''