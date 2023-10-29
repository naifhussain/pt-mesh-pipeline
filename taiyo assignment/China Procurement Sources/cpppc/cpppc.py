import requests
from lxml import html
import csv

# Define the URL to scrape
url = "https://www.cpppc.org/en/PPPyd.jhtml"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using lxml
    tree = html.fromstring(response.text)
    
    # Define an XPath expression to target the articles
    with open('articles.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Title', 'Content'])
        i=1
        while i>0:
            try:
                article_xpath = f"/html/body/div[4]/div[1]/div/ul/li[{i}]"
                title_path = article_xpath + '/a'
                content_path = article_xpath + '/div'
                article = tree.xpath(article_xpath)
                title = article[0].xpath(title_path)[0].text
                content = article[0].xpath(content_path)[0].text
                csv_writer.writerow([title, content])
                i+=1
            except:
                print(i)
                break
                
    print("Scraping and CSV export completed.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

import requests
from lxml import html
import csv

# Define the URL to scrape
url = "https://www.cpppc.org/en/PPPyd.jhtml"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using lxml
    tree = html.fromstring(response.text)
    
    # Create a CSV file to store the scraped data
    with open('articles1.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Title', 'Content'])
        
        i = 1
        while True:
            try:
                # Define the XPath expressions for title and content
                article_xpath = f"/html/body/div[4]/div[2]/div/ul/li[{i}]"
                title_path = article_xpath + '/a'
                content_path = article_xpath + '/div'
                article = tree.xpath(article_xpath)
                title = article[0].xpath(title_path)[0].text
                content = article[0].xpath(content_path)[0].text
                csv_writer.writerow([title, content])
                i+=1
            except:
                print(i)
                break
                
    print("Scraping and CSV export completed.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")  