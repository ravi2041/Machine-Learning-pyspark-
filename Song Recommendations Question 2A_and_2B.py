from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.mllib.stat import Statistics
import pandas as pd
from pyspark.sql.functions import udf
from pyspark.ml.feature import OneHotEncoderEstimator, StringIndexer, VectorAssembler
from pyspark.ml.feature import StringIndexer
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

# This will give a unique label to each genre. This label will be converted to int type later

df = user_song_combine

indexer = StringIndexer(inputCol="user_id", outputCol="user_label")
indexer_2 = StringIndexer(inputCol="song_id", outputCol="song_label")
indexed = indexer.fit(df).transform(df)
indexed_2 = indexer_2.fit(indexed).transform(indexed)

def to_int(x):
    return int(x)

udf_to_int = udf(to_int, IntegerType())
als_dataset = indexed_2.withColumn("user_label_int", udf_to_int("user_label")).withColumn("song_label_int", udf_to_int("song_label"))
#als_dataset.show(10, False)

als_dataset = als_dataset.drop("user_label").drop("song_label")


train, test = als_dataset.randomSplit([0.7, 0.3], seed = 2000)

# Used this method earlier to split the dataset and ensure 20% plays
# from pyspark.sql.functions import lit

# seed = 1000

# fractions = als_dataset.select("song_id").distinct().withColumn("fraction", lit(0.75)).rdd.collect()
# print(fractions)


# training = als_dataset.stat.sampleBy("song_id", fractions, seed)

# # 24678860

# test = als_dataset.join(train, on=["song_id","user_id"], how ="leftanti")

# test.count()

# # 8226879


# # 24678860

# test = als_dataset.join(train, on=["song_id","user_id"], how ="leftanti")


# Getting the distinct user
user_training = train.select("user_id").distinct() 

# Getting distinct user
user_testing_check = test.select("user_id").distinct()

# Subtracting unique users 
# We check if there is any distinct users which train or test doesnt have then we can find by subtracting train from test.
minus_user_id = user_training.subtract(user_testing_check)
#0


als = ALS(implicitPrefs=True, userCol="user_label_int", itemCol="song_label_int", ratingCol="count", coldStartStrategy="drop")
          
model = als.fit(train)

rawPredictions = model.transform(test)

def to_float(col):
    return float(col)

udf_to_float = udf(to_float, DoubleType())

predictions = rawPredictions\
    .withColumn("count", udf_to_float(rawPredictions["count"]))\
    .withColumn("prediction", udf_to_float(rawPredictions["prediction"]))

evaluator = RegressionEvaluator(metricName="rmse", labelCol="play_count", predictionCol="prediction")
# rmse = evaluator.evaluate(predictions)
# print("Root-mean-square error = " + str(rmse))

# Question 2 B.
# Predicting songs for a certain user


movies = als_dataset.select(als.getUserCol()).filter(als_dataset["user_label_int"].rlike("14[0-5]")).distinct()
movieSubSetRecs = model.recommendForUserSubset(movies, 10)
movieSubSetRecs.show(10, False)

# +--------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
# |user_label_int|recommendations                                                                                                                                                             |
# +--------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
# |143           |[[10, 0.7991416], [7, 0.77103287], [0, 0.7623659], [11, 0.75945157], [17, 0.7496676], [9, 0.6951245], [44, 0.67278486], [49, 0.66093284], [26, 0.655926], [109, 0.64585423]]|
# +--------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


