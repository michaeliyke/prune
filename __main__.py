"""
PRUNE - p
p d1 d2 d3 -p .txt __pycache__ nodemodules -d
pruner d1 d2 d3 --pattern .txt __pychache__ nodemodules --dry-run
NOTE: source folder(s) are all the first positional arguments

--pattern|-p|--starts-with|-s|--ends-with|-e|--contains|-c|--objects|-o
-o - exact match object names

Special options/flags
-M|--maximum, -l|--level :: list
-W|--overwrite, -K|--keep, -S|--skip :: copy or move

STEPS:
collect args using ga:
  positionals = source_dirs
  matching and its args
  then flags
"""

import os
from pathlib import Path
import sys
from typing import Callable
#TODO: rename from ga_cli import cli_parse
from ga_cli import parse
# python -m pruning.dir C:\Users\Iyke\BASES\COURSES\cloud node_modules -d
from pruning.dir.prune import match_fn, prune, walk
from pruning.utils import check_args, create_err as err

#
# -o - 
options = {
  '-p': '--pattern',
  '-s': '--starts-with',
  '-e': '--ends-with',
  '-c': '--contains',
  '-o': '--objects',
  '--pattern': {'name': 'pattern', 'short': '-p', 'desc': 'pattern matches object name'},
  '--starts-with': {'name': 'starts-with', 'short': '-s', 'desc': 'object name starts with'},
  '--ends-with': {'name': 'ends-with', 'short': '-e', 'desc': 'object name ends with'},
  '--contains': {'name': 'contains', 'short': '-c', 'desc': 'object name contains'},
  '--objects': {'name': 'objects', 'short': '-o', 'desc': 'exactly match object names'},
}

flags = {}


d = parse(options=options)

print(d)