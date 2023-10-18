from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master('spark://spark-master:7077') \
    .appName('DeltaLake') \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.0.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.warehouse.dir", "hdfs://namenode:90000/spark-warehouse") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()