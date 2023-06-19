COMMAND FORMAT

# Prune files
 python -m pruning.prune_files . ._
 python -m pruning.prune_files . .txt
 python -m pruning.prune_files . __pycache__
 python -m pruning.move . .txt OR python -m pruning.move . .txt ["C:\Program Files" C:\ProgramData Temp Tem Test]
 python -m pruning.list . .txt OR python -m pruning.move . .txt ["C:\Program Files" C:\ProgramData Temp Tem Test]
 python -m pruning.copy . .txt OR python -m pruning.copy . .txt ["C:\Program Files" C:\ProgramData Temp Tem Test]

---------------------------------
array=.x .y .z|.x,.y,.z

list: list|list --all|-a - default
list-type: list --type|-t array
list-except: list --except|-e array
list-not-type: same as above
list-dirs: list --dirs|-d
 
# Prune folders -  coming soon

# copy arbitrary -  coming soon
 
 # Move arbitrary - coming soon
 # . moves an fs object to a stated or a temp location within first parent - directlory tree is maintained for clarity

 # Prune arbitrary - current - coming soon

 # FOR TESTING PURPOSES:
 # python -m pruning.prune  -m pruning.copy . .txt C:\ProgramData Temp Tem Test "C:\Program Files"
 # python -m pruning.list  -m pruning.copy __pycache__ . .txt C:\ProgramData Temp Tem Test "C:\Program Files"

 ga --delete user mails phones --fry --force --cascade true --keep-track --log track --delete-type safe

 ga -d user mails phones -fF -c true -k -l track -D safe

-d: user mails phones
-c: true
-l: track
-D safe
# flags: -fFk
# options: -d -c -l -D
_pos: {flgs: {}, opts: {}, rgs: {}, t_wrds: 10}

postional: ['a', '25', 'xy'] # Three postional arguments
[instruction]positions - 3 - Unnecessary - recognize all inputs as positional arg until a flag or an option 