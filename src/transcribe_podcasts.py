import pandas as pd
import urllib.request
import pydub
import speech_recognition as sr
from datetime import datetime

from collections import defaultdict

# read in tracker
df = pd.read_csv("data/episode_tracker.csv")
df["published"] = pd.to_datetime(df["published"])

# add in extra metadata
df["year"] = df["published"].apply(lambda x: str(x.year))
df["month"] = df["published"].apply(lambda x: str(x.month).zfill(2))
df["day"] = df["published"].apply(lambda x: str(x.day).zfill(2))
df["date"] = df["year"] + "-" + df["month"] + "-" + df["day"]
df["out_tag"] = df["date"] + "__" + df["title"].apply(lambda x: x.lower().replace(" ", "_"))
df["out_tag"] = df["out_tag"].apply(lambda x: x.replace("#", ""))


def download_episode(url, out_tag):
    # download episode
    mp3_out = "data/audio/" + out_tag + ".mp3"
    print("downloading: " + mp3_out)
    urllib.request.urlretrieve(url, mp3_out)
    # convert mp3 to wav
    wav_out = "data/audio/" + out_tag + ".wav"
    print("converting mp3 to wav: " + wav_out)
    mp3 = pydub.AudioSegment.from_mp3(mp3_out)
    mp3.export(wav_out, format="wav")
    return None


def transcribe_episode(out_tag):
    # transcribe audio to text
    transcript_out = "data/transcripts/" + out_tag + ".txt"
    r = sr.Recognizer()
    podcast_file = sr.AudioFile("data/audio/" + out_tag + ".wav")
    print("recording audio file...")
    with podcast_file as source:
        audio = r.record(source)
    print("transcribing audio file...")
    trans = r.recognize_google(audio)
    # write results to disk
    print("writing transcription to disk...")
    text_file = open(transcript_out, "w")
    text_file.write(trans)
    text_file.close()
    return trans


# testing
# download_episode(df.loc[0, "url"], df.loc[0, "out_tag"])
# transcribe_episode("jre_test_clip")
transcribe_episode(df.loc[0, "out_tag"])
