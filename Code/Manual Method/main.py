import logic
import psqi
from datetime import datetime

# 1. Determine Diagnosis
if logic.psqi_number <= 5:
    diagnosis = "Good Sleep Quality"
else:
    diagnosis = "Poor Sleep Quality"

# 2. Create the Report Content
report = f"""
==================================================
PSQI SLEEP QUALITY REPORT
==================================================
Patient Name: {psqi.name}
Date of Test: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
--------------------------------------------------
COMPONENT SCORES:
C1 (Subjective Quality):  {logic.comp1_score}
C2 (Sleep Latency):       {logic.comp2_score}
C3 (Sleep Duration):      {logic.comp3_score}
C4 (Sleep Efficiency):    {logic.comp4_score}
C5 (Sleep Disturbances):  {logic.comp5_score}
C6 (Use of Meds):         {logic.comp6_score}
C7 (Daytime Dysfunction): {logic.comp7_score}
--------------------------------------------------
GLOBAL PSQI SCORE: {logic.psqi_number}
DIAGNOSIS: {diagnosis}
==================================================
"""

print(f"PSQI SCORE = {logic.psqi_number}")

clean_name = psqi.name.replace(" ", "_")
filename = f"{clean_name}_PSQI.txt"

with open(filename, "w") as file:
    file.write(report)

print(f"Report has been successfully created: {filename}")