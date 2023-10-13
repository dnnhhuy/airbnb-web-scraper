from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
class AirbnbHost():
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        
    def get_host_name(self):
        host_name = self.driver.find_element(by=By.CSS_SELECTOR, value='span[class^="t1gpcl1t"]').text
        return host_name
    
    def get_host_about(self):
        try:
            readmore_btn = self.driver.find_element(by=By.XPATH, value='//button[text()="Read more"]')
            readmore_btn.click()
        except:
            print('There is no read more button')
        try:
            host_about = self.driver.find_element(by=By.CSS_SELECTOR, value='span[class="_1e2prbn"]').text
        except:
            host_about = ''
        return host_about
    
    def check_superhost(self):
        host_is_superhost = self.driver.find_element(by=By.CSS_SELECTOR, value='span[class^="s14m4l2n"]').text
        if host_is_superhost == 'Superhost':
            return True
        else:
            return False
        
    def get_host_listings_count(self):
        host_listings_count = self.driver.find_element(by=By.CSS_SELECTOR, value='div[id="listings-scroller-description"]').text
        host_listings_count = re.findall(r'\d+', host_listings_count)
        host_listings_count = max(host_listings_count)
        return host_listings_count
    
    def get_host_review_score(self):
        try:
            host_review_score = self.driver.find_element(by=By.CSS_SELECTOR, value='span[data-testid="Rating-stat-heading"]').text
        except:
            host_review_score = ''
        return host_review_score
    
    def get_host_number_of_reviews(self):
        try:
            host_number_of_reviews = self.driver.find_element(by=By.CSS_SELECTOR, value='span[data-testid="Reviews-stat-heading"]').text
        except:
            host_number_of_reviews = ''
        return host_number_of_reviews
    
    def get_hosting_time(self):
        hosting_time = self.driver.find_element(by=By.XPATH, value='//span[contains(text(),"hosting")]').text
        return hosting_time

    def get_host_picture_url(self):
        host_picture_url = self.driver.find_element(by=By.XPATH, value='//div[@role="img"][contains(@aria-label, "User Profile")]/picture/img').get_attribute('src')
        return host_picture_url
    def check_host_identity_verified(self):
        confirmed_section = self.driver.find_element(by=By.CSS_SELECTOR, value='div[class^="vz9l9w5"]')
        try:
            confirmed_section.find_element(by=By.XPATH, value='//*[text()="Identity"]')
            return True
        except:
            return False
        