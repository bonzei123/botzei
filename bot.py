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

        # remove all found urls, whitespaces and line
        # breaks
        for url in urls:
            content = content.replace(url, "")
        content = content.replace(" ", "")
        content = content.replace("\n", "")

        if not content:
            removal_message = "Dieser Pfosten wurde entfernt, da er ein räudiger Selbstpfosten mit nur 'nem Link ist." \
                              "  \nSchäm dich!  \nDu kannst den Link gerne als Linkpfostierung nochmal einreichen."
            submission.mod.remove()
            submission.mod.send_removal_message(removal_message, title='Pfostierungsentfernung', type='public')

def count(subreddit):

    all_strings = []
    translated = []
    need_approval = []
    undecided = []

    for submission in subreddit.hot(limit=1000):
        if submission.stickied:
            sticky = submission
        else:
            all_strings.append(submission)
            if submission.link_flair_text == "Erledigt":
                translated.append(submission)

            elif submission.link_flair_text == "Entscheidung benötigt":
                need_approval.append(submission)

            else:
                undecided.append(submission)

    percentage = len(translated)/len(all_strings)
    message = "Hey! There are "+str(len(all_strings))+" strings submitted already! \n" \
            "We already translated "+str(len(translated))+" of them! (this is "+str((percentage*100))+"%!) \n" \
            "There are "+ str((len(all_strings)-len(translated))) +" strings to translate, where "+ str(len(undecided)) +" of them are undecided and " \
            + str(len(need_approval)) +" need an urgent decision!\n"
    
    comment_exists = False
    for comment in sticky.comments:
        if comment.author.name == "botzei":
            comment.edit(message)
            comment_exists = True
    if not comment_exists:    
        sticky.reply(message)
    print(message)

if __name__ == "__main__":

    # credentials are imported from credentials.py
    try:
        twoFA = "788459"
        reddit = praw.Reddit(client_id=client_id,
                            client_secret=client_secret,
                            password=password+":"+twoFA,
                            user_agent=user_agent,
                            username=username)
    except:
        print("error")
    print("Login successful")

    subreddit = reddit.subreddit('translation_german')
    count(subreddit)
    # for submission in subreddit.stream.submissions():
    #     onlylink(submission)
