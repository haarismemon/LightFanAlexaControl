import smtplib
import subprocess
import re

from credentials import *

ngrokResponse = subprocess.check_output("""curl --silent --show-error http://127.0.0.1:4040/api/tunnels""", shell=True)
p = '"public_url":"http.://([^"]*)"'
m = re.search(p, ngrokResponse)
newEndpoint = 'https://' + m.group(1)


smtpUser = username
smtpPass = password

toAdd = email
fromAdd = smtpUser

alexaDevConsole = '\n\nAlexa Dev Console: ' + alexaDevConsoleUrl

subject = 'Alexa Pi New Endpoint'
header = 'To: ' + toAdd + '\n' 'From: ' + fromAdd + '\n' + 'Subject: ' + subject

ip_address = subprocess.check_output("hostname -I | awk '{print $1}'", shell=True)

body = 'The pi zero for the alexa light control has been switched off and back on again.\n\nNew endpoint is:\n' + newEndpoint + alexaDevConsole + '\n\nIP Address: ' + ip_address

print header + '\n' + body

s = smtplib.SMTP('smtp.gmail.com',587)

s.ehlo()
s.starttls()
s.ehlo()

s.login(smtpUser, smtpPass)
s.sendmail(fromAdd, toAdd, header + '\n' + body)

s.quit()
