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
        self.get_room_detail('www.airbnb.com/rooms/14128504?adults=1&category_tag=Tag%3A8678&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1594544502&search_mode=flex_destinations_search&check_in=2023-10-26&check_out=2023-10-31&source_impression_id=p3_1697183059_BCnPIi6Hcu%2Fibp8z&previous_page_section_name=1000')

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
                picture_url = item.find_element(by=By.CSS_SELECTOR, value='div[role="presentation"]').find_element(by=By.TAG_NAME, value='img').get_attribute('src')
                print(picture_url)
                # self.get_host_info()
                # self.get_room_detail(listing_url)
                
            try:
                next_btn = self.driver.find_element(by=By.CSS_SELECTOR, value='a[aria-label="Next"]')
                next_btn.click()
            except:
                break
        return collections


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

        # name = self.driver.find_element(by=By.TAG_NAME, value='h1').text
        # description = self.get_room_description()
        
        
        try:
            overview_section = self.driver.find_element(by=By.XPATH, value='//div[contains(@data-section-id, "OVERVIEW_DEFAULT")]')
            overviews = overview_section.find_element(by=By.TAG_NAME, value='ol').text.strip().split('·')
        except:
            overview_section = self.driver.find_element(by=By.XPATH, value='//div[@data-section-id="LISTING_INFO"]')
            overviews = overview_section.find_element(by=By.CSS_SELECTOR, value='ul').text
        print(overviews)
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
            review_section = self.driver.find_elements(by=By.CSS_SELECTOR, value='div[data-section-id="REVIEWS_DEFAULT"]')
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
        except:
            
            print('There is no review yet')
    
    def get_host_info(self):
        try:
            host_section = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-section-id="HOST_PROFILE_DEFAULT"]'))
            )
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
            host_section = WebDriverWait(self.driver, 10).until(
                EC. presence_of_element_located((By.CSS_SELECTOR, 'div[data-section-id="MEET_YOUR_HOST"]'))
            )
            
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
            
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[1])

    