from functools import partial
from tkinter import *
from turtle import width
from redirect import to_out_br_statement,to_inbr_balance_calculator,to_inbr_statement_calculator,to_out_br_balance
import datetime
from payment_allocator import allocate_payment
import os

root = Tk()
root.geometry("500x350")
root.resizable(False, False)
root.title("Balance Calculator")
bg_color    = '#1a1925'
mid_color   = '#235d52'
mid_color_dark = '#1c4039'
fg_color    = '#f48e36'
root['background']=bg_color

opener                   = Frame(root, bg=bg_color)
outbr_stament_maker      = Frame(root, bg=bg_color)
outbr_balance_calculator = Frame(root, bg=bg_color)
inbr_stament_maker       = Frame(root, bg=bg_color)
inbr_balance_calculator  = Frame(root, bg=bg_color)
results_frame            = Frame(root, bg=bg_color)
to_do_frame              = Frame(root, bg=bg_color)
income_allocator         = Frame(root, bg=bg_color)
date_choice              = IntVar(inbr_stament_maker,1)
statement_type           = IntVar(inbr_stament_maker,0)
data_format              = IntVar(inbr_balance_calculator,1)
product_choice           = StringVar(outbr_stament_maker, "1")
acc_id                   = StringVar()
final_date               = StringVar()
main_payments            = IntVar(inbr_stament_maker,1)
extra_payments           = IntVar()
in_duplum                = IntVar(inbr_stament_maker,1)
only_expired             = IntVar(inbr_stament_maker,1)


start_path               = "C:\\Users\\Tinashe.Muwikwa\\Dropbox\\"
p                        = (os.getcwd().replace('\\','\\')+"\\Dropbox\\").split("\\")
full_name                = p[2].split(".")
user_name                = full_name[0]+" "+full_name[1]
start_path               = p[0]+"\\"+p[1]+"\\"+p[2]+"\\Dropbox\\"

def get_final_date(date):
    dates = date.split("/")
    day   = int(dates[0])
    month = int(dates[1])
    year  = int(dates[2])
    a     = (datetime.date(year,month,day))
    b     = (datetime.date(1900,1,1))
    return (a-b).days

def get_last_day():
    today = datetime.date.today()
    new_date = datetime.date(today.year,today.month,1)-datetime.timedelta(days=1)
    return new_date

def switch_frame(old_frame, new_frame):
    new_frame.pack()
    old_frame.pack_forget()

def get_path(product):
    file_path     = ""
    save_path     = ""
    path          = ""
    frequency     = 0
    id_prefix     = ''

    if product   == 1:
        file_path = "Outside loans\\Assets\\Balances\\Assets.csv"
        save_path = "Outside loans\\Assets\\Balances\\Assets_balances.csv"
        path      = "Outside loans\\Assets\\Balances\\"
        id_prefix = 'as-'

    elif product ==2:
        file_path = "Outside loans\\Bakeries\\Balances\\Bakeries_USD.csv"
        save_path = "Outside loans\\Bakeries\\Balances\\Bakeries_USD_balances.csv"
        path      = "Outside loans\\Bakeries\\Balances\\"
        id_prefix = 'bk-u-'

    elif product ==3:
        file_path = "Outside loans\\Bakeries\\Balances\\Bakeries_RTGS.csv"
        save_path = "Outside loans\\Bakeries\\Balances\\Bakeries_RTGS_balances.csv"
        path      = "Outside loans\\Bakeries\\Balances\\"
        id_prefix = 'bk-'

    elif product ==4:
        file_path = "Outside loans\\Detergents\\Balances\\Detergents_USD.csv"
        save_path = "Outside loans\\Detergents\\Balances\\Detergents_USD_balances.csv"
        path = "Outside loans\\Detergents\\Balances\\"
        id_prefix = 'dt-u-'

    elif product ==5:
        file_path = "Outside loans\\Detergents\\Balances\\Detergents_RTGS.csv"
        save_path = "Outside loans\\Detergents\\Balances\\Detergents_RTGS_balances.csv"
        path      = "Outside loans\\Detergents\\Balances\\"
        id_prefix = 'dt-'

    elif product ==6:
        file_path = "Outside loans\\MicroVendor\\Balances\\MicroVendor_USD.csv"
        save_path = "Outside loans\\MicroVendor\\Balances\\MicroVendor_USD_balances.csv"
        path      = "Outside loans\\MicroVendor\\Balances\\"
        id_prefix = 'mv-u-'

    elif product ==7:
        file_path = "Outside loans\\MicroVendor\\Balances\\MicroVendor_RTGS.csv"
        save_path = "Outside loans\\MicroVendor\\Balances\\MicroVendor_RTGS_balances.csv"
        path      = "Outside loans\\MicroVendor\\Balances\\"
        id_prefix = 'mv-'

    elif product ==8:
        file_path = "Outside loans\\Solar Lights\\Balances\\Solar.csv"
        save_path = "Outside loans\\Solar Lights\\Balances\\Solar_balances.csv"
        path      = "Outside loans\\Solar Lights\\Balances\\"
        id_prefix = 'sl-'

    return (start_path+file_path,start_path+save_path, start_path+path, frequency, id_prefix)

def calculate_outbr_statement():
    messages       = []
    errors         = []
    paths          = []
    if date_choice.get()==1:
        final_date = (get_last_day() - datetime.date(1900,1,1)).days+1
    else:
        final_date = (datetime.date.today() - datetime.date(1900,1,1)).days+1
    file_path,save_path,path,frequency,id_prefix = get_path(int(product_choice.get()))
    product_id = id_prefix+str(acc_id.get())
    report = to_out_br_statement(final_date,file_path,save_path,path,frequency,product_id,start_path,id_prefix)
    messages.append(report[0])
    errors.append(report[1])
    paths.append(report[2])
    result_packer(messages,errors,paths,outbr_stament_maker)
    switch_frame(outbr_stament_maker,results_frame)

def calculate_inbr_balance():
    messages       = []
    errors         = []
    paths          = []
    try:
        this_final_date = get_final_date(final_date.get())+1
    except:
        return
    report = to_inbr_balance_calculator(start_path, this_final_date,user_name,in_duplum,data_format.get(),statement_type.get(),only_expired.get())
    
    messages.append(report[0])
    errors.append(report[1])
    paths.append(report[2])
    result_packer(messages,errors,paths,inbr_balance_calculator)
    switch_frame(inbr_balance_calculator,results_frame)

def calculate_outbr_balance():
    messages            = []
    errors              = []
    paths               = []
    this_final_date     = 0
    try:
        this_final_date = get_final_date(final_date.get())+1
    except:
        return
    if int(product_choice.get())==9:
        for i in range(1,9):
            file_path,save_path,path,frequency,_id_prefix = get_path((i))
            product_id = _id_prefix
            report = to_out_br_balance(this_final_date,file_path,save_path,path,_id_prefix)
            messages.append(report[0])
            errors.append(report[1])
            paths.append(report[2])
    else:
        file_path,save_path,path,frequency,_id_prefix = get_path(int(product_choice.get()))
        product_id = _id_prefix
        report = to_out_br_balance(this_final_date,file_path,save_path,path,product_id)
        messages.append(report[0])
        errors.append(report[1])
        paths.append(report[2])
    result_packer(messages,errors,paths,outbr_balance_calculator)
    switch_frame(outbr_balance_calculator,results_frame) 

def calculate_inbr_statement():
    report   = to_inbr_statement_calculator(start_path,main_payments.get(),extra_payments.get(),in_duplum.get(),user_name,statement_type.get())
    messages = report[0]
    errors   = report[1]
    paths    = report[2]
    result_packer(messages,errors,paths,inbr_stament_maker)
    switch_frame(inbr_stament_maker,results_frame)

def to_income_allocator(month,year):
    messages            = []
    errors              = []
    paths               = []
    report = allocate_payment(month=month, year=int(year), start_path=start_path)
    messages.append(report[0])
    errors.append(report[1])
    paths.append(report[2])
    result_packer(messages,errors,paths,income_allocator)
    switch_frame(income_allocator,results_frame)

def change_and_clear(current_frame, new_frame):
    switch_frame(current_frame,new_frame)
    for widget in current_frame.winfo_children():
        widget.destroy()

def open_file(path):
    os.system('start EXCEL.EXE "{}"'.format(path))

def result_packer(messages,errors,paths,previous_frame):
    Label(results_frame,text = "Results",bg = bg_color, fg = fg_color, font=("Arial", 12)).grid(column = 2, row=0,padx=4,pady=5)
    row = 0
    for i in range(len(messages)):
        if errors[i]:
            color = fg_color
            action_with_arg = partial(open_file, paths[i])
            open_btn = Button(results_frame,text = messages[i],fg = fg_color, bd=0,bg=mid_color,activebackground=mid_color_dark,command= action_with_arg)
            open_btn.grid(column = 1, row=1+i,pady=2,columnspan=3)
        else:
            color = 'red'
            Label(results_frame,text = messages[i], bg=mid_color_dark, fg=color).grid(column = 1, row=1+i,padx=4,pady=0,columnspan=3)
        row = i+3
        
    home = Button(results_frame, text = 'Home',width=10, fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color_dark,command =lambda: change_and_clear(results_frame,opener))
    home.grid(row = row+1, column = 3, padx=4, pady=4)

    back_btn = Button(results_frame, text = 'Back',width=10,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color_dark,command = lambda: change_and_clear(results_frame,previous_frame))
    back_btn.grid(row = row+1, column = 1, padx=4, pady=4)

def opener_packer():
    user_name = Label(opener,text = "Choose module",bg = bg_color, fg = fg_color, font=("Arial", 12))
    user_name.grid(column = 2, row=0,padx=4,pady=5)
    
    btn1 = Button(opener, text = 'OUTBR Statement Maker',width=20,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color_dark, command=lambda: switch_frame(opener,outbr_stament_maker))
    btn1.grid(row = 1, column = 1, padx=4,pady=4)

    btn2 = Button(opener, text = 'OUTBR Balance Calculator',width=20,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color_dark,command =lambda: switch_frame(opener,outbr_balance_calculator))
    btn2.grid(row = 1, column = 3, padx=4,pady=4)

    btn3 = Button(opener, text = 'Loan Statement Maker',width=20,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color_dark,command =lambda: switch_frame(opener,inbr_stament_maker) )
    btn3.grid(row = 2, column = 1, padx=4,pady=4)

    btn4 = Button(opener, text = 'Inbr Balance Calculator',width=20,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color_dark,command =lambda: switch_frame(opener,inbr_balance_calculator))
    btn4.grid(row = 2, column = 3, padx=4,pady=4)
    
    btn5 = Button(opener, text = 'Income Allocator',width=20,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color_dark,command =lambda: switch_frame(opener,income_allocator))
    btn5.grid(row = 3, column = 1, padx=4,pady=4)

    exit_btn = Button(opener, text = 'Exit',width=10,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color_dark,command = root.destroy)
    exit_btn.grid(row = 4, column = 2, padx=4,pady=4)
    
    Label(opener,text = "",bg = bg_color, fg = 'red').grid(row = 5, column = 1, padx=4,pady=4)
    
    features = Button(opener, text = 'Upcoming Features',width=15,fg = fg_color, bd=0, height=1,bg=mid_color,activebackground=mid_color_dark,command =lambda: switch_frame(opener,to_do_frame))
    features.grid(row = 8, column = 2, padx=4,pady=4)
    
    Label(opener,text = "Version 1.1",bg = bg_color, fg = fg_color).grid(row = 9, column = 2, padx=4,pady=4)

def outbr_stament_maker_packer():
    heading = Label(outbr_stament_maker,text = "OUTBR Statement",bg = bg_color, fg = fg_color, font=("Arial", 11))
    heading.grid(column = 1, row=0,pady=5)
    
    values = {"1.Assets" : 1,
        "2.Bakeries USD" : 2,
        "3.Bakeries RTGS" : 3,
        "4.Detergents USD" : 4,
        "5.Detergents RTGS" : 5,
        "6.MicroVendors USD" : 6,
        "7.MicroVendors RTGS" : 7,
        "8.Solar Lights" : 8}
    row = 0
    for (text, value) in values.items():
        column = 0
        row = int((value+1)/2)
        if value%2==0:
            column = 2
        Radiobutton(outbr_stament_maker, text = text, variable = product_choice,value = value, fg = fg_color, bg = bg_color,activebackground=mid_color, font=("Arial", 10)).grid(column=column, row=row, sticky="w")
    
    date = Label(outbr_stament_maker,text = "Statement as at date?", bg = bg_color,fg = fg_color)
    date.grid(column = 1, row=row+1,padx=4,pady=5)
    
    Radiobutton(outbr_stament_maker, text = "As at {}".format(get_last_day()), variable = date_choice,value = 1,fg = fg_color, bg = bg_color,activebackground=mid_color).grid(column=0, row=row+2, sticky="w")
    Radiobutton(outbr_stament_maker, text = "As at today", variable = date_choice,value = 2,fg = fg_color, bg = bg_color,activebackground=mid_color).grid(column=2, row=row+2, sticky="w")
    
    acc = Label(outbr_stament_maker,text = "Account id",bg = bg_color,fg = fg_color)
    acc.grid(column = 1, row=row+3,padx=4,pady=5)
    
    acc_id_label = Label(outbr_stament_maker,text = "Account id number only",bg = bg_color,fg = fg_color)
    acc_id_label.grid(column = 0, row=row+4,padx=4,pady=5)
    
    acc_id_entry = Entry(outbr_stament_maker,textvariable = acc_id, font=('calibre',10,'normal'))
    acc_id_entry.grid(row = row+4, column = 1, padx=4, pady=4)

    calculate = Button(outbr_stament_maker,text = 'Calculate',width=10,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color,command =lambda: calculate_outbr_statement())
    calculate.grid(row = row+5, column = 2, padx=4, pady=4)

    back_btn = Button(outbr_stament_maker, text = 'Back', width=10,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color,command = lambda: switch_frame(outbr_stament_maker,opener))
    back_btn.grid(row = row+5, column = 0, padx=4, pady=4)

def outbr_balance_calculator_packer():
    user_name = Label(outbr_balance_calculator,text = "OUTBR Balance Calculator",bg = bg_color, fg = fg_color, font=("Arial", 11))
    user_name.grid(column = 1, row=0,pady=5)
    
    values    = {
        "1.Assets" : 1,
        "2.Bakeries USD" : 2,
        "3.Bakeries RTGS" : 3,
        "4.Detergents USD" : 4,
        "5.Detergents RTGS" : 5,
        "6.MicroVendors USD" : 6,
        "7.MicroVendors RTGS" : 7,
        "8.Solar Lights" : 8,
        "9.All Products" : 9
        }
    row = 0
    for (text, value) in values.items():
        column = 0
        row = int((value+1)/2)
        if value%2==0:
            column = 2
        Radiobutton(outbr_balance_calculator, text = text, variable = product_choice,value = value, fg = fg_color, bg = bg_color,activebackground=mid_color).grid(column=column, row=row, sticky="w")

    date = Label(outbr_balance_calculator,text = "Balances as at date?",bg = bg_color, fg = fg_color, font=("Arial", 9))
    date.grid(column = 1, row=row+1,padx=4,pady=5)

    acc_id_label = Label(outbr_balance_calculator,text = "DD/MM/YYYY",bg = bg_color, fg = fg_color, font=("Arial", 9))
    acc_id_label.grid(column = 0, row=row+4,padx=4,pady=5)

    date_entry = Entry(outbr_balance_calculator,textvariable = final_date, font=('calibre',10,'normal'))
    date_entry.grid(row = row+4, column = 1, padx=4, pady=4)

    calculate = Button(outbr_balance_calculator, text = 'Calculate',width=10,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color,command =lambda: calculate_outbr_balance())
    calculate.grid(row = row+5, column = 2, padx=4, pady=4)

    back_btn = Button(outbr_balance_calculator, text = 'Back',width=10,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color,command = lambda: switch_frame(outbr_balance_calculator,opener))
    back_btn.grid(row = row+5, column = 0, padx=4, pady=4)

def inbr_stament_maker_packer():
    
    heading = Label(inbr_stament_maker,text = "INBR Statement Maker",bg = bg_color, fg = fg_color, font=("Arial", 11))
    heading.grid(column = 1, row=0, pady=5)
    
    payments = Label(inbr_stament_maker,text = "Choose Payments source",bg = bg_color, fg = fg_color, font=("Arial", 9))
    payments.grid(column = 1, row=1, pady=5)
    
    Checkbutton(inbr_stament_maker, text="Main Payments", variable=main_payments,bg = bg_color, fg = fg_color,activebackground=mid_color,font=("Arial", 10)).grid(row=2, column = 0)
    Checkbutton(inbr_stament_maker, text="Extra Payments", variable=extra_payments,bg = bg_color, fg = fg_color,activebackground=mid_color,font=("Arial", 10)).grid(row=2, column = 2)
    type = Label(inbr_stament_maker,text = "Statement Type",bg = bg_color, fg = fg_color, font=("Arial", 9))
    type.grid(column = 1, row=3, pady=5)
    Radiobutton(inbr_stament_maker, text = "ZWL Statement", variable = statement_type,value = 0,fg = fg_color, bg = bg_color,activebackground=mid_color).grid(column=0, row=4, sticky="w")
    Radiobutton(inbr_stament_maker, text = "USD Statement", variable = statement_type,value = 1,fg = fg_color, bg = bg_color,activebackground=mid_color).grid(column=2, row=4, sticky="w")
    
    Checkbutton(inbr_stament_maker, text="Apply In Duplum Rule", variable=in_duplum,bg = bg_color, fg = fg_color,activebackground=mid_color).grid(row=5, column = 1)
    
    home_btn = Button(inbr_stament_maker,text = 'Back',width=10,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color,command = lambda: switch_frame(inbr_stament_maker,opener))
    home_btn.grid(row     = 7, column = 0, padx=4, pady=4)
    colculate = Button(inbr_stament_maker,text = 'Calculate',width=10,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color,command = lambda: calculate_inbr_statement())
    colculate.grid(row     = 7, column = 2, padx=4, pady=4)

def inbr_balance_calculator_packer():
    heading = Label(inbr_balance_calculator,text = "INBR Balance Calculator",bg = bg_color, fg = fg_color, font=("Arial", 11))
    heading.grid(column = 1, row=0, pady=5)
    
    format = Label(inbr_balance_calculator,text = "Choose Outout format",bg = bg_color, fg = fg_color, font=("Arial", 9))
    format.grid(column = 1, row=1, pady=5)
    
    Radiobutton(inbr_balance_calculator, text = "Loan Book Format", variable = data_format,value = 1,fg = fg_color, bg = bg_color,activebackground=mid_color).grid(column=0, row=4, sticky="w")
    Radiobutton(inbr_balance_calculator, text = "Detailed Format", variable = data_format,value = 0,fg = fg_color, bg = bg_color,activebackground=mid_color).grid(column=2, row=4, sticky="w")
    
    currency = Label(inbr_balance_calculator,text = "Balance type?",bg = bg_color, fg = fg_color, font=("Arial", 9))
    currency.grid(column = 1, row=5, pady=5)
    
    Radiobutton(inbr_balance_calculator, text = "ZWL Balances", variable = statement_type,value = 0,fg = fg_color, bg = bg_color,activebackground=mid_color).grid(column=0, row=6, sticky="w")
    Radiobutton(inbr_balance_calculator, text = "USD Balances(Indexed)", variable = statement_type,value = 1,fg = fg_color, bg = bg_color,activebackground=mid_color).grid(column=2, row=6, sticky="w")
    
    Checkbutton(inbr_balance_calculator, text="Only expired loans", variable=only_expired, bg=bg_color, fg=fg_color,activebackground=mid_color).grid(row=7, column = 0)
    Checkbutton(inbr_balance_calculator, text="Apply In Duplum Rule", variable=in_duplum, bg=bg_color, fg=fg_color,activebackground=mid_color).grid(row=7, column = 2)
    
        
    date = Label(inbr_balance_calculator,text = "Date as at?",bg = bg_color, fg = fg_color, font=("Arial", 9))
    date.grid(column = 1, row=8, pady=5)
    
    acc_id_label = Label(inbr_balance_calculator,text = "DD/MM/YYYY",bg = bg_color, fg = fg_color, font=("Arial", 9))
    acc_id_label.grid(column = 0, row=9, padx=4, pady=5)

    date_entry = Entry(inbr_balance_calculator,textvariable = final_date, font=('calibre',10,'normal'))
    date_entry.grid(row = 9, column = 1, padx=4, pady=4)
    
    calculate = Button(inbr_balance_calculator, text = 'Calculate',width=10,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color,command =lambda: calculate_inbr_balance())
    calculate.grid(row = 10, column = 2, padx=4, pady=4)

    back_btn = Button(inbr_balance_calculator, text = 'Back',width=10,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color,command = lambda: switch_frame(inbr_balance_calculator,opener))
    back_btn.grid(row = 10, column = 0, padx=4, pady=4)

def to_do_packer():
    tasks = [
            {"task": "Improve Income Reports",
             "date": "9-13-2022",
             "finished": False},
            {"task": "Correct Penalty calculation",
             "date": "10-24-2022",
             "finished": False},
            {"task": "Add extra payments for solar lights",
             "date": "9-13-2022",
             "finished": False},
            {"task": "Integrate demand reports maker",
             "date": "9-13-2022",
             "finished": False},
            {"task":"Make Program work with no setting up",
             "date": "9-13-2022",
             "finished": False}]
    Label(to_do_frame,text = "Upcoming Features",bg = bg_color, fg = fg_color, font=("Arial", 14)).grid(column = 1, row=0,pady=5)
    
    last_row = 0
    for i in range(len(tasks)):
        text = "{}. {}".format(tasks[i]["task"],tasks[i]["date"])
        if tasks[i]["finished"]:
            text = "{}. {}".format(tasks[i]["task"],"Done")
            Label(to_do_frame,text = text,bg = bg_color, fg = fg_color).grid(column = 1, row=i+1,pady=5)
        else:
            Label(to_do_frame,text = text,bg = bg_color, fg = fg_color).grid(column = 1, row=i+1,pady=5)
        last_row = i+1
    back_btn = Button(to_do_frame, text = 'Back',width=10,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color_dark,command =lambda: switch_frame(to_do_frame,opener))
    back_btn.grid(row = last_row+1, column = 1, padx=4,pady=4)

def income_allocator_packer():
    Label(income_allocator,text = "Income Allocator",bg = bg_color, fg = fg_color, font=("Arial", 14)).grid(column = 1, row=0,pady=5)
    
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    current_year = datetime.date.today().year
    current_month = datetime.date.today().month
    years   = [x for x in range(current_year,2019-1,-1)]
    chosen_month = StringVar()
    chosen_month.set(months[current_month-1])
    chosen_year = StringVar()
    chosen_year.set(str(current_year))
  
    Label(income_allocator,text = "Choose Month",bg = bg_color, fg = fg_color, font=("Arial", 9)).grid(column = 0, row=2,pady=5)
  
    month_drop = OptionMenu( income_allocator , chosen_month , *months )
    month_drop.config(width = 10, bg = bg_color, fg = fg_color,activebackground=mid_color)
    month_drop.grid(row = 3, column = 0)
    
    month_drop["menu"].config(bg = mid_color,fg = fg_color)
    
    Label(income_allocator,text = "Choose Year",bg = bg_color, fg = fg_color, font=("Arial", 9)).grid(column = 2, row=2,pady=5)
  
    year_drop = OptionMenu( income_allocator , chosen_year , *years )
    year_drop.config(width = 10, bg = bg_color, fg = fg_color,activebackground=mid_color)
    year_drop.grid(row = 3, column = 2)
    
    back_btn = Button(income_allocator, text = 'Back', width=10,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color,command =lambda: switch_frame(income_allocator,opener))
    back_btn.grid(row = 4, column = 0, padx=4, pady=4)
    
    calc_btn = Button(income_allocator, text = 'Calculate', width=10,fg = fg_color, bd=0, height=2,bg=mid_color,activebackground=mid_color,command = lambda: to_income_allocator(months.index(chosen_month.get())+1,chosen_year.get()))
    calc_btn.grid(row = 4, column = 2, padx=4, pady=4)

if __name__=="__main__":
    opener_packer()
    outbr_stament_maker_packer()
    outbr_balance_calculator_packer()
    inbr_stament_maker_packer()
    inbr_balance_calculator_packer()
    to_do_packer()
    income_allocator_packer()
    # inbr_stament_maker.pack()
    # outbr_balance_calculator.pack()
    # outbr_stament_maker.pack()
    # results.pack()
    opener.pack()
    root.mainloop()