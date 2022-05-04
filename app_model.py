from flask import Flask, jsonify, request
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Lasso
import pickle
import os

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

model = pickle.load(open('ad_model.pkl','rb'))

@app.route('/api/v1/predict', methods=['GET'])
def predict():
    
    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)

    if tv is None or radio is None or newspaper is None:
        return "Args empty, the data are not enough to predict"
    else:
        prediction = model.predict([[tv,radio,newspaper]])
    
    return jsonify({'predictions': prediction[0]})

#http://127.0.0.1:5000/api/v1/predict?tv=10&radio=25&newspaper=50

@app.route('/api/v1/retrain', methods=['GET'])
def retrain():
    
    data = pd.read_csv('data/Advertising.csv', index_col=0)
    
    X = data.drop(columns=['sales'])
    y = data['sales']

    model = Lasso(alpha=6000)
    model.fit(X, y)

    pickle.dump(model, open('ad_model.pkl', 'wb'))

    return 'well done'

app.run()