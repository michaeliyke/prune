import sys

from pruning.prune_files.prune_files import matcher, prune, walk
from pruning.utils import check_args

ok, args_tuple, err_message = check_args(sys.argv)
path, m, dry_run = args_tuple

if not ok:
  raise Exception(err_message)

walk(dir=path, pruner=prune, matcher=matcher(contains=m), dry=dry_run)
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