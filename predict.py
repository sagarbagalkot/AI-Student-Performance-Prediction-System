import joblib
import numpy as np

# Load trained model
model = joblib.load("model/student_model.pkl")


def predict_student_performance(
    attendance,
    study_hours,
    assignment_marks,
    internal_marks,
    practical_marks,
    previous_marks
):

    # Input data for prediction
    data = np.array([[
        attendance,
        study_hours,
        assignment_marks,
        internal_marks,
        practical_marks,
        previous_marks
    ]])

    # Predict result
    prediction = model.predict(data)

    # Check if model supports probability
    if hasattr(model, "predict_proba"):

        probability = model.predict_proba(data)

        if prediction[0] == 1:
            result = "Pass"
            confidence = round(probability[0][1] * 100, 2)
        else:
            result = "Fail"
            confidence = round(probability[0][0] * 100, 2)

    else:
        result = "Pass" if prediction[0] == 1 else "Fail"
        confidence = 0.00

    return result, confidence