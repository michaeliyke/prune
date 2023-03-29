import sys
from typing import List
from copy import deepcopy
from itertools import pairwise

tool = 'ga'

FLAGS = {
  '-e': '--example',
  '--example': {'name': 'example', 'short': '-e'},
}

OPTIONS = {
  '-e': '--example',
  '--example': {'name': 'example', 'short': '-e', 'array': False, 'values': [True, False] }
}

def get_option(x: str):
  if not x in OPTIONS: raise Exception(f'Option \'{x}\' is not recognized')
  if x.startswith('--'): return OPTIONS[x]
  if x.startswith('-'): return OPTIONS[OPTIONS[x]]

def get_flag(x: str):
  if not x in FLAGS: raise Exception(f'Flag \'{x}\' is not recognized')
  if x.startswith('--'): return FLAGS[x]
  if x.startswith('-'): return FLAGS[FLAGS[x]]

def get_args_of(*, option: str, multiple: bool, args: List):
  # python -m pruning.list . .txt
  # get_args_of('-m', multiple=true, args='python -m pruning.list . .txt')
  
  
  # args will be modified
  # if multiple, match args until a dash(-) is encountered
  # if not, option is the next match

  # match
  # a match is a single word without or within quotes or a sentence in quotes
  pass


def parse():
  sys.argv.pop(0)
  sys.argv.insert(0, tool)
  args = deepcopy(sys.argv[1:])

  options, flags = [], []
  option_names, flag_names = [], []

  element: str
  # Harvest options and flags 
  for i, element in enumerate(deepcopy(args)):
    if element.startswith('-') or element.startswith('--'):
      if element in OPTIONS:
        # expand shortened options and proceed
        option = get_option(element)
        args.pop(i)
        args.insert(i, f'--{option}')
        options.append(option)
        continue

      # The case of fals are two - a full flag and short flags assumed combined
      # Tackle full flag
      if element in FLAGS:
        # expand shortened options and proceed
        flag = get_flag(element)
        args.pop(i)
        args.insert(i, f'--{flag}')
        flags.append(flag)
        continue

      # Tackle short flags, assumed combined
      # But first ensure that element is an actual set of recognized flags
      cpy = [x for x in element[1:] if f'-{x}' in FLAGS]
      if len(cpy) != len(element[1:]): continue
      
      # Expand the flags to individual components
      # Each short flag can only be one character besides the dash(-)
      args.pop(i)
      for ii, token in enumerate(element[1:]):
        flag = get_flag(f'-{token}')
        args.insert(i+ii, f'--{flag}')
        flags.append(flag)
  
  # Check flag repeats
  for flag in flags:
    if flag['name'] in flag_names: raise Exception(f'Flag \'--{flag}\' duplicated')
    flag_names.append(f'--{flag["name"]}')

  # Check option repeats
  for option in options:
    if option['name'] in option_names: raise Exception(f'Option \'--{option}\' duplicated')
    flag_names.append(f'--{option["name"]}')
    
  # VALIDATE FLAGS and OPTIONS
  # ensure a flag goes before a flag, an option or is at the end - 
  # flag cannot go just before an argument
  
  # The first argument must be a flag or an option
  if len(args) > 0:
    if args[0] not in option_names and args[0] not in flag_names:
      raise Exception('Unrecognized argument \'{args[0]}\' ')
  
    # The last argument must either be a flag or an option argument
    if args[-1] in option_names:
      raise Exception('Option \'{args[-1]}\' expects input(s)')

  t: str
  nxt: str
  for t, nxt in pairwise(args):
    # A flag can go before a flag or an option
    if t in flag_names and nxt in flag_names: continue
    if t in flag_names and nxt not in flag_names:
      # Flag can go before an option
      if nxt in option_names: continue
      raise Exception('Unrecognized argument \'{nxt}\' ')

    # An option cannot go before a flag or another option
    if t in option_names:
      if nxt in option_names: 
        raise Exception('Unexpected option\'{nxt}\'')
      if  nxt in flag_names: 
        raise Exception('Unexpected flag \'{nxt}\'')
      
  # A non-array option cannot receieve multiple arguments
  items = {}
  print(args)
  return items

# I think there's a thing or two about writing code in the morning. I mean early enough
# in the morning when your brain still answers yes to most of your questions before bating.
# Jokes apart, but it seems to me that the morning energy is kinda different generally,
# nomatter which area. @cosmas, @broiyke, and @ebenezer what do you think. 
# Did you notice that

# #coding-ideas: One way to say what something is not is to sy what it is,
# another way to say what something is, is to say what it is not. 
# Sometimes, you can have it both ways, but you can never be locked out of both. 
# Sometimes, it's easy to describe a situation in code, but sometimes, it's not. 
# So, one way to describe somethig is to just say what it is. But another way to
# describe the same thing is to say what it is not in a way that connects the dots. 
# In my experience, you can have it one way or both ways, but never neither way!
# Think nature does some good here.