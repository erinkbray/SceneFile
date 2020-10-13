# {folder_path}/{descriptor}_{task}_{v###}.{ext}

import maya.cmds as cmds
import logging
from pymel.core.system import Path
import pymel.core as pmc
import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

log = logging.getLogger(__name__)


def maya_main_window():
    """returns the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class SmartSaveUI(QtWidgets.QDialog):
    """Smart Save UI Class"""

    def __init__(self):
        super(SmartSaveUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Smart Save")
        self.setMinimumWidth(500)
        self.setMaximumHeight(300)
        self.setWindowFlags(self.windowFlags() ^QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()
        self.create_connections()


    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Smart Save")
        self.title_lbl.setStyleSheet("font: bold 30px")
        self.folder_lay = self._create_folder_ui()
        self.filename_lay = self._create_file_name_ui()
        self.button_lay = self._create_save_button_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.folder_lay)
        self.main_lay.addLayout(self.filename_lay)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def _create_save_button_ui(self):
        """Creates Save & Save Increment Buttons"""
        self.save_btn = QtWidgets.QPushButton("Save")
        self.save_increment_btn = QtWidgets.QPushButton("Save Increment")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.save_btn)
        layout.addWidget(self.save_increment_btn)
        return layout

    def _create_file_name_ui(self):
        """Creates UI to select filename"""
        layout = self._create_filename_headers()
        self.descriptor_le = QtWidgets.QLineEdit("main")
        self.descriptor_le.setMinimumWidth(100)
        self.task_le = QtWidgets.QLineEdit("model")
        self.task_le.setFixedWidth(100)
        self.ver_sbx = QtWidgets.QSpinBox()
        self.ver_sbx.setValue(1)
        self.ver_sbx.setFixedWidth(80)
        self.ver_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.ext_lbl = QtWidgets.QLabel(".ma")
        layout.addWidget(self.descriptor_le, 1, 0)
        layout.addWidget(QtWidgets.QLabel("_"), 1, 1 )
        layout.addWidget(self.task_le, 1, 2)
        layout.addWidget(QtWidgets.QLabel("_v"), 1, 3)
        layout.addWidget(self.ver_sbx, 1, 4)
        layout.addWidget(self.ext_lbl, 1, 5)
        return layout

    def _create_filename_headers(self):
        """Creates and adds to layout descriptive headers for filename line entries"""
        self.descriptor_header_lbl = QtWidgets.QLabel("Descriptor")
        self.descriptor_header_lbl.setStyleSheet("font: bold")
        self.task_header_lbl = QtWidgets.QLabel("Task")
        self.task_header_lbl.setStyleSheet("font: bold")
        self.ver_header_lbl = QtWidgets.QLabel("Version")
        self.ver_header_lbl.setStyleSheet("font: bold")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.descriptor_header_lbl, 0, 0)
        layout.addWidget(self.task_header_lbl, 0, 2)
        layout.addWidget(self.ver_header_lbl, 0, 4)
        return layout

    def _create_folder_ui(self):
        """Creates folder selector UI"""
        default_folder = Path(cmds.workspace(rootDirectory=True, query=True))
        self.folder_le = QtWidgets.QLineEdit(default_folder)
        self.folder_browse_btn = QtWidgets.QPushButton("...")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.folder_le)
        layout.addWidget(self.folder_browse_btn)
        return layout

    def create_connections(self):
        """Connect widget signals to slots"""
        self.folder_browse_btn.clicked.connect(self.browse_dir)
        self.save_btn.clicked.connect(self.save)
        self.save_increment_btn.clicked.connect(self.save)

    @QtCore.Slot()
    def browse_dir(self):
        """Browse the directory"""
        print("uwu")
        dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, caption="Select Directory",
            dir=self.folder_le.text(),
            options=QtWidgets.QFileDialog.ShowDirsOnly |
                    QtWidgets.QFileDialog.DontResolveSymlinks)
        self.folder_le.setText(dir)

    @QtCore.Slot()
    def save(self):
        """Saves the scene file"""
        self._populate_scenefile_properties()
        self.scene.save()

    @QtCore.Slot()
    def increment_save(self):
        """Saves the scene file using increment_save"""
        self._populate_scenefile_properties()
        self.scene.increment_save()

    def _populate_scenefile_properties(self):
        self.scene = SceneFile()
        self.scene.folder_path = self.folder_le.text()
        self.scene.folder_path= Path(self.scene.folder_path.encode('ascii', 'ignore'))
        self.scene.descriptor = self.descriptor_le.text()
        self.scene.descriptor = self.scene.descriptor.encode('ascii', 'ignore')
        self.scene.task = self.task_le.text()
        self.scene.task = self.scene.task.encode('ascii', 'ignore')

        self.scene.ver = int(self.ver_sbx.value())


class SceneFile(object):
    """A Representation of a Scene File"""
    def __init__(self, path=None):
        self.folder_path = Path()
        self.descriptor = 'main'
        self.task = None
        self.ver = 1
        self.ext = 'ma'
        scene = pmc.system.sceneName()
        if not path and scene:
            path = scene
        if not path and not scene:
            log.warning("Unable to initialize SceneFile object from a new"
                        "scene. Please specify a path.")
            return
        self._init_from_path(path)

    @property
    def filename(self):
        pattern = "{descriptor}_{task}_v{ver:03d}{ext}"
        return pattern.format(descriptor=self.descriptor,
                              task=self.task,
                              ver=self.ver,
                              ext=self.ext)

    @property
    def path(self):
        return self.folder_path / self.filename

    def _init_from_path(self, path):
        path = Path(path)
        self.folder_path = path.parent
        self.ext = path.ext
        self.descriptor, self.task, ver = path.name.stripext().split("_")
        self.ver = int(ver.split("v")[-1])

    def save(self):
        """Saves the scene file.

        Returns:
            Path: The path to the scene file if successful
        """
        try:
            return pmc.system.saveAs(self.path)
        except RuntimeError as err:
            log.warning("Missing directories in path. Creating folders...")
            self.folder_path.makedirs_p()
            return pmc.system.saveAs(self.path)

    def next_avail_ver(self):
        """Return the next available version number in the folder."""
        pattern = "{descriptor}_{task}_v*{ext}".format(
            descriptor=self.descriptor, task=self.task, ext=self.ext)
        matching_scenefiles = []
        for file_ in self.folder_path.files():
            if file_.name.fnmatch(pattern):
                matching_scenefiles.append(file_)
        if not matching_scenefiles:
            return 1
        matching_scenefiles.sort(reverse=True)
        latest_scenefile = matching_scenefiles[0]
        latest_scenefile = latest_scenefile.name.stripext()
        latest_ver_num = int(latest_scenefile.split("_v")[-1])
        return latest_ver_num + 1

    def increment_save(self):
        """Increments the version and saves the scene file.

        If the existing version of a file already exists, it should increment
        from the largest version number available in the folder.

        Returns:
            Path: The path to the scene if successful.
        """
        self.ver = self.next_avail_ver()
        print(self.ver)
        self.save()
