from snscrape.modules import twitter
import json
import re
from datetime import date
import pandas

# Define a list of offensive words
offensive_words = ['lan', 'amk', 'aq', 'sikeyim', 'sokayım', 'sg', 'siktir', 'mq']

# Define the keywords/hashtags
queries = ["YÖK", "üniversite", "uzaktan" ,"uzaktanegitim", "online", "onlineegitim", "yuzyuze", "yuzyuzeegitim"]

# Define how many data will be got
maxResult = 100

# Scrapping Operation
def scrapeSearch(query, since, until):
    scraper = twitter.TwitterSearchScraper(query + ' since:' + since.strftime('%Y-%m-%d') + ' until:' + until.strftime('%Y-%m-%d'))
    return scraper

# Define the date range
since = date(2023, 2, 11)
until = date(2023, 2, 18)

# The data will be added to this list first. Then it will be ported to Excel with Pandas module.
tweetDataList = []

for query in queries:
    scraper = scrapeSearch(query, since, until)
    counter = 0
    for i, tweet in enumerate(scraper.get_items(), start=1):
        tweetURL = f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
        tweetJSON = json.loads(tweet.json())
        tweet_text = tweetJSON['renderedContent']

        # User name
        user_name = tweet.user.username
        # Date of tweeted
        tweet_date = tweet.date.strftime("%Y-%m-%d %H:%M:%S")
        # How many likes
        like_count = tweet.likeCount
        # How many retweets
        retweet_count = tweet.retweetCount
        # How many followers
        follower_count = tweet.user.followersCount
        # How many following
        following_count = tweet.user.friendsCount

        # Check if tweet contains any offensive words
        if any(re.search(r'\b{}\b'.format(word), tweet_text, re.IGNORECASE) for word in offensive_words):
            continue
        else:
            try:
                # If not exist offensive_words in the tweets;
                # Add to the tweetDataList the tweets.
                tweetDataList.append([counter, user_name, tweet_date, like_count, retweet_count, follower_count, following_count, tweetURL, tweet_text])
                # Increment the counter
                counter += 1
                print("*************************************************************")
                print(counter)
                print("*************************************************************")
                # Define your columns of Excel by tweetDataList
                dataframe = pandas.DataFrame(tweetDataList, columns=["Tweet ID", "Kullanıcı Adı", "Tarih", "Beğeni Sayısı", "Retweet Sayısı", "Takipçi Sayısı", "Takip Edilenlerin Sayısı", "Tweet URL Adresi", "Tweet İçeriği"])
                # Add the data to Excel with 'index=False'. Because we defined a counter already.
                dataframe.to_excel("tweetsForThesis.xlsx", index=False)
                print(tweetDataList)

            except PermissionError:
                # Send an error message if the Excel file already exists.
                print("[!] HATA: Aynı isimde bir dosyanız bulunuyor olabilir.")
                break
        
        # If the counter equals the maximum number of data received break the loop
        if counter == maxResult:
            print("[*] Maksimum veri sayısına ulaşıldı.")
            break
    # And the big loop too.
    break
