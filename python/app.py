from flask import Flask
from flask import request
import regex as re
import string


app = Flask(__name__)

seen_strings = {}

@app.route('/')
def root():
    return '''
    <pre>
    Welcome to the Stringinator 3000 for all of your string manipulation needs.

    GET / - You're already here!
    POST /stringinate - Get all of the info you've ever wanted about a string. Takes JSON of the following form: {"input":"your-string-goes-here"}
    GET /stats - Get statistics about all strings the server has seen, including the longest and most popular strings.
    </pre>
    '''.strip()


# Returns the first most popular non-whitespace, non-punctuation characters
def mostPopularChar(input):
    # Remove all punctuation and non-whitespace characters
    sanitized = re.sub(r"[\p{P}\s]+", "", input)
    if not len(sanitized):
        return ''
    
    freqs = {}
    maxFreq = 0

    # Build dict of frequencies
    for char in sanitized:
        if not char in freqs:
            freqs[char] = 1
        else:
            freqs[char] += 1
        
        if freqs[char] > maxFreq:
            maxFreq = freqs[char]
    
    # Reiterate to find first max freqency
    for char in freqs:
        if freqs[char] == maxFreq:
            return char
    
    return ''


@app.route('/stringinate', methods=['GET','POST'])
def stringinate():
    input = ''
    if request.method == 'POST':
        input = request.json['input']
    else:
        input = request.args.get('input', '')

    if input in seen_strings:
        seen_strings[input] += 1
    else:
        seen_strings[input] = 1

    return {
        "input": input,
        "length": len(input),
        "popularChar": mostPopularChar(input)
    }

@app.route('/stats')
def string_stats():
    return {
        "inputs": seen_strings,
    }
