def calculate_balances(type,tenure,interest_amount,principal_amount,penalty_rate,payment_dates,usd_payments,zwl_payments,interest_rate,due_dates,grace_period,in_duplum_rule):
    intrest_added       = [0]
    penalty_added       = [0]
    principal_added     = [0]
    intrest_balance     = [0]
    penalty_balance     = [0]
    principal_balance_1 = [0]
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

    for t in range(len(due_dates)-1):
        date = (datify(due_dates[t]))
        if t%2 != 0:
            if t<tenure*2:
                new_interest_amount = interest_amount
                new_principal_amount = 0
                if t>grace_period*2:
                    new_principal_amount = principal_amount
            else:
                new_interest_amount = interest_rate*principal_balance_1[-1]
                new_principal_amount = 0
            if in_duplum_rule:
                if in_duplum:
                    new_interest_amount = 0
                elif penalty_balance[-1]+intrest_balance[-1]+new_interest_amount >= principal_balance_2[-1]:
                    in_duplum = True
                    new_interest_amount = principal_balance_2[-1]-penalty_balance[-1]-intrest_balance[-1]
            
            total_interest +=new_interest_amount
            new_interest_balance = intrest_balance[-1]+new_interest_amount
            new_principal_balance = principal_balance_1[-1]+new_principal_amount
            
            intrest_added.append(new_interest_amount)
            intrest_balance.append(max(new_interest_balance,0))
            principal_added.append(0)
            principal_balance_1.append(principal_balance_1[-1])
            
            principal_added.append(new_principal_amount)
            principal_balance_1.append((new_principal_balance))
            intrest_added.append(0)
            intrest_balance.append(intrest_balance[-1])
            
            for i in range(2):
                penalty_added.append(0)
                penalty_balance.append(penalty_balance[-1])
                principal_balance_2.append(principal_balance_2[-1])
                loan_payment.append(0)
                loan_payment_zwl.append(0)
                dates.append(date)
                exc_rate.append(0)
                payment_to_penalty.append(0)
                payment_to_interest.append(0)
                payment_to_principal.append(0)
                excess_payments.append(0)
        else:
            new_penalty = 0
            if t>grace_period*2:
                new_penalty = (principal_balance_1[-1]+intrest_balance[-1]+penalty_balance[-1])*penalty_rate
            if in_duplum_rule:
                if in_duplum:
                    new_penalty = 0
                elif penalty_balance[-1]+intrest_balance[-1]+new_penalty >= principal_balance_2[-1]:
                    in_duplum = True
                    new_penalty = principal_balance_2[-1]-penalty_balance[-1]-intrest_balance[-1]
            total_penalty += new_penalty
            new_penalty_balance =  penalty_balance[-1]+new_penalty
            penalty_added.append(new_penalty)
            penalty_balance.append(max(new_penalty_balance,0))
            
            intrest_added.append(0)
            intrest_balance.append(intrest_balance[-1])
            principal_added.append(0)
            principal_balance_1.append(principal_balance_1[-1])
            principal_balance_2.append(principal_balance_2[-1])
            loan_payment.append(0)
            loan_payment_zwl.append(0)
            dates.append(date)
            exc_rate.append(0)
            payment_to_penalty.append(0)
            payment_to_interest.append(0)
            payment_to_principal.append(0)
            excess_payments.append(0)
        
        inbetween_dates,inbetween_usd_payments,inbetween_zwl_payments,exchange_rates = get_payments(payment_dates,usd_payments,zwl_payments,due_dates[t],due_dates[t+1])
        if len(inbetween_usd_payments)>0:
            inbetween_usd_payments[0] = inbetween_usd_payments[0]+extra_payment
        else:
            inbetween_dates.append(due_dates[t])
            inbetween_usd_payments.append(extra_payment)
            inbetween_zwl_payments.append(0)
            exchange_rates.append(0)
        
        for i in range(len(inbetween_dates)):
            total_payment = inbetween_usd_payments[i]
            penalty_payment, interest_payment, principal_payment,extra_payment = split_payment(total_payment,intrest_balance[-1],penalty_balance[-1],principal_balance_1[-1])
            
            
            if penalty_payment + interest_payment + principal_payment==0 and t != 0 and inbetween_zwl_payments[i]==0:
                pass
            else:
                payment_to_penalty.append(penalty_payment)
                payment_to_interest.append(interest_payment)
                payment_to_principal.append(principal_payment)
                excess_payments.append(extra_payment)
                loan_payment.append(inbetween_usd_payments[i])
                loan_payment_zwl.append(inbetween_zwl_payments[i])
                exc_rate.append(exchange_rates[i])
                principal_balance_1.append(principal_balance_1[-1]-principal_payment)
                principal_balance_2.append(principal_balance_2[-1]-principal_payment)
                intrest_balance.append(intrest_balance[-1]-interest_payment)
                penalty_balance.append(penalty_balance[-1]-penalty_payment)
                penalty_added.append(0)
                intrest_added.append(0)
                principal_added.append(0)
                dates.append(datify(inbetween_dates[i]))

        if principal_balance_2[-1]<=0.05:
            break
    if type==1:
        return (dates,penalty_added,intrest_added,principal_added,penalty_balance,intrest_balance,principal_balance_1,principal_balance_2,loan_payment,
            loan_payment_zwl,exc_rate,payment_to_penalty,payment_to_interest,payment_to_principal,excess_payments)
    else:
        total_interest_added = total_penalty + total_interest
        return [penalty_balance[-1],intrest_balance[-1],max(0,principal_balance_1[-1]),max(0,principal_balance_2[-1]),penalty_balance[-1]+intrest_balance[-1]+max(0,principal_balance_2[-1])]
