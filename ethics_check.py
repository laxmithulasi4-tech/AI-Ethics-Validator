import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv("data.csv")

# Calculate Result using pass mark logic (>=35)
data["Calculated_Result"] = data["Marks"].apply(
    lambda x: "Pass" if x >= 35 else "Fail"
)


# ---------------- GENDER BIAS ----------------
gender_total = data.groupby("Gender").size()
gender_passed = data[data["Result"] == "Pass"].groupby("Gender").size()
gender_pass_pct = (gender_passed / gender_total) * 100
gender_diff = abs(gender_pass_pct.max() - gender_pass_pct.min())

# ---------------- ATTENDANCE BIAS ----------------
data["Attendance_Group"] = data["Attendance"].apply(
    lambda x: "Low Attendance" if x < 70 else "High Attendance"
)

att_total = data.groupby("Attendance_Group").size()
att_passed = data[data["Result"] == "Pass"].groupby("Attendance_Group").size()
att_pass_pct = (att_passed / att_total) * 100
att_pass_pct = att_pass_pct.fillna(0)
att_diff = abs(att_pass_pct.max() - att_pass_pct.min())

# ---------------- MARKS BIAS ----------------
data["Marks_Group"] = data["Marks"].apply(
    lambda x: "Low Marks" if x < 75 else "High Marks"
)

marks_total = data.groupby("Marks_Group").size()
marks_passed = data[data["Result"] == "Pass"].groupby("Marks_Group").size()
marks_pass_pct = (marks_passed / marks_total) * 100
marks_pass_pct = marks_pass_pct.fillna(0)
marks_diff = abs(marks_pass_pct.max() - marks_pass_pct.min())

# ---------------- ETHICS SCORE ----------------
avg_diff = (gender_diff + att_diff + marks_diff) / 3
ethics_score = max(0, 100 - avg_diff)

# ---------------- OUTPUT ----------------
print("\nGENDER PASS %:\n", gender_pass_pct)
print("Gender Bias Difference:", gender_diff)

print("\nATTENDANCE PASS %:\n", att_pass_pct)
print("Attendance Bias Difference:", att_diff)

print("\nMARKS PASS %:\n", marks_pass_pct)
print("Marks Bias Difference:", marks_diff)

print("\nOVERALL ETHICS SCORE:", ethics_score)

if ethics_score < 50:
    print("❌ HIGH RISK: AI IS UNETHICAL")
elif ethics_score < 80:
    print("⚠️ MODERATE RISK: REVIEW REQUIRED")
else:
    print("✅ LOW RISK: AI IS ETHICAL")

# ---------------- VISUALIZATION ----------------
plt.figure()
gender_pass_pct.plot(kind="bar")
plt.title("Gender Bias Analysis")
plt.ylabel("Pass Percentage")
plt.ylim(0, 100)
# SAVE IMAGE FOR PROOF
plt.savefig("outputs/gender_bias_output.png")

plt.show()
print("\nRECOMMENDATIONS TO REDUCE BIAS:")

if gender_diff > 20:
    print("- Review gender-based outcome imbalance")
    print("- Ensure gender is not directly or indirectly influencing decisions")

if att_diff > 50:
    print("- Avoid strict attendance cutoffs")
    print("- Consider attendance as a supportive factor, not a rejection factor")

if marks_diff > 50:
    print("- Avoid single pass-mark threshold decisions")
    print("- Introduce grace marks or human review for borderline cases")

print("- Combine multiple factors instead of relying on one rule")
print("- Include human oversight for critical decisions")
