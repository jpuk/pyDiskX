from PyQt5 import QtCore, QtGui, QtWidgets
import pyDiskX
import os

class Ui_MainWindow(object):
    selected_folder_name = ""
    folder_object = None
    previous_folder_object_list = []
    folder_list_being_cleared = False
    currently_folders_deep = 0


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 703)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.rootDirectoyPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.rootDirectoyPushButton.setGeometry(QtCore.QRect(20, 10, 141, 32))
        self.rootDirectoyPushButton.setObjectName("rootDirectoyPushButton")
        self.folderListView = QtWidgets.QListWidget(self.centralwidget)
        self.folderListView.setGeometry(QtCore.QRect(20, 60, 591, 241))
        self.folderListView.setObjectName("folderListView")
        self.fileListView = QtWidgets.QListWidget(self.centralwidget)
        self.fileListView.setGeometry(QtCore.QRect(20, 330, 591, 311))
        self.fileListView.setObjectName("fileListView")
        self.getTreeSizePushButton = QtWidgets.QPushButton(self.centralwidget)
        self.getTreeSizePushButton.setGeometry(QtCore.QRect(220, 10, 113, 32))
        self.getTreeSizePushButton.setObjectName("getTreeSizePushButton")
        self.foldersLabel = QtWidgets.QLabel(self.centralwidget)
        self.foldersLabel.setGeometry(QtCore.QRect(20, 40, 591, 16))
        self.foldersLabel.setObjectName("foldersLabel")
        self.filesLabel = QtWidgets.QLabel(self.centralwidget)
        self.filesLabel.setGeometry(QtCore.QRect(20, 310, 60, 16))
        self.filesLabel.setObjectName("filesLabel")
        self.backPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.backPushButton.setGeometry(QtCore.QRect(160, 10, 61, 32))
        self.backPushButton.setObjectName("backPushButton")
        self.treeSizeLabel = QtWidgets.QLabel(self.centralwidget)
        self.treeSizeLabel.setGeometry(QtCore.QRect(330, 20, 281, 16))
        self.treeSizeLabel.setText("")
        self.treeSizeLabel.setObjectName("treeSizeLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # my message handler connectors
        self.rootDirectoyPushButton.clicked.connect(self.select_folder_push_button_clicked)
        self.folderListView.itemSelectionChanged.connect(self.folder_list_view_selection_changed)
        self.getTreeSizePushButton.clicked.connect(self.get_tree_size_push_button_clicked)
        self.backPushButton.clicked.connect(self.back_push_button_clicked)

        # set ui defaults
        self.backPushButton.setDisabled(True)
        self.getTreeSizePushButton.setDisabled(True)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.rootDirectoyPushButton.setText(_translate("MainWindow", "Select Directory"))
        self.getTreeSizePushButton.setText(_translate("MainWindow", "Get Tree Size"))
        self.foldersLabel.setText(_translate("MainWindow", "Folders:"))
        self.filesLabel.setText(_translate("MainWindow", "Files:"))
        self.backPushButton.setText(_translate("MainWindow", "Back"))

    ## my handler functions
    def get_tree_size_push_button_clicked(self):
        self.folder_object = pyDiskX.Folder(full_path_name=self.folder_object.full_path_name)
        size = self.folder_object.tree_size.tree_size
        self.treeSizeLabel.setText(str(round(size, 4)) + "MB")

    def back_push_button_clicked(self):
        print("Back push button clicked")
        self.clear_folder_list_view()
        self.folder_object = self.previous_folder_object_list[self.currently_folders_deep-1]
        self.currently_folders_deep -= 1
        print("Decreased folders deep to {}".format(self.currently_folders_deep))
        if self.currently_folders_deep == 0:
            self.previous_folder_object_list = []
            self.backPushButton.setDisabled(True)
        self.foldersLabel.setText(str("Folders: {}".format(self.folder_object.full_path_name)))
        self.folder_list_view_selection_changed(sel=0, first=True)

    def update_folder_and_files_list_boxes(self, folder_object):
        # print("Folders")
        if folder_object.contained_folders:
            for folder in folder_object.contained_folders:
                self.folderListView.addItem(folder.folder_name + " - {}MB of files at this level".format(round(folder.size, 4)))
                # print("  " + str(folder.folder_name))
        # print("Files")
        if folder_object.contained_files:
            for file in folder_object.contained_files:
                self.fileListView.addItem(file.file_name + " - {}MB".format(round(file.size, 4)))
                # print("  " + str(file.file_name))

    def folder_list_view_selection_changed(self, sel=None, first=False):
        if self.folder_list_being_cleared is not True:
            if sel is None:
                sel = int(self.folderListView.currentIndex().row())
            print("Folder list box selection changed {}".format(sel))

            if first is not True:
                self.clear_folder_list_view()
                self.previous_folder_object_list.append(self.folder_object)
                self.currently_folders_deep += 1
                self.backPushButton.setEnabled(True)
                print("Increased folders deep to {}".format(self.currently_folders_deep))
                print("previous folders object list contains: {}".format(len(self.previous_folder_object_list)))
                self.update_folders_label()
                if self.folder_object.contained_folders:
                    self.folder_object = self.folder_object.contained_folders[sel]
                    self.update_folders_label()

            self.update_folder_and_files_list_boxes(self.folder_object)

    def clear_folder_list_view(self):
        self.folder_list_being_cleared = True
        self.folderListView.clear()
        self.fileListView.clear()
        self.folder_list_being_cleared = False

    def select_folder_push_button_clicked(self):
        self.folder_object = None
        self.previous_folder_object = None
        self.folderListView.clear()
        self.fileListView.clear()
        self.getTreeSizePushButton.setEnabled(True)

        self.selected_folder_name = os.path.abspath(QtWidgets.QFileDialog.getExistingDirectory())
        print("Select folder push button clicked - {}".format(self.selected_folder_name))
        self.update_folders_label()
        self.folder_object = pyDiskX.Folder(full_path_name=self.selected_folder_name)
        self.update_folders_label()
        self.folder_list_view_selection_changed(sel=0, first=True)

    def update_folders_label(self):
        print("Updating folders label")
        if self.folder_object:
            self.foldersLabel.setText(str("Folders: {}".format(self.folder_object.full_path_name)))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
