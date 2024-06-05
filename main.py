#!/bin/python3
"""

"""
import argparse
import os.path
import sys
import urllib.error

from pwn import *
from colorama import Style, Fore, Back
import re
from urllib import request
from urllib.request import urlretrieve



def main(argParser):
    choice = argParser.subcommand
    patternLength = argParser.length
    envVar = os.environ["HOME"]
    configFolder = envVar + "/.config/pypattern/"
    configPath = configFolder + "/patternSettings"
    if (not os.path.exists(configFolder)):
        os.makedirs(configFolder)
    if (not os.path.exists(configPath)):
        print(Fore.BLACK + Back.BLUE + "[*] Creating Config [*]" + Style.RESET_ALL)
        fdSetting = open(configPath, "w+")
        fdSetting.write("patternPath:" + configFolder + "/cyclicPatternGeneration")
        fdSetting.close()
        writePattern(configFolder)
        print(Fore.BLACK + Back.GREEN + "[*] Config and pattern created in $HOME/.config/pypattern/ folder [*]" + Style.RESET_ALL)


    patternPath = open(configPath, "r").readlines()[0].split(':')[1]
    if (choice == "create"):
        patternCreated = patternCreate(patternLength, argParser.end, patternPath,argParser.offset, argParser.charset)
        print(patternCreated)
    elif (choice == "find"):
        origPattern = patternCreate(patternLength, argParser.end, patternPath,argParser.offset, charset=None)
        patternToFind = argParser.pattern
        patternToFind, patternOffset = patternFind(origPattern, patternToFind)
        if (patternToFind == -1):
            print(Fore.RED + Back.BLACK + "[!] Pattern Not Found [!]" + Style.RESET_ALL, end='')
        else:
            if (not argParser.quiet):
                print(Fore.GREEN + Back.BLACK + "[*]" + Style.RESET_ALL + "Offset: " + str(patternOffset))
                if (argParser.offset):
                    print(Fore.GREEN + Back.BLACK + "[*]" + Style.RESET_ALL + "artificial Offset: " + str(
                        argParser.offset))
                if (patternOffset > 5):
                    print(Fore.RED + Back.BLACK + origPattern[0:patternOffset] + Style.RESET_ALL, end='')
                    print(Fore.GREEN + Back.BLACK + patternToFind + Style.RESET_ALL, end='')
                    print(Fore.RED + Back.BLACK + origPattern[
                                                  patternOffset + (len(patternToFind)):patternLength] + Style.RESET_ALL,
                          end='')
                elif (not patternOffset):  # patternOffset is 0
                    print(Fore.GREEN + Back.BLACK + patternToFind + Style.RESET_ALL, end='')
            else:
                print(patternOffset)
    elif (choice == "config"):
        newPath = input("New Path To Pattern File: ")

    else:
        sys.exit("Action not recognized, exiting")


def writePattern(pathToPattern):
    print(Fore.BLACK + Back.BLUE + "[*] Downloading Pattern [*]" + Style.RESET_ALL)

    try:
        request.urlopen('https://google.com', timeout=1)
    except urllib.error.URLError as err:
        print(err)
        print(Back.RED + Fore.BLACK + "[!!] Need internet connection to retrieve pattern [!!]" + Style.RESET_ALL)
        print(Back.RED + Fore.BLACK + "[!] You can also specify a patternFile with a path by running 'pypattern config' [!]" + Style.RESET_ALL)
        sys.exit(-1)
    res = urlretrieve("https://raw.githubusercontent.com/lafreuxpabo/mypattern/main/cyclicPatternGeneration", pathToPattern + "cyclicPatternGeneration")
    if (res[0] == 200):
        print(Back.RED + Fore.BLACK + "[*] Downloaded patternFile [*]" + Style.RESET_ALL)


def fromBytesWith0x(patternToFind):
    finalPatternRemade = ''
    for idx in range(len(patternToFind) - 1, 0, -2):
        tmp = '' + patternToFind[idx - 1] + patternToFind[idx]
        if ('0x' not in tmp):
            finalPatternRemade += chr(int(tmp, 16))
    return finalPatternRemade


def patternCreate(length: int, end, pathToPattern, offset=0, charset=None):
    fd = open(pathToPattern, 'r')
    if (not charset):
        line = fd.readlines()[0][0 + offset:length + offset]
    else:
        line = ''
        charset = charset.split(',')
        cInd = 0
        while (len(line) != length):
            line += charset[cInd]
            cInd += 1
            cInd = cInd % len(charset)
    return line


def patternFind(patternBase, patternToFind):
    regexPatternStart0x = "0x[0-9]+"
    finalPatternRemade = patternToFind
    if (re.search(regexPatternStart0x, finalPatternRemade)):
        finalPatternRemade = fromBytesWith0x(patternToFind)
    if (finalPatternRemade in patternBase):
        return (finalPatternRemade, patternBase.index(finalPatternRemade))
    else:
        return (-1, -1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Pattern Project',
        description='Allow easy generation of patterns in SHELL',
        epilog="Two args, a length, and an action between 'find' and 'create', returns a pattern or an offset")
    parser.add_argument('length', type=int)

    actionSubParsers = parser.add_subparsers(dest='subcommand')
    actionSubParsers.required = True
    parser_find = actionSubParsers.add_parser('find')
    parser_find.add_argument(
        'pattern',
        help='Find pattern in string.')
    parser_find.add_argument("--offset", "-o",
                             help="Offset option, allows to specify an offset when creating your pattern, "
                                  "instead of starting from pattern[0], it will starts from pattern[offset]",
                             type=int,
                             required=False, default=0)
    parser_find.add_argument("--quiet", "-q",
                             help="Turn off verbose output, return only offset",
                             required=False, default=False, action='store_true')

    parser_create = actionSubParsers.add_parser('create')
    parser_create.add_argument("--charset", "-c",
                               help="Charset Options, allows to specify a charset for pattern, each chars must be "
                                    "separated by comma. ie: a,b,c...", required=False)

    parser_create.add_argument("--offset", "-o",
                               help="Offset option, allows to specify an offset when creating your pattern, "
                                    "instead of starting from pattern[0], it will starts from pattern[offset]",
                               type=int,
                               required=False, default=0)
    parser_create.add_argument("--end", "-e",
                              help="Value to add at the end of the generated pattern",
                              type=int,
                              required=False, default=0)

    parser_config = actionSubParsers.add_parser('config')

    args = parser.parse_args()
    main(args)

