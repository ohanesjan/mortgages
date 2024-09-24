#%%
%load_ext autoreload
%autoreload 2

import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# pd.reset_option('display.max_rows')
# pd.reset_option('display.max_columns')


from matplotlib import pyplot as plt


from src.loan_amortization import annuity_mortgage_schedule, linear_mortgage_schedule, combine_mortgage_options_list
#%%

########## Option 1 - 100% LTV ##########

# Define mortgage parameters
rate = 0.038  # 5% annual interest rate
loan_value = 350000  # Loan amount
property_value = 350000  # Property value - for it can be different than the loan
maturity_months = 360  # maturity of the mortgage in months
# bulk_repayments = [(12, 30000), (24, 10000)]  # Bulk repayments in months 12 and 24
adjustment_type = 'payment'

# Generate options_list for both adjustment options
# Option 1: Adjust Maturity
schedule_o1 = annuity_mortgage_schedule(
    rate,
    loan_value,
    maturity_months,
    # bulk_repayments,
    adjust=adjustment_type,
    property_value=property_value
)

########## Option 2 - 100k downpayment ##########

# Define mortgage parameters
rate = 0.038  # 5% annual interest rate
loan_value = 250000  # Loan amount
property_value = 350000  # Property value - for it can be different than the loan
maturity_months = 360  # maturity of the mortgage in months
# bulk_repayments = [(12, 30000), (24, 10000)]  # Bulk repayments in months 12 and 24
adjustment_type = 'payment'

# Generate options_list for both adjustment options
# Option 1: Adjust Maturity
schedule_o2 = annuity_mortgage_schedule(
    rate,
    loan_value,
    maturity_months,
    # bulk_repayments,
    adjust=adjustment_type,
    property_value=property_value
)


########## Option 3 - 100k + 30k loan downpayment ##########

# Define mortgage parameters
rate = 0.038  # 5% annual interest rate
loan_value = 220000  # Loan amount
property_value = 350000  # Property value - for it can be different than the loan
maturity_months = 360  # maturity of the mortgage in months
# bulk_repayments = [(12, 30000), (24, 10000)]  # Bulk repayments in months 12 and 24
adjustment_type = 'payment'

# Generate options_list for both adjustment options
# Option 1: Adjust Maturity
schedule_o3_l1 = annuity_mortgage_schedule(
    rate,
    loan_value,
    maturity_months,
    # bulk_repayments,
    adjust=adjustment_type,
    property_value=property_value
)


# Define mortgage parameters
rate = 0.058  
loan_value = 30000  # Loan amount
property_value = 1  # Property value - for it can be different than the loan
maturity_months = 24  # maturity of the mortgage in months
# bulk_repayments = [(12, 30000), (24, 10000)]  # Bulk repayments in months 12 and 24
adjustment_type = 'payment'

# Generate options_list for both adjustment options
# Option 1: Adjust Maturity
schedule_o3_l2 = annuity_mortgage_schedule(
    rate,
    loan_value,
    maturity_months,
    # bulk_repayments,
    adjust=adjustment_type,
    property_value=property_value
)

loans_o3 = [
    (schedule_o3_l1,1),
    (schedule_o3_l2,1)
]

schedule_o3_combined = combine_mortgage_options_list(loans_o3, total_property_value= 350000)
########## Option 4 - 100k - bulk payment downpayment ##########

# Define mortgage parameters
rate = 0.038  # 5% annual interest rate
loan_value = 250000  # Loan amount
property_value = 350000  # Property value - for it can be different than the loan
maturity_months = 360  # maturity of the mortgage in months
bulk_repayments = [(12, 15000), (24, 15000)]  # Bulk repayments in months 12 and 24
adjustment_type = 'payment'

# Generate options_list for both adjustment options
# Option 1: Adjust Maturity
schedule_o4 = annuity_mortgage_schedule(
    rate,
    loan_value,
    maturity_months,
    bulk_repayments,
    adjust=adjustment_type,
    property_value=property_value
)


################# Options list #################
options_list = [schedule_o1,schedule_o2,schedule_o3_combined,schedule_o4]
labels = [
    '350k mor',
    '250k mor',
    '220k mor + 30k loan',
    '250k mor 24m 30k repayment',
]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']  # Blue, Orange, Green, Red

# %%


# Create a four-panel plot
fig, axs = plt.subplots(2, 2, figsize=(16, 12))

# Define x-axis ticks (every 12 months up to the maximum month)
max_month = max([schedule['month'].max() for schedule in options_list])
x_ticks = list(range(0, int(max_month) + 12, 12))

# Plot 1: Monthly Payments Over Time with breakdown
for schedule, label, color in zip(options_list, labels, colors):
    # Fill between for principal and interest
    axs[0, 0].fill_between(
        schedule['month'],
        0,
        schedule['monthly_principal_repayment'],
        facecolor=color,
        alpha=0.6,
        label=f'Principal ({label})'
    )
    axs[0, 0].fill_between(
        schedule['month'],
        schedule['monthly_principal_repayment'],
        schedule['monthly_repayment'],
        facecolor=color,
        alpha=0.3,
        label=f'Interest ({label})'
    )
    # Plot lines on top
    axs[0, 0].plot(
        schedule['month'],
        schedule['monthly_repayment'],
        color=color,
        linewidth=1.5,
        label=f'Total Payment ({label})'
    )

# Set title and labels for Plot 1
axs[0, 0].set_title('Monthly Payments Over Time')
axs[0, 0].set_xlabel('Year')
axs[0, 0].set_ylabel('Monthly Payment (€)')
axs[0, 0].grid(True)
axs[0, 0].set_xticks(x_ticks)
axs[0, 0].set_xticklabels([str(int(x/12)) for x in x_ticks])

# Adjust legend to avoid duplicates
handles, labels_plot = axs[0, 0].get_legend_handles_labels()
by_label = dict(zip(labels_plot, handles))
axs[0, 0].legend(by_label.values(), by_label.keys(), loc='upper right', fontsize='small')

# Plot 2: Remaining Loan Balance Over Time
for schedule, label, color in zip(options_list, labels, colors):
    axs[0, 1].plot(
        schedule['month'],
        schedule['remaining_loan_value'],
        label=label,
        color=color
    )

# Set title and labels for Plot 2
axs[0, 1].set_title('Remaining Loan Balance Over Time')
axs[0, 1].set_xlabel('Year')
axs[0, 1].set_ylabel('Remaining Loan Balance (€)')
axs[0, 1].legend(fontsize='small')
axs[0, 1].grid(True)
axs[0, 1].set_xticks(x_ticks)
axs[0, 1].set_xticklabels([str(int(x/12)) for x in x_ticks])

# Plot 3: Cumulative Interest Paid Over Time
for schedule, label, color in zip(options_list, labels, colors):
    axs[1, 0].plot(
        schedule['month'],
        schedule['cumulatively_paid_interest'],
        label=label,
        color=color
    )

# Set title and labels for Plot 3
axs[1, 0].set_title('Cumulative Interest Paid Over Time')
axs[1, 0].set_xlabel('Year')
axs[1, 0].set_ylabel('Cumulative Interest Paid (€)')
axs[1, 0].legend(fontsize='small')
axs[1, 0].grid(True)
axs[1, 0].set_xticks(x_ticks)
axs[1, 0].set_xticklabels([str(int(x/12)) for x in x_ticks])

# Plot 4: Cumulative Interest Saved Over Time
for schedule, label, color in zip(options_list, labels, colors):
    axs[1, 1].plot(
        schedule['month'],
        schedule['cumulative_interest_saved'],
        label=label,
        color=color
    )

# Set title and labels for Plot 4
axs[1, 1].set_title('Cumulative Interest Saved Over Time')
axs[1, 1].set_xlabel('Year')
axs[1, 1].set_ylabel('Cumulative Interest Saved (€)')
axs[1, 1].legend(fontsize='small')
axs[1, 1].grid(True)
axs[1, 1].set_xticks(x_ticks)
axs[1, 1].set_xticklabels([str(int(x/12)) for x in x_ticks])

plt.tight_layout()
plt.show()

# %%
