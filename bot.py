import praw
import re
from datetime import datetime
from credentials import *

SUBREDDIT_NAME = "translation_german"
TRANSLATION_WIDGET_NAME = "Translation Status"

def onlylink(submission):
    if submission.is_self and not submission.approved:
        content = submission.selftext
        regexhttp = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        regexwww = r'www.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
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
            if removed == 0:
                print(vars(log))
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

    # this edits the sidebar
    sidebar_text = "#__"+a+"__\n\n" \
            + "#__"+b+"%__ translated\n\n" \
            + "#__"+c+"__ open \n\n" \
            + "#__"+d+"__ undecided\n\n" \
            + "#__"+e+"__ need urgent decision\n\n" \
            + "#__urgent translations:__\n\n"
    
    cnt = 1
    for post in need_approval:
        string = str(cnt)+". ["+post.title+"]("+post.url+")\n\n"
        sidebar_text += string
        cnt += 1

    sidebar_text +="#__old submissions:__\n\n"

    cnt = 1
    for post in undecided:
        time = datetime.now().timestamp() - post.created_utc
        if  datetime.utcfromtimestamp(time).day > 10:
            string = str(cnt)+". ["+post.title+"]("+post.url+")\n\n"
            sidebar_text += string
            cnt +=1

    sidebar_text += "[Konsistenztabelle] (https://docs.google.com/spreadsheets/d/1ez07F6jysWb7pAKo5gNzCjegAclD3RCWZdNAEy_TL4U/edit?usp=sharing)"

    return sidebar_text


def update_r2_sidebar(subreddit, sidebar_text):
    sidebar = subreddit.wiki['config/sidebar']

    # edits sidebar only if somthings changed
    if sidebar.content_md != sidebar_text:
        sidebar.edit(sidebar_text)


def update_d2x_sidebar(subreddit, sidebar_text):
    translation_widget = None
    widgets = subreddit.widgets.sidebar
    for widget in widgets:
        if(widget.shortName == TRANSLATION_WIDGET_NAME):
            translation_widget = widget

    # create widget if it does not exist
    if(translation_widget is None):
        translation_widget = create_translation_widget(subreddit)

    # edits widget only if somthings changed
    if(translation_widget.text != sidebar_text):
        translation_widget.mod.update(text=sidebar_text)


def create_translation_widget(subreddit):
    # the styles will be inherited from the global template
    styles = {'backgroundColor': '', 'headerColor': ''}
    translation_widget = subreddit.widgets.mod.add_text_area(
        TRANSLATION_WIDGET_NAME, 'placeholder content', styles)
    return translation_widget


if __name__ == "__main__":

    # credentials are imported from credentials.py
    reddit = praw.Reddit(client_id=client_id,
                        client_secret=client_secret,
                        password=password,
                        user_agent=user_agent,
                        username=username)

    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    print("begin script "+str(datetime.now()))

    sidebar_text = count(subreddit)
    update_r2_sidebar(subreddit, sidebar_text)
    update_d2x_sidebar(subreddit, sidebar_text)

    print("finished script "+str(datetime.now()))

    # for submission in subreddit.stream.submissions():
    #     onlylink(submission)
