from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import date, timedelta
class AirbnbReview():
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
    
    def get_reviews_modal(self):
        reviews_modal = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="modal-container"]'))
        )
        return reviews_modal

    def close_reviews_modal(self, reviews_modal):
        close_btn = reviews_modal.find_element(by=By.CSS_SELECTOR, value='button[aria-label="Close"]')
        close_btn.click()
    
    def get_review_score(self, reviews_modal):
        review_score_cleanliness = ''
        review_score_communication = ''
        review_score_checkin = ''
        review_score_accuracy = ''
        review_score_location = ''
        review_score_value = ''
        try:
            review_score_cleanliness = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Cleanliness"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
            review_score_communication = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Communication"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
            review_score_checkin = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Check-in"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
            review_score_accuracy = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Accuracy"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
            review_score_location = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Location"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
            review_score_value = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Value"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
        except:
            try: 
                review_score_cleanliness = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Cleanliness"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
                review_score_communication = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Communication"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
                review_score_checkin = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Check-in"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
                review_score_accuracy = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Accuracy"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
                review_score_location = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Location"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
                review_score_value = reviews_modal.find_element(by=By.XPATH, value='//div[text()="Value"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
            except:
                print("There is no sub review scores")
        return review_score_cleanliness, review_score_communication, review_score_checkin, review_score_accuracy, review_score_location, review_score_value

    def get_review_score_without_modal(self, review_section):
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
    
    def get_reviews(self, number_of_reviews, reviews_modal):
        review_comments = []
        reviews = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="pdp-reviews-modal-scrollable-panel"]//div[starts-with(@class,"r1are2x1")]'))
        )
        # Get total number of reviews
        while len(reviews) < int(number_of_reviews):
            self.driver.execute_script("arguments[0].scrollIntoView();", reviews[-1])
            reviews = reviews_modal.find_elements(by=By.XPATH, value='//div[@data-testid="pdp-reviews-modal-scrollable-panel"]//div[starts-with(@class,"r1are2x1")]')
            
        for review in reviews:
            reviewer_name = review.find_element(by=By.CSS_SELECTOR, value='h3[class^="hpipapi"]').text
            try:
                review_date = review.find_element(by=By.CSS_SELECTOR, value='li[class="_1f1oir5"]').text
            except:
                review_date = review.find_element(By.CSS_SELECTOR, value='div[class^="s1joulhb"]').text.split('\n')[-1]
                if 'day' in review_date:
                    days = review_date.split(' ')[0]
                    review_date = (date.today() - timedelta(days=int(days))).strftime("%B %Y")
                elif 'week' in review_date:
                    weeks = review_date.split(' ')[0]
                    review_date = (date.today() - timedelta(weeks=int(weeks))).strftime("%B %Y")
                elif 'month' in review_date:
                    month = review_date.split(' ')[0]
                    review_date = (date.today() - timedelta(month=int(month))).strftime("%B %Y")
                    
            comment = review.find_element(by=By.CSS_SELECTOR, value='span[class^="ll4r2nl"]').text
            review_comments.append([reviewer_name, review_date, comment])
        return review_comments

    def get_reviews_no_modal(self, number_of_reviews):
        review_comments = []
        reviews = self.driver.find_elements(by=By.XPATH, value='//div[@data-section-id="REVIEWS_DEFAULT"]//div[@role="list"]//div[@role="listitem"]')
        for review in reviews:
            reviewer_name = review.find_element(by=By.CSS_SELECTOR, value='h3[class^="hpipapi"]').get_attribute('innerText')
            try:
                review_date = review.find_element(by=By.CSS_SELECTOR, value='li[class="_1f1oir5"]').text
            except:
                review_date = review.find_element(By.CSS_SELECTOR, value='div[class^="s1joulhb"]').text.split('\n')[-1]
                if 'day' in review_date:
                    days = review_date.split(' ')[0]
                    review_date = (date.today() - timedelta(days=int(days))).strftime("%B %Y")
                elif 'week' in review_date:
                    weeks = review_date.split(' ')[0]
                    review_date = (date.today() - timedelta(weeks=int(weeks))).strftime("%B %Y")
                elif 'month' in review_date:
                    month = review_date.split(' ')[0]
                    review_date = (date.today() - timedelta(month=int(month))).strftime("%B %Y")
            
            comment = review.find_element(by=By.CSS_SELECTOR, value='span[class^="ll4r2nl"]').text
            review_comments.append([reviewer_name, review_date, comment])
        return review_comments