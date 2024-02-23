FROM ubuntu:latest
Run rm /bin/sh && ln -s /bin/bash /bin/sh

Run apt update
Run apt install python3 python3-pip apache2 libapache2-mod-wsgi-py3 -y
Run a2dissite 000-default.conf

EXPOSE 80

COPY ./punch /var/www/html/punch
COPY ./punch.conf /etc/apache2/sites-enabled/punch.conf

RUN /bin/bash -c "chown -R :www-data /var/www/html/punch"
RUN /bin/bash -c "chmod -R 775 /var/www/html/punch"

WORKDIR /var/www/html/punch

RUN pip3 install virtualenv
RUN python3 -m virtualenv env
RUN /bin/bash -c "source /var/www/html/punch/env/bin/activate"

RUN /bin/bash -c "service apache2 start"

ENTRYPOINT ["/usr/sbin/apache2ctl"]

CMD ["-D", "FOREGROUND"]
