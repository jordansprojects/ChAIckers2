from index_table import *

table = IndexTable()


print("TESTING FOR BLACK:")
for location in range (32):
    print("from index location " + str(location) + " I can go to " + str(table.get_steps(BLACK, location)) + ".")
    print("from index location " + str(location) + " I can go to " + str(table.get_hops(BLACK, location)) + ".")

print("TESTING FOR WHITE:")
for location in range (32):
    print("from index location " + str(location) + " I can go to " + str(table.get_steps(WHITE, location)) + ".")
    print("from index location " + str(location) + " I can go to " + str(table.get_hops(WHITE, location)) + ".")


print("TESTING FOR KING:")
for location in range (32):
    print("from index location " + str(location) + " I can go to " + str(table.get_steps(WHITE_KING, location)) + ".")
    print("from index location " + str(location) + " I can go to " + str(table.get_hops(BLACK_KING, location)) + ".")

