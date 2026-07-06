import os
import numpy as np
import joblib
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# ---- Load ML model once at startup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH   = os.path.join(BASE_DIR, 'ml', 'sleep_model.pkl')
FEATURE_PATH = os.path.join(BASE_DIR, 'ml', 'features.pkl')

pipeline = joblib.load(MODEL_PATH)
FEATURES = joblib.load(FEATURE_PATH)

LABEL_MAP = {0: 'Poor', 1: 'Fair', 2: 'Good'}
LABEL_COLOR = {
    0: {'primary': '#FF6B6B', 'secondary': '#FF8E8E'},
    1: {'primary': '#FFB347', 'secondary': '#FFD47A'},
    2: {'primary': '#4ECDC4', 'secondary': '#44D4B2'},
}

RECOMMENDATIONS = {
    0: [
        {'icon': '\U0001f319', 'title': 'Strict Sleep Schedule',
         'desc': 'Go to bed and wake up at the same time every day, even on weekends. This resets your circadian rhythm.'},
        {'icon': '\U0001f4f5', 'title': 'Digital Detox 2h Before Bed',
         'desc': 'Your screen time and brightness are high. Blue light suppresses melatonin by up to 85%. Use Night Mode or blue-light glasses.'},
        {'icon': '\U0001f9d8', 'title': 'Stress Reduction Protocol',
         'desc': 'Practice 4-7-8 breathing or progressive muscle relaxation. Your EDA/stress score indicates high arousal that prevents deep sleep.'},
        {'icon': '\U0001f321', 'title': 'Cool Your Sleep Environment',
         'desc': 'Set room temperature to 65-68 F (18-20 C). Your skin temperature data suggests your body is not cooling enough for deep sleep stages.'},
        {'icon': '\U0001f48a', 'title': 'Consult a Sleep Specialist',
         'desc': 'Your PSQI score indicates clinically poor sleep. Consider a formal sleep study to rule out sleep apnea or insomnia.'},
        {'icon': '\U0001f3c3', 'title': 'Morning Exercise',
         'desc': 'Exercise at least 5-6 hours before bed. Even 30 minutes of brisk walking increases deep sleep by 15%.'},
    ],
    1: [
        {'icon': '\u23f0', 'title': 'Optimize Your Bedtime Window',
         'desc': 'Your sleep latency suggests you are going to bed slightly off your natural rhythm. Try adjusting bedtime by 30 minutes earlier.'},
        {'icon': '\U0001f4f1', 'title': 'Reduce Screen Brightness',
         'desc': 'Lower screen brightness to under 30% after sunset. Consider enabling auto Night Mode from 8 PM.'},
        {'icon': '\U0001f375', 'title': 'Evening Ritual',
         'desc': 'Replace evening scrolling with chamomile tea and light reading. This reduces cortisol and prepares your nervous system for sleep.'},
        {'icon': '\U0001f4aa', 'title': 'Increase Active Zone Minutes',
         'desc': 'Aim for 30+ Active Zone Minutes daily. Aerobic exercise significantly improves REM and deep sleep proportions.'},
        {'icon': '\U0001fac1', 'title': 'Improve SpO2 Levels',
         'desc': 'Practice nasal breathing exercises (Buteyko method). Sleeping on your side improves airway patency and oxygen saturation.'},
    ],
    2: [
        {'icon': '\u2728', 'title': 'Excellent Sleep Architecture!',
         'desc': 'Your REM and deep sleep proportions are in the optimal range. Keep up your current sleep routine.'},
        {'icon': '\U0001f3af', 'title': 'Maintain Your Rhythm',
         'desc': 'Your circadian alignment is strong. Consistent sleep/wake times are your biggest asset. Protect them even on weekends.'},
        {'icon': '\U0001f33f', 'title': 'Keep Stress in Check',
         'desc': 'Your stress scores are well managed. Continue mindfulness, journaling, or whatever technique is working for you.'},
        {'icon': '\U0001f3cb', 'title': 'Fine-tune Activity Timing',
         'desc': 'Great active zone minutes! To maximize deep sleep, ensure intense exercise ends 3+ hours before bed.'},
        {'icon': '\U0001f4a7', 'title': 'Hydration Optimization',
         'desc': 'Stay well hydrated during the day but taper off 2 hours before sleep to avoid disruptive nighttime awakenings.'},
    ]
}

INSIGHTS = {
    0: "Your wearable data reveals significant disruptions in your sleep architecture. High stress indicators, elevated EDA, and fragmented sleep patterns are impacting both your REM and deep sleep stages.",
    1: "Your sleep data shows a mixed picture. Some nights are restful, but there is room for meaningful improvement. Small habit changes can push you from Fair to consistently Good sleep.",
    2: "Outstanding! Your biometric data reflects excellent sleep health. Strong sleep efficiency, healthy SpO2 levels, and well-managed stress are combining to give you restorative, high-quality sleep.",
}


def landing(request):
    return render(request, 'analyzer/landing.html')


@csrf_exempt
def simulate_wearable(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    quality_bias = request.POST.get('quality_bias', 'random')

    if quality_bias == 'good':
        base = np.random.uniform(0.7, 1.0)
    elif quality_bias == 'poor':
        base = np.random.uniform(0.0, 0.35)
    else:
        base = np.random.uniform(0.2, 0.9)

    stress = float(np.clip(1 - base + np.random.normal(0, 0.1), 0, 1))
    base = float(base)

    data = {
        'heart_rate':        round(float(np.clip(45 + (1-base)*35 + stress*10 + np.random.normal(0,4), 42, 100)), 1),
        'spo2':              round(float(np.clip(98.5 - (1-base)*5 - stress*1.5 + np.random.normal(0,0.8), 88, 100)), 1),
        'skin_temperature':  round(float(np.clip(34.5 - base*1.2 + stress*0.5 + np.random.normal(0,0.3), 32.5, 36.5)), 2),
        'eda':               round(float(np.clip(0.5 + stress*7 + (1-base)*3 + np.random.exponential(0.5), 0.1, 12.0)), 2),
        'active_zone_min':   int(np.clip(20 + base*100 + np.random.normal(0,15), 0, 150)),
        'screen_time':       int(np.clip(15 + (1-base*0.7)*180 + np.random.normal(0,20), 0, 240)),
        'screen_brightness': int(np.clip(20 + (1-base*0.7)*70 + np.random.normal(0,10), 0, 100)),
        'stress_score':      int(np.clip(80 - stress*60 + np.random.normal(0,8), 1, 100)),
        'sleep_efficiency':  round(float(np.clip(92 - (1-base)*28 - stress*5 + np.random.normal(0,3), 55, 99)), 1),
        'sleep_latency':     int(np.clip(8 + (1-base)*52 + stress*20 + np.random.exponential(3), 2, 90)),
        'waso':              int(np.clip(5 + (1-base)*70 + stress*15 + np.random.exponential(5), 0, 90)),
        'rem_pct':           round(float(np.clip(22 + base*10 - stress*8 + np.random.normal(0,3), 10, 35)), 1),
        'deep_pct':          round(float(np.clip(14 + base*8 - (1-base)*4 + np.random.normal(0,2.5), 5, 28)), 1),
    }
    return JsonResponse(data)


def analyze(request):
    if request.method != 'POST':
        return redirect('landing')
    try:
        input_data = {feat: float(request.POST.get(feat, 0)) for feat in FEATURES}
        X = np.array([[input_data[f] for f in FEATURES]])
        label_idx = int(pipeline.predict(X)[0])
        proba = pipeline.predict_proba(X)[0]

        request.session['result'] = {
            'label':     LABEL_MAP[label_idx],
            'label_idx': label_idx,
            'proba': {
                'Poor': round(float(proba[0]) * 100, 1),
                'Fair': round(float(proba[1]) * 100, 1),
                'Good': round(float(proba[2]) * 100, 1),
            },
            'colors':    LABEL_COLOR[label_idx],
            'insight':   INSIGHTS[label_idx],
            'recommendations': RECOMMENDATIONS[label_idx],
            'inputs':    {k: round(v, 2) for k, v in input_data.items()},
        }
        return redirect('result')
    except Exception as e:
        return render(request, 'analyzer/landing.html', {'error': str(e)})


def result(request):
    data = request.session.get('result')
    if not data:
        return redirect('landing')
    return render(request, 'analyzer/result.html', {'data': data})
