from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_amazon_reviews_selenium(url):
    options = webdriver.ChromeOptions()
    
    # ✅ Correctly set the Chrome binary location
    options.binary_location = "C:/chrome-win64/chrome.exe"  # Update this to match your actual Chrome path
    
    # ✅ Use an existing user profile to stay logged in
    options.add_argument(f"user-data-dir=C:/Users/thema/AppData/Local/Google/Chrome for Testing/User Data")  # Change to your actual user profile path
    options.add_argument("profile-directory=Default")  

    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")

    # ✅ Explicitly set ChromeDriver Path
    chromedriver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

    # ✅ Convert Product URL to Reviews URL
    if "dp/" in url:
        product_id = url.split("dp/")[1].split("/")[0]  
        reviews_url = f"https://www.amazon.com/product-reviews/{product_id}/"
    else:
        reviews_url = url  

    driver.get(reviews_url)

    # ✅ Wait for reviews to be visible
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//li[@data-hook="review"]'))
    )

    # ✅ Scroll to load all reviews
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  
    
    # ✅ Debugging: Save a screenshot
    driver.save_screenshot("amazon_screenshot.png")

    reviews = []

    while True:
        # ✅ Locate all review blocks correctly
        review_blocks = driver.find_elements(By.XPATH, '//li[@data-hook="review"]')

        for review_block in review_blocks:
            try:
                reviewer = review_block.find_element(By.XPATH, './/span[@class="a-profile-name"]').text
                rating = review_block.find_element(By.XPATH, './/i[@data-hook="review-star-rating"]').text
                review_text = review_block.find_element(By.XPATH, './/span[@data-hook="review-body"]').text
                date = review_block.find_element(By.XPATH, './/span[@data-hook="review-date"]').text

                reviews.append({
                    "Reviewer": reviewer,
                    "Rating": rating,
                    "Review": review_text,
                    "Date": date
                })
            except Exception as e:
                print(f"Skipping review due to error: {e}")

        # ✅ Click "Next Page" if available
        try:
            next_button = driver.find_element(By.XPATH, '//li[@class="a-last"]/a')
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(5)  
        except:
            break  

    driver.quit()

    # ✅ Save data to CSV
    df = pd.DataFrame(reviews)
    df.to_csv("Reviews.csv", index=False)
    print("Scraping completed! Reviews saved in 'Reviews.csv'")

if __name__ == '__main__':
    product_url = input("Enter Amazon Product URL: ")
    get_amazon_reviews_selenium(product_url)
