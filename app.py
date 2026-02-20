# Import flask and its components
from flask import *

# import the pymysql module - It helps us to create a connection between python flask and mysql database
import pymysql

# Create a flask application and give it a name
app = Flask(__name__)


# Below is the sign up route
@app.route("/api/signup", methods = ["POST"])
def signup():
    if request.method == "POST":
        # Extract the different details entered on the form
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]

        # by use of the print function leyts print all those details send with the upcoming request.
        # print(username, email, password, phone)

        # establish a connection between flask/python and mysql
        connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

        # create a cursor to execute the sql queries
        cursor = connection.cursor()

        # structure an sql to insert the details received from the form
        # %s is a place holder -> A placeholder stands in places of actual i.e we shall replace later
        sql = "INSERT INTO users(username,email,phone,password) VALUES(%s, %s, %s, %s)"

        # create a tuple that will hold all the data gottten from the form.
        data = (username, email, phone, password)

        #by use of the cursor execute the sql as you replace the placeholders with the actual values
        cursor.execute(sql, data)

        # commit the changes to the database
        connection.commit()



        return jsonify({"message" : "User registered successfully"})
    


# below is the login/sign in route
@app.route("/api/signin", methods = ["POST"])
def signin():
     if request.method =="POST":
       #extract data from the form
       email = request.form["email"]
       password = request.form["password"]

       print(email,password)
    #    return jsonify({"message" : "Signin route accessed"})
       connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")
        # create a cursor to execute the sql queries
       cursor = connection.cursor(pymysql.cursors.DictCursor)
       sql ="SELECT * FROM users WHERE email = %s AND password = %s"
        # create a tuple that will hold all the data gottten from the form.
       data = (email, password)
       #by use of the cursor execute the sql as you replace the placeholders with the actual values
       cursor.execute(sql, data)
       # check whether there are rows returned and store the same on a variable
       count = cursor.rowcount
        # if there are records it means the email and the password are coreect otherwise it means they are wrong

       if count == 0:
           return jsonify({"message" : "Login failed"})
       else:
        # There must be a user so we create a variable that will hold the details of the user fetched from the database
           user = cursor.fetchone()
        #return the deatils to the front-end as welll as a message
           return jsonify({"message" : "User signed up successfully","user":user})


# Run the application  
app.run(debug=True)