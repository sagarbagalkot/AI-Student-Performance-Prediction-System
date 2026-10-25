import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

import joblib

data_path = "dataset/student_data.csv"

df = pd.read_csv(data_path)



print("Dataset Loaded Successfully")
print(df.head())

df["Result"] = df["Result"].map({
    "Pass": 1,
    "Fail": 0
})

X = df[
[
    "Attendance",
    "Study_Hours",
    "Assignment_Marks",
    "Internal_Marks",
    "Practical_Marks",
    "Previous_Semester_Marks"
]
]

y = df["Result"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


model.fit(
    X_train,
    y_train
)

prediction = model.predict(X_test)


accuracy = accuracy_score(
    y_test,
    prediction
)


print("-----------------------------")
print("Model Accuracy:", accuracy)
print("-----------------------------")


print(
    classification_report(
        y_test,
        prediction
    )
)

model_folder = "model"


if not os.path.exists(model_folder):
    os.makedirs(model_folder)

joblib.dump(
    model,
    "model/student_model.pkl"
)

print("Model Saved Successfully!")