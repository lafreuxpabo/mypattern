#!/bin/python3
"""

"""
import argparse
import sys

from colorama import Style, Fore, Back
import re


def main(argParser):
    choice = argParser.subcommand
    patternLength = argParser.length

    if (choice == "create"):
        patternCreated = patternCreate(patternLength, argParser.offset, argParser.charset)
        print(patternCreated)
    elif (choice == "find"):
        origPattern = patternCreate(patternLength, argParser.offset, charset=None)
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
    else:
        sys.exit("Action not recognized, exiting")


def fromBytesWith0x(patternToFind):
    finalPatternRemade = ''
    for idx in range(len(patternToFind) - 1, 0, -2):
        tmp = '' + patternToFind[idx - 1] + patternToFind[idx]
        if ('0x' not in tmp):
            finalPatternRemade += chr(int(tmp, 16))
    return finalPatternRemade


def patternCreate(length: int, offset=0, charset=None):
    fd = open("./cyclicPatternGeneration", 'r')
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

    args = parser.parse_args()
    main(args)
