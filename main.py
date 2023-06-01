from Utilities import practiscore as ps
from Utilities import filehandler as fh
from config import *

print("Let's get this thing on the hump!")
print()

path = root + "/Data/txtFiles/"
fh.convert_to_json(path)

# ps.download_match(199230)

print()
print('Target Destroyed')
