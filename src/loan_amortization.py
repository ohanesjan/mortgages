import pandas as pd

###### Annuity mortgage ######

def annuity_mortgage_schedule(rate, loan_value, maturity_months, bulk_repayments = [], adjust='payment', property_value=None):
    """
    Creates a DataFrame for an annuity mortgage schedule with options to adjust either the maturity
    or the monthly payment after bulk repayments. Includes additional columns for detailed analysis.

    Parameters:
    - rate: Annual fixed interest rate as a decimal (e.g., 0.05 for 5%)
    - loan_value: Initial loan amount
    - maturity_months: Loan term in months
    - bulk_repayments: List of tuples (month, bulk repayment amount)
    - adjust: 'payment' to reduce the monthly payment after bulk repayments (default), or 'maturity' to reduce the loan term
    - property_value: Value of the property (used to calculate LTV ratio). If None, defaults to loan_value.

    Returns:
    - pandas DataFrame with detailed mortgage amortization schedule.
    """

    # Use loan_value as property_value if property_value is not provided
    if property_value is None:
        property_value = loan_value

    # Calculate initial monthly payment
    P = loan_value
    r = rate / 12  # Monthly interest rate
    n = maturity_months

    if r == 0:
        # No interest
        monthly_payment = P / n
    else:
        monthly_payment = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

    # Initialize variables
    remaining_balance = P
    cumulative_paid_amount = 0
    cumulative_paid_principal = 0
    cumulative_paid_interest = 0
    cumulative_bulk_repayments = 0
    cumulative_interest_saved = 0

    # Original schedule without bulk repayments for interest saved calculation
    original_remaining_balance = P

    # Create a dictionary for bulk repayments for quick access
    bulk_repayment_dict = dict(bulk_repayments)

    # Lists to store data
    months = []
    monthly_repayments = []
    monthly_principal_repayments = []
    monthly_interest_repayments = []
    bulk_repayments_list = []
    cumulative_paid_amounts = []
    cumulative_paid_principals = []
    cumulative_paid_interests = []
    cumulative_bulk_repayments_list = []
    remaining_balances = []
    remaining_terms = []
    interest_saved_monthly = []
    cumulative_interest_saved_list = []
    total_payments = []
    ltvs = []

    month = 1
    n_remaining = n

    while remaining_balance > 0 and n_remaining > 0:
        # Interest payment on the beginning balance
        interest_payment = remaining_balance * r

        # Original interest payment without bulk repayments
        original_interest_payment = original_remaining_balance * r

        # Interest saved this month
        interest_saved = original_interest_payment - interest_payment

        # Principal repayment
        principal_payment = monthly_payment - interest_payment

        # Check for bulk repayment
        bulk_repayment = bulk_repayment_dict.get(month, 0)

        # Total principal payment this month
        total_principal_payment = principal_payment + bulk_repayment

        # Adjust if total principal payment exceeds remaining balance
        if total_principal_payment > remaining_balance:
            total_principal_payment = remaining_balance
            principal_payment = remaining_balance - bulk_repayment
            monthly_payment = principal_payment + interest_payment

        # Update cumulative values
        cumulative_paid_amount += monthly_payment + bulk_repayment
        cumulative_paid_principal += total_principal_payment
        cumulative_paid_interest += interest_payment
        cumulative_bulk_repayments += bulk_repayment
        cumulative_interest_saved += interest_saved

        # Update remaining balance
        remaining_balance -= total_principal_payment
        original_remaining_balance -= principal_payment  # Exclude bulk repayments for original schedule

        # Update LTV ratio as a ratio (not percentage)
        ltv_ratio = remaining_balance / property_value

        # Append data to lists
        months.append(month)
        monthly_repayments.append(monthly_payment)
        monthly_principal_repayments.append(principal_payment)
        monthly_interest_repayments.append(interest_payment)
        bulk_repayments_list.append(bulk_repayment)
        cumulative_paid_amounts.append(cumulative_paid_amount)
        cumulative_paid_principals.append(cumulative_paid_principal)
        cumulative_paid_interests.append(cumulative_paid_interest)
        cumulative_bulk_repayments_list.append(cumulative_bulk_repayments)
        remaining_balances.append(remaining_balance)
        remaining_terms.append(n_remaining)
        interest_saved_monthly.append(interest_saved)
        cumulative_interest_saved_list.append(cumulative_interest_saved)
        total_payments.append(monthly_payment + bulk_repayment)
        ltvs.append(ltv_ratio)

        # If loan is paid off, break
        if remaining_balance <= 0:
            break

        # Decrement remaining periods
        n_remaining -= 1

        # Recalculate monthly payment after bulk repayment if 'adjust' is 'payment'
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
                    # Last payment includes all remaining balance and interest
                    monthly_payment = remaining_balance + remaining_balance * r

        # Increment month
        month += 1

    # Create DataFrame with updated column names
    df = pd.DataFrame({
        'month': months,
        'monthly_repayment': monthly_repayments,
        'monthly_principal_repayment': monthly_principal_repayments,
        'monthly_interest_repayment': monthly_interest_repayments,
        'bulk_repayment': bulk_repayments_list,
        'total_payment': total_payments,
        'cumulatively_paid_amount': cumulative_paid_amounts,
        'cumulatively_paid_principal': cumulative_paid_principals,
        'cumulatively_paid_interest': cumulative_paid_interests,
        'cumulative_bulk_repayments': cumulative_bulk_repayments_list,
        'interest_saved_this_month': interest_saved_monthly,
        'cumulative_interest_saved': cumulative_interest_saved_list,
        'remaining_loan_value': remaining_balances,
        'remaining_term_months': remaining_terms,
        'loan_to_value_ratio': ltvs
    })

    return df


###### Linear mortgage ######

def linear_mortgage_schedule(rate, loan_value, maturity_months, bulk_repayments = [], adjust='payment', property_value=None):
    """
    Creates a DataFrame for a linear mortgage schedule with options to adjust either the maturity
    or the monthly payment after bulk repayments. Includes additional columns for detailed analysis.

    Parameters:
    - rate: Annual fixed interest rate as a decimal (e.g., 0.05 for 5%)
    - loan_value: Initial loan amount
    - maturity_months: Loan term in months
    - bulk_repayments: List of tuples (month, bulk repayment amount)
    - adjust: 'payment' to reduce the monthly payment after bulk repayments (default), or 'maturity' to reduce the loan term
    - property_value: Value of the property (used to calculate LTV ratio). If None, defaults to loan_value.

    Returns:
    - pandas DataFrame with detailed mortgage amortization schedule.
    """

    # Use loan_value as property_value if property_value is not provided
    if property_value is None:
        property_value = loan_value

    # Calculate initial monthly principal repayment
    P = loan_value
    n = maturity_months
    r = rate / 12  # Monthly interest rate

    # Initial monthly principal repayment is constant
    monthly_principal_payment = P / n

    # Initialize variables
    remaining_balance = P
    cumulative_paid_amount = 0
    cumulative_paid_principal = 0
    cumulative_paid_interest = 0
    cumulative_bulk_repayments = 0
    cumulative_interest_saved = 0

    # Original schedule without bulk repayments for interest saved calculation
    original_remaining_balance = P

    # Create a dictionary for bulk repayments for quick access
    bulk_repayment_dict = dict(bulk_repayments)

    # Lists to store data
    months = []
    monthly_repayments = []
    monthly_principal_repayments = []
    monthly_interest_repayments = []
    bulk_repayments_list = []
    cumulative_paid_amounts = []
    cumulative_paid_principals = []
    cumulative_paid_interests = []
    cumulative_bulk_repayments_list = []
    remaining_balances = []
    remaining_terms = []
    interest_saved_monthly = []
    cumulative_interest_saved_list = []
    total_payments = []
    ltvs = []

    month = 1
    n_remaining = n

    while remaining_balance > 0 and n_remaining > 0:
        # Interest payment on the beginning balance
        interest_payment = remaining_balance * r

        # Total monthly repayment
        monthly_payment = monthly_principal_payment + interest_payment

        # Original interest payment without bulk repayments
        original_interest_payment = original_remaining_balance * r

        # Interest saved this month
        interest_saved = original_interest_payment - interest_payment

        # Check for bulk repayment
        bulk_repayment = bulk_repayment_dict.get(month, 0)

        # Total principal payment this month
        total_principal_payment = monthly_principal_payment + bulk_repayment

        # Adjust if total principal payment exceeds remaining balance
        if total_principal_payment > remaining_balance:
            total_principal_payment = remaining_balance
            monthly_principal_payment = remaining_balance - bulk_repayment
            monthly_payment = monthly_principal_payment + interest_payment

        # Update cumulative values
        cumulative_paid_amount += monthly_payment + bulk_repayment
        cumulative_paid_principal += total_principal_payment
        cumulative_paid_interest += interest_payment
        cumulative_bulk_repayments += bulk_repayment
        cumulative_interest_saved += interest_saved

        # Update remaining balance
        remaining_balance -= total_principal_payment
        original_remaining_balance -= monthly_principal_payment  # Exclude bulk repayments for original schedule

        # Update LTV ratio as a ratio
        ltv_ratio = remaining_balance / property_value

        # Append data to lists
        months.append(month)
        monthly_repayments.append(monthly_payment)
        monthly_principal_repayments.append(monthly_principal_payment)
        monthly_interest_repayments.append(interest_payment)
        bulk_repayments_list.append(bulk_repayment)
        cumulative_paid_amounts.append(cumulative_paid_amount)
        cumulative_paid_principals.append(cumulative_paid_principal)
        cumulative_paid_interests.append(cumulative_paid_interest)
        cumulative_bulk_repayments_list.append(cumulative_bulk_repayments)
        remaining_balances.append(remaining_balance)
        remaining_terms.append(n_remaining)
        interest_saved_monthly.append(interest_saved)
        cumulative_interest_saved_list.append(cumulative_interest_saved)
        total_payments.append(monthly_payment + bulk_repayment)
        ltvs.append(ltv_ratio)

        # If loan is paid off, break
        if remaining_balance <= 0:
            break

        # Decrement remaining periods
        n_remaining -= 1

        # Recalculate monthly principal payment after bulk repayment if 'adjust' is 'payment'
        if adjust == 'payment' and bulk_repayment > 0 and remaining_balance > 0:
            if n_remaining > 0:
                monthly_principal_payment = remaining_balance / n_remaining
            else:
                monthly_principal_payment = remaining_balance

        # Adjust 'maturity' option
        elif adjust == 'maturity' and bulk_repayment > 0 and remaining_balance > 0:
            n_remaining = int(remaining_balance / monthly_principal_payment)
            if remaining_balance % monthly_principal_payment != 0:
                n_remaining += 1  # Add an extra month for any remaining balance
            if n_remaining > 0:
                monthly_principal_payment = remaining_balance / n_remaining
            else:
                monthly_principal_payment = remaining_balance

        # Increment month
        month += 1

    # Create DataFrame with updated column names
    df = pd.DataFrame({
        'month': months,
        'monthly_repayment': monthly_repayments,
        'monthly_principal_repayment': monthly_principal_repayments,
        'monthly_interest_repayment': monthly_interest_repayments,
        'bulk_repayment': bulk_repayments_list,
        'total_payment': total_payments,
        'cumulatively_paid_amount': cumulative_paid_amounts,
        'cumulatively_paid_principal': cumulative_paid_principals,
        'cumulatively_paid_interest': cumulative_paid_interests,
        'cumulative_bulk_repayments': cumulative_bulk_repayments_list,
        'interest_saved_this_month': interest_saved_monthly,
        'cumulative_interest_saved': cumulative_interest_saved_list,
        'remaining_loan_value': remaining_balances,
        'remaining_term_months': remaining_terms,
        'loan_to_value_ratio': ltvs
    })

    return df



def combine_mortgage_schedules(loans, total_property_value=None):
    """
    Combines multiple mortgage schedules into a total schedule, accounting for different loan start months.

    Parameters:
    - loans: List of tuples, each containing:
        - schedule: pandas DataFrame representing a mortgage schedule.
        - start_month: Integer indicating the starting month of the loan.
    - total_property_value: Total property value for calculating Loan-to-Value Ratio. If None, LTV is not calculated.

    Returns:
    - pandas DataFrame with the combined mortgage schedule.
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

    # For 'remaining_term_months', we will take the maximum remaining term among loans
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