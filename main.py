import os
import requests

from atproto import Client, client_utils

mastodon_instance_url = 'https://botsin.space'

# Retrieve secrets from GitHub
access_token = os.environ['ACCESS_TOKEN']
at_password = os.environ['AT_PASSWORD']
wordnik_api_key = os.environ['API_KEY']

# Wordnik API endpoint for the word of the day
wordnik_url = f'http://api.wordnik.com/v4/words.json/wordOfTheDay?api_key={wordnik_api_key}'

def postBluesky(toot):
    client = Client()
    client.login('wotd.skeets.online', at_password)
    
    text = client_utils.TextBuilder().text(toot)
    post = client.send_post(text)
    client.like(post.uri, post.cid)

try:
    # Get the word of the day from Wordnik
    response = requests.get(wordnik_url)
    data = response.json()
    print(data)
    word_of_the_day = data['word']
    definition = data['definitions'][0]['text']

    # Format the toot
    toot = f"📚 Word of the day: {word_of_the_day}\n\nDefinition: {definition}"

    # Mastodon API endpoint for posting a status
    toot_url = f"{mastodon_instance_url}/api/v1/statuses"

    # Set the status parameters
    params = {
        'status': toot,
        'visibility': 'unlisted',  # Adjust visibility as needed
    }

    # Make the API request to post the toot
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.post(toot_url, params=params, headers=headers)
    postBluesky(toot)

    if response.status_code == 200:
        print("Toot posted successfully!")
    else:
        print(f"Error posting toot: {response.text}")

except Exception as e:
    print(f"Error: {e}")
