import os
from glob import glob
from shutil import move
from zipfile import ZipFile
from sys import argv


def normalize(file_name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f",
        "h",
        "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    translated = file_name.translate(TRANS)
    clear_name = ""
    for char in translated:
        if char.isdigit() or char.isalpha():
            clear_name += char
        else:
            clear_name += "_"

    return clear_name


def sort_files(my_path):
    extensions = {
        "images": ['.jpeg', '.png', '.jpg', '.svg'],
        "video": ['.avi', '.mp4', '.nov', '.mkv', '.webm'],
        "documents": ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx', '.html'],
        "music": ['.mp3', '.ogg', '.wav', '.amr'],
        "archives": ['.zip', '.gz', '.tar'],
    }

    '''Renaming files'''
    for root, dirs, files in os.walk(my_path):
        for file in files:
            os.rename(os.path.join(root, file),
                      os.path.join(root, normalize(os.path.splitext(file)[0]) + os.path.splitext(file)[1]))

    filename = glob(fr"{my_path}\**\*.*", recursive=True)

    '''Sorting files by folders'''
    for file in filename:
        cr_path = ""

        for key, value in extensions.items():
            if os.path.splitext(file)[1] in value:
                cr_path = fr"{my_path}\{key}"

        if cr_path == "":
            cr_path = fr"{my_path}\unknown"

        if not os.path.exists(cr_path):
            os.mkdir(cr_path)
        move(file, cr_path)

    '''Deleting empty folders'''
    list_of_folders = list(os.walk(my_path))
    for pathing, _, _ in list_of_folders[::-1]:
        if len(os.listdir(pathing)) == 0:
            os.rmdir(pathing)

    '''Unpacking archives'''
    for archive in os.listdir(fr"{my_path}\archives"):
        os.mkdir(fr"{my_path}\archives\{os.path.splitext(archive)[0]}")
        extract_dir = fr"{my_path}\archives\{os.path.splitext(archive)[0]}"
        with ZipFile(fr"{my_path}\archives\{archive}") as arch:
            arch.extractall(extract_dir)

        def renamed(dirpath, names, encoding):
            new_names = [old.encode('cp437').decode(encoding) for old in names]
            for old, new in zip(names, new_names):
                os.rename(os.path.join(dirpath, old),
                          os.path.join(dirpath, normalize(os.path.splitext(new)[0]) + os.path.splitext(new)[1]))
            return new_names

        encoding = 'cp866'
        os.chdir(extract_dir)
        for dirpath, dirs, files in os.walk(os.curdir, topdown=True):
            renamed(dirpath, files, encoding)
            dirs[:] = renamed(dirpath, dirs, encoding)


if __name__ == '__main__':
    sort_files(argv[1])
