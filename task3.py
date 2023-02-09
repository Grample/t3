import os
import sys
from threading import Thread
import logging
from pathlib import Path
import re
from shutil import unpack_archive, move

StartPos = ""
if len(sys.argv) > 1:
    StartPos = sys.argv[1]
else:
    print("No arguments passed")
    exit(22)

if not Path(StartPos).exists:
    print('Folder not exists')
    exit(20)

Images = os.path.join(StartPos, 'images')
Documents = os.path.join(StartPos, 'documents')
Musics = os.path.join(StartPos, 'audio')
Videos = os.path.join(StartPos, 'video')
Archives = os.path.join(StartPos, 'archives')
Other = os.path.join(StartPos, 'other')

Path(Images).mkdir(exist_ok=True)
Path(Documents).mkdir(exist_ok=True)
Path(Musics).mkdir(exist_ok=True)
Path(Videos).mkdir(exist_ok=True)
Path(Archives).mkdir(exist_ok=True)
Path(Other).mkdir(exist_ok=True)

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

Transl = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    Transl[ord(c)] = l
    Transl[ord(c.upper())] = l.upper()

ImList = []
DcList = []
AuList = []
VdList = []
ArchList = []
OthList = []
SuffList = set()
OthSuffList = set()

def normalize_name(name):
    new_name = ''
    for char in name:
        if re.search(r'[0-9A-z]', char):
            char = char
        elif re.search(r'[А-Яа-яёєіїґ]', char):
            char = Transl[ord(char)]
        else:
            char = '_'
        new_name += char
    return new_name

def sort(Current_folder):
    for CurrentItem in Path(Current_folder).iterdir():
        Threads = []
        if CurrentItem.is_dir():
            if CurrentItem.name not in ('images', 'documents', 'audio', 'video', 'archives', 'other'):
                th = Thread(target=sort, args=(CurrentItem,))
                th.start()
                Threads.append(th)

        if CurrentItem.is_file():
            normalized_file_name = normalize_name(CurrentItem.stem) + CurrentItem.suffix
            if CurrentItem.suffix.lower() in ('.jpeg', '.png', '.jpg', '.svg'):
                ImList.append(normalized_file_name)
                SuffList.add(CurrentItem.suffix)
                move(CurrentItem, os.path.join(Images, normalized_file_name))

            elif CurrentItem.suffix.lower() in ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx', '.ppt'):
                DcList.append(normalized_file_name)
                SuffList.add(CurrentItem.suffix)
                move(CurrentItem, os.path.join(Documents, normalized_file_name))

            elif CurrentItem.suffix.lower() in ('.mp3', '.ogg', '.wav', '.amr'):
                AuList.append(normalized_file_name)
                SuffList.add(CurrentItem.suffix)
                move(CurrentItem, os.path.join(Musics, normalized_file_name))

            elif CurrentItem.suffix.lower() in ('.avi', '.mp4', '.mov', '.mkv'):
                VdList.append(normalized_file_name)
                SuffList.add(CurrentItem.suffix)
                move(CurrentItem, os.path.join(Videos, normalized_file_name))

            elif CurrentItem.suffix.lower() in ('.zip', '.gz', '.tar'):
                ArchList.append(normalized_file_name)
                SuffList.add(CurrentItem.suffix)
                unpack_archive(CurrentItem, os.path.join(Archives, normalize_name(CurrentItem.stem)))
                os.remove(CurrentItem)

            else:
                OthList.append(CurrentItem.name)
                OthSuffList.add(CurrentItem.suffix)
                move(CurrentItem, os.path.join(Other, CurrentItem.name))

        [th.join() for th in Threads]
        if CurrentItem.is_dir():
            if CurrentItem.name not in ('images', 'documents', 'audio', 'video', 'archives', 'other'):
                Path(CurrentItem).rmdir()

if __name__ == "__main__":
    sort(StartPos)

    print(f'''\n
            ImList={ImList}\n
            DcList={DcList}\n
            AuList={AuList}\n
            VdList={VdList}\n
            ArchList={ArchList}\n
            OthList={OthList}\n
            SuffList={SuffList}\n
            OthSuffList={OthSuffList}\n''')