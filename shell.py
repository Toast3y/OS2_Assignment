# Very basic Posix shell
#Editor: Chris Dunne
#Ver: 1
#Date: 15/12/2013
import os
import sys
import readline
import shlex
import glob

prompt = "sh>> "

def copyright():
  sys.stderr.write("""
Copyright (C) 2012-13 Brian Gillespie
This program comes with ABSOLUTELY NO WARRANTY; This is free
software, and you are welcome to redistribute it under certain
conditions; Type "copyright" or "license" for more information.
""" + "\n")
  return True

# Parsed splitting of input into constituent arguments
def parse(cmd):
  return shlex.split(cmd)

def internal(argv):
  cmd = argv[0]
  if cmd == "copyright":
    return copyright()

  return False

# Execute an execute command (i.e. run a  program on disk)
# If this succeeds it never returns
def execute(cmd, argv):
  try:
    os.execv(cmd, argv)
  except OSError: pass

def call(argv):
  if os.fork() == 0:
    cmd = argv[0]
	
	
    for argument in argv:
	  if '*' in argument:
	    #Implementation of file globbing
	    #Simply replaces arguments using pythons glob scripts
	    #Deletes the argument with the wild card after, so it'll probably fetch the first thing it finds
	    argv.extend(glob.glob(argument))
		argv.remove(argument)
	  elif '>' in argument:
	    #Output Redirection into files
	    fd = os.open(argv[(argv.index(argument))+1], os.O_CREAT | os.O_TRUNC | os.O_RWDR)
		os.dup2(fd, 1)
	  elif '<' in argument:
	    #Input Redirection into files
		fd = os.open(argv[(argv.index(argument))+1], os.O_RDONLY)
		os.dup2(fd, 0)
	
    if '/' in cmd:
      # Relative or absolute path specified
      execute(cmd, argv)
    else:
      for dir in os.getenv('PATH').split(':'):
        # Keep trying each directory in PATH until we find it
        execute(dir + '/' + cmd, argv)

    # If we get here then execution has failed
    sys.stderr.write('Unrecognised command: ' + cmd + '\n')
    os._exit(1)
  else:
    #Cause the shell to wait if there's no ampersand in the parsed arguments
    if not '&' in argv:
      os.wait()
	  
	  

# Read, print, eval, loop (REPL)
copyright()
while True:
  try:
    cmd = input(prompt).strip()
    if cmd == "":
      # Empty command so just prompt again
      pass
    elif cmd == "exit":
      # Exit the shell
      break
    else:
      argv = parse(cmd)
      if not internal(argv):
        call(argv)
  except EOFError:
      # User has pressed Ctrl-D
    break
