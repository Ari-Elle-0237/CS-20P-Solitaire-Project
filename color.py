# color.py
# Steve J. Hodges, Cabrillo College, sthodges@cabrillo.edu
# first test of colors; uses tput-ncurses-bash


import os

WHITE = 7
BLACK = 0
GREEN = 2
RED = 1

def color(n):
    # source : https://stackoverflow.com/questions/6537487/changing-shell-text-color-windows
    # does not seem to work, but does get the error message to go away which is good enough for now
    os.system(f"tput setaf {n}") if os.name == 'posix' else os.system(f'color {n}')

def fgcolor(n):
    color(n)

def bgcolor(n):
    os.system(f"tput setab {n}") if os.name == 'posix' else os.system(f'color {n}')

def nocolor(n):
    os.system("tput sgr0") if os.name == 'posix' else os.system(f'color {n}')
    
