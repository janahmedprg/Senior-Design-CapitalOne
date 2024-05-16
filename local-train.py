import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import sklearn
import numpy as np


df_train = pd.read_csv("traindata.csv")
df_test = pd.read_csv("testdata.csv")

df_train.drop(df_train.columns[0],axis=1, inplace=True)
df_test.drop(df_test.columns[0],axis=1,inplace=True)

df_train.drop(columns=["trans_date_trans_time", "cc_num", "merchant", "category", "first", "last", "gender", "street", "city", "state", "zip", "job", "dob", "trans_num"], inplace=True)
df_test.drop(columns=["trans_date_trans_time", "cc_num", "merchant", "category", "first", "last", "gender", "street", "city", "state", "zip", "job", "dob", "trans_num"], inplace=True)


x_train=df_train.drop("is_fraud",axis=1)
y_train=df_train["is_fraud"]
x_test=df_test.drop("is_fraud",axis=1)
y_test=df_test["is_fraud"]

print(x_train)
print(x_test)


print("Building training and testing datasets")
print() 


# print("train data shape",x_train.shape)
# print("test data shape",x_test.shape)
# print("y train shape", y_train.shape)
# print("y test shape", y_test.shape)

print("Training RandomForest Model....")
print()
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train.values,y_train.values)
print()

print()
y_pred_test = model.predict(x_test.values)
print(x_test.head(1))
print(y_test.head(1))
test_acc = accuracy_score(y_test, y_pred_test)
test_rep = classification_report(y_test, y_pred_test)

print()
print("---- METRICS RESULTS FOR TESTING DATA ----")
print()
print("Total Rows are:", x_test.shape[0])
print("[TESTING] Model Accuracy is:", test_acc)
print("[TESTING] Testing Report:")
print(test_rep)
dat = np.array([[996.31,42.5200,-78.6847,7728,1372113010,43.110777,-78.685005]])
print(dat)
print(model.predict(dat))
