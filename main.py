#!/bin/python3
"""

"""
import argparse
from colorama import Style, Fore, Back
import re




def main(argParser):
    choice = argParser.subcommand
    patternLength = argParser.length

    if (choice == "create"):
        if (argParser.charset):
            patternCreated = patternCreate(patternLength, argParser.charset)
        else:
            patternCreated = patternCreate(patternLength)
        print(patternCreated)
    else:
        origPattern = patternCreate(patternLength)
        patternToFind = argParser.pattern
        patternToFind, patternOffset = patternFind(origPattern, patternToFind)
        if (patternToFind == -1):
            print(Fore.RED + Back.BLACK + "[!] Pattern Not Found [!]" + Style.RESET_ALL, end='')
        else:
            print(Fore.GREEN + Back.BLACK + "[*]" + Style.RESET_ALL + "Offset: " + str(patternOffset))
            if (not argParser.quiet):
                if (patternOffset > 5):
                    print(Fore.RED + Back.BLACK + origPattern[0:patternOffset] + Style.RESET_ALL, end='')
                    print(Fore.GREEN + Back.BLACK + patternToFind + Style.RESET_ALL, end='')
                    print(Fore.RED + Back.BLACK + origPattern[patternOffset + (len(patternToFind)):patternLength] + Style.RESET_ALL, end='')
                elif (not patternOffset):  # patternOffset is 0
                    print(Fore.GREEN + Back.BLACK + patternToFind + Style.RESET_ALL, end='')
            else:
                print(origPattern[0:patternOffset])


def fromBytesWith0x(patternToFind):
    finalPatternRemade = ''
    for idx in range(len(patternToFind) - 1, 0, -2):
        tmp = '' + patternToFind[idx-1] + patternToFind[idx]
        if ('0x' not in tmp):
            finalPatternRemade += chr(int(tmp, 16))
    return finalPatternRemade


def patternCreate(length: int, charset=None):
    fd = open("/home/saturne/Bureau/Projets/mypattern/cyclicPatternGeneration", 'r')
    if (not charset):
        line = fd.readlines()[0][0:length]
    else:
        line = ''
        charset = charset.split(',')
        cInd = 0
        while(len(line) != length):
            line += charset[cInd]
            cInd += 1
            cInd = cInd % len(charset)
    return line


def patternFind(patternBase, patternToFind):
    #regexPatternBytesBackslashX = "[\\]..+"
    regexPatternStart0x = "0x[0-9]+"
    finalPatternRemade = patternToFind
    if (re.search(regexPatternStart0x, finalPatternRemade)):
        finalPatternRemade = fromBytesWith0x(patternToFind)
    #if (re.search(regexPatternBytesBackslashX, patternToFind)):
    #    patternToFind.replace("\\x", "")
    #    finalPatternRemade = fromBytesWith0x(patternToFind)
    #    print(finalPatternRemade)
    if (finalPatternRemade in patternBase):
        return (finalPatternRemade, patternBase.index(finalPatternRemade))
    else:
        return (-1, -1)





if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Pattern Project',
        description='Allow easy generation of patterns in SHELL',
        epilog="Two args, a length, and an action between 'find' and 'create', returns an offset")
    parser.add_argument('length', type=int)
    parser.add_argument('--quiet', '-q', dest="quiet", help="Quiet Options, print only pattern", type=bool)  # option that takes a value

    actionSubParsers = parser.add_subparsers(dest='subcommand')
    actionSubParsers.required = True
    parser_find = actionSubParsers.add_parser('find')
    parser_find.add_argument(
        'pattern',
        help='Find pattern in string.')

    parser_create = actionSubParsers.add_parser('create')
    charsetSubParsers = parser_create.add_argument("--charset", "-c" ,help="Charset Options")
    charsetSubParsers.required = False
    parser_dump = actionSubParsers.add_parser("charset",
                                              description="set of characters to use for pattern generation, separated by coma. ie: a,b,c...",)



    args = parser.parse_args()
    main(args)

