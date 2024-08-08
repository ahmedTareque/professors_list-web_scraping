import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

# Step 1: Request the webpage
url = "https://www.ou.edu/coe/cs/people/faculty"
# page_to_scrape = requests.get(url)

# Set up Selenium
driver = webdriver.Chrome()  # or whichever browser you are using
driver.get(url)

# Let JavaScript load the content
driver.implicitly_wait(10)

# Step 2: Parse the webpage content
soup = BeautifulSoup(driver.page_source, "html.parser")

# Step 3: Find and extract relevant data
# This assumes the structure is similar to the example you provided. Adjust selectors as needed.

# Step 3: Find and extract relevant data
professors = []

# Assuming each professor's card is within a 'div' with class 'card-profile'
cards = soup.find_all("div", class_=["card-profile", "card card-profile adjunta p-5"])

# If using only the more general class doesn't work, try both selectors.
# cards = soup.select("div.card-profile, div.card.card-profile.adjunta.p-5")

for card in cards:
    name = card.find("div", class_="card-title").get_text(strip=True) if card.find("div", class_="card-title") else "null"
    title = card.find("div", class_="card-description").find("p").get_text(strip=True) if card.find("div", class_="card-description") else "null"
    email = card.find("div", class_="card-description").find_all("p")[1].get_text(strip=True) if len(card.find("div", class_="card-description").find_all("p")) > 1 else "null"
    website = card.find("div", class_="card-description").find_all("p")[2].get_text(strip=True) if len(card.find("div", class_="card-description").find_all("p")) > 2 else "null"
    research_focus = ", ".join([li.get_text(strip=True) for li in card.find("ul").find_all("li")]) if card.find("ul") else "null"

    professors.append([name, title, email, website, research_focus])

# Step 4: Create a DataFrame
df = pd.DataFrame(professors, columns=["Name", "Title", "Email", "Website", "Research Focus"])

# Step 5: Save to Excel
df.to_excel("professors.xlsx", index=False)

print("Data has been saved to professors.xlsx")