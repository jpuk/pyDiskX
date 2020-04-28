from os import walk
from os import path
from os import sep

class QuickTreeSize():
    def __init__(self, folder_name):
        self._folder_list = []
        self._file_list = []
        self._tree_size = 0.0
        if path.isdir(folder_name):
            self.enumerate_all_folders(folder_name)
        else:
            print("{} isn't a valid folder".format(folder_name))

    def enumerate_all_folders(self, dirname_f):
        for (dirpath_o, dirnames_o, filenames_o) in walk(dirname_f):
            self._folder_list.append(dirpath_o)
            for filename in filenames_o:
                full_path = "{}{}{}".format(dirpath_o, sep, filename)
                #print(full_path)
                self._file_list.append(full_path)
                try:
                    self._tree_size += path.getsize(full_path)
                except:
                    print("Error getting size of {}".format(full_path))
            for dir_i in dirnames_o:
                self._folder_list.append(dir_i)
                self.enumerate_all_folders(dirpath_o + sep + dir_i)
            break

    def size_in_MB(self):
        return round((self._tree_size / 1024) / 1024, 4)

    def size_in_KB(self):
        return self._tree_size

    def list_folders(self):
        return self._folder_list

    def list_files(self):
        return self._file_list

    def __add__(self, value):
        if isinstance(value, tuple):
            print("value {} {}".format(value[0], value[1]))
        if isinstance(value, float):
            ret = self._tree_size = self._tree_size + float(value)
        if isinstance(value, int):
            ret = self._tree_size = self._tree_size + float(value)
        if isinstance(value, str):
            ret = str(self._folder_list) + value
        if isinstance(value, QuickTreeSize):
            ret = str(self._folder_list) + str(value._folder_list)

        return ret

    def __radd__(self, value):
        if isinstance(value, tuple):
            print("value {} {}".format(value[0], value[1]))
        if isinstance(value, float):
            ret = self._tree_size = self._tree_size + float(value)
        if isinstance(value, int):
            ret = self._tree_size = self._tree_size + float(value)
        if isinstance(value, str):
            ret = str(self._folder_list) + value
        if isinstance(value, QuickTreeSize):
            ret = str(self._folder_list) + str(value._folder_list)

        return ret

    def __sub__(self, value):
        ret = self._tree_size = self._tree_size - float(value)
        return ret

    def __rsub__(self, value):
        ret = self._tree_size = self._tree_size - float(value)
        return ret

    def __float__(self):
        return self._tree_size

    def __int__(self):
        print("Precision lost casting to int")
        return int(self._tree_size)

    def __str__(self):
        return str(self._folder_list)

    def __len__(self):
        return len(self._folder_list)