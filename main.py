from scraper.airbnb_scraper import Airbnb
from selenium import webdriver
from datetime import date, timedelta
if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    # options.add_argument("--headless")
    with Airbnb(options=options) as bot:
        bot.load_main_page()
        bot.select_destination("Da Lat")
        bot.select_dates((date.today() + timedelta(days=3)).strftime("%m/%d/%Y"), (date.today() + timedelta(days=5)).strftime("%m/%d/%Y"))
        # bot.select_guests(2, 0, 0, 0)
        bot.search_click()
        bot.get_room_info()
    