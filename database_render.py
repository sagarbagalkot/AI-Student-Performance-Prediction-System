users = []
predictions = []


def register_user(name,email,password):

    users.append({
        "id":len(users)+1,
        "name":name,
        "email":email,
        "password":password
    })


def login_user(email,password):

    for user in users:
        if user["email"] == email and user["password"] == password:
            return (
                user["id"],
                user["name"]
            )

    return None


def save_prediction(
        user_id,
        student_name,
        attendance,
        study_hours,
        assignment_marks,
        internal_marks,
        practical_marks,
        previous_marks,
        result,
        confidence):

    predictions.append(
        (
        len(predictions)+1,
        student_name,
        attendance,
        study_hours,
        assignment_marks,
        internal_marks,
        practical_marks,
        previous_marks,
        result
        )
    )


def get_dashboard_data():

    total=len(predictions)

    if total==0:
        return (0,0,0,0,0)

    avg_att=sum(
        x[2] for x in predictions
    )/total

    pass_count=len(
        [x for x in predictions if x[8]=="Pass"]
    )

    pass_percentage=(pass_count/total)*100

    fail_percentage=100-pass_percentage


    avg_marks=sum(
        x[7] for x in predictions
    )/total


    return (
        total,
        round(avg_att,2),
        round(pass_percentage,2),
        round(fail_percentage,2),
        round(avg_marks,2)
    )


def get_all_predictions():

    return predictions


def delete_prediction(id):
    pass