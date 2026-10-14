# import the library
from flask import Flask
from config import Config
from models import db

# create the flask app
app = Flask(__name__)
app.config.from_object(Config)

# initiate the database connection
db.init_app(app)

# create the databass table 
with app.app_context():
    db.create_all()
    print("Database tables created successfully")


# create a simple home page
@app.route("/")
def get_home():
    return {
        "status" : "success",
        "message" : "Chemical Safety Analyser App"
    }

# run the app
if __name__ == '__main__':
    app.run(debug=True, port=5500)