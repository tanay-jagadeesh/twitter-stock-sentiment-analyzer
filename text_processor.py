""""Purpose of this file is to clean data""""
import re 

def remove_url(txt, p):
    res = re.sub(p, "[URL REMOVED]", txt)
    return res

def remove_special_characters(s):
    res = re.sub(r'[^a-zA-Z0-9]', '', s)
    return res

def lowercase(txt):
    lower = txt.lower()
    return lower

def remove_whitespace(txt):
    cleaned = txt.strip()
    return cleaned