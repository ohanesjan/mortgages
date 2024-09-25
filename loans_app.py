import sys
import os

# Get the absolute path to the 'src' directory
src_path = os.path.join(os.path.dirname(__file__), 'src')

# Add 'src' to the Python path if it's not already there
if src_path not in sys.path:
    sys.path.append(src_path)


import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.loan_amortization import annuity_mortgage_schedule, linear_mortgage_schedule, combine_mortgage_schedules



# -----------------------------
# Helper Functions
# -----------------------------

def initialize_session_state():
    if 'options' not in st.session_state:
        st.session_state['options'] = []
    if 'option_counter' not in st.session_state:
        st.session_state['option_counter'] = 0

def add_option():
    st.session_state['option_counter'] += 1
    new_option = {
        'id': st.session_state['option_counter'],
        'mortgages': []
    }
    st.session_state['options'].append(new_option)

def remove_option():
    if st.session_state['options']:
        st.session_state['options'].pop()

def add_mortgage(option_id):
    for option in st.session_state['options']:
        if option['id'] == option_id:
            option['mortgages'].append(len(option['mortgages']) + 1)
            break

def remove_mortgage(option_id):
    for option in st.session_state['options']:
        if option['id'] == option_id:
            if option['mortgages']:
                option['mortgages'].pop()
            break

def get_option_label(option):
    return f"Option {option['id']}"

def get_mortgage_label(option_id, mortgage_id):
    return f"Mortgage {mortgage_id} in Option {option_id}"

# -----------------------------
# Initialize Session State
# -----------------------------
initialize_session_state()

# -----------------------------
# App Title and Description
# -----------------------------
st.set_page_config(
    page_title="Mortgage Schedule Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Mortgage Schedule Analyzer")



st.markdown("""
This application allows you to define multiple mortgage options, each containing multiple mortgages/loans. You can input the parameters for each mortgage, combine them within their respective options, and visualize the comparative performance through interactive Plotly plots.

### **Features:**
- **Dynamic Options:** Add or remove mortgage options.
- **Dynamic Mortgages:** Within each option, add or remove multiple mortgages.
- **Selective Plotting:** Choose which options to include in the visualizations.
- **Interactive Plots:** Enhanced visualizations using Plotly.
""")

# -----------------------------
# Sidebar: Total Property Value
# -----------------------------
st.sidebar.header("🔍 Total Property Value")
total_property_value = st.sidebar.number_input(
    "Enter the total property value (€):",
    min_value=0.0,
    value=300000.0,
    step=1000.0,
    format="%.2f"
)

st.sidebar.markdown("---")

# -----------------------------
# Option Management
# -----------------------------
st.header("🔄 Manage Mortgage Options")

# Buttons to add/remove options
col_add, col_remove = st.columns(2)
with col_add:
    if st.button("➕ Add Option"):
        add_option()

with col_remove:
    if st.button("➖ Remove Option"):
        remove_option()

# Display each option with its mortgages
for option in st.session_state['options']:
    with st.expander(get_option_label(option)):
        # Buttons to add/remove mortgages within the option
        col_mortgage_add, col_mortgage_remove = st.columns(2)
        with col_mortgage_add:
            if st.button(f"➕ Add Mortgage to {get_option_label(option)}", key=f"add_mortgage_{option['id']}"):
                add_mortgage(option['id'])
        with col_mortgage_remove:
            if st.button(f"➖ Remove Mortgage from {get_option_label(option)}", key=f"remove_mortgage_{option['id']}"):
                remove_mortgage(option['id'])

        # Display each mortgage within the option
        for mortgage_id in option['mortgages']:
            st.subheader(get_mortgage_label(option['id'], mortgage_id))



            col1, col2 = st.columns(2)

            with col1:
                mortgage_type = st.selectbox(
                    f"Type for {get_mortgage_label(option['id'], mortgage_id)}:",
                    options=["Annuity", "Linear"],
                    key=f"type_{option['id']}_{mortgage_id}"
                )

            with col2:
                rate_percentage = st.number_input(
                    f"Annual Interest Rate (%) for {get_mortgage_label(option['id'], mortgage_id)}:",
                    min_value=0.0,
                    max_value=100.0,
                    value=5.0,
                    step=0.1,
                    format="%.2f",
                    key=f"rate_percentage_{option['id']}_{mortgage_id}"
                )

            col3, col4 = st.columns(2)

            with col3:
                loan_value = st.number_input(
                    f"Loan Amount (€) for {get_mortgage_label(option['id'], mortgage_id)}:",
                    min_value=0.0,
                    value=100000.0,
                    step=1000.0,
                    format="%.2f",
                    key=f"loan_{option['id']}_{mortgage_id}"
                )

            with col4:
                maturity_months = st.number_input(
                    f"Maturity (Months) for {get_mortgage_label(option['id'], mortgage_id)}:",
                    min_value=1,
                    max_value=600,
                    value=360,
                    step=12,
                    key=f"maturity_{option['id']}_{mortgage_id}"
                )

            col5, col6 = st.columns(2)
            with col5:
                adjust_option = st.radio(
                    f"Adjustment Option for {get_mortgage_label(option['id'], mortgage_id)}:",
                    # options=["Payment (default)", "Maturity"],
                    options=["payment", "maturity"],
                    index=0,
                    help="In case of a bulk payment:\n"\
                    "- Payment : reduces the monthly payment\n"\
                    "- Maturity : reduces the period over which the loan is repaid""",
                    key=f"adjust_{option['id']}_{mortgage_id}"
                )

            with col6:
                start_month = st.number_input(
                    f"Start Month for {get_mortgage_label(option['id'], mortgage_id)}:",
                    min_value=1,
                    max_value=1000,
                    value=1,
                    step=1,
                    key=f"start_{option['id']}_{mortgage_id}"
                )
            

            st.markdown("**Bulk Repayments:**")
            bulk_repayments_input = st.text_area(
                f"Bulk Repayments for {get_mortgage_label(option['id'], mortgage_id)} (format: month:amount, separated by commas):",
                value="",
                help="Example: 12:5000,36:10000",
                key=f"bulk_{option['id']}_{mortgage_id}"
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

            st.markdown("---")

# -----------------------------
# Plot Generation
# -----------------------------
st.header("📈 Generate and Visualize Plots")

if st.button("Generate Plots"):
    if not st.session_state['options']:
        st.error("Please add at least one mortgage option with at least one mortgage.")
    else:
        # Collect all combined schedules per option
        combined_schedules = {}
        option_labels = []
        colors = [
            '#1f77b4',  # Blue
            '#ff7f0e',  # Orange
            '#2ca02c',  # Green
            '#d62728',  # Red
            '#9467bd',  # Purple
            '#8c564b',  # Brown
            '#e377c2',  # Pink
            '#7f7f7f',  # Gray
            '#bcbd22',  # Olive
            '#17becf'   # Cyan
        ]

        for option in st.session_state['options']:
            option_id = option['id']
            option_label = get_option_label(option)
            mortgages = option['mortgages']
            mortgage_details = []
            for mortgage_id in mortgages:
                # Fetch inputs for each mortgage
                m_type = st.session_state.get(f"type_{option_id}_{mortgage_id}", "Annuity").lower()
                m_rate_percentage = st.session_state.get(f"rate_percentage_{option_id}_{mortgage_id}", 5.0)
                m_rate = m_rate_percentage/100 # Convert to decimal
                m_loan = st.session_state.get(f"loan_{option_id}_{mortgage_id}", 100000.0)
                m_maturity = st.session_state.get(f"maturity_{option_id}_{mortgage_id}", 360)
                m_adjust = st.session_state.get(f"adjust_{option_id}_{mortgage_id}", 'payment')
                m_start = st.session_state.get(f"start_{option_id}_{mortgage_id}", 1)
                # Parse bulk repayments from input
                bulk_key = f"bulk_{option_id}_{mortgage_id}"
                bulk_input = st.session_state.get(bulk_key, "")
                bulk_repayments = []
                if bulk_input.strip():
                    try:
                        entries = bulk_input.split(',')
                        for entry in entries:
                            month, amount = entry.strip().split(':')
                            bulk_repayments.append( (int(month.strip()), float(amount.strip())) )
                    except:
                        st.error(f"Invalid bulk repayment format for {get_mortgage_label(option_id, mortgage_id)}.")

                # Generate schedule for this mortgage
                if m_type == 'annuity':
                    schedule = annuity_mortgage_schedule(
                        rate=m_rate,
                        loan_value=m_loan,
                        maturity_months=m_maturity,
                        bulk_repayments=bulk_repayments,
                        adjust=m_adjust,
                        property_value=total_property_value
                    )
                elif m_type == 'linear':
                    schedule = linear_mortgage_schedule(
                        rate=m_rate,
                        loan_value=m_loan,
                        maturity_months=m_maturity,
                        bulk_repayments=bulk_repayments,
                        adjust=m_adjust,
                        property_value=total_property_value
                    )
                mortgage_details.append( (schedule, m_start) )

            # Combine all mortgages within the option into one schedule
            combined_schedule = combine_mortgage_schedules(mortgage_details, total_property_value=total_property_value)
            combined_schedules[option_label] = combined_schedule
            option_labels.append(option_label)

        # Allow user to select which options to plot
        selected_options = st.multiselect(
            "Select Mortgage Options to Include in the Plots:",
            options=option_labels,
            default=option_labels
        )

        if not selected_options:
            st.error("Please select at least one mortgage option to plot.")
        else:
            # Prepare data for plotting
            plot_schedules = {label: combined_schedules[label] for label in selected_options}
            colors_plot = colors[:len(plot_schedules)]  # Assign colors

            # Identify the schedule with the lowest cumulative interest paid at the end
            total_cumulative_interests = {}
            for label, schedule in plot_schedules.items():
                total_cumulative_interests[label] = schedule['cumulatively_paid_interest'].iloc[-1]

            min_label = min(total_cumulative_interests, key=total_cumulative_interests.get)

            # Create a DataFrame to align cumulative interests over time
            # Find the maximum month across all selected schedules
            max_month_plot = max([schedule['month'].max() for schedule in plot_schedules.values()])

            # Initialize a DataFrame with months as the index
            cumulative_interest_df_plot = pd.DataFrame({'month': range(1, max_month_plot + 1)})
            cumulative_interest_df_plot.set_index('month', inplace=True)

            # Add cumulative interest data for each schedule
            for label, schedule in plot_schedules.items():
                # Reindex the cumulative interest to align months
                temp = schedule.set_index('month')['cumulatively_paid_interest']
                temp = temp.reindex(range(1, max_month_plot + 1), method='ffill')  # Forward fill after loan is paid off
                cumulative_interest_df_plot[label] = temp

            # Add the cumulative interest of the minimum interest schedule
            min_cumulative_interest_plot = cumulative_interest_df_plot[min_label]

            # Compute the difference between each schedule and the minimum interest schedule
            for label in plot_schedules.keys():
                cumulative_interest_df_plot[label] = cumulative_interest_df_plot[label] - min_cumulative_interest_plot

            # # -----------------------
            # # Debug
            # # -----------------------
            # st.write(f"Rate for {get_mortgage_label(option_id, mortgage_id)}: {m_rate}")
            # st.write("Combined Schedule for Selected Options:")
            # # st.dataframe(combined_schedule)
            # st.dataframe(schedule)
            

            # -----------------------
            # Plotting with Plotly
            # -----------------------

            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    "📊 Monthly Payments Over Time",
                    "💰 Remaining Loan Balance Over Time",
                    "📈 Cumulative Interest Paid Over Time",
                    "🔍 Difference in Cumulative Interest Paid Compared to Minimum"
                ),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )

            # Plot 1: Monthly Payments Over Time with breakdown
            for idx, (label, schedule) in enumerate(plot_schedules.items()):

                color = colors_plot[idx % len(colors_plot)]
    
                # Convert hex color to RGB tuple
                hex_color = color.lstrip('#')
                rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                
                # Create fill colors with different transparency levels
                fillcolor1 = f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.4)'  # Transparency 0.8
                fillcolor2 = f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.1)'  # Transparency 0.5
                
                # Plot monthly_principal_repayment line with fill to zero
                fig.add_trace(
                    go.Scatter(
                        x=schedule['month'],
                        y=schedule['monthly_principal_repayment'],
                        mode='lines',
                        name=f"Principal ({label})",
                        line=dict(color=color, width=2, dash='dash'),
                        fill='tozeroy',
                        fillcolor=fillcolor1
                    ),
                    row=1, col=1
                )
                
                # Plot monthly_repayment line with fill to next y
                fig.add_trace(
                    go.Scatter(
                        x=schedule['month'],
                        y=schedule['monthly_repayment'],
                        mode='lines',
                        name=f"Total Payment ({label})",
                        line=dict(color=color, width=4),
                        fill='tonexty',
                        fillcolor=fillcolor2
                    ),
                    row=1, col=1
                )

                # color = colors_plot[idx % len(colors_plot)]
                # fig.add_trace(
                #     go.Scatter(
                #         x=schedule['month'],
                #         y=schedule['monthly_principal_repayment'],
                #         mode='lines',
                #         name=f"Principal ({label})",
                #         line=dict(color=color, width=2, dash='dash')
                #     ),
                #     row=1, col=1
                # )
                # fig.add_trace(
                #     go.Scatter(
                #         x=schedule['month'],
                #         y=schedule['monthly_interest_repayment'],
                #         mode='lines',
                #         name=f"Interest ({label})",
                #         line=dict(color=color, width=2, dash='dash')
                #     ),
                #     row=1, col=1
                # )
                # fig.add_trace(
                #     go.Scatter(
                #         x=schedule['month'],
                #         y=schedule['monthly_repayment'],
                #         mode='lines',
                #         name=f"Total Payment ({label})",
                #         line=dict(color=color, width=4)
                #     ),
                #     row=1, col=1
                # )

            # Plot 2: Remaining Loan Balance Over Time
            for idx, (label, schedule) in enumerate(plot_schedules.items()):
                color = colors_plot[idx % len(colors_plot)]
                fig.add_trace(
                    go.Scatter(
                        x=schedule['month'],
                        y=schedule['remaining_loan_value'],
                        mode='lines',
                        name=label,
                        line=dict(color=color, width=2)
                    ),
                    row=1, col=2
                )

            # Plot 3: Cumulative Interest Paid Over Time
            for idx, (label, schedule) in enumerate(plot_schedules.items()):
                color = colors_plot[idx % len(colors_plot)]
                fig.add_trace(
                    go.Scatter(
                        x=schedule['month'],
                        y=schedule['cumulatively_paid_interest'],
                        mode='lines',
                        name=label,
                        line=dict(color=color, width=2)
                    ),
                    row=2, col=1
                )

            # Plot 4: Difference in Cumulative Interest Paid Compared to Minimum Interest Schedule
            for idx, (label, schedule) in enumerate(plot_schedules.items()):
                if label != min_label:
                    color = colors_plot[idx % len(colors_plot)]
                    fig.add_trace(
                        go.Scatter(
                            x=cumulative_interest_df_plot.index,
                            y=cumulative_interest_df_plot[label],
                            mode='lines',
                            name=label,
                            line=dict(color=color, width=2)
                        ),
                        row=2, col=2
                    )

            # Update layout
            fig.update_layout(
                height=900,
                showlegend=True,
                title_text="🏦 Mortgage Schedule Comparative Analysis",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    # y=1.02,
                    y=-0.2,
                    xanchor="right",
                    x=1
                )
            )

            # Update axes titles
            fig.update_xaxes(title_text="Month", row=1, col=1)
            fig.update_yaxes(title_text="€", row=1, col=1)

            fig.update_xaxes(title_text="Month", row=1, col=2)
            fig.update_yaxes(title_text="€", row=1, col=2)

            fig.update_xaxes(title_text="Month", row=2, col=1)
            fig.update_yaxes(title_text="€", row=2, col=1)

            fig.update_xaxes(title_text="Month", row=2, col=2)
            fig.update_yaxes(title_text="Difference (€)", row=2, col=2)

            # Display the Plotly figure
            st.plotly_chart(fig, use_container_width=True)

            # Optionally, provide a download button for the combined schedules
            # Create a combined DataFrame for all selected options
            combined_all_options = pd.DataFrame()
            for label, schedule in plot_schedules.items():
                temp = schedule.copy()
                temp['Option'] = label
                combined_all_options = pd.concat([combined_all_options, temp], ignore_index=True)

            csv = combined_all_options.to_csv(index=False)
            st.download_button(
                label="📥 Download Combined Schedule as CSV",
                data=csv,
                file_name='combined_schedule.csv',
                mime='text/csv',
                key='download-csv'
            )