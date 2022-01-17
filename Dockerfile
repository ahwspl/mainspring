FROM ubuntu:20.04

MAINTAINER Darshit Kothari <darshit.kothari@ahwspl.com>

RUN apt-get update && apt-get install -y \
        software-properties-common
    RUN apt-get update && apt-get install -y \
        python3 \
        python3-pip
    RUN python3 -m pip install pip
    RUN apt-get update && apt-get install -y \
        python3-distutils \
        python3-setuptools \
        git
    RUN python3 -m pip install pip --upgrade pip
RUN apt-get install net-tools && apt-get install curl
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

RUN apt-get -qq update && \
    apt-get -qq install python3-virtualenv git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN virtualenv /mnt/scheduler && \
    . /mnt/scheduler/bin/activate && \
    pip install -e git+https://github.com/ahwspl/mainspring.git#egg=mainspring && \
    pip install -r /mnt/scheduler/src/mainspring/simple_scheduler/requirements.txt
#
#ADD simple_scheduler/docker/apns.pem /mnt/scheduler/
ADD simple_scheduler/docker/run_scheduler /mnt/scheduler/bin/run_scheduler
RUN chmod 755 /mnt/scheduler/bin/run_scheduler

CMD ["/mnt/scheduler/bin/run_scheduler"]