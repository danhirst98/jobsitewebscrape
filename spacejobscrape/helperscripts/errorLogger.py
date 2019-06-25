from spacejobscrape.helperscripts.emailSender.gmail import gmail, message


class scrapeError:
    def __init__(self, type, script):
        self.type = type
        self.script = script


class ErrorLogger:
    def __init__(self, email):
        self.errorlist = []
        self.email = email

    def sendSummaryEmail(self):
        email = gmail.GMail('Job.Import <seds.job.import@gmail.com>', 'Rurcoj-tusrup-6zudje')
        msg = message.Message('Summary Email', to='<%s>' % self.email, text=self.toString())
        email.send(msg)
        return

    def addError(self, type, script):
        self.errorlist.append(scrapeError(type, script))
        return

    def toString(self):
        if not self.errorlist:
            return "Success"
        else:
            return "Failure"
