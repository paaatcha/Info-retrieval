#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Author: André Pacheco
Email: pacheco.comp@gmail.com

This script verifies if the python libraries are installed in the PC. 
Otherwise, it asks to install.

"""

import os

# Checking numpy
try:
    import numpy
except ImportError, e:
    print 'The numpy lib is not installed. Insert your password to install it: \n'
    os.system("sudo apt-get install python-numpy")

# Checking scipy
try:
    import scipy
except ImportError, e:
    print 'The scipy lib is not installed. Insert your password to install it: \n'
    os.system("sudo apt-get install python-scipy")
    
# Checking matplotlib
try:
    import matplotlib
except ImportError, e:
    print 'The matplotlib lib is not installed. Insert your password to install it: \n'
    os.system("sudo apt-get install python-matplotlib")
    

print 'Your PC has all the necessary libs. Let\'s the games begin'


