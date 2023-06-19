import os
from os import PathLike
from pathlib import Path
from typing import Callable, Union


def walk(directory: Union[str, PathLike], cb: Callable):
  for current_path, dirs, files in os.walk(Path(directory), topdown=True):
    cb(files, dirs, current_path)
