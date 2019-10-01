# Q2 (a) to (c) Audio Similairty

# Q2 (a) Three models - logistic regression, random forest, gradient boost

# Q2 (b) 

genre_with_methods_of_moments.count()
# Out[147]: 994623

genre_with_methods_of_moments.filter(genre_with_methods_of_moments.genre == "Electronic").count()
#Out[178]: 40027

#---- A UDF to select the rows which we want ---
# from pyspark.sql.functions import udf

def is_electronic(genre):

	if genre == "Electronic":
		return 1
	else:
		return 0

check_electronic =  udf(lambda x : is_electronic(x), IntegerType()) 

genre_with_electronic = genre_with_methods_of_moments\
                        .withColumn("Electronic", check_electronic(genre_with_methods_of_moments.genre))

#genre_with_electronic.groupby("Electronic").agg({"track_id" : "count"}).show()

# +----------+---------------+
# |Electronic|count(track_id)|
# +----------+---------------+
# |         1|          40027|
# |         0|         954596|
# +----------+---------------+


genre_with_electronic.groupby("genre").agg({"track_id" : "count"}).show()

# +--------------+---------------+
# |         genre|count(track_id)|
# +--------------+---------------+
# |        Stage |           1603|
# |         Vocal|           6064|
# |     Religious|           8720|
# |Easy_Listening|           1523|
# |    Electronic|          40027|
# |          Jazz|          17612|
# |         Blues|           6741|
# | International|          14047|
# |      Children|            457|
# |           RnB|          13854|
# |           Rap|          20566|
# |   Avant_Garde|            998|
# |         Latin|          17389|
# |          Folk|           5701|
# |      Pop_Rock|         232995|
# |       New Age|           3925|
# |     Classical|            541|
# |          null|         581330|
# |       Country|          11411|
# | Comedy_Spoken|           2051|
# +--------------+---------------+
# only showing top 20 rows


genre_electronic_withoutNull = genre_with_electronic.filter(genre_with_electronic["genre"].isNotNull())

#genre_electronic_withoutNull.count()
#Out[188]: 413293

#genre_electronic_withoutNull.groupby("Electronic").agg({"track_id" : "count"}).show()

# +----------+---------------+
# |Electronic|count(track_id)|
# +----------+---------------+
# |         1|          40027|
# |         0|         373266|
# +----------+---------------+

# class_balance ( 1 : 0) = 0.10723  or 10.7 %

# Saving the File for Models Ahead 

# genre_electronic_withoutNull.write.mode("overwrite").format("csv").option("compression", "snappy")\
#                   .mode("overwrite").save("hdfs:///user/jss109/outputs/assign_2/genre_electronic_withoutNull")
# genre_dataset_1 = spark.read.orc("hdfs:////user/jss109/outputs/assign_2/genre_electronic_withoutNull", header = 'true')

# genre_electronic_withoutNull.write.format("com.databricks.spark.csv")\
# .save('hdfs:///user/jss109/outputs/assign_2/genre_electronic_withoutNull.csv', header = 'true')
# # Total Observations of Tmax Tmin

genre_electronic_withoutNull = (
  spark.read.format("com.databricks.spark.csv")
  .option("header", "true")
  .option("inferSchema", "true")
  .load('hdfs:///user/jss109/outputs/assign_2/genre_electronic_withoutNull.csv')
  )

genre_electronic_withoutNull.dtypes


## ------ ML MODELS Ahead --------------

from pyspark.ml.classification import LogisticRegression, GBTClassifier, RandomForestClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer, IndexToString, VectorAssembler
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
from pyspark.sql import DataFrame
from pyspark import SparkContext, SQLContext
from pyspark.ml import Pipeline
from pyspark.sql.functions import udf
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

from pyspark.sql.types import *
from pyspark.sql import functions as F
from math import cos, asin, sqrt
from pyspark.sql.functions import *
from pyspark.sql.functions import udf
from pyspark.sql.functions import col, unix_timestamp, to_date

# -------------------------------------

genre_electronic_withoutNull_2 = genre_electronic_withoutNull.drop("track_id", "genre")

genre_dataset_headers = genre_electronic_withoutNull_2.schema.names

print(genre_dataset_headers)  
# # ['Method_of_Moments_Overall_Standard_Deviation_1',
#  'Method_of_Moments_Overall_Standard_Deviation_2',
#  'Method_of_Moments_Overall_Standard_Deviation_3',
#  'Method_of_Moments_Overall_Standard_Deviation_4',
#  'Method_of_Moments_Overall_Standard_Deviation_5',
#  'Method_of_Moments_Overall_Average_1',
#  'Method_of_Moments_Overall_Average_2',
#  'Method_of_Moments_Overall_Average_3',
#  'Method_of_Moments_Overall_Average_4',
#  'Method_of_Moments_Overall_Average_5',
#  'Electronic']

df = genre_electronic_withoutNull_2
df.dtypes
cols = df.columns

stages = []
label_stringIdx = StringIndexer(inputCol = 'Electronic', outputCol = 'label')
stages += [label_stringIdx]
numericCols = df.schema.names[0:-1]

assembler = VectorAssembler(inputCols=numericCols, outputCol="features")
stages += [assembler]


# from pyspark.ml import Pipeline

pipeline = Pipeline(stages = stages)
pipelineModel = pipeline.fit(df)
df = pipelineModel.transform(df)
selectedCols = ['label', 'features'] + cols
df = df.select(selectedCols)
df.printSchema()

# root
#  |-- label: double (nullable = false)
#  |-- features: vector (nullable = true)
#  |-- Method_of_Moments_Overall_Standard_Deviation_1: double (nullable = true)
#  |-- Method_of_Moments_Overall_Standard_Deviation_2: double (nullable = true)
#  |-- Method_of_Moments_Overall_Standard_Deviation_3: double (nullable = true)
#  |-- Method_of_Moments_Overall_Standard_Deviation_4: double (nullable = true)
#  |-- Method_of_Moments_Overall_Standard_Deviation_5: double (nullable = true)
#  |-- Method_of_Moments_Overall_Average_1: double (nullable = true)
#  |-- Method_of_Moments_Overall_Average_2: double (nullable = true)
#  |-- Method_of_Moments_Overall_Average_3: double (nullable = true)
#  |-- Method_of_Moments_Overall_Average_4: double (nullable = true)
#  |-- Method_of_Moments_Overall_Average_5: double (nullable = true)
#  |-- Electronic: integer (nullable = true)

# Splitting the dataset 

train_initial, test = df.randomSplit([0.7, 0.3], seed = 2018)
print("Training Dataset Count: " + str(train_initial.count()))
print("Test Dataset Count: " + str(test.count()))

# LR without any class balance, but different thresholds : 0.5, 0.3, 0.1

lr = LogisticRegression(featuresCol = 'features', labelCol = 'label')   # Vee - maxIter=10,regParam=0.3, elasticNetParam=0)

lrModel = lr.fit(train_initial)
predictions = lrModel.transform(test)
total = predictions.count()
#-----------------------

threshold = 0.5

def apply_custom_threshold(probability, threshold):
    return int(probability[1] > threshold)

apply_custom_threshold_udf = F.udf(lambda x: apply_custom_threshold(x, threshold), IntegerType())

temp = predictions.withColumn("customPrediction", apply_custom_threshold_udf(F.col("probability")))

nP = temp.filter((F.col('customPrediction') == 1)).count()
nN = temp.filter((F.col('customPrediction') == 0)).count()
TP = temp.filter((F.col('customPrediction') == 1) & (F.col('label') == 1)).count()
FP = temp.filter((F.col('customPrediction') == 1) & (F.col('label') == 0)).count()
FN = temp.filter((F.col('customPrediction') == 0) & (F.col('label') == 1)).count()
TN = temp.filter((F.col('customPrediction') == 0) & (F.col('label') == 0)).count()

print('With threshold =  {}'.format(threshold))
print('num positive: {}'.format(nP))
print('num negative: {}'.format(nN))
print('precision: {}'.format(TP / (TP + FP)))
print('recall: {}'.format(TP / (TP + FN)))
print('accuracy: {}'.format((TP + TN) / total))
print('f1 : {}'. format(2 /  (  1/(TP / (TP + FN))  +  1/ (TP / (TP + FP))  ) ) )

binary_evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction", labelCol="label", metricName="areaUnderROC")
auroc = binary_evaluator.evaluate(predictions)
print('auroc: {}'.format(auroc))

#----------------------

# Training Dataset Count: 289224
# Test Dataset Count: 124069
# With threshold =  0.5
# num positive: 280
# num negative: 123783
# precision: 0.44642857142857145
# recall: 0.010406260406260406
# accuracy: 0.9029364113394002
# f1 : 0.020338431500162707
# auroc: 0.7030882946470611



##############Random Forest Without Class balance################################

labelIndexer = StringIndexer(inputCol="label", outputCol="indexedLabel").fit(df)

featureIndexer =\
    VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4).fit(df)

rf = RandomForestClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", numTrees=200 ,impurity='gini')

# Convert indexed labels back to original labels.
labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel",
                               labels=labelIndexer.labels)

# Chain indexers and forest in a Pipeline
pipeline = Pipeline(stages=[labelIndexer, featureIndexer, rf, labelConverter])

# Train model.  This also runs the indexers.
model = pipeline.fit(train_initial)

# Make predictions.
predictions = model.transform(test)

# Metrics

threshold = 0.5  

def apply_custom_threshold(probability, threshold):
    return int(probability[1] > threshold)

apply_custom_threshold_udf = F.udf(lambda x: apply_custom_threshold(x, threshold), IntegerType())

temp = predictions.withColumn("customPrediction", apply_custom_threshold_udf(F.col("probability")))

nP = temp.filter((F.col('customPrediction') == 1)).count()
nN = temp.filter((F.col('customPrediction') == 0)).count()
TP = temp.filter((F.col('customPrediction') == 1) & (F.col('label') == 1)).count()
FP = temp.filter((F.col('customPrediction') == 1) & (F.col('label') == 0)).count()
FN = temp.filter((F.col('customPrediction') == 0) & (F.col('label') == 1)).count()
TN = temp.filter((F.col('customPrediction') == 0) & (F.col('label') == 0)).count()

print('With threshold =  {}'.format(threshold))
print('num positive: {}'.format(nP))
print('num negative: {}'.format(nN))
print('precision: {}'.format(TP / (TP + FP)))
print('recall: {}'.format(TP / (TP + FN)))
print('accuracy: {}'.format((TP + TN) / total))
print('f1 : {}'. format(2/(  1/(TP / (TP + FN))  +  1/ (TP / (TP + FP))    )))

binary_evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction", labelCol="label", metricName="areaUnderROC")
auroc = binary_evaluator.evaluate(predictions)
print('auroc: {}'.format(auroc))

# With threshold =  0.5
# num positive: 7
# num negative: 124056
# precision: 0.42857142857142855
# recall: 0.00024975024975024975
# accuracy: 0.9031701635459404
# f1 : 0.0004992095848240286
# auroc: 0.7732492416330565



########## Gradient Boost Algorithm#######################

gbt = GBTClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", maxIter=100, lossType='logistic')

# Chain indexers and GBT in a Pipeline
pipeline = Pipeline(stages=[labelIndexer, featureIndexer, gbt])

# Train model.  This also runs the indexers.
model = pipeline.fit(train_initial)             # using the original dataset without any class balance

# Make predictions.
predictions = model.transform(test)

# Select example rows to display.
# predictions.select("prediction", "indexedLabel", "features").show(5)

# Select (prediction, true label) and compute test error
evaluator = MulticlassClassificationEvaluator(
    labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test Error = %g" % (1.0 - accuracy))


total = predictions.count()
# ------------------------------------------------------------------------
threshold = 0.5    

def apply_custom_threshold(probability, threshold):
    return int(probability[1] > threshold)

apply_custom_threshold_udf = F.udf(lambda x: apply_custom_threshold(x, threshold), IntegerType())

temp = predictions.withColumn("customPrediction", apply_custom_threshold_udf(F.col("probability")))

nP = temp.filter((F.col('customPrediction') == 1)).count()
nN = temp.filter((F.col('customPrediction') == 0)).count()
TP = temp.filter((F.col('customPrediction') == 1) & (F.col('label') == 1)).count()
FP = temp.filter((F.col('customPrediction') == 1) & (F.col('label') == 0)).count()
FN = temp.filter((F.col('customPrediction') == 0) & (F.col('label') == 1)).count()
TN = temp.filter((F.col('customPrediction') == 0) & (F.col('label') == 0)).count()

print('With threshold =  {}'.format(threshold))
print('num positive: {}'.format(nP))
print('num negative: {}'.format(nN))
print('precision: {}'.format(TP / (TP + FP)))
print('recall: {}'.format(TP / (TP + FN)))
print('accuracy: {}'.format((TP + TN) / total))
print('f1 : {}'. format(2/(  1/(TP / (TP + FN))  +  1/ (TP / (TP + FP))    )))
binary_evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction", labelCol="label", metricName="areaUnderROC")
auroc = binary_evaluator.evaluate(predictions)
print('auroc: {}'.format(auroc))

# Test Error = 0.0935009
# With threshold =  0.5
# num positive: 2156
# num negative: 121907
# precision: 0.5955473098330241
# recall: 0.1068931068931069
# accuracy: 0.9064991173839098
# f1 : 0.18125352907961603
# auroc: 0.7971103532867686



# ------------ The Balancing Act : Balancing the dataset - Down & UP Sampling -------
# From here on :-

# train_initial   =  unbalanced training dataset (70% split from the original) 
# train_down           =  Down sampled training dataset. Detials below.
# train_up        =  Up sampled training dataet. Details below.

# test            =  unbalanced test dataset (30% split from the original)


# 1 : Down Sampling the training data -------------------------------------------

train_0 = train_initial.filter(train_initial["Electronic"] == 0)  
train_1 = train_initial.filter(train_initial["Electronic"] == 1)  

# Randomly removing 85% of '0' class  

more_0s, less_0s = train_0.randomSplit([0.85, 0.15], seed = 2000)
print("Less 0s count :", less_0s.count())
print("More 0s count:", more_0s.count())

# Merging 'less_electronic' and 'genre_1' to achieve a DF with above class balance

train_down = train_1.union(less_0s)
print("Down Sampled Dataset: 'train_down'")
train_down.groupby("Electronic").agg({"label" : "count"}).show()

# Down Sampled Dataset: 'train_down'
# +----------+------------+
# |Electronic|count(label)|
# +----------+------------+
# |         1|       28012|
# |         0|       39014|
# +----------+------------+

# Original Training Dataset Count: 289490
# Balanced Training Dataset Count:  66991
# class_balance (total '1' / less count) =  27960 / (27960 + 39031) =   42 : 58 balance (1 : 0)

# Second : Up Sampling with replacement
# df_2.sample(withReplacement=True, 5.0, seed = 1)    # 5 x times
# ////  DOUBTS /////   Something wrong in this method ??

# train_up = train_initial.sample(True, 10.0, seed=99)   
# print("Up Sampled Dataset: 'train_up'")
# # train_up.groupby("Electronic").agg({"label" : "count"}).show()

# ---------------------------------- MODELS ---------------------------------------------------

# Logistic Regression ----

	# with down sampled training data
	# with up sampled training data
	# Both of the above with different thresholds

# 1. With down sampled data ---------------

# from pyspark.ml.classification import LogisticRegression

lr = LogisticRegression(featuresCol = 'features', labelCol = 'label', maxIter=10, regParam=0.3, elasticNetParam=0)

lrModel = lr.fit(train_down)
predictions = lrModel.transform(test)
total = predictions.count()

# Metrics

threshold = 0.5    

def apply_custom_threshold(probability, threshold):
    return int(probability[1] > threshold)

apply_custom_threshold_udf = F.udf(lambda x: apply_custom_threshold(x, threshold), IntegerType())

temp = predictions.withColumn("customPrediction", apply_custom_threshold_udf(F.col("probability")))

nP = temp.filter((F.col('customPrediction') == 1)).count()
nN = temp.filter((F.col('customPrediction') == 0)).count()
TP = temp.filter((F.col('customPrediction') == 1) & (F.col('label') == 1)).count()
FP = temp.filter((F.col('customPrediction') == 1) & (F.col('label') == 0)).count()
FN = temp.filter((F.col('customPrediction') == 0) & (F.col('label') == 1)).count()
TN = temp.filter((F.col('customPrediction') == 0) & (F.col('label') == 0)).count()

print('With threshold =  {}'.format(threshold))
print('num positive: {}'.format(nP))
print('num negative: {}'.format(nN))
print('precision: {}'.format(TP / (TP + FP)))
print('recall: {}'.format(TP / (TP + FN)))
print('accuracy: {}'.format((TP + TN) / total))
print('f1 : {}'. format(2/(  1/(TP / (TP + FN))  +  1/ (TP / (TP + FP))    )))

binary_evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction", labelCol="label", metricName="areaUnderROC")
auroc = binary_evaluator.evaluate(predictions)
print('auroc: {}'.format(auroc))

# With threshold =  0.5
# num positive: 15799
# num negative: 108270
# precision: 0.26704221786189
# recall: 0.3511444028297961
# accuracy: 0.8438288371793116
# f1 : 0.3033724023872869
# auroc: 0.7041354117646778


# MOdel 2 .------Random Forest Starts --------------------------------------------
# Train a RandomForest model.

labelIndexer = StringIndexer(inputCol="label", outputCol="indexedLabel").fit(df)

featureIndexer =\
    VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4).fit(df)

rf = RandomForestClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", numTrees=500 ,maxDepth=4,impurity='gini')

# Convert indexed labels back to original labels.
labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel",
                               labels=labelIndexer.labels)

# Chain indexers and forest in a Pipeline
pipeline = Pipeline(stages=[labelIndexer, featureIndexer, rf, labelConverter])

# Train model.  This also runs the indexers.
model = pipeline.fit(train_down)

# Make predictions.
predictions = model.transform(test)

# Metrics

threshold = 0.5  

def apply_custom_threshold(probability, threshold):
    return int(probability[1] > threshold)

apply_custom_threshold_udf = F.udf(lambda x: apply_custom_threshold(x, threshold), IntegerType())

temp = predictions.withColumn("customPrediction", apply_custom_threshold_udf(F.col("probability")))

nP = temp.filter((F.col('customPrediction') == 1)).count()
nN = temp.filter((F.col('customPrediction') == 0)).count()
TP = temp.filter((F.col('customPrediction') == 1) & (F.col('label') == 1)).count()
FP = temp.filter((F.col('customPrediction') == 1) & (F.col('label') == 0)).count()
FN = temp.filter((F.col('customPrediction') == 0) & (F.col('label') == 1)).count()
TN = temp.filter((F.col('customPrediction') == 0) & (F.col('label') == 0)).count()

print('With threshold =  {}'.format(threshold))
print('num positive: {}'.format(nP))
print('num negative: {}'.format(nN))
print('precision: {}'.format(TP / (TP + FP)))
print('recall: {}'.format(TP / (TP + FN)))
print('accuracy: {}'.format((TP + TN) / total))
print('f1 : {}'. format(2/(  1/(TP / (TP + FN))  +  1/ (TP / (TP + FP))    )))

binary_evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction", labelCol="label", metricName="areaUnderROC")
auroc = binary_evaluator.evaluate(predictions)
print('auroc: {}'.format(auroc))

# entropy and number of trees 100
# With threshold =  0.5
# num positive: 27623
# num negative: 96446
# precision: 0.24544763421786192
# recall: 0.5642946317103621
# accuracy: 0.7898105086685635
# f1 : 0.34209596851506135
# auroc: 0.7666364403952706

# gini and number of trees 200
# With threshold =  0.5
# num positive: 26546
# num negative: 97523
# precision: 0.2510359376177202
# recall: 0.5546400332917187
# accuracy: 0.7966212349579669
# f1 : 0.3456341899846996
# auroc: 0.7670755188697187



# Model 3 - GBT-----------------------------------------------------------------------

# Gradient Boost 
gbt = GBTClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", maxIter=100, lossType='logistic')

# Chain indexers and GBT in a Pipeline
pipeline = Pipeline(stages=[labelIndexer, featureIndexer, gbt])

# Train model.  This also runs the indexers.
model = pipeline.fit(train_down)             # using the original dataset without any class balance

# Make predictions.
predictions = model.transform(test)

# Select example rows to display.
# predictions.select("prediction", "indexedLabel", "features").show(5)

# Select (prediction, true label) and compute test error
evaluator = MulticlassClassificationEvaluator(
    labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test Error = %g" % (1.0 - accuracy))


total = predictions.count()
# ------------------------------------------------------------------------
threshold = 0.5    

def apply_custom_threshold(probability, threshold):
    return int(probability[1] > threshold)

apply_custom_threshold_udf = F.udf(lambda x: apply_custom_threshold(x, threshold), IntegerType())

temp = predictions.withColumn("customPrediction", apply_custom_threshold_udf(F.col("probability")))

nP = temp.filter((F.col('customPrediction') == 1)).count()
nN = temp.filter((F.col('customPrediction') == 0)).count()
TP = temp.filter((F.col('customPrediction') == 1) & (F.col('label') == 1)).count()
FP = temp.filter((F.col('customPrediction') == 1) & (F.col('label') == 0)).count()
FN = temp.filter((F.col('customPrediction') == 0) & (F.col('label') == 1)).count()
TN = temp.filter((F.col('customPrediction') == 0) & (F.col('label') == 0)).count()

print('With threshold =  {}'.format(threshold))
print('num positive: {}'.format(nP))
print('num negative: {}'.format(nN))
print('precision: {}'.format(TP / (TP + FP)))
print('recall: {}'.format(TP / (TP + FN)))
print('accuracy: {}'.format((TP + TN) / total))
print('f1 : {}'. format(2/(  1/(TP / (TP + FN))  +  1/ (TP / (TP + FP))    )))
binary_evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction", labelCol="label", metricName="areaUnderROC")
auroc = binary_evaluator.evaluate(predictions)
print('auroc: {}'.format(auroc))


# Test Error = 0.213093
# With threshold =  0.5
# num positive: 29487
# num negative: 94576
# precision: 0.2554006850476481
# recall: 0.626956376956377
# accuracy: 0.7869066522653813
# f1 : 0.3629485047832478
# auroc: 0.7989688909080508




# ---------------Basic Models End ---------------------------------------------------------------

# https://spark.apache.org/docs/2.3.1/api/python/pyspark.ml.html#module-pyspark.ml.classification

# https://spark.apache.org/docs/2.3.1/api/python/pyspark.ml.html#module-pyspark.ml.classification
