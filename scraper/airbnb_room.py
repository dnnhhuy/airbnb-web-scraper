from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from scraper.utils import *
from scraper.airbnb_reviews import AirbnbReview
class AirbnbRoom():
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        # self.rooms_list = self.get_rooms_list()
        self.get_room_detail('www.airbnb.com/rooms/47009789?adults=2&check_in=2023-10-15&check_out=2023-10-17&source_impression_id=p3_1697094632_2op7KtQg6uD10TcO&previous_page_section_name=1000')
    
    def get_rooms_list(self):
        collections = []
        while True:
            WebDriverWait(self.driver, 3600).until(
                lambda method: len(self.driver.find_elements(by=By.CSS_SELECTOR, value='div[itemprop="itemListElement"]')) > 1
            )
            items = self.driver.find_elements(by=By.CSS_SELECTOR, value='div[itemprop="itemListElement"]')
            for item in items:
                name = item.find_element(by=By.CSS_SELECTOR, value='meta[itemprop="name"]').get_attribute('content')
                listing_url = item.find_element(by=By.CSS_SELECTOR, value='meta[itemprop="url"]').get_attribute('content')
                self.get_room_detail(listing_url)
            try:
                next_btn = self.driver.find_element(by=By.CSS_SELECTOR, value='a[aria-label="Next"]')
                next_btn.click()
            except:
                break
        return collections

    def check_room_superhost(self):
        try:
            self.driver.find_element(by=By.XPATH, value='//*[text()="Superhost"]')
            host_is_superhost = True
        except:
            host_is_superhost = False
        return host_is_superhost

    def get_room_description(self):
        description_section = self.driver.find_element(by=By.CSS_SELECTOR, value='div[data-section-id="DESCRIPTION_DEFAULT"]')
        description = description_section.find_element(by=By.XPATH, value='//div[@data-section-id="DESCRIPTION_DEFAULT"]/div[1]/div/span/span').get_attribute('innerHTML').strip()
        description = remove_html_tags(description)
        return description       
    
    def get_amenities(self):
        amenities = [] 
        show_all_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Show all")]'))
        )
        show_all_btn.click()
        time.sleep(3)
        amenities_elements = self.driver.find_elements(by=By.CSS_SELECTOR, value='div[class^="twad414"]')
        for amenity in amenities_elements:
            if 'Unavailable' not in amenity.text:
                amenities.append(amenity)
        close_btn = self.driver.find_element(by=By.CSS_SELECTOR, value='button[aria-label="Close"]')
        close_btn.click()
        return amenities
    
    def get_room_detail(self, url):
        listing_url = 'https://' + url
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(url=listing_url)
            
        try:
            close_btn = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Close"]'))
            )
            close_btn.click()
        except:
            print('There is no notification to close')

        name = self.driver.find_element(by=By.TAG_NAME, value='h1').text
        description = self.get_room_description()
        host_is_superhost = self.check_room_superhost()
        
        overviews = self.driver.find_element(by=By.XPATH, value='//div[@data-section-id="OVERVIEW_DEFAULT"]//ol').text.strip().split('·')
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
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
    
    def get_room_review(self):
        review_section = self.driver.find_elements(by=By.CSS_SELECTOR, value='div[data-section-id="REVIEWS_DEFAULT"]')
        if len(review_section) > 0:
            review_show_all_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="pdp-show-all-reviews-button"]'))
            )
            review_show_all_btn.click()
            reviews_popup = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="modal-container"]'))
            )
            reviews = AirbnbReview(self.driver, reviews_popup)
            review_score_rating, number_of_reviews, review_score_cleanliness, review_score_communication, review_score_checkin, review_score_accuracy, review_score_location, review_score_value =reviews.get_review_score()
            results = reviews.get_reviews(number_of_reviews)
        else:
            review_score_rating = ''
            number_of_reviews = ''
            review_score_cleanliness = ''
            review_score_communication = ''
            review_score_checkin = ''
            review_score_accuracy = ''
            review_score_location = ''
            review_score_value = ''
            results = []
            print('There is no review yet')
    
    def get_host_info(self):
        
        
        