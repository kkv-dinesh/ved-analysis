import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for
from statsmodels.tsa.arima.model import ARIMA

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET'  , 'POST'])
def upload():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Perform VED analysis
    ved_results, chart_path = perform_ved_analysis(file_path)

    # Render the results template with VED analysis results and chart path
    return render_template('results.html', ved_results=ved_results, chart_path=chart_path)

def perform_ved_analysis(file_path):
    # Step 1: Load your data into a pandas DataFrame
    data = pd.read_csv(file_path)
    # Step 2: Preprocess the data
    data = data.fillna(method='ffill')

    # Step 3: Group the data by 'Sub_Category' and aggregate the 'no_of_ratings' column
    demand_data = data.groupby('Sub_Category')['no_of_ratings'].sum().reset_index()

    # Step 4: Filter out rows with out-of-range integer values in 'no_of_ratings'
    demand_data['no_of_ratings'] = pd.to_numeric(demand_data['no_of_ratings'], errors='coerce')
    demand_data = demand_data.dropna(subset=['no_of_ratings'])
    demand_data['no_of_ratings'] = demand_data['no_of_ratings'].astype(int)

    # Step 5: Fit an ARIMA model and forecast for each Sub_Category
    forecasts = {}

    for sub_category, sub_data in data.groupby('Sub_Category'):
        sub_data = sub_data.copy()
        sub_data['no_of_ratings'] = pd.to_numeric(sub_data['no_of_ratings'], errors='coerce')
        sub_data = sub_data.dropna(subset=['no_of_ratings'])
        sub_data['no_of_ratings'] = sub_data['no_of_ratings'].astype(int)
        sub_data = sub_data.loc[sub_data['no_of_ratings'] >= 0]  # Drop rows with negative ratings

        if len(sub_data) > 1:
            sub_data = sub_data.reset_index(drop=True)  # Reset the index

            model = ARIMA(sub_data['no_of_ratings'], order=(1, 0, 1))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=1)  # Forecast only one step ahead

            if forecast is not None and len(forecast) > 0:
                if isinstance(forecast, np.ndarray):
                    forecasts[sub_category] = forecast[0]
                elif isinstance(forecast, pd.Series):
                    forecasts[sub_category] = forecast.iloc[0]
                else:
                    forecasts[sub_category] = np.nan
            else:
                forecasts[sub_category] = np.nan
        else:
            forecasts[sub_category] = np.nan

    # Perform VED analysis
    df_demand_forecast = pd.DataFrame({
        'Sub_Category': list(forecasts.keys()),
        'Forecasted_Demand': list(forecasts.values())
    })

    df_demand_forecast['Cumulative_Demand'] = df_demand_forecast['Forecasted_Demand'].cumsum()
    total_demand = df_demand_forecast['Forecasted_Demand'].sum()
    df_demand_forecast['Percentage_Demand'] = df_demand_forecast['Forecasted_Demand'] / total_demand * 100
    df_demand_forecast['Cumulative_Percentage'] = df_demand_forecast['Percentage_Demand'].cumsum()

    df_demand_forecast['VED_Category'] = pd.cut(df_demand_forecast['Cumulative_Percentage'],
                                                bins=[0, 70, 90, 100],
                                                labels=['Vital', 'Essential', 'Desirable'])

    ved_results = df_demand_forecast.to_dict(orient='records')

    # Count the number of Vital, Essential, and Desirable items
    ved_counts = df_demand_forecast['VED_Category'].value_counts()

    # Generate the pie chart
    ved_labels = ['Vital', 'Essential', 'Desirable']
    ved_values = ved_counts.values.tolist()

    fig, ax = plt.subplots()
    ax.pie(ved_values, labels=ved_labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    chart_path = os.path.join('static', 'ved_chart3.png')

    plt.savefig(chart_path)
    plt.close()

    return ved_results, chart_path

if __name__ == '__main__':
    app.run(debug=True)
