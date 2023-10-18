from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.types import *
from delta import *
from delta.pip_utils import configure_spark_with_delta_pip
from schema import *

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
    .appName('Testing') \
    .config(conf=conf)
    
spark = configure_spark_with_delta_pip(spark).getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

df = spark.read.format('delta').load('hdfs://namenode:9000/spark-warehouse/room_reviews/')

df1 = df.groupBy('reviewer_id', 'room_id') \
    .count() \
    .where('count > 1')
df2 = df.join(df1, ['reviewer_id', 'room_id'])
df2.show()