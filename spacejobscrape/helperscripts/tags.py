
def getCategory(title,desc):
    """
    Returns whether the position is a job or an internship

    Should be as easy as an if statement, though if you could find anything more robust that'd be amazing.

    :param title: job title (str)
    :param desc: job description (str)
    :return: "job" or "internship" (str)
    """

    if 'intern' in title or 'internship' in title:
        return 'internship'
    else:
        return 'job'

def getSkills(desc):
    """
    Finds the skills associated with the position

    Uses skills-ml and other labels to identify up to 10 skills for the position. Can be anything from programming languages to experience with engines. May need to create a list of available skills beforehand

    :param desc: job description (str)
    :return: list of skills (list of strs)
    """

    return ['none']

def getITAR(desc):
    """
    Finds if the position is ITAR restricted or not

    There are some jobs that include the ITAR restricted language which is copy pasted, meaning it should be relatively easy to identify. Alternatively, we could sort this by citizenship (i.e. do you need American citizenship, US permanent residency or just a visa to work). The citizenship approach would probably be more useful. Approach could be:
    1. Check for ITAR copy pasted language
    2. If there isn't, check for anything about permanent residency
    3. If there isn't, check for anything about US citizen
    4. If not, assume that it's open
    If we could do something more sophisticated and robust, that'd be great. Can't find any repos on github about anything similar, so may have to just do this ourselves - still do your own research

    :param desc: job desc (str)
    :return: ITAR restriction or not (boolean)
    """

    return False

def getField(title,desc):
    """
    Finds the field of the position (e.g. project management, software engineering, etc.)

    You can use whichever definitions you want, but if you need more guidance we can get Morgan to write up the job fields she wants people to search by. Ideally this would be a skills-ml tool, or at least using something more sophisticated than if/else statements.

    :param title: job title (str)
    :param desct: job description (str)
    :return: job type (str)
    """

    return ""

def getExperienceLevel(title,desc):
    """
    Returns the experience level required for the position (entry level, junior, senior, etc.)

    Not a required v1 feature, but would be nice to have. Especially as we are thinking about skewing this towards junior/entry level jobs, it would be good to be able to categorise that. Most jobs have 'senior' or 'sr.' on their job titles so we could possibly identify through that. Please add any categorisations that you think are useful

    :param title: job title (str)
    :param desc: job description (str)
    :return: 'entry','junior','senior' (str)
    """


def getTags():
    """
    Script that will run the tag identifier scripts

    This will probably be integrated into the job class, but I need to do some playing around to make sure it is useful. Play with this if you want but don't worry.

    :return: complete list of tags (list of tuples probably)
    """

    return []