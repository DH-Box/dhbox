DH Box
=====

A toolbox for Digital Humanities.

###DH BOX Local Install Process
Currently DH Box requires a linux that has apt-get. DH Box has been most thoroughly tested on Ubuntu.

1. [Install Docker](https://www.docker.com/)
2. Install `pip`, Python package manager
3. Clone git repo (`git clone https://github.com/DH-Box/dhbox.git`)
4. Navigate to `dhbox/` 
5. Run `pip install -r requirements.txt` (preferably in a virtualenv)
6. Rename `config.cfg.template` to `config.cfg` and edit settings as desired
7. Run `manage start` to download the DH Box seed, or navigate to `dhbox/seed` and run `docker build -t thedhbox/seed:latest .` if you want to build it yourself (takes 15 minutes or more).
8. Run `manage build_database`
9. Run `python wsgi.py`
10. Navigate to site on `http://localhost:80`

###If you are developing for DH Box, there are a few more steps:

11. Install Node and Node Package Manager: `apt-get install nodejs npm`
12. Install Gulp and Bower: `npm install gulp bower`
13. Changes to the site go into the `/src` directory. Propagate changes with `gulp build`
