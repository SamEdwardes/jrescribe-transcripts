# Joe Rogan Experience Transcripts

Python program to automatically transcribe Joe Rogan Experience (JRE) podcasts (http://podcasts.joerogan.net/).

## Background

Inspired by https://github.com/achendrick/jrescribe-transcripts.

## How to use

The program works by:

1. Updating RSS feed data to track all JRE podcasts
2. Downloading podcast in a `.mp3` format
3. Breaking the `.mp3` file into smaller chunks and converting to `.wav` format
4. For each chunk, a transcript is created using the [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) package and [CMUSphinx](https://cmusphinx.github.io/wiki/)

#### Using CMUSphinx

I found CMUSphinx tricky to set up on my computer. Many dependencies are required. To simplify things and avoid downloading extra programs to my computer I used Docker to create an isolated environment. I recommend using my [Dockerfile](Dockerfile) instead of trying to download everything to save yourself and your computer trouble shooting pain!

## References

- https://github.com/achendrick/jrescribe-transcripts
- https://realpython.com/python-speech-recognition/
