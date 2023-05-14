import sys
# python -m pruning.dir C:\Users\Iyke\BASES\COURSES\cloud node_modules -d
from pruning.dir.prune import match_fn, prune, walk
from pruning.utils import check_args, create_err as err

ok, args_tuple, err_message = check_args(sys.argv)
path, m, dry_run = args_tuple

if not ok:
  raise Exception(err_message)

# walk(dir=path, prune=prune, match_fn=match_fn(contains=m), dry=dry_run)
job = prune(match_fn=match_fn, dry_run=dry_run) # setup a job
walk(dir=path, job=job)


def walk(*, dir:str, job:Callable, stop_on_err=True):
  """walk is an interface for traversing a directory tree performing arbitrary prune job on all items.
  Pruning job receives only the path of a directory item from walk and performs actions. 
  It informs walk if it has encountered an error or not by returning a status object.
  Walk will continue is status is None or its err_m property is non-empty.
  Then walk implements a stop on error crank which instructs it to continue regardless of errors.
  By default, walk will quit upon encountering an error. In other words, the prune program is in charge
  of what happens in this case. It should return an error status if the execution shouldn't go further.
  Walk will simply display the error message contained in the status object and quit.
  """
  for path, dirs, f_names in os.walk(Path(dir), topdown=True):
    for f_name in f_names + dirs:
      status = job(Path(path) / f_name)
      # Job will only recieve a fully qualified name of a resource and no more to do it's job
      if status and 'err_m' in status:
        if status['err_m'] and stop_on_err: print(status['err_m']); return
      else: raise Exception('Incorrect error interface in status object')





# walk(dir=path, pruner=prune, match_fn=match_fn(endswith=m), dry=dry_run)
# walk(dir=path, pruner=prune, match_fn=match_fn(startswith=m), dry=dry_run)
# walk(
#   dir=path,
#   pruner=prune,
#   dry=dry_run,
#   match_fn=match_fn(match_fn=match_fn_test, match_str=m),
# )



# default is --contains
# --ends|--endswith|-e, --starts|--startswith|-s, 
# --contains|--find|--search|--index|-c|-f|-S|-i
# /?|--help|-h
# No commands - refer them to run help command