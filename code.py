import sys
import subprocess
import os
import time
# CODE.PY
# This program is the 'I'm to lazy to think for myself' way to run,
# compile, debug, etc

help_text = """Simply pass in a file or link
this will probably do whatever you were planning on doing
passing in a directory will look for a make file or similar to deal with
Currently compiles/runs C,java,python,go,php
bascially this program just applies sensical defaults so you don't
have to remember a bunch of random ass options and optimizations

\033[96m--debug\033[97m will open the debug evn for the respective langage
or tell you you're stupid because you tried debugging
a ling or some shit

\033[96m--fuzz\033[97m will fuzz your input program if possible

\033[96m-v\033[97m will output all choices the program makes

\033[96m-h\033[97m will display this output

\033[96m--gcc\033[97m will set set C to use GCC instead of clang, this can
be made defalut by editing code.py pretty easily

Seaching for \033[94mXCONFX\033[97m in the code will show anywhere a comment
can be removed switched to alter for other configs
"""
flaglist = ['-h', '--gcc', '-v', '-fuzz', '--debug']

###################


# To start out we need to parse to see what the argument needs us to do
def GetExtension(filestr):
    extension = ''
    keepChars = False
    for char in filestr:
        if char is '.':
            keepChars = True
        if keepChars is True:
            extension = extension + char
    return(extension)

# First the argument is checked to be a local file or link
# if it is it's extension is used to figgure out what to do next (ie .c, .py)


# if .c the file is parsed to see if the math library is included
def CCode(file, filestr):
    # UNCOMMENT THIS to change to GCC
    # c_compile_str = "gcc"
    c_compile_str = "clang"
    if '--gcc' in sys.argv:
        c_compile_str = "gcc"
    if contains_math(file):
        c_compile_str = c_compile_str + " -lm -O3 "
    c_compile_str = c_compile_str + " " + filestr + " -o "
    c_compile_str = c_compile_str + filestr[:-2]
    my_env = os.environ
    print(c_compile_str)
    p = subprocess.Popen(c_compile_str, env=my_env, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        # Filter stdout
        for line in iter(p.stdout.readline, ''):
            sys.stdout.flush()
            # Print status
            print(">>> " + line.rstrip())
            sys.stdout.flush()
    except Exception:
        sys.stdout.flush()
    while p.poll() is None:
        # Process hasn't exited yet, let's wait some
        time.sleep(0.5)
    return_code = p.returncode

    if return_code == 1:
        print("\033[91mCompilation not sucessful!")
    if return_code == 0:
        runstr = 'xterm -hold -e ./' + filestr[:-2]
        p = subprocess.call(runstr, env=my_env, shell=True)
        print(p)
    # if compilation was sucessful (assumed by a return code of 0)
    # the program will be ran


# if file is .py see if there is a print line, and if so parse it for perens
# this is the poor mans way of checking python version

# if file is .java then we have some work to do

# if we have .go

# Ruby...

# C#

# PHP

def contains_math(file):
    for line in file:
        if line == "#include \"math.h\"" or "#include <math.h>":
            return True

###
# Main
###


inputlist = []
if len(sys.argv) == 1:
    print(help_text)
    exit(1)
if '-h' in sys.argv:
    print(help_text)
    exit(1)
for item in sys.argv:
    if item not in flaglist:
        inputlist.append(item)
filestr = inputlist[1]
file = open(filestr, "r")
extension = GetExtension(filestr)
if extension == ".c":
    CCode(file, filestr)
