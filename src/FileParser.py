#!/usr/bin/python3

import os

def getParsed(rawFile):
    """ Return a dictionnary containing the body part and header part of passed
    file. None if passed file is bad formatted. """

    cnt = 0
    result = {}
    passedLines = ""
    firstLine = False
    for line in rawFile.splitlines():
        if(firstLine):
            firstLine = False
            if(line == ""):
                continue
        if(line == '---' and cnt != 3):
            cnt+=1
            if(cnt == 2):
                result["header"] = passedLines
                passedLines = ""
                firstLine = True
                cnt+=1
            continue
        passedLines+=line+"\n"
    if(cnt != 3):
        return None
    result["body"] = passedLines
    return result
