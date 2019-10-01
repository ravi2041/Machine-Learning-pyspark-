"""
1. LR, RF and GBT with CV

2. All run on the 'train_initial' training dataset (original unbalanced)

"""

from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

# 1. LR with CV ----------------------------------------------

# (train_initial, test) = df.randomSplit([0.7, 0.3])  # IF REQUIRED - else, already done earlier.

lr = LogisticRegression(featuresCol = 'features', labelCol = 'label')

paramGrid = ParamGridBuilder() \
    .addGrid(lr.elasticNetParam, [0.1, 0.5, 0.9]) \
    .addGrid(lr.regParam, [0.1, 0.3, 0.6]) \
    .addGrid(lr.maxIter, [10, 20, 50]) \
    .build()

crossval = CrossValidator(estimator=lr,
                          estimatorParamMaps=paramGrid,
                          evaluator=BinaryClassificationEvaluator(),
                          numFolds=5)

cvModel = crossval.fit(train_down)
predictions = cvModel.transform(test)
total = predictions.count()

threshold = 0.5   # Results with threshold = 0.1, 0.2  and 0.5 given below

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

# Original training data : train_initial
# With threshold =  0.5
# num positive: 42
# num negative: 124027
# precision: 0.047619047619047616
# recall: 0.00016645859342488556
# accuracy: 0.9028524450104377
# f1 : 0.0003317574852782616
# auroc: 0.6860595236018103



# ---------------------------- LR with CV ends----------------------------------------

# 2. RF with CV ----------------------------------------------------------------------

labelIndexer = StringIndexer(inputCol="label", outputCol="indexedLabel").fit(df)

featureIndexer =\
    VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4).fit(df)

rf = RandomForestClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures")

# Convert indexed labels back to original labels.
labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel",
                               labels=labelIndexer.labels)

# Chain indexers and forest in a Pipeline
pipeline = Pipeline(stages=[labelIndexer, featureIndexer, rf, labelConverter])

  #gini  # .addGrid(rf.maxDepth , [4]) \

paramGrid = ParamGridBuilder() \
    .addGrid(rf.numTrees, [ 200, 400,600]) \
    .addGrid(rf.impurity,['entropy','gini']) \
    .addGrid(rf.maxDepth,[2,3,4]) \
    .build()

crossval = CrossValidator(estimator=pipeline,
                          estimatorParamMaps=paramGrid,
                          evaluator=BinaryClassificationEvaluator(),
                          numFolds=5)

cvModel = crossval.fit(train_down)

predictions = cvModel.transform(test)
total = predictions.count()

threshold = 0.5   # Results with threshold = 0.1, 0.2  and 0.5 given below

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

#-------------------------------

# With threshold =  0.5
# num positive: 28205
# num negative: 95858
# precision: 0.23545470661230278
# recall: 0.5528638028638029
# accuracy: 0.7828925626496216
# f1 : 0.3302583484596066
# auroc: 0.7664886035717177




# ---------------------------- RF with CV ends----------------------------------------

# 3. Gradient BOOST Classifier  with CV ------------------------------------------------

# Train a GBT model.

gbt = GBTClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", maxIter=10)

# Chain indexers and GBT in a Pipeline
pipeline = Pipeline(stages=[labelIndexer, featureIndexer, gbt])

from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

paramGrid = ParamGridBuilder() \
    .addGrid(gbt.maxIter, [100,150,200]) \
    .addGrid(gbt.lossType, ['logistic']) \
    .addGrid(gbt.maxDepth,[3,4,5]) \
    .build()

crossval = CrossValidator(estimator=pipeline,
                          estimatorParamMaps=paramGrid,
                          evaluator=BinaryClassificationEvaluator(),
                          numFolds=5)

cvModel = crossval.fit(train_down)

predictions = cvModel.transform(test)
# selected = prediction.select("label","rawPrediction", "probability", "prediction")
# for row in int(range(len(selected.collect())))<10:
#     print(row)

total = predictions.count()


threshold = 0.5    # Results with threshold = 0.1, 0.2  and 0.5 given below

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
# num positive: 26787
# num negative: 97016
# precision: 0.29051405532534436
# recall: 0.6502339572192514
# accuracy: 0.8126782065054966


# ---------- GBT with CV ends ----------------------------------------------------  
