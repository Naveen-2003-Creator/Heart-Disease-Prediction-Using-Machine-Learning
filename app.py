import numpy as np
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# Load the trained model
model = pickle.load(open('model/heartmodel.pkl', 'rb'))
print("Loaded model type:", type(model))

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/heart', methods=['GET', 'POST'])
def heart():
    return render_template('heart.html', message='')

@app.route('/predict', methods=['POST'])
def predictpage():
    try:
        print(request.form)
        feature_order = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                         'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

        # Check for empty fields
        if any(request.form.get(f, '') == '' for f in feature_order):r
            return render_template("heart.html", message="Please fill all fields!")

        # Convert to float and predict
        to_predict_list = [float(request.form.get(f)) for f in feature_order]
        values = np.array(to_predict_list).reshape(1, -1)
        pred = model.predict(values)[0]

        result = ("⚠️ The model predicts a high chance of Heart Disease 😟."
                  if pred == 1 else
                  "✅ The model predicts a low chance of Heart Disease 🤗.")

        return render_template('predict.html', prediction=result)

    except ValueError:
        return render_template("heart.html", message="Please enter valid numeric data.")

if __name__ == '__main__':
    app.run(debug=True)
