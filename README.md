# JRScrap2

It' s a rewrite of JRScrap.

This time, it' s written in Python 2.7 with the help of the [Kivy framework](https://kivy.org/#home).

# Why it's better than JRScrap ?

Because it can run on Windows/Linux/Mac from  source code and Android.
Some pre-compiled version are there too - see below.

It does not use the .COM connection to JRMC, but only MCWS !
It was not possible, few years ago, to do it only with MCWS.

So, there's no more excuse not to make you version of it, because this time everything is FREE, IDE included.

# Why it's uglier than JRScrap ?
Currently, it' s in a alpha-very early stage, but functionnal.
All data come from TMDB, some of FanArt.

TV show's are **not** supported and there's **no** OpenSubtitle support for now.

So, it cannot act as a complete JRScrap replacement for now.

It works completely with MCWS, (so  it's HTTP )
Files can be on a NAS, there's no problem.

# What it always will be
Free

# What it never will be

A replacement for Gizmo or JRemote, because I will **never** try to compete with this excellent tools. My only concern and intention is to try to fullfill some specific task that you can't do with JRMC alone.That's it,that's all.

Long-term support is far from garanteed, same for regular updates : it's the power of freedom, you can hack it yourself !

## Installation:

* A Windows installer is [here](https://github.com/fredele/JRScrap2/blob/master/windows/Output/setup%20JRScrap2.exe?raw=true).

* A android .apk is [here](https://github.com/fredele/JRScrap2/blob/master/android/bin/JRScrap2-0.1-debug.apk).

Must be installed via "adb install <package_name.apk>" or kivy's buildozer, it's not available on the AppStore currently.

* On Linux, it can be run from source, but I think I will never try to do a package (too many distros. - far too few users).
* For Mac users, well, I'm not a fanboy ...

## Setup:

Activate MCWS in JRMC, authentication **MUST** be set !

Find the IP address of your server and configure JRSCrap2 in it's settings (click on the wheel et the bottom-right corner).

* Host : the IP address of your server
* Port : the port it runs (52199 is default)
* Username : the auth. set in JRMC
* Password : same thing ...

Restart JRScrap and it shoud show your Movies.

## Manual:
See the little wiki [here](https://github.com/fredele/JRScrap2/wiki).


