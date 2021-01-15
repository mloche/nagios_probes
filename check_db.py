#!/bin/python3

from random import randint
import sys

UNKNOWN = 0
OK = 1
WARNING = 2
CRITICAL = 3

status_code=randint(0,3)
sys.stdout.write("DB is OK! ")
sys.exit(1)
