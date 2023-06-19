COMMAND FORMAT

# Prune files
 python -m pruning.prune_files . ._
 python -m pruning.prune_files . .txt
 python -m pruning.prune_files . __pycache__

# move or copy 
# - sources and destinations
python -m pruning.move . .txt OR python -m pruning.move . -s .txt -d "dir1" dir2 Temp Tem Test
python -m pruning.copy . .txt OR python -m pruning.copy . -s .txt -d "dir1" dir2 Temp Tem Test



 # Prune folders - coming soon

 # Prune arbitrary - coming soon
# copy arbitrary -  coming soon
 
 # Move arbitrary - current - coming soon
 # . moves an fs object to a stated or a temp location within first parent - directlory tree is maintained for clarity