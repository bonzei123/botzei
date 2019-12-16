import praw
from rb import onlyLink
import credentials

reddit = praw.Reddit(client_id=credentials.client_id,
                     client_secret=credentials.client_secret,
                     password=credentials.password,
                     user_agent=credentials.user_agent,
                     username=credentials.username)

print(reddit.user.me())

subreddit = reddit.subreddit('rockharz')
for submission in subreddit.stream.submissions():
    if submission.is_self:
        if onlyLink(submission.selftext):
            if not submission.approved:
                submission.reply("Dieser Post wird entfernt, da er ein räudiger selfpost mit nur einem link ist.   \nSchäm dich!")
                submission.mod.remove()
