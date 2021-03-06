# Docker file for builing Celery application of Krypted 
# Usage: docker build --build-arg VERSION=master ./docker/celery/ 
FROM python:3.6
ARG VERSION

RUN apt-get update --no-install-recommends && \
    apt-get install --no-install-recommends -y \
    git=1:2.20.1-2+deb10u1 \
    bzip2=1.0.6-9.2~deb10u1 \ 
    wget=1.20.1-1.1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2

RUN adduser --disabled-password --gecos '' krypted

RUN git clone --branch $VERSION https://github.com/KryptedGaming/krypted.git /opt/krypted/ && \
    cp /opt/krypted/conf/settings.py.example /opt/krypted/app/app/settings.py && \
    pip3 install -r /opt/krypted/requirements.txt && \
    pip3 install mysqlclient==1.4.2.post1 && \ 
    pip3 install uwsgi==2.0.18

# COPY ENTRYPOINT
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
