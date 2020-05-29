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

    for submission in subreddit.hot(limit=2500):
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


    removed = 0
    for log in subreddit.mod.log(limit=10000):
        if log.action == "removelink":
            removed += 1

    all_string_count = len(all_strings)+removed
    translated_count = len(translated)+removed
    undecided_count = len(undecided)
    need_approval_count = len(need_approval)

    a = str(translated_count)+"/"+str(all_string_count)
    b = str(round( (translated_count) / (all_string_count)*100,2))
    c = str(all_string_count - translated_count)
    d = str(undecided_count)
    e = str(need_approval_count)

    
    message = "Hey! There are "+str(all_string_count)+" strings submitted already! \n" \
            "We already translated "+str(translated_count)+" of them! (this is "+b+"%!) \n" \
            "There are "+ c+" strings to translate, where "+ d +" of them are undecided and " \
            + e +" need an urgent decision!\n"
    print(message) # for quick info/debugging in console

    # For a comment in the sticky submission
    # comment_exists = False
    # for comment in sticky.comments:
    #     if comment.author.name == "botzei":
    #         comment.edit(message)
    #         comment_exists = True
    # if not comment_exists:    
    #     sticky.reply(message)


    # this edits the sidebar
    sidebar_text = "__"+a+"__\n\n" \
            + "__"+b+"%__ translated\n\n" \
            + "__"+c+"__ open \n\n" \
            + "__"+d+"__ undecided\n\n" \
            + "__"+e+"__ need urgent decision\n\n" \
            + "[Konsistenztabelle] (https://docs.google.com/spreadsheets/d/1ez07F6jysWb7pAKo5gNzCjegAclD3RCWZdNAEy_TL4U/edit?usp=sharing)"
    
    sidebar = subreddit.wiki['config/sidebar']
    
    # edits sidebar only if somthings changed
    if sidebar.content_md != sidebar_text:
        sidebar.edit(sidebar_text)


if __name__ == "__main__":

    # credentials are imported from credentials.py
    reddit = praw.Reddit(client_id=client_id,
                        client_secret=client_secret,
                        password=password,
                        user_agent=user_agent,
                        username=username)

    print("Login successful")

    subreddit = reddit.subreddit('translation_german')
    count(subreddit)


    # for submission in subreddit.stream.submissions():
    #     onlylink(submission)
