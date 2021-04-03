FROM ubuntu:18.04 as base

# set working directory
WORKDIR /usr/src/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive


# set project environment variables
# grab these via Python's os.environ
# these are 100% optional here
ENV AWS_ACCESS_KEY_ID abc123!
ENV AWS_SECRET_ACCESS_KEY 123abc!

# Install Ubuntu dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        libopencv-dev \
        build-essential \
        libssl-dev \
        libpq-dev \
        libcurl4-gnutls-dev \
        libexpat1-dev \
        gettext \
        unzip \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        gcc \
        g++ \
        ruby \
        bf \
        openjdk-8-jdk \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# install environment dependencies
RUN pip3 install --upgrade pip
RUN pip3 install psycopg2 pipenv

# Install project dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /usr/src/

CMD gunicorn owljudge.wsgi:application --bind 0.0.0.0:$PORT
