import numpy as np
import pandas as pd
import requests
import io
import datetime



def df_time_ecb(data_type: str, parameters: dict, tindex: int):
    '''''Returns DataFrame from ECB data base
    Conntact https://sdw-wsrest.ecb.europa.eu/help/ for more details
    data_type can be either specific defined parameter, see ECBkeys, or a completly new one
    If tindex==1, returnes DataFrame as time series'''

    ECBkeys = {
        'euribor1m': 'FM/M.U2.EUR.RT.MM.EURIBOR1MD_.HSTA',
        'euribor3m': 'FM/M.U2.EUR.RT.MM.EURIBOR3MD_.HSTA',
        'euribor6m': 'FM/M.U2.EUR.RT.MM.EURIBOR6MD_.HSTA',
        'euribor1y': 'FM/M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA'
    }

    # Building blocks for the URL
    entrypoint = 'https://sdw-wsrest.ecb.europa.eu/service/data/'  # Using protocol 'https'

    if data_type in ECBkeys.keys():
        url = entrypoint + ECBkeys[data_type]
    else:
        url= entrypoint +data_type

    # Make the HTTP request again, now requesting for CSV format
    response = requests.get(url, params=parameters, headers={'Accept': 'text/csv'})
    # Response succesful? (Response code 200)
    if response.status_code ==200:
        print("Successfully retrieved data")
    else:
        print("Failed to retrieve data")
    df = pd.read_csv(io.StringIO(response.text))
    ts = df.filter(['TIME_PERIOD', 'OBS_VALUE'], axis=1)
    del df #removes the full data frame
    ts['TIME_PERIOD'] = pd.to_datetime(ts['TIME_PERIOD'])
    # when tindex ==1 then index is set to the time column
    if tindex==1:
        ts = ts.set_index('TIME_PERIOD')

    return ts


def loan_analysis(amount: float, first_date, loan_period: int, fixed_period: int,
                  fixed_interest: float, var_base_interest: float, var_interest):
    '''Returns DataFrame with all instalments analysis.
    var_interest can be either a number, fixed rate, or string, like 'euribor6m'.
    '''

    # ----- Data Frame creation -----
    last_date = first_date.astype('datetime64[M]') + np.timedelta64(loan_period,'M')
    payment_dates=np.arange(first_date,last_date,dtype='datetime64[M]')
    loan_pd=pd.DataFrame(index=payment_dates)

    # ----- principal payments -----
    #TODO This can be modified to incorporate different repayment strategies (linear, annuity...)
    principal_payments = np.full(loan_period, amount / loan_period)
    loan_pd.insert(0, 'principal_payment', pd.Series(principal_payments, index=payment_dates))

    # ----- interest analysis -----
    # Outstanding principal per month;
    outstanding_principal= np.flip(np.cumsum(principal_payments))
    loan_pd.insert(1,'outstanding_principal',pd.Series( outstanding_principal, index=payment_dates))


    if fixed_interest >= 1: fixed_interest *= 1 / 100
    if var_base_interest >= 1: var_base_interest *= 1 / 100


    loan_pd.insert(2,'fixed_interest',pd.Series(fixed_interest,index=payment_dates[0:fixed_period]))
    loan_pd.insert(3, 'var_base_interest', pd.Series(var_base_interest, index=payment_dates[fixed_period:]))

    if type(var_interest) == str:
        parameters = {
            'startPeriod': payment_dates[fixed_period], #TODO Fix this, breaks when fixed_period == loan_period
            'endPeriod': payment_dates[-1]
        } # parameters contains the dates for the euribor rate, passed to the function on the next line
        loan_pd.insert(4, 'var_interest', df_time_ecb(var_interest, parameters, tindex=1))

        #df_time_ecb returns interest in %, so we divide with 100
        loan_pd.var_interest *= 1/100
    elif type(var_interest) == int:
        loan_pd.insert(4, 'var_interest', pd.Series(var_interest/100, index=payment_dates[fixed_period:]))

    elif type(var_interest) == float:
        loan_pd.insert(4, 'var_interest', pd.Series(var_interest, index=payment_dates[fixed_period:]))


    loan_pd = loan_pd.fillna(0)
    #Compute interest payments. Those are annual interest rates, so the payment is divided by 12
    loan_pd['fixed_payment']=loan_pd['outstanding_principal']*loan_pd['fixed_interest'] /12
    loan_pd['base_payment'] = loan_pd['outstanding_principal'] * loan_pd['var_base_interest'] /12
    loan_pd['var_payment'] = loan_pd['outstanding_principal'] * loan_pd['var_interest'] /12

    loan_pd.insert(1, 'interest_payment',loan_pd['fixed_payment']+ loan_pd['base_payment'] + loan_pd['var_payment'])
    loan_pd.insert(2,'payment',loan_pd['principal_payment']+loan_pd['interest_payment'])

    return loan_pd


