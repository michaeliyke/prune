import os
from pathlib import Path
from typing import Callable, List, Union

from send2trash import send2trash as trash

from pruning.utils import create_err


def err(message):
  raise Exception(message)

def check_match(*, matcher, endswith, startswith, contains):
  filtr = list(filter(None, [matcher, endswith, startswith, contains]))
  if len(filtr) > 1:
    err('Only one of \'matcher|endswith|startswith|contains\' is allowed')

  if not filtr:
    err('One of \'matcher|endswith|startswith|contains\' is required')
  

def prune(fp: Path, *, dry=False, fail_match, endswith='', startswith='', contains=''):
  """fp: file Path
  dry: dry-run bool
  endswith: str
  startswith: str
  contains: str
  matcher: Callable
  Only one of matcher, endswith, startswith, contains is allowed.
  """
  check_match(
    matcher=fail_match,
    endswith=endswith,
    startswith=startswith,
    contains=contains,
  )
  # Filtering
  err_msg = "Matching failed with cirteria:  '{}'"
  if startswith and not fp.name.startswith(startswith):
    return create_err(err_id=90, err_m=err_msg.format('startswith'))

  if endswith and not fp.name.endswith(endswith):  
    return create_err(err_id=90, err_m=err_msg.format('endswith'))

  if contains and not fp.name.find(contains) > -1:  
    return create_err(err_id=90, err_m=err_msg.format('contains'))

  if fail_match:
    fail = fail_match(fp)
    if fail: return fail
  
  if fp.exists():
    if dry is not True:
      print(f'Moved to trash - {fp.name}')
      trash(fp)
    else:
      print(f'(dry-run) Moved to trash - {fp.name}')
  else:
    print(f'NotFound: {fp}', end='\t')



def walk(*, dir:str, pruner:Callable, matcher, dry=False):
  for path, dirs, f_names in os.walk(Path(dir), topdown=True):
    for f_name in f_names:
      status = pruner(Path(path) / f_name, matcher=matcher, dry=dry==True)
      if status and 'err_m' in status:
        if status['err_m__']: print(status['err_m']); return
      else: raise Exception('Incorrect error interface in status object')


def matcher(*, fail_test=None, test_str='', endswith='', startswith='', contains='')->dict:
  if fail_test and not test_str: 
    raise Exception("'fail_test' has not 'test_str'")

  def fn(fp: Path):
    nonlocal startswith, endswith, contains, fail_test, test_str
    message = "Matching failed with cirteria '{}': {}"
    ok = create_err(err_code='Ok')

    if startswith:
      if fp.name.startswith(startswith): return ok
      return create_err(err_id=90, err_m=message.format(startswith, fp.name))
    
    if endswith:
      if fp.name.endswith(endswith): return ok
      return create_err(err_id=90, err_m=message.format(endswith, fp.name))
    
    if contains:
      if fp.name.find(contains) > -1: return ok
      return create_err(err_id=90, err_m=message.format(contains, fp.name))
    
    if fail_test:
      fail = fail_test(fp, match_str=test_str)
      if isinstance(fail, dict) and 'err_m' in fail:
        if not fail['err_m']: return ok
        return create_err(err_id=90, err_m=message.format(test_str, fp.name))
      return create_err(err_id=90, err_m='Fail_test fn must return a correct error interface')
      
    return create_err(err_id=90, err_m='No validation criteria provided')

  return fn


def matcher_test(fp: Path, *, test_str) -> dict:
  m = "Matching failed with cirteria:  '{}'".format(test_str)
  v = create_err(err_code='Ok') if fp.name.find(test_str) >= 0 else create_err(err_id=90, err_m=m)
  return v