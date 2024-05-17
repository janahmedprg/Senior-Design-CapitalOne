# Securing Machine Learning Model Deployment with AWS

## Introduction
Our senior design project goal was to deploy a machine learning model and ensure its security
against potential attack vectors. With the increasing adoption of machine learning, it is
crucial to be able to understand how to secure ML models.
This documentation provides a solution with all the steps to securing the endpoint of our deployed model.

## Goal
- Deploy a machine learning model on a cloud platform.
- Implement robust security measures to protect the model's endpoint.

## Background

### ML Model
We decided to choose the
[Credit Card Transactions Fraud Detection Dataset](https://www.kaggle.com/datasets/kartik2112/fraud-detection)
from Kaggle in order to train our model. The relevant columns for our
model are
- `'cc_num'`: Credit card number used for the transaction.
- `'amt'`: Amount of the transaction.
- `'lat'`: Latitude of the transaction location.
- `'long'`: Longitude of the transaction location.
- `'merch_lat'`: Latitude of the merchant location.
- `'merch_long'`: Longitude of the merchant location.
- `'is_fraud'`: Binary indicator (0 or 1) representing whether the transaction is fraudulent (0 is not fraud, 1 is fraud).

We decided to use a Random Forrest Classifier for our ML model
since it is the most appropriate for this scenario. Each decision tree
of the random forest is trained on some randomly selected sample. Once
all the trees are created, the model predicts the class label of
the input features by majority voting of all the decision trees.
We varied the values of some parameters of the `sklearn.RandomForestClassifier`and found that to get the best model for our
dataset we needed to increase the number of decision trees, introduce
randomness when sampling from the dataset, and have the weights of both
classes (0 and 1) to be balanced. We then varied the number of data
the model trained on to get the most optimal model. In Figure 1 we can
see the heat maps of the normalized confusion matrix and accuracy
of each model when trained on different sizes of data. From here
we can see that the most optimal model is when we train
on 100000 rows.

![Figure 1](img/hmap_col.jpg)
*Figure 1: Heat map of normalized confusion matrices.*

### Deployment
We decided to utilize AWS services since we collaborated with
Capital One, and
they mostly use AWS for their applications.
We chose Amazon SageMaker for a few reasons such as
- It is fully managed meaning the
user doesn't have to worry about the operational aspects of
running a machine learning platform.
- It can be easily
integrated with other AWS services.
- It is highly scalable.

To find the training script and deployment notebook of the model
refer [train.py](train.py) and [model-deploy.ipynb](model-deploy.ipynb). The following contains the details about the deployed model
```
---- METRICS RESULTS FOR TESTING DATA ----
Total Rows are: 555719
[TESTING] Model Accuracy is: 0.9897520149571996
[TESTING] Confusion Matrix:
[[548852   4722]
 [   973   1172]]
[TESTING] Normalized Confusion Matrix:
[[0.99146998 0.00853002]
 [0.45361305 0.54638695]]
[TESTING] Testing Report:
              precision    recall  f1-score   support

           0       1.00      0.99      0.99    553574
           1       0.20      0.55      0.29      2145

    accuracy                           0.99    555719
   macro avg       0.60      0.77      0.64    555719
weighted avg       1.00      0.99      0.99    555719
```
Once we deploy our model, then on the **Amazon SageMaker**&#8594;**Training**&#8594;**Training jobs** dashboard
we can see our completed training job as in Figure 2. 
![Figure2](img/trainJob.png)
*Figure 2: Amazon SageMaker Training jobs dashboard.*

We can also see our deployed model on the **Amazon SageMaker**&#8594;**Inference**&#8594;**Endpoints** dashboard as in Figure 3.
![Figure 3](img/enpoint.png)
*Figure 3: Amazon SageMaker Endpoint dashboard.*

## Securing the Endpoint
### Endpoint Architecture
To secure our ML endpoint we decided to follow the best practices
mentioned in the
[Security in Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/security.html)
developer guide. We built the architecture shown
in Figure 4 focusing on the security features of AWS Shield.
![Figure 4](img/architecture.png)
*Figure 4: Endpoint Architecture.*

### Creating a Lambda Function

