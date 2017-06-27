FROM phusion/baseimage:0.9.18
MAINTAINER Steve

# Set correct environment variables.
ENV HOME /root
ENV DEBIAN_FRONTEND noninteractive

ENV REFRESHED_AT 2017-03-09
RUN groupadd dhbox

# RUN echo "deb http://cran.rstudio.com/bin/linux/ubuntu trusty/" >> /etc/apt/sources.list
RUN apt-get -y update

# General needs
RUN curl -sL https://deb.nodesource.com/setup_5.x | sudo -E bash -
RUN apt-get -qy install emacs git python-apt apt-utils software-properties-common sudo curl wget unzip opensmtpd nodejs libssl-dev libpam0g-dev zlib1g-dev dh-autoreconf automake autoconf build-essential python3-pandas
# RUN apt-get install ipython-notebook python-pip python3-pip python-dev python3-dev python3-scipy python3-pandas python3-matplotlib python3-numpy
RUN pip install corpus-downloader

RUN wget https://repo.continuum.io/archive/Anaconda3-4.1.1-Linux-x86_64.sh -O /anaconda.sh
RUN bash /anaconda.sh -b -p /opt/anaconda 
ENV PATH /opt/anaconda/bin:$PATH
ADD ./conda.sh /etc/profile.d/conda.sh
RUN /opt/anaconda/bin/conda install pip
RUN /opt/anaconda/bin/pip install paramiko
RUN chmod 777 -R /opt/anaconda/

# For Wetty
RUN npm install -g wetty

WORKDIR /


# For MALLET
RUN apt-get -qy install default-jdk ant
RUN mkdir /mallet
RUN wget -O /tmp/mallet.tar.gz http://mallet.cs.umass.edu/dist/mallet-2.0.7.tar.gz
RUN tar xfz /tmp/mallet.tar.gz --strip-components=1 -C /mallet
RUN ant -buildfile /mallet/build.xml

# For Jupyter
# RUN pip3 install jupyter
# RUN add-apt-repository ppa:chris-lea/zeromq
# RUN apt-get update
# RUN apt-get -qy --force-yes install libzmq3-dbg libzmq3-dev libzmq3 littler
# # Set default CRAN repo
# RUN echo 'options("repos"="http://cran.rstudio.com")' >> /usr/lib/R/etc/Rprofile.site
# # Install IRkernel
# RUN Rscript -e "install.packages(c('rzmq','repr','IRkernel','IRdisplay'), repos = c('http://irkernel.github.io/', getOption('repos')))" -e "IRkernel::installspec()"

# For NLTK
# RUN apt-get -qy install python-numpy python-scipy python-matplotlib
# RUN pip install NLTK

# For R-Studio
RUN apt-get -qy --force-yes install r-base r-base-dev gdebi-core libatlas3-base libapparmor1 apparmor-profiles libssl0.9.8
RUN wget http://download2.rstudio.org/rstudio-server-0.98.501-amd64.deb -O rstudio.deb
RUN yes | gdebi rstudio.deb
RUN ln -s /etc/apparmor.d/rstudio-server /etc/apparmor.d/disable/

# For brackets
RUN npm install brackets -g
# RUN npm install -g grunt-cli
#     # npm install -g node-inspector
# RUN git clone https://github.com/rabchev/brackets-server.git
# WORKDIR /brackets-server
# RUN npm cache clean
# RUN npm update -g
# RUN git submodule update --init --recursive && \
#     npm install && \
#     grunt build
WORKDIR /
RUN apt-get -qy install apache2 mysql-server
# For the file manager
RUN npm install node-file-manager -g

# Adding Deamons to containers
RUN mkdir -p /etc/service/rserver
ADD ./runit_scripts/rserver.sh /etc/service/rserver/run
RUN chmod +x /etc/service/rserver/run

RUN mkdir -p /etc/service/mysql
ADD ./runit_scripts/mysql.sh /etc/service/mysql/run
RUN chmod +x /etc/service/mysql/run

RUN mkdir -p /etc/service/wetty
ADD ./runit_scripts/wetty.sh /etc/service/wetty/run
RUN chmod +x /etc/service/wetty/run

RUN mkdir -p /etc/service/apache2
ADD ./runit_scripts/apache2.sh /etc/service/apache2/run
RUN chmod +x /etc/service/apache2/run

RUN mkdir -p /etc/service/explorer
ADD ./runit_scripts/explorer.sh /etc/service/explorer/run
RUN chmod +x /etc/service/explorer/run

RUN mkdir -p /etc/service/smtpd
ADD ./runit_scripts/smtpd.sh /etc/service/smtpd/run
RUN chmod +x /etc/service/smtpd/run

RUN mkdir -p /etc/service/notebook
ADD ./runit_scripts/notebook.sh /etc/service/notebook/run
RUN chmod +x /etc/service/notebook/run

RUN mkdir -p /etc/service/brackets
ADD ./runit_scripts/brackets.sh /etc/service/brackets/run
RUN chmod +x /etc/service/brackets/run

##startup scripts
RUN mkdir -p /etc/my_init.d
ADD ./runit_scripts/startup.sh /etc/my_init.d/startup.sh
RUN chmod +x /etc/my_init.d/startup.sh

EXPOSE 22 25 8787 8081 8080 4000 4200 8888

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]
