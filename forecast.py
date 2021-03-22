import pandas as pd
import statsmodels.api as sm
from pandas.tseries.offsets import DateOffset


def preprocess_data(df):

    df['TimeStamp'] = df['TimeStamp'].astype('datetime64[s]')
    df = df.set_index('TimeStamp')
    df = df.resample('D').mean()
    df['Failure']=df['GeneratorTemp'].apply(lambda x: 1 if x >= 95 or x <= 1 else 0)
    df = df.drop(['Failure'], axis=1)

    return df

#df = preprocess_data(df)


def forecast(df, feature_name, forecast_time):
    # SARIMAX
    
    model = sm.tsa.statespace.SARIMAX(df[feature_name],
                                      order = (1, 1, 1),
                                      seasonal_order = (1, 1, 1, 30),
                                      enforce_stationarity = False,
                                      enforce_invertibility = False)
    model_fit = model.fit()  
    print("Model AIC:  ", model_fit.aic)
    
    future_dates = [df.index[-1] + DateOffset(days = x) for x in range(0, forecast_time)]
    future_dates = pd.DataFrame(index = future_dates[1:], columns = [('Forecast')])
    f_df = pd.concat([df, future_dates])
    f_df[('Forecast')] = model_fit.predict(start = future_dates.index[0],
                                                      end = future_dates.index[-1],
                                                      dynamic= True)
    f_df = f_df.fillna("")
    return f_df

