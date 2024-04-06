#!/bin/python3
"""

"""
import argparse
from colorama import Style, Fore, Back





def main(argParser):
    choice = argParser.subcommand
    patternLength = argParser.length
    if (choice == "create"):
        patternCreated = patternCreate(patternLength)
        print(patternCreated)
    else:
        origPattern = patternCreate(patternLength)
        patternToFind = argParser.pattern
        patternOffset = patternFind(origPattern, patternToFind)
        print(Fore.GREEN + Back.BLACK + "[*]" + Style.RESET_ALL + "Offset: " + str(patternOffset))
        prePattern = []
        postpattern = []
        if (patternOffset > 5):
            print(Fore.RED + Back.BLACK + origPattern[0:patternOffset] + Style.RESET_ALL, end='')
            print(Fore.GREEN + Back.BLACK + patternToFind + Style.RESET_ALL, end='')
            print(Fore.RED + Back.BLACK + origPattern[patternOffset+(len(patternToFind)):patternLength] + Style.RESET_ALL, end='')
        elif (not patternOffset):  # patternOffset is 0
            print(Fore.GREEN + Back.BLACK + patternToFind + Style.RESET_ALL, end='')



def patternCreate(length: int):
    fd = open("/home/saturne/Bureau/Projets/pattern/cyclicPatternGeneration", 'r')
    line = fd.readlines()[0][0:length]
    return line


def patternFind(patternBase, patternToFind):
    return patternBase.index(patternToFind)











if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Pattern Project',
        description='Allow easy generation of patterns in SHELL',
        epilog='Two args, on mandatory to specify length of pattern and -f to find a substr in pattern, returns an offset')
    parser.add_argument('length', type=int)
    subparsers = parser.add_subparsers(dest='subcommand')
    subparsers.required = True
    #  subparser for dump
    parser_dump = subparsers.add_parser('find')
    # add a required argument
    parser_dump.add_argument(
        'pattern',
        help='Find pattern in string.')

    #  subparser for upload
    parser_upload = subparsers.add_parser('create')
    #parser.add_argument('-f', '--find', action='store_true')  # option that takes a value
    args = parser.parse_args()
    main(args)

