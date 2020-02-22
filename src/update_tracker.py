import os
import re
from collections import defaultdict

import feedparser
import numpy as np
import pandas as pd

def clean_text(x):
    x = x.lower()
    x = re.sub(r'([^\s\w]|_)+', '', x) # remove all non-alpha numeric but space
    x = x.replace("  ", "_")
    x = x.replace(" ", "_")
    return x

def refresh_jre_data(rss_url):
    """Get fresh data from rss feed
    
    Parameters
    ----------
    rss_url : [type]
        [description]
    
    Returns
    -------
    [type]
        [description]
    """    
    data = defaultdict(list)
    jre_rss = feedparser.parse(rss_url)
    for i in jre_rss.entries:
        data["id"].append(i["id"])
        data["title"].append(i["title"])
        data["url"].append(i["link"])
        data["published"].append(i["published"])
        data["summary"].append(i["summary"])
        data["transcription_created"] = np.NaN
        # >>> jre_rss.entries[0].keys()
        # dict_keys(['title', 'title_detail', 'published', 'published_parsed', 'id',
        # 'guidislink', 'links', 'link', 'image', 'summary', 'summary_detail', 'content',
        # 'itunes_duration', 'itunes_explicit', 'tags', 'subtitle', 'subtitle_detail',
        # 'itunes_episode', 'itunes_episodetype'])
    df = pd.DataFrame(data=data)
    df["published"] = pd.to_datetime(df["published"])
    df["year"] = df["published"].apply(lambda x: str(x.year))
    df["month"] = df["published"].apply(lambda x: str(x.month).zfill(2))
    df["day"] = df["published"].apply(lambda x: str(x.day).zfill(2))
    df["date"] = df["year"] + "-" + df["month"] + "-" + df["day"]
    df["out_tag"] = df["date"] + "_" + df["title"].apply(clean_text)
    
    return df

def update_jre_tracker(df, episode_tracker_path):
    """Update the tracker file with newest data from RSS feed
    
    Parameters
    ----------
    df : [type]
        [description]
    episode_tracker_path : [type]
        [description]
    
    Returns
    -------
    [type]
        [description]
    """
    if not os.path.exists(episode_tracker_path):
        print("creating new tracker...")
        df.to_csv(episode_tracker_path, index=False)
        df["transcription_created"] = False
    else:
        print("tracker already exists, updating with latest rss info...")
        df_old = pd.read_csv(episode_tracker_path)

        # merge existing tracker with updated data
        df = pd.merge(
            left=df.drop(columns=["transcription_created"]), 
            right=df_old[["id", "transcription_created"]],
            on="id",
            how="left"
        )
        # replace np.NaN with False
        df["transcription_created"] = df["transcription_created"].fillna(value=False)
    
    return df

##############################################
# MAIN
##############################################
rss_url = "http://joeroganexp.joerogan.libsynpro.com/rss"
episode_tracker_path = "data/episode_tracker.csv"

df = refresh_jre_data(rss_url)
df = update_jre_tracker(df, episode_tracker_path)
df.to_csv(episode_tracker_path, index=False)
