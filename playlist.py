import os
import glob

path = '/home/biot/Downloads/Songs/DnB/'

files = sorted(glob.glob(path + '*.mp3'), key=os.path.getctime)
tales = []

for file in files:
    _, tale = os.path.split(file)
    tales.append(tale)
    print(tale)

print(len(tales))

with open(path + 'DnB.txt', "w") as file:
    for tale in tales:
        file.write(tale)
        file.write('\n')


