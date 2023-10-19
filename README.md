# Airbnb WebScraper
## Overview
This project scrapes data from Airbnb Website and stores data in data lake house hosted by HDFS. The code will walkthrough all of listing rooms which are searching's results and scrape all of information available on the room's page (e.g room name, room description, price, review scores, etc.)

## Tools & Technology
- [Selenium](https://www.selenium.dev/): is an open-source browser automation tools and libraries mainly used for scraping in this project.
- [Apache Spark](https://spark.apache.org/): distributed processing system used for transform and load data to data lakehouse
- [Apache Hadoop](https://hadoop.apache.org/): based storage system to store delta table
- [Delta Lake](https://delta.io/): open-source storage layer run on top of HDFS in this project to create transaction log for parquet data.

## Workflow
The project's workflow described as below:

![workflow](images/Selenium%20Workflow.jpg)

Selenium will load the main page, input several query in the search query specified in **main.py** (You're able to modify it as your preferences). Then it click the search button. It will scraping through all of listings available on all pages of the searching's result for the room's information, host's information and all reviews of the rooms. Then Spark come to be a part of transform data to dataframe and store data to data lakehouse built on HDFS.

## Demo
Demo for scraping data task:

![demo](images/ezgif.com-video-to-gif.gif)

## ER Diagram
The data scraped will have ER Diagram as below:

![er diagram](images/ER%20Diagram.jpg)

## Schema
This is the schema described results as tables:

![schema](images/Schema%20Diagram.jpg)

## Data Example

