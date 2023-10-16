from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from scraper.utils import *
from scraper.airbnb_reviews import AirbnbReview
from scraper.airbnb_host import AirbnbHost
class AirbnbRoom():
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        # self.rooms_list = self.get_rooms_list()
        self.room = self.get_room_detail('www.airbnb.com/rooms/863921875691552996?adults=2&check_in=2023-10-18&check_out=2023-10-20&source_impression_id=p3_1697352446_T5a2pPBA0VMdX%2FvG&previous_page_section_name=1000&federated_search_id=ad916579-4c7a-42b0-89ad-bedcc00bcf64')

    def get_rooms_list(self):
        collections = []
        page = 1
        while True:
            print("Page ", page)
            WebDriverWait(self.driver, 3600).until(
                lambda method: len(self.driver.find_elements(by=By.CSS_SELECTOR, value='div[itemprop="itemListElement"]')) > 1
            )
            items = self.driver.find_elements(by=By.CSS_SELECTOR, value='div[itemprop="itemListElement"]')
            for item in items:
                listing_url = item.find_element(by=By.CSS_SELECTOR, value='meta[itemprop="url"]').get_attribute('content')
                picture_url = item.find_element(by=By.CSS_SELECTOR, value='div[role="presentation"]').find_element(by=By.TAG_NAME, value='img').get_attribute('src')
                print(listing_url)
                self.get_room_detail(listing_url)
                
            try:
                next_btn = self.driver.find_element(by=By.CSS_SELECTOR, value='a[aria-label="Next"]')
                next_btn.click()
                page += 1
            except:
                break
        return collections


    def get_room_description(self):
        description = WebDriverWait(self.driver, 10).until( 
            EC.visibility_of_element_located((By.XPATH, '//div[@data-section-id="DESCRIPTION_DEFAULT"]//span[starts-with(@class, "ll4r2nl")]'))
        ).get_attribute('innerHTML')
        description = remove_html_tags(description)
        return description       
    
    def get_amenities(self):
        amenities = [] 
        show_all_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Show all")]'))
        )
        show_all_btn.click()
        amenities_elements = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class^="twad414"]'))
        )
        for amenity in amenities_elements:
            if 'Unavailable' not in amenity.text:
                amenities.append(amenity.text)
        close_btn = self.driver.find_element(by=By.CSS_SELECTOR, value='button[aria-label="Close"]')
        close_btn.click()
        return amenities
    
    def get_room_detail(self, url):
        listing_url = 'https://' + url
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(url=listing_url)
            
        try:
            translation_dialog = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Translation on"]'))
            )
            close_btn = self.driver.find_element(By.XPATH, '//div[@aria-label="Translation on"][@role="dialog"]//button[@aria-label="Close"]')
            close_btn.click()
        except:
            print('There is no notification to close')

        name = self.driver.find_element(by=By.TAG_NAME, value='h1').text
        description = self.get_room_description()
        try:
            overview_section = self.driver.find_element(by=By.XPATH, value='//div[contains(@data-section-id, "OVERVIEW_DEFAULT")]')
            overviews = overview_section.find_element(by=By.TAG_NAME, value='ol').text.strip().split('·')
        except:
            overview_section = self.driver.find_element(by=By.XPATH, value='//div[@data-section-id="LISTING_INFO"]')
            overviews = overview_section.find_element(by=By.CSS_SELECTOR, value='ul').text
        accommodates = ''
        bathrooms = ''
        bedrooms = ''
        beds = ''
        for overview in overviews:
            if 'guest' in overview:
                accommodates = overview
            if 'bedroom' in overview:
                bedrooms = overview
            if 'bed' in overview:
                beds = overview
            if 'bathroom' in overview:
                bathrooms = overview      
        amenities = self.get_amenities()
        price = self.driver.find_element(by=By.XPATH, value='//*[contains(text(), "per night")]').get_attribute('innerHTML').strip()
        self.get_room_review()
        self.get_host_info()
        # self.driver.close()
        # self.driver.switch_to.window(self.driver.window_handles[0])
    
    def get_room_review(self):
        review_score_rating = ''
        number_of_reviews = 0
        review_score_cleanliness = ''
        review_score_communication = ''
        review_score_checkin = ''
        review_score_accuracy = ''
        review_score_location = ''
        review_score_value = ''
        results = []
        
        try:
            review_section = self.driver.find_element(by=By.XPATH, value='//div[@data-section-id="REVIEWS_DEFAULT"]')
            review_stats = review_section.find_element(by=By.TAG_NAME, value="h2").get_attribute('innerText').split('\n')[1]
        except:
            review_section = self.driver.find_element(by=By.XPATH, value='//div[@data-section-id="REVIEWS_EMPTY_DEFAULT"]')
            review_stats = review_section.find_element(by=By.TAG_NAME, value="h2").get_attribute('innerText')
        
        if 'No reviews' in review_stats:
            print("There is no review yet")
        else:
            reviews = AirbnbReview(self.driver)
            if '·' in review_stats:
                review_score_rating, number_of_reviews = review_stats.split('·')
                number_of_reviews = number_of_reviews.split(' ')[1].split(' ')[0]
            else:
                number_of_reviews = review_stats.split(' ')[0]
            try:
                review_show_all_btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@data-section-id="REVIEWS_DEFAULT"]//button[1]'))
                )
                review_show_all_btn.click()
                
                review_score_cleanliness, review_score_communication, review_score_checkin, review_score_accuracy, review_score_location, review_score_value =reviews.get_review_score()
                review_comments = reviews.get_reviews(number_of_reviews)
                reviews.close_reviews_modal()
            except:
                try:
                    review_score_cleanliness = self.driver.find_element(by=By.XPATH, value='//div[@data-section-id="REVIEWS_DEFAULT"]//div[text()="Cleanliness"]//following-sibling::div').get_attribute('innerText')
                    review_score_communication = self.driver.find_element(by=By.XPATH, value='//div[@data-section-id="REVIEWS_DEFAULT"]//div[text()="Communication"]//following-sibling::div').get_attribute('innerText')
                    review_score_checkin = self.driver.find_element(by=By.XPATH, value='//div[@data-section-id="REVIEWS_DEFAULT"]//div[text()="Check-in"]//following-sibling::div').get_attribute('innerText')
                    review_score_accuracy = self.driver.find_element(by=By.XPATH, value='//div[@data-section-id="REVIEWS_DEFAULT"]//div[text()="Accuracy"]//following-sibling::div').get_attribute('innerText')
                    review_score_location = self.driver.find_element(by=By.XPATH, value='//div[@data-section-id="REVIEWS_DEFAULT"]//div[text()="Location"]//following-sibling::div').get_attribute('innerText')
                    review_score_value = self.driver.find_element(by=By.XPATH, value='//div[@data-section-id="REVIEWS_DEFAULT"]//div[text()="Value"]//following-sibling::div').get_attribute('innerText')
                except: 
                    try:
                        review_score_cleanliness = review_section.find_element(by=By.XPATH, value='//div[text()="Cleanliness"]//following-sibling::div/span').get_attribute('innerText')
                        review_score_communication = review_section.find_element(by=By.XPATH, value='//div[text()="Communication"]//following-sibling::div/span').get_attribute('innerText')
                        review_score_checkin = review_section.find_element(by=By.XPATH, value='//div[text()="Check-in"]//following-sibling::div/span').get_attribute('innerText')
                        review_score_accuracy = review_section.find_element(by=By.XPATH, value='//div[text()="Accuracy"]//following-sibling::div/span').get_attribute('innerText')
                        review_score_location = review_section.find_element(by=By.XPATH, value='//div[text()="Location"]//following-sibling::div/span').get_attribute('innerText')
                        review_score_value = review_section.find_element(by=By.XPATH, value='//div[text()="Value"]//following-sibling::div/span').get_attribute('innerText')
                    except:
                        print("This is no sub review scores")
                review_comments = reviews.get_reviews_no_modal(number_of_reviews)
            print(review_score_rating, number_of_reviews, review_score_cleanliness, review_score_communication, review_score_checkin, review_score_accuracy, review_score_location, review_score_value)
            print(review_comments)
            
                        
    
    def get_host_info(self):
        try:
            host_section = self.driver.find_element(by=By.CSS_SELECTOR, value='div[data-section-id="HOST_PROFILE_DEFAULT"]')
            try:
                host_response_time = host_section.find_element(by=By.XPATH, value='//*[text()="Response time"]').text
            except:
                host_response_time = ''
            try:
                host_response_rate = host_section.find_element(by=By.XPATH, value='//*[text()="Response rate"]').text
            except:
                host_response_rate = ''
            host_since = host_section.find_element(by=By.CSS_SELECTOR, value='div[class^="s9fngse"]').text
        except:
            host_section = self.driver.find_element(by=By.CSS_SELECTOR, value='div[data-section-id="MEET_YOUR_HOST"]')
            
        host_url = host_section.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
        host_id = host_url.split('/')[-1]
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[2])
        self.driver.get(url=host_url)
        
        host_detail = AirbnbHost(self.driver)
        host_name = host_detail.get_host_name()
        host_about = host_detail.get_host_about()
        host_is_superhost = host_detail.check_superhost()
        host_listings_count = host_detail.get_host_listings_count()
        host_review_score = host_detail.get_host_review_score()
        host_number_of_reviews = host_detail.get_host_number_of_reviews()
        hosting_time = host_detail.get_hosting_time()
        host_picture_url = host_detail.get_host_picture_url()
        host_identity_verified = host_detail.check_host_identity_verified()
        print(host_name, host_about, host_is_superhost, host_listings_count, host_review_score, host_number_of_reviews, hosting_time, host_picture_url, host_identity_verified)
            
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[1])

    