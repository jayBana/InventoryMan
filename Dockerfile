FROM ubuntu:14.04
MAINTAINER Janos Bana <janosbana@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update
RUN apt-get install -y vim python3 python3-pip nginx supervisor

# Setup Flask application
RUN pip3 install --upgrade pip
RUN pip3 install virtualenv virtualenvwrapper
RUN mkdir -p /home/www/G53IDS && cd /home/www/G53IDS
COPY G53IDS /home/www/G53IDS
RUN mkdir -p ~/.virtualenvs
ENV WORKON_HOME=~/.virtualenvs \
    VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3 \
    VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv

RUN echo "WORKON_HOME=~/.virtualenvs" >> ~/.bashrc \
    && echo "VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc \
    && echo "VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv" >> ~/.bashrc \
    && echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

RUN source /usr/local/bin/virtualenvwrapper.sh \
    && mkvirtualenv -p /usr/bin/python3 env-g53ids \
    && pip3 install --upgrade pip \
    && pip3 install -Ur /home/www/G53IDS/requirements-flask.txt

# Setup nginx
RUN rm /etc/nginx/sites-enabled/default
RUN cp /home/www/G53IDS/.config/flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Setup supervisord
RUN mkdir -p /var/log/supervisor
RUN cp /home/www/G53IDS/.config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN cp /home/www/G53IDS/.config/gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

# Start processes
CMD /bin/bash -c "source /home/www/G53IDS/.config/start_server.sh"
