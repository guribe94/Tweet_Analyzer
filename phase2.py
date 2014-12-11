import csv
import TweetAnalyzer


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
        tweettext = TweetAnalyzer.tweet_words(tweet)
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
        for x in TweetAnalyzer.tweet_words(tweet):
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
