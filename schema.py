from pyspark.sql.types import *
schema = {
    'host_detail': StructType([
        StructField('host_id', LongType(), False),
        StructField('host_url', StringType(), True),
        StructField('host_name', StringType(), True),
        StructField('host_about', StringType(), True),
        StructField('host_is_superhost', BooleanType(), False),
        StructField('host_listings_count', IntegerType(), False),
        StructField('host_review_score', FloatType(), True),
        StructField('host_number_of_reviews', IntegerType(), True),
        StructField('hosting_time', StringType(), True),
        StructField('host_picture_url', StringType(), True),
        StructField('host_identity_verified', BooleanType(), True)
    ]),
    'room_detail': StructType([
        StructField('room_id', LongType(), False),
        StructField('host_id', LongType(), False),
        StructField('picture_url', StringType(), True),
        StructField('name', StringType(), True),
        StructField('description', StringType(), True),
        StructField('accommodates', StringType(), True),
        StructField('bedrooms', StringType(), True),
        StructField('beds', StringType(), True),
        StructField('bathrooms', StringType(), True),
        StructField('amenities', StringType(), True),
        StructField('price', StringType(), True),
        StructField('review_score_rating', StringType(), True),
        StructField('number_of_reviews', StringType(), True),
        StructField('review_score_clealiness', StringType(), True),
        StructField('review_score_communication', StringType(), True),
        StructField('review_score_checkin',StringType(), True),
        StructField('review_score_location', StringType(), True),
        StructField('review_score_value', StringType(), True)
    ]),
    'room_reviews': StructType([
        StructField('reviewer_id', LongType(), False),
        StructField('room_id', LongType(), False),
        StructField('rerviewer_name', StringType(), True),
        StructField('review_date', StringType(), True),
        StructField('comment', StringType(), True)
    ])
}