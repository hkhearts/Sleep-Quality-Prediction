import datetime

def calculate_time_difference(bed_time_str, wake_time_str):
    """
    Calculates hours spent in bed handling midnight crossing.
    Format expected: HH:MM (24-hour format, e.g., 23:00 for 11 PM)
    """
    try:
        t_bed = datetime.datetime.strptime(bed_time_str, "%H:%M")
        t_wake = datetime.datetime.strptime(wake_time_str, "%H:%M")
        
        # Calculate difference
        if t_wake < t_bed:
            # If wake time is earlier than bed time, it means next day (crossed midnight)
            t_wake += datetime.timedelta(days=1)
            
        diff = t_wake - t_bed
        return diff.total_seconds() / 3600 # Return in hours
    except ValueError:
        return 0 # Error handling

print("--- PITTSBURGH SLEEP QUALITY INDEX (PSQI) ---")
name = input("Enter the Name of the Person: ")

# --- INPUT SECTION ---
print("\nINSTRUCTIONS: Please answer for the majority of days in the past month.")
print("For time inputs, please use 24-hour format (e.g., 23:00 for 11 PM, 07:30 for 7:30 AM)")

# Q1 - Q4: Free Entry
q1_bed_time = input("Q1. Usual Bed Time (HH:MM): ")
q2_mins_to_fall_asleep = int(input("Q2. Minutes to fall asleep each night: "))
q3_wake_time = input("Q3. Usual Getting Up Time (HH:MM): ")
q4_hours_slept = float(input("Q4. Hours of ACTUAL sleep per night: "))

# Q5: Frequency Questions (Scale 1-4 mapped to 0-3 later)
print("\nQ5. How often have you had trouble sleeping because you...")
print("Scale: 1=Not during month, 2=Less than once a week, 3=Once/twice a week, 4=Three+ times")

q5a_op = int(input("a) Cannot get to sleep within 30 mins: "))
q5b_op = int(input("b) Wake up in middle of night/early morning: "))
q5c_op = int(input("c) Have to get up to use bathroom: "))
q5d_op = int(input("d) Cannot breathe comfortably: "))
q5e_op = int(input("e) Cough or snore loudly: "))
q5f_op = int(input("f) Feel too cold: "))
q5g_op = int(input("g) Feel too hot: "))
q5h_op = int(input("h) Had bad dreams: "))
q5i_op = int(input("i) Have pain: "))
q5j_op = int(input("j) Other reasons (please describe first if any, else enter 1): "))

# Q6: Subjective Quality
print("\nQ6. How would you rate your sleep quality overall?")
print("1=Very Good, 2=Fairly Good, 3=Fairly Bad, 4=Very Bad")
q6_op = int(input("Enter choice (1-4): "))

# Q7: Meds
print("\nQ7. How often have you taken medicine to help you sleep?")
print("Scale: 1=Not during month, 2=Less than once a week, 3=Once/twice a week, 4=Three+ times")
q7_op = int(input("Enter choice (1-4): "))

# Q8: Dysfunction
print("\nQ8. Trouble staying awake while driving, eating, or social activity?")
print("Scale: 1=Not during month, 2=Less than once a week, 3=Once/twice a week, 4=Three+ times")
q8_op = int(input("Enter choice (1-4): "))

# Q9: Enthusiasm
print("\nQ9. Problem keeping up enough enthusiasm to get things done?")
print("1=No problem, 2=Slight problem, 3=Somewhat of a problem, 4=Big problem")
q9_op = int(input("Enter choice (1-4): "))

# Note: Q10 (Roommate) is excluded from calculation as per PSQI rules.

# --- CALCULATION SECTION ---

# Component 1: Subjective Sleep Quality
# PDF Rule: Very Good(1)=>0, Fairly Good(2)=>1, Fairly Bad(3)=>2, Very Bad(4)=>3
comp1_score = q6_op - 1

# Component 2: Sleep Latency
# Step 1: Score Q2 (Minutes)
if q2_mins_to_fall_asleep <= 15:
    q2_score_val = 0
elif q2_mins_to_fall_asleep <= 30: # Covers 16-30
    q2_score_val = 1
elif q2_mins_to_fall_asleep <= 60:
    q2_score_val = 2
else:
    q2_score_val = 3

# Step 2: Score Q5a (Frequency)
q5a_score_val = q5a_op - 1 # Convert 1-4 scale to 0-3

# Step 3: Sum and Map
comp2_sum = q2_score_val + q5a_score_val
if comp2_sum == 0:
    comp2_score = 0
elif 1 <= comp2_sum <= 2:
    comp2_score = 1
elif 3 <= comp2_sum <= 4:
    comp2_score = 2
else:
    comp2_score = 3

# Component 3: Sleep Duration
# PDF Rule: >7=0, 6-7=1, 5-6=2, <5=3
if q4_hours_slept > 7:
    comp3_score = 0
elif 6 <= q4_hours_slept <= 7:
    comp3_score = 1
elif 5 <= q4_hours_slept < 6:
    comp3_score = 2
else: # Less than 5
    comp3_score = 3

# Component 4: Habitual Sleep Efficiency
# Step 1: Calculate Hours in Bed
hours_in_bed = calculate_time_difference(q1_bed_time, q3_wake_time)

# Step 2: Calculate Efficiency %
if hours_in_bed > 0:
    efficiency_percent = (q4_hours_slept / hours_in_bed) * 100
else:
    efficiency_percent = 0

# Step 3: Assign Score
if efficiency_percent > 85:
    comp4_score = 0
elif 75 <= efficiency_percent <= 84:
    comp4_score = 1
elif 65 <= efficiency_percent <= 74:
    comp4_score = 2
else: # < 65%
    comp4_score = 3

# Component 5: Sleep Disturbances
# Sum of Q5b through Q5j (adjusted to 0-3 scale)
disturb_sum = (q5b_op-1) + (q5c_op-1) + (q5d_op-1) + (q5e_op-1) + \
              (q5f_op-1) + (q5g_op-1) + (q5h_op-1) + (q5i_op-1) + (q5j_op-1)

if disturb_sum == 0:
    comp5_score = 0
elif 1 <= disturb_sum <= 9:
    comp5_score = 1
elif 10 <= disturb_sum <= 18:
    comp5_score = 2
else:
    comp5_score = 3

# Component 6: Use of Sleeping Medication
comp6_score = q7_op - 1

# Component 7: Daytime Dysfunction
# Sum of Q8 and Q9 (adjusted to 0-3 scale)
dysfunction_sum = (q8_op - 1) + (q9_op - 1)

if dysfunction_sum == 0:
    comp7_score = 0
elif 1 <= dysfunction_sum <= 2:
    comp7_score = 1
elif 3 <= dysfunction_sum <= 4:
    comp7_score = 2
else:
    comp7_score = 3

# --- FINAL GLOBAL SCORE ---
global_psqi_score = comp1_score + comp2_score + comp3_score + \
                    comp4_score + comp5_score + comp6_score + comp7_score

print("\n" + "="*30)
print(f"REPORT FOR: {name}")
print("="*30)
print(f"C1 (Subjective Quality): {comp1_score}")
print(f"C2 (Sleep Latency):      {comp2_score}")
print(f"C3 (Sleep Duration):     {comp3_score}")
print(f"C4 (Sleep Efficiency):   {comp4_score} (Eff: {efficiency_percent:.1f}%)")
print(f"C5 (Disturbances):       {comp5_score}")
print(f"C6 (Medication Use):     {comp6_score}")
print(f"C7 (Daytime Dysfunction):{comp7_score}")
print("-" * 30)
print(f"GLOBAL PSQI SCORE:       {global_psqi_score}")
print("-" * 30)

if global_psqi_score <= 5:
    print("CONCLUSION: Good Sleep Quality")
else:
    print("CONCLUSION: Poor Sleep Quality")