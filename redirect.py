from advanced_outbr_calculator import (load_file,get_payment_dates,get_sl_payments, create_statement,get_data_1,get_information,save_xlsx,
                                       load_workbook, dataframe_to_xlsx,add_details,save_data,get_outbr_balances,load_rates,
                                       download_payments_from_file,normalise_dates,get_data_2,get_dates_due,calculate_balances, datify,reset_rates)
import datetime
import pandas as pd
import os

def get_name(data,i):
    return (data.iloc[[i],2]).values[0]

def to_out_br_statement(final_date, file_path,save_path,path,frequency,product_id,start_path,product_prefix):
    data     = load_file(file_path)
    loan_id  = product_id
    try:
        loan_index = (data.index[data['No,']==loan_id].tolist()[0])
    except:
        print('loan not found')
        return ("Loan not found",False,'')
    tenure,interest_amount,principal_amount,interest_rate,all_payment_dates,payments,penalty_rate,paid_off,disbursement_date = get_data_1(data,loan_index)
    payment_dates = get_payment_dates(disbursement_date,all_payment_dates,final_date)
    usd_payments = payments
    # IF SOLAR LIGHT, GET PAYMENTS FROM FILE....LOADING FILE
    if product_prefix=="sl-":
        df = load_file(path+'payments.csv')
        sl_id = data.iloc[[loan_index],1].values[0]
        sl_payments = get_sl_payments(df, sl_id)
        payment_dates = sl_payments[1]
        usd_payments  = sl_payments[0]
    zwl_payments = [0]*len(payments)
    
    statement           = create_statement(tenure,interest_amount,principal_amount,interest_rate,payment_dates,usd_payments,zwl_payments,penalty_rate,disbursement_date,frequency,final_date, 0, True)
    tail                = statement.tail(1)
    outstanding_balance =(tail['Penalty balance']+tail['Interest Balance']+tail['Loan Balance']).values[0]
    info_dict           = get_information(get_name(data,loan_index),tenure,0,interest_amount,principal_amount,interest_rate,final_date,payments,penalty_rate,False,outstanding_balance)
    file_name           = get_name(data,loan_index)
    wb                  = load_workbook(start_path+"Payoffs\\Statements\\sources\\"+'template.xlsx')
    wb                  = dataframe_to_xlsx(statement,wb,"statement",15,0)
    wb                  = dataframe_to_xlsx(simplify_statement(statement),wb,"simplified",14,1)
    wb                  = add_details(info_dict,wb,"statement")
    save_path           = path+"Statements\\"+"{}.xlsx".format(file_name)
    return save_xlsx(wb,save_path,file_name)
    # return save_data(statement,path+'Statements\\'+file_name, file_name)

def to_out_br_balance(final_date,file_path,save_path,path,product_prefix):
    data = load_file(file_path)
    name = save_path.split("\\")[-1]
    return save_data(get_outbr_balances(data, final_date,path, product_prefix),save_path,name)

def get_personal_path(path,folder):
    if not os.path.exists(path+folder):
        os.makedirs(path+folder)
    return path+folder+"\\"

def simplify_statement(statement):
    new_st = statement[['Description', 'DR']].copy()
    repayments = statement[['Description','Penalty Payment', 'Interest Payment','Principal Payment']].copy()
    new_st = new_st[new_st["Description"] != "Principal Due"]
    repayments = repayments[repayments["Description"] != "Principal Due"]
    loan_amount = statement["Loan Balance"][0]
    payments  = repayments.sum(axis = 'columns', numeric_only=True)
    
    new_st["CR"]=(list(payments))
    balance = [loan_amount]
    for dr,cr in zip(new_st["DR"],payments):
        balance.append(balance[-1]+dr-cr)
    balance.pop(0)
    new_st["Balance"]=balance
    return new_st

def get_last_month_date(month, year):
    next_month = month+1
    next_year = year
    if next_month==13:
        next_month=1
        next_year += 1
    return (datetime.date(next_year,next_month,1)-(datetime.date(1900,1,1))).days

def to_inbr_statement_calculator(start_path,main_payments,extra_payments,in_duplum_rule,user_name,statement_type, account_id):
    if statement_type==0:
        reset_rates()
    else:
        load_rates(start_path)
    if account_id:
        try:
            data_path            = (start_path+"Payoffs\\Statements\\sources\\")+"loans_list.csv"
            all_data                 = load_file(data_path)
            acc = "'{}".format(account_id).strip()
            loan_index = (all_data.index[all_data['Loan Account']==acc].tolist()[0])
            data = all_data[loan_index:loan_index+1]
        except:
            print("Loan details not found.")
            return (["Loan details not found."],[False],[""])
    else:
        data_path            = get_personal_path(start_path+"Payoffs\\Statements\\",user_name)+"a_inputs\\input.csv"
        data                 = load_file(data_path)
    final_date           = ((datetime.date.today())-(datetime.date(1900,1,1))).days+1
    main_payments_path   = start_path+"Payoffs\\Statements\\sources\\"
    extra_payments_path  = get_personal_path((start_path+"Payoffs\\Statements\\"),user_name)+"a_inputs\\"
    messages             = []
    errors               = []
    paths                = []
    to_year              = datetime.date.today().year
    frames               = []
    payments_data        = pd.DataFrame()
    extra = pd.DataFrame()
    if main_payments:
        for year in range(2019,to_year+1):
            frames.append(load_file(main_payments_path+"{}.csv".format(year)))
        frames.append(load_file(main_payments_path+"indexed_payments.csv"))
        payments_data = pd.concat(frames)
    if extra_payments:
        extra   = load_file(extra_payments_path+'extra_payments.csv')
    for loan_index in range(len(data.axes[0])):
        account_id,tenure,interest_amount,principal_amount,interest_rate,penalty_rate,disbursement_date,zwl_loan_amount, grace_period = get_data_2(data,loan_index)
        zwl_payments , payment_dates = download_payments_from_file(payments_data,extra,account_id)
        usd_payments = [0]*len(zwl_payments)
        payment_dates = normalise_dates(payment_dates)
        statement = create_statement(tenure,interest_amount,principal_amount,interest_rate,payment_dates,usd_payments,zwl_payments,penalty_rate,disbursement_date,0,final_date, grace_period, in_duplum_rule)
        tail = statement.tail(1)
        outstanding_balance =(tail['Penalty balance']+tail['Interest Balance']+tail['Loan Balance']).values[0]
        info_dict = get_information(data.iloc[[loan_index],1].values[0],tenure,zwl_loan_amount,interest_amount,principal_amount,interest_rate,final_date,zwl_payments,penalty_rate,True,outstanding_balance)
        month     = get_current_month()
        path = get_personal_path(get_personal_path(start_path+"Payoffs\\Statements\\",user_name),month)
        name = (data.iloc[[loan_index],1]).values[0]
        wb   = load_workbook(start_path+"Payoffs\\Statements\\sources\\template.xlsx")
        wb   = dataframe_to_xlsx(statement,wb,'statement',15,0)
        wb   = dataframe_to_xlsx(simplify_statement(statement),wb,"simplified",14,1)
        wb   = add_details(info_dict,wb,"statement")
        save_path = path+"{}.xlsx".format(name)
        report = save_xlsx(wb,save_path,name)
        messages.append(report[0])
        errors.append(report[1])
        paths.append(report[2])
    return (messages,errors,paths)

def unbundle_data(data,index):
    account_id         = (data.iloc[[index],0]).values[0]
    account_name       = (data.iloc[[index],1]).values[0]
    loan_amount        = (data.iloc[[index],2]).values[0]
    out_princ          = (data.iloc[[index],3]).values[0]
    out_interest       = (data.iloc[[index],4]).values[0]
    out_bal            = (data.iloc[[index],5]).values[0]
    instalment         = (data.iloc[[index],6]).values[0]
    arrears            = (data.iloc[[index],7]).values[0]
    due_dates          = (data.iloc[[index],8]).values[0]
    ref                = (data.iloc[[index],9]).values[0]
    tenure             = (data.iloc[[index],10]).values[0]
    intrest_rate       = (data.iloc[[index],11]).values[0]
    penalty_rate       = (data.iloc[[index],12]).values[0]
    disbursement_date  = normalise_dates((data.iloc[[index],13]).values)[0]
    grace_period       = (data.iloc[[index],14]).values[0]
    principal_amount   = loan_amount/(tenure-grace_period)
    if (grace_period>0) or instalment==0:
        interest_amount = (instalment-loan_amount)/tenure
        instalment = loan_amount/(tenure-grace_period)+(loan_amount*intrest_rate)
    else:
        interest_amount = instalment - principal_amount
    return (account_id,account_name,loan_amount,out_princ,out_interest,out_bal,instalment,arrears,due_dates,ref,tenure,intrest_rate,penalty_rate,
            disbursement_date,grace_period,principal_amount,interest_amount)

def get_current_month():
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    today = datetime.date.today()
    return months[today.month-1]+" "+str(today.year)

def format_data(account_id,account_name,penalty_balance,interest_balance,principal_arrears,loan_balance,outstanding_balance,installment,arrears,due_dates,ref,loan_book_format):
    if loan_book_format:
        arrears_amount = max(principal_arrears+interest_balance+penalty_balance,arrears)
        return [account_id,account_name,loan_balance,interest_balance+penalty_balance,outstanding_balance,installment,arrears_amount,due_dates,ref]
    else:
        return [account_id,account_name,penalty_balance,interest_balance,principal_arrears, loan_balance,outstanding_balance]

def get_inbr_balances(source_data,payments_data,final_date, in_duplum , loan_book_format, only_expired):
    all = []
    for row in range(len(source_data.index)):
    # for i in range(1):
    #     row = 253
        (account_id,account_name,loan_amount,out_princ,out_interest,out_bal,instalment,arrears,arrear_due_days,ref,tenure,
        intrest_rate,penalty_rate,disbursement_date,grace_period,principal_amount,interest_amount) = unbundle_data(source_data,row)
        due_dates                  = get_dates_due(disbursement_date,final_date,tenure, False,True)
        payments,payment_dates     = download_payments_from_file(payments_data,pd.DataFrame(),account_id)
        payment_dates              = normalise_dates(payment_dates)
        if disbursement_date>final_date:
            l        = format_data(account_id,account_name,0,0,0,0,0,instalment,0,0,"a",loan_book_format)+[0]
        elif disbursement_date+30.2*(tenure+1)>final_date and only_expired==1:
            l        = format_data(account_id,account_name,0,out_interest,0,out_princ,out_bal,instalment,arrears,arrear_due_days,ref,loan_book_format)+[0]
        else:
            balances = calculate_balances(2,tenure,interest_amount,principal_amount,penalty_rate,payment_dates,payments,payments,intrest_rate,due_dates,grace_period,in_duplum)
            l        = format_data(account_id,account_name,balances[0],balances[1],balances[2],balances[3],balances[4],instalment,0,arrear_due_days,ref,loan_book_format)+[1]
        all.append(l)
    if loan_book_format:
        columns = ['Account id', 'Account Name', 'Outstanding Principal','Interest in Arrears', 'Outstanding Balance',"Installment amount","Arrears Amount","Due days", "ref","Inrerst after maturity"]
    else:
        columns = ['Account id', 'Account Name', 'Penalty Balance','Interest in Arrears', 'Principal in arrears','Loan Balance', 'Outstanding Balance @{}'.format(datify(int(final_date-1)))]
    return pd.DataFrame(all,columns =columns)

def to_inbr_balance_calculator(start_path,final_date,user_name,in_duplum,loan_book_format,currency,only_expired):
    file_path       = start_path+"Payoffs\\Statements\\sources\\loans.csv"
    source_path     = get_personal_path(start_path+"Payoffs\\Statements\\",user_name)+"a_inputs\\loans_list.csv"
    payments_path   = start_path+"Payoffs\\Statements\\sources\\"
    save_path       = (get_personal_path(start_path+"Payoffs\\Statements\\",user_name))+"balances_output.csv"
    payments_data   = pd.DataFrame()
    frames          = []
    to_year         = datetime.date.today().year
    if currency==0:
        reset_rates()
    else:
        load_rates(start_path)
    for year in range(2019,to_year+1):
        frames.append(load_file(payments_path+"{}.csv".format(year)))
    frames.append(load_file(payments_path+"indexed_payments.csv"))
    payments_data   = pd.concat(frames)
    source_data     = load_file(source_path)
    return save_data(get_inbr_balances(source_data,payments_data,final_date, in_duplum, loan_book_format, only_expired),save_path,'Loans Output')
