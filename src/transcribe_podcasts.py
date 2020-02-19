import pandas as pd
import urllib.request
import pydub
import speech_recognition as sr
from datetime import datetime

from collections import defaultdict

df = pd.read_csv("data/episode_tracker.csv")
df["published"] = pd.to_datetime(df["published"])

meta = podcast_meta = df.iloc[0:3,:]
def download_episode(podcast_meta):
    # name files
    podcast_meta = df.iloc[0,:]
    year = str(podcast_meta["published"].year)
    month = str(podcast_meta["published"].month).zfill(2)
    day = str(podcast_meta["published"].day).zfill(2)
    date = year + "-" + month + "-" + day
    out_tag = date + "__" + podcast_meta["title"].lower().replace(" ", "_")

    # download episode
    mp3_out = "data/audio/" + out_tag + ".mp3"
    urllib.request.urlretrieve(podcast_meta["url"], mp3_out)

    # convert wav to mp3 
    wav_out = "data/audio/" + out_tag + ".wav"                                                          
    mp3 = pydub.AudioSegment.from_mp3(mp3_out)
    mp3.export(wav_out, format="wav")

    return None


def transcribe_episode():
    # create transcript
    transcript_out = "data/transcripts/" + out_tag + ".txt"
    r = sr.Recognizer()
    podcast_file = sr.AudioFile('data/audio/jre_test_clip.wav')
    with podcast_file as source:
        audio = r.record(source)
    trans = r.recognize_google(audio)
    print(trans)





