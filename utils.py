from pathlib import Path
from typing import List, Tuple, Dict

ERRS = {
    0: 'Err_InternalError',
    1: 'Err_Path_ArgMissing',
    2: 'Err_Match_ArgMissing',
    3: 'Err_DryRun_CommandDuplicate',
    4: 'Err_Resource_NotFound',
    5: 'Err_UnknownArgFound',
    10: "Success",
  }

def check_args_ext(args: List[str]) -> Dict:
  leng = len(args)
  if leng == 1: return create_err(err_id=1, err_message='Missing \'path\' argument')
  if leng == 2: return create_err(err_id=2, err_message='Missing \'match\' argument')
  known_commands = ['--dry-run', '-d'] # shall be read from file
  
  check_unknown_command(args[3:], known_commands)
  if '--dry-run' in args and '-d' in args:
    return create_err(err_id=3,err_message='Duplicate command for dry run')
  
  dry_run = '--dry-run' in args or '-d' in args
  args = list(filter(lambda c: c not in known_commands, args))
# TODO: Handle 0 argument - use . for dir and * for files
# TODO: Handle 1 argument - use [0] for dir and * for files

  path = Path(args[1]).resolve()
  match = args[2]
  if not path.exists():
    return create_err(err_message=f'{path} does not exist', err_id=4)

  return create_err(
    err_code='Success', 
    err_id=10, path=path, 
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


def create_err(*, err_code=None, err_id=None, err_message='', **kwargs):
  if err_id==None and err_code:
    pos = list(ERRS.values()).index(err_code)
    err_id = list(ERRS.keys())[pos]
  
  if err_code == None and isinstance(err_id, int):
    err_code = ERRS.get(err_id)
  
  if not err_code in ERRS.values() or not err_id in ERRS:
    return err_ext(err_id=0, err_code='Err_InternalError')

  err = err_ext(err_code=err_code, err_id=err_id, err_message=err_message)
  err.update(kwargs)
  return err


def err_ext(*, err_code: str, err_id: int, err_message: str):
  if not err_code and err_id: err_code = ERRS.get(err_id)
  if not err_id and err_code:
    pos = list(ERRS.values()).index(err_code)
    err_id = list(ERRS.keys())[pos]

  return dict(
    err_message=err_message,
    err_code=err_code,
    err_id=err_id,
  )


def check_unknown_command_ext(args: List[str], known_commands: List[str]):
  for command in args:
    if not command in known_commands: 
      return err_ext(
        err_message=f'Unexpected input: \'{command}\'',
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

  