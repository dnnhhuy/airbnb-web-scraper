from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from datetime import date, timedelta
class AirbnbReview():
    def __init__(self, driver: WebDriver, reviews_popup: WebElement) -> None:
        self.driver = driver
        self.review_popup = reviews_popup
    
    def get_review_score(self):
        try:
            review_score_rating = self.review_popup.find_element(by=By.CLASS_NAME, value='_1hiur72m').get_attribute('innerHTML').strip()
            number_of_reviews = self.review_popup.find_element(by=By.CLASS_NAME, value='_il5oc7').get_attribute('innerHTML').strip().split(' ')[0]
            review_score_cleanliness = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Cleanliness"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
            review_score_communication = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Communication"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
            review_score_checkin = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Check-in"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
            review_score_accuracy = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Accuracy"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
            review_score_location = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Location"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
            review_score_value = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Value"]/../following-sibling::div[contains(@class, "v1kb7fro")]').text
        except:
            review_stats = self.review_popup.find_element(by=By.CSS_SELECTOR, value='div[class="_19wpxkk"]')
            review_score_rating, number_of_reviews = review_stats.text.split('·')
            number_of_reviews = number_of_reviews.split(' ')[1]
            review_score_cleanliness = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Cleanliness"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
            review_score_communication = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Communication"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
            review_score_checkin = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Check-in"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
            review_score_accuracy = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Accuracy"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
            review_score_location = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Location"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
            review_score_value = self.review_popup.find_element(by=By.XPATH, value='//div[text()="Value"]//following-sibling::div/descendant::span[@class="_n9tijb"]').text
        return review_score_rating, number_of_reviews, review_score_cleanliness, review_score_communication, review_score_checkin, review_score_accuracy, review_score_location, review_score_value
    
    def get_reviews(self, number_of_reviews):
        results = []
        reviews_section = self.review_popup.find_element(by=By.CSS_SELECTOR, value='div[data-testid="pdp-reviews-modal-scrollable-panel"]')
        reviews = reviews_section.find_elements(by=By.CSS_SELECTOR, value='div[class^="r1are2x1"]')
        # Get total number of reviews
        while len(reviews) < int(number_of_reviews):
            self.driver.execute_script("arguments[0].scrollIntoView();", reviews[-1])
            reviews = reviews_section.find_elements(by=By.CSS_SELECTOR, value='div[class^="r1are2x1"]')
        
        for review in reviews:
            reviewer_name = review.find_element(by=By.CSS_SELECTOR, value='h3[class^="hpipapi"]').text
            review_date = review.find_elements(by=By.CSS_SELECTOR, value='li[class="_1f1oir5"]')
            if len(review_date) == 0:
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
            else:
                review_date = review_date[0].text
            comment = review.find_element(by=By.CSS_SELECTOR, value='span[class^="ll4r2nl"]').text
            results.append([reviewer_name, review_date, comment])
        return results