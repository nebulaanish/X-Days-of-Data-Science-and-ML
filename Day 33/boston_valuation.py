from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

boston_dataset = load_boston()
data = pd.DataFrame(data=boston_dataset.data,columns =boston_dataset.feature_names)

features = data.drop(['INDUS',"AGE"],axis=1)
log_prices = np.log(boston_dataset.target)
target = pd.DataFrame(log_prices,columns = ["PRICES"])

CRIM_idx = 0
ZN_idx = 1
CHAS_idx = 2
RM_idx = 4
PTRATIO_idx = 8
# property_stats is a dummy data to test our model. it needs to have values for all paramters or columns in our dataset
property_stats = np.array(features.mean()).reshape(1,11)
# property_stats

regr = LinearRegression().fit(features,target)
fitted_vals = regr.predict(features)

# Find mean squared and root mean squared errors
MSE = mean_squared_error(target,fitted_vals)
RMSE = np.sqrt(MSE)
RMSE

def get_log_estimate(number_of_rooms,
                    students_per_classroom,
                     next_to_river= False,
                    high_confidence=True):
    
    property_stats[0][RM_idx] = number_of_rooms
    property_stats[0][PTRATIO_idx] = students_per_classroom
    
    if next_to_river:
        property_stats[0][CHAS_idx] = 1
    else:
        property_stats[0][CHAS_idx] = 0
    log_estimate = regr.predict(property_stats)[0][0]
    
    if high_confidence:
        lower_bound = log_estimate - 2* RMSE
        upper_bound = log_estimate + 2* RMSE
        interval = 95
    else:
        lower_bound = log_estimate - RMSE
        upper_bound = log_estimate + RMSE
        interval = 68
    
    return log_estimate,lower_bound,upper_bound,interval


old_median_price =np.median(boston_dataset.target)

today_median_price = 583.3
scale_factor = today_median_price / old_median_price


def get_dollar_estimate(number_of_rooms,students_per_classroom,next_to_river=False,high_confidence=True):
    """ Estimate the price of property in boston.
    Parameters: 
    number_of_rooms -- int
        Number of rooms in the property
    students_per_classroom -- Number of students in a classroom in that area
    
    next_to_river -- bool,optional
        True if property is close to river else False
    high_confidence -- bool,optional
        True for high range and false for a lower range
    
    
    """
    
    
    if number_of_rooms != int(number_of_rooms):
        print("Room number can't be float")
        return
    if number_of_rooms<1 or students_per_classroom <1 or students_per_classroom >100:
        print("Enter realistic values and try again !! ")
        return
    
    log_est,lower,upper,conf = get_log_estimate(number_of_rooms,students_per_classroom,
                                                next_to_river,high_confidence)

    # converting to today's dollar estimated value
    dollar_est = np.e ** log_est * 1000 * scale_factor
    dollar_upper = np.e ** upper * 1000 * scale_factor
    dollar_lower = np.e ** lower * 1000 * scale_factor

    rounded_est = round(dollar_est,-3)
    rounded_upper = round(dollar_upper,-3)
    rounded_lower = round(dollar_lower,-3)

    print(f"Estimated price is {rounded_est}")
    print(f'At {conf}% confidence lower end is {rounded_lower} and higher end is {rounded_upper}')
