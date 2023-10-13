from types import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import scraper.constants as const
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper.airbnb_room import AirbnbRoom
class Airbnb(webdriver.Chrome):
    def __init__(self, options: Options = None, service: Service = None, keep_alive: bool = True, teardown = False) -> None:
        super().__init__(options, service, keep_alive)
        self.maximize_window()
        self.teardown = teardown
        
    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None):
        if self.teardown:
            self.quit()
            
    def load_main_page(self):
        self.get(const.BASE_URL)
        
    def select_destination(self, destination):
        anywhere_btn = WebDriverWait(self, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[text()="Anywhere"]'))
        )
        anywhere_btn.click()
        
        search_field = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.ID, 'bigsearch-query-location-input'))
        )
        search_field.send_keys(destination)
        time.sleep(5)
        first_result = self.find_element(by=By.ID, value="bigsearch-query-location-suggestion-0")
        first_result.click()
    
    ## mm/dd/yyyy
    def select_dates(self, checkin_date, checkout_date):
        checkin_element = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'div[data-testid="calendar-day-{checkin_date}"]'))
        )
        checkin_element.click()
        
        checkout_element = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'div[data-testid="calendar-day-{checkout_date}"]'))
        )
        checkout_element.click()

    def select_guests(self, adults=0, children=0, infants=0, pets=0):
        occupation_element = self.find_element(by=By.CSS_SELECTOR, value='div[data-testid="structured-search-input-field-guests-button"]')
        occupation_element.click()
        
        while True:
            adults_count_element = int(self.find_element(by=By.CSS_SELECTOR, value='span[data-testid="stepper-adults-value"]').get_attribute('innerHTML').strip())
            children_count_element = int(self.find_element(by=By.CSS_SELECTOR, value='span[data-testid="stepper-children-value"]').get_attribute('innerHTML').strip())
            infants_count_element = int(self.find_element(by=By.CSS_SELECTOR, value='span[data-testid="stepper-infants-value"]').get_attribute('innerHTML').strip())
            pets_count_element = int(self.find_element(by=By.CSS_SELECTOR, value='span[data-testid="stepper-pets-value"]').get_attribute('innerHTML').strip())
            if adults > adults_count_element:
                increase_btn = self.find_element(by=By.CSS_SELECTOR, value='button[data-testid="stepper-adults-increase-button"]')
                increase_btn.click()
            elif adults < adults_count_element:
                decrease_btn = self.find_element(by=By.CSS_SELECTOR, value='button[data-testid="stepper-adults-decrease-button"]')
                decrease_btn.click()
            
            if children > children_count_element:
                increase_btn = self.find_element(by=By.CSS_SELECTOR, value='button[data-testid="stepper-children-increase-button"]')
                increase_btn.click()
            elif children < children_count_element:
                decrease_btn = self.find_element(by=By.CSS_SELECTOR, value='button[data-testid="stepper-children-decrease-button"]')
                decrease_btn.click()
                
            if infants > infants_count_element:
                increase_btn = self.find_element(by=By.CSS_SELECTOR, value='button[data-testid="stepper-infants-increase-button"]')
                increase_btn.click()
            elif infants < infants_count_element:
                decrease_btn = self.find_element(by=By.CSS_SELECTOR, value='button[data-testid="stepper-infants-decrease-button"]')
                decrease_btn.click()
                
            if pets > pets_count_element:
                increase_btn = self.find_element(by=By.CSS_SELECTOR, value='button[data-testid="stepper-pets-increase-button"]')
                increase_btn.click()
            elif pets < pets_count_element:
                decrease_btn = self.find_element(by=By.CSS_SELECTOR, value='button[data-testid="stepper-pets-decrease-button"]')
                decrease_btn.click()
            
            if adults == adults_count_element and children == children_count_element and infants == infants_count_element and pets == pets_count_element:
                break
    
    def search_click(self):
        search_btn = self.find_element(by=By.CSS_SELECTOR, value='button[data-testid="structured-search-input-search-button"]')
        search_btn.click()
    
    def get_room_info(self):
        rooms = AirbnbRoom(driver=self)
            
            