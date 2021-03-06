import urllib.parse
import configparser
import requests
import sys
from bs4 import BeautifulSoup
import sqlite3
import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

if (len(sys.argv) == 1):
    print('Missing arguments -p (Dry run, only print output) -te (Dry run, only sends the email for test purposes) or -e (Add record in database and send email)')
    sys.exit()
argv = sys.argv[1]

conf = {
    'mailserver': None,
    'mailport': None,
    'mailuser': None,
    'mailpassword': None,
    'mailaddress': None,
    'mailsendto': None,
    'mailsendcc': None,
    'printer': None,
    'printerip': None
}
# read configuration
config_fn = "ricohconf.ini"

config = configparser.ConfigParser()

config.read(config_fn)

conf['mailserver'] = config['EMAIL']['server']
conf['mailport'] = config['EMAIL']['port']
conf['mailuser'] = config['EMAIL']['username']
conf['mailpassword'] = config['EMAIL']['password']
conf['mailaddress'] = config['EMAIL']['address']
conf['mailsendto'] = config['EMAIL']['sendto']
conf['mailsendcc'] = config['EMAIL']['sendcc']
conf['printer'] = config['GENERAL']['printer']
conf['printerip'] = config['GENERAL']['printerip']

def getval(text):
    text = str(text).replace('<td nowrap="">', '')
    text = text.replace('</td>','')
    return text

def existsRecord():
    """Verifies if open record exists on the SqLite database."""
    connslq = sqlite3.connect('ricohprints.db')
    csql = connslq.cursor()	
    csql.execute('SELECT * FROM prints WHERE enviado=False')
    records = len(csql.fetchall())
    csql.close()
    if (records > 0):
        return True
    else:
        return False

def lastRecord():
    """Returns next ID on the SqLite database."""
    connslq = sqlite3.connect('ricohprints.db')
    csql = connslq.cursor()	
    csql.execute('SELECT * FROM prints ORDER BY id DESC LIMIT 1')
    row = csql.fetchall()
    csql.close()
    return row

def addRecord(id, pb, cores):
    """Adds record to the SqLite database."""
    connslq = sqlite3.connect('ricohprints.db')
    csql = connslq.cursor()
    csql.execute('INSERT INTO prints VALUES (?, ?, ?, ?, ?)', (id, pb, cores, True, datetime.datetime.now().strftime('%Y-%m-%d')))
    connslq.commit()

def sendEmail(msgtxt, msghtml):
    """Sends email with print counts"""
    context = ssl.create_default_context()

    message = MIMEMultipart("alternative")
    message["Subject"] = "Envio de contagens da impressora {impressora} - Data {data}".format(impressora=conf['printer'], data=datetime.datetime.now().strftime('%Y-%m-%d')) 
    message["From"] = conf['mailaddress']
    message["To"] = conf['mailsendto']
    message["Cc"] = conf['mailsendcc']
    part1 = MIMEText(msgtxt, "plain")
    part2 = MIMEText(msghtml, "html")

    message.attach(part1)
    message.attach(part2)
    
    toaddrs = [conf['mailsendto']] + [conf['mailsendcc']]
    with smtplib.SMTP_SSL(conf['mailserver'], conf['mailport'], context=context) as server:
        server.login(conf['mailuser'], conf['mailpassword'])
        server.sendmail(
            conf['mailaddress'], toaddrs, message.as_string()
        )

if __name__ == "__main__":
    response = urllib.request.urlopen('http://' + conf['printerip'] + '/web/guest/pt/websys/status/getUnificationCounter.cgi')
    soup = BeautifulSoup(response,features="html.parser")
    tables = soup.find_all("table")
    copiador = []
    impressora = []
    final = []

    for index, table in enumerate(soup.find_all("table")):
        if (table.find("div", text="Copiador")):
            counter = -1
            for i , td in enumerate(tables[index + 1].find_all("td")):
                if ("Preto e branco" in td):
                    counter = i + 2
                    txt = "P&B"
                    continue
                if ("Cor integral" in td):
                    counter = i + 2
                    txt = "Cores"
                    continue
                if ("Cor ??nica" in td):
                    counter = i + 2
                    txt = "Cor ??nica"
                    continue
                if ("2 Cores" in td):
                    counter = i + 2
                    txt = "2 Cores"
                    continue
                if counter == i:
                    if len(copiador) < 4:
                        copiador.append(getval(td))
                    counter = -1
                    txt = ""
                    continue
        if (table.find("div", text="Impressora")):
            counter = -1
            for i , td in enumerate(tables[index + 1].find_all("td")):
                if ("Preto e branco" in td):
                    counter = i + 2
                    txt2 = "P&B"
                    continue
                if ("Cor integral" in td):
                    counter = i + 2
                    txt2 = "Cores"
                    continue
                if ("Cor ??nica" in td):
                    counter = i + 2
                    txt2 = "Cor ??nica"
                    continue
                if ("2 Cores" in td):
                    counter = i + 2
                    txt2 = "2 Cores"
                    continue
                if counter == i:
                    if len(impressora) < 4:
                        impressora.append(getval(td))
                    counter = -1
                    txt2 = ""
                    continue
    final.append(int(copiador[0]) + int(impressora[0]))
    final.append(int(copiador[1]) + int(copiador[2]) + int(copiador[3]) + int(impressora[1]) + int(impressora[2]) + int(impressora[3]))
    if existsRecord() == False:
        lastr = lastRecord()
        text = """\
            Envio de contagens da impressora {impressora}:

            Contagem Preto e Branco Atual: {pbatual} (M??s anterior: {pbanterior}) resultado m??s: {pbresultado}
            Contagem Cores Atual: {coratual} (M??s anterior: {coranterior}) resultado m??s: {corresultado}
            
            Com os melhores cumprimentos,
            
            """.format(impressora=conf['printer'], pbatual=final[0], pbanterior=lastr[0][1], pbresultado=int(final[0]) - int(lastr[0][1]), coratual=final[1], coranterior=lastr[0][2], corresultado=int(final[1]) - int(lastr[0][2]))
        dataenvio = "??ltima data de envio: {data}".format(data=lastr[0][4])
        html= """\
            <html>
                <body>
                    Envio de contagens da impressora {impressora}:
                    <br><br>
                    Contagem Preto e Branco Atual: <strong>{pbatual}</strong> (M??s anterior: {pbanterior}) <strong>resultado m??s: <u>{pbresultado}</u></strong><br>
                    Contagem Cores Atual: <strong>{coratual}</strong> (M??s anterior: {coranterior}) <strong>resultado m??s: <u>{corresultado}</u></strong>
                    <br><br>
                    Com os melhores cumprimentos,
                </body>
            </html>
            """.format(impressora=conf['printer'], pbatual=final[0], pbanterior=lastr[0][1], pbresultado=int(final[0]) - int(lastr[0][1]), coratual=final[1], coranterior=lastr[0][2], corresultado=int(final[1]) - int(lastr[0][2]))
        if (argv == "-p"):
            print(text + dataenvio)
        if (argv == "-te"):
            print(text)
            sendEmail(text, html)
            print("Test email Sent")
        if (argv == "-e"):
            print(text)
            sendEmail(text, html)
            print("Email sent")
            addRecord(int(lastr[0][0]) + 1, final[0], final[1])
            print("Added new record to db")
