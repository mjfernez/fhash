# fhash

## fhash - a simple python tool for generating, passing and formatting hash values

So some may not agree, but I find hash values make very good master passwords for tools like 
password managers and other security software. Why go with just a passphrase when you can pipe
the sucker in a million and a half one-way functions? I've found this is only a practical
solution though if:
1) You know you will always be able to copy and paste on the device you are using
2) You know you will always have a hashing tool either natively or available online

For convenience, I used online tools for years, but this led to bad habits. See some tools like
to use caps (it is a hex number after all) but some stick with lowercase. Seems like a useless
distinction and it probably is, but since some of my hash passwords are upper case and some are
lower, it'd be nice to have a simple portable tool to do that so I don't need to rely on some
random guy on the internet.

So here it is (more or less)!

The script is self contained and executable so Linux users can just use:

$./fhash.py sha2 -i "Hello, World!"

If you really like it and want to use it from anywhere on your system, copy it into your path:

$ sudo cp fhash.py /usr/bin/fhash

No Windows support, yet sorry! Please make a pull request if you want to add that, should be
easy enough to do, just haven't gotten around to it

The default output can be passed to other commands as in:

$ fhash.py md5 -i $(fhash.py sha2 -i "Hello, world!")

You can optionally use the '-v' flag for more details (mostly was used for debugging), but this
example above will not work correctly with it

Use '-h' '--help' to see the list of flags and how to use them. If you have suggestions on how
to improve the help menu to make the tool easier to understand, please submit a pull request or
open an issue!

(Don't run the script itself as administrator by the way, this sometimes messes things up)


Any and all contributors welcome. Please just make sure any edits are
1) Compliant with PEP8
2) Do not have any lines over 95 characters (this is half my screen so it fits nicely
 - not sure if this is a universal standard though)
