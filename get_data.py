import json
import requests


# Guessing age from name API
def guess_age_from_name(your_name):
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
