import psqi
from datetime import datetime, timedelta

# Component 1: Subjective Sleep Quality

comp1_score = psqi.q6_op - 1

# Component 2: Sleep Latency

# 1. Q2 Score
if(psqi.no_of_mins_q2 <= 15):
    q2_score = 0
elif(psqi.no_of_mins_q2 <= 30):
    q2_score = 1
elif(psqi.no_of_mins_q2 <= 60):
    q2_score = 2
else:
    q2_score = 3

# 2. Question 5a
q5a_score = psqi.q5a_op - 1

# 3. Addition
sum_od_2_5a = q2_score + q5a_score

# Component2 score
if(sum_od_2_5a == 0):
    comp2_score = 0
elif(sum_od_2_5a >= 1 and sum_od_2_5a <=2):
    comp2_score = 1
elif(sum_od_2_5a >= 3 and sum_od_2_5a <= 4):
    comp2_score = 2
elif(sum_od_2_5a >=5 and sum_od_2_5a <=6):
    comp2_score = 3

# Component 3: Sleep duration
# Note: Logic corrected to match PDF (>7 is good, <5 is bad)
if(psqi.hour_of_sleep_per_night > 7):
    comp3_score = 0
elif(psqi.hour_of_sleep_per_night >= 6):
    comp3_score = 1
elif(psqi.hour_of_sleep_per_night >= 5):
    comp3_score = 2
else:
    comp3_score = 3
    
# Component 4: Habitual sleep efficiency
fmt = "%H:%M"
t_bed = datetime.strptime(psqi.usual_bed_time, fmt)
t_wake = datetime.strptime(psqi.usual_getting_up_time, fmt)

# Handle crossing midnight (next day)
if t_wake < t_bed:
    t_wake += timedelta(days=1)

diff = t_wake - t_bed
no_of_hours_spent_in_bed = diff.total_seconds() / 3600

habitual_sleep_efficiency = (psqi.hour_of_sleep_per_night/no_of_hours_spent_in_bed) * 100

if(habitual_sleep_efficiency < 65):
    comp4_score = 3
elif(habitual_sleep_efficiency <= 74):
    comp4_score = 2
elif(habitual_sleep_efficiency <= 84):
    comp4_score = 1
else:
    comp4_score = 0

# Component 5: Step distrubances

# Decrement q5b through q5j by 1
psqi.q5b_op, psqi.q5c_op, psqi.q5d_op, psqi.q5e_op, psqi.q5f_op, psqi.q5g_op, psqi.q5h_op, psqi.q5i_op, psqi.q5j_op = map(lambda x: x - 1, [psqi.q5b_op, psqi.q5c_op, psqi.q5d_op, psqi.q5e_op, psqi.q5f_op, psqi.q5g_op, psqi.q5h_op, psqi.q5i_op, psqi.q5j_op])

disturbances = [
    psqi.q5b_op, psqi.q5c_op, psqi.q5d_op, 
    psqi.q5e_op, psqi.q5f_op, psqi.q5g_op, 
    psqi.q5h_op, psqi.q5i_op, psqi.q5j_op
]

sum_of_5b_5j = sum(disturbances)

if sum_of_5b_5j == 0:
    comp5_score = 0
elif 1 <= sum_of_5b_5j <= 9:
    comp5_score = 1
elif 10 <= sum_of_5b_5j <= 18:
    comp5_score = 2
else: # 19-27
    comp5_score = 3

# Component 6: Use of sleeping medication
comp6_score = psqi.q7_op - 1

# Component 7: Day Time dysfuntion

sum_od_8_9 = (psqi.q8_op - 1) + (psqi.q9_op - 1)


# Component 7 score
if(sum_od_8_9 == 0):
    comp7_score = 0
elif(sum_od_8_9 >= 1 and sum_od_8_9 <=2):
    comp7_score = 1
elif(sum_od_8_9 >= 3 and sum_od_8_9 <= 4):
    comp7_score = 2
elif(sum_od_8_9 >=5 and sum_od_8_9 <=6):
    comp7_score = 3
    

# PSQI final Score
result_list = [
    comp1_score, comp2_score, comp3_score, comp4_score,
    comp5_score, comp6_score, comp7_score
]

psqi_number = sum(result_list)