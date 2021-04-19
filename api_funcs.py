import json
import requests


# Guessing age from name API
def guess_age_from_name(your_name):
    """"
    Enter a name and return an age

    Args:
        your_name (string): the end user's name

    Returns:
        age: the end users age

    Raises:
        Exception: None

    """
    response = requests.request('GET', f'https://api.agify.io/?name={your_name}')
    if response.status_code != 200:
        print(response.status_code)
    parsed = json.loads(response.text)
    age = parsed['age']
    return age


my_age = guess_age_from_name('blessed')


# Kanye quotes API
def get_kanye_quote():
    """Get a kanye qoute."""
    response = requests.request('GET', 'https://api.kanye.rest/')
    if response.status_code != 200:
        print(response.status_code)
    return json.loads(response.text)['quote']


kanye_quote = get_kanye_quote()


# Wholesome qoutes API
def get_nice_qoute():
    """Get a nice qoute."""
    response = requests.request('GET',
                                'https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json')
    if response.status_code != 200:
        print(response.status_code)
    author = json.loads(response.text)['quoteAuthor']
    quote = json.loads(response.text)['quoteText']

    return author, quote


my_qoute, my_author = get_nice_qoute()
