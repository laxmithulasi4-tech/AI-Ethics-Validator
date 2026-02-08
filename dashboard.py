import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- TITLE ----------------
st.title("AI Ethics Validator Dashboard")

# ---------------- TOGGLE ----------------
decision_type = st.radio(
    "Select Decision Type to Evaluate:",
    ("Original Result", "Calculated Result (>=35)")
)

# ---------------- LOAD DATA ----------------
data = pd.read_csv("data.csv")

# Calculate Result using pass mark logic (>=35)
data["Calculated_Result"] = data["Marks"].apply(
    lambda x: "Pass" if x >= 35 else "Fail"
)

# Decide which result column to use
if decision_type == "Original Result":
    result_column = "Result"
else:
    result_column = "Calculated_Result"

# =================================================
# 1️⃣ GENDER BIAS
# =================================================
gender_total = data.groupby("Gender").size()
gender_passed = data[data[result_column] == "Pass"].groupby("Gender").size()
gender_pass_pct = (gender_passed / gender_total) * 100

st.subheader("Gender Bias Analysis")

fig1, ax1 = plt.subplots()
gender_pass_pct.plot(kind="bar", ax=ax1)
ax1.set_ylabel("Pass Percentage")
ax1.set_ylim(0, 100)

plt.savefig("dashboard_gender_bias.png")
st.pyplot(fig1)

# =================================================
# 2️⃣ ATTENDANCE BIAS
# =================================================
data["Attendance_Group"] = data["Attendance"].apply(
    lambda x: "Low Attendance" if x < 70 else "High Attendance"
)

att_total = data.groupby("Attendance_Group").size()
att_passed = data[data[result_column] == "Pass"].groupby("Attendance_Group").size()
att_pass_pct = (att_passed / att_total) * 100
att_pass_pct = att_pass_pct.fillna(0)

st.subheader("Attendance Bias Analysis")

fig2, ax2 = plt.subplots()
att_pass_pct.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Pass Percentage")
ax2.set_ylim(0, 100)

plt.savefig("dashboard_attendance_bias.png")
st.pyplot(fig2)

# =================================================
# 3️⃣ MARKS BIAS  ✅ (FIXED)
# =================================================
data["Marks_Group"] = data["Marks"].apply(
    lambda x: "Low Marks" if x < 75 else "High Marks"
)

marks_total = data.groupby("Marks_Group").size()
marks_passed = data[data[result_column] == "Pass"].groupby("Marks_Group").size()
marks_pass_pct = (marks_passed / marks_total) * 100
marks_pass_pct = marks_pass_pct.fillna(0)

st.subheader("Marks Bias Analysis")

fig3, ax3 = plt.subplots()
marks_pass_pct.plot(kind="bar", ax=ax3)
ax3.set_ylabel("Pass Percentage")
ax3.set_ylim(0, 100)

plt.savefig("dashboard_marks_bias.png")
st.pyplot(fig3)

# ---------------- SUCCESS MESSAGE ----------------
st.success("Dashboard Generated Successfully")
