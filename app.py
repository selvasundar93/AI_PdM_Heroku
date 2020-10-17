import pickle
import numpy as np
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import tensorflow as tf 
import joblib

app = Flask(__name__)
api = Api(app)

# Load pre-trained Models
global model_DL
model_DL = tf.keras.models.load_model('LSTM_Autoencoder.h5')
model_rms = pickle.load(open('lof_rms_trained_model.pkl', 'rb'))
model_mean = pickle.load(open('lof_mean_trained_model.pkl', 'rb'))
model_dt = pickle.load(open('DT_Classifier.pkl', 'rb'))

def Anomaly_output(x):
    if x==1:
        return "Normal"
    elif x==-1:
        return "Anomaly"
    else:
        return "No Proper Input"

def class_ff(x):
    switch={
        1:'0-20%',
        2:'20-40%',
        3:'40-60%',
        4:'60-80%',
        5:'80-100%'}
    return switch.get(x)

def class_rul(x):
    switch={
        1:'80%',
        2:'60%',
        3:'40%',
        4:'20%',
        5:'<20%'}
    return switch.get(x)

@app.route('/')
def home_endpoint():
    return 'Anomaly Detection & RUL Estimation'

# Univariate Anomaly Detection - RMS or Mean
class MakePrediction(Resource):
    def post(self):
        posted_data = request.get_json()
        rms = posted_data["rms"]
        mean = posted_data["mean"]
        if ((rms==0.0) & (mean==0.0)):
            op = 0
        else:
            if rms==0.0:
                op = model_mean.predict(np.array(mean).reshape(-1,1))
            else:
                op = model_rms.predict(np.array(rms).reshape(-1,1))
        Aop = Anomaly_output(op)
        return jsonify({"Output": Aop})

# Multivariate Anomaly Detection - Mean Value
class MakePrediction1(Resource):
    def post(self):
        posted_data1 = request.get_json()
        b1 = posted_data1["Bearing1"]
        b2 = posted_data1["Bearing2"]
        b3 = posted_data1["Bearing3"]
        b4 = posted_data1["Bearing4"]
        b_comb = np.array([b1,b2,b3,b4]).reshape(1,4)
        if ((b1==0.0) & (b2==0.0) & (b3==0.0) & (b4==0.0)):
            op = 0
        else:
            scaler = joblib.load("scaler_file")
            b_comb = scaler.transform(b_comb)
            dl_pred = model_DL.predict(b_comb.reshape(b_comb.shape[0], 1, b_comb.shape[1]))
            dl_pred = dl_pred.reshape(dl_pred.shape[0], dl_pred.shape[2])
            score = np.mean(np.abs(dl_pred-b_comb), axis = 1)
            threshold = 0.29
            if score < threshold:
                op = 1
            else:
                op = -1
        Aop1 = Anomaly_output(op)
        return jsonify({"Output": Aop1})
# RUL Prediction
class RULPrediction(Resource):
    def post(self):
        posted_data2 = request.get_json()
        b_r = posted_data2["Bearing1_RMS"]
        b_k = posted_data2["Bearing1_Kurt"]
        b_r_p = posted_data2["Bearing1_RMS_Prev"]
        b_k_p = posted_data2["Bearing1_Kurt_Prev"]
        if ((b_r==0.0) & (b_k==0.0) & (b_r_p==0.0) & (b_k_p==0.0)):
            return jsonify({"RUL_Class": "No Proper Input",
                        "Fraction Failing": "No Proper Input",
                        "RUL": "No Proper Input"})
        else:
        	b_comb1 = np.array([b_r,b_k,b_r_p,b_k_p]).reshape(1,4)
        	rul_pred = model_dt.predict(b_comb1)
        	ff = class_ff(int(rul_pred))
        	rul_val = class_rul(int(rul_pred))
        	return jsonify({"RUL_Class": int(rul_pred),
                        "Fraction Failing": ff,
                        "RUL":rul_val})
           
api.add_resource(MakePrediction, '/Ano_Det_Uni')    
api.add_resource(MakePrediction1, '/Ano_Det_Multi')  
api.add_resource(RULPrediction, '/RUL_Predict') 
   
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)

