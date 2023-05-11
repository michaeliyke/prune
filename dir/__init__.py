# import os
# import pathlib
# from os import PathLike
# from typing import Callable, Union

# from pruning.pruner import prune


# def prune_dirs(directory: Union[str, PathLike], cb: Callable):
#   for _, dirs, _ in os.walk(pathlib(directory), topdown=True):
#     cb(dirs)

