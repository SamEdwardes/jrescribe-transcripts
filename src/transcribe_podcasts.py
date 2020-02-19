import requests
import feedparser
import pandas as pd
import urllib.request
import pydub
import speech_recognition as sr

from collections import defaultdict

rss_url = "http://joeroganexp.joerogan.libsynpro.com/rss"
jre_rss = feedparser.parse(rss_url)

data = defaultdict(list)

limit = 5
count = 0
for i in jre_rss.entries:
    count += 1
    if count > limit:
        break
    data["id"].append(i["id"])
    data["title"].append(i["title"])
    data["url"].append(i["link"])
    # >>> jre_rss.entries[0].keys()
    # dict_keys(['title', 'title_detail', 'published', 'published_parsed', 'id', 
    # 'guidislink', 'links', 'link', 'image', 'summary', 'summary_detail', 'content', 
    # 'itunes_duration', 'itunes_explicit', 'tags', 'subtitle', 'subtitle_detail', 
    # 'itunes_episode', 'itunes_episodetype'])


data = pd.DataFrame(data=data)
print(data)

# download episodes
urllib.request.urlretrieve(data.loc[0, "url"], "data/audio/test.mp3")
# convert wav to mp3                                                            
mp3 = pydub.AudioSegment.from_mp3("data/audio/jre_test_clip.mp3")
mp3.export("data/audio/jre_test_clip.wav", format="wav")


# create transcript
r = sr.Recognizer()
podcast_file = sr.AudioFile('data/audio/jre_test_clip.wav')
with podcast_file as source:
    audio = r.record(source)
trans = r.recognize_google(audio)
print(trans)



