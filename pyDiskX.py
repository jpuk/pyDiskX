import os
import pathlib

_OS = int()

def __init__():
    get_os()

def get_os():
    global _OS
    os_choice = {"nt": 0, "posix": 1}
    for o in os_choice:
        print(o)
        if o == os.name:
            _OS = os_choice[o]
            print("OS is {} setting _OS to {}".format(str(os.name), _OS))
            return _OS

    print("Unknown OS, assuming unix-like. OS = {}".format(os.name))
    _OS = 1
    return -1

class TreeSize():
    size = 0.0
    root_path = ""

    def __init__(self, root_path=None):
        if root_path:
            self.root_path = root_path

    def add_folder_size(self, size):
        self.size += size
        return self.size


class FilesFolders:
    id = 0
    full_path_name = pathlib.Path()
    size = 0

    def set_full_path_name(self, full_path_name):
        self.full_path_name = pathlib.Path(full_path_name)

    def set_id(self, id):
        self.id = id


class File(FilesFolders):
    file_name = ""
    is_file = False
    extension = ""

    def __init__(self, full_path_name=None):
        #print("File object created for {}".format(full_path_name))
        if full_path_name != None:
            self.set_full_path_name(full_path_name)
            if os.path.isfile(full_path_name):
                self.is_file = True
                self.extract_filename_from_path()
                self.get_size()
                self.get_extension()
            else:
                print("Error - {} is not a valid file".format(full_path_name))

    def get_size(self):
        self.size = (os.path.getsize(self.full_path_name) / 1024) / 1024
        return self.size
        #print("Got size of file {} - {}MB".format(self.full_path_name, self.size))

    def get_extension(self):
        if _OS == 0:
            self.file_name = str(self.file_name).upper()
        else:
            self.file_name = str(self.file_name)

        #print("Determining file type by extension for {}".format(self.file_name))
        if self.file_name.rfind(".") == -1:
            #print("Unknown extension")
            self.extension = "UNKNOWN_EXT"
        else:
            self.extension = self.file_name[self.file_name.rfind(".") + 1:]
            #print("Extension is type {}".format(self.extension))
        return self.extension

    def extract_filename_from_path(self):
        sep_pos = str(self.full_path_name).rfind(os.sep)
        self.file_name = str(self.full_path_name)[sep_pos+1:]
        #print("Filename {} extracted from path {}".format(self.file_name, self.full_path_name))


class Folder(FilesFolders):
    folder_name = str()
    folder_contents_list = []
    contained_folders = []
    contained_files = []
    is_folder = bool()
    contained_files_size = 0.0
    contained_file_extensions_tree = {}
    contained_file_extensions = {}
    tree_size = None
    parent_folder_object = None
    max_depth = None
    depth = 0

    def __init__(self, parent=None, full_path_name=None, max_depth=None, depth=None):
        #print("Folder object created for {}".format(full_path_name))
        if full_path_name != None:
            folder_name = ""
            self.folder_contents_list = []
            self.contained_folders = []
            self.contained_files = []
            self.contained_file_extensions = {}
            self.id = 0
            self.size = 0
            self.is_folder = False
            self.contained_files_size = 0
            self.contained_file_extensions = {}
            self.tree_size = TreeSize(root_path=full_path_name)
            self.max_depth = max_depth
            if depth:
                self.depth = depth
            else:
                self.depth = 0
            if parent:
                self.parent_folder_object=parent
            else:
                self.parent_folder_object = self

            self.set_full_path_name(full_path_name)
            if os.path.isdir(full_path_name):
                self.is_folder = True
                self.folder_name = self.full_path_name.name
                self.enumerate_content()
                self.get_size()
            else:
                print("Error - {} is not a directory".format(full_path_name))

    def enumerate_content(self):
        file_count = 0
        folder_count = 0
        #print("max depth is {}".format(self.max_depth))
        if self.max_depth:
            if self.depth >= self.max_depth:
                print("Maximum folder depth reached! {}".format(self.max_depth))
                return -1


        for item in os.listdir(self.full_path_name):
            self.folder_contents_list.append(item)
            full_path = os.path.join(self.full_path_name, item)
            #print("Full path is {}".format(full_path))

            try:
                if os.path.isdir(os.path.abspath(full_path)):
                    #print("depth is {}".format(self.depth))
                    folder = Folder(parent=self.parent_folder_object, full_path_name=full_path, depth=self.depth+1,
                                    max_depth=self.parent_folder_object.max_depth)
                    folder.set_id(folder_count)
                    folder_count = folder_count + 1
                    self.contained_folders.append(folder)
            except:
                print("Error listing folder!")

            if os.path.isfile(os.path.abspath(full_path)):
                file = File(full_path)
                file.set_id(file_count)
                self.contained_files_size += (file.size / 1024) / 1024
                file_count = file_count + 1
                self.contained_files.append(file)
                if file.extension not in self.contained_file_extensions:
                    self.contained_file_extensions[file.extension] = 1
                    self.contained_file_extensions_tree[file.extension] = 1
                    #print("added new extension to dict {}".format(file.extension))
                else:
                    self.contained_file_extensions[file.extension] += 1
                    self.contained_file_extensions_tree[file.extension] += 1
                    #print("found another file with an extension we've already recorded. {} now {}".format(
                    #    file.extension, self.contained_file_extensions[file.extension]))
        #print("Contents enumerated for {} - {} Files - {} Folders".format(self.full_path_name, file_count, folder_count))

    def get_size(self):
        size = 0
        if self.contained_files:
            for f in self.contained_files:
                size += f.size
        self.size = size
        self.parent_folder_object.tree_size.add_folder_size(size)
        print("Folder {} is {}MB".format(self.full_path_name, size))
        return size


# run init function when run as module
__init__()