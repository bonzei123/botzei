import praw
import re
from credentials import *


def onlylink(submission):
    if submission.is_self and not submission.approved:
        content = submission.selftext
        regexhttp = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        regexwww = 'www.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(regexhttp, submission.selftext)
        urls.extend(re.findall(regexwww, content))

        # remove all found urls, whitespaces and linebreaks
        for url in urls:
            content = content.replace(url, "")
        content = content.replace(" ", "")
        content = content.replace("\n", "")

        if not content:
            removal_message = "Dieser Post wird entfernt, da er ein räudiger selfpost mit nur einem link ist.   " \
                              "\nSchäm dich! "
            submission.mod.remove()
            submission.mod.send_removal_message(removal_message, title='depp', type='public')


if __name__ == "__main__":

    # credentials are imported from credentials.py
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         password=password,
                         user_agent=user_agent,
                         username=username)

    print(reddit.user.me())

    subreddit = reddit.subreddit('rockharz')
    for submission in subreddit.stream.submissions():
        onlylink(submission)
