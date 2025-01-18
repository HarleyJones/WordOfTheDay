import json
import os
import random
from atproto import Client, client_utils

# Environment variable for password
at_password = os.environ['AT_PASSWORD']

def postBluesky(toot):
    client = Client()
    client.login('wotd.harljo.uk', at_password)

    # Use TextBuilder to create the post with hashtags
    text_builder = client_utils.TextBuilder(toot)
    text_builder.tag('#WordOfTheDay')
    text_builder.tag('#WOTD')
    text_builder.tag('#BOT')

    post = client.send_post(text_builder)
    client.like(post.uri, post.cid)

try:
    # Load dictionary from JSON file
    with open('dictionary.json', 'r') as f:
        dictionary = json.load(f)

    # Randomly select a word and its definition
    words = list(dictionary.keys())
    definitions = list(dictionary.values())
    index = random.randint(0, len(words) - 1)
    word = words[index]
    definition = definitions[index]

    # Format the post content
    formatted_text = f"📚 The word of the day is {word}!\n––––––––––\nDefinition/s:\n{definition}\n\n#WordOfTheDay #WOTD #BOT"
    postBluesky(formatted_text)

except Exception as e:
    print(f"Error: {e}")
