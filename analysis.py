import pandas as pd
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
import math

# Load the dataset
experiment_data = pd.read_csv('experiment_data.csv')

# Define the column names for the 'Target_Size', 'Distance_from_center', and 'Trial_time'
W = 'Target_size'  # Replace with the actual column name for Width (your size of targets)
A = 'Distance_from_center'  # Replace with the actual column name for Amplitude (distance from center)
T = 'Trial_time'  # Replace with the actual column name for Trial Time (how long your trials took)

# Calculate mean for each configuration
means = experiment_data.groupby([W, A])[T].mean().reset_index()

# Calculate standard deviation for each configuration
std_devs = experiment_data.groupby([W, A])[T].std().reset_index()

# Identify and remove outliers over 3 deviations
def remove_outliers(df, std_devs):
    cleaned_df = pd.DataFrame()
    for index, row in std_devs.iterrows():
        width = row[W]
        amplitude = row[A]
        mean = row[T]
        std = std_devs[(std_devs[W] == width) & (std_devs[A] == amplitude)][T].values[0]
        condition = df[(df[W] == width) & (df[A] == amplitude)]
        condition = condition[(condition[T] >= mean - 3 * std) & (condition[T] <= mean + 3 * std)]
        cleaned_df = pd.concat([cleaned_df, condition])
    return cleaned_df

cleaned_data = remove_outliers(experiment_data, std_devs)

# Recalculate means without outliers
cleaned_means = cleaned_data.groupby([W, A])[T].mean().reset_index()

# Calculate Index of Difficulty (ID) for each configuration
cleaned_means['ID'] = np.log2((cleaned_means[A] / cleaned_means[W]) + 1)

# Calculate Index of Performance (IP) for each configuration
cleaned_means['IP'] = cleaned_means['ID'] / cleaned_means[T]  # IP in bits per second

# Rename columns to A, W, ID, MT, and IP
cleaned_means.rename(columns={W: 'W', A: 'A', T: 'MT'}, inplace=True)

# Scatter chart with ID on X axis and MT on Y axis
plt.scatter(cleaned_means['ID'], cleaned_means['MT'])

# Linear regression
slope, intercept, r_value, _, _ = linregress(cleaned_means['ID'], cleaned_means['MT'])
line = slope * cleaned_means['ID'] + intercept

plt.plot(cleaned_means['ID'], line, 'r', label=f'y={slope:.2f}x+{intercept:.2f}\n$R^2$={r_value**2:.2f}')
plt.legend()

plt.xlabel('Index of Difficulty (ID)')
plt.ylabel('Mean Trial Time (MT)')
plt.title('ID vs. MT Scatter Chart with Linear Regression')
plt.show()

# Print the cleaned means dataframe with updated column names
print(cleaned_means)
