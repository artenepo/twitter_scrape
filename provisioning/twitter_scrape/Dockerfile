FROM python:3.6.2

WORKDIR /mnt/src
# because docker caches each new line of command, we should add new packages one per new line to avoid long image rebuilds
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y nano git

RUN pip install flask==0.12.2
RUN pip install gunicorn==19.7.1
RUN pip install requests==2.13.0
RUN pip install beautifulsoup4==4.4.1

# for python testing purposes
RUN pip install \
    httpie \
    ipython \
    nose \
    pinocchio \
    honcho

ADD start_server.sh /mnt/start_server.sh

VOLUME ["/var/log/"]
VOLUME ["/mnt/src/"]
CMD ["/mnt/start_server.sh"]
