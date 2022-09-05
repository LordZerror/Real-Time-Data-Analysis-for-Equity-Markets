import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time
import pyfiglet
import smtplib

api_key = ''

ts = TimeSeries(key=api_key, output_format='pandas')

while True:
    print()
    print(pyfiglet.figlet_format("Real Time Data Analysis for", font="digital"))
    print(pyfiglet.figlet_format("US Markets", font="digital"))
    name = input("Enter the name of the stock: ")
    print(
    f'''
1. Generate an excel sheet containing intra-day data of {name}
2. Generate a mail alert for {name} stock when it reaches a certain volatility
3. Exit App''')
    choice = int(input("\nEnter your choice: "))
    if choice in [1, 2]:
        data, meta_data = ts.get_intraday(symbol=name, interval='1min', outputsize='full')
    if choice == 1:
        data.to_excel("output.xlsx")
        print("File Formed Successfully")
    elif choice == 2:
        value = float(input("Enter the percentage change to be checked : "))
        close_data = data['4. close']
        percentage_change = close_data.pct_change()
        last_change = percentage_change[-1]

        if abs(last_change) > value:
            gmail_user = 'user email id'
            gmail_pass = 'make app passwords from security in GMail'
            sent_from = gmail_user
            mail = input("Enter the email address to send to: ")
            to = mail
            subject = f"{name} ALERT"
            body = f"{name} Alert for Volatility\n Last Change Percentage: {last_change}"
            email_text = f"""\
            From: {sent_from}
            To: {to}
            Subject: {subject}

            {body}
            """
            try:
                smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                smtp_server.ehlo()
                smtp_server.login(gmail_user, gmail_pass)
                smtp_server.sendmail(sent_from, to, email_text)
                smtp_server.close()
                print ("Email sent successfully!")
            except Exception as ex:
                print ("Exception Occured: ",ex)
        else:
            print("Currently Low Volatility")

    elif choice == 3:
        print("Thank you! Happy Trading!")
        exit()
    else:
        print("Please enter a valid choice.")
