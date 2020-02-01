#!/usr/bin/python3
from io import IOBase
import os
import sys
import argparse
import locale
import hashlib

# Defines the basic options and constants used
algos = ['md5', 'sha1', 'sha2', 'sha3']
modes = [224, 256, 384, 512]
formats = ['lowercase', 'uppercase', 'binary', 'decimal']
slash = '/'
pwd = os.getcwd()
os_encoding = locale.getpreferredencoding()

# For sha256 and sha3 only
DEFAULT_SIZE = 256

# For the verbose option
VERBOSE = False

'''Checks if the user put a directory as an input to a hash function.
As I see it, hashing a directory is ambiguous since it's not clear if you 
want to hash everything in the directory or the file structure itself.

But if you want to hash everything, you can just use just use /<directory>/* 
It's probably easier in other use-cases to zip the whole file structure and hash that.
@obj: the string or file object inputted by the user (Note: expects a file)
'''


def checkDirectory(obj):
    if os.path.isdir(obj):
        print('Error: "{}" specified is a directory. Must be a file'.format(obj))
        return True
    else:
        return False


'''Specifies the size in bits of the chosen function.
If the user put in a invalid length, throw an error
Returns the default length if no size is provided
@func: the hash function use (md5, sha1, sha2, sha3)
@size: the desired length of the output. i.e. sha256 
        outputs a message of 256 bits or 64 hex-digits
'''


def checkFunction(func, size):
    if(func in algos[0:2]):
        bsize = 160 if (algos.index(func)) else 128
        if(size == None):
            if(VERBOSE):
                print('Using default message size of ' +
                      '{} bits'.format(bsize))
        else:
            if(VERBOSE):
                print('Warning: "size" option is ignored for ' +
                      'sha1 and md5 since they are fixed-length')
                print('Using message size of {} bits'.format(bsize))
        return bsize
    else:
        if(size == None):
            if(VERBOSE):
                print('Using default message size, 256-bits')
            return DEFAULT_SIZE
        elif(size not in modes):
            print('Error: Message size must be 224, 256, 384, or 512 for {}'.format(func))
            sys.exit()
        else:
            if(VERBOSE):
                print('Using message size of ' +
                      '{} bits'.format(size))
            return size


'''Formats the hash value according to the user's choice
@msg: the string to be formatted
@fmt: the target format
'''


def formatOutput(msg, fmt):
    if(fmt == 'lowercase'):
        return msg.lower()
    elif(fmt == 'uppercase'):
        return msg.upper()
    elif(fmt == 'binary'):
        return '{}'.format(bin(int(msg, 16)))
    elif(fmt == 'decimal'):
        return str(int(msg, 16))
    else:
        print('You somehow passed an invalid format. Please file a bug report')
        sys.exit()


'''Returns the requested hash function "func" at the specified "size" (if it applies)
@func: the hash function use (md5, sha1, sha2, sha3)
@size: the desired length of the output. i.e. sha256 
        outputs a message of 256 bits or 64 hex-digits
'''


def getAlgorithm(func, size):
    if(func == 'md5'):
        return hashlib.md5()
    elif(func == 'sha1'):
        return hashlib.sha1()
    elif(func == 'sha2'):
        return eval('hashlib.sha' + str(size) + '()')
    elif(func == 'sha3'):
        return eval('hashlib.sha3_' + str(size) + '()')
    else:
        print('You somehow passed a function that doesnt exist. Please file a bug report')
        print('Quitting...')
        sys.exit()


'''The core hasing function. 
This takes an input string or file "msg" and hashes it with "algo"
@msg: the string or file to be hashed
@algo: the hashing algorithm to use
'''


def getHash(msg, algo):
    hasher = algo
    if(isinstance(msg, IOBase)):
        with open(msg, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
    else:
        buf = msg
        hasher.update(msg.encode(os_encoding))
    return hasher.hexdigest()


'''Sets up the tool to parse arguments correctly (help menu is added by default)
@args: all arguments inputted by the user
'''


def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input',
                        nargs='+',
                        required=True,
                        help='Input file or text. Try using sha2 -i "Hello, World!"')
    parser.add_argument('-o', '--output',
                        nargs='?',
                        default=None,
                        help='Destination file to save to. '
                        'Prints to screen if none specified. '
                        'You can save a comma separated list '
                        'of files and hashes by specifying the '
                        'file extension ".csv", otherwise saves hash values only as text')
    parser.add_argument('-s', '--size',
                        default=None,
                        type=int,
                        help='Message length in bytes 224, 256, 384, 512 '
                        '(only valid for sha 2 and 3).')
    parser.add_argument('-f', '--format',
                        choices=formats,
                        default=formats[0],
                        help='Formatting for the output')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Optionally add additional information to the output. '
                        'without this flag, the program will just print the hash')
    parser.add_argument('function',
                        choices=algos,
                        help='Use the specified hash function')

    return parser.parse_args(args)


'''Saves one or more hashes to file. Overwrites the file if it exists
@hashes: the hash or list of hashes to be saved
@output: the output destination specified by the user 
            (expects a file or "None" to print to screen)
'''


def saveOutput(hashes, output):
    while(os.path.isfile(output)):
        opt = input('That file exists. Ok to overwrite? (y/n): ')
        if(opt.lower() in ['y', 'yes']):
            break
        elif(opt.lower() in ['n', 'no']):
            output = input('Ok, type the new file name or file path: ')
        else:
            pass

    with open(output, 'w+') as f:
        f.seek(0)
        for h in hashes:
            f.write(h + '\n')
        f.truncate()
    print('File {} created!'.format(output))


if __name__ == "__main__":
    try:
        opts = getOptions(sys.argv[1:])
        inp = opts.input
        out = opts.output
        func = opts.function
        size = opts.size
        fmt = opts.format
        VERBOSE = opts.verbose

        if(inp == None):
            print('Error: No input given')
            sys.exit()

        # Check to make sure size and function inputs are valid
        size = checkFunction(func, size)

        # If the user chose to output to a file/directory
        if(out != None):
            if(checkDirectory(out)):
                sys.exit()

        # Go through the list of arguments provided by the user after the -i option
        for i in inp:
            if(checkDirectory(i)):
                inp.remove(i)

       # After going through the list, check to see if there are any files to hash
       # Really not the most elegant way to do this... consider refactoring
        if(inp == None):
            print('Error: No files in input!')
            sys.exit()

        hashes = []
        for j in inp:
            if(VERBOSE):
                print('Calculating {} hash for "{}"...'.format(func, j))
            md = getHash(j, getAlgorithm(func, size))
            formatted = formatOutput(md, fmt)
            hashes.append(formatted)
            if(out == None):
                print(formatted)

        if(out != None):
            if(out.endswith('.csv')):
                saveOutput(['{}, {}'.format(i, j)
                            for i, j in zip(inp, hashes)], out)
            else:
                saveOutput(hashes, out)
    except (KeyboardInterrupt):
        print('\nUser stopped the program')
        sys.exit()
    except:
        print('\nUnexpected Error')
        sys.exit()
