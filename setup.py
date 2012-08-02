#!/usr/bin/env python

##
# This file is part of the uSherpa Python Library project
#
# Copyright (C) 2012 Stefan Wendler <sw@kaltpost.de>
#
# The uSherpa Python  Library is free software; you can redistribute 
# it and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  uSherpa Python Library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
# 
#  You should have received a copy of the GNU Lesser General Public
#  License along with the JSherpa firmware; if not, write to the Free
#  Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
#  02111-1307 USA.  
##

'''
uSherpa Python Library setup-script. To install this library use: 

  sudo python setup.py install  

'''

from distutils.core import setup

setup(name='pysherpa',
	version='0.1',
	description='uSherpa Python Library',
	long_description='Client library for Python to use MCU running uSherpa Firmware. Depends on pyserial.',
	author='Stefan Wendler',
	author_email='sw@usherpa.org',
	url='http://www.usherpa.org/',
	license='LGPL 2.1',
	packages=['usherpa'],
	platforms=['Linux'],
	package_dir = {'': 'src'}
)
