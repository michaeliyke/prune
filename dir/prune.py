import os
from pathlib import Path
from typing import Callable, List, Union

from send2trash import send2trash as trash

from pruning.utils import create_err


def err(message):
  raise Exception(message)

def check_match(*, match_fn, endswith, startswith, contains):
  filtr = list(filter(None, [match_fn, endswith, startswith, contains]))
  if len(filtr) > 1:
    err('Only one of \'match_fn|endswith|startswith|contains\' is allowed')

  if not filtr:
    err('One of \'match_fn|endswith|startswith|contains\' is required')
  
def prune(match_fn:Callable, dry_run=False, endswith='', startswith='', contains=''):
  """
    dry: dry-run bool
    endswith: str
    startswith: str
    contains: str
    match_fn: Callable
    Only one of match_fn, endswith, startswith, contains is allowed.
  """
  check_match(
    match_fn=match_fn,
    endswith=endswith,
    startswith=startswith,
    contains=contains,
  )
  
  def _job(fp: Path):
    """
    _job is the single critical functionality dependency of this module. This is where the particular
    defining task is performed. It expects and performs actions against only one resource at a time. 
    fp: is the fully qulified path of resource on the file system
    """
    # Filtering
    err_msg = "Matching failed with cirteria:  '{}'"
    if startswith and not fp.name.startswith(startswith):
      return create_err(err_id=90, err_m=err_msg.format('startswith'))

    if endswith and not fp.name.endswith(endswith):  
      return create_err(err_id=90, err_m=err_msg.format('endswith'))

    if contains and not fp.name.find(contains) > -1:  
      return create_err(err_id=90, err_m=err_msg.format('contains'))

    if match_fn:
      fail = match_fn(fp)
      if fail: return fail
    
    if fp.exists():
      if dry_run is not True:
        print(f'Moved to trash - {fp.name}')
        trash(fp)
      else:
        print(f'(dry-run) Moved to trash - {fp.name}')
    else:
      print(f'NotFound: {fp}', end='\t')

  return _job



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
      # status = prune(Path(path) / f_name, match_fn=match_fn, dry=dry==True)
      # Job will only recieve a fully qualified name of a resource and no more to do it's job
      status = job(Path(path) / f_name)
      if status and 'err_m' in status:
        if status['err_m'] and stop_on_err: print(status['err_m']); return
      else: raise Exception('Incorrect error interface in status object')


def match_fn(*, match_fn=None, test_str='', endswith='', startswith='', contains='')->dict:
  if match_fn and not test_str: 
    raise Exception("'fail_test' has not 'test_str'")

  def fn(fp: Path):
    nonlocal startswith, endswith, contains, match_fn, test_str
    message = "Matching failed with cirteria '{}'{{{}: {}}}" # eg 'contains'{nodemodules: .browserslistrc}
    ok = create_err(err_code='Ok')

    if startswith:
      if fp.name.startswith(startswith): return ok
      return create_err(err_id=90, err_m=message.format('startswith', startswith, fp.name))
    
    if endswith:
      if fp.name.endswith(endswith): return ok
      return create_err(err_id=90, err_m=message.format('endswith', endswith, fp.name))
    
    if contains:
      if fp.name.find(contains) > -1: return ok
      return create_err(err_id=90, err_m=message.format('contains', contains, fp.name))
    
    if match_fn:
      fail = match_fn(fp, match_str=test_str)
      if isinstance(fail, dict) and 'err_m' in fail:
        if not fail['err_m']: return ok
        return create_err(err_id=90, err_m=message.format(test_str, fp.name))
      return create_err(err_id=90, err_m='match_fn must return a correct error interface')
      
    return create_err(err_id=90, err_m='No validation criteria provided')

  return fn


def match_fn_test(fp: Path, *, test_str) -> dict:
  m = "Matching failed with cirteria:  '{}'".format(test_str)
  v = create_err(err_code='Ok') if fp.name.find(test_str) >= 0 else create_err(err_id=90, err_m=m)
  return v