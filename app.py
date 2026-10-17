# import the library
from flask import Flask, request, jsonify
from backend.prediction import get_prediction
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


# create the prediction route
@app.route("/prediction", methods=['POST'])
def prediction():
    try:
        data = request.get_json()
        text_report = data.get("text")
        if not text_report:
            return jsonify({"Error" : "Missing input feature data"}), 400

        prediction_result = get_prediction(text_report)
        return jsonify({
            "status" : "success",
            "prediction" : prediction_result
        }), 200
    except Exception as e:
        return jsonify({
            "status" : "error",
            "message" : str(e)
        }), 500

# run the app
if __name__ == '__main__':
    app.run(debug=True, port=5500)