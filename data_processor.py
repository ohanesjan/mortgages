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
                  fixed_interest: float, var_base_interest: float, var_interest) -> pd.DataFrame:
    '''Returns DataFrame with all instalments analysis.
    var_interest can be either a number, fixed rate, or string, like 'euribor6m'.
    '''

    # ----- Data Frame creation -----
  
    #There is a strange behaviour of some functions if index starts from 1 instead of 0!  
    instalment_order=np.arange(0,loan_period,dtype=int)
    index_list=instalment_order
    loan_pd=pd.DataFrame(index=index_list)
    #The number of payment
    loan_pd["payment_number"] = np.arange(1,loan_period+1, dtype=int)

    # ----- Payment dates -----
    last_date = first_date.astype('datetime64[M]') + np.timedelta64(loan_period,'M')
    payment_dates=np.arange(first_date,last_date,dtype='datetime64[M]')
    #loan_pd=pd.DataFrame(index=payment_dates)
    loan_pd.insert(0, 'payment_dates', pd.Series(payment_dates, index=index_list))

    # ----- Interest rates -----
        #Number of payments per year, hard coded. ! introduce it as a variable  
    n_yearly_payments=12
    var_period=loan_period-fixed_period

    if fixed_interest >= 1: fixed_interest *= 1 / 100
    if var_base_interest >= 1: var_base_interest *= 1 / 100

    fixed_interest_list=np.concatenate((np.full(fixed_period,fixed_interest),np.full(var_period,0)))
    var_base_interest_list=np.concatenate((np.full(fixed_period,0),np.full(var_period,var_base_interest)))
    #TODO Fix next section so it can follow a particular index;
    #Next line works only if var_interest is a float rate;
    var_interest_list=np.concatenate((np.full(fixed_period,0),np.full(var_period,var_interest)))

    loan_pd['fixed_interest']=fixed_interest_list
    loan_pd['var_base_interest']=var_base_interest_list
    loan_pd['var_interest']=var_interest_list
    loan_pd['floating_interest']=var_base_interest_list+var_interest_list
    loan_pd['interest']=fixed_interest_list+var_base_interest_list+var_interest_list


    # ----- Linear repayment -----
        # -- principal payments --
    #TODO This can be modified to incorporate different repayment strategies (linear, annuity...)
    principal_payment_lin = np.full(loan_period, amount / loan_period)
    outstanding_principal_lin= np.flip(np.cumsum(principal_payment_lin))
    
    loan_pd['principal_payment_linear']=principal_payment_lin
    loan_pd['outstanding_principal_linear']=outstanding_principal_lin
    loan_pd['interest_payment_linear']=loan_pd['outstanding_principal_linear']*loan_pd['interest']/n_yearly_payments
    loan_pd['payment_linear']=loan_pd['principal_payment_linear']+loan_pd['interest_payment_linear']
    #loan_pd.insert(0, 'principal_payment', pd.Series(principal_payments, index=index_list))




        # -- annuity -- !! Works just for fully fixed period and with consant fixed interest

    
    #Annual Interest rate distributed over the number of annual payments
    fixed_interest_monthly=fixed_interest/n_yearly_payments
    annuity_factor =((1+fixed_interest_monthly)**loan_period-1)/(((1+fixed_interest_monthly)**loan_period)*fixed_interest_monthly) 
    monthly_instalment_ann=amount/annuity_factor
    

    payment_ann=np.full(fixed_period,monthly_instalment_ann)
    # outstanding_principal_ann=np.full(loan_period,0.)
    # interest_payment_ann=np.full(loan_period,0.)
    # principal_payment_ann=np.full(loan_period,0.)
    
    outstanding_principal_ann=np.empty(loan_period)
    interest_payment_ann=np.empty(loan_period)
    principal_payment_ann=np.empty(loan_period)

    outstanding_principal_ann[0]=amount
    interest_payment_ann[0]=outstanding_principal_ann[0]*fixed_interest/n_yearly_payments
    principal_payment_ann[0]=monthly_instalment_ann-interest_payment_ann[0]

    for n in np.arange(1,loan_period,1):
        outstanding_principal_ann[n]=outstanding_principal_ann[n-1]-principal_payment_ann[n-1]
        interest_payment_ann[n]=outstanding_principal_ann[n]*fixed_interest/n_yearly_payments
        principal_payment_ann[n]=monthly_instalment_ann-interest_payment_ann[n]


    loan_pd['principal_payment_annuity']=principal_payment_ann
    loan_pd['outstanding_principal_annuity']=outstanding_principal_ann
    loan_pd['interest_payment_annuity']=interest_payment_ann
    loan_pd['payment_annuity']=payment_ann



#Group comment from here onwards


    # #Continue with the annuity. Maybe defien a repayment class that can take the repayment plan as an option. 	

    # # ----- interest analysis -----
    # # Outstanding principal per month;
    # outstanding_principal= np.flip(np.cumsum(principal_payments))
    # loan_pd.insert(1,'outstanding_principal',pd.Series( outstanding_principal, index=index_list))

    # #TODO Instead of creating shorter Series, generate a list with the same length as loan_period and set to 0
    # #  for the instalments with var/fixed interest 
    # loan_pd.insert(2,'fixed_interest',pd.Series(fixed_interest,index=index_list[0:fixed_period]))
    # loan_pd.insert(3, 'var_base_interest', pd.Series(var_base_interest, index=index_list[fixed_period:]))

    # if type(var_interest) == str:
    #     parameters = {
    #         'startPeriod': payment_dates[fixed_period], #TODO Fix this, breaks when fixed_period == loan_period
    #         'endPeriod': payment_dates[-1]
    #     } # parameters contains the dates for the euribor rate, passed to the function on the next line
    #     loan_pd.insert(4, 'var_interest', df_time_ecb(var_interest, parameters, tindex=1))

    #     #df_time_ecb returns interest in %, so we divide with 100
    #     loan_pd.var_interest *= 1/100
    # elif type(var_interest) == int:
    #     loan_pd.insert(4, 'var_interest', pd.Series(var_interest/100, index=index_list[fixed_period:]))

    # elif type(var_interest) == float:
    #     loan_pd.insert(4, 'var_interest', pd.Series(var_interest, index=index_list[fixed_period:]))


    # loan_pd = loan_pd.fillna(0)
    # #Compute interest payments. Those are annual interest rates, so the payment is divided by 12
    # loan_pd['fixed_payment']=loan_pd['outstanding_principal']*loan_pd['fixed_interest'] /12
    # loan_pd['base_payment'] = loan_pd['outstanding_principal'] * loan_pd['var_base_interest'] /12
    # loan_pd['var_payment'] = loan_pd['outstanding_principal'] * loan_pd['var_interest'] /12

    # loan_pd.insert(1, 'interest_payment',loan_pd['fixed_payment']+ loan_pd['base_payment'] + loan_pd['var_payment'])
    # loan_pd.insert(2,'payment',loan_pd['principal_payment']+loan_pd['interest_payment'])

    return loan_pd


