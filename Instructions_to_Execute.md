# AI Techniques for Predictive Maintenance
## Instructions to Execute 
* Open the URL "https:/ai-pdm.herokuapp.com/"
* Use Jupyter Notebook or any Script to send & receive data from this app
### Univariate Anomaly Detection
* URL = "https:/ai-pdm.herokuapp.com/Ano_Det_Uni"
* Load __"{"rms":value,"mean":value}"__ as JSON data
	* Ex: *"{"rms": 0.0782, "mean": 0.0619}"*
* API will respond back with JSON data in the form "{"Output": output_value}"
	* Ex: *"{"Output": Normal}"*

### Remaining Useful Life Estimation
* URL = "https:/ai-pdm.herokuapp.com/RUL_Predict"
* Load __"{"Bearing1_RMS":value,"Bearing1_Kurt":value,"Bearing1_RMS_Prev":value,"Bearing1_Kurt_Prev":value}"__ as JSON data
	* Ex: *"{"Bearing1_RMS":0.0790,"Bearing1_Kurt":3.5062,"Bearing1_RMS_Prev":0.0789,"Bearing1_Kurt_Prev":3.5963}"*
* API will respond back with JSON data in the form "{"RUL_Class":output_value,"Fraction Failing":output_value, "RUL":output_value}"
	* Ex: *"{"RUL_Class":2,"Fraction Failing":"20-40%", "RUL":"60%"}"*

### Input - Description
Input|Detail
-----|------
rms|__Root Mean Square__ Value of 1 sec Vibration Signal of __Bearing 1__
mean|__Mean Square__ Value of 1 sec Vibration Signal of __Bearing 1__
Bearing1_RMS|__Root Mean Square__ Value of 1 sec Vibration Signal of __Bearing 1__ at *time t*
Bearing1_Kurt|__Kurtosis__ Value of 1 sec Vibration Signal of __Bearing 1__ at *time t*
Bearing1_RMS_Prev|__Root Mean Square__ Value of 1 sec Vibration Signal of __Bearing 1__ at *time t-1*
Bearing1_Kurt_Prev|__Kurtosis__ Value of 1 sec Vibration Signal of __Bearing 1__ at *time t-1*

#### Note:
* Three outputs are possible (Anomaly Detection): Normal, Anomaly, No Proper Input
	* __Normal__ : Vibrations in Normal Range - Healthy State
	* __Anomaly__: Vibrations exceeds Normal Range - Unhealthy / Possibility of failure in near future
	* __No Proper Input__ : If all inputs are "0" - Sensor Fault / Machine is turned off
* For accurate prediction, input values must be given with atleast four decimal places (Ex: 0.0825)
* Refer Tests folder for examples
* Refer Tests/FE_Data for feature engineered dataset 