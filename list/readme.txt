COMMAND FORMAT

# Prune files
 python -m pruning.prune_files . ._
 python -m pruning.prune_files . .txt
 python -m pruning.prune_files . __pycache__
 python -m pruning.move . .txt OR python -m pruning.move . .txt ["C:\Program Files" C:\ProgramData Temp Tem Test]
 python -m pruning.list . .txt OR python -m pruning.move . .txt ["C:\Program Files" C:\ProgramData Temp Tem Test]
 python -m pruning.copy . .txt OR python -m pruning.copy . .txt ["C:\Program Files" C:\ProgramData Temp Tem Test]
 
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
internal: {flag_pos: {}, opt_pos: {}, arg_pos: {}, total_words: 10, rebuilt: ''}