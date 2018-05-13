# SV2
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) 

Security auditing tool, module-based, similar to [lynis](https://github.com/CISOfy/lynis), but developed with python and enthusiasm.

## Advice
This project is in no active development (ie: we develop it when we have time).
Also, it's very unstable, and bugs are frequents (at least for now). **But anyway, you can learn new things with this random project, and it is funny. :D**

## Why did you do it?
It occurred to someone, there was no reason not to do it and it seemed fun.

The idea is to collect a general security recomendations in a form of a software that already checks whether your system is already configured to be secure or not. As such, it's not intended to be an enterprise level software with a lot of junk but a simple script that may or may not satisfy your needs.

### Prerequisites

* Python3
* pip3 (optionall)

### Installing

### First option, from github 

* Clone this repository and go to the project directory:
```
git clone https://github.com/OSPG/sv2
cd sv2
```
* Install python dependencies:
```
pip3 install -r requirements.txt
```

### Second option, from gentoo overlay

* Configure this overlay https://mumei.space/david/gentoo-overlay
* emerge app-forensics/sv2

That is all. :)

If you execute it (as root) you may see something like:
![](http://i.imgur.com/LPmqZgp.png)

## Built With

* [Python](https://python.org) - The official website of Python.
* [pyyaml](https://github.com/yaml/pyyaml) - Github repository of PyYaml.
* [psutil](https://github.com/giampaolo/psutil) - Github repository of psutil.
* [python-iptables](https://github.com/ldx/python-iptables) - Github repository of python-iptables

## Contributing

Nothing special, fork the repository, make changes and send a pull request.
Contributions are welcome. ^^

## Authors

* **David Román** - *Initial work* - [GitHub profile](https://github.com/stkw0)
* **Pablo Álvarez Córdoba** - *Initial work* - [GitHub profile](https://github.com/palvarezcordoba/), [Linkedin profile](https://www.linkedin.com/in/pablo-Álvarez-Córdoba/)

See also the list of [contributors](https://github.com/OSPG/sv2/contributors) who participated in this project.
