import time
import csv

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options
chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--start-maximized")
driver = uc.Chrome(options=chrome_options)

# Load the OpenLibrary fiction search results page
driver.get("https://openlibrary.org/search?subject=Fiction")

# Initialize variables
books_collected = 0
max_books = 2000

# Open CSV file once for writing headers
with open("book_results.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Author"])  # Header row

while books_collected < max_books:
    # Find the results container
    results_wrapper = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, ".//div[@class='resultsContainer search-results-container']"))
    )

    # Scroll to the results and wait 5 seconds
    driver.execute_script("arguments[0].scrollIntoView(true);", results_wrapper)
    time.sleep(5)

    # Find all book wrappers
    book_items = results_wrapper.find_elements(By.XPATH, ".//div[@class='sri__main']")

    # Loop through each book
    for book in book_items:
        if books_collected >= max_books:
            break
        # Find Info
        try:
            title = book.find_element(By.XPATH, ".//h3[@class='booktitle']").text.strip()
            try:
                author = book.find_element(By.XPATH, ".//span[@class='bookauthor']").text.replace("by ", "").strip()
            except:
                author = "Unknown Author"

            # Append to CSV
            with open("book_results.csv", mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([title, author])

            print(f"Extracted data for '{title}' by {author}")
            books_collected += 1
        except Exception as e:
            print(f"Error extracting book: {e}")
            continue

    # Stop if we've reached 2000 books
    if books_collected >= max_books:
        print(f"Reached target: {books_collected} books collected.")
        break

    # Try to click the "Next" button
    try:
        next_button = driver.find_element(By.XPATH, ".//a[@class='ChoosePage' and contains(text(), 'Next')]")
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(5)  # Wait for the next page to load
    except Exception as e:
        print(f"Error clicking next button: {e}. Collected {books_collected} books so far.")
        break

# Close the driver with error handling
try:
    driver.quit()
except Exception as e:
    print(f"Error closing driver: {e}")

print(f"Finished. Total books collected: {books_collected}")