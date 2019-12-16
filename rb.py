import re


def onlyLink(text):
    regexhttp = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    regexwww = 'www.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(regexhttp, text)
    urls.extend(re.findall(regexwww, text))
    text2 = text
    for url in urls:
        text2 = text2.replace(url, "")

    if not text2:
        return True
    else:
        return False


if __name__ == "__main__":
    print(onlyLink("lololo www.google.de"))
