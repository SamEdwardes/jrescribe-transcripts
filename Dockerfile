# author: Sam Edwardes
# date: 2020-02-04
# BUILD:
#   docker build --tag jrescribetranscripts .
# RUN CONTAINER AND OPEN BASH:
#   docker run -it --rm jrescribetranscripts
# RUN AND ATTACH DIR:
# docker run -it --rm -v $(pwd):/root/jre jrescribetranscripts
FROM ubuntu

# basic set up
RUN apt-get update
RUN apt-get install tree
RUN apt-get install -y python3.7 python-dev python3-pip build-essential swig git libpulse-dev

# more python packages
RUN pip3 install --no-cache-dir pandas

# POCKETSPHINX
# https://pypi.org/project/pocketsphinx/
RUN apt-get install -y libasound2-dev
RUN pip3 install --upgrade --no-cache-dir pocketsphinx
RUN pip3 install SpeechRecognition
RUN pip3 install pydub
RUN apt-get install -y ffmpeg

# more python packages
RUN pip3 install --no-cache-dir feedparser


# REFERENCE
# https://gist.github.com/AlekseiCherkes/8e8b9cd2dd22cceb77a0#file-dockerfile-sphinx
# https://github.com/greghesp/assistant-relay/issues/49
