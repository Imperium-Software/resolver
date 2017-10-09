![Resolver Header Image](https://i.imgur.com/mipsPa9.png "Resolver")

![Build Status](https://travis-ci.org/Imperium-Software/resolver.svg?branch=master)
[![Stories in Ready](https://badge.waffle.io/Imperium-Software/resolver.png?label=ready&title=Ready)](https://waffle.io/ErnstEksteen/COS301_GA-SATSolver?utm_source=badge)
[![Code Health](https://landscape.io/github/Imperium-Software/resolver/master/landscape.svg?style=flat)](https://landscape.io/github/Imperium-Software/resolver/master)
[![Python Versions](https://img.shields.io/badge/python-3.4%2C3.5%2C3.6-blue.svg)]()
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)]()

Resolver is a SAT solver, or a scientific tool for finding solutions for boolean formulae.
If a problem can be encoded as a boolean formula, solutions can automatically be found by the software.
This is done using a state-of-the-art genetic algorithm and other heuristics.
This software allows solving of complex problems in classical planning, automatic theorem proving and hardware and software verification.

## Features
- Complete implementation of GASAT SAT solving algorithm and variations
- Graphical user and command-line interfaces that can be accessed remotely
- Beginner friendly features intended for education on boolean satisfiability and genetic algorithms
- Comprehensive reporting and statistics gathering with export feature
- Graphing of statistics gathered during the solving process
- And many more...

## Dependencies
- Python 3.4+
- [bitarray](https://pypi.python.org/pypi/bitarray/) 0.8.1
- Node.js v6.11.3+
- npm v3.10.10+

## Quick Start
Download the latest release from the [Releases](https://github.com/Imperium-Software/resolver/releases) page and extract it somewhere.

In the extracted folder, start the server using the command:
```sh
python SATSolver/main.py
```

The graphical user interface can then be used to connect to this server instance. It can be started using these commands:
```sh
cd SATSolver/interface
npm install
electron .
```

See the [User Guide](https://github.com/Imperium-Software/resolver/wiki/User-Guide) for more details.

## Credits
This project is developed and maintained by:
- [Dewald de Jager](https://github.com/DewaldDeJager)
- [Craig van Heerden](https://github.com/craig95)
- [Regan Koopmans](https://github.com/Regan-Koopmans)
- [Vignesh Iyer](https://github.com/Vignesh-95)
- [Ernst Eksteen](https://github.com/ErnstEksteen)

The core of this project is an implementation of the [GASAT algorithm](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.108.7124&rep=rep1&type=pdf) by Lardeux et al.

## Team Resources
- [Team Website](https://imperium-software.github.io/)
- [Slack](https://imperium-se.slack.com)
- [Project Briefing Documentation](http://cs.up.ac.za/files/COS301/Download/1905/)
- [Requirements Documentation](https://www.overleaf.com/9687894kqqdwgmqymsx)
- [Requirements Documentation PDF](https://dearvolt.com/imperium/software-requirements-specification.pdf)
- [Architectural Design Specifications](https://github.com/Imperium-Software/resolver/wiki/Architectural-Design-Specifications)
- [Latest Testing Report](https://drive.google.com/file/d/0B9BjYGq76aeBNnk1NUx4ek5zMWM/view?usp=sharing)
- [CS Group Page](http://cs.up.ac.za/teams/pages/manage/147/5)
