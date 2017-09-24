"""
7/22/2017
@author: Matthew Bird
name    house_gather
"""

import re
import time

import praw
import requests.auth


def get_urls(subreddit, settings, count, time_filter):
    client_auth = requests.auth.HTTPBasicAuth(settings['client_id'], settings['secret'])
    post_data = {"grant_type": "password", "username": settings['reddit_username'],
                 "password": settings['reddit_password']}
    headers = {"User-Agent": "ChangeMeClient/0.1 by " + settings['reddit_username']}

    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data,
                             headers=headers)
    response_json = response.json()
    time.sleep(.2)

    headers = {"Authorization": response_json['token_type'] + ' ' + response_json['access_token'],
               "User-Agent": "ChangeMeClient/0.1 by " + settings['reddit_username']}
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)

    reddit = praw.Reddit(client_id=settings['client_id'],
                         client_secret=settings['secret'],
                         user_agent="ChangeMeClient/0.1 by " + settings['reddit_username'])
    urls = []
    for submission in reddit.subreddit(subreddit).top(limit=count, time_filter=time_filter):
        try:
            url = str(submission.url)
            line = re.sub('[.]', '', url)
            if 'youtube' in line.lower() and 'playlist' not in line.lower():
                urls.append(url)
        except:
            print('youtube url no good')
    return urls


if __name__ == '__main__':
    print get_urls('house', count=10)
