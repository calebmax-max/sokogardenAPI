# Import flask and its components
from flask import *
import os

# import the pymysql module - It helps us to create a connection between python flask and mysql database
import pymysql

# Create a flask application and give it a name
app = Flask(__name__)

# configure the location where your product images will be savedon your application
app.config["UPLOAD_FOLDER"] = "static/images"


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
       


       # below is the route for adding products
@app.route("/api/add_product", methods = ["POST"])
def Addproducts():
    if request.method == "POST":
        # extract the data entered on the form
        product_name = request.form["product_name"]
        product_description = request.form["product_description"]
        product_cost = request.form["product_cost"]
        # for the product photo we shall fetch it from the files as shown below
        product_photo = request.files["product_photo"]

        # extract the file name of the product photo
        filename = product_photo.filename

        # by use of the os module (operating system) we can extract the file path where the email is currently saved

        photo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # save the product photo image into the new location
        product_photo.save(photo_path)



        #print them out to test whether you are receiving the details sent with the request
        #print(product_name, product_description,product_cost,product_photo)

        # establish a connection to the db 
        connection = pymysql.connect(host="localhost", user="root", password="",database="sokogardenonline")
        # create a cursor
        cursor = connection.cursor()


        #structure the sql query to insert the products details to the details 
        sql = "INSERT INTO product_details(product_name, product_description, product_cost, product_photo) VALUES (%s, %s, %s, %s)"

        # create a tuple that will hold the data from the form which are currently held from the different ariables declared.
        data = (product_name, product_description, product_cost,filename)

        # use the cursor to execute the sql as you replace the placeholders with the actual data 
        cursor.execute(sql, data)

        # commit hte changes to the databases
        connection.commit()
             
        return jsonify({"message": "Product added successfully"}) 
     
        


# Run the application  
app.run(debug=True)