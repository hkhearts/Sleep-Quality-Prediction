"""
Sleep Quality ML Model - Research-Based Synthetic Data Generator & Trainer
Based on:
- Pittsburgh Sleep Quality Index (PSQI) research
- Fitbit/wearable sensor studies (SpO2, HRV, EDA, Skin Temp)
- Sleep Medicine literature on REM/Deep sleep correlations
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
import joblib
import os

np.random.seed(42)
N = 80000

# ─────────────────────────────────────────────────────────────────────
# 1. GENERATE LATENT FACTORS (hidden drivers of sleep quality)
# ─────────────────────────────────────────────────────────────────────
# Base sleep health score: 0 (very poor) → 1 (excellent)
base_health = np.random.beta(2.5, 2.5, N)  # bell-shaped around 0.5

# Sub-factors (all [0,1])
circadian_alignment  = np.clip(base_health + np.random.normal(0, 0.15, N), 0, 1)
stress_level         = np.clip(1 - base_health + np.random.normal(0, 0.2, N), 0, 1)
activity_level       = np.clip(base_health + np.random.normal(0, 0.2, N), 0, 1)
screen_exposure      = np.clip(1 - base_health * 0.7 + np.random.normal(0, 0.2, N), 0, 1)

# ─────────────────────────────────────────────────────────────────────
# 2. WEARABLE SENSOR FEATURES (correlated with latent factors)
# ─────────────────────────────────────────────────────────────────────

# Heart Rate (bpm) — lower resting HR = healthier; poor sleepers have elevated night HR
resting_hr = (
    45 + (1 - base_health) * 35
    + stress_level * 10
    + np.random.normal(0, 4, N)
).clip(42, 100).round(1)

# SpO2 (%) — good sleepers maintain >95%; apnea/poor sleep drops it
spo2 = (
    98.5 - (1 - base_health) * 5
    - stress_level * 1.5
    + np.random.normal(0, 0.8, N)
).clip(88, 100).round(1)

# Skin Temperature (°C) — drops ~1-2°C during good sleep (distal warming)
skin_temp = (
    34.5 - base_health * 1.2
    + stress_level * 0.5
    + np.random.normal(0, 0.3, N)
).clip(32.5, 36.5).round(2)

# EDA / Sweat Gland Activity (μS) — high EDA = arousal/stress (bad for sleep)
eda = (
    0.5 + stress_level * 7
    + (1 - base_health) * 3
    + np.random.exponential(0.5, N)
).clip(0.1, 12.0).round(2)

# Active Zone Minutes (AZM) — moderate activity helps sleep
azm = (
    20 + activity_level * 100
    + np.random.normal(0, 15, N)
).clip(0, 150).round(0).astype(int)

# Screen Time before bed (minutes)
screen_time = (
    15 + screen_exposure * 180
    + np.random.normal(0, 20, N)
).clip(0, 240).round(0).astype(int)

# Screen Brightness (0-100)
screen_brightness = (
    20 + screen_exposure * 70
    + np.random.normal(0, 10, N)
).clip(0, 100).round(0).astype(int)

# Stress Management Score (1-100, higher = better managed)
stress_score = (
    80 - stress_level * 60
    + np.random.normal(0, 8, N)
).clip(1, 100).round(0).astype(int)

# ─────────────────────────────────────────────────────────────────────
# 3. SLEEP ARCHITECTURE OUTPUTS
# ─────────────────────────────────────────────────────────────────────

# Sleep Efficiency (%) — time asleep / time in bed
sleep_efficiency = (
    92 - (1 - base_health) * 28
    - stress_level * 5
    + np.random.normal(0, 3, N)
).clip(55, 99).round(1)

# Sleep Latency (minutes to fall asleep)
sleep_latency = (
    8 + (1 - base_health) * 52
    + stress_level * 20
    + screen_exposure * 10
    + np.random.exponential(3, N)
).clip(2, 90).round(0).astype(int)

# WASO — Wake After Sleep Onset (minutes)
waso = (
    5 + (1 - base_health) * 70
    + stress_level * 15
    + np.random.exponential(5, N)
).clip(0, 90).round(0).astype(int)

# REM % (ideal ~20-25%)
rem_pct = (
    22 + base_health * 10
    - stress_level * 8
    + np.random.normal(0, 3, N)
).clip(10, 35).round(1)

# Deep Sleep % (ideal ~15-20%)
deep_pct = (
    14 + base_health * 8
    - (1 - base_health) * 4
    + activity_level * 3
    + np.random.normal(0, 2.5, N)
).clip(5, 28).round(1)

# ─────────────────────────────────────────────────────────────────────
# 4. PSQI SIMULATION (0-21, >5 = poor)
# ─────────────────────────────────────────────────────────────────────
psqi_raw = (
    2
    + (1 - base_health) * 12
    + stress_level * 4
    + screen_exposure * 2
    - activity_level * 1.5
    + np.random.normal(0, 1.5, N)
)
psqi_score = np.clip(psqi_raw, 0, 21).round(0).astype(int)

# ─────────────────────────────────────────────────────────────────────
# 5. SLEEP QUALITY LABEL (multi-class)
# ─────────────────────────────────────────────────────────────────────
# 0 = Poor  (PSQI > 10, efficiency < 72%)
# 1 = Fair  (PSQI 6-10, efficiency 72-84%)
# 2 = Good  (PSQI <= 5, efficiency >= 85%)

labels = []
for i in range(N):
    eff = sleep_efficiency[i]
    psqi = psqi_score[i]
    lat = sleep_latency[i]
    w = waso[i]
    rem = rem_pct[i]
    dep = deep_pct[i]

    # Composite score
    score = (
        (eff - 55) / 44 * 0.35          # efficiency: 0-1
        - (lat / 90) * 0.20             # latency penalty
        - (w / 90) * 0.20              # WASO penalty
        + (rem - 10) / 25 * 0.12       # REM bonus
        + (dep - 5) / 23 * 0.13        # Deep bonus
        - (psqi / 21) * 0.25           # PSQI penalty (overlapping, adds robustness)
        + np.random.normal(0, 0.03)     # small noise
    )

    if score >= 0.35:
        labels.append(2)   # Good
    elif score >= 0.12:
        labels.append(1)   # Fair
    else:
        labels.append(0)   # Poor

labels = np.array(labels)

# ─────────────────────────────────────────────────────────────────────
# 6. ASSEMBLE DATAFRAME
# ─────────────────────────────────────────────────────────────────────
df = pd.DataFrame({
    'heart_rate':         resting_hr,
    'spo2':               spo2,
    'skin_temperature':   skin_temp,
    'eda':                eda,
    'active_zone_min':    azm,
    'screen_time':        screen_time,
    'screen_brightness':  screen_brightness,
    'stress_score':       stress_score,
    'sleep_efficiency':   sleep_efficiency,
    'sleep_latency':      sleep_latency,
    'waso':               waso,
    'rem_pct':            rem_pct,
    'deep_pct':           deep_pct,
    'psqi_score':         psqi_score,
    'sleep_quality':      labels
})

print("Label distribution:")
print(df['sleep_quality'].value_counts().sort_index())
print(df.describe().round(2))

# ─────────────────────────────────────────────────────────────────────
# 7. TRAIN / TEST SPLIT
# ─────────────────────────────────────────────────────────────────────
FEATURES = [
    'heart_rate', 'spo2', 'skin_temperature', 'eda',
    'active_zone_min', 'screen_time', 'screen_brightness',
    'stress_score', 'sleep_efficiency', 'sleep_latency',
    'waso', 'rem_pct', 'deep_pct'
]

X = df[FEATURES]
y = df['sleep_quality']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ─────────────────────────────────────────────────────────────────────
# 8. TRAIN GRADIENT BOOSTING CLASSIFIER (best for tabular data)
# ─────────────────────────────────────────────────────────────────────
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', GradientBoostingClassifier(
        n_estimators=300,
        learning_rate=0.08,
        max_depth=5,
        min_samples_split=20,
        subsample=0.85,
        random_state=42
    ))
])

print("\nTraining Gradient Boosting Classifier...")
pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nTest Accuracy: {acc:.4f} ({acc*100:.2f}%)")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Poor', 'Fair', 'Good']))

# Cross-validation
cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
print(f"\nCV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# ─────────────────────────────────────────────────────────────────────
# 9. SAVE MODEL & FEATURE LIST
# ─────────────────────────────────────────────────────────────────────
out_dir = os.path.dirname(os.path.abspath(__file__))
joblib.dump(pipeline, os.path.join(out_dir, 'sleep_model.pkl'))
joblib.dump(FEATURES, os.path.join(out_dir, 'features.pkl'))

print(f"\nModel saved to: {out_dir}/sleep_model.pkl")
print("Training complete!")
