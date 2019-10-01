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
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.classification import LogisticRegression, GBTClassifier, RandomForestClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer, IndexToString, VectorAssembler
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from pyspark.ml.classification import OneVsRest
from pyspark.ml import Pipeline

# genre_ml_final.groupby("genre").agg({"genre":"count"}).show()

audio_dataset_new_multiclass = genre_with_methods_of_moments.filter(col("genre").isNotNull())

multiclass_dataset = audio_dataset_new_multiclass
indexer = StringIndexer(inputCol="genre", outputCol="genre_id")
multiclass_dataset = indexer.fit(multiclass_dataset).transform(multiclass_dataset)

multiclass_dataset = multiclass_dataset.drop("track_id",'genre')

var = multiclass_dataset.schema.names[0:-1]

def to_int(x):
    return int(x)

udf_to_int = udf(to_int, IntegerType())
multiclass_dataset = multiclass_dataset.withColumn("int_genre_id", udf_to_int("genre_id"))


multiclass_dataset = multiclass_dataset.drop("genre_id")


df = multiclass_dataset
cols = df.columns

stages = []
label_stringIdx = StringIndexer(inputCol = 'int_genre_id', outputCol = 'label')
stages += [label_stringIdx]
numericCols = multiclass_dataset.schema.names[0:-1]

assembler = VectorAssembler(inputCols=numericCols, outputCol="features")
stages += [assembler]


from pyspark.ml import Pipeline
pipeline = Pipeline(stages = stages)
pipelineModel = pipeline.fit(df)
df = pipelineModel.transform(df)
selectedCols = ['label', 'features'] + cols


# Split the data into training and test sets (30% held out for testing)
(trainingData, testData) = df.randomSplit([0.7, 0.3])

# Train a Random Forest model.
rf = RandomForestClassifier(labelCol="categoryIndex", featuresCol="features", numTrees=100,  maxDepth=10, impurity="entropy")
rf = OneVsRest(classifier=rf)

# Chain RF in a Pipeline
pipeline = Pipeline(stages=[rf])

# Train model.
model = pipeline.fit(trainingData)

# Make predictions.
predictions = model.transform(testData)



#predictions.groupby("int_genre_id").agg({"int_genre_id" : "count"}).show()
# +------------+-------------------+
# |int_genre_id|count(int_genre_id)|
# +------------+-------------------+
# |          12|               1744|
# |          13|               1213|
# |          14|                597|
# |          18|                159|
# |           6|               4149|
# |           9|               2089|
# |          16|                473|
# |          17|                321|
# |           5|               4135|
# |          10|               1967|
# |           1|              12025|
# |           3|               5308|
# |           7|               3468|
# |          11|               1867|
# |          15|                507|
# |          19|                136|
# |          20|                 61|
# |           2|               6154|
# |           4|               5175|
# |           0|              69832|
# +------------+-------------------+
# only showing top 20 rows



predictions.select("categoryIndex", "int_genre_id", "features", "rawPrediction", "prediction", "probability").show(5)

# +-------------+------------+----------+--------------------+----------+--------------------+
# |categoryIndex|int_genre_id|  features|       rawPrediction|prediction|         probability|
# +-------------+------------+----------+--------------------+----------+--------------------+
# |          0.0|           0|(10,[],[])|[53.1568774797907...|       0.0|[0.53156877479790...|
# |          0.0|           0|(10,[],[])|[53.1568774797907...|       0.0|[0.53156877479790...|
# |          0.0|           0|(10,[],[])|[53.1568774797907...|       0.0|[0.53156877479790...|
# |          0.0|           0|(10,[],[])|[53.1568774797907...|       0.0|[0.53156877479790...|
# |          0.0|           0|(10,[],[])|[53.1568774797907...|       0.0|[0.53156877479790...|
# +-------------+------------+----------+--------------------+----------+--------------------+
# only showing top 5 rows


# Evaluations 
predictions = predictions.withColumnRenamed("int_genre_id", "label")

def multiclass_evaluator(df):
    evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
    metrics = {
    'precision':evaluator.evaluate(df, {evaluator.metricName: "weightedPrecision"}),
    'recall':evaluator.evaluate(df, {evaluator.metricName: "weightedRecall"}),
    'accuracy':evaluator.evaluate(df, {evaluator.metricName: "accuracy"}),
    'f1':evaluator.evaluate(df, {evaluator.metricName: "f1"})
    }
    return metrics

multiclass_evaluator(predictions)


# {'precision': 0.4459828758562083,
#  'recall': 0.583062864727926,
#  'accuracy': 0.5830628647279261,
#  'f1': 0.4633229632165778}


#Test Error = 0.418824

