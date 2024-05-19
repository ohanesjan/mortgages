#%%
import requests
import urllib.request
from bs4 import BeautifulSoup

#%%
# URL of the webpage you want to scrape
url = r"https://www.funda.nl/zoeken/koop/?selected_area=%5B%22nl%22%5D"

# Send an HTTP GET request to the URL
response = requests.get(url)
print(response.content)

# response = urllib.request.urlopen(url).read()
# print(response.content)
#%%
# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.prettify())



    #print(soup)
    # Find all the listing elements on the page
    # listing_elements = soup.find_all('div', class_="border-light-2 mb-4 border-b pb-4")

    # listing_elements = soup.find_all( attrs={"data-test-id" : "search-result-item"})
    # listing_elements = soup.find_all( attrs={"data-test-id" : "search-result-item"})
    listing_elements = soup.find_all( 'p')
    
    # Extract and print location and price for each listing
    for element in listing_elements:
        print(element.string , end="\n"*2)
        # Extract location
        # title = element.find('span', class_='object-header__title').text.strip()
        # post_code_city = element.find('span', class_='object-header__subtitle fd-color-dark-3').text.strip()

        # # Extract price
        # price_element = element.find('div', class_='object-header__price')
        # price = price_element.text.strip() if price_element else "Price not available"

        # # Print location and price
        # print(f'Title : {title}, Location : {post_code_city}, Price : {price} \n')
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)


# %%
quites_url = "http://www.values.com/inspirational-quotes"

r = requests.get(quites_url)
   
# soup = BeautifulSoup(r.content, 'html5lib')
soup_q = BeautifulSoup(r.content, 'html.parser')

print(soup_q.prettify())


# %%

# Define the URL of the webpage to scrape
url = "https://www.funda.nl/zoeken/koop/?selected_area=%5B%22nl%22%5D"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all the listing elements
    # listings = soup.find_all('article', class_='search-result')

    listings = soup.find_all('div', {'data-test-id' : 'search-result-item'})

    # Iterate through each listing and extract the desired information
    for listing in listings:
        # Extract the price
        price = listing.find('p', {'data-test-id': 'price-sale'}).text.strip()
        
        # Extract the title
        title = listing.find('h2', {'data-test-id': 'street-name-house-number'}).text.strip()
        
        # Extract the location
        location = listing.find('div', {'data-test-id': 'postal-code-city'}).text.strip()
        
        # Print the extracted information
        print(f"Price: {price}")
        print(f"Title: {title}")
        print(f"Location: {location}")
        print()
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# %%
