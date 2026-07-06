import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- 1. Define Dataset Size ---
N_RECORDS = 100000

# --- 2. Generate Time-Related Data ---
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(days=i // 24) for i in range(N_RECORDS)] # Distribute records across time
# Random times, primarily simulating post-sleep measurements (morning)
time_stamps = [f"{np.random.randint(7, 10):02d}:{np.random.randint(0, 60):02d}:{np.random.randint(0, 60):02d}" 
               for _ in range(N_RECORDS)]

# --- 3. Generate Input Variables ---
data = {
    'Date': dates,
    'Time': time_stamps,
    'Skin temperature': np.random.uniform(33.0, 35.0, N_RECORDS).round(2),
    'Screen brightness': np.random.randint(0, 101, N_RECORDS),
    'Screen time': np.random.randint(0, 241, N_RECORDS), # Minutes
    'Blood oxygen levels (SpO₂) Sensor': np.random.randint(90, 100, N_RECORDS),
    'Continuous heart rate': np.random.randint(40, 101, N_RECORDS),
    'Active Zone Minutes': np.random.randint(0, 151, N_RECORDS),
    'Stress management score': np.random.randint(1, 101, N_RECORDS),
    'Activity of sweat gland (EDA sensor data)': np.random.uniform(0.0, 10.0, N_RECORDS).round(1)
}

# --- 4. Generate Output Variables and Weights ---
data['Sleep efficiency'] = np.random.uniform(0.70, 0.98, N_RECORDS).round(3) # 70% to 98%
data['Sleep latency'] = np.random.randint(5, 61, N_RECORDS) # Minutes
data['REM sleep percentage'] = np.random.uniform(0.15, 0.35, N_RECORDS).round(3)
data['Deep sleep percentage'] = np.random.uniform(0.05, 0.25, N_RECORDS).round(3)
data['WASO'] = np.random.randint(10, 91, N_RECORDS) # Wake After Sleep Onset (minutes)

# Weight factors (w1 to w5)
data['w1_efficiency'] = np.random.uniform(0.5, 1.5, N_RECORDS).round(2)
data['w2_WASO'] = np.random.uniform(0.5, 1.5, N_RECORDS).round(2)
data['w3_latency'] = np.random.uniform(0.5, 1.5, N_RECORDS).round(2)
data['w4_deep_sleep'] = np.random.uniform(0.5, 1.5, N_RECORDS).round(2)
data['w5_REM_sleep'] = np.random.uniform(0.5, 1.5, N_RECORDS).round(2)

# --- 5. Calculate Custom Sleep Quality Value ---
df = pd.DataFrame(data)

# Apply the custom formula:
# Sleep Quality Value = w1*SE - w2*WASO - w3*SL + w4*Deep% + w5*REM%
df['Sleep Quality Value'] = (
    df['w1_efficiency'] * df['Sleep efficiency'] -
    df['w2_WASO'] * df['WASO'] / 60 - # Normalize WASO to hours/scale for formula
    df['w3_latency'] * df['Sleep latency'] / 60 + # Normalize Sleep latency
    df['w4_deep_sleep'] * df['Deep sleep percentage'] +
    df['w5_REM_sleep'] * df['REM sleep percentage']
).round(4)

# --- 6. Simulate Pittsburgh Sleep Quality Index (PSQI) Score ---
# PSQI total score ranges from 0 to 21. > 5 is generally poor sleep.
# We'll use a simple method to correlate PSQI inversely with Sleep Quality Value
# and positively with negative metrics like WASO and Latency, adding some noise.
# This simulates the comparison you intend to make.
df['PSQI (Simulated)'] = np.clip(
    (5 + 
     (df['Sleep latency'] / 30) * 1.5 + # Higher latency -> higher PSQI
     (df['WASO'] / 60) * 2 + # Higher WASO -> higher PSQI
     (1 - df['Sleep efficiency']) * 10 + # Lower efficiency -> higher PSQI
     np.random.normal(0, 1.5, N_RECORDS) # Add random noise
    ), 0, 21
).round().astype(int)

# --- 7. Final DataFrame Preparation ---
# Reorder and rename columns for clarity
final_columns = [
    'Date', 'Time', 
    'Skin temperature', 'Screen brightness', 'Screen time', 
    'Blood oxygen levels (SpO₂) Sensor', 'Continuous heart rate', 
    'Active Zone Minutes', 'Stress management score', 
    'Activity of sweat gland (EDA sensor data)',
    # Output Variables (Targets)
    'Sleep efficiency', 'Sleep latency', 'REM sleep percentage', 
    'Deep sleep percentage', 'WASO',
    # Weight Factors
    'w1_efficiency', 'w2_WASO', 'w3_latency', 'w4_deep_sleep', 'w5_REM_sleep',
    # Custom Sleep Performance Metrics
    'Sleep Quality Value', 'PSQI (Simulated)'
]

df = df[final_columns]

# --- 8. Save the Dataset ---
filename = 'synthetic_sleep_performance_dataset_100k.csv'
df.to_csv(filename, index=False)

print(f"Successfully generated {N_RECORDS} records.")
print(f"Dataset saved to: {filename}")
print("\nFirst 5 rows of the generated dataset:")
print(df.head())