#%%
%load_ext autoreload
%autoreload 2

import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# pd.reset_option('display.max_rows')
# pd.reset_option('display.max_columns')


from src.loan_amortization import annuity_mortgage_schedule, linear_mortgage_schedule, combine_mortgage_schedules


#%%
# Define parameters
rate = 0.05  # 5% annual interest rate
loan_value = 80000   # Loan amount of 80,000
property_value = 100000  # Property value of 100,000
maturity_months = 360  # 30-year mortgage
bulk_repayments = [(12, 5000), (24, 10000)]  # Bulk repayments in months 12 and 24

# Generate the amortization schedule with property value provided
schedule_df = annuity_mortgage_schedule(
    rate, loan_value, maturity_months, bulk_repayments, adjust='payment', property_value=property_value
)


# Display the first few rows
display(schedule_df)


#%%
test_dict = dict([(12,500),(24,1000)])

print(test_dict.get(1,1))

#%%
###### Linear

# Define parameters
rate = 0.05  # 5% annual interest rate
loan_value = 100000  # Loan amount of 100,000
property_value = 120000  # Property value of 120,000
maturity_months = 360  # 30-year mortgage
bulk_repayments = [(12, 5000), (24, 10000)]  # Bulk repayments in months 12 and 24

# Option 1: Adjust Maturity (default)
schedule_df_maturity = linear_mortgage_schedule(
    rate, loan_value, maturity_months, bulk_repayments, adjust='maturity', property_value=property_value
)

# Option 2: Adjust Monthly Payment
schedule_df_payment = linear_mortgage_schedule(
    rate, loan_value, maturity_months, bulk_repayments, adjust='payment', property_value=property_value
)

# Display the first few rows for both options
print("Adjust Maturity:")
print(schedule_df_maturity.head(15))

print("\nAdjust Monthly Payment:")
print(schedule_df_payment.head(15))

import matplotlib.pyplot as plt

# Plot Remaining Loan Balance Over Time
plt.figure(figsize=(10, 6))
plt.plot(schedule_df_maturity['Month'], schedule_df_maturity['Remaining Loan Value'], label='Adjust Maturity')
plt.plot(schedule_df_payment['Month'], schedule_df_payment['Remaining Loan Value'], label='Adjust Payment')
plt.xlabel('Month')
plt.ylabel('Remaining Loan Value')
plt.title('Remaining Loan Balance Over Time')
plt.legend()
plt.grid(True)
plt.show()

#%%
# Define mortgage parameters
rate = 0.04  # 5% annual interest rate
loan_value = 350000  # Loan amount of $100,000
property_value = 350000  # Property value of $120,000
maturity_months = 360  # 30-year mortgage
bulk_repayments = [(12, 30000), (24, 10000)]  # Bulk repayments in months 12 and 24

# Generate schedules for both adjustment options
# Option 1: Adjust Maturity
schedule_maturity = annuity_mortgage_schedule(
    rate, loan_value, maturity_months, bulk_repayments, adjust='maturity', property_value=property_value
)

# Option 2: Adjust Monthly Payment
schedule_payment = annuity_mortgage_schedule(
    rate, loan_value, maturity_months, bulk_repayments, adjust='payment', property_value=property_value
)



# Clear previous plot
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Define x-axis ticks (every 12 months up to the maximum month)
max_month = max(schedule_maturity['month'].max(), schedule_payment['month'].max())
x_ticks = list(range(0, int(max_month) + 12, 12))

# First plot: Monthly Payments Over Time with breakdown
# Clear previous plot
axs[0, 0].clear()

# Define colors
color_maturity = '#1f77b4'  # Blue
color_payment = '#ff7f0e'   # Orange

# Adjust Maturity Option
axs[0, 0].fill_between(
    schedule_maturity['month'],
    0,
    schedule_maturity['monthly_principal_repayment'],
    facecolor=color_maturity,
    alpha=0.9,  # Increased opacity for principal
    label='Principal (Adjust Maturity)'
)
axs[0, 0].fill_between(
    schedule_maturity['month'],
    schedule_maturity['monthly_principal_repayment'],
    schedule_maturity['monthly_repayment'],
    facecolor=color_maturity,
    alpha=0.6,
    label='Interest (Adjust Maturity)'
)
# Add lines on top
axs[0, 0].plot(
    schedule_maturity['month'],
    schedule_maturity['monthly_repayment'],
    color=color_maturity,
    linewidth=1.5,
    label='Total Payment (Adjust Maturity)'
)
axs[0, 0].plot(
    schedule_maturity['month'],
    schedule_maturity['monthly_principal_repayment'],
    color=color_maturity,
    linewidth=1.5
)

# Adjust Payment Option
axs[0, 0].fill_between(
    schedule_payment['month'],
    0,
    schedule_payment['monthly_principal_repayment'],
    facecolor=color_payment,
    alpha=0.9,  # Increased opacity for principal
    label='Principal (Adjust Payment)'
)
axs[0, 0].fill_between(
    schedule_payment['month'],
    schedule_payment['monthly_principal_repayment'],
    schedule_payment['monthly_repayment'],
    facecolor=color_payment,
    alpha=0.6,
    label='Interest (Adjust Payment)'
)
# Add lines on top
axs[0, 0].plot(
    schedule_payment['month'],
    schedule_payment['monthly_repayment'],
    color=color_payment,
    linewidth=1.5,
    label='Total Payment (Adjust Payment)'
)
axs[0, 0].plot(
    schedule_payment['month'],
    schedule_payment['monthly_principal_repayment'],
    color=color_payment,
    linewidth=1.5
)

# Set title and labels
axs[0, 0].set_title('Monthly Payments Over Time')
axs[0, 0].set_xlabel('Year')
axs[0, 0].set_ylabel('Monthly Payment (€)')
axs[0, 0].grid(True)
axs[0, 0].set_xticks(x_ticks)
axs[0, 0].set_xticklabels([str(int(x/12)) for x in x_ticks])

# Adjust the legend to avoid duplicate labels
handles, labels = axs[0, 0].get_legend_handles_labels()
by_label = dict(zip(labels, handles))
axs[0, 0].legend(by_label.values(), by_label.keys())

# Remaining plots (updated with new column names)
# Plot 2: Remaining Loan Balance Over Time
axs[0, 1].plot(schedule_maturity['month'], schedule_maturity['remaining_loan_value'], label='Adjust Maturity', color=color_maturity)
axs[0, 1].plot(schedule_payment['month'], schedule_payment['remaining_loan_value'], label='Adjust Payment', color=color_payment)
axs[0, 1].set_title('Remaining Loan Balance Over Time')
axs[0, 1].set_xlabel('Year')
axs[0, 1].set_ylabel('Remaining Loan Balance (€)')
axs[0, 1].legend()
axs[0, 1].grid(True)
axs[0, 1].set_xticks(x_ticks)
axs[0, 1].set_xticklabels([str(int(x/12)) for x in x_ticks])

# Plot 3: Cumulative Interest Paid Over Time
axs[1, 0].plot(schedule_maturity['month'], schedule_maturity['cumulatively_paid_interest'], label='Adjust Maturity', color=color_maturity)
axs[1, 0].plot(schedule_payment['month'], schedule_payment['cumulatively_paid_interest'], label='Adjust Payment', color=color_payment)
axs[1, 0].set_title('Cumulative Interest Paid Over Time')
axs[1, 0].set_xlabel('Year')
axs[1, 0].set_ylabel('Cumulative Interest Paid (€)')
axs[1, 0].legend()
axs[1, 0].grid(True)
axs[1, 0].set_xticks(x_ticks)
axs[1, 0].set_xticklabels([str(int(x/12)) for x in x_ticks])

# Plot 4: Cumulative Interest Saved Over Time
axs[1, 1].plot(schedule_maturity['month'], schedule_maturity['cumulative_interest_saved'], label='Adjust Maturity', color=color_maturity)
axs[1, 1].plot(schedule_payment['month'], schedule_payment['cumulative_interest_saved'], label='Adjust Payment', color=color_payment)
axs[1, 1].set_title('Cumulative Interest Saved Over Time')
axs[1, 1].set_xlabel('Year')
axs[1, 1].set_ylabel('Cumulative Interest Saved (€)')
axs[1, 1].legend()
axs[1, 1].grid(True)
axs[1, 1].set_xticks(x_ticks)
axs[1, 1].set_xticklabels([str(int(x/12)) for x in x_ticks])

plt.tight_layout()
plt.show()


#%%

############## Combining loans ##############



# Mortgage 1: Starts at month 1
schedule1 = annuity_mortgage_schedule(
    rate=0.038,  # 4% annual interest
    loan_value=200000,  # Loan amount of €200,000
    maturity_months=360,  # 30-year mortgage
    bulk_repayments=[(24, 10000)],  # €10,000 bulk repayment in month 24
    adjust='maturity',
    property_value=250000
)

# Mortgage 2: Starts at month 13
schedule2 = annuity_mortgage_schedule(
    rate=0.055,  # 5% annual interest
    loan_value=150000,  # Loan amount of €150,000
    maturity_months=240,  # 20-year mortgage
    bulk_repayments=[(36, 5000)],  # €5,000 bulk repayment in month 36
    adjust='payment',
    property_value=200000
)

# Combine the schedules with different starting months
loans = [
    (schedule1, 1),    # Loan 1 starts at month 1
    (schedule2, 13),   # Loan 2 starts at month 13
]

combined_schedule = combine_mortgage_schedules(loans, total_property_value=450000)

# Display the first 36 months of the combined schedule
display(combined_schedule)

# %%
