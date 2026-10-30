from flask import Flask, render_template, request, redirect, session

from predict import predict_student_performance

from database_render import(
    save_prediction,
    get_dashboard_data,
    get_all_predictions,
    delete_prediction,
    register_user,
    login_user
)

app = Flask(__name__)

app.secret_key = "student_ai_secret_key"

@app.route("/")
def home():

    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        register_user(name, email, password)

        return redirect("/login")


    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]


        user = login_user(
            email,
            password
        )


        if user:

            session["user_id"] = user[0]

            session["username"] = user[1]


            return redirect("/prediction")


        else:

            return "Invalid Email or Password"



    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")



@app.route("/prediction")
def prediction():

    if "user_id" not in session:

        return redirect("/login")


    return render_template("prediction.html")


@app.route("/predict", methods=["POST"])
def predict():


    if "user_id" not in session:

        return redirect("/login")


    try:


        student_name = request.form["student_name"]


        attendance = float(request.form["attendance"])

        study_hours = float(request.form["study_hours"])

        assignment_marks = float(request.form["assignment_marks"])

        internal_marks = float(request.form["internal_marks"])

        practical_marks = float(request.form["practical_marks"])

        previous_marks = float(request.form["previous_marks"])


        result, confidence = predict_student_performance(

            attendance,

            study_hours,

            assignment_marks,

            internal_marks,

            practical_marks,

            previous_marks

        )


        save_prediction(

            session["user_id"],

            student_name,

            attendance,

            study_hours,

            assignment_marks,

            internal_marks,

            practical_marks,

            previous_marks,

            result,

            confidence

        )

        return render_template(

            "result.html",

            student_name=student_name,

            result=result,

            confidence=confidence

        )

    except Exception as e:

        return f"Prediction Error : {e}"


@app.route("/dashboard")
def dashboard():


    data = get_dashboard_data()


    students = get_all_predictions()



    return render_template(

        "dashboard.html",

        total_students=data[0],

        average_attendance=data[1],

        pass_percentage=data[2],

        fail_percentage=data[3],

        average_marks=data[4],

        students=students

    )


@app.route("/analysis")
def analysis():

    return render_template("analysis.html")

@app.route("/about")
def about():

    return render_template("about.html")

@app.route("/delete/<int:id>")
def delete(id):


    delete_prediction(id)


    return redirect("/dashboard")

if __name__ == "__main__":

    app.run(debug=True)