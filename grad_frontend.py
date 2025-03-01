import gradio as gr
import numpy as np
import pandas as pd
import backend

import matplotlib.pyplot as plt

def calculate_and_plot(sessions, signups, library, resources, trials):

    # Read the last values from training data
    df = pd.read_csv('data_w_ext.csv')
    last_values = df.iloc[-1]

    # Calculate new values based on percentage changes
    new_values = {
        'sessions': last_values['sessions'] * (1 + sessions/100),
        'signups': last_values['signups'] * (1 + signups/100),
        'library': last_values['library'] * (1 + library/100),
        'resources': last_values['resources'] * (1 + resources/100),
        'trials': last_values['trials'] * (1 + trials/100)
    }

    mean, std = backend.prediction(backend.load_model(), backend.load_synthetic(), new_values)

    # Create array of months from Jan 2022 to Jan 2025
    # Extract paid MAU from training data
    
    paid_mau = df['paid_monthly_active_users'].values
    months = pd.date_range(start='2022-08-01', end='2024-12-01', freq='ME')


    # Plot historical data
    plt.figure(figsize=(10, 6))
    plt.plot(months[:len(paid_mau)], paid_mau, label='Historical')

    # Add prediction point
    prediction_date = months[-1] + pd.DateOffset(months=1)
    plt.plot(prediction_date, mean, 'ro', label='Prediction')

    plt.title('Paid MAU Over Time')
    plt.xlabel('Date')
    plt.ylabel('Paid MAU')
    plt.legend()
    plt.grid(True)
    plt.errorbar(prediction_date, mean, yerr=1.96*std, fmt='none', color='red', capsize=5, label='95% CI')

    
    
    
    summary = f"""Prediction: {mean:,.0f}
                Standard Deviation: {std:,.0f}"""
    
    return plt.gcf(), summary

# Create Gradio interface
iface = gr.Interface(
    fn=calculate_and_plot,
    inputs=[
        gr.Number(label="Sessions", value=0),
        gr.Number(label="Signups", value=0),
        gr.Number(label="Library", value=0),
        gr.Number(label="Resources", value=0),
        gr.Number(label="Trials Increase (%)", value = 0)
    ],
    outputs=[
        gr.Plot(label="Paid MAU"),
        gr.Textbox(label="Next Month Paid MAU", lines=3)
    ],
    title="Buffer Paid MAU prediction",
    description="Calculate and visualize Buffer's Paid MAU"
)

if __name__ == "__main__":
    iface.launch()