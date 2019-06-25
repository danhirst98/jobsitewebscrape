from spacejobscrape.helperscripts.emailSender.gmail import gmail,message
import sys, os

class scrapeError:
    def __init__(self,error,company):
        self.error = error
        self.company = company


class ErrorLogger:
    def __init__(self,email):
        self.errorlist = []
        self.email = email

    def sendSummaryEmail(self):
        email = gmail.GMail('Job.Import <seds.job.import@gmail.com>', 'Rurcoj-tusrup-6zudje')
        msg = message.Message('Job Import %s' % self.result(), to='<%s>' % self.email, text=self.toString())
        email.send(msg)
        return


    def addError(self,error,company):


        self.errorlist.append(scrapeError(error,company))
        return

    def result(self):
        if not self.errorlist:
            return "Success"
        else:
            return "Failure"

    def toString(self):
        if not self.errorlist:
            return "There were no errors when running the job scrape."
        else:
            body = "There were errors in the following webscrape files"
            for err in self.errorlist:
                errorstring = "%s: %s\n" % (str(err.company), str(err.error))
                body += errorstring
            return body