import pandas as pd
from datetime import datetime

def getHourFromDate(date):
    hour = ""
    try:
        d = datetime.strptime(date, "%Y-%m-%d %H:%M:%S%z")
        hour = str(d.hour)
    except:
        # print('Error processing row')
        hour = "-1"
    return hour

def getDate(date):
    hour = ""
    try:
        d = datetime.strptime(date, "%Y-%m-%d")
        date = str(d)
    except:
        # print('Error processing row')
        date = "-1"
    return date

#Schema -> date,id,content,username,like_count,retweet_count

tweet_data = pd.read_csv('archive\Twitter_Jan_Mar.csv')

#Get top 10 liked and retweeted tweets

tweet_data['like_rank'] = tweet_data['like_count'].rank(ascending=False)
tweet_data['retweet_rank'] = tweet_data['retweet_count'].rank(ascending=False)

print('Top 10 liked tweets:')
print(tweet_data[tweet_data['like_rank']<=10][['content', 'like_count']].to_string(index=False))

print('Top 10 retweeted tweets:')
print(tweet_data[tweet_data['retweet_rank']<=10][['content', 'retweet_count']].to_string(index=False))

#Get top 10 active users

print('Top 10 active users based on tweet posted:')
tweet_data_user = tweet_data.groupby(['username'])['id'].count().reset_index(name='tweet_count')
print(tweet_data_user.sort_values('tweet_count', ascending=False).head(10).to_string(index=False))

# Get top active days and hours by tweet volume

# tweet_data['time'] = tweet_data.apply(lambda x : x['date'].split()[1].split('+')[0].split(':')[0]+"00 HRS", axis=1)
tweet_data['time'] = tweet_data.apply(lambda x : getHourFromDate(x['date'])+"00 HRS", axis=1)
tweet_data['date'] = tweet_data.apply(lambda x : x['date'].split()[0], axis=1)

print('Top 10 active days based on tweet volume:')
tweet_data_day = tweet_data.groupby('date')['id'].count().reset_index(name='tweet_count')
print(tweet_data_day.sort_values('tweet_count', ascending=False).head(10).to_string(index=False))

print('Top 10 active hours based on tweet volume:')
tweet_data_hour = tweet_data.groupby('time')['id'].count().reset_index(name='tweet_count')
print(tweet_data_hour.sort_values('tweet_count', ascending=False).head(10).to_string(index=False))

#Average word length of tweets

print('Average word length of the posted tweets:')
tweet_data['word_cnt'] = tweet_data.apply(lambda x : len(str(x['content']).split()), axis=1)
print(tweet_data['word_cnt'].mean())
# print(tweet_data.sort_values('word_cnt', ascending=False).head(10).to_string(index=False))

