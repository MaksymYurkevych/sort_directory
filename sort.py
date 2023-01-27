from os import rename, path, mkdir, rmdir, walk, listdir, chdir, curdir
from glob import glob
from shutil import move, Error
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
    for root, dirs, files in walk(my_path):

        for file in files:
            rename(path.join(root, file),
                   path.join(root, normalize(path.splitext(file)[0]) + path.splitext(file)[1]))

    filename = glob(fr"{my_path}\**\*", recursive=True)
    used_names = []
    known_extensions = []
    unknown_extensions = []

    '''Sorting files by folders'''
    for file in filename:

        if path.isdir(file):
            continue

        if not path.splitext(path.basename(file))[1]:
            name = path.splitext(path.basename(file))[0]
            name += ".gfdsgfds"

        cr_path = ""

        for key, value in extensions.items():
            if path.splitext(file)[1] in value:
                cr_path = fr"{my_path}\{key}"
                if not path.splitext(file)[1] in known_extensions:
                    known_extensions.append(path.splitext(file)[1])

        if cr_path == "":
            cr_path = fr"{my_path}\unknown"
            if not path.splitext(file)[1] in unknown_extensions:
                unknown_extensions.append(path.splitext(file)[1])

        if not path.exists(cr_path):
            mkdir(cr_path)
        try:
            move(file, cr_path)
        except Error:
            if path.basename(file) in used_names:
                new_name = path.splitext(file)[0] + "1" + path.splitext(file)[1]
                rename(file, new_name)
                move(new_name, cr_path)

        used_names.append(path.basename(file))

    print(f"Known extensions: {known_extensions}")
    print(f"Unknown extensions: {unknown_extensions}")

    '''Deleting empty folders'''
    list_of_folders = list(walk(my_path))
    for pathing, _, _ in list_of_folders[::-1]:
        if len(listdir(pathing)) == 0:
            rmdir(pathing)

    '''Unpacking archives'''
    for archive in listdir(fr"{my_path}\archives"):
        mkdir(fr"{my_path}\archives\{path.splitext(archive)[0]}")
        extract_dir = fr"{my_path}\archives\{path.splitext(archive)[0]}"
        with ZipFile(fr"{my_path}\archives\{archive}") as arch:
            arch.extractall(extract_dir)

        def renamed(dirpath, names, encoding):
            new_names = [old.encode('cp437').decode(encoding) for old in names]
            for old, new in zip(names, new_names):
                rename(path.join(dirpath, old),
                       path.join(dirpath, normalize(path.splitext(new)[0]) + path.splitext(new)[1]))
            return new_names

        encoding = 'cp866'
        chdir(extract_dir)
        for dirpath, dirs, files in walk(curdir, topdown=True):
            renamed(dirpath, files, encoding)
            dirs[:] = renamed(dirpath, dirs, encoding)

    '''Counting files by extensions'''
    all_extensions = known_extensions + unknown_extensions
    all_extensions_dict = {}


    for extension in all_extensions:
        counter = 0
        for file in filename:
            if file.endswith(extension):
                counter += 1
        all_extensions_dict[extension] = counter

    print("The number of extensions sorted")
    for k, v in all_extensions_dict.items():
        print(f"{k} : {v} item(s)")


def main():
    try:
        sort_files(argv[1])
    except IndexError:
        print("Please provide a path to a folder to be sorted")


if __name__ == '__main__':
    main()
