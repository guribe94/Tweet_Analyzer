import Tkinter
import tkFileDialog
import TweetAnalyzer
import tkMessageBox


class TweetAnalyzerGUI:
    def __init__(self):

        # Create the main window.
        self.main_window = Tkinter.Tk()
        self.main_window.title("Tweet Analyzer")

        # Create frames for the groups of widgets.
        self.input_frame = Tkinter.Frame(self.main_window)
        self.output_frame = Tkinter.Frame(self.main_window)
        self.filter_frame = Tkinter.Frame(self.main_window)
        self.positive_negative_frame = Tkinter.Frame(self.main_window)
        self.button_frame = Tkinter.Frame(self.main_window)

        #Get the location of the input file
        self.tweet_input_label = \
            Tkinter.Label(self.input_frame,text="Enter a file of tweets to be"
                                                " analyzed:")
        self.tweet_input_button = Tkinter.Button(self.input_frame,
                                                 text="Choose a file",
                                                 command=self.get_input_file)
        self.sentiment_input_label = Tkinter.Label(self.input_frame,
                                                   text="Enter a file of "
                                                        "sentiment values to"
                                                        " use:")
        self.sentiment_input_button = Tkinter.Button(self.input_frame,
                                                     text="Choose a file",
                                                     command=
                                                     self.get_sentiments_file)
        self.tweet_input_label.pack(side='left')
        self.tweet_input_button.pack(side='left')
        self.sentiment_input_label.pack(side='left')
        self.sentiment_input_button.pack(side='left')

        #Get the location of the output file
        self.output_label = Tkinter.Label(self.output_frame,
                                          text="Enter a location for analyzed"
                                               " tweets to be stored:")
        self.output_button = Tkinter.Button(self.output_frame,
                                            text="Choose an output file",
                                            command=self.get_output_file)
        self.output_label.pack(side='left')
        self.output_button.pack(side='left')
        #State filter
        self.state_filter_label = Tkinter.Label(self.filter_frame,
                                                text='Enter a two letter state'
                                                     ' abbreviation to filter by:')
        self.state_filter_entry = Tkinter.Entry(self.filter_frame, width=10)

        self.state_filter_label.pack(side='left')
        self.state_filter_entry.pack(side='left')
        #Zip code filter
        self.zip_filter_label = Tkinter.Label(self.filter_frame,
                                              text='Enter a zip code to filter'
                                                   ' by:')
        self.zip_filter_entry = Tkinter.Entry(self.filter_frame, width=10)

        self.zip_filter_label.pack(side='left')
        self.zip_filter_entry.pack(side='left')
        #Text filter
        self.text_filter_label = Tkinter.Label(self.filter_frame,
                                               text='Enter text to filter by:')
        self.text_filter_entry = Tkinter.Entry(self.filter_frame, width=10)

        self.text_filter_label.pack(side='left')
        self.text_filter_entry.pack(side='left')

        #Most positive and most negative sentiment
        self.positive_negative_label = Tkinter.Label(
            self.positive_negative_frame,text="Enter a word to find which "
                                              "states have most positive and"
                                              " negative sentiments:")
        self.positive_negative_entry = Tkinter.Entry(
            self.positive_negative_frame, width=10)

        self.positive_negative_label.pack(side='left')
        self.positive_negative_entry.pack(side='left')

        # Create and pack the button widgets.
        self.analyze_tweets_button = Tkinter.Button(self.button_frame,
                                                    text='Analyze Tweets',
                                                    command=self.analyze)
        self.find_positive_negative_button = Tkinter.Button(
            self.button_frame,text='Find State With Most Positive and '
                                   'Negative Sentiment',
            command=self.find_positive_negative)
        self.quit_button = Tkinter.Button(self.button_frame, text='Quit',
                                          command=self.main_window.quit)
        self.analyze_tweets_button.pack(side='left')
        self.find_positive_negative_button.pack(side='left')
        self.quit_button.pack(side='left')

        # Pack the frames.
        self.input_frame.pack()
        self.output_frame.pack()
        self.filter_frame.pack()
        self.positive_negative_frame.pack()
        self.button_frame.pack()

        # Start the main loop.
        Tkinter.mainloop()

    def get_input_file(self):
        #Save the path of the input file given
        self.tweet_input_filename = tkFileDialog.askopenfilename()

    def get_sentiments_file(self):
        #Save the path of the sentiments file given
        self.sentiments_input_filename = tkFileDialog.askopenfilename()

    def get_output_file(self):
        #Save the path of the output file given
        self.outfile = tkFileDialog.asksaveasfilename()

    def analyze(self):
        #Open the file given
        f = open(self.tweet_input_filename, 'r')
        tweets = []
        #Create a dictionary of sentiments and values from the given file
        sentiments = TweetAnalyzer.create_sentiment_database(
            self.sentiments_input_filename)
        # Make the array of tweets
        for line in f:
            tweet = TweetAnalyzer.make_tweet(line)
            tweets.append(tweet)
        # Add the geographic information to the tweets
        tweets = TweetAnalyzer.add_geo(tweets)
        tweets = TweetAnalyzer.assign_sentiments(tweets, sentiments)

        #Check to see what filters to apply...only apply filter if something is typed in the entry box
        if len(self.state_filter_entry.get()) > 0:
            tweets = TweetAnalyzer.find_tweets_from_state(
                self.state_filter_entry.get(), tweets)

        if len(self.zip_filter_entry.get()) > 0:
            tweets = TweetAnalyzer.find_tweets_from_zip(
                self.state_filter_entry.get(), tweets)

        if len(self.text_filter_entry.get()) > 0:
            tweets = TweetAnalyzer.find_tweets_containing(
                self.text_filter_entry.get(), tweets)

        #Write the analyzed tweets to a file
        TweetAnalyzer.write_tweets(tweets, self.outfile)

        #Tell user it completed successfully
        tkMessageBox.showinfo("Operation completed",
                              "Tweets analyzed successfully. Check output file"
                              " for results.")

    def find_positive_negative(self):
        #Open the given file
        f = open(self.tweet_input_filename, 'r')
        tweets = []
        #Create a dictionary of sentiments and values from the given file
        sentiments = TweetAnalyzer.create_sentiment_database(
            self.sentiments_input_filename)
        # Make the array of tweets
        for line in f:
            tweet = TweetAnalyzer.make_tweet(line)
            tweets.append(tweet)
        # Add the geographic information to the tweets
        tweets = TweetAnalyzer.add_geo(tweets)
        tweets = TweetAnalyzer.assign_sentiments(tweets, sentiments)

        #Check to see what filters to apply...only apply filter if something is typed in the entry box
        if len(self.state_filter_entry.get()) > 0:
            tweets = TweetAnalyzer.find_tweets_from_state(
                self.state_filter_entry.get(), tweets)

        if len(self.zip_filter_entry.get()) > 0:
            tweets = TweetAnalyzer.find_tweets_from_zip(
                self.state_filter_entry.get(), tweets)

        if len(self.text_filter_entry.get()) > 0:
            tweets = TweetAnalyzer.find_tweets_containing(
                self.text_filter_entry.get(), tweets)

        #Get the most positive, negative and average sentiment
        positive_state = \
            TweetAnalyzer.most_positive(tweets,
                                        self.positive_negative_entry.get())
        negative_state = \
            TweetAnalyzer.most_negative(tweets,
                                        self.positive_negative_entry.get())
        avg_sentiment = TweetAnalyzer.find_average_sentiment(tweets)

        #Display what is found to the user
        tkMessageBox.showinfo("Operation completed",
                              "Tweets analyzed successfully. "
                              "\nState with most positive sentiment: " + str(
                                  positive_state) + "\nState with most "
                                                    "negative sentiment: " +
                              str(negative_state) + "\nAverage sentiment: "
                              + str(avg_sentiment))

# Create an instance of the TweetAnalyzerGUI class.
analyzer = TweetAnalyzerGUI()
