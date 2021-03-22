import os
import datetime
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import forecast as f
from flask_bootstrap import Bootstrap


df = (pd.read_excel("wind_turbine_failure.xlsx"))
df = f.preprocess_data(df)
time = df.index.date.tolist()
gentmp_data = df["GeneratorTemp"].tolist()
ambtmp_data = df["Ambient Air temp"].tolist()
nacelle_data = df["Nacelle Position"].tolist()

app = Flask(__name__)
Bootstrap(app)
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/gentmp")
def gentmp():
    times = time
    legend = "Gentemp Values"
    g_data = gentmp_data
    return render_template("gentemp.html", values=g_data, labels=times, legend=legend)

@app.route("/gentmp_predict", methods=['POST'])
def gentmp_predict():
    #times = time
    legend = "Gentemp Values"
    g_data = gentmp_data
    feature_name = 'GeneratorTemp'
    df1 = df.drop(['Ambient Air temp','Nacelle Position'],axis=1)
    forecast_time = int(request.form['input_forecast'])
    forecast_df = f.forecast(df1, feature_name, forecast_time)
    print(forecast_df)
    p_legend = "Predicted Values"
    p_time = forecast_df.index.date.tolist()
    p_gentmp_data = forecast_df["Forecast"].tolist()
    
    forecast_df = forecast_df.reset_index()
    forecast_df = forecast_df.rename(columns={"index": "Timestamp"})
    return render_template("gentemp.html", 
                           values=g_data, 
                           labels=p_time, 
                           legend=legend, 
                           tables=[forecast_df.to_html(classes='forecast_df')],
                           p_legend=p_legend,
                           p_gentmp_data=p_gentmp_data)

@app.route("/ambtmp")
def ambtmp():
    times = time
    legend = "Ambtemp Values"
    a_data = ambtmp_data    
    return render_template("ambtemp.html", values=a_data, labels=times, legend=legend)

@app.route("/ambtmp_predict", methods=['POST'])
def ambtmp_predict():
    #times = time
    legend = "Ambtemp Values"
    a_data = ambtmp_data
    print(df)
    feature_name = 'Ambient Air temp'
    df1 = df.drop(['GeneratorTemp','Nacelle Position'],axis=1)
    forecast_time = int(request.form['input_forecast'])
    forecast_df = f.forecast(df1, feature_name, forecast_time)
    print(forecast_df.head)
    a_legend = "Predicted Values"
    a_time = forecast_df.index.date.tolist()

    a_ambtmp_data = forecast_df["Forecast"].tolist()
    
    forecast_df = forecast_df.reset_index()
    forecast_df = forecast_df.rename(columns={"index": "Timestamp", "Ambient Air temp": "Amb Air temp" })
    return render_template("ambtemp.html", 
                           values=a_data, 
                           labels=a_time, 
                           legend=legend, 
                           tables=[forecast_df.to_html(classes='forecast_df')],
                           a_legend=a_legend,
                           a_ambtmp_data=a_ambtmp_data)

@app.route("/nacelle")
def nacelle():
    times = time
    legend = "Nacelle Position Values"
    n_data = nacelle_data
    return render_template("nacelle.html", values=n_data, labels=times, legend=legend)

@app.route("/nacelle_predict", methods=['POST'])
def nacelle_predict():
    #times = time
    legend = "Nacelle Position Values"
    n_data = nacelle_data
    feature_name = 'Nacelle Position'
    df1 = df.drop(['Ambient Air temp','GeneratorTemp'],axis=1)
    forecast_time = int(request.form['input_forecast'])
    forecast_df = f.forecast(df1, feature_name, forecast_time)
    print(forecast_df)
    n_legend = "Predicted Values"
    n_time = forecast_df.index.date.tolist()
    n_nacelle_data = forecast_df["Forecast"].tolist()
    
    forecast_df = forecast_df.reset_index()
    forecast_df = forecast_df.rename(columns={"index": "Timestamp"})
    return render_template("nacelle.html", 
                           values=n_data, 
                           labels=n_time, 
                           legend=legend, 
                           tables=[forecast_df.to_html(classes='forecast_df')],
                           n_legend=n_legend,
                           n_nacelle_data=n_nacelle_data)


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
#    app.run()

