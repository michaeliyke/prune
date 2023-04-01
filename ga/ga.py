import sys
from typing import List
from copy import deepcopy
from itertools import pairwise

from pruning.utils import create_err as err

tool = 'ga'

FLAGS = {
  '-m': '--merge',
  '--merge': {'name': 'merge', 'short': '-m'},
  '-f': '--force',
  '--force': {'name': 'force', 'short': '-f'},
  '-g': '--global',
  '--global': {'name': 'global', 'short': '-g'},
  '--tags': {'name': 'tags', 'short': ''},
  '--allow-unrelated-histories': {'name': 'allow-unrelated-histories', 'short': ''},
  
  # more
  '-F': '--fry',
  '--fry': {'name': 'fry', 'short': '-F'},
  '-k': '--keep-track',
  '--keep-track': {'name': 'keep-track', 'short': '-k'},

}

OPTIONS = {
  '-e': '--example',
  '--example': {'name': 'example', 'short': '-e', 'array': False, 'values': [True, False] },
  '-t': '--touch',
  '--touch': {'name': 'touch'},

  # more
  '-D': '--delete-type',
  '--delete-type': {'name': 'delete-type'},
  '-d': '--delete',
  '--delete': {'name': 'delete', 'array': True},
  '-c': '--cascade',
  '--cascade': {'name': 'cascade'},
  '-l': '--log',
  '--log': {'name': 'log'},
}

def get_option(x: str, OPTIONS: dict):
  if not x in OPTIONS: return err(err_id=73, err_m=f'Option \'{x}\' is not recognized')
  if x.startswith('--'): return OPTIONS[x]
  if x.startswith('-'): return OPTIONS[OPTIONS[x]]

def get_flag(x: str, FLAGS: dict):
  if not x in FLAGS: return err(err_id=74, err_m=f'Flag \'{x}\' is not recognized')
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


def parse() -> dict:
  sys.argv.pop(0)
  sys.argv.insert(0, tool)
  args = deepcopy(sys.argv[1:])

  # FLAGS General Initial Validation
  key: str
  for key in FLAGS.keys(): 
    # Handle omission of the dash(-) in naming an flag
    if key[0] != '-': return err(err_m='flag names must start with a dash: \'-\'', err_id=84)
    # Dissallow having a key in both options and flags
    if key in OPTIONS:
      return err(err_id=30, err_m=f'Same key \'{key}\' found in OPTIONS and FLAGS')
    
    # Handle the short flag form
    # The long version of a short flag must exist
    if key.startswith('-') and key.count('-') == 1 and len(key) == 2:
      if not FLAGS[key] in FLAGS:
        return err(err_id=84, err_m=f'Invalid flag \'{key}\' detected in settings')
      # Ensure that both name and short props of the flag dict are present
      fl = FLAGS[key]
      if not (isinstance(FLAGS[fl], dict) and 'name' in FLAGS[fl] and 'short' in FLAGS[fl]):
        return err(err_id=84, err_m=f'Invalid flag \'{key}\' detected in settings')
      if FLAGS[fl]['name'] == fl[2:] and FLAGS[fl]['short'] != key:
        return err(err_id=6, err_m=f'Flag \'{key}\' does not match it\'s long form')      
    # Handle the long flag form
    # a full flag is 3 characters and above
    # flag value is dict with name same as the name of the flag without the dashes(--)
    if key.startswith('--'):
      if len(key) < 3:
        return err(err_id=84, err_m=f'Invalid flag \'{key}\' detected in settings')
      if not (isinstance(FLAGS[key], dict) and FLAGS[key]['name'] == key[2:]):
        return err(err_id=84, err_m=f'Invalid flag \'{key}\' detected in settings')

  for key in OPTIONS.keys():
    # Handle omission of the dash(-) in naming an option
    if key[0] != '-': return err(err_m='option names must start with a dash: \'-\'', err_id=83)
    # Handle the short option form
    # The long version of a short option must exist
    if key.startswith('-') and key.count('-') == 1 and len(key) == 2:
      if not OPTIONS[key] in OPTIONS:
        return err(err_id=83, err_m=f'Invalid option \'{key}\' detected in settings')
      # Ensure that both name and short props of the option dict are present
      fl = OPTIONS[key]
      if not isinstance(OPTIONS[fl], dict) and 'name' in FLAGS[fl]:
        return err(err_id=83, err_m=f'Invalid option \'{key}\' detected in settings')
      if not OPTIONS[fl]['name'] == fl[2:]:
        return err(err_id=6, err_m=f'Option \'{key}\' does not match it\'s long form')      
    # Handle the long option form##############################
    # a full option is 3 characters and above
    # option value is dict with name same as the name of the option without the dashes(--)
    if key.startswith('--'):
      if len(key) < 3:
        return err(err_id=83, err_m=f'Invalid option \'{key}\' detected in settings')
      if not (isinstance(OPTIONS[key], dict) and OPTIONS[key]['name'] == key[2:]):
        return err(err_id=84, err_m=f'Invalid option \'{key}\' detected in settings')
      


  options, flags = [], []
  option_names, flag_names = [], []
  _OPTIONS = deepcopy(OPTIONS)
  _FLAGS = deepcopy(FLAGS)

  element: str
  # Harvest user options and flags 
  for i, element in enumerate(deepcopy(args)):
    if element.startswith('-') or element.startswith('--'):
      if element in _OPTIONS:
        # obtain a proper reprsentation of the option update the user args with the full/expanded name
        option = get_option(element, _OPTIONS)
        # Check option repeats
        if f'--{option["name"]}' in option_names: 
          return err(err_id=33, err_m=f'Option \'--{option["name"]}\' duplicated')
        option_names.append(f'--{option["name"]}')
        args.pop(i)
        args.insert(i, f'--{option["name"]}')
        options.append(option)
        continue

      # The cases of a flag are two variants names: (a) full flags (b) short flags
      # Case: full flag
      if element in _FLAGS:
        # obtain a proper reprsentation of the flag update the user args with the full/expanded name
        flag = get_flag(element, _FLAGS)
        # Check flag repeats
        if '--'+flag['name'] in flag_names:
          return err(err_id=34, err_m=f'Flag \'--{flag["name"]}\' duplicated')
        flag_names.append('--'+flag['name'])
        args.pop(i)
        args.insert(i, '--'+flag['name'])
        flags.append(flag)
        continue

      # Tackle short flags, a combined set of flags is assumed
      # But first ensure that element is an actual set of recognized flags
      cpy = [x for x in element[1:] if f'-{x}' in _FLAGS]
      # Otherwise, unrecognized set flags pass for an argument and so is skipped
      if len(cpy) != len(element[1:]): continue #
      
      # Expand the flags to individual components
      # Each short flag can only be one character besides the dash(-)
      args.pop(i)
      for ii, token in enumerate(element[1:]):
        flag = get_flag(f'-{token}', _FLAGS)
        # Check flag repeats
        if '--'+flag['name'] in flag_names:
          return err(err_id=34, err_m=f'Flag \'--{flag["name"]}\' duplicated')
        flag_names.append('--'+flag['name'])
        args.insert(i+ii, f'--{flag["name"]}')
        flags.append(flag)
  
  
  # # Check flag repeats
  # for flag in flags:
  #   if f'--{flag["name"]}' in flag_names: 
  #     return err(err_id=34, err_m=f'Flag \'--{flag}\' duplicated')
  #   flag_names.append(f'--{flag["name"]}')

  # Check option repeats
  # for option in options:
  #   if f'--{option["name"]}' in option_names: 
  #     return err(err_id=33, err_m=f'Option \'--{option}\' duplicated')
  #   option_names.append(f'--{option["name"]}')
    
  # VALIDATE FLAGS and OPTIONS
  # ensure a flag goes before a flag, an option or is at the end - 
  # flag cannot go just before an argument
  
  # The first argument must be a flag or an option
  # The last argument must either be a flag or an option argument
  if len(args) > 0:
    if args[-1] in option_names:
      return err(err_id=16, err_m=f'Option \'{args[-1]}\' expects input(s)')
    if args[0] not in option_names and args[0] not in flag_names:
      return err(err_id=75, err_m=f'Unrecognized argument \'{args[0]}\'')
  
  t: str
  nxt: str
  for t, nxt in pairwise(args):
    # A flag can go before a flag or an option
    if t in flag_names and nxt in flag_names: continue
    if t in flag_names and nxt not in flag_names:
      # Flag can go before an option
      if nxt in option_names: continue
      return err(err_id=75, err_m=f'Unrecognized argument \'{nxt}\'')

    # An option cannot go before a flag or another option
    if t in option_names:
      if nxt in option_names:
        return err(err_id=63, err_m=f'Unexpected option\'{nxt}\'')
      if  nxt in flag_names:
        return err(err_id=64, err_m=f'Unexpected flag \'{nxt}\'')

  # items = {
  #   'options': option_names,
  #   'flags': flag_names,
  #   'details': parse_args_details(args=args, _OPTIONS=_OPTIONS, _FLAGS=_FLAGS),
  # }
  # return {
  # **err(err_code='Ok', err_id=100),
  # **items,
  # }
  parsed = parse_args_details(args=args, _OPTIONS=_OPTIONS, _FLAGS=_FLAGS)

  return err(
    err_code='Ok', 
    err_id=100, 
    options=option_names,
    flags=flag_names,
    extend=parsed,
    )



def parse_args_details(*, args: List[str], _OPTIONS: dict, _FLAGS: dict):
  details = {}
  o = ''
  _pos = {'opts': {}, 'flgs': {}, 'rgs': {}, 't_wrds': len(args),}
  _poss = {x: y for x, y in enumerate('-'*len(args))}
  opt_args = [] # store arguments of each option
  index = -1
  while len(args) != 0:
    index += 1
    p = args.pop(0)

    # option
    if p in _OPTIONS: # or it is the end
      # Register current set of arguments under the given option and empty opt_args
      if opt_args:
        details[o] = opt_args
        opt_args = []
      # _pos['opts'][index] = p
      _poss[index] = ['o', p]
      o = p
      continue
    # flags
    if p in _FLAGS: 
      # _pos['flgs'][index] = p; 
      _poss[index] = ['f', p]
      continue
    # plain argument
    opt_args.append(p)
    # _pos['rgs'][index] = p;
    _poss[index] = ['a', p]
    if len(args) == 0:
      details[o] = opt_args
  details['_poss'] = _poss

  return details

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
# 

# It is not enough that we build products that function. We also need to build
# products that bring joy and excittment, pleasure, and fun, and yes, beauty to 
# people's lives - Don Norman
# 
# 
# If we want users to like our software, we should design it to behave like a likeable
# person: respectful, generous and helpful. 
# - Alan Cooper, Software Designer and Programmer


# Wireframing is the most important step of any design. It forces you to think 
# about how things will be organized  and function.

# The time it takes to make a decision increases as the number of alternatives increases
# - William Edmund Hick