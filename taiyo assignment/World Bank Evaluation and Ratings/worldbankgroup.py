from bs4 import BeautifulSoup
import pandas as pd
import requests

def data_scraper(url):
    world_bank_dict = {'Tender Title': [],
                       'Description': [],
                       'Doc Sub Category': [],
                       'Country': [],
                       'Content Type': [],
                       'Date': []}

    webpage = requests.get(url)
    if webpage.status_code == 200:
        soup = BeautifulSoup(webpage.content, 'html.parser')

    # getting the link
    list_of_link = []
    links = soup.find_all('a', {'data-customlink': 'sp:body content'})
    for elements in links:
        link = elements.get('href')
        if link not in list_of_link:
            list_of_link.append(link)


    for link in list_of_link:

        response = requests.get('https://ieg.worldbankgroup.org/ieg-search' + link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # title

            title = soup.find_all('a',{'data-customlink':'sr:body content'})
            for elements in title:
                world_bank_dict['Tender Title'].append(elements.get_text())

            # getting the description

            description = soup.find_all('span', {'class': 'nontrimmed'})
            for elements in description:
                world_bank_dict['Description'].append(elements.get_text().replace("\n", "").replace("          ", ""))

            # Doc Category

            doc_category = soup.find_all('span', {'class': 'doc-sub-type'})
            for elements in doc_category:
                world_bank_dict['Doc Sub Category'].append(elements.get_text().lstrip("Doc Sub Category :"))

            # Country

            country = soup.find_all('span', {'class': 'countrylist'})
            for elements in country:
                world_bank_dict['Country'].append(elements.get_text().lstrip("Country : "))

            # Date
            date = soup.find_all('time')
            for elements in date:
                world_bank_dict['Date'].append(elements.get_text())

            # content_type
            content_type = soup.find_all('span', {'class': 'doc-sub-type'})
            for elements in content_type:
                world_bank_dict['Content Type'].append(elements.get_text().lstrip('Doc Sub Category :'))

        world_bank_df = pd.DataFrame.from_dict(world_bank_dict)
        world_bank_df.to_csv("World Bank Projects and Tenders.csv", header=True, index=False)

    return world_bank_df


data = data_scraper('https://ieg.worldbankgroup.org/ieg-search?search_api_fulltext=tenders&field_topic=All&field_sub_category=All&content_type_1=&field_organization_tags=All&type_2_op=not&type_2%5B%5D=homepage_spotlight_feature&sort_by=search_api_relevance&sort_order=DESC')

print(data)