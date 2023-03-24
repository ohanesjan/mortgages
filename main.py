import matplotlib.pyplot as plt
#import pandas as pd
import numpy as np
from data_processor import *


df_loan_fixed=loan_analysis(amount=400000, first_date=np.datetime64('2020-02-01'), loan_period =360 ,fixed_period=30*12,
                  fixed_interest=2.38, var_base_interest=0, var_interest=0)

df_loan_var3m=loan_analysis(amount=400000, first_date=np.datetime64('2020-02-01'), loan_period =360 ,fixed_period=0*12,
                  fixed_interest=0, var_base_interest=0, var_interest='euribor3m')


df_loan_fixed4d5=loan_analysis(amount=400000, first_date=np.datetime64('2020-02-01'), loan_period =360 ,fixed_period=30*12,
                  fixed_interest=4.5, var_base_interest=0, var_interest=0)

plt.plot(df_loan_fixed['payment'][np.datetime64('2020-02-01'):np.datetime64('2023-02-01')],label='2.38%')
plt.plot(df_loan_var3m['payment'][np.datetime64('2020-02-01'):np.datetime64('2023-02-01')],label='3m euribor')
plt.plot(df_loan_fixed4d5['payment'][np.datetime64('2020-02-01'):np.datetime64('2023-02-01')],label='4.5%')
plt.ylabel('monthly installment (\N{euro sign})')
plt.xlabel('month')
plt.legend()
plt.show()


total_fixed=df_loan_fixed['payment'][np.datetime64('2020-02-01'):np.datetime64('2023-02-01')].sum()
total_3m=df_loan_var3m['payment'][np.datetime64('2020-02-01'):np.datetime64('2023-02-01')].sum()

print(f'Payed so far with fixed interest rate: \N{euro sign}{total_fixed} ')
print(f'Payed so far if interest rate was 3months EURIBOR: \N{euro sign} {total_3m}')
print(f'Difference to date between 3m EURIBOR and fixed interest: \N{euro sign} {total_3m-total_fixed}')


