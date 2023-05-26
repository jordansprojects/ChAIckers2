import unittest
import sys
import os


sys.path.append(os.getcwd() + '/..')
from index_table import *




table = IndexTable()
print("TESTING FOR BLACK:")
for location in range (32):
    print("from index location " + str(location) + " I can go to " + str(table.get_steps(location,BLACK)) + ".")
    print("from index location " + str(location) + " I can go to " + str(table.get_hops(location,BLACK)) + ".")

print("TESTING FOR WHITE:")
for location in range (32):
    print("from index location " + str(location) + " I can go to " + str(table.get_steps(location,WHITE)) + ".")
    print("from index location " + str(location) + " I can go to " + str(table.get_hops(location, WHITE)) + ".")


print("TESTING FOR KING:")
for location in range (32):
    print("from index location " + str(location) + " I can go to " + str(table.get_steps(location, WHITE_KING)) + ".")
    print("from index location " + str(location) + " I can go to " + str(table.get_hops(location, BLACK_KING)) + ".")

