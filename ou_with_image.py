import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from openpyxl import Workbook
from openpyxl.drawing.image import Image as OpenpyxlImage
from io import BytesIO

# Step 1: Request the webpage
url = "https://www.ou.edu/coe/cs/people/faculty"

# Set up Selenium
driver = webdriver.Chrome()  # or whichever browser you are using
driver.get(url)

# Let JavaScript load the content
driver.implicitly_wait(10)

# Step 2: Parse the webpage content
soup = BeautifulSoup(driver.page_source, "html.parser")

# Step 3: Find and extract relevant data
professors = []
cards = soup.find_all("div", class_=["card-profile", "card card-profile adjunta p-5"])

for card in cards:
    name = card.find("div", class_="card-title").get_text(strip=True) if card.find("div", class_="card-title") else "null"
    image_url = card.find("img", class_="card-avatar")['src'] if card.find("img", class_="card-avatar") else "null"
    title = card.find("div", class_="card-description").find("p").get_text(strip=True) if card.find("div", class_="card-description") else "null"
    email = card.find("div", class_="card-description").find_all("p")[1].get_text(strip=True) if len(card.find("div", class_="card-description").find_all("p")) > 1 else "null"
    website = card.find("div", class_="card-description").find_all("p")[2].get_text(strip=True) if len(card.find("div", class_="card-description").find_all("p")) > 2 else "null"
    research_focus = ", ".join([li.get_text(strip=True) for li in card.find("ul").find_all("li")]) if card.find("ul") else "null"

    professors.append([name, image_url, title, email, website, research_focus])

# Step 4: Create an Excel Workbook
wb = Workbook()
ws = wb.active
ws.title = "Professors"

# Add the headers
headers = ["Name", "Image", "Title", "Email", "Website", "Research Focus"]
ws.append(headers)

# Step 5: Add data and images to the Excel file
for idx, prof in enumerate(professors, start=2):
    ws.append(prof[:1] + prof[2:])  # Add all data except image URL
    image_url = prof[1]

    # Download and insert the image
    if image_url != "null":
        image_url_full = f"https://www.ou.edu{image_url}"
        image_response = requests.get(image_url_full)
        img = OpenpyxlImage(BytesIO(image_response.content))
        img.width, img.height = 100, 100  # Resize image to fit in cell
        ws.add_image(img, f"B{idx}")

# Step 6: Save the Excel file
wb.save("ou_with_images.xlsx")

print("Data has been saved to ou_with_images.xlsx")
