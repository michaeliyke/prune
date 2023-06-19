list
move
copy
delete - pruner

pruner helps to remove unnecessary fs objects. This is it's core objective - to help sift through all the sub-dirs
and their nested dirs and remove unnecessary files or folder or both. It basically is a helper tool to help clean up a
folder tree from the commad line. By default, pruner moves affected objects to system trash which can still be restored.

Additionally, it can list, move or copy fs objects to desired location(s).
The performance will be considered in a later version.

COMMAND FORMS
--pattern|-p|--starts-with|-s|--ends-with|-e|--contains|-c|--objects|-o
-o - exact match object names

Special options/flags
-M|--maximum, -l|--level :: list
-W|--overwrite, -K|--keep, -S|--skip :: copy or move

PRUNE
p d1 d2 d3 -p .txt __pycache__ nodemodules -d
pruner d1 d2 d3 --pattern .txt __pychache__ nodemodules --dry-run
NOTE: source folder(s) are all the first positional arguments


MOVE OR COPY
p.move -s|-c|-e|-p|-o  # No destinations provided so save in temp on exec folder
p.move -e .txt .jpg -d C:\objs F:\store # store .txt and .jpg in both locations
(Duplicate flags: --over-write|-W|--keep|-K|--skip|-S)


List
List fs objects as you like and to the depth you appreciate i.e limited or maximum
p.list # all objects within current tree
p.list -l 1|-l 2|-l 3|-l x # all objects within current tree with depth limited to one level, two, three or x
p.list source -o,-p,-c,-e,-s x y z -M # list x y z from source down to maximum depth
NOTE: default depth is -l 1, --level x is specified as -l x or --level x
source is the first positional argument and is single
COMMAND FORMAT

# Prune files
 python -m pruning.prune_files . ._
 python -m pruning.prune_files . .txt
 python -m pruning.prune_files . __pycache__

 # Prune folders - coming soon

 # Prune arbitrary - coming soon
