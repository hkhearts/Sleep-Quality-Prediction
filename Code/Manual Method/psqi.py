# The personal details of the patients
name = input("Enter the Name of the Person: ")

# So the questions to be asked is seperated into the 7 components

# THe instructions
instruction = "The following questions relate to your usual sleep habits during the past month only. Your answers should indicate the most accurate reply for the majority of the days and nights in the past month. \nPlease answer all questions."
print(instruction)

''' These are the questioneries for the time calculation '''

# Question 1
q1 = "During the past month, when have you usually gonna to bed at night? (HH:MM 24-hr format)"
print(q1)
usual_bed_time = input()

# Question 2
q2 = "During the past month, how long (in minutes) has it usually take you to fall asleep each night?"
print(q2)
no_of_mins_q2 = int(input())

# Question 3
q3 = "During the past month, when have you usually gotten up in the morning? (HH:MM 24-hr format)"
print(q3)
usual_getting_up_time = input()

# Question 4
q4 = "During the past month, how many hours of actual sleep did u get at night?(This maybe different than number of hours you spend in bed.) (give the data in HOURS)"
print(q4)
hour_of_sleep_per_night = float(input())


''' These are the Check one for the best response question '''
# Question 5
q5 = "During the past month, how often have you had trouble sleeping because you"
print(q5)

print("a) ..can't get to sleep within 30 minutes")
print("    1. Not during the past month")
print("    2. Less than once a week")
print("    3. Once or twice a week")
print("    4. Three or more times a week")
q5a_op = int(input("Enter the number for the question: "))

print("b) ..wake up in the middle of the night or early morning")
print("    1. Not during the past month")
print("    2. Less than once a week")
print("    3. Once or twice a week")
print("    4. Three or more times a week")
q5b_op = int(input("Enter the number for the question: "))

print("c) ..have to get up to use the bathroom")
print("    1. Not during the past month")
print("    2. Less than once a week")
print("    3. Once or twice a week")
print("    4. Three or more times a week")
q5c_op = int(input("Enter the number for the question: "))

print("d) ..can't breathe comfortably")
print("    1. Not during the past month")
print("    2. Less than once a week")
print("    3. Once or twice a week")
print("    4. Three or more times a week")
q5d_op = int(input("Enter the number for the question: "))

print("e) ..cough or snore loudly")
print("    1. Not during the past month")
print("    2. Less than once a week")
print("    3. Once or twice a week")
print("    4. Three or more times a week")
q5e_op = int(input("Enter the number for the question: "))

print("f) ..feel too cold")
print("    1. Not during the past month")
print("    2. Less than once a week")
print("    3. Once or twice a week")
print("    4. Three or more times a week")
q5f_op = int(input("Enter the number for the question: "))

print("g) ..feel too hot")
print("    1. Not during the past month")
print("    2. Less than once a week")
print("    3. Once or twice a week")
print("    4. Three or more times a week")
q5g_op = int(input("Enter the number for the question: "))

print("h) ..had bad dreams")
print("    1. Not during the past month")
print("    2. Less than once a week")
print("    3. Once or twice a week")
print("    4. Three or more times a week")
q5h_op = int(input("Enter the number for the question: "))

print("i) ..have pain")
print("    1. Not during the past month")
print("    2. Less than once a week")
print("    3. Once or twice a week")
print("    4. Three or more times a week")
q5i_op = int(input("Enter the number for the question: "))

print("j) Other Reasons")
other_describe_5 = input("Please Describe in your own words: ")

print("How often during the past month have you had trouble sleeping because of this")
print("    1. Not during the past month")
print("    2. Less than once a week")
print("    3. Once or twice a week")
print("    4. Three or more times a week")
q5j_op = int(input("Enter the number for the question: "))

# Question 6
q6 = "During the past month, how would you rate ur sleep quality overall?"
print(q6)
print("    1. Very good")
print("    2. Fairly good")
print("    3. Fairly bad")
print("    4. Very bad")
q6_op = int(input("Enter the number for the question: "))

# Question 7
q7 = "During the past month, how often have you taken medicine (prescribed or 'over the counter') to help you sleep?"
print(q7)
print("    1. Not during the past month")
print("    2. Less than once a week")
print("    3. Once or twice a week")
print("    4. Three or more times a week")
q7_op = int(input("Enter the number for the question: "))

# Question 8
q8 = "During the past month, how often have you had trouble staying awake while driving, eating mesls, or engagging in social activity?"
print(q8)
print("    1. Not during the past month")
print("    2. Less than once a week")
print("    3. Once or twice a week")
print("    4. Three or more times a week")
q8_op = int(input("Enter the number for the question: "))

# Question 9
q9 = "During the past month, how much of a problem has it been for you to keep up enough enthusiasm to get things done?"
print(q9)
print("    1. No Problem at all")
print("    2. Only a very Slight problem")
print("    3. Somewhat of a problem")
print("    4. A very big problem")
q9_op = int(input("Enter the number for the question: "))

# The roommate question 
print("Answer to this fo the further questions")
print("1. No bed partner or roomate")
print("2. Partner/roomate in other room")
print("3. Partner in same room, but not same bed")
print("4. Partner in same bed")

rm_q = int(input())

if(rm_q > 0):
    
    # Question 10
    q10 = "During the past month, how much of a problem has it been for you to keep up enough enthusiasm to get things done?"
    print("ASk your roommate or bed artner, ask him/her how often in the past month you have had")
    
    print("a) ..loud snoring")
    print("    1. Not during the past month")
    print("    2. Less than once a week")
    print("    3. Once or twice a week")
    print("    4. Three or more times a week")
    q10a_op = int(input("Enter the number for the question: "))
    
    print("b) ..loud pauses between breaths while asleep")
    print("    1. Not during the past month")
    print("    2. Less than once a week")
    print("    3. Once or twice a week")
    print("    4. Three or more times a week")
    q10b_op = int(input("Enter the number for the question: "))
    
    print("c) ..legs twitching or jerking while you sleep")
    print("    1. Not during the past month")
    print("    2. Less than once a week")
    print("    3. Once or twice a week")
    print("    4. Three or more times a week")
    q10c_op = int(input("Enter the number for the question: "))
    
    print("d) ..episodes of disorientation or confusion during sleep")
    print("    1. Not during the past month")
    print("    2. Less than once a week")
    print("    3. Once or twice a week")
    print("    4. Three or more times a week")
    q10d_op = int(input("Enter the number for the question: "))
    
    print("e) Other Reasons")
    other_describe_10 = input("Please Describe in your own words: ")
    print("    1. Not during the past month")
    print("    2. Less than once a week")
    print("    3. Once or twice a week")
    print("    4. Three or more times a week")
    q10e_op = int(input("Enter the number for the question: "))