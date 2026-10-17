# import the libraries
from pathlib import Path
import joblib 
import spacy 

# define the spacy variable
nlp = spacy.load('en_core_web_sm')
BASE_PATH = Path(__file__).resolve().parent

model = joblib.load(BASE_PATH / "../notebooks/logistic_model.pkl")
vectoriser = joblib.load(BASE_PATH / "../notebooks/vectoriser.pkl")

def get_prediction(text: str):
    # create a try catch statement to get the data and perform the prediction
    try:
        processed_text = text.replace("°C", "celcius").replace("° C", "celcius")
        sentence = nlp(processed_text)

        cleaned_sentence = []
        for token in sentence:
            # remove all spaces and stop words
            if token.is_stop or token.is_space or token.is_punct:
                continue

            token = token.lemma_.lower()
            if token == "datum":
                token = "data"
            
            # append the token to the sentence
            cleaned_sentence.append(token)

            # join the cleaned_sentence now 
        cleaned_text = " ".join(cleaned_sentence)

        #vectorise the text
        vectorise_data = vectoriser.transform([cleaned_text])
        predicted_category = model.predict(vectorise_data)[0]
        prediction_probability = model.predict_proba(vectorise_data)[0].max()
        round_probability = prediction_probability * 100

        return{
            "status" : "success",
            "predicted_incident" : predicted_category,
            "confidence_score" : round(round_probability, 2),
            "model_version" : "Logistic Regression",
            "report" : text
        }
    
    except Exception as e:
        return{
            "message" : f"Error Predicting the Incident type : {e}"
        }

