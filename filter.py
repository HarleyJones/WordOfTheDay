import json

# Load bad words from file
with open('badwords.txt', 'r') as f:
    bad_words = [line.strip().lower() for line in f]

# Load JSON wordlist
with open('dictionary_unfiltered.json', 'r') as f:
    wordlist = json.load(f)

# Filter bad words
filtered_wordlist = {word: count for word, count in wordlist.items() if word.lower() not in bad_words}

# Dump the filtered wordlist to a file
with open('dictionary.json', 'w') as f:
    json.dump(filtered_wordlist, f, indent=4)