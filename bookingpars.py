from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging

# Configurable parameters
OUTPUT_FILENAME = 'hotels.txt'
NUM_PAGES_TO_SCRAPE = 5

# Setup logging
logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def scrape_hotel_names(driver, page):
    # Use WebDriverWait to wait for the hotel names to load
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, f'button[aria-label=" {page}"]'), str(page))
    )

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all hotel names using the data-testid attribute
    hotel_names = [hotel.text for hotel in soup.select('div[data-testid="title"]')]
    
    return hotel_names


def write_hotel_names_to_file(hotel_names):
    try:
        # Append the hotel names into a text document
        with open(OUTPUT_FILENAME, 'a', encoding='utf-8') as f:
            for hotel_name in hotel_names:
                f.write(f'{hotel_name}\n')
    except Exception as e:
        logging.error(f"Error occurred while writing to file: {e}")
        print("Error occurred while writing to file. Check the log file for more details.")

def navigate_to_next_page(driver, page):
    try:
        # Check if the next page button exists
        next_page_buttons = driver.find_elements(By.CSS_SELECTOR, f'button[aria-label=" {page + 1}"]')

        if next_page_buttons:
            # If next page button exists, wait for it to be clickable and then click
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'button[aria-label=" {page + 1}"]'))
            )
            next_page_button = next_page_buttons[0]
            next_page_button.click()

            # Wait until the page has loaded completely
            WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, f'button[aria-label=" {page + 1}"]'), str(page + 1))
            )

            print(f"Navigated to page {page + 1}")
        else:
            # If next page button doesn't exist, we've reached the end of the pages
            print(f"Reached the end of the pages at page {page}. No more pages to navigate.")
            return
    except Exception as e:
        logging.error(f"Error occurred while navigating to next page: {e}")
        print("Error occurred while navigating to the next page. Check the log file for more details.")

def main():
    driver_path = r'C:\Users\Ilya\Downloads\chromedriver_win32\chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.add_argument(f"executable_path={driver_path}")
    
    with webdriver.Chrome(options=options) as driver:
        try:
            # Navigate to Booking.com
            driver.get('https://www.booking.com/')
            print("Opened Booking.com")

            # Wait for user to manually search and navigate to the page with the list of hotels
            input("Press Enter in the console after you have manually searched and the page with hotels is loaded...")
            
            for page in range(1, NUM_PAGES_TO_SCRAPE + 1):
                hotel_names = scrape_hotel_names(driver, page)
                write_hotel_names_to_file(hotel_names)
                navigate_to_next_page(driver, page)

        except Exception as e:
            logging.error(f"Unexpected error occurred: {e}")
            print("An unexpected error occurred. Check the log file for more details.")

        finally:
            driver.quit()

if __name__ == "__main__":
    main()
