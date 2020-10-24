
## Dataset Description

### Anomaly_Detection_Dataset
Input|Detail
-----|------
Bearing1_Mean|__Mean__ Value of 1 sec Vibration Signal of __Bearing 1__
Bearing2_Mean|__Mean__ Value of 1 sec Vibration Signal of __Bearing 2__
Bearing3_Mean|__Mean__ Value of 1 sec Vibration Signal of __Bearing 3__
Bearing4_Mean|__Mean__ Value of 1 sec Vibration Signal of __Bearing 4__
Bearing1_RMS|__Root Mean Square__ Value of 1 sec Vibration Signal of __Bearing 1__
Bearing1_Kurt|__Kurtosis__ Value of 1 sec Vibration Signal of __Bearing 1__

### RUL_Dataset
Input|Detail
-----|------
Bearing1_RMS|__Root Mean Square__ Value of 1 sec Vibration Signal of __Bearing 1__ at time *_t_*
Bearing1_Kurt|__Kurtosis__ Value of 1 sec Vibration Signal of __Bearing 1__ at time *_t_*
Bearing1_RMS_Prev|__Root Mean Square__ Value of 1 sec Vibration Signal of __Bearing 1__ at time *_t-1_*
Bearing1_Kurt_Prev|__Kurtosis__ Value of 1 sec Vibration Signal of __Bearing 1__ at time *_t-1_*
Class|__Remaining Useful Life__ Class
Class | Fraction Failing | RUL
------|------------------|----
1 | 0-20% | 80%
2 | 20-40% | 60%
3 | 40-60% | 40%
4 | 60-80% | 20%
5 | 80-100% | < 20%
