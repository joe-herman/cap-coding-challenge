from flask import Flask
from flask import request
import regex as re
import redis
from redlock import RedLockFactory

# Redis connection
cache = redis.Redis(host='cap-redis', port=6379, db=0)

# Able to create an exclusive lock for updating longest word
redlocker = RedLockFactory(
    connection_details=[{
        'host': 'cap-redis',
        'port': 6379,
        'db': 0
    }]
)
CACHE_POPULARITY="STRPOP"
CACHE_LONGEST_STR="LONGSTR"
CACHE_LONGEST_LEN="LONGLEN"

app = Flask(__name__)

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

    # Increment this input in the sortedSet cache,
    # or implicitly initialize it to 1
    cache.zincrby(CACHE_POPULARITY, 1, input)

    # Synchronously set the length
    length = len(input)
    with redlocker.create_lock("length_lock"):
        cacheRaw = cache.get(CACHE_LONGEST_LEN)
        cacheLen = 0 if cacheRaw is None else int(bytes.decode(cacheRaw))
        if length > cacheLen:
            cache.set(CACHE_LONGEST_STR, input)

    return {
        "input": input,
        "length": length,
        "popularChar": mostPopularChar(input)
    }


@app.route('/stats')
def string_stats():
    # Get all strings and their scores
    counts = cache.zrange(CACHE_POPULARITY, -2, -1, withscores=True)
    inputs = {}
    for strCount in counts:
        inputs[bytes.decode(strCount[0])] = round(strCount[1])

    longest_str = bytes.decode(cache.get(CACHE_LONGEST_STR))
    return {
        "inputs": inputs,
        "most_popular": bytes.decode(cache.zrevrange(CACHE_POPULARITY, 0, 0)[0]),
        "longest_input_received": longest_str,
        "longest_input_len": len(longest_str)
    }
