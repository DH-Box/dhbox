FROM phusion/baseimage:0.9.16
MAINTAINER Steve

# Set correct environment variables.
ENV HOME /root
ENV DEBIAN_FRONTEND noninteractive

ENV REFRESHED_AT 2016-01-09

RUN echo "deb http://cran.rstudio.com/bin/linux/ubuntu trusty/" >> /etc/apt/sources.list
RUN apt-get -y update

# General needs
RUN apt-get -qy install emacs git python-apt apt-utils python-pip python3-pip python-dev python3-dev sudo curl git wget unzip python-pip opensmtpd ipython-notebook nodejs npm python3-scipy python3-pandas python3-matplotlib python3-numpy
RUN pip install PyYAML jinja2 paramiko


# For Shellinabox
RUN apt-get -qy install libssl-dev libpam0g-dev zlib1g-dev dh-autoreconf automake autoconf build-essential
RUN git clone https://github.com/shellinabox/shellinabox.git
WORKDIR /shellinabox
RUN ls -l
RUN autoreconf -i
RUN ./configure && make && make install
ADD ./shellinabox /etc/default/
WORKDIR /

# For MALLET
RUN apt-get -qy install default-jdk ant
RUN mkdir /mallet
RUN wget -O /tmp/mallet.tar.gz http://mallet.cs.umass.edu/dist/mallet-2.0.7.tar.gz
RUN tar xfz /tmp/mallet.tar.gz --strip-components=1 -C /mallet
RUN ant -buildfile /mallet/build.xml

# For Jupyter
RUN pip3 install jupyter
RUN add-apt-repository ppa:chris-lea/zeromq
RUN apt-get update
RUN apt-get -qy --force-yes install libzmq3-dbg libzmq3-dev libzmq3 littler
# Set default CRAN repo
RUN echo 'options("repos"="http://cran.rstudio.com")' >> /usr/lib/R/etc/Rprofile.site
# Install IRkernel
RUN Rscript -e "install.packages(c('rzmq','repr','IRkernel','IRdisplay'), repos = c('http://irkernel.github.io/', getOption('repos')))" -e "IRkernel::installspec()"


# For NLTK
RUN apt-get -qy install python-numpy python-scipy python-matplotlib
RUN pip install NLTK

# For R-Studio
RUN apt-get -qy --force-yes install r-base r-base-dev gdebi-core libatlas3-base libapparmor1 apparmor-profiles libssl0.9.8
RUN wget http://download2.rstudio.org/rstudio-server-0.98.501-amd64.deb -O rstudio.deb
RUN yes | gdebi rstudio.deb
RUN ln -s /etc/apparmor.d/rstudio-server /etc/apparmor.d/disable/

# For Omeka
RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd
RUN apt-get -qy install apache2 php5 rsync mysql-server php5-mysql imagemagick python-mysqldb
RUN mkdir -p /var/www/omeka/
RUN wget -O /tmp/omeka.zip http://omeka.org/files/omeka-2.3.zip
RUN unzip -qo /tmp/omeka.zip -d /var/www/omeka/
RUN cp -r /var/www/omeka/omeka-2.3/* /var/www/omeka/
RUN cp -r /var/www/omeka/omeka-2.3/.htaccess /var/www/omeka/
RUN rm -rf /var/www/omeka/omeka-2.3/
RUN chown -R www-data /var/www
RUN chgrp -R www-data /var/www
RUN echo "cgi.fix_pathinfo=0" > etc/php5/apache2/conf.d/10-fix_pathinfo.ini
RUN /usr/sbin/mysqld & \
    sleep 10s &&\
    echo "CREATE USER 'omeka'@'localhost' IDENTIFIED BY 'omeka';" | mysql &&\
    echo "CREATE USER 'omeka'@'%' IDENTIFIED BY 'omeka';" | mysql &&\
    echo "CREATE DATABASE omeka CHARACTER SET='utf8' COLLATE='utf8_unicode_ci';" | mysql &&\
    echo "GRANT ALL PRIVILEGES ON omeka.* TO 'omeka'@'localhost';" | mysql &&\
    echo "GRANT ALL PRIVILEGES ON omeka.* TO 'omeka'@'%';" | mysql

ADD ./omeka/omeka.conf /etc/apache2/sites-available/000-omeka.conf
RUN a2ensite 000-omeka.conf
RUN a2enmod rewrite
ADD ./omeka/db.ini /var/www/omeka/
RUN chmod 0666 /var/www/omeka/db.ini
ADD ./omeka/config.ini /var/www/omeka/application/config/config.ini
ADD ./omeka/htaccess /var/www/omeka/.htaccess
RUN chmod -R 777 /var/www/omeka/files

# For brackets
RUN apt-get install -qy nodejs nodejs-legacy npm
RUN npm install brackets -g

# Adding Deamons to containers
RUN mkdir -p /etc/service/rserver
ADD ./runit_scripts/rserver.sh /etc/service/rserver/run
RUN chmod +x /etc/service/rserver/run

RUN mkdir -p /etc/service/mysql
ADD ./runit_scripts/mysql.sh /etc/service/mysql/run
RUN chmod +x /etc/service/mysql/run

RUN mkdir -p /etc/service/apache2
ADD ./runit_scripts/apache2.sh /etc/service/apache2/run
RUN chmod +x /etc/service/apache2/run

RUN mkdir -p /etc/service/shellinabox
ADD ./runit_scripts/shellinabox.sh /etc/service/shellinabox/run
RUN chmod +x /etc/service/shellinabox/run

RUN mkdir -p /etc/service/smtpd
ADD ./runit_scripts/smtpd.sh /etc/service/smtpd/run
RUN chmod +x /etc/service/smtpd/run

RUN mkdir -p /etc/service/brackets
ADD ./runit_scripts/brackets.sh /etc/service/brackets/run
RUN chmod +x /etc/service/brackets/run

RUN mkdir -p /etc/service/notebook
ADD ./runit_scripts/notebook.sh /etc/service/notebook/run
RUN chmod +x /etc/service/notebook/run

##startup scripts
#ENV HEY hey
RUN mkdir -p /etc/my_init.d
ADD ./runit_scripts/startup.sh /etc/my_init.d/startup.sh
RUN chmod +x /etc/my_init.d/startup.sh

EXPOSE 22 25 8787 80 4200 8888

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]
