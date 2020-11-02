import maya.cmds as cmds
import logging
import random
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


class ScatterUI(QtWidgets.QDialog):
    """Scatter UI Class"""

    # broadly repurposed from the smartsave project

    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(600)
        self.setMaximumHeight(300)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
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
        layout.addWidget(QtWidgets.QLabel("_"), 1, 1)
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
        # repurpose this
        self.folder_browse_btn.clicked.connect(self.browse_dir)
        self.save_btn.clicked.connect(self.save)
        self.save_increment_btn.clicked.connect(self.increment_save)

    @QtCore.Slot()
    def increment_save(self):
        """Saves the scene file using increment_save"""
        # this is called when the corresponding button is clicked


class Scatter():

    def __init__(self, density=100, rotate_x_min=0, rotate_x_max=0, rotate_y_min=0, rotate_y_max=0, rotate_z_min=0,
                 rotate_z_max=0, scale_min=1, scale_max=1):
        self.density = density
        self.rotate_x_min = rotate_x_min
        self.rotate_x_max = rotate_x_max
        self.rotate_y_min = rotate_y_min
        self.rotate_y_max = rotate_y_max
        self.rotate_z_min = rotate_z_min
        self.rotate_z_max = rotate_z_max
        self.scale_min = scale_min
        self.scale_max = scale_max

    def main(self):
        # string $selection[] = `ls - sl - fl`;
        selection = cmds.ls(sl=True, fl=True)

        # string $vertexNames[] = `filterExpand - selectionMask 31 - expand true $selection`;
        vertex_names = cmds.filterExpand(selection, selectionMask=31, expand=True)
        # string $objectToInstance = $selection[0];
        object_to_instance = selection[0]

        # if (`objectType $objectToInstance` == "transform"){

        if cmds.objectType(object_to_instance) == "transform":
            self.instance_objects(object_to_instance, vertex_names)
        else:
            log.error("Please select a transform object for your first object")

    def instance_objects(self, object_to_instance, vertex_names):
        """instances an object to each vertex, scaling and rotating it appropriately"""
        for vertex in vertex_names:
            new_instances = []
            if random.randint(1, 100) < self.density:
                new_instance = cmds.instance(object_to_instance)
                new_instances.append(new_instance)

            new_instances = self.scale_instances(new_instances, self.scale_min, self.scale_max)
            new_instances = self.rotate_instances(new_instances, self.rotate_x_min, self.rotate_x_max,
                                                self.rotate_y_min, self.rotate_y_max, self.rotate_z_min,
                                                self.rotate_z_max)
            for inst in new_instances:
                position = cmds.pointPosition(vertex, w=True)
                cmds.move(position[0], position[1], position[2], inst, a=True, ws=True)


    def scale_instances(self, instances, min, max):
        """returns a randomly scaled instance according to user preference"""
        for inst in instances:
            scale_factor = random.uniform(min, max)
            cmds.scale(scale_factor, scale_factor, scale_factor, inst, relative=True)
        return instances


    def rotate_instances(self, instances, x_min, x_max, y_min, y_max, z_min, z_max):
        """Randomly rotates the instance and returns it"""
        for inst in instances:
            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)
            z = random.randint(z_min, z_max)
            cmds.rotate(x, inst, rotateX=True, relative=True)
            cmds.rotate(y, inst, rotateY=True, relative=True)
            cmds.rotate(z, inst, rotateZ=True, relative=True)
        return instances
