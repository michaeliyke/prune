import os
from pathlib import Path
from typing import Callable, List, Union

from send2trash import send2trash as trash


def err(message):
  raise Exception(message)

def check_match(*, matcher, endswith, startswith, contains):
  filtr = list(filter(None, [matcher, endswith, startswith, contains]))
  if len(filtr) > 1:
    err('Only one of \'matcher|endswith|startswith|contains\' is allowed')

  if not filtr:
    err('One of \'matcher|endswith|startswith|contains\' is required')
  
  
def prune(fp: Path, *, dry=False, matcher, endswith='', startswith='', contains=''):
  """fp: file Path
  dry: dry-run bool
  endswith: str
  startswith: str
  contains: str
  matcher: Callable
  Only one of matcher, endswith, startswith, contains is allowed.
  """
  check_match(
    matcher=matcher, 
    endswith=endswith, 
    startswith=startswith, 
    contains=contains,
  )
  # Filtering
  if startswith and not fp.name.startswith(startswith):  return
  if endswith and not fp.name.endswith(endswith):  return
  if contains and not fp.name.find(contains) > -1:  return
  if matcher and not matcher(fp): return
  
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
      pruner(
        Path(path) / f_name,
        matcher=matcher,
        dry=dry==True,
      )


def matcher(*, matcher=None, match_str='', endswith='', startswith='', contains=''):
  if matcher and not match_str: err('\'matcher\' has  no \'match_str\'')
  def fn(fp: Path):
    nonlocal startswith, endswith, contains, matcher, match_str
    if startswith: return fp.name.startswith(startswith)
    if endswith: return fp.name.endswith(endswith)
    if contains: return fp.name.find(contains) > -1
    if matcher: return matcher(fp, match_str=match_str)

  return fn


def matcher_test(fp: Path, *, match_str):
  return fp.name.find(match_str) >= 0