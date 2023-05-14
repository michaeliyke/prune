import sys
# python -m pruning.dir C:\Users\Iyke\BASES\COURSES\cloud node_modules -d
from pruning.dir.pruner import match_fn, prune, walk
from pruning.utils import check_args

ok, args_tuple, err_message = check_args(sys.argv)
path, m, dry_run = args_tuple

if not ok:
  raise Exception(err_message)

walk(dir=path, prune=prune, match_fn=match_fn(contains=m), dry=dry_run)
# walk(dir=path, pruner=prune, matcher=matcher(endswith=m), dry=dry_run)
# walk(dir=path, pruner=prune, matcher=matcher(startswith=m), dry=dry_run)
# walk(
#   dir=path,
#   pruner=prune,
#   dry=dry_run,
#   matcher=matcher(matcher=matcher_test, match_str=m),
# )



# default is --contains
# --ends|--endswith|-e, --starts|--startswith|-s, 
# --contains|--find|--search|--index|-c|-f|-S|-i
# /?|--help|-h
# No commands - refer them to run help command