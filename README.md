usherpa-pysherpa
================
18.07.2012 Stefan Wendler
sw@kaltpost.de

This library provides a Python binding to a MCU running the [uSherpa] (http://github.com/wendlers/usherpa-firmware.git) firmware.

The README describes, how to install the library by using ant on the commandline. 


Project Directory Layout
------------------------

* `example-src`		Examples
* `LICENSE`			License information 
* `MANIFEST.in`		Manifest for distribution
* `README.md`		This readme
* `setenv.sh`		Set PYTHONPATH for testing
* `setup.py`		Setup script to install/distribute
* `src`				Sources of this library


Prerequisites
-------------

* To use the library, the pyserial library has to be installed. 
* A MCU (currently the TI Launchpad with MSP430G2553) with uSherpa firmware flashed.

  For details see the uSherpa firmware documentation:
    
     https://github.com/wendlers/usherpa-firmware/tree/master/doc  


Install the Library
-------------------

To install the library issue the following command in the top-level directory:

	python setup.py install

Alternatively you could place the "usherpa" folder from "src" to a directory of
your choice and make yout PYTHONDIR point to it. E.g. if you copied "usherpa"
to "~/python/usherpa":

	export PYTHONPATH=~/python/usherpa


Examples
--------

Some examples are located under "example-src/". On the command line, 
you could run them after you installed the library like this like this:

	python example-src/<ExampleToRun>

If you prefer running the examples without installing the library, you 
could do the following:

	. setup.sh
	python example-src/<ExampleToRun>
