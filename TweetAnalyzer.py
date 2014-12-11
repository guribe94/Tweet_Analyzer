from datetime import datetime
from re import sub
from math import radians, pow, asin, cos, sin, sqrt
import csv


# Phase 1: Adding geo data

def make_tweet(tweet_line):
    """Return a tweet, represented as a python dictionary.
    tweet_line: a string corresponding to a line formatted as in all_tweets.txt

    Dictionary keys:
    text  -- A string; the text of the tweet, all in lowercase
    time  -- A datetime object; the time that the tweet was posted
    lat   -- A number; the latitude of the tweet's location
    lon   -- A number; the longitude of the tweet's location

    """
    # Take the numbers between the 2 []
    lat_long = tweet_line[tweet_line.find("[") + 1:tweet_line.find("]")]
    # Cut the numbers between the brackets out of the tweet line
    tweet_line = tweet_line[len(lat_long) + 2:]
    # Split into 2 numbers at the ,
    loc_array = lat_long.split(",")
    # Convert numbers into a float
    lat = float(loc_array[0])
    lon = float(loc_array[1])
    # Remove data from the beginning of the tweet, after the lat and lon is removed the data is 23 characters
    tweet_data = tweet_line[:23]
    text = tweet_line[23:]
    # Split data on spaces
    data = tweet_data.split()
    # Create a timestamp of when the tweet was made
    timestamp = data[1] + " " + data[2]
    # Create the format for the timestamp
    stamp_format = '%Y-%m-%d %H:%M:%S'
    # Make a datetime object from the date
    date = datetime.strptime(timestamp, stamp_format)
    # Create a dictionary for the tweet
    tweet = {"text": text, "time": date, "lat": lat, "lon": lon}
    return tweet


def tweet_text(tweet):
    """Return the text of a tweet as a string"""
    # Take the value associated with the "text" key
    return tweet["text"]


def tweet_words(tweet):
    """Return a list of the words in the text of a tweet not
    including punctuation."""
    # Get text from the dictionary of tweet
    text = tweet["text"]
    # Convert all the text to lowercase because individual words will be displayed
    text = text.lower()
    # Remove everything that is not a letter and replace it with a space
    text = sub('[^a-z\ \']+', " ", text)
    # Split the text on space
    words = text.split()
    # return an array of the words in the tweets
    return words


def tweet_time(tweet):
    """Return the datetime that represents when the tweet was posted."""
    # Take the value associated with the "time" key
    return tweet["time"]


def tweet_location(tweet):
    """Return an tuple that represents the tweet's location."""
    # Create a tupple of the latitude and longitude
    location = (float(tweet["lat"]), float(tweet["lon"]))
    return location


def make_zip(zipcode):
    """Return a zip code, represented as a python dictionary.
    zipcode: a list containing a single zip codes data ordered as in zips.csv

    Dictionary keys:
    zip    -- A string; the sip code
    state   -- A string; Two-letter postal code for state
    lat    -- A number; latitude of zip code location
    lon    -- A number; longitude of zip code location
    city   -- A string; name of city assoicated with zip code

    """
    # Split each input line on the ,
    zipdata = zipcode.split(",")
    # Remove leading and trailing space and the "" that surround values
    code = zipdata[0].strip().strip('"').strip()
    state = zipdata[1].strip().strip('"').strip()
    lat = zipdata[2].strip().strip('"').strip()
    lon = zipdata[3].strip().strip('"').strip()
    city = zipdata[4].strip().strip('"').strip()
    # Create a dictionary of zip code info
    zipinfo = {"zip": code, "state": state, "lat": lat, "lon": lon, "city": city}
    return zipinfo


def find_zip(tweet, zip_list):
    """return zipcode associated with a tweets location data
    zip_list is a list of zip_codes represented as dictionaries"""
    # Get the location of the tweet
    tweetloc = tweet_location(tweet)
    # Take the location of the first zip code
    firstloc = (zip_list[0]["lat"], zip_list[0]["lon"])
    # Calculate the distance between the two locations
    smallestdistance = geo_distance(tweetloc, firstloc)
    # Set the index of the smallest distance this will be updated in the loop below
    smallestindex = 0
    count = 0
    for zip in zip_list:
        # For each zip code in the list calculate the new distance
        ziplat = zip_list[count]["lat"]
        ziplon = zip_list[count]["lon"]
        ziploc = (ziplat, ziplon)
        distance = geo_distance(tweetloc, ziploc)
        count = count + 1
        # Check to see if the newly calculated distance is smaller than the previous smallestdistance if it is update
        # the smallestdistance and record the index
        if distance < smallestdistance:
            smallestdistance = distance
            smallestindex = count
    # If the smallest distance is more than 200 miles away it is not in the US and does not have a real zip code
    if smallestdistance > 200:
        zipdata = {"zip":"N/A", "state":"N/A"}
    else:
        # Create a dictionary of the zip code data
        zipdata = {"zip":zip_list[smallestindex]["zip"], "state":zip_list[smallestindex]["state"]}



    # Return the dictionary of zip code info
    return zipdata

def geo_distance(loc1, loc2):
    """Return the great circle distance (in miles) between two
    tuples of (latitude,longitude)

    Uses the "haversine" formula.
    http://en.wikipedia.org/wiki/Haversine_formula"""
    # radius of earth given in miles
    radiusofearth = 6378.1
    # Take latitude and longitue from the given tupples
    lat1 = float(loc1[0])
    lon1 = float(loc1[1])
    lat2 = float(loc2[0])
    lon2 = float(loc2[1])
    # Part of the equation that goes inside the inverse sin
    theta = sqrt(
        pow(sin(radians((lat2 - lat1) / 2)), 2) + (
        (( cos(radians(lat1))) * ( cos(radians(lat2)))) * pow(sin(radians((lon2 - lon1) / 2)), 2)))
    # Calculate distance with the haversin formula
    distance = (radiusofearth * 2) * asin(theta)
    # Convert from kilometers to miles
    distanceinmiles = distance * 0.621371
    return distanceinmiles


def add_geo(tweets):
    """adds the new keys state and zip to each tweet dictionary in the list tweets"""
    # Open the roster of zip codes, this is hardcoded because zip codes won't change
    f = open('zips.csv', 'r')
    # Skip the first line which contains no data other than formatting
    f.readline()
    zipinfo = f.readlines()
    zip_list = []
    # For each line in the zipcode roster create a dictionary of zip code information and add it to the array
    for zip in zipinfo:
        dict = make_zip(zip)
        zip_list.append(dict)
    # For each tweet in the array of tweets append zip code and state information
    for tweet in tweets:
        code = find_zip(tweet, zip_list)
        tweet["zip"] = code["zip"]
        tweet["state"] = code["state"]

    return tweets


def write_tweets(tweets, outfile):
    """writes the list of tweets to a text file with name outfile"""
    # Create an outout file
    f = open(outfile, 'w')
    # For each tweet in the array of tweets write it out to the output file
    for tweet in tweets:
        # write each dictionary plus a new line character
        f.write(str(tweet) + '\n')
    # Close the file
    f.close()

def create_sentiment_database(filename):
    """Create a database of the sentiment value associated with the given csv
    file. It is assumed that the input file is a csv file with the first value
    being the word and the second value being the sentiment value

    """
    # Read the values from the input filename
    reader = csv.reader(open(filename))
    sentiment = {}
    # For each line read from the CSV file add it to the dictionary of
    # sentiments...the word is the key
    for each in reader:
        sentiment[each[0]] = float(each[1])
    # Return the dictionary of sentiments
    return sentiment


def assign_sentiments(tweets, sentiments):
    """Assign each tweet a sentiment value between 1 and -1"""
    # For each tweet in the given array calculate and add a sentiment
    for tweet in tweets:
        # Get the words in each tweet
        tweettext = tweet_words(tweet)
        # Initilize a vairable for sentiment value, initially there
        # should be no sentiment
        sentimentvalue = 0
        for word in tweettext:
            # Check to see if each word is in the sentiments databse
            if word in sentiments:
                # If it is add it to the sentimentvalue
                sentimentvalue += sentiments[word]
        # At the end if the sentiment is 0 make the sentiment equal None
        if sentimentvalue == 0:
            tweet["sentiment"] = None
        # If the sentiment is greater than 1 set the value to 1
        elif sentimentvalue > 1:
            tweet["sentiment"] = 1
        # If the sentiment is less than -1 set the value to -1
        elif sentimentvalue < -1:
            tweet["sentiment"] = -1
        # Otherwise set the sentiment value to the calculated sentiment value
        else:
            tweet["sentiment"] = sentimentvalue
    # Return the dictionary with the sentiments added
    return tweets


def find_tweets_containing(word, tweets):
    """Search tweets for ones containing specified word.
    Returns list of tweets with specified word

    """
    # Create an array for the found tweets
    foundtweets = []
    # For each tweet check if the work exists
    for tweet in tweets:
        for x in tweet_words(tweet):
            # If the word given is in the tweet add it to the
            # array of found tweets
            if x == word:
                foundtweets.append(tweet)
                # Exit the for loop on the first instance so the tweet isn't
                # added twice if the word occurs more than once
                break
    # Return the list of found tweets
    return foundtweets


def find_tweets_from_state(state, tweets):
    """Search tweets for ones from a specified state.
    Returns list of tweets from the specified state

    """
    # Create an array for the found tweets
    foundtweets = []
    for tweet in tweets:
        # Check each tweet to see is from the state being filtered
        if tweet["state"] == state:
            # Add it to the array of found tweets
            foundtweets.append(tweet)
    # return the list of found tweets
    return foundtweets


def find_tweets_from_zip(zip, tweets):
    """Search tweets for ones from a specified zip code.
     Returns list of tweets from the specified zip code

     """
    # Create an array for the found tweets
    foundtweets = []
    # For each tweet in the array of tweets check if the zip code
    # matches the one being filtered
    for tweet in tweets:
        if tweet["zip"] == zip:
            # If it is add it to the array of found tweets
            foundtweets.append(tweet)
    # return the list of found tweets
    return foundtweets


def tweet_filter(tweets, **kwargs):
    """Filter tweets based on a given word, zip code, state,
     or a combination of the 3

     """
    # If the user gives a word to filter by run the filter by the word
    if "word" in kwargs:
        tweets = find_tweets_containing(kwargs["word"], tweets)
    # If the user gives a zip code to filter by run the filter by the zip code
    if "zip" in kwargs:
        tweets = find_tweets_from_zip(kwargs["zip"], tweets)
    # If the user gives a state to filter by run the filter by the state
    if "state" in kwargs:
        tweets = find_tweets_from_state(kwargs["state"], tweets)
    # Return the filtered tweets
    return tweets


def find_average_sentiment(tweets):
    """Calculate the average sentiment of each tweet in the given dictionary,
    return a dictionary with the same data and the sentiment value appended

    """

    # Set a variable for the sentimenttotal, initilize it to 0
    sentimenttotal = 0
    totaltweets = len(tweets)
    for tweet in tweets:
        # For each tweet if the sentiment value is not None add it
        # to the sentimenttotal
        if tweet["sentiment"] != None:
            sentimenttotal += tweet["sentiment"]
    # Calculate the average
    averagesentiment = (sentimenttotal / totaltweets)
    # Return the average
    return averagesentiment


def create_state_database(filename):
    """Create a database of states from the given filename. Return an array
     containing each state. It is assumed that the input file has one state
     abbreviation on each line

     """
    # Create a array for the states
    states = []
    # Open the given file in read mode
    f = open(filename, 'r')
    # For each line add it in the file add the state to the array of states
    for line in f:
        # Strip all new line characters and other whitespace that might exist
        line = line.strip()
        # Add it to the list of states
        states.append(line)
    return states


def most_positive(tweets, word):
    """Find the state which has the most positive sentiment about a given
    word, return the state as an abbreviation

    """

    # create an array of all 50 states
    states = create_state_database("states.txt")
    # create a variable to keep track of which tweet has the highest sentiment
    highestsentiment = 0
    statename = ""
    filetered = []
    # Calculate the average sentiment value for each state
    for state in states:
        filtered = tweet_filter(tweets, word=word, state=state)
        if filtered:
            sentiment = find_average_sentiment(filtered)
        else:
            sentiment = -10
        # Check if the sentiment that was just calculated is greater
        #  than the previous highestsentiment
        if sentiment > highestsentiment:
            # If it is take note of the new highest sentiment and
            # the state that it came from
            highestsentiment = sentiment
            statename = state
    # Return the state with the highest sentiment
    return statename


def most_negative(tweets, word):
    """Find the state which has the most negative sentiment about a
    given word, return the state as an abbreviation

    """
    # create an array of all 50 states
    states = create_state_database("states.txt")
    filtered = []
    # create a variable to keep track of which tweet has the lowest sentiment
    lowestsentiment = 0
    statename = ""
    # Calculate the average sentiment value for each state
    for state in states:
        state = state.strip()
        filtered = tweet_filter(tweets, word=word, state=state)
        if filtered:
            sentiment = find_average_sentiment(filtered)
        else:
            sentiment = 10
        # Check if the sentiment that was just calculated is less
        # than the previous lowest sentiment
        if sentiment < lowestsentiment:
            # If it is take note of the new highest sentiment and
            # the state that it came from
            lowestsentiment = sentiment
            statename = state
    # Return the state with the lowest sentiment
    return statename

