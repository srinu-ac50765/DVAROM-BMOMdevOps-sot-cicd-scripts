
import logging.handlers
#from utils import py
import smtplib
import sys
    
# Import the email modules we'll need
from email.message import EmailMessage
log = logging.getLogger("emailLib")

MAILHOST = 'mailgate.corp.intranet'
FROM     = 'ning.li@centurylink.com'
CC       = ["ning.li@centurylink.com", "roby.valiyaparambil1@centurylink.com", "Harish.Madisetty@centurylink.com", "Naimesh.Bhatt@centurylink.com", "Raj.Mishra@CenturyLink.com"]
#CC       = ["ning.li@centurylink.com"]

def sendEmail(subject, recipientsList, message):        
  
    try:

        msg             = EmailMessage()
        msg['From']     = FROM
        msg['Subject']  = subject
        msg['To']       = recipientsList
        msg['Cc'] = CC
                
        msg.set_content(message)
        
        log.debug('\n\t*** About to send mail to %s*** \n', recipientsList)

        smtpClient = smtplib.SMTP(MAILHOST)
        smtpClient.send_message(msg)
        smtpClient.close()

    except Exception as e:
        log.exception(e)
        log.error('\n*** Could not send mail to recipient(s) ***')
        sys.exit(1)

    log.debug('\n\t*** Done sending mail ***')

# https://stackoverflow.com/questions/1610845/collate-output-in-python-logging-memoryhandler-with-smtphandler/1611958#1611958
class BufferingSMTPHandler(logging.handlers.BufferingHandler):
    
    def __init__(self):
        capacity = 1000000;
        logging.handlers.BufferingHandler.__init__(self, capacity)
        self.setFormatter(logging.Formatter('%(message)s'))
        self.subject = ""
        self.toaddrs=""
        self.msgPreamble=""
    
    def sendEmail(self, subject, toaddres, msgPreamble = ""):
        self.subject = subject
        self.toaddrs = toaddres
        self.msgPreamble = msgPreamble + "\r\n\r\n";
        self.flush()

    def flush(self):
        if len(self.buffer) > 0:
            try:
                msg = self.msgPreamble
                for record in self.buffer:
                    s = self.format(record)
                    #print(s)
                    msg = msg + s + "\r\n"
                #smtp.sendmail(self.fromaddr, self.toaddrs, msg)
                sendEmail(self.subject, self.toaddrs, msg)
                #smtp.quit()
            except:
                self.handleError(None)  # no particular record
            self.buffer = []
