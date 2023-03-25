from pathlib import Path
from typing import List, Tuple


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


def check_unknown_command(args: List[str], known_commands: List[str]):
  for command in args:
    if not command in known_commands: 
      err(f'Unexpected input: \'{command}\'')

