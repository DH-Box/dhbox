DH Box
=====

A toolbox for Digital Humanities.

[Wiki](https://github.com/DH-Box/dhbox/wiki)


###DH BOX Local Install Process
Currently DH Box requires a linux that has apt-get.
#### One line install:
```
wget -qO- https://raw.githubusex/develop/install_dhbox.sh | sudo sh
```
1. [Install Docker](https://www.docker.com/)
2. Install `pip`, Python package manager
3. Clone git repo (`git clone https://github.com/DH-Box/dhbox.git`)
4. Navigate to `dhbox/` 
5. Run `pip install -r requirements.txt` (preferably in a virtualenv)
6. Navigate to `dhbox/seed` 
7. Run `sudo docker build -t dhbox/seed:latest .` (takes 15 minutes or more)
8. Navigate to `dhbox/`
9. Run `python dhbox.py`
10. Navigate to site on `http://localhost:5000`
