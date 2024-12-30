from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the target webpage
driver.get("https://ismir.net/conferences/ismir2017.html")  # Replace with the actual URL

# Find all <a> tags inside <strong> tags
links = driver.find_elements(By.XPATH, "//strong/a")
# Get the href attribute of each link
hrefs = [link.get_attribute("href") for link in links]
# print(f"Links: {hrefs}")


# Limit to the first 3 links
# links = links[:3]

# List to store article names and descriptions
articles = []

total_links = len(links)
# Iterate over each link
start_time = time.time()
for link, href in zip(links, hrefs):
    current_index = links.index(link) + 1
    percentage_complete = (current_index / total_links) * 100
    print("===>")
    print(f"Processing link {current_index} of {total_links} ({percentage_complete:.2f}% complete)")
    article_name = link.text
    print(article_name)
    link.click()
    time.sleep(2)  # Wait for the page to load

    # Extract the description text
    # description = driver.find_element(By.ID, "description").text
    try:
        # Extract the description text
        description = driver.find_element(By.ID, "description").text
    except NoSuchElementException:
        description = "Description not found"

    articles.append({"year": 2017, "name": article_name, "description": description, "url": href})
    print(description)

    # Go back to the main page
    driver.back()
    time.sleep(2)  # Wait for the page to load

# Close the WebDriver
driver.quit()

# Print the articles list
for article in articles:
    print(f"Article Name: {article['name']}")
    print(f"Description: {article['description']}\n")
    print(f"Url: {article['url']}\n")

# Save the articles list to a text file
with open("2017-ismir.json", "w") as json_file:
    json.dump(articles, json_file, indent=4)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time elapsed: {elapsed_time:.2f} seconds")