from snscrape.modules import twitter
import json
import re
from datetime import date
import pandas

# Define a list of offensive words
offensiveWords = {'lan', 'amk', 'aq', 'sikeyim', 'sokayım', 'sg', 'siktir', 'mq', "koyayım"}

# Define the keywords/hashtags
queries = {"YÖK", "üniversite", "uzaktan" ,"uzaktanegitim", "online", "onlineegitim", "yuzyuze", "yuzyuzeegitim"}

# Define how many data will be got
maxResult = 11000

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
    for i, tweet in enumerate(scraper.get_items(), start=1):
        tweetURL = f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
        tweetJSON = json.loads(tweet.json())
        tweet_text = tweetJSON['renderedContent']

        # Check if tweet contains any offensive words
        if any(re.search(r'\b{}\b'.format(word), tweet_text, re.IGNORECASE) for word in offensiveWords):
            continue
        else:
            # Get informations; username, date, likes, retweets, followers, following
            user_name = tweet.user.username
            tweet_date = tweet.date.strftime("%Y-%m-%d %H:%M:%S")
            like_count = tweet.likeCount
            retweet_count = tweet.retweetCount
            follower_count = tweet.user.followersCount
            following_count = tweet.user.friendsCount

            # If not exist offensive_words in the tweets, add to the tweetDataList the tweets.
            tweetDataList.append([i, user_name, tweet_date, like_count, retweet_count, follower_count, following_count, tweetURL, tweet_text])
            
            # Increment the counter
            i += 1
            print(i)

        # If the counter equals the maximum number of data received break the loop
        if i > maxResult:
            print("[*] Maksimum veri sayısına ulaşıldı.")
            # Create a data frame and define your columns of Excel by tweetDataList
            dataframe = pandas.DataFrame(tweetDataList, columns=["Tweet ID", "Kullanıcı Adı", "Tarih", "Beğeni Sayısı", "Retweet Sayısı", "Takipçi Sayısı", "Takip Edilenlerin Sayısı", "Tweet URL Adresi", "Tweet İçeriği"])
            # Add the data to Excel with 'index=False'. Because we defined a counter already.
            dataframe.to_excel("data.xlsx", index=False)
            print("[*] Veriler Excel dosyasına aktarıldı.")
            break
    break
