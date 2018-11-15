
# Why

For the 2018-19 season, for the test stand!

# Who

Eric, mainly. Max made it, ask him.

# How

Run with `python callibrate.py` and do the callibration,
then `python loadcell_to_csv.py` which should load your config 
and print readings to screen, while periodically saving intermidiate csv's,
then you hit enter and it save `final.csv` with timestamp.

# Really?

No, you also need to install the badly designed phidgets library. They're so bad, 
they don't ever have an up to date pypi package! Wow. Sad.

First, get the drivers, which are binaries and probably full of malware:

<https://www.phidgets.com/docs/Operating_System_Support>


Now, for the python lib, just go here:

<https://www.phidgets.com/docs/Language_-_Python>

and download this:

<https://www.phidgets.com/downloads/phidget22/libraries/any/Phidget22Python.zip>

then unzip it and cd (or chdir if you are a windows victim) into Phidget22Python,
and run `python setup.py install`. Or if you still can't use the command line or 
add things to your path, you're out of luck. Sorry.
