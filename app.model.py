from flask import Flask, jsonify, request
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Lasso
import pickle
import os
import sqlite3

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True


app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello Pablo!'

@app.route('/predict', methods=['GET'])
def predict():
    model = pickle.load(open('data/advertising_model','rb'))

    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)

    if tv is None or radio is None or newspaper is None:
        return "Missing args, the input values are needed to predict"
    else:
        prediction = model.predict([[tv,radio,newspaper]])
        return "The prediction of sales investing that amount of money in TV, radio and newspaper is: " + str(round(prediction[0],2)) + 'k €'

#http://127.0.0.1:5000/predict?tv=10&radio=23&newspaper=3

# 2. Crea un endpoint que reentrene de nuevo el modelo con los datos disponibles en la carpeta data, que guarde ese modelo reentrenado, devolviendo en la respuesta la media del MAE de un cross validation con el nuevo modelo
@app.route('/retrain', methods=['PUT'])
def retrain():
    df = pd.read_csv('data/Advertising.csv', index_col=0)
    X = df.drop(columns=['sales'])
    y = df['sales']

    model = pickle.load(open('data/advertising_model','rb'))
    model.fit(X,y)
    pickle.dump(model, open('data/advertising_model_v1','wb'))

    scores = cross_val_score(model, X, y, cv=10, scoring='neg_mean_absolute_error')

    return "New model retrained and saved as advertising_model_v1. The results of MAE with cross validation of 10 folds is: " + str(abs(round(scores.mean(),2)))

@app.route('/insert_data', methods=['POST']) #En PythonAniwhere deberá ser un GET
def reward():

    connection = sqlite3.connect('advertising_sales2.db')
    cursor = connection.cursor()

    TV = request.args['TV']
    radio = request.args['radio']
    newspaper = request.args['newspaper']

    query = "INSERT INTO s (TV, radio, newspaper) VALUES (?, ?, ?)"

    result = cursor.execute(query, (TV, radio, newspaper)).fetchall()

    
    connection.commit()
    connection.close()
    return 'Datos añadidos' 

@app.route('/view_data', methods=['GET'])
def reward3():

    connection = sqlite3.connect('advertising_sales2.db')
    cursor = connection.cursor()

    query = "SELECT * FROM s"
    result = cursor.execute(query).fetchall()

    connection.close()
    
    return result


@app.route('/insert_data+prediction', methods=['POST']) #Aqui añadimos los datos igual que antes pero las sales seran con una predicción
def rewarding():

    model = pickle.load(open('data/advertising_model','rb'))

    TV = request.args['TV']
    radio = request.args['radio']
    newspaper = request.args['newspaper']

    prediction = model.predict([[TV,radio,newspaper]])  #Hacemos una predicción con los argumentos y la añadimos a la columna de sales
    prediction = str(prediction)
    connection = sqlite3.connect('advertising_sales2.db')
    cursor = connection.cursor()

    query = "INSERT INTO s (TV, radio, newspaper,sales) VALUES (?, ?, ?, ?)"

    result = cursor.execute(query, (TV, radio, newspaper, prediction)).fetchall()

    
    connection.commit()
    connection.close()
    return 'Datos añadidos' #+ "The prediction is: " + str(round(prediction[0],2)) + 'k €'
app.run()