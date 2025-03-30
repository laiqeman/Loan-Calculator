import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate_loan(amount, rate, years, frequency):
    n = {'Monthly': 12, 'Yearly': 1}[frequency]
    r = (rate / 100) / n  # Convert annual rate to per-period rate
    total_periods = years * n
    
    if r > 0:
        payment = amount * (r * (1 + r) ** total_periods) / ((1 + r) ** total_periods - 1)
    else:
        payment = amount / total_periods
    
    schedule = []
    balance = amount
    total_interest = 0
    
    for period in range(1, total_periods + 1):
        interest = balance * r
        principal = payment - interest
        balance -= principal
        total_interest += interest
        schedule.append([period, payment, principal, interest, max(0, balance)])
    
    return payment, total_interest, pd.DataFrame(schedule, columns=["Period", "Payment", "Principal", "Interest", "Balance"])

# Streamlit UI
st.title("📊 Loan Calculator")

# User Inputs
loan_amount = st.number_input("Loan Amount ($)", min_value=1000, value=50000, step=1000)
interest_rate = st.slider("Annual Interest Rate (%)", 0.1, 20.0, 5.0, 0.1)
loan_term = st.slider("Loan Term (Years)", 1, 30, 10)
payment_frequency = st.selectbox("Payment Frequency", ["Monthly", "Yearly"])

# Compute Loan
if st.button("Calculate Loan"):  
    monthly_payment, total_interest, amortization_df = calculate_loan(loan_amount, interest_rate, loan_term, payment_frequency)
    
    st.subheader("📌 Loan Summary")
    st.write(f"**{payment_frequency} Payment:** ${monthly_payment:.2f}")
    st.write(f"**Total Interest Paid:** ${total_interest:.2f}")
    st.write(f"**Total Repayment Amount:** ${loan_amount + total_interest:.2f}")
    
    st.subheader("📈 Loan Amortization Schedule")
    st.dataframe(amortization_df)
    
    # Visualization
    fig, ax = plt.subplots()
    ax.plot(amortization_df["Period"], amortization_df["Balance"], label="Remaining Balance", color='blue')
    ax.set_xlabel("Period")
    ax.set_ylabel("Balance ($)")
    ax.set_title("Loan Balance Over Time")
    ax.legend()
    st.pyplot(fig)
    
    # Pie Chart for Payment Breakdown
    labels = ['Principal', 'Interest']
    sizes = [loan_amount, total_interest]
    fig2, ax2 = plt.subplots()
    ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
    ax2.axis('equal')  # Equal aspect ratio ensures pie is a circle.
    st.pyplot(fig2)

st.markdown("### ✅ Developed with Streamlit")
