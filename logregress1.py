exclude = ['the', 'to', 'of', 'and', 'a', '', 'in', 'that', 'for', 'on', 'is', 'with', 'was',
           'as', 'has', 'up', 'by', 'our', 'at', 'from', 'be', 'are', 'what', 'you', 'more', 'i',
           'an', 'who', 'will', 'we', 'also', 'or', 'and', 'if', 'into', 'before', 'can', 'many',
           'over', 'it', 'do', 'me', 'its']


def sentences(text):

    def split(t, seps):
        for s in seps:
            t = [w for e in t for w in e.split(s) if w != '']
        return t

    text = text.replace('\n', '').replace('(', '').replace(')', '').replace('”', '') \
        .replace('“', '').replace("'s", '').replace(':', '').replace('-', '').lower()
    return split([text], ['.', '!', '?'])