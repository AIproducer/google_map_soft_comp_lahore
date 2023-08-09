from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Function to extract company information
def extract_company_info(driver, link_url):
    driver.get(link_url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    company_name = soup.find('h1', class_='DUwDvf lfPIob').text
    print("Company Name:", company_name)

    address_element = soup.find('button', {'data-item-id': 'address'})
    address = address_element.find('div', class_='Io6YTe').text.strip()
    print("Address:", address)

    website_element = soup.find('a', {'data-item-id': 'authority'})
    website_link = website_element['href'] if website_element else "Website link not found."
    print("Website:", website_link)

    phone_element = soup.find('button', {'data-item-id': 'phone:tel:03084926007'})
    phone_number = phone_element.find('div', class_='Io6YTe').text.strip() if phone_element else "Phone number not found."
    print("Phone Number:", phone_number)

    return company_name, website_link, phone_number, address, link_url

# Set up the webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Base URL for the product search
base_url = 'https://www.google.com/maps/search/software+house+lahore+pakistan/@31.4837737,74.2133143,11.75z?entry=ttu'

# Fetch the HTML content from the URL
driver.get(base_url)
html_content = driver.page_source
soup = BeautifulSoup(html_content, "html.parser")

company_divs = soup.find_all("div", class_="Nv2PK tH5CWc THOPZb")

# Lists to store company information
company_names = []
website_links = []
phone_numbers = []
addresses = []
google_links = []

for company_div in company_divs:
    anchor_element = company_div.find('a', class_='hfpxzc')
    if anchor_element is not None:
        link_url = anchor_element['href']
        print("Google Link:", link_url)

        # Extract company information using the helper function
        company_name, website_link, phone_number, address, google_link = extract_company_info(driver, link_url)

        # Append the data to the respective lists
        company_names.append(company_name)
        website_links.append(website_link)
        phone_numbers.append(phone_number)
        addresses.append(address)
        google_links.append(link_url)
    else:
        print("Link not found for this company.")

# Create a DataFrame to store the data
data = {
    'Company Name': company_names,
    'Website Link': website_links,
    'Phone Number': phone_numbers,
    'Address': addresses,
    'Google Link': google_links
}
df = pd.DataFrame(data)

# Print the DataFrame
print(df)

# Close the webdriver
driver.quit()