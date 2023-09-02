
#%%
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import pandas as pd
import numpy as np

from data_processor import *
# %%

# loan_amount=350000
# loan_period = 12*30
# fixed_interest = 4.5

loan_amount=60000
loan_period = 12*15
fixed_period = loan_period
fixed_interest = 3.75
var_base_interest = 0.0
var_interest = 0.0


df_loan_fixed_test=loan_analysis(amount=loan_amount, first_date=np.datetime64('2020-02-01'), loan_period =loan_period ,fixed_period=fixed_period,
                  fixed_interest=fixed_interest, var_base_interest= var_base_interest, var_interest=var_interest)
# df_loan_fixed_test.head()

#%%
# Linear and annuity, monthly insallments
fig, ax = plt.subplots()
x = df_loan_fixed_test['payment_number'].to_numpy()
ax.plot(x, df_loan_fixed_test['payment_linear'],label='Linear',color = 'blue' )
ax.plot(x, df_loan_fixed_test['payment_annuity'],label='Annuity', color = 'orange')

# ax.fill_between(x, df_loan_fixed_test['principal_payment_linear'], color = 'blue', alpha = 0.5, linewidth = 0.0)
# ax.fill_between(x, df_loan_fixed_test['principal_payment_linear'],df_loan_fixed_test['payment_linear'], color = 'blue',alpha=0.2,linewidth = 0.0)

# ax.fill_between(x , df_loan_fixed_test['principal_payment_annuity'], color = 'orange', alpha = 0.5, linewidth = 0.0)
# ax.fill_between(x, df_loan_fixed_test['principal_payment_annuity'], df_loan_fixed_test['payment_annuity'], color = 'orange', alpha = 0.2, linewidth = 0.0)

ax.set_xlim(0, x.max() )
ax.set_ylim(0, (df_loan_fixed_test['payment_linear'].max())*1.1)
ax.legend()
ax.xaxis.set_major_locator(ticker.IndexLocator(base=5*12, offset=-1))
ax.xaxis.set_minor_locator(ticker.IndexLocator(base=12,offset=-1))
ax.set_ylabel('monthly installment (\N{euro sign})') 
ax.set_xlabel('month')
#ax.grid()
fig.show()

#%%
# Linear and annuity, cumulative payment per month 
fig, ax = plt.subplots()
x = df_loan_fixed_test['payment_number'].to_numpy()
ax.plot(x, df_loan_fixed_test['payment_linear'].cumsum() ,label='Linear',color = 'blue' )
ax.plot(x, df_loan_fixed_test['payment_annuity'].cumsum(),label='Annuity', color = 'orange')

# ax.fill_between(x, df_loan_fixed_test['principal_payment_linear'], color = 'blue', alpha = 0.5, linewidth = 0.0)
# ax.fill_between(x, df_loan_fixed_test['principal_payment_linear'],df_loan_fixed_test['payment_linear'], color = 'blue',alpha=0.2,linewidth = 0.0)

# ax.fill_between(x , df_loan_fixed_test['principal_payment_annuity'], color = 'orange', alpha = 0.5, linewidth = 0.0)
# ax.fill_between(x, df_loan_fixed_test['principal_payment_annuity'], df_loan_fixed_test['payment_annuity'], color = 'orange', alpha = 0.2, linewidth = 0.0)

ax.set_xlim(0, x.max() )
ax.set_ylim(0, (df_loan_fixed_test['payment_linear'].cumsum().max())*1.1)
ax.legend()
ax.xaxis.set_major_locator(ticker.IndexLocator(base=5*12, offset=-1))
ax.xaxis.set_minor_locator(ticker.IndexLocator(base=12,offset=-1))
ax.set_ylabel('payed cumulatively (\N{euro sign})') 
ax.set_xlabel('month')
#ax.grid()
fig.show()

#%%
fig, ax = plt.subplots(1,2, sharex=True)
x = df_loan_fixed_test['payment_number'].to_numpy()
# ax[0].plot(x, df_loan_fixed_test['payment_linear'],label='Linear',color = 'blue' )
# ax[1].plot(x, df_loan_fixed_test['payment_annuity'],label='Annuity', color = 'orange')

ax[0].plot(x, df_loan_fixed_test['payment_linear'],color = 'blue' )
ax[1].plot(x, df_loan_fixed_test['payment_annuity'], color = 'orange')

ax[0].fill_between(x, df_loan_fixed_test['principal_payment_linear'], color = 'blue', alpha = 0.5, linewidth = 0.0, label = 'principal')
ax[0].fill_between(x, df_loan_fixed_test['principal_payment_linear'],df_loan_fixed_test['payment_linear'], color = 'blue',alpha=0.2,linewidth = 0.0, label = 'interest')

ax[1].fill_between(x , df_loan_fixed_test['principal_payment_annuity'], color = 'orange', alpha = 0.5, linewidth = 0.0, label = 'principal')
ax[1].fill_between(x, df_loan_fixed_test['principal_payment_annuity'], df_loan_fixed_test['payment_annuity'], color = 'orange', alpha = 0.2, linewidth = 0.0, label = 'interest')

plt.setp(ax,
         xlim = (0, x.max() ),
         ylim = (0, (df_loan_fixed_test['payment_linear'].max())*1.1),
         xlabel = 'month'    
        )

ax[0].legend()
ax[1].legend()
ax[0].set_ylabel('monthly installment (\N{euro sign})') 
ax[0].xaxis.set_major_locator(ticker.IndexLocator(base=5*12, offset=-1))
ax[0].xaxis.set_minor_locator(ticker.IndexLocator(base=12,offset=-1))
#ax.grid()

fig.show()
# %%
#%%
# Cumulative payments, linear and annuity on separate subplots
fig, ax = plt.subplots(1,2, sharex=True)
x = df_loan_fixed_test['payment_number'].to_numpy()
# ax[0].plot(x, df_loan_fixed_test['payment_linear'],label='Linear',color = 'blue' )
# ax[1].plot(x, df_loan_fixed_test['payment_annuity'],label='Annuity', color = 'orange')

ax[0].plot(x, df_loan_fixed_test['payment_linear'].cumsum(),color = 'blue' )
ax[1].plot(x, df_loan_fixed_test['payment_annuity'].cumsum(), color = 'orange')

ax[0].fill_between(x, df_loan_fixed_test['principal_payment_linear'].cumsum(), color = 'blue', alpha = 0.5, linewidth = 0.0, label = 'principal')
ax[0].fill_between(x, df_loan_fixed_test['principal_payment_linear'].cumsum(),df_loan_fixed_test['payment_linear'].cumsum(), color = 'blue',alpha=0.2,linewidth = 0.0, label = 'interest')

ax[1].fill_between(x , df_loan_fixed_test['principal_payment_annuity'].cumsum(), color = 'orange', alpha = 0.5, linewidth = 0.0, label = 'principal')
ax[1].fill_between(x, df_loan_fixed_test['principal_payment_annuity'].cumsum(), df_loan_fixed_test['payment_annuity'].cumsum(), color = 'orange', alpha = 0.2, linewidth = 0.0, label = 'interest')

plt.setp(ax,
         xlim = (0, x.max() ),
         ylim = (0, (df_loan_fixed_test['payment_linear'].cumsum().max())*1.1),
         xlabel = 'month'    
        )

ax[0].legend()
ax[1].legend()
ax[0].set_ylabel('payed cumulatively (\N{euro sign})') 
ax[0].xaxis.set_major_locator(ticker.IndexLocator(base=5*12, offset=-1))
ax[0].xaxis.set_minor_locator(ticker.IndexLocator(base=12,offset=-1))
#ax.grid()

fig.show()
# %%
