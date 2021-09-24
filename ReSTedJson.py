#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Objective: to print LOADED json data from previously SAVED file
"""

import json
from misc import simpleEnum
from khutils import printhead

title = __file__.split('/')[-1].split('.')[0]

# printing dir(json):
simpleEnum(json, name="json package")

# loading json file
jsonname = 'sdata.json'

# with open(jsonname, 'r') as jsonf:
#     dataRead = json.load(jsonf)

filesHistory = {
    "rest": ['a/b/c1', 'a/b/c2', 'a/b/c3', 'a/b/c4', 'a/b/c5'],
    "css": "None"
}

with open("tmp/fileHistory.json", "w") as logSave:
    json.dump(filesHistory, logSave, indent=4)

# loading:
with open("tmp/fileHistory.json", "r") as logLoad:
    historyLoaded = json.load(logLoad)

print("json log loaded:\n", historyLoaded)
print(f"historyLoaded['rest'] = {historyLoaded['rest']}")
print(f"historyLoaded['css'] = {historyLoaded['css']}")
