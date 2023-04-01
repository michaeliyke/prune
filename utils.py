from pathlib import Path
from typing import List, Tuple, Dict

ERRS = {
    0: 'Err_InternalError',
    1: 'Err_Path_ArgMissing',
    2: 'Err_Match_ArgMissing',
    3: 'Err_DryRun_CommandDuplicate',
    4: 'Err_Resource_NotFound',
    5: 'Err_UnknownArgFound',
    6: 'Err_Value_Mismatch',
    7: 'Err_Data_Mismach',
  }

ERRS.update({
  # Missing
    10: 'Err_Expected',
    11: 'Err_Command_Expected',
    12: 'Err_Token_Expected',
    13: 'Err_Option_Expected',
    14: 'Err_Flag_Expected',
    15: 'Err_Argument_Expected',
    16: 'Err_Input_Expected',

  # Missing
    20: 'Err_Missing',
    21: 'Err_Command_Missing',
    22: 'Err_Token_Missing',
    23: 'Err_Option_Missing',
    24: 'Err_Flag_Missing',
    25: 'Err_Argument_Missing',
    26: 'Err_Input_Missing',

    # Duplicate
    30: 'Err_Duplicated',
    31: 'Err_Command_Duplicated',
    32: 'Err_Token_Duplicated',
    33: 'Err_Option_Duplicated',
    34: 'Err_Flag_Duplicated',
    35: 'Err_Argument_Duplicated',
    36: 'Err_Input_Duplicated',

    # Notfound
    40: 'Err_Notfound',
    41: 'Err_Command_Notfound',
    42: 'Err_Token_Notfound',
    43: 'Err_Option_Notfound',
    44: 'Err_Flag_Notfound',
    45: 'Err_Argument_Notfound',
    46: 'Err_Input_Notfound',

    # Unknown
    50: 'Err_Unknown',
    51: 'Err_Command_Unknown',
    52: 'Err_Token_Unknown',
    53: 'Err_Option_Unknown',
    54: 'Err_Flag_Unknown',
    55: 'Err_Argument_Unknown',
    56: 'Err_Input_Unknown',

    # Unexpected
    60: 'Err_Unxpected',
    61: 'Err_Command_Unxpected',
    62: 'Err_Token_Unxpected',
    63: 'Err_Option_Unxpected',
    64: 'Err_Flag_Unxpected',
    65: 'Err_Argument_Unxpected',
    66: 'Err_Input_Unxpected',

    # Unrecognized
    70: 'Err_Unrecognized',
    71: 'Err_Command_Unrecognized',
    72: 'Err_Token_Unrecognized',
    73: 'Err_Option_Unrecognized',
    74: 'Err_Flag_Unrecognized',
    75: 'Err_Argument_Unrecognized',
    76: 'Err_Input_Unrecognized',

    # Invalid
    80: 'Err_Invalid',
    81: 'Err_Command_Invalid',
    82: 'Err_Token_Invalid',
    83: 'Err_Option_Invalid',
    84: 'Err_Flag_Invalid',
    85: 'Err_Argument_Invalid',
    86: 'Err_Input_Invalid',

    # Success
    100: 'Ok',
    101: 'Success',
    102: 'Complete',
    103: 'Done',

  })

def check_args_ext(args: List[str]) -> Dict:
  leng = len(args)
  if leng == 1: return create_err(err_id=1, err_m='Missing \'path\' argument')
  if leng == 2: return create_err(err_id=2, err_m='Missing \'match\' argument')
  known_commands = ['--dry-run', '-d'] # shall be read from file
  
  check_unknown_command(args[3:], known_commands)
  if '--dry-run' in args and '-d' in args:
    return create_err(err_id=3,err_m='Duplicate command for dry run')
  
  dry_run = '--dry-run' in args or '-d' in args
  args = list(filter(lambda c: c not in known_commands, args))
# TODO: Handle 0 argument - use . for dir and * for files
# TODO: Handle 1 argument - use [0] for dir and * for files

  path = Path(args[1]).resolve()
  match = args[2]
  if not path.exists():
    return create_err(err_m=f'{path} does not exist', err_id=4)

  return create_err(
    err_code='Success', 
    err_id=101, path=path, 
    match=match, dry_run=dry_run,
    )
  

def check_args(args: List[str]) -> Tuple:
  leng = len(args)
  if leng == 1: err('Missing \'path\' argument')
  if leng == 2: err('Missing \'match\' argument')
  known_commands = ['--dry-run', '-d']
  
  check_unknown_command(args[3:], known_commands)
  if '--dry-run' in args and '-d' in args:err('Duplicate command for dry run')
  dry_run = '--dry-run' in args or '-d' in args
  args = list(filter(lambda c: c not in known_commands, args))
# TODO: Handle 0 argument - use . for dir and * for files
# TODO: Handle 1 argument - use [0] for dir and * for files
  path = Path(args[1]).resolve()
  match = args[2]
  if not path.exists(): err(f'{path} does not exist')
  args_tuple = path, match, dry_run
  
  return True, args_tuple, ''




def err(message: str):
  raise Exception(message)


def create_err(*, err_code=None, err_id=None, err_m='', extend={}, **kwargs):
  # Extension can be applied in two ways:
  # (1) By passing arbtrary kwargs
  # (2) By using extend=dict arg
  if err_id==None and err_code:
    pos = list(ERRS.values()).index(err_code)
    err_id = list(ERRS.keys())[pos]
  
  if err_code == None and isinstance(err_id, int):
    err_code = ERRS.get(err_id)
  
  if not err_code in ERRS.values() or not err_id in ERRS:
    return err_ext(err_id=0, err_code='Err_InternalError')

  err = err_ext(err_code=err_code, err_id=err_id, err_m=err_m)
  err.update(kwargs)
  err.update(extend)
  return err


def err_ext(*, err_code: str, err_id: int, err_m: str):
  if not err_code and err_id: err_code = ERRS.get(err_id)
  if not err_id and err_code:
    pos = list(ERRS.values()).index(err_code)
    err_id = list(ERRS.keys())[pos]

  return dict(
    err_m=err_m,
    err_code=err_code,
    err_id=err_id,
  )


def check_unknown_command_ext(args: List[str], known_commands: List[str]):
  for command in args:
    if not command in known_commands: 
      return err_ext(
        err_m=f'Unexpected input: \'{command}\'',
        err_code='Err_UnknownArgFound',
        )


def check_unknown_command(args: List[str], known_commands: List[str]):
  for command in args:
    if not command in known_commands: 
      err(f'Unexpected input: \'{command}\'')


def get_args_of(*, option: str, multiple: bool, args: List):
  # python -m pruning.list . .txt
  # args will be modified
  # if multiple, match args until a dash(-) is encountered
  # if not, option is the next match

  # match
  # a match is a single word without or within quotes or a sentence in quotes
  pass
