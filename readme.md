https://www.phidgets.com/?view=code_samples&lang=Python

# Thermocouple

https://www.phidgets.com/?tier=3&catid=14&pcid=12&prodid=727

+ Precision: +-0.75C

# Check for attachment

 lsusb
 

# Compile code

./configure

sudo make

sudo make install

# Setting udev Rules

If you don't want to be using sudo to run Phidget programs (including the Network Server) forever, you will want to create a udev rule to allow yourself access to the Phidget when you are not root.

Udev has an easy way to set the owner and permissions of the USB interface of the Phidget - it finds all devices that match a given set of rules, and applies new traits to them. But you need to give udev something to match in order to apply the new settings. Here, we will tell udev to match the vendor code for Phidgets, Inc.

We recommend that you use the rules file included in the library download you have already installed. Check the README file included in that download for information on how exactly to install it, or continue reading here.

The rules for udev are kept in files in /etc/udev/rules.d and are traditionally grouped into order of running (10 runs before 20, 30, etc) and device type (cd, network, etc). There should be one or more files in there already. Simply find the file named 99-libphidget22.rules included with our library files, and move it into /etc/udev/rules.d.

Strictly speaking, the files run in lexical order (i.e. the order they're listed when you use the ls command). A device can match many rules, and all will apply (if possible). If conflicting rules are found, the first rule found is followed. 
