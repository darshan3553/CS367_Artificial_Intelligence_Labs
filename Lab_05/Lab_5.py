# Part 1: Data Collection and Preprocessing
try:
    import yfinance as yf
except ModuleNotFoundError:
    import os
    os.system('pip install yfinance')
    import yfinance as yf

import pandas as pd

# Download historical stock data (Apple Inc.)
ticker = 'AAPL'
data = yf.download(ticker, start='2010-01-01', end='2020-01-01')

# Display first few rows of the data
print(data.head())

# Calculate daily returns from adjusted close prices
data['Daily_Returns'] = data['Adj Close'].pct_change()

# Drop missing values (if any)
data.dropna(inplace=True)

# Show the first few rows of the data with returns
print(data.head())

# Part 2: Gaussian Hidden Markov Model
try:
    from hmmlearn.hmm import GaussianHMM
except ModuleNotFoundError:
    import os
    os.system('pip install hmmlearn')
    from hmmlearn.hmm import GaussianHMM

import numpy as np

# Reshape the returns data to fit HMM model (HMM expects a 2D array)
returns_data = data['Daily_Returns'].values.reshape(-1, 1)

# Initialize HMM model with 2 hidden states (low and high volatility)
model = GaussianHMM(n_components=2, covariance_type="full", n_iter=1000, random_state=42)

# Fit the model to the returns data
model.fit(returns_data)

# Predict the hidden states
hidden_states = model.predict(returns_data)

# Add the hidden states to the original data
data['Hidden_State'] = hidden_states

# Show the first few rows of the data with hidden states
print(data.head())

# Part 3: Interpretation and Inference
import matplotlib.pyplot as plt

# Plot the adjusted closing price with hidden states color-coded
plt.figure(figsize=(10, 6))
plt.plot(data['Adj Close'], label='Adjusted Close Price', color='black')

# Plot the hidden states over time
plt.scatter(data.index, data['Adj Close'], c=data['Hidden_State'], cmap='viridis', label='Hidden States')
plt.colorbar(label='Hidden State')

plt.title(f"{ticker} Stock Price and Hidden Market States")
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()

# Transition matrix
transition_matrix = model.transmat_

# Display the transition matrix
print("Transition Matrix:")
print(transition_matrix)

# Part 4: Evaluation and Visualization
# Plot the daily returns and color-code the time periods based on hidden states
plt.figure(figsize=(10, 6))
plt.plot(data['Daily_Returns'], label='Daily Returns', color='black')

# Color-code the periods based on hidden state
plt.scatter(data.index, data['Daily_Returns'], c=data['Hidden_State'], cmap='viridis', label='Hidden States')
plt.colorbar(label='Hidden State')

plt.title(f"{ticker} Daily Returns and Market Regimes")
plt.xlabel('Date')
plt.ylabel('Daily Returns')
plt.legend()
plt.show()

# Calculate mean return for each state (regime)
mean_return_per_state = data.groupby('Hidden_State')['Daily_Returns'].mean()
print(mean_return_per_state)

# Part 5: Conclusions and Insights
# Summary of market regimes
state_summary = {
    0: {"Regime": "Low Volatility (Bull Market)", "Mean Return": model.means_[0], "Variance": model.covars_[0]},
    1: {"Regime": "High Volatility (Bear Market)", "Mean Return": model.means_[1], "Variance": model.covars_[1]},
}

for state, summary in state_summary.items():
    print(f"State {state}:")
    print(f"  Regime: {summary['Regime']}")
    print(f"  Mean Return: {summary['Mean Return']}")
    print(f"  Variance: {summary['Variance']}")

# Future State Prediction
# Get the current state (most recent state)
current_state = data['Hidden_State'].iloc[-1]

# Predict the next state using the transition matrix
next_state_prob = transition_matrix[current_state]

print(f"Current State: {current_state}")
print(f"Next State Probabilities: {next_state_prob}")
