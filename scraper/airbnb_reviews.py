from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import date, timedelta
import time
from selenium.webdriver.common.keys import Keys

class AirbnbReview():
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
    
    def get_reviews_modal(self):
        reviews_modal = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="modal-container"]'))
        )
        return reviews_modal

    def close_reviews_modal(self, reviews_modal: WebElement):
        close_btn = reviews_modal.find_element(by=By.CSS_SELECTOR, value='button[aria-label="Close"]')
        close_btn.click()
    
    def get_review_score(self, reviews_modal: WebElement):
        review_score_cleanliness = ''
        review_score_communication = ''
        review_score_checkin = ''
        review_score_accuracy = ''
        review_score_location = ''
        review_score_value = ''
        try:
            review_score_cleanliness = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Cleanliness"]/../following-sibling::div[contains(@class, "v1kb7fro")]').get_attribute('innerText')
            review_score_communication = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Communication"]/../following-sibling::div[contains(@class, "v1kb7fro")]').get_attribute('innerText')
            review_score_checkin = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Check-in"]/../following-sibling::div[contains(@class, "v1kb7fro")]').get_attribute('innerText')
            review_score_accuracy = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Accuracy"]/../following-sibling::div[contains(@class, "v1kb7fro")]').get_attribute('innerText')
            review_score_location = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Location"]/../following-sibling::div[contains(@class, "v1kb7fro")]').get_attribute('innerText')
            review_score_value = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Value"]/../following-sibling::div[contains(@class, "v1kb7fro")]').get_attribute('innerText')
        except:
            try: 
                review_score_cleanliness = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Cleanliness"]//following-sibling::div/descendant::span[@class="_n9tijb"]').get_attribute('innerText')
                review_score_communication = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Communication"]//following-sibling::div/descendant::span[@class="_n9tijb"]').get_attribute('innerText')
                review_score_checkin = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Check-in"]//following-sibling::div/descendant::span[@class="_n9tijb"]').get_attribute('innerText')
                review_score_accuracy = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Accuracy"]//following-sibling::div/descendant::span[@class="_n9tijb"]').get_attribute('innerText')
                review_score_location = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Location"]//following-sibling::div/descendant::span[@class="_n9tijb"]').get_attribute('innerText')
                review_score_value = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Value"]//following-sibling::div/descendant::span[@class="_n9tijb"]').get_attribute('innerText')
            except:
                print("There is no sub review scores")
        return review_score_cleanliness, review_score_communication, review_score_checkin, review_score_accuracy, review_score_location, review_score_value

    def get_review_score_without_modal(self, review_section: WebElement):
        review_score_cleanliness = ''
        review_score_communication = ''
        review_score_checkin = ''
        review_score_accuracy = ''
        review_score_location = ''
        review_score_value = ''
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
        return review_score_cleanliness, review_score_communication, review_score_checkin, review_score_accuracy, review_score_location, review_score_value
    
    def scroll_down(self):
        """A method for scrolling the page."""

        # Get scroll height.
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:

            # Scroll down to the bottom.
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:

                break

            last_height = new_height
            
    def get_reviews(self, reviews_modal: WebElement):
        review_comments = []
        reviews = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="pdp-reviews-modal-scrollable-panel"]//div[starts-with(@class,"r1are2x1")]'))
        )
        
        # Scroll to the end of review page
        while True: 
            self.driver.execute_script("arguments[0].scrollIntoView();", reviews[-1])
            time.sleep(1)
            new_reviews = reviews_modal.find_elements(by=By.XPATH, value='//div[@data-testid="pdp-reviews-modal-scrollable-panel"]//div[starts-with(@class,"r1are2x1")]')
            if len(new_reviews) > len(reviews):
                reviews = new_reviews
            else:
                break
                
        reviews = reviews_modal.find_elements(by=By.XPATH, value='//div[@data-testid="pdp-reviews-modal-scrollable-panel"]//div[starts-with(@class,"r1are2x1")]')
        for review in reviews:
            reviewer_id = review.find_element(by=By.CSS_SELECTOR, value='a[class^="_9bezani"]').get_attribute('href').split('/')[-1]
            reviewer_name = review.find_element(by=By.CSS_SELECTOR, value='h3[class^="hpipapi"]').get_attribute('innerText')
            try:
                review_date = review.find_element(by=By.CSS_SELECTOR, value='li[class="_1f1oir5"]').get_attribute('innerText')
            except:
                review_date = review.find_element(By.CSS_SELECTOR, value='div[class^="s1joulhb"]').get_attribute('innerText').split('\n')[-1]
                if 'day' in review_date:
                    days = review_date.split(' ')[0]
                    review_date = (date.today() - timedelta(days=int(days))).strftime("%B %Y")
                elif 'week' in review_date:
                    weeks = review_date.split(' ')[0]
                    review_date = (date.today() - timedelta(weeks=int(weeks))).strftime("%B %Y")
                elif 'month' in review_date:
                    month = review_date.split(' ')[0]
                    review_date = (date.today() - timedelta(month=int(month))).strftime("%B %Y")
                    
            comment = review.find_element(by=By.CSS_SELECTOR, value='span[class^="ll4r2nl"]').get_attribute('innerText')
            review_comments.append([reviewer_id, reviewer_name, review_date, comment])
        return review_comments

    def get_reviews_without_modal(self, number_of_reviews):
        review_comments = []
        reviews = self.driver.find_elements(by=By.XPATH, value='//div[@data-section-id="REVIEWS_DEFAULT"]//div[@role="list"]//div[@role="listitem"]')
        for review in reviews:
            reviewer_id = review.find_element(by=By.CSS_SELECTOR, value='a[class^="_9bezani"]').get_attribute('href').split('/')[-1]
            reviewer_name = review.find_element(by=By.CSS_SELECTOR, value='h3[class^="hpipapi"]').get_attribute('innerText')
            try:
                review_date = review.find_element(by=By.CSS_SELECTOR, value='li[class="_1f1oir5"]').get_attribute('innerText')
            except:
                review_date = review.find_element(By.CSS_SELECTOR, value='div[class^="s1joulhb"]').get_attribute('innerText').split('\n')[-1]
                if 'day' in review_date:
                    days = review_date.split(' ')[0]
                    review_date = (date.today() - timedelta(days=int(days))).strftime("%B %Y")
                elif 'week' in review_date:
                    weeks = review_date.split(' ')[0]
                    review_date = (date.today() - timedelta(weeks=int(weeks))).strftime("%B %Y")
                elif 'month' in review_date:
                    month = review_date.split(' ')[0]
                    review_date = (date.today() - timedelta(month=int(month))).strftime("%B %Y")
            
            comment = review.find_element(by=By.CSS_SELECTOR, value='span[class^="ll4r2nl"]').get_attribute('innerText')
            review_comments.append([reviewer_id, reviewer_name, review_date, comment])
        return review_comments