import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Salary Comparison App", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #f5fff5;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💼 Salary Comparison App")
st.markdown("📅 Compare your salary across **2025, 2026, and 2027** with CPI and detailed breakdown.")

# Sidebar Inputs
st.sidebar.header("🔧 Inputs")

base_pay = st.sidebar.number_input("Base Pay (PKR)", min_value=0, value=50000)
percent_change = st.sidebar.number_input("Increase/Decrease in %", value=0)
adjusted_base = base_pay * (1 + percent_change / 100)

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

# Calculation Function
def calculate_components(base):
    housing = base * 0.45
    utility = base * 0.10
    cola = base * (cola_percent / 100)
    thirteenth = base if has_13th_salary else 0

    allowances = {
        "Base Pay": base,
        "Housing (45%)": housing,
        "Utility (10%)": utility,
        "Transportation": transport,
        "Shift": shift,
        "Entertainment": entertainment,
        "Laundry": laundry,
        "Sales": sales,
        "Technical": technical,
        "COLA": cola,
        "13th Salary": thirteenth
    }

    gross = sum(allowances.values())
    deductions = {
        "Provident Fund (10%)": base * 0.10,
        "Income Tax": income_tax
    }
    total_deductions = sum(deductions.values())
    net_salary = gross - total_deductions

    return allowances, deductions, gross, total_deductions, net_salary

# Year-wise Calculations
years = [2025, 2026, 2027]
salary_data = []

for i, year in enumerate(years):
    base_for_year = adjusted_base * ((1 + (cpi / 100)) ** i)
    allowances, deductions, gross, total_deductions, net_salary = calculate_components(base_for_year)
    salary_data.append({
        "Year": year,
        "Gross Pay": round(gross),
        "Total Deductions": round(total_deductions),
        "Net Salary": round(net_salary)
    })

# DataFrame
df = pd.DataFrame(salary_data)

# Display Breakdown
st.subheader("📋 Salary Breakdown")
with st.expander("Click to view breakdown for 2025"):
    allowances, deductions, gross, total_deductions, net = calculate_components(adjusted_base)
    st.markdown("### Allowances")
    st.table(pd.DataFrame(allowances.items(), columns=["Component", "Amount (PKR)"]))
    st.markdown("### Deductions")
    st.table(pd.DataFrame(deductions.items(), columns=["Component", "Amount (PKR)"]))

    st.markdown(f"✅ **Gross Pay:** PKR {round(gross):,.0f}")
    st.markdown(f"🧾 **Total Deductions:** PKR {round(total_deductions):,.0f}")
    st.markdown(f"💰 **Net Salary:** PKR {round(net):,.0f}")

# Display Table
st.subheader("📊 Year-wise Net Salary Summary")
st.dataframe(df)

# Chart
fig, ax = plt.subplots()
ax.bar(df["Year"].astype(str), df["Net Salary"], color="green")
ax.set_title("Net Salary Comparison (2025 - 2027)")
ax.set_ylabel("Net Salary (PKR)")
st.pyplot(fig)
