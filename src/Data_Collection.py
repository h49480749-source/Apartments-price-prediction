import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger('Data-Collection')
def collect_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9"
    }
    data = []
    i = 0

    while True:
        i +=1
        print(f'Scraping page {i}')
        url = f'https://www.dubizzle.com.eg/en/properties/apartments-duplex-for-sale/mountain-view-icity-compound/?page={i}&filter=type_eq_1'

        response = requests.get(url, headers=headers)
        page_html = response.text
        soup = BeautifulSoup(page_html, "lxml")
        EndOfResults = soup.find('span',string='Results from other locations')
        if EndOfResults is not None:
            break
        items = soup.find_all('article')
        for j in range(len(items)):
            link = items[j].find('a')['href']
            url = 'https://www.dubizzle.com.eg'+link
            response = requests.get(url, headers=headers)
            page_html = response.text
            soup = BeautifulSoup(page_html, "lxml")
            if soup.find('span',attrs={'aria-label':'Price'}):
                price = soup.find('span',attrs={'aria-label':'Price'}).text
            else:
                price = None
            if soup.find('span',string='Area (m²)'):  
                Area = soup.find('span',string='Area (m²)').find_next_sibling('span').text
            else:
                Area = None
            if soup.find('span',string='Bedrooms'):
                Bedrooms = soup.find('span',string='Bedrooms').find_next_sibling('span').text
            else:
                Bedrooms = None
            if soup.find('span',string='Payment Option'):
                payment = soup.find('span',string='Payment Option').find_next_sibling('span').text
            else:
                payment = None
            if soup.find('span',string='Completion status'):
                status = soup.find('span',string='Completion status').find_next_sibling('span').text
            else:
                status = None
            if soup.find('span',string='Ownership'):
                ownership = soup.find('span',string='Ownership').find_next_sibling('span').text
            else:
                ownership = None
            if soup.find('span',string='Bathrooms'):
                Bathrooms = soup.find('span',string='Bathrooms').find_next_sibling('span').text
            else:
                Bathrooms = None
            PrivateGarden = 'No'
            for span in soup.find_all("span"):
                text = span.get_text(separator=" ", strip=True)
                if "Private Garden" in text:
                    PrivateGarden = 'Yes'   
            data.append({'Area':Area,'Payment':payment,'Ownership':ownership,'Status':status,'Bedrooms':Bedrooms,'Bathrooms':Bathrooms,'PrivateGarden':PrivateGarden,'price':price})
    df = pd.DataFrame(data)
    df.to_csv('data/Apartments.csv',index=False)
    logging.info("Data collection completed successfully")

if __name__ == "__main__":
    collect_data()

