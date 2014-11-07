FROM debian:stable
MAINTAINER Steve
RUN apt-get -y update
RUN apt-get install -y git openssh-server apache2 supervisor python-apt apt-utils
RUN apt-get -qy install python-pip python-dev git
RUN pip install PyYAML jinja2 paramiko
RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd
ADD . /src

# Install ansible
RUN pip install ansible==1.7
ADD hosts /etc/ansible/hosts
WORKDIR /src
RUN ansible-playbook start.yml -c local
EXPOSE 22 8787 80 4200