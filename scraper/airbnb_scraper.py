from __future__ import annotations
from types import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import scraper.constants as const
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper.airbnb_room import AirbnbRoom
from delta import *
from schema import *

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
        try:
            anywhere_btn = WebDriverWait(self, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//*[text()="Anywhere"]'))
            )
            anywhere_btn.click()
        except:
            print("There is no anywhere button")
        
        search_field = WebDriverWait(self, 10).until(
            EC.visibility_of_element_located((By.ID, "bigsearch-query-location-input"))
        )
        search_field.send_keys(destination)
        first_result = WebDriverWait(self, 10).until(
            EC.visibility_of_element_located((By.ID, "bigsearch-query-location-suggestion-0"))
        )
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
    
    def get_rooms_info(self, spark=None):
        rooms = AirbnbRoom(driver=self)
        # room_detail_df, room_reviews_df, host_detail_df = rooms.get_room_detail('www.airbnb.com/rooms/654718042713876549?check_in=2023-10-21&check_out=2023-10-23&source_impression_id=p3_1697615793_Z24hCAImdE7MFu%2Bv&previous_page_section_name=1000', '')
        room_detail_delta_table = DeltaTable.forPath(spark, 'hdfs://namenode:9000/spark-warehouse/room_detail')
        room_reviews_delta_table = DeltaTable.forPath(spark, 'hdfs://namenode:9000/spark-warehouse/room_reviews')
        host_detail_delta_table = DeltaTable.forPath(spark, 'hdfs://namenode:9000/spark-warehouse/host_detail')
        
        for listing_url, picture_url in rooms.rooms_list:
            print(listing_url)
            room_detail_df, room_reviews_df, host_detail_df = rooms.get_room_detail(listing_url, picture_url)
            
            room_detail_df.iteritems = room_detail_df.items
            room_detail_df = spark.createDataFrame(room_detail_df)
            
            if len(room_reviews_df) > 0:
                room_reviews_df.iteritems = room_reviews_df.items
                room_reviews_df = spark.createDataFrame(room_reviews_df)
            else:
                room_reviews_df = spark.createDataFrame(data=[], schema=schema['room_reviews'])
            
            host_detail_df.iteritems = host_detail_df.items
            host_detail_df = spark.createDataFrame(host_detail_df)
            
            room_detail_delta_table.alias('oldTable') \
                .merge(room_detail_df.alias('newTable'), 'oldTable.room_id = newTable.room_id') \
                .whenMatchedUpdateAll() \
                .whenNotMatchedInsertAll() \
                .execute()
                    
            
            room_reviews_delta_table.alias('oldTable') \
                .merge(room_reviews_df.alias('newTable'), 'oldTable.reviewer_id = newTable.reviewer_id AND oldTable.room_id = newTable.room_id AND oldTable.review_date = newTable.review_date AND oldTable.comment = newTable.comment') \
                .whenMatchedUpdateAll() \
                .whenNotMatchedInsertAll() \
                .execute() \
            
            host_detail_delta_table.alias('oldTable') \
                .merge(host_detail_df.alias('newTable'), 'oldTable.host_id = newTable.host_id') \
                .whenMatchedUpdateAll() \
                .whenNotMatchedInsertAll() \
                .execute() \
                
        return None
        
            