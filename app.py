import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Salary Comparison App", layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #f5fff5;
    }
    .stApp {
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💼 Salary Comparison App")
st.markdown("Compare your salary across 2025, 2026, and 2027 with adjustments for CPI and more.")

# Sidebar for user inputs
st.sidebar.header("🔧 Salary Input Settings")

base_pay = st.sidebar.number_input("Base Pay (PKR)", min_value=0, value=50000)
percent_change = st.sidebar.number_input("Increase/Decrease in %", value=0)
adjusted_base_pay = base_pay * (1 + percent_change / 100)

transport = st.sidebar.number_input("Transportation Allowance", value=8000)
shift = st.sidebar.number_input("Shift Allowance", value=0)
entertainment = st.sidebar.number_input("Entertainment Allowance", value=0)
laundry = st.sidebar.number_input("Laundry Allowance", value=0)
sales = st.sidebar.number_input("Sales Allowance", value=0)
technical = st.sidebar.number_input("Technical Allowance", value=0)
cola_percent = st.sidebar.number_input("COLA (%)", value=0.0)
income_tax = st.sidebar.number_input("Income Tax", value=0)

has_13th_salary = st.sidebar.checkbox("Include 13th Salary?")
cpi = st.sidebar.number_input("Consumer Price Index (CPI) %", value=10.0)

# Function to calculate salary
def calculate_salary(base, year_multiplier=1):
    cola = base * (cola_percent / 100)
    housing = base * 0.45
    utility = base * 0.10
    thirteenth = base if has_13th_salary else 0
    total_income = (
        base + housing + utility + transport + shift + entertainment +
        laundry + sales + technical + cola + thirteenth
    )

    provident_fund = base * 0.10
    total_deductions = provident_fund + income_tax
    net = total_income - total_deductions

    # Apply CPI multiplier
    net_adjusted = net * ((1 + (cpi / 100)) ** year_multiplier)
    return round(net_adjusted)

# Prepare year-wise salary
years = [2025, 2026, 2027]
salaries = [calculate_salary(adjusted_base_pay, i) for i in range(3)]

# Display results
df = pd.DataFrame({
    "Year": years,
    "Net Salary (Adjusted with CPI)": salaries
})

st.subheader("📊 Net Salary Year-wise (After Allowances & Deductions)")
st.dataframe(df)

# Plotting
fig, ax = plt.subplots()
ax.bar(df["Year"].astype(str), df["Net Salary (Adjusted with CPI)"], color="green")
ax.set_ylabel("Net Salary (PKR)")
ax.set_title("Year-wise Net Salary Comparison")
st.pyplot(fig)

