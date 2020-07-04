# Native
import smtplib
import re


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from string import Template
from config import address, password

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def sendEmail(data):

    # set up the SMTP server
    s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
    s.login(address, password)

    message_template = read_template('resources/message.txt')

    keys = data.keys() 
    email_regex = re.compile(r".+?([Ee]mail)")
    desc = data["desc"]

    # Replace all newlines with <br>
    desc = re.sub(r"\n", "<br>", desc)

    # Replace the space preceeding the last two statements with <br>
    desc = re.sub(r"\s(?=(Value to client:))", "<br>", desc)
    desc = re.sub(r"\s(?=(Additional Info:))", "<br>", desc)

    # newline after statement
    desc = re.sub(r"Challenge to client:", "Challenge to client:<br>", desc)
    desc = re.sub(r"Value to client:", "Value to client:<br>", desc)
    desc = re.sub(r"Additional Info:", "Additional Info:<br>", desc)

    # Bold each subcategory in description
    desc = re.sub(r"Challenge to client:", "<strong>Challenge to client:</strong>", desc)
    desc = re.sub(r"Value to client:", "<strong>Value to client:</strong>", desc)
    desc = re.sub(r"Additional Info:", "<strong>Additional Info:</strong>", desc)

    for key in keys:
        if re.fullmatch(email_regex, key):
            
            msg = MIMEMultipart() # create a message
            
            message = message_template.substitute(
            leadName = data["leadName"],
            consultant = data["consultant"],
            consEmail = data["consEmail"],
            dateSubmitted = data["dateSubmitted"],
            bizUnit = data["bizUnit"],
            capability = data["capability"],
            desc = desc,
            tmEmail = data["tmEmail"],
            cmEmail = data["cmEmail"],
            account = data["clientAcct"],
            clientDept = data["clientDept"],
            clientContact = data["clientContact"]
            )

            # setup the parameters of the message
            msg['From'] = address
            msg['To'] = data[key]
            msg['Subject']= f'New Lead: {data["clientAcct"]} - "{data["leadName"]}"'
            
            # add in the message body
            msg.attach(MIMEText(message, 'HTML', _charset="UTF-8"))

            # send the message via the server set up earlier.
            s.send_message(msg)

            del msg

    # Terminate the SMTP session and close the connection
    s.quit()