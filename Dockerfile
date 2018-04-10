FROM python:3

MAINTAINER Dockerfiles

# Upgrade pip to the newest version

RUN pip3 install -U pip

# to prevent re-installing (all your) dependencies when you made a change a line or two in your app.
COPY requirements/production.txt /home/docker/code/
COPY requirements/base.txt /home/docker/code/

# Install all the dependecies and libraries needed for the production mode
RUN pip3 install -r /home/docker/code/production.txt

# add (the rest of) our code
COPY . /home/docker/code/

# set the work directory
WORKDIR /home/docker/code/

# setting the listing port for the container
EXPOSE 443