from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import date, timedelta
class AirbnbReview():
    def __init__(self, driver: WebDriver, reviews_popup: WebElement) -> None:
        self.driver = driver
        self.review_popup = reviews_popup
    
    def get_review_score(self):
        review_score_rating = ''
        number_of_reviews = ''
        review_score_cleanliness = ''
        review_score_communication = ''
        review_score_checkin = ''
        review_score_accuracy = ''
        review_score_location = ''
        review_score_value = ''
        try:
            review_score_rating = self.review_popup.find_element(by=By.CLASS_NAME, value='_1hiur72m').get_attribute('innerHTML').strip()
            number_of_reviews = self.review_popup.find_element(by=By.CLASS_NAME, value='_il5oc7').get_attribute('innerHTML').strip().split(' ')[0]
            try:
                review_score_cleanliness = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Cleanliness"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
                review_score_communication = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Communication"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
                review_score_checkin = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Check-in"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
                review_score_accuracy = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Accuracy"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
                review_score_location = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Location"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
                review_score_value = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Value"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
            except:
                print("There is no sub review scores")
        except:
            review_stats = self.review_popup.find_element(by=By.CSS_SELECTOR, value='div[class="_19wpxkk"]')
            review_score_rating, number_of_reviews = review_stats.text.split('·')
            number_of_reviews = number_of_reviews.split(' ')[1]
            try:    
                review_score_cleanliness = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Cleanliness"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
                review_score_communication = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Communication"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
                review_score_checkin = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Check-in"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
                review_score_accuracy = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Accuracy"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
                review_score_location = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Location"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
                review_score_value = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Value"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
            except:
                print("There is no sub review scores")
        return review_score_rating, number_of_reviews, review_score_cleanliness, review_score_communication, review_score_checkin, review_score_accuracy, review_score_location, review_score_value
    
    def get_reviews(self, number_of_reviews):
        review_comments = []
        reviews = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="pdp-reviews-modal-scrollable-panel"]//div[starts-with(@class,"r1are2x1")]'))
        )
        # Get total number of reviews
        while len(reviews) < int(number_of_reviews):
            self.driver.execute_script("arguments[0].scrollIntoView();", reviews[-1])
            reviews = self.review_popup.find_elements(by=By.XPATH, value='//div[@data-testid="pdp-reviews-modal-scrollable-panel"]//div[starts-with(@class,"r1are2x1")]')
            
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