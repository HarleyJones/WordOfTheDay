import json
import os
import requests
import random
from atproto import Client, client_utils

mastodon_instance_url = 'https://mastodon.cloud'
debugTesting = 0

# Retrieve secrets from GitHub
if (debugTesting == 0):
    access_token = os.environ['ACCESS_TOKEN']
    at_password = os.environ['AT_PASSWORD']

def postBluesky(toot):
    client = Client()
    client.login('wotd.bluesky.bot', at_password)
    
    text = client_utils.TextBuilder().text(toot)
    post = client.send_post(text)
    client.like(post.uri, post.cid)

try:
    with open('dictionary_unfiltered.json', 'r') as f:
        dictionary = json.load(f)

    words = list(dictionary.keys())
    definitions = list(dictionary.values())

    index = random.randint(0, len(words))
    word = words[index]
    definition = definitions[index]

    # Format the toot
    formatted_text = f"📚 The word of the day is {word}!\n––––––––––\nDefinition/s:\n{definition}"
    toot = f"{formatted_text}\n\n#wordoftheday #wotd #english #bot"
    if (debugTesting == 0):
        # Mastodon API endpoint for posting a status
        toot_url = f"{mastodon_instance_url}/api/v1/statuses"

        params = {
            'status': toot,
            'visibility': 'unlisted',
        }

        # Make the API request to post the toot
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.post(toot_url, params=params, headers=headers)
        postBluesky(formatted_text)

        if response.status_code == 200:
            print("Toot posted successfully!")
        else:
            print(f"Error posting toot: {response.text}")

except Exception as e:
    print(f"Error: {e}")
