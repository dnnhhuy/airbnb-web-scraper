from scraper.airbnb_scraper import Airbnb
from selenium import webdriver
from datetime import date, timedelta

from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.types import *
from delta import *
from delta.pip_utils import configure_spark_with_delta_pip

conf = SparkConf()
conf.set('spark.jars.packages', "io.delta:delta-core_2.12:2.3.0")
conf.set("spark.sql.warehouse.dir", "hdfs://namenode:9000/spark-warehouse")
conf.set("spark.cores.max", 2)
conf.set("spark.driver.memory", "4g")
conf.set("spark.executor.memory", "4g")
conf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
spark = SparkSession.builder \
    .master('spark://spark-master:7077') \
    .appName('DeltaLake') \
    .config(conf=conf)
    
spark = configure_spark_with_delta_pip(spark).getOrCreate()

spark.sparkContext.setLogLevel("ERROR")
# spark.sparkContext.addPyFile("/src/scraper/airbnb_scraper.py")
# spark.sparkContext.addPyFile("/src/schema.py")

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    with Airbnb(options=options, teardown=True) as bot:
        # bot.load_main_page()
        # bot.select_destination("Da Lat")
        # bot.select_dates((date.today() + timedelta(days=3)).strftime("%m/%d/%Y"), (date.today() + timedelta(days=5)).strftime("%m/%d/%Y"))
        # bot.select_guests(2, 0, 0, 0)
        # bot.search_click()
        room_detail_df, room_reviews_df, host_detail_df = bot.get_room_info()
        
        room_detail_df.iteritems = room_detail_df.items
        room_detail_df = spark.createDataFrame(room_detail_df)
        
        room_reviews_df.iteritems = room_reviews_df.items
        room_reviews_df = spark.createDataFrame(room_reviews_df)
        
        host_detail_df.iteritems = host_detail_df.items
        host_detail_df = spark.createDataFrame(host_detail_df)
        
        room_detail_df.show()
        room_reviews_df.show()
        host_detail_df.show()
    