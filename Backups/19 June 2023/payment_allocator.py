from calendar import month
from locale import normalize
from advanced_outbr_calculator import (dates_in_month,get_dates_due,datify,load_file,save_data,get_sl_payments,get_payment_dates,
                                       get_payments,calculate_balances,normalise_dates)
from redirect import get_last_month_date
import datetime
import pandas as pd

def load_information(data,index):
    loan_id              = (data.iloc[[index],1]).values[0]
    name                 = (data.iloc[[index],2]).values[0]
    paid_up              = (data.iloc[[index],3]).values[0]
    principal_amount     = (data.iloc[[index],4]).values[0]
    interest_amount      = (data.iloc[[index],5]).values[0]
    adminstration_amount = (data.iloc[[index],6]).values[0]
    insurance_amount     = (data.iloc[[index],7]).values[0]
    disbursement_date    = int((data.iloc[[index],8]).values[0])-2
    tenure               = (data.iloc[[index],9]).values[0]
    product              = (data.iloc[[index],10]).values[0]
    value                = (data.iloc[[index],11]).values[0]
    re_value             = (data.iloc[[index],12]).values[0]
    td_balance           = (data.iloc[[index],13]).values[0]
    deposit              = (data.iloc[[index],14]).values[0]
    interest_rate        = (data.iloc[[index],15]).values[0]
    penalty_rate         = (data.iloc[[index],16]).values[0]
    payments             = list(data.iloc[[index],17:].values[0])
    payment_dates        = list(data.columns[17:])
    return (loan_id,name,paid_up,principal_amount,interest_amount,adminstration_amount,insurance_amount,disbursement_date,tenure,product,value,
            re_value,td_balance,deposit,interest_rate,penalty_rate,payments,payment_dates)

def allocate_repayment(payment,principal_balance,interest_balance,adminstration_balance,insurance_balance):
    if payment == 0:
        return (0,0,0,0)
    cash = payment
    if cash<adminstration_balance:
        return(cash,0,0,0)
    if cash-adminstration_balance<insurance_balance:
        return(adminstration_balance,cash-adminstration_balance,0,0)
    if cash-adminstration_balance-insurance_balance<interest_balance:
        return (adminstration_balance,insurance_balance,(cash-adminstration_balance-insurance_balance),0)
    return (adminstration_balance,insurance_balance,interest_balance,cash-adminstration_balance-insurance_balance-interest_balance)

def months_between(start,end):
    months = 0
    current = start
    while current<=end:
        months+=1
        current += dates_in_month(current)
    return months-1

def split_income(product,monthly_payment,penalty_balance ,interest_balance,principal_balance,disbursement_date,adminstration_amount,insurance_amount,deposit,final_date,interest_amount,principal_amount,loan_balance):
    admin_paid     = 0
    insurance_paid = 0
    penalty_paid   = 0
    interest_paid  = 0
    principal_paid = 0
    deposit_paid   = 0
    
    if datify(disbursement_date).month == datify(final_date+5).month and datify(disbursement_date).year==datify(final_date+5).year:
        deposit_paid   = deposit
        if product=="MicroVendor":
            insurance_paid = insurance_amount
            admin_paid     = adminstration_amount
    
    cash                = max(0,monthly_payment-deposit_paid)
    
    total_charges = insurance_amount+adminstration_amount+penalty_balance+interest_balance+principal_balance+principal_amount+interest_amount
    if total_charges > 0:
        insurance_paid  = min(insurance_amount,cash)
        cash            = max(0,cash-insurance_paid)
        admin_paid      = min(adminstration_amount,cash)
        cash            = max(0,cash-admin_paid)
        penalty_paid    = min(penalty_balance,cash)
        cash            = max(0,cash-penalty_paid)
        interest_paid   = min(interest_balance,cash)
        cash            = max(0,cash-interest_paid)
        principal_paid  = min(principal_balance,cash)
        cash            = max(0,cash-principal_paid)
        
        while cash>0:
            interest_charged  = min(interest_amount,cash)
            interest_paid    += interest_charged
            cash              = max(0,cash-interest_charged)
            principal_charged = min(principal_amount,cash)
            principal_paid   += principal_charged
            cash              = max(0,cash-principal_charged)
    else:
        principal_paid = min(loan_balance,cash)
        interest_paid = cash - principal_paid

    total_amount_paid = insurance_paid+admin_paid+deposit_paid+principal_paid+interest_paid+penalty_paid
    return [deposit_paid,principal_paid,insurance_paid,admin_paid,interest_paid,penalty_paid,total_amount_paid]

def strip_payment_dates(final_date,disbursement_date,payments,payment_dates):
    new_dates             = get_payment_dates(disbursement_date,payment_dates)
    final = 0
    for i in range(len(new_dates)):
        if new_dates[i]<final_date:
            final+=1
        else:
            break
    new_payment_dates     = new_dates[new_dates.index(disbursement_date):final+1]
    new_payments          = payments[new_dates.index(disbursement_date):final+1]
    return new_payment_dates, new_payments

def onify(due_dates):
    f = []
    for date in due_dates:
        d = datify(date)
        new_date = (datetime.date(d.year,d.month,1)-datetime.date(1900,1,1)).days
        f.append(new_date)
    return f

def get_month_payments(payment_dates,payments,first_date,final_date):
    # get payments made in that month
    final_payments = []
    dates = []
    for date,payment in zip(payment_dates,payments):
        if int(date)>=first_date and int(date)<final_date:
            final_payments.append(payment)
            dates.append(date)
    return (dates,final_payments)

def outstanding_costs(admin,insurance,total_paid):
    # determine if nsy=urance or admin have been paid yet: retrns the outstanding balances
    cash            = total_paid
    insurance_paid  = min(insurance,cash)
    cash            = cash-insurance_paid
    admin_paid      = min(admin,cash)
    return (admin - admin_paid, insurance - insurance_paid) 

def arranged_payments(data, last_run_date, path):
    entries = []
    date = datify(last_run_date)
    first_date = last_run_date
    last_date = get_last_month_date(date.month, date.year)
    solar_payment_df    = load_file(path+'Outside loans\\Solar Lights\\Balances\\payments.csv')
    for row in range(len(data.index)):
    # for i in range(1):
    #     row = 12
        loan_id,name,paid_up,principal_amount,interest_amount,adminstration_amount,insurance_amount,disbursement_date,tenure,product,value,re_value,td_balance,deposit,interest_rate,penalty_rate,payments,payment_dates = load_information(data,row)
        # Put final date as 0 so that it never puts an instalment before its due
        if disbursement_date>last_date:
            continue
        if product == "Solar Lights":
            sl_payments   = get_sl_payments(solar_payment_df,loan_id)
            payment_dates = sl_payments[1]
            payments      = sl_payments[0]
        payment_dates = [int(payment_date) for payment_date in payment_dates]
        monthly_payments = get_month_payments(payment_dates,payments,first_date,last_date)
        first_details = [datify(disbursement_date),name,product,value,re_value,(interest_amount+principal_amount)*tenure]
        if len(monthly_payments[0])==0:
            monthly_payments[0].append(disbursement_date)
            monthly_payments[1].append(0)
        for m_date,m_payment in zip(monthly_payments[0],monthly_payments[1]):
            due_dates = get_dates_due(disbursement_date,last_run_date,tenure, False,True)
            payments = [float(payment) for payment in payments]
            (penalty_balance ,interest_balance,principal_balance,loan_balance,outstanding_balance) = calculate_balances(2,tenure,interest_amount,principal_amount,penalty_rate,
                                                                                        payment_dates,payments,payments,interest_rate,due_dates,
                                                                                        0,True)
            payments_to = sum([j for i,j in zip(payment_dates,payments) if i<last_run_date])
            adminstration_amount,insurance_amount = outstanding_costs(adminstration_amount,insurance_amount, payments_to)
            split_repayment = split_income(product,m_payment,penalty_balance,interest_balance,principal_balance,disbursement_date,adminstration_amount,insurance_amount,deposit,last_run_date,interest_amount,principal_amount,loan_balance)
            
            interest_paid = split_repayment[2]
            principal_paid = split_repayment[1]
            
            outstanding_balance = max(0,outstanding_balance-principal_paid-interest_paid)
            if paid_up == 1:
                outstanding_balance = 0
            if split_repayment[-1]==0:
                continue
            entries.append(first_details+split_repayment+[outstanding_balance])
    return entries

def get_final_date(month,year):
    return ((datetime.date(year,month+1,1)-datetime.timedelta(1))-(datetime.date(1900,1,1))).days+1

def allocate_payment(currency, month,year,start_path):
    if currency=="USD":
        file_path = start_path + "Outside loans\\Income\\Payments\\all_payments.csv"
        save_path = start_path + "Outside loans\\Income\\Payments\\arranged_payment.csv"
    elif currency=="ZWL":
        file_path = start_path + "Outside loans\\Income\\Payments\\all_payments_rtgs.csv"
        save_path = start_path + "Outside loans\\Income\\Payments\\arranged_payment_rtgs.csv"
    data          = load_file(file_path)

    final_date    = ((datetime.date(year,month,1)-datetime.timedelta(1))-(datetime.date(1900,1,1))).days+1
    
    d             = arranged_payments(data, final_date, start_path)
    final_df      = pd.DataFrame(d,columns =['DATE', 'CLIENT NAME', 'PRODUCT','INITIAL COST PRICE', 'REVALUED PRICE','EXPECTED PAYMENT','DEPOSIT',
                                'LOAN CAPITAL','INSURANCE', 'ADMINISTRATION','INTEREST','PENALTY INTEREST', "TOTAL PAID","BALANCE TD"])
    return (save_data(final_df,save_path,"PAYMENTS"))
