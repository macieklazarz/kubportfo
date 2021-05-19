from flask import Flask, render_template, url_for, request, redirect, send_file
from email.message import EmailMessage
from twilio.rest import Client
import csv
import datetime
import smtplib
import time
app = Flask(__name__)
# print(__name__)

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        database.write(f'\n{data["email"]},  {data["message"]}, {datetime.datetime.now()}')
        # database.write('data')



def mail_sender(data):
    email = EmailMessage()
    email['from'] = data.get("email")
    email['to'] = 'tuzownia@gmail.com'
    # email['subject'] = data.get("subject")
    email['subject'] = (f'Wiadomość od {data.get("email")}')

    email.set_content(f'Wiadomość od {data.get("email")}: {data.get("message")}')
    # email.set_content('mail contebt')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('92maciek92maciek92@gmail.com', 'c1helsea')
        smtp.send_message(email)
        # print(email)


def sms_message():
    account_sid = 'wstaw'
    auth_token = 'wstaw'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+48726417085",
        from_="+12058435485",
        body="you have new message on mail")

    print(message.sid)


def not_sent(message):
    with open('mail_sms_failure.txt', mode='a') as mail_sms_failure:
        mail_sms_failure.write(f'\n{datetime.datetime.now()} - {message}')

def time_stamp():
    with open('time_file.txt', mode='w') as time_file:
        time_file.write(str(time.time()))


def time_compare():
    with open('time_file.txt', mode='r') as time_file:
        var1 = float(time_file.read())
        # print(f'poprzedni czas: {var1}')
        # print(f'roznica czasow{time.time()-var1}')
        return(time.time()-var1)


@app.route('/')
def my_home():
    # print(url_for('static', filename='bolt.ico'))
    return render_template('index.html')


@app.route('/<name>')
def my_home2(name=None):
    # print(url_for('static', filename='bolt.ico'))
    return render_template(name)


@app.route('/submit_form', methods = ['POST','GET'])
def submit_form():
    if request.method=='POST':
        data = request.form.to_dict()
        # print(data)
        # print(data.get("mail"))

        if time_compare()>2:
            print(f'data: {data}')
            write_to_file(data)
            # write_to_csv(data)
            time_stamp()
            try:
                mail_sender(data)
            except:
               not_sent('mail not sent')
            # try:
            #     sms_message()
            # except:
            #     not_sent('sms not sent')
            return redirect('/mailsent.html#contact')
        else:
            # print("lipa")
            return redirect('/mailsent.html#contact')
    else:
        return 'sth is wrong'

# @app.route('/getPlotCSV') # this is a job for GET, not POST
# def plot_csv():
#     return send_file('image.jpg',
#                      mimetype='jpg',
#                      attachment_filename='image.jpg',
#                      as_attachment=True)
