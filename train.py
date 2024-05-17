from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import sklearn
import joblib
import argparse
import joblib
import os
import pandas as pd

def model_fn(model_dir):
    clf = joblib.load(os.path.join(model_dir, "model.joblib"))
    return clf

if __name__ =='__main__':
    print("[INFO] Extracting arguments")
    parser = argparse.ArgumentParser()

    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--random_state", type=int, default=0)

    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR"))
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN"))
    parser.add_argument("--test", type=str, default=os.environ.get("SM_CHANNEL_TEST"))
    parser.add_argument("--train-file", type=str, default="fraudTrain.csv")
    parser.add_argument("--test-file", type=str, default="fraudTest.csv")

    args, _ = parser.parse_known_args()

    print("SKLearn Version:", sklearn.__version__)
    print("Joblib Version:", joblib.__version__)

    print("[INFO] Reading data")
    print()

    df_train = pd.read_csv(os.path.join(args.train, args.train_file))
    df_test = pd.read_csv(os.path.join(args.test, args.test_file))

    df_train.drop(df_train.columns[0],axis=1, inplace=True)
    df_test.drop(df_test.columns[0],axis=1,inplace=True)

    df_train = df_train[['cc_num','amt','lat','long','merch_lat','merch_long','is_fraud']]
    df_test = df_test[['cc_num','amt','lat','long','merch_lat','merch_long','is_fraud']]

    df_train = df_train.sort_values(by=['is_fraud'], ascending=False).head(100000)
    
    x_train=df_train.drop("is_fraud",axis=1)
    y_train=df_train["is_fraud"]
    x_test=df_test.drop("is_fraud",axis=1)
    y_test=df_test["is_fraud"]

    
    print("Building training and testing datasets")
    print() 


    print("train data shape",x_train.shape)
    print("test data shape",x_test.shape)
    print("y train shape", y_train.shape)
    print("y test shape", y_test.shape)

    print("Training RandomForest Model....")
    print()
    model = RandomForestClassifier(n_estimators=args.n_estimators, random_state=args.random_state, class_weight='balanced')
    model.fit(x_train.values,y_train.values)
    print()
    
    model_path = os.path.join(args.model_dir, "model.joblib")
    joblib.dump(model, model_path)
    print("Model persisted at", model_path)
    print()
    y_pred_test = model.predict(x_test.values)
    test_acc = accuracy_score(y_test.values, y_pred_test)
    test_rep = classification_report(y_test.values, y_pred_test)
    conf_mat = confusion_matrix(y_test.values, y_pred_test)

    print()
    print("---- METRICS RESULTS FOR TESTING DATA ----")
    print()
    print("Total Rows are:", x_test.shape[0])
    print("[TESTING] Model Accuracy is:", test_acc)
    print("[TESTING] Confusion Matrix:")
    print(conf_mat)
    print("[TESTING] Testing Report:")
    print(test_rep)