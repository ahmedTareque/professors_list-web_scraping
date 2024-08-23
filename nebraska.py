import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

# Step 1: Request the webpage
url = "https://computing.unl.edu/directory-group/"

# Set up Selenium
driver = webdriver.Chrome()  # or whichever browser you are using
driver.get(url)

# Let JavaScript load the content
driver.implicitly_wait(10)

# Step 2: Parse the webpage content
soup = BeautifulSoup(driver.page_source, "html.parser")

# Step 3: Find and extract relevant data
professors = []

# Assuming each professor's info is within a 'div' with class 'dcf-col dcf-mt-5 dcf-mb-5'
cards = soup.find_all("div", class_="dcf-col dcf-mt-5 dcf-mb-5")

for card in cards:
    name = card.find("h3").get_text(strip=True) if card.find("h3") else "null"
    title = card.find("span", class_="title").get_text(strip=True) if card.find("span", class_="title") else "null"
    email = card.find("span", class_="email").find("a").get_text(strip=True) if card.find("span", class_="email") else "null"
    phone = card.find("span", class_="phone").get_text(strip=True) if card.find("span", class_="phone") else "null"
    location = card.find("span", class_="location").get_text(strip=True) if card.find("span", class_="location") else "null"
    
    # Check for the publication link span
    publication_span = card.find("span", style="font-size:smaller")
    publication_href = publication_span.find("a")['href'] if publication_span and publication_span.find("a") else "null"
    
    professors.append([name, title, email, phone, location, publication_href])

# Step 4: Create a DataFrame
df = pd.DataFrame(professors, columns=["Name", "Title", "Email", "Phone", "Location", "Publications Link"])

# Step 5: Save to Excel
df.to_excel("University_of_Nebraska_Lincoln.xlsx", index=False)

print("Data has been saved to University_of_Nebraska_Lincoln.xlsx")
