import requests
from bs4 import BeautifulSoup
import csv
import time


starting_point = "https://shop.yoyoexpert.com/collections/1a-string-trick-yo-yos?view=listall"
# https://shop.yoyoexpert.com/collections/1a-string-trick-yo-yos?view=listall&page=2
# https://shop.yoyoexpert.com/collections/1a-string-trick-yo-yos?page=10&view=listall
# collections/1a-string-trick-yo-yos?page=10&view=listall


base_site = "https://shop.yoyoexpert.com"
out_csv_file = "yoyo_raw_data.csv"
in_csv_file = "visited_urls.csv"
#n = 30 # Number of pages to scrape this run

products = []
urls = [starting_point]
errors = 0

# Initialize visited_urls with existing URLs from the file
try:
    with open(in_csv_file, mode='r', encoding='utf-8') as txt_file:
        visited_urls = [line.strip() for line in txt_file.readlines() if line.strip() != starting_point]
except FileNotFoundError:
    visited_urls = []


sv_url_len = len(visited_urls)
print("\n")
print("Starting Crawler:")
print("\n")

#  and len(visited_urls) < n+sv_url_len
while len(urls) > 0:
    current_url = urls.pop()
    print(f"Now attempting to visit: {current_url}")
    
    response = requests.get(current_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # mark the current URL as visited
    visited_urls.append(current_url)

    # find other urls
    link_elements = soup.select("a[href]")
    
    for link_element in link_elements:
        url = link_element["href"]
        if "/collections/1a-string-trick-yo-yos?page=" in url:
            if base_site not in url:
                url = base_site+url
            if url not in visited_urls and url not in urls:
                urls.insert(0, url)

        if "/collections/1a-string-trick-yo-yos/products" in url:
            if base_site not in url:
                url = base_site+url
            if url not in visited_urls and url not in urls:
                urls.append(url)


    # if current_url is product page
    if "/products" in current_url:
        print('I found a new yoyo!')
        product = {}
        key_list = ["url", "name", "price", "brand", "diameter", "width", "gap width", "weight", "bearing size", "response", "material", "designed in", "made in", "machined in", "released"]

        for key in key_list:
            product[key] = "NA"

        product["url"] = current_url

        try:
            product["name"] = soup.select_one(".product-title").text.strip()
            print(f"Name: {soup.select_one('.product-title').text.strip()}")
        except:
            print("Name: Not found")
        
        try:
            product["price"] = soup.select_one(".hidden-xs.prices span.price").text.strip()
            print(f"Price: {soup.select_one('.hidden-xs.prices span.price').text.strip()}")
        except:
            print("Price: Not found")
        
        try:
            product["brand"] = soup.select_one(".product-vendor").text.strip()
            print(f"Brand: {soup.select_one('.product-vendor').text.strip()}")
        except:
            print("Brand: Not found")

        
        try:    # Extract table data
            table_data = {}
            for row in soup.select(".stats tr"):
                cells = row.select("td")
                if len(cells) == 2:
                    key = cells[0].text.strip().replace(":", "").lower().replace("release date", "released")
                    value = cells[1].text.strip().replace(",", "").replace(" ","").replace("\n","").replace("\r","")
                    if key in key_list:
                        table_data[key] = value
                    else:
                        print(f"   **Warning: {key} is not found in key list.")
                        errors += 1

            # Add table data to product
            product.update(table_data)
        except:
            print("   ** Error Scraping Spec Table")
            errors += 1

        products.append(product)

        # Write to the CSV
        with open(out_csv_file, mode='a', newline='', encoding='utf-8') as file:
            fieldnames = key_list
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(product)


    else: print("No product found on this page.")

    # Save the visted urls to a csv
    if "/collections/1a-string-trick-yo-yos?page=" not in current_url and current_url != starting_point:
        with open(in_csv_file, mode='a', encoding='utf-8') as txt_file:
            txt_file.write(current_url + '\n')

    print(f"I have visited {len(visited_urls)-sv_url_len} new urls and {len(visited_urls)} urls total.")
    print(f"There are currently {len(urls)} urls in my queue to vist.")
    print(f"So far I have found {len(products)} new yoyos this run.")
    print(f"** {errors} errors found this run.")

    # Following their robots.txt we need to sleep 30 seconds

    #if len(visited_urls) < n+sv_url_len: 
    print("Sleeping 30 sec (to comply with yoyoexpert's robots.txt)")
    time.sleep(30)
    print("\n")
    


print(f"Crawling/Scraping complete.")
print(f"I visited {len(visited_urls)-sv_url_len} urls.")
print(f"I added data for {len(products)} yoyos.")
print(f"** There were {errors} issues detected while scraping.")
print("\n")