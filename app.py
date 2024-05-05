import pickle
import numpy as np
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load pre-trained Models
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
    return 'Univaraite Anomaly Detection & RUL Estimation'

@app.route('/Ano_Det_Uni', methods=['POST'])
def post():
    posted_data = request.get_json(force=True)
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

# RUL Prediction
@app.route('/RUL_Predict', methods=['POST'])
def post1():
    posted_data2 = request.get_json(force=True)
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

   
if __name__ == '__main__':
    app.run(port=5000,debug=True)

