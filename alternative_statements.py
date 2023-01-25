from advanced_outbr_calculator import datify,get_payments

rates,rates_dates = [1],[0]

def calculate_alternative_statement(type,tenure,interest_amount,principal_amount,penalty_rate,payment_dates,usd_payments,zwl_payments,interest_rate,due_dates,grace_period,in_duplum_rule,rates,rates_dates):
    intrest_added       = [0]
    penalty_added       = [0]
    principal_added     = [0]
    intrest_balance     = 0
    penalty_balance     = [0]
    principal_balance   = 0
    principal_balance_2 = [principal_amount*(tenure-grace_period)]
    loan_payment        = [0]
    loan_payment_zwl    = [0]
    dates               = [datify(due_dates[0])]
    extra_payment       = 0
    exc_rate            = [0]
    payment_to_penalty  = [0]
    payment_to_interest = [0]
    payment_to_principal= [0]
    excess_payments     = [0]
    total_interest      = 0
    total_penalty       = 0
    in_duplum           = False
    
    
    for t in range(len(due_dates)-2):
        date = (datify(due_dates[t]))
        if t%2 != 0:
            monthly_balance = 0
            if t<tenure*2:
                new_interest_amount  = interest_amount
                new_principal_amount = principal_amount
            
            inbetween_dates,inbetween_usd_payments,inbetween_zwl_payments,exchange_rates = get_payments(payment_dates,usd_payments,zwl_payments,due_dates[t],due_dates[t+2])
            
            try:
                period_rate = exchange_rates[0]
            except:
                period_rate=rates[-1]
            
            
            # USD SIDE
            intrest_added.append(new_interest_amount)
            principal_added.append(new_principal_amount)
            
            monthly_balance += new_interest_amount+new_principal_amount
            
            principal_balance+=new_principal_amount
            intrest_balance+=new_interest_amount
            
            intrest_added.append(0)
            intrest_balance.append(intrest_balance[-1])