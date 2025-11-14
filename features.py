# features.py
from urllib.parse import urlparse
import re

# ---- helpers copied/cleaned from your notebook ----

def count_www(url: str) -> int:
    return str(url).count('www')

def count_atrate(url: str) -> int:
    return str(url).count('@')

def no_of_dir(url: str) -> int:
    urldir = urlparse(str(url)).path
    return urldir.count('/')

def no_of_embed(url: str) -> int:
    urldir = urlparse(str(url)).path
    return urldir.count('//')

# single big regex exactly like your code
_SHORTENING_RE = re.compile(
    r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
    r'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
    r'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
    r'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
    r'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
    r'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
    r'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
    r'tr\.im|link\.zip\.net',
    re.IGNORECASE
)
def shortening_service(url: str) -> int:
    return 1 if _SHORTENING_RE.search(str(url)) else 0

def count_https(url: str) -> int:
    return str(url).count('https')

def count_http(url: str) -> int:
    return str(url).count('http')

def count_per(url: str) -> int:
    return str(url).count('%')

def count_ques(url: str) -> int:
    return str(url).count('?')

def count_hyphen(url: str) -> int:
    return str(url).count('-')

def count_equal(url: str) -> int:
    return str(url).count('=')

def url_length(url: str) -> int:
    return len(str(url))

def hostname_length(url: str) -> int:
    return len(urlparse(str(url)).netloc)

# suspicious words regex from your code
_SUS_RE = re.compile(r'PayPal|login|signin|bank|account|update|free|lucky|service|bonus|ebayisapi|webscr', re.IGNORECASE)
def suspicious_words(url: str) -> int:
    return 1 if _SUS_RE.search(str(url)) else 0

def digit_count(url: str) -> int:
    return sum(ch.isnumeric() for ch in str(url))

def letter_count(url: str) -> int:
    return sum(ch.isalpha() for ch in str(url))

# (optional) not in your snippet, but often present; harmless if unused
def count_dot(url: str) -> int:
    return str(url).count('.')

# ---- the function the server calls ----
def main(url: str):
    """
    Return a DICT where keys match your DataFrame column names from the notebook.
    Any column absent in feature_columns.json will be ignored by the server;
    any column present there but missing here will be auto-filled to 0.
    """
    s = str(url)

    return {
        # EXACT column names from your code:
        'count-www':          count_www(s),
        'count@':             count_atrate(s),
        'count_dir':          no_of_dir(s),
        'count_embed_domian': no_of_embed(s),
        'short_url':          shortening_service(s),
        'count-https':        count_https(s),
        'count-http':         count_http(s),
        'count%':             count_per(s),
        'count?':             count_ques(s),
        'count-':             count_hyphen(s),
        'count=':             count_equal(s),
        'url_length':         url_length(s),
        'hostname_length':    hostname_length(s),
        'sus_url':            suspicious_words(s),
        'count-digits':       digit_count(s),
        'count-letters':      letter_count(s),

        # useful extras (safe placeholders if not used):
        'count_dot':          count_dot(s),     # just in case this exists in your columns
        'tld_length':         len((urlparse(s).hostname or '').split('.')[-1]) if urlparse(s).hostname else 0,
        'no_of_dir':          s.count('/'),     # some notebooks use this name as well
        'no_of_embed':        urlparse(s).path.count('//'),
        'count_www':          s.count('www'),   # if some variant uses underscore naming
    }
