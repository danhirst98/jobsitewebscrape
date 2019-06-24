from spacejobscrape.helperscripts.emailSender.gmail import gmail,message

def sendSummaryEmail(text,email):
    email = gmail.GMail('Job.Import <seds.job.import@gmail.com>','Rurcoj-tusrup-6zudje')
    msg = message.Message('Summary Email',to='Dan <dan.hirst@seds.org>',text=text)
    email.send(msg)
    return

class ErrorLogger:
    def __init__(self,email):
        self.errorlist = []
        self.email = email

    def addError(self):
        return