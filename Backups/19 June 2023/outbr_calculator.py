from code import interact
from itertools import product
import pandas as pd
import datetime

def load_file(file_path):
    df = pd.read_csv(file_path)
    return df.fillna(0)

def split_payment(payment,interest_balance, penalty_balance, principal_balance):
    if payment == 0:
        return (0,0,0,0)
    cash = payment
    if cash<penalty_balance:
        return(cash,0,0,0)
    if cash-penalty_balance<interest_balance:
        return(penalty_balance,cash-penalty_balance,0,0)
    if cash-penalty_balance-interest_balance<principal_balance:
        return (penalty_balance,interest_balance,(cash-penalty_balance-interest_balance),0)
    return (penalty_balance,interest_balance,principal_balance,(cash-penalty_balance-interest_balance-principal_balance))

def date():
    dates = []
    for year in [2020, 2021, 2022]:
        for month in ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]:
            dates.append("{}-{}".format(month,year))
    return dates

def get_payments(dates,payments,from_date,to_date):
    pass

def calculate_balances(type,tenure,interest_amount,principal_amount,penalty_rate,payments,interest_rate,months,months_lapsed,months_from_2020):
    intrest_added       = [0]
    penalty_added       = [0]
    principal_added     = [0]
    intrest_balance     = [0]
    penalty_balance     = [0]
    principal_balance_1 = [0]
    principal_balance_2 = [principal_amount*tenure]
    loan_payment        = [0]
    months_index        = [months_from_2020]
    for t in range(months-1):
        new_month = months_from_2020+t+1
        print()
        print('month {}'.format(date()[new_month]))
        if t == 0:
            total_payment = payments[t+months_lapsed]
            penalty_payment, interest_payment, principal_payment,extra_payment = split_payment(total_payment,interest_amount,0,principal_amount)
            
            intrest_added.append(max(interest_amount,0))
            intrest_balance.append(max(interest_amount,0))
            penalty_added.append(0)
            penalty_balance.append(0)
            principal_added.append(0)
            principal_balance_1.append(0)
            principal_balance_2.append(principal_balance_2[-1])
            loan_payment.append(0)
            months_index.append(new_month)
            
            principal_added.append(principal_amount)
            principal_balance_1.append(max(principal_amount,0))
            penalty_added.append(0)
            penalty_balance.append(0)
            intrest_added.append(0)
            intrest_balance.append(intrest_balance[-1])
            principal_balance_2.append(principal_balance_2[-1])
            loan_payment.append(0)
            months_index.append(new_month)
            
            principal_balance_2.append(max(principal_amount*tenure,0))
            penalty_added.append(0)
            penalty_balance.append(0)
            intrest_added.append(0)
            intrest_balance.append(intrest_balance[-1])
            principal_added.append(0)
            principal_balance_1.append(principal_balance_1[-1])
            loan_payment.append(0)
            months_index.append(new_month)
            
            principal_balance_2.append(principal_balance_2[-1]-principal_payment)
            penalty_added.append(0)
            penalty_balance.append(0)
            intrest_added.append(0)
            intrest_balance.append(intrest_balance[-1]-interest_payment)
            principal_added.append(0)
            principal_balance_1.append(principal_balance_1[-1]-principal_payment)
            loan_payment.append(total_payment)
            months_index.append(new_month)
            
            # print(payments[t+months_lapsed])
            # print(penalty_balance[-1])
            # print(intrest_balance[-1])
            # print(principal_balance_1[-1])
            # print(principal_balance_2[-1])
        
            continue
        if t < tenure:
            new_penalty = (principal_balance_1[-1]+intrest_balance[-1]+penalty_balance[-1])*penalty_rate
            new_penalty_balance =  penalty_balance[-1]+new_penalty
            new_interest_balance = intrest_balance[-1]+interest_amount
            new_principal_balance = principal_balance_1[-1]+principal_amount
            total_payment = payments[t+months_lapsed]+extra_payment
            penalty_payment, interest_payment, principal_payment,extra_payment = split_payment(total_payment,new_interest_balance,new_penalty_balance,new_principal_balance)
            
            penalty_added.append(new_penalty)
            penalty_balance.append(max(new_penalty_balance,0))
            intrest_added.append(0)
            intrest_balance.append(intrest_balance[-1])
            principal_added.append(0)
            principal_balance_1.append(principal_balance_1[-1])
            principal_balance_2.append(principal_balance_2[-1])
            loan_payment.append(0)
            months_index.append(new_month)
            
            intrest_added.append(interest_amount)
            intrest_balance.append(max(new_interest_balance,0))
            penalty_added.append(0)
            penalty_balance.append(penalty_balance[-1])
            principal_added.append(0)
            principal_balance_1.append(principal_balance_1[-1])
            principal_balance_2.append(principal_balance_2[-1])
            loan_payment.append(0)
            months_index.append(new_month)
            
            principal_added.append(principal_amount)
            principal_balance_1.append((new_principal_balance))
            intrest_added.append(0)
            intrest_balance.append(intrest_balance[-1])
            penalty_added.append(0)
            penalty_balance.append(penalty_balance[-1])
            principal_balance_2.append(principal_balance_2[-1])
            loan_payment.append(0)
            months_index.append(new_month)
            
            principal_balance_2.append(principal_balance_2[-1])
            intrest_added.append(0)
            intrest_balance.append(intrest_balance[-1])
            penalty_added.append(0)
            penalty_balance.append(penalty_balance[-1])
            principal_added.append(0)
            principal_balance_1.append(principal_balance_1[-1])
            loan_payment.append(0)
            months_index.append(new_month)
            
            principal_balance_2.append(principal_balance_2[-1]-principal_payment)
            intrest_added.append(0)
            intrest_balance.append(intrest_balance[-1]-interest_payment)
            penalty_added.append(0)
            penalty_balance.append(penalty_balance[-1]-penalty_payment)
            principal_added.append(0)
            principal_balance_1.append(principal_balance_1[-1]-principal_payment)
            loan_payment.append(total_payment)
            months_index.append(new_month)
            
            
            # print(payments[t+months_lapsed])
            # print(penalty_balance[-1])
            # print(intrest_balance[-1])
            # print(principal_balance_1[-1])
            # print(principal_balance_2[-1])
        
            continue
        
        new_penalty = (principal_balance_1[-1]+intrest_balance[-1]+penalty_balance[-1])*penalty_rate
        new_penalty_balance = penalty_balance[-1]+new_penalty
        new_interest = principal_balance_1[-1]*interest_rate
        new_interest_balance = intrest_balance[-1]+new_interest
        new_principal_balance = principal_balance_1[-1]
        total_payment = payments[t+months_lapsed]+extra_payment
        penalty_payment, interest_payment, principal_payment,extra_payment = split_payment(total_payment,new_interest_balance,new_penalty_balance,new_principal_balance)
        
        if sum(penalty_added)+sum(intrest_added)+new_penalty+new_interest>principal_amount*tenure:
            new_penalty = 0
            new_interest = 0
            new_penalty_balance = penalty_balance[-1]
            new_interest_balance = intrest_balance[-1]
            total_payment = payments[t+months_lapsed]+extra_payment
            penalty_payment, interest_payment, principal_payment,extra_payment = split_payment(total_payment,new_interest_balance,new_penalty_balance,new_principal_balance)

        penalty_added.append(new_penalty)
        penalty_balance.append(max(new_penalty_balance,0))
        intrest_added.append(0)
        intrest_balance.append(intrest_balance[-1])
        principal_added.append(0)
        principal_balance_1.append(principal_balance_1[-1])
        principal_balance_2.append(principal_balance_2[-1])
        loan_payment.append(0)
        months_index.append(new_month)
        
        intrest_added.append(new_interest)
        intrest_balance.append(max(new_interest_balance,0))
        penalty_added.append(0)
        penalty_balance.append(penalty_balance[-1])
        principal_added.append(0)
        principal_balance_1.append(principal_balance_1[-1])
        principal_balance_2.append(principal_balance_2[-1])
        loan_payment.append(0)
        months_index.append(new_month)
        
        principal_added.append(0)
        principal_balance_1.append((new_principal_balance))
        intrest_added.append(0)
        intrest_balance.append(intrest_balance[-1])
        penalty_added.append(0)
        penalty_balance.append(penalty_balance[-1])
        principal_balance_2.append(principal_balance_2[-1])
        loan_payment.append(0)
        months_index.append(new_month)
        
        principal_balance_2.append(principal_balance_2[-1])
        intrest_added.append(0)
        intrest_balance.append(intrest_balance[-1])
        penalty_added.append(0)
        penalty_balance.append(penalty_balance[-1])
        principal_added.append(0)
        principal_balance_1.append(principal_balance_1[-1])
        loan_payment.append(0)
        months_index.append(new_month)
        
        principal_balance_2.append(principal_balance_2[-1]-principal_payment)
        intrest_added.append(0)
        intrest_balance.append(intrest_balance[-1]-interest_payment)
        penalty_added.append(0)
        penalty_balance.append(penalty_balance[-1]-penalty_payment)
        principal_added.append(0)
        principal_balance_1.append(principal_balance_1[-1]-principal_payment)
        loan_payment.append(total_payment)
        months_index.append(new_month)
    
        print(payments[t+months_lapsed])
        print(penalty_balance[-1])
        print(intrest_balance[-1])
        print(principal_balance_1[-1])
        print(principal_balance_2[-1])
        
    if (type == 1):
        return (penalty_added,intrest_added,principal_added,penalty_balance,intrest_balance,principal_balance_1,principal_balance_2,loan_payment,months_index)
    else:
        return [penalty_balance[-1],intrest_balance[-1],max(0,principal_balance_1[-1]),principal_balance_2[-1],penalty_balance[-1]+intrest_balance[-1]+principal_balance_2[-1]]

def get_lapsed_months(date_disbursed):
    # 1 January 2020 is 43831
    i=(int((int(date_disbursed) - 43831)/30.5))
    return int((int(date_disbursed) - 43831)/30.5)

def collect_information(data, row):
    disbursement_date = int(data.iloc[[row],5])
    done = int(data.iloc[[row],2])
    tenure = int(data.iloc[[row],6])
    interest_amount = (data.iloc[[row],4]).values[0]
    principal_amount= (data.iloc[[row],3]).values[0]
    interest_rate = (data.iloc[[row],7]).values[0]
    payments = list(data.iloc[[row],9:].values[0])
    penalty_rate= (data.iloc[[row],8]).values[0]
    months =list(data.columns[9:])
    disbursement_t = 0
    if (disbursement_date)>=int(months[0]):
        for i in range(len(months)):
            if disbursement_date<=int(months[i+1]) and disbursement_date>int(months[i]):
                disbursement_t = i
                months_from_2020 = get_lapsed_months(disbursement_date)
                break
    else:
        months_from_2020 = get_lapsed_months(months[0])
    
    return (tenure,interest_amount,principal_amount,interest_rate,payments,penalty_rate,len(months),disbursement_t,done,months_from_2020)

def get_balances(data):
    all = []
    # inf = collect_information(data, 171)
    # calculate_balances(0,inf[0],inf[1],inf[2],inf[5],inf[4],inf[3],inf[6]-inf[7],inf[7],inf[9])
    for row in range(len(data.index)):
        inf = collect_information(data, row)
        if inf[8]==1:
            l = [(data.iloc[[row],0]).values[0],(data.iloc[[row],1]).values[0]]+[0,0,0,0,0]
        else:
            l = [(data.iloc[[row],0]).values[0],(data.iloc[[row],1]).values[0]]+calculate_balances(0,inf[0],inf[1],inf[2],inf[5],inf[4],inf[3],inf[6]-inf[7],inf[7],inf[9])
        all.append(l)
        new_balances = pd.DataFrame(all,columns =['Account id', 'Account Name', 'Penalty Balance','Interest in Arrears', 'Principal in arrears',
                                'Principal Balance', 'Outstanding Balance @{}'.format(datetime.date.today())])
    return new_balances

def save_data(df, save_path):
    try:
        df.to_csv(save_path)
    except:
        print("File could not be saved because it is open.")
    finally:
        print('Done')
        
def date():
    dates = []
    for year in [2020, 2021, 2022]:
        for month in ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]:
            dates.append("{}-{}".format(month,year))
    return dates



def statement(l):
    all = []
    # penalty_added,intrest_added,principal_added,penalty_balance,intrest_balance,principal_balance_1,principal_balance_2,loan_payment,months_index

    for i in range(len(l[0])):
        description = ""
        dates = []
        all_dates  = date()
        dates.append(all_dates[l[8][i]])
        if i==0:
            description="Loan Disbursement"
        elif (l[0][i])>0:
            description = "Penalty Due"
        elif (l[1][i])>0:
            description = "Interest Due"
        elif (l[2][i])>0:
            description = "Principal Due"
        elif (l[7][i])>0:
            description = "Loan Repayment"
        else:
            continue
        all.append([dates,description,l[0][i]+l[1][i]+l[2][i],l[7][i],l[3][i],l[4][i],l[5][i],l[6][i]])
    new_balances = pd.DataFrame(all,columns =['Date','Description', 'DR', 'CR','Penalty balance', 'Interest Balance',
                                'Principal Balance', 'Loan Balance'])
    return new_balances

def create_statement(data,loan_index):
    inf = collect_information(data, loan_index)
    l= calculate_balances(1,inf[0],inf[1],inf[2],inf[5],inf[4],inf[3],inf[6]-inf[7],inf[7],inf[9])
    
    print("----------------------------------------------")
    # tenure,interest_amount,principal_amount,interest_rate,payments,penalty_rate,len(months),disbursement_t,done
    print("Client Name: {}".format(data.iloc[[loan_index],1].values[0]))
    print("Loan ID: {}".format(data.iloc[[loan_index],0].values[0]))
    print("Loan amount: ${}".format(round(inf[0]*inf[2]*100)/100))
    print("Tenure: {}".format(inf[0]))
    print("Instalment: ${}".format(inf[1]+inf[2]))
    print("Instalment - Principal: ${}".format(round(inf[2]*100)/100))
    print("Instalment - Interest:  ${}".format(round(inf[1]*100)/100))
    print("Interest Rate: {}%".format(inf[3]*100))
    print("Penalty Rate: {}%".format(inf[5]*100))
    print("Total repayments: ${}".format(sum(inf[4])))
    print("----------------------------------------------")
    return statement(l)

def get_files(product):
    start_path = "C:\\Users\\Tinashe.Muwikwa\\Dropbox\\Outside loans\\"
    file_path = ""
    save_path = ""
    path = ""
    if product == 1:
        file_path = "Assets\\Balances\\Assets.csv"
        save_path = "Assets\\Balances\\Assets_balances.csv"
        path = "Assets\\Balances\\"
    elif product==2:
        file_path = "Bakeries\\Balances\\Bakeries_USD.csv"
        save_path = "Bakeries\\Balances\\Bakeries_USD_balances.csv"
        path = "Bakeries\\Balances\\"
    elif product==3:
        file_path = "Bakeries\\Balances\\Bakeries_RTGS.csv"
        save_path = "Bakeries\\Balances\\Bakeries_RTGS_balances.csv"
        path = "Bakeries\\Balances\\"
    elif product==4:
        file_path = "Detergents\\Balances\\Detergents_USD.csv"
        save_path = "Detergents\\Balances\\Detergents_USD_balances.csv"
        path = "Detergents\\Balances\\"
    elif product==5:
        file_path = "Detergents\\Balances\\Detergents_RTGS.csv"
        save_path = "Detergents\\Balances\\Detergents_RTGS_balances.csv"
        path = "Detergents\\Balances\\"
    elif product==6:
        file_path = "MicroVendor\\Balances\\MicroVendor_USD.csv"
        save_path = "MicroVendor\\Balances\\MicroVendor_USD_balances.csv"
        path = "MicroVendor\\Balances\\"
    elif product==7:
        file_path = "MicroVendor\\Balances\\MicroVendor_RTGS.csv"
        save_path = "MicroVendor\\Balances\\MicroVendor_RTGS_balances.csv"
        path = "MicroVendor\\Balances\\"
    return (start_path+file_path,start_path+save_path, start_path+path)

def get_name(data,i):
    return (data.iloc[[i],1]).values[0]

def get_product():
    print('-----------------------------------------')
    print('Product Lists')
    print("1.Assets")
    print("2.Bakeries USD ")
    print("3.Bakeries RTGS")
    print("4.Detergents USD")
    print("5.Detergents RTGS")
    print("6.MicroVendors USD")
    print("7.MicroVendors RTGS")
    print('-----------------------------------------')
    return int(input("Enter The product number: "))

if __name__=="__main__":
    print("-----------------------------------------")
    print("1.Create statement")
    print("2.Calculate Balances")
    print("-----------------------------------------")
    type = int(input("Enter module: "))
    
    if type == 1:
        print("-------------------------------------")
        product = get_product()
        file_path,save_path,path = get_files(product)
        data = load_file(file_path)
        search_name = True
        loan_index = 0
        while search_name:
            print()
            print("-------------------------------------")
            loan_id = (input("Enter Loan Id: "))
            try:
                loan_index = (data.index[data['No,']==loan_id].tolist()[0])
            except:
                print("Loan Not found")
            else:
                search_name = False
        if (data.iloc[[loan_index],2]).values[0] == 1:
            print("Statement not found")
        else:
            save_data(create_statement(data, loan_index),path+"{}_statement.csv".format(get_name(data,loan_index)))
    elif type==2:
        product = get_product()
        file_path,save_path,path = get_files(product)
        data = load_file(file_path)
        save_data(get_balances(data),save_path)