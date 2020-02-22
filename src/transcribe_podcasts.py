import glob
import os
import urllib.request
from collections import defaultdict
from datetime import datetime

import numpy as np
import pandas as pd
import pydub
import speech_recognition as sr


def download_episode(url, out_tag):
    mp3_out = "data/audio/" + out_tag + ".mp3"
    if not os.path.exists(mp3_out):
        print("downloading: " + mp3_out)
        urllib.request.urlretrieve(url, mp3_out)
    else:
        print("already downloaded: " + mp3_out)

    return None


def convert_mp3_to_wav(out_tag, clip_length_seconds=60):
    mp3_in = "data/audio/" + out_tag + ".mp3"
    wav_out = "data/audio/" + out_tag
    print("converting mp3 to wav: " + wav_out)

    # divide audio into chunks
    audio = pydub.AudioSegment.from_mp3(mp3_in)
    audio_duration = audio.duration_seconds
    chunk_size = clip_length_seconds
    num_chunks = int(np.ceil(audio_duration / chunk_size))
    for i in range(0, num_chunks):
        iteration = str(i + 1).zfill(3)
        print("\t iteration: " + iteration)
        start_ms = (i * chunk_size) * 1000  # convert to milliseconds
        end_ms = min(audio_duration, (i + 1) * chunk_size) * \
            1000  # convert to milliseconds
        audio[start_ms: end_ms].export(
            wav_out + f"_{iteration}.wav", format="wav", bitrate="64k")

    return None

def transcribe_episode(out_tag, start_seconds=None, duration_seconds=None):
    # transcribe audio to text
    print("transcribing file: " + out_tag)
    transcript_out = "data/transcripts/" + out_tag
    wav_path = "data/audio/" + out_tag
    trans_list = []
    r = sr.Recognizer()
    iteration = 1
    to_do = glob.glob(wav_path + "*.wav")
    to_do.sort()
    for i in to_do:
        iteration_str = str(iteration).zfill(3)
        print("\t iteration: " + i)
        podcast_file = sr.AudioFile(i)
        with podcast_file as source:
            audio = r.record(source, offset=start_seconds,
                             duration=duration_seconds)
        trans = r.recognize_sphinx(audio)
        trans_list.append("")
        trans_list.append(trans)
        # write intermediate results to disk
        text_file = open(transcript_out + "_" + iteration_str + ".txt", "w")
        text_file.write(trans)
        text_file.close()
        # delete wav file
        os.remove(i)
        iteration += 1

    # write results to disk
    text_file = open(transcript_out + ".txt", "w")
    text_file.write("\n".join(trans_list))
    text_file.close()

    return trans_list



##############################################
# MAIN
##############################################
episode_tracker_path = "data/episode_tracker.csv"
df = pd.read_csv(episode_tracker_path)

for i in range(1, 2):
    start_time = datetime.now()
    out_tag = df.loc[i, "out_tag"]
    url = df.loc[i, "url"]
    print("\n" + "#"  * 32 + "\n" + out_tag + "\n" + "#" * 32)
    if df.loc[i, "transcription_created"] == False:
        download_episode(url, out_tag)
        convert_mp3_to_wav(out_tag, clip_length_seconds=120)
        transcribe_episode(out_tag, start_seconds=None, duration_seconds=None)
        df.loc[i, "transcription_created"] = True
        df.to_csv(episode_tracker_path, index=False)
        os.remove("data/audio/" + out_tag + ".mp3")
    else:
        print("already transcribed: " + out_tag)
    end_time = datetime.now()
    print(f"Total time: {end_time - start_time}")
    print("COMPLETE!")


##############################################
# TESTING
##############################################
# try on short clip ----
# convert_mp3_to_wav("jre_test_clip")
# transcribe_episode("jre_test_clip")

# download and test on long clip ----
# download_episode(df.loc[2, "url"], df.loc[2, "out_tag"])
# transcribe_episode(df.loc[2, "out_tag"])
