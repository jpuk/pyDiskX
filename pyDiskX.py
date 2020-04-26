import os
import pathlib


class TreeSize():
    tree_size = 0.0

    #def __init__(self):

    def add_folder_size(self, size):
        self.tree_size += size
        return self.tree_size


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

    def __init__(self, full_path_name=None):
        #print("File object created for {}".format(full_path_name))
        if full_path_name != None:
            self.set_full_path_name(full_path_name)
            if os.path.isfile(full_path_name):
                self.is_file = True
                self.file_name = self.full_path_name.name
                self.get_size()
            else:
                print("Error - {} is not a valid file".format(full_path_name))

    def get_size(self):
        self.size = (os.path.getsize(self.full_path_name) / 1024) / 1024
        #print("Got size of file {} - {}MB".format(self.full_path_name, self.size))



class Folder(FilesFolders):
    folder_name = str()
    folder_contents_list = []
    contained_folders = []
    contained_files = []
    is_folder = bool()
    contained_files_size = 0.0
    tree_size = None
    parent_folder_object = None

    def __init__(self, parent=None, full_path_name=None):
        #print("Folder object created for {}".format(full_path_name))
        if full_path_name != None:
            folder_name = ""
            self.folder_contents_list = []
            self.contained_folders = []
            self.contained_files = []
            self.id = 0
            self.size = 0
            self.is_folder = False
            self.contained_files_size = 0
            self.tree_size = TreeSize()
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

        for item in os.listdir(self.full_path_name):
            self.folder_contents_list.append(item)
            full_path = os.path.join(self.full_path_name, item)
            #print("Full path is {}".format(full_path))

            if os.path.isdir(os.path.abspath(full_path)):
                folder = Folder(parent=self.parent_folder_object, full_path_name=full_path)
                folder.set_id(folder_count)
                folder_count = folder_count + 1
                self.contained_folders.append(folder)

            if os.path.isfile(os.path.abspath(full_path)):
                file = File(full_path)
                file.set_id(file_count)
                self.contained_files_size += (file.size / 1024) / 1024
                file_count = file_count + 1
                self.contained_files.append(file)

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

    '''def get_folder_tree_size(self, folder=None, first=True):
        #global main_folder_tree_size
        if folder is None:
            folder = self
        if first is True:
            print("first run, setting var to starting folder size {}".format(self.size))
            self.main_folder_tree_size = self.size
        print(id(folder))
        if folder.contained_folders:
            for inner_folder in folder.contained_folders:
                print("inner folder size {} for {}".format(inner_folder.size, inner_folder.full_path_name))
                self.main_folder_tree_size += inner_folder.size
                print("Running total = {}".format(self.main_folder_tree_size))
                if inner_folder.contained_folders:
                    for inner_inner_folder in inner_folder.contained_folders:
                        inner_inner_folder.get_folder_tree_size(inner_inner_folder, first=False)

        return self.main_folder_tree_size'''
