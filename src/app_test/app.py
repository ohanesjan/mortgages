# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="Mortgage Schedule Analyzer", layout="wide")

# -----------------------------
# Mortgage Schedule Functions
# -----------------------------

def annuity_mortgage_schedule(rate, loan_value, maturity_months, bulk_repayments, adjust='payment', property_value=None):
    """
    Creates a DataFrame for an annuity mortgage schedule with options to adjust either the maturity
    or the monthly payment after bulk repayments. Includes additional columns for detailed analysis.
    """
    if property_value is None:
        property_value = loan_value

    P = loan_value
    r = rate / 12  # Monthly interest rate
    n = maturity_months

    if r == 0:
        monthly_payment = P / n
    else:
        monthly_payment = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

    remaining_balance = P
    cumulative_paid_amount = 0
    cumulative_paid_principal = 0
    cumulative_paid_interest = 0
    cumulative_bulk_repayments = 0
    cumulative_interest_saved = 0

    original_remaining_balance = P

    bulk_repayment_dict = dict(bulk_repayments)

    data = {
        'month': [],
        'monthly_repayment': [],
        'monthly_principal_repayment': [],
        'monthly_interest_repayment': [],
        'bulk_repayment': [],
        'total_payment': [],
        'cumulatively_paid_amount': [],
        'cumulatively_paid_principal': [],
        'cumulatively_paid_interest': [],
        'cumulative_bulk_repayments': [],
        'interest_saved_this_month': [],
        'cumulative_interest_saved': [],
        'remaining_loan_value': [],
        'remaining_term_months': [],
        'loan_to_value_ratio': []
    }

    month = 1
    n_remaining = n

    while remaining_balance > 0 and n_remaining > 0:
        interest_payment = remaining_balance * r
        original_interest_payment = original_remaining_balance * r
        interest_saved = original_interest_payment - interest_payment
        principal_payment = monthly_payment - interest_payment

        bulk_repayment = bulk_repayment_dict.get(month, 0)
        total_principal_payment = principal_payment + bulk_repayment

        if total_principal_payment > remaining_balance:
            total_principal_payment = remaining_balance
            principal_payment = remaining_balance - bulk_repayment
            monthly_payment = principal_payment + interest_payment

        cumulative_paid_amount += monthly_payment + bulk_repayment
        cumulative_paid_principal += total_principal_payment
        cumulative_paid_interest += interest_payment
        cumulative_bulk_repayments += bulk_repayment
        cumulative_interest_saved += interest_saved

        remaining_balance -= total_principal_payment
        original_remaining_balance -= principal_payment

        ltv_ratio = remaining_balance / property_value

        data['month'].append(month)
        data['monthly_repayment'].append(monthly_payment)
        data['monthly_principal_repayment'].append(principal_payment)
        data['monthly_interest_repayment'].append(interest_payment)
        data['bulk_repayment'].append(bulk_repayment)
        data['total_payment'].append(monthly_payment + bulk_repayment)
        data['cumulatively_paid_amount'].append(cumulative_paid_amount)
        data['cumulatively_paid_principal'].append(cumulative_paid_principal)
        data['cumulatively_paid_interest'].append(cumulative_paid_interest)
        data['cumulative_bulk_repayments'].append(cumulative_bulk_repayments)
        data['interest_saved_this_month'].append(interest_saved)
        data['cumulative_interest_saved'].append(cumulative_interest_saved)
        data['remaining_loan_value'].append(remaining_balance)
        data['remaining_term_months'].append(n_remaining)
        data['loan_to_value_ratio'].append(ltv_ratio)

        if remaining_balance <= 0:
            break

        n_remaining -= 1

        if adjust == 'payment' and bulk_repayment > 0 and remaining_balance > 0:
            if r == 0:
                if n_remaining > 0:
                    monthly_payment = remaining_balance / n_remaining
                else:
                    monthly_payment = remaining_balance
            else:
                if n_remaining > 0:
                    monthly_payment = remaining_balance * (r * (1 + r) ** n_remaining) / ((1 + r) ** n_remaining - 1)
                else:
                    monthly_payment = remaining_balance + remaining_balance * r

        month += 1

    df = pd.DataFrame(data)
    return df

def linear_mortgage_schedule(rate, loan_value, maturity_months, bulk_repayments, adjust='payment', property_value=None):
    """
    Creates a DataFrame for a linear mortgage schedule with options to adjust either the maturity
    or the monthly payment after bulk repayments. Includes additional columns for detailed analysis.
    """
    if property_value is None:
        property_value = loan_value

    P = loan_value
    n = maturity_months
    r = rate / 12  # Monthly interest rate
    monthly_principal_payment = P / n

    remaining_balance = P
    cumulative_paid_amount = 0
    cumulative_paid_principal = 0
    cumulative_paid_interest = 0
    cumulative_bulk_repayments = 0
    cumulative_interest_saved = 0

    original_remaining_balance = P

    bulk_repayment_dict = dict(bulk_repayments)

    data = {
        'month': [],
        'monthly_repayment': [],
        'monthly_principal_repayment': [],
        'monthly_interest_repayment': [],
        'bulk_repayment': [],
        'total_payment': [],
        'cumulatively_paid_amount': [],
        'cumulatively_paid_principal': [],
        'cumulatively_paid_interest': [],
        'cumulative_bulk_repayments': [],
        'interest_saved_this_month': [],
        'cumulative_interest_saved': [],
        'remaining_loan_value': [],
        'remaining_term_months': [],
        'loan_to_value_ratio': []
    }

    month = 1
    n_remaining = n

    while remaining_balance > 0 and n_remaining > 0:
        interest_payment = remaining_balance * r
        monthly_payment = monthly_principal_payment + interest_payment
        original_interest_payment = original_remaining_balance * r
        interest_saved = original_interest_payment - interest_payment

        bulk_repayment = bulk_repayment_dict.get(month, 0)
        total_principal_payment = monthly_principal_payment + bulk_repayment

        if total_principal_payment > remaining_balance:
            total_principal_payment = remaining_balance
            monthly_principal_payment = remaining_balance - bulk_repayment
            monthly_payment = monthly_principal_payment + interest_payment

        cumulative_paid_amount += monthly_payment + bulk_repayment
        cumulative_paid_principal += total_principal_payment
        cumulative_paid_interest += interest_payment
        cumulative_bulk_repayments += bulk_repayment
        cumulative_interest_saved += interest_saved

        remaining_balance -= total_principal_payment
        original_remaining_balance -= monthly_principal_payment

        ltv_ratio = remaining_balance / property_value

        data['month'].append(month)
        data['monthly_repayment'].append(monthly_payment)
        data['monthly_principal_repayment'].append(monthly_principal_payment)
        data['monthly_interest_repayment'].append(interest_payment)
        data['bulk_repayment'].append(bulk_repayment)
        data['total_payment'].append(monthly_payment + bulk_repayment)
        data['cumulatively_paid_amount'].append(cumulative_paid_amount)
        data['cumulatively_paid_principal'].append(cumulative_paid_principal)
        data['cumulatively_paid_interest'].append(cumulative_paid_interest)
        data['cumulative_bulk_repayments'].append(cumulative_bulk_repayments)
        data['interest_saved_this_month'].append(interest_saved)
        data['cumulative_interest_saved'].append(cumulative_interest_saved)
        data['remaining_loan_value'].append(remaining_balance)
        data['remaining_term_months'].append(n_remaining)
        data['loan_to_value_ratio'].append(ltv_ratio)

        if remaining_balance <= 0:
            break

        n_remaining -= 1

        if adjust == 'payment' and bulk_repayment > 0 and remaining_balance > 0:
            if n_remaining > 0:
                monthly_principal_payment = remaining_balance / n_remaining
            else:
                monthly_principal_payment = remaining_balance

        elif adjust == 'maturity' and bulk_repayment > 0 and remaining_balance > 0:
            n_remaining = int(remaining_balance / monthly_principal_payment)
            if remaining_balance % monthly_principal_payment != 0:
                n_remaining += 1  # Add an extra month for any remaining balance
            if n_remaining > 0:
                monthly_principal_payment = remaining_balance / n_remaining
            else:
                monthly_principal_payment = remaining_balance

        month += 1

    df = pd.DataFrame(data)
    return df

def combine_mortgage_schedules(loans, total_property_value=None):
    """
    Combines multiple mortgage schedules into a total schedule, accounting for different loan start months.
    """
    # Find the maximum month among all schedules
    max_month = 0
    for schedule, start_month in loans:
        max_month = max(max_month, start_month + schedule['month'].max() - 1)

    # Initialize DataFrame with months
    per_month_values = pd.DataFrame({'month': range(1, max_month + 1)})
    per_month_values.set_index('month', inplace=True)

    # Initialize columns to zero
    columns_to_sum = [
        'monthly_repayment',
        'monthly_principal_repayment',
        'monthly_interest_repayment',
        'bulk_repayment',
        'total_payment',
        'interest_saved_this_month',
    ]
    for col in columns_to_sum:
        per_month_values[col] = 0.0

    # Initialize total Remaining Loan Value per month
    total_remaining_loan_value = pd.Series(0.0, index=per_month_values.index)

    # For 'remaining_term_months', take the maximum remaining term among loans
    total_remaining_term = pd.Series(0, index=per_month_values.index)

    for schedule, start_month in loans:
        # Adjust the months in the schedule to align with the overall timeline
        schedule_adjusted = schedule.copy()
        schedule_adjusted['month'] = schedule_adjusted['month'] + start_month - 1
        schedule_adjusted.set_index('month', inplace=True)

        # Reindex the DataFrame to have all months, fill missing months appropriately
        df_temp = schedule_adjusted.reindex(per_month_values.index)

        # Forward fill 'remaining_loan_value' and 'remaining_term_months'
        df_temp['remaining_loan_value'] = df_temp['remaining_loan_value'].ffill().fillna(0)
        df_temp['remaining_term_months'] = df_temp['remaining_term_months'].ffill().fillna(0)

        # Fill other columns with zeros where missing
        df_temp = df_temp.fillna(0)

        # Sum per-month values
        for col in columns_to_sum:
            per_month_values[col] += df_temp[col]

        # Sum 'remaining_loan_value'
        total_remaining_loan_value += df_temp['remaining_loan_value']

        # Take the maximum 'remaining_term_months'
        total_remaining_term = total_remaining_term.combine(df_temp['remaining_term_months'], func=max)

    # Reset index to get 'month' as a column
    per_month_values.reset_index(inplace=True)

    # Recalculate cumulative sums
    per_month_values['cumulatively_paid_amount'] = per_month_values['total_payment'].cumsum()
    per_month_values['cumulatively_paid_principal'] = (per_month_values['monthly_principal_repayment'] + per_month_values['bulk_repayment']).cumsum()
    per_month_values['cumulatively_paid_interest'] = per_month_values['monthly_interest_repayment'].cumsum()
    per_month_values['cumulative_bulk_repayments'] = per_month_values['bulk_repayment'].cumsum()
    per_month_values['cumulative_interest_saved'] = per_month_values['interest_saved_this_month'].cumsum()

    # Add 'remaining_loan_value' and 'remaining_term_months' to per_month_values
    per_month_values['remaining_loan_value'] = total_remaining_loan_value.values
    per_month_values['remaining_term_months'] = total_remaining_term.values

    # Calculate 'loan_to_value_ratio' if total_property_value is provided
    if total_property_value is not None:
        per_month_values['loan_to_value_ratio'] = per_month_values['remaining_loan_value'] / total_property_value

    return per_month_values




# -----------------------------
# Streamlit Interface
# -----------------------------

st.title("📊 Mortgage Schedule Analyzer")

st.markdown("""
This application allows you to input parameters for multiple mortgage schedules and visualize their comparative performance through four key interactive plots:
1. **Monthly Payments Over Time**: Breakdown into principal and interest.
2. **Remaining Loan Balance Over Time**.
3. **Cumulative Interest Paid Over Time**.
4. **Difference in Cumulative Interest Paid** compared to the most cost-effective schedule.

You can add or remove mortgage schedules dynamically below.
""")

# Sidebar for total property value
st.sidebar.header("Total Property Value")
total_property_value = st.sidebar.number_input(
    "Enter the total property value (€):",
    min_value=0.0,
    value=300000.0,
    step=1000.0,
    format="%.2f"
)

st.sidebar.markdown("""
---
""")

# Initialize session state for mortgage count
if 'mortgage_count' not in st.session_state:
    st.session_state.mortgage_count = 1

# Functions to add/remove mortgages
def add_mortgage():
    if st.session_state.mortgage_count < 10:
        st.session_state.mortgage_count += 1

def remove_mortgage():
    if st.session_state.mortgage_count > 1:
        st.session_state.mortgage_count -= 1

# Buttons to add/remove mortgages
col_add, col_remove = st.columns(2)
with col_add:
    st.button("➕ Add Mortgage", on_click=add_mortgage)
with col_remove:
    st.button("➖ Remove Mortgage", on_click=remove_mortgage)

st.markdown("---")
st.header("🔄 Input Mortgage Schedules")

# Function to create mortgage input sections
def mortgage_input_section(index):
    with st.expander(f"💼 Mortgage {index + 1} Details", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            mortgage_type = st.selectbox(
                f"Select Mortgage Type for Mortgage {index + 1}:",
                options=["Annuity", "Linear"],
                key=f"type_{index}"
            )
        
        with col2:
            rate = st.number_input(
                f"Enter Annual Interest Rate (%) for Mortgage {index + 1}:",
                min_value=0.0,
                max_value=100.0,
                value=5.0,
                step=0.1,
                format="%.2f",
                key=f"rate_{index}"
            ) / 100  # Convert to decimal
        
        col3, col4 = st.columns(2)
        
        with col3:
            loan_value = st.number_input(
                f"Enter Loan Amount (€) for Mortgage {index + 1}:",
                min_value=0.0,
                value=100000.0,
                step=1000.0,
                format="%.2f",
                key=f"loan_{index}"
            )
        
        with col4:
            maturity_months = st.number_input(
                f"Enter Maturity (Months) for Mortgage {index + 1}:",
                min_value=1,
                max_value=600,
                value=360,
                step=12,
                key=f"maturity_{index}"
            )
        
        st.markdown("**Bulk Repayments:**")
        bulk_repayments_input = st.text_area(
            f"Enter Bulk Repayments for Mortgage {index + 1} (format: month:amount, separated by commas):",
            value="",
            help="Example: 12:5000,36:10000",
            key=f"bulk_{index}"
        )
        
        # Parse bulk repayments
        bulk_repayments = []
        if bulk_repayments_input.strip():
            try:
                entries = bulk_repayments_input.split(',')
                for entry in entries:
                    month, amount = entry.strip().split(':')
                    bulk_repayments.append( (int(month.strip()), float(amount.strip())) )
            except:
                st.error("Please enter bulk repayments in the correct format: month:amount, separated by commas.")
        
        adjust_option = st.radio(
            f"Select Adjustment Option for Mortgage {index + 1}:",
            options=["Payment (default)", "Maturity"],
            index=0,
            key=f"adjust_{index}"
        )
        
        if adjust_option == "Payment (default)":
            adjust = 'payment'
        else:
            adjust = 'maturity'
        
        return {
            'type': mortgage_type.lower(),
            'rate': rate,
            'loan_value': loan_value,
            'maturity_months': maturity_months,
            'bulk_repayments': bulk_repayments,
            'adjust': adjust
        }

# Collect inputs for mortgages
options_list = []
for i in range(st.session_state.mortgage_count):
    mortgage = mortgage_input_section(i)
    # Only add mortgage if loan_value > 0
    if mortgage['loan_value'] > 0:
        options_list.append(mortgage)

# Button to generate plots
if st.button("Generate Plots"):
    if not options_list:
        st.error("Please input at least one mortgage with a loan amount greater than €0.")
    else:
        # Generate schedules
        schedules = []
        labels = []
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']  # Extend colors for up to 10 mortgages
        for idx, mortgage in enumerate(options_list):
            if mortgage['type'] == 'annuity':
                schedule = annuity_mortgage_schedule(
                    rate=mortgage['rate'],
                    loan_value=mortgage['loan_value'],
                    maturity_months=mortgage['maturity_months'],
                    bulk_repayments=mortgage['bulk_repayments'],
                    adjust=mortgage['adjust'],
                    property_value=total_property_value
                )
            elif mortgage['type'] == 'linear':
                schedule = linear_mortgage_schedule(
                    rate=mortgage['rate'],
                    loan_value=mortgage['loan_value'],
                    maturity_months=mortgage['maturity_months'],
                    bulk_repayments=mortgage['bulk_repayments'],
                    adjust=mortgage['adjust'],
                    property_value=total_property_value
                )
            schedules.append(schedule)
            labels.append(f"Mortgage {idx + 1}: {mortgage['type'].capitalize()} Adjust {mortgage['adjust'].capitalize()}")

        # Combine the schedules (assuming all start at month 1)
        loans = [(schedule, 1) for schedule in schedules]
        combined_schedule = combine_mortgage_schedules(loans, total_property_value=total_property_value)

        # Identify the schedule with the lowest cumulative interest paid at the end
        total_cumulative_interests = []
        for schedule in schedules:
            total_cumulative_interests.append(schedule['cumulatively_paid_interest'].iloc[-1])

        min_interest_index = total_cumulative_interests.index(min(total_cumulative_interests))
        min_interest_schedule = schedules[min_interest_index]
        min_label = labels[min_interest_index]

        # Create a DataFrame to align cumulative interests over time
        max_month = max([schedule['month'].max() for schedule in schedules])

        # Initialize a DataFrame with months as the index
        cumulative_interest_df = pd.DataFrame({'month': range(1, max_month + 1)})
        cumulative_interest_df.set_index('month', inplace=True)

        # Add cumulative interest data for each schedule
        for schedule, label in zip(schedules, labels):
            # Reindex the cumulative interest to align months
            temp = schedule.set_index('month')['cumulatively_paid_interest']
            temp = temp.reindex(range(1, max_month + 1), method='ffill')  # Forward fill after loan is paid off
            cumulative_interest_df[label] = temp

        # Add the cumulative interest of the minimum interest schedule
        min_cumulative_interest = cumulative_interest_df[min_label]

        # Compute the difference between each schedule and the minimum interest schedule
        for label in labels:
            cumulative_interest_df[label] = cumulative_interest_df[label] - min_cumulative_interest

        # -----------------------------
        # Plotting with Plotly
        # -----------------------------

        # Create four Plotly figures
        fig1 = go.Figure()
        fig2 = go.Figure()
        fig3 = go.Figure()
        fig4 = go.Figure()

        # Plot 1: Monthly Payments Over Time with breakdown
        for idx, (schedule, label) in enumerate(zip(schedules, labels)):
            color = colors[idx % len(colors)]
            fig1.add_trace(go.Scatter(
                x=schedule['month'],
                y=schedule['monthly_principal_repayment'],
                mode='lines',
                name=f'Principal ({label})',
                line=dict(color=color, width=2)
            ))
            fig1.add_trace(go.Scatter(
                x=schedule['month'],
                y=schedule['monthly_repayment'],
                mode='lines',
                name=f'Total Payment ({label})',
                line=dict(color=color, width=2, dash='dash')
            ))

        fig1.update_layout(
            title="Monthly Payments Over Time",
            xaxis_title="Month",
            yaxis_title="Payment (€)",
            legend_title="Legend",
            template="plotly_white"
        )

        # Plot 2: Remaining Loan Balance Over Time
        for idx, (schedule, label) in enumerate(zip(schedules, labels)):
            color = colors[idx % len(colors)]
            fig2.add_trace(go.Scatter(
                x=schedule['month'],
                y=schedule['remaining_loan_value'],
                mode='lines',
                name=label,
                line=dict(color=color, width=2)
            ))

        fig2.update_layout(
            title="Remaining Loan Balance Over Time",
            xaxis_title="Month",
            yaxis_title="Remaining Loan Balance (€)",
            legend_title="Legend",
            template="plotly_white"
        )

        # Plot 3: Cumulative Interest Paid Over Time
        for idx, (schedule, label) in enumerate(zip(schedules, labels)):
            color = colors[idx % len(colors)]
            fig3.add_trace(go.Scatter(
                x=schedule['month'],
                y=schedule['cumulatively_paid_interest'],
                mode='lines',
                name=label,
                line=dict(color=color, width=2)
            ))

        fig3.update_layout(
            title="Cumulative Interest Paid Over Time",
            xaxis_title="Month",
            yaxis_title="Cumulative Interest Paid (€)",
            legend_title="Legend",
            template="plotly_white"
        )

        # Plot 4: Difference in Cumulative Interest Paid Compared to Minimum Interest Schedule
        for idx, label in enumerate(labels):
            if label != min_label:
                color = colors[idx % len(colors)]
                fig4.add_trace(go.Scatter(
                    x=cumulative_interest_df.index,
                    y=cumulative_interest_df[label],
                    mode='lines',
                    name=label,
                    line=dict(color=color, width=2)
                ))

        fig4.update_layout(
            title="Difference in Cumulative Interest Paid Compared to Minimum Interest Schedule",
            xaxis_title="Month",
            yaxis_title="Difference in Cumulative Interest Paid (€)",
            legend_title="Legend",
            template="plotly_white"
        )

        # Arrange the plots in a 2x2 grid
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            st.plotly_chart(fig2, use_container_width=True)
        with col1:
            st.plotly_chart(fig3, use_container_width=True)
        with col2:
            st.plotly_chart(fig4, use_container_width=True)
