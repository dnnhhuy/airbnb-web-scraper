from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from scraper.utils import *
from scraper.airbnb_reviews import AirbnbReview
from scraper.airbnb_host import AirbnbHost
import pandas as pd

pd.set_option('display.max_columns', None)

class AirbnbRoom():
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.rooms_list = self.get_rooms_list()
        
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
                listing_url = listing_url.split('?')[0]
                picture_url = item.find_element(by=By.CSS_SELECTOR, value='div[role="presentation"]').find_element(by=By.TAG_NAME, value='img').get_attribute('src')
                
                collections.append([listing_url, picture_url])
            try:
                next_btn = self.driver.find_element(by=By.CSS_SELECTOR, value='a[aria-label="Next"]')
                next_btn.click()
                page += 1
            except:
                break
        return collections


    def get_room_description(self):
        try:
            description = WebDriverWait(self.driver, 10).until( 
                EC.visibility_of_element_located((By.XPATH, '//div[@data-section-id="DESCRIPTION_DEFAULT"]//span[starts-with(@class, "ll4r2nl")]'))
            ).get_attribute('innerHTML')
            description = remove_html_tags(description)
        except:
            description = ''
        return description       
    
    def get_amenities(self):
        amenities = [] 
        show_all_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@data-section-id="AMENITIES_DEFAULT"]//button[contains(text(), "Show all")]'))
        )
        show_all_btn.click()
        time.sleep(2)
        
        amenities_elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class^="twad414"]'))
        )
        for amenity in amenities_elements:
            if 'Unavailable' not in amenity.get_attribute('innerText'):
                amenities.append(amenity.get_attribute('innerText'))
        close_btn = self.driver.find_element(by=By.CSS_SELECTOR, value='button[aria-label="Close"]')
        close_btn.click()
        return amenities
    
    def get_room_detail(self, url, picture_url):
        listing_url = 'https://' + url
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(url=listing_url)
            
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Translation on"]'))
            )
            close_btn = self.driver.find_element(By.XPATH, '//div[@aria-label="Translation on"][@role="dialog"]//button[@aria-label="Close"]')
            close_btn.click()
        except:
            print('There is no notification to close')
        room_id = url.split('/')[-1]
        name = self.driver.find_element(by=By.XPATH, value='//div[@data-section-id="TITLE_DEFAULT"]//h1').get_attribute('innerText')
        description = self.get_room_description()
        try:
            overview_section = self.driver.find_element(by=By.XPATH, value='//div[contains(@data-section-id, "OVERVIEW_DEFAULT")]')
            overviews = overview_section.find_element(by=By.TAG_NAME, value='ol').get_attribute('innerText').strip().split('·')
        except:
            overview_section = self.driver.find_element(by=By.XPATH, value='//div[@data-section-id="LISTING_INFO"]')
            overviews = overview_section.find_element(by=By.CSS_SELECTOR, value='ul').get_attribute('innerText')
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
        review_score_rating, number_of_reviews, review_score_cleanliness, review_score_communication, review_score_checkin, review_score_accuracy, review_score_location, review_score_value, review_comments = self.get_room_review()
        host_id, host_url, host_name, host_about, host_is_superhost, host_listings_count, host_review_score, host_number_of_reviews, hosting_time, host_picture_url, host_identity_verified, host_response_time, host_response_rate, host_since = self.get_host_info()
        
        room_detail_df = pd.DataFrame(data=[[room_id, host_id, picture_url, name, description, accommodates, bedrooms, beds, bathrooms, amenities, price, review_score_rating, number_of_reviews, review_score_cleanliness, review_score_communication, review_score_checkin, review_score_accuracy, review_score_location, review_score_value]], columns=['room_id', 'host_id', 'picture_url', 'name', 'description', 'accommodates', 'bedrooms', 'beds', 'bathrooms', 'amenities', 'price', 'review_score_rating', 'number_of_reviews', 'review_score_cleanliness', 'review_score_communication', 'review_score_checkin', 'review_score_accuracy', 'review_score_location', 'review_score_value'])
        
        room_reviews_df = pd.DataFrame(data=review_comments, columns=['reviewer_id', 'reviewer_name', 'review_date', 'comment'])
        room_reviews_df['room_id'] = room_id
        room_reviews_df = room_reviews_df[['reviewer_id', 'room_id', 'reviewer_name', 'review_date', 'comment']]
        
        host_detail_df = pd.DataFrame(data=[[host_id, host_url, host_name, host_about, host_is_superhost, host_listings_count, host_review_score, host_number_of_reviews, hosting_time, host_picture_url, host_identity_verified, host_response_time, host_response_rate, host_since]], columns=['host_id', 'host_url', 'host_name', 'host_about', 'host_is_superhost', 'host_listings_count', 'host_review_score', 'host_number_of_reviews', 'hosting_time', 'host_picture_url', 'host_identity_verified', 'host_response_time', 'host_response_rate', 'host_since'])
        
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        return room_detail_df, room_reviews_df, host_detail_df
    
    def get_room_review(self):
        review_score_rating = ''
        number_of_reviews = 0
        review_score_cleanliness = ''
        review_score_communication = ''
        review_score_checkin = ''
        review_score_accuracy = ''
        review_score_location = ''
        review_score_value = ''
        review_comments = []
        
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
                reviews_modal = reviews.get_reviews_modal()
                review_score_cleanliness, review_score_communication, review_score_checkin, review_score_accuracy, review_score_location, review_score_value = reviews.get_review_score(reviews_modal)
                review_comments = reviews.get_reviews(reviews_modal)
                reviews.close_reviews_modal(reviews_modal)
            except:
                review_score_cleanliness, review_score_communication, review_score_checkin, review_score_accuracy, review_score_location, review_score_value = reviews.get_review_score_without_modal(review_section)
                review_comments = reviews.get_reviews_without_modal(number_of_reviews)
          
        return review_score_rating, number_of_reviews, review_score_cleanliness, review_score_communication, review_score_checkin, review_score_accuracy, review_score_location, review_score_value, review_comments
            
                        
    
    def get_host_info(self):
        host_response_time = ''
        host_response_rate = ''
        host_since = ''
        try:
            host_section = self.driver.find_element(by=By.CSS_SELECTOR, value='div[data-section-id="HOST_PROFILE_DEFAULT"]')
            try:
                host_response_time = host_section.find_element(by=By.XPATH, value='//*[text()="Response time"]').get_attribute('innerText')
            except:
                print('There is no host reponse time')
            try:
                host_response_rate = host_section.find_element(by=By.XPATH, value='//*[text()="Response rate"]').get_attribute('innerText')
            except:
                print('There is no host reponse rate')
            try:
                host_since = host_section.find_element(by=By.CSS_SELECTOR, value='div[class^="s9fngse"]').get_attribute('innerText')
            except:
                print('There is no host since')
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
        
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[1])
        return host_id, host_url, host_name, host_about, host_is_superhost, host_listings_count, host_review_score, host_number_of_reviews, hosting_time, host_picture_url, host_identity_verified, host_response_time, host_response_rate, host_since
       
        

    