DH Box
=====

A toolbox for Digital Humanities.

[Wiki](https://github.com/DH-Box/dhbox/wiki)


###DH BOX Local Install Process
1. [Install Docker](https://www.docker.com/)
2. Install `pip`, Python package manager
3. Clone git repo (`git clone https://github.com/DH-Box/dhbox.git`)
4. Navigate to `dhbox/` 
5. Run `sudo pip install -r requirements.txt` (preferably in a virtualenv)
6. Navigate to dhbox/Docker-DHBox/seed
7. Start docker: `sudo systemctl start docker`
8. Run `sudo docker build -t dhbox/seed .` (takes 15 minutes or more)
9. Navigate to `dhbox/`
10. Run `python site.py`
11. Navigate to site on `http://localhost:5000`
