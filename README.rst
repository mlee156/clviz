# clviz

[![](https://img.shields.io/pypi/v/clarityviz.svg)](https://pypi.python.org/pypi/clarityviz/0.0.1)
[![Build Status](https://travis-ci.org/alee156/clviz.svg?branch=master)](https://travis-ci.org/alee156/clviz)

**clviz** is a Python 2 package for Clarity brain analysis. It supports  ANALYZE (plain, SPM99, SPM2 and later), GIFTI, NIfTI1, NIfTI2, MINC1, MINC2, MGH and ECAT as well as Philips PAR/REC.

## Installation

To install the prerequisite packages, clone the directory using:
```
git clone https://github.com/alee156/clviz.git
cd clviz
pip install -r requirements.txt
```

Afterwards install opencv. This is easily accomplishable if you have brew or conda by using either
 ```
 brew install opencv
 ```
 or
 ```
 conda install opencv
 ```
 If not, install opencv by following their build instruction here: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_setup/py_table_of_contents_setup/py_table_of_contents_setup.html#py-table-of-content-setup

After installing the prerequisites there's two options for using clviz. You can use clviz as a standalone package and
perform basic analysis on your own files, or you can install ndreg and ndio and use clviz as a powerful integrating tool
for graph-based analysis.

```
pip install clarityviz
```

## Docker Installation
```
docker pull lkzhu1/ubuntu:prototype1
docker run -t -i lkzhu1/ubuntu:prototype1
```

## Getting Started

In development but tutorials will be uploaded shortly!

## Documentation

Complete documentation is located at https://neurodatadesign.github.io/seelviz//reveal/clarityviz.m.html. 


## Credits

Credit to installation script in .travis.yml goes to https://github.com/milq/scripts-ubuntu-debian.


