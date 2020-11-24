import maya.cmds as cmds
import logging
import random
import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import math


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
        self.setMaximumHeight(400)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        """Creates the Scatter UI"""
        self.main_lay = QtWidgets.QVBoxLayout()
        title_lbls = self._create_title_labels()
        self.main_lay.addLayout(title_lbls)
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addWidget(self.instr_label)
        scale_ui = self._create_scale_ui()
        self.main_lay.addLayout(scale_ui)
        rotate_ui = self._create_rotation_ui()
        self.main_lay.addLayout(rotate_ui)
        density_ui = self._create_density_ui()
        button_ui = self._create_button_ui()
        self.main_lay.addLayout(density_ui)
        self.main_lay.addLayout(button_ui)
        self.setLayout(self.main_lay)

    def _create_button_ui(self):
        """creates button ui"""
        self.vertex_button = QtWidgets.QPushButton("Scatter to vertices!")
        self.faces_button = QtWidgets.QPushButton("Hellify! (broken scatter to faces)")
        self.buttons_lay = QtWidgets.QHBoxLayout()
        self.buttons_lay.addWidget(self.vertex_button)
        self.buttons_lay.addWidget(self.faces_button)
        return self.buttons_lay

    def _create_title_labels(self):
        """Creates title and instruction labels for the main UI window"""
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 30px")
        self.instr_label = QtWidgets.QLabel("1. Select the object you want to make copies of. Then, shift click "
                                            "the object you want to map the copies onto.")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.title_lbl)
        layout.addWidget(self.instr_label)
        return layout

    def _create_scale_ui(self):
        """Creates Scale Min and Max Line Spin boxes and labels"""
        self.scale_lbl = QtWidgets.QLabel("2. Select minimum and maximum scale factors for "
                                          "each copy to randomly scale to")
        self.min_scale_sbx = QtWidgets.QDoubleSpinBox()
        self.min_scale_sbx.setValue(1)
        self.min_scale_sbx.setSingleStep(.1)
        self.max_scale_sbx = QtWidgets.QDoubleSpinBox()
        self.max_scale_sbx.setValue(1)
        self.max_scale_sbx.setSingleStep(.1)
        layout = QtWidgets.QVBoxLayout()
        h_layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scale_lbl)
        h_layout.addWidget(self.min_scale_sbx)
        h_layout.addWidget(self.max_scale_sbx)
        layout.addLayout(h_layout)
        return layout

    def _create_density_ui(self):
        """creates density UI including label and sbx"""
        density_lbl = QtWidgets.QLabel("4. Select the amount (0-100%) of vertices/faces to scatter to")
        self.density_sbx = QtWidgets.QSpinBox()
        self.density_sbx.setRange(0, 101)
        self.density_sbx.setValue(100)
        self.density_sbx.setSingleStep(1)
        density_lay = QtWidgets.QVBoxLayout()
        density_lay.addWidget(density_lbl)
        density_lay.addWidget(self.density_sbx)
        return density_lay

    def _create_rotation_ui(self):
        """creates rotation UI including X, Y, and Z min/max spinboxes and labels"""
        layout = QtWidgets.QVBoxLayout()
        rotation_lbl = QtWidgets.QLabel("3. Select the minimum and maximum degrees for the copies to randomly rotate.")
        layout.addWidget(rotation_lbl)
        grid_layout = QtWidgets.QGridLayout()
        self._create_x_rotation_ui(grid_layout)
        self._create_y_rotation_ui(grid_layout)
        self._create_z_rotation_ui(grid_layout)
        self._create_xyz_labels(grid_layout)
        layout.addLayout(grid_layout)
        return layout

    def _create_z_rotation_ui(self, grid_lay):
        """creates Z axis rotation spinboxes"""
        self.min_z_sbx = QtWidgets.QSpinBox()
        self.min_z_sbx.setSingleStep(5)
        self.min_z_sbx.setValue(0)
        self.max_z_sbx = QtWidgets.QSpinBox()
        self.max_z_sbx.setSingleStep(5)
        self.max_z_sbx.setValue(0)
        self.min_z_sbx.setRange(0, 359)
        self.max_z_sbx.setRange(0, 359)
        grid_lay.addWidget(self.min_z_sbx, 2, 4)
        grid_lay.addWidget(self.max_z_sbx, 3, 4)
        return grid_lay

    def _create_y_rotation_ui(self, grid_lay):
        """creates Y axis rotation spinboxes"""
        self.min_y_sbx = QtWidgets.QSpinBox()
        self.min_y_sbx.setValue(0)
        self.min_y_sbx.setSingleStep(5)
        self.max_y_sbx = QtWidgets.QSpinBox()
        self.max_y_sbx.setValue(0)
        self.max_y_sbx.setSingleStep(5)
        self.min_y_sbx.setRange(0, 359)
        self.max_y_sbx.setRange(0, 359)
        grid_lay.addWidget(self.min_y_sbx, 2, 2)
        grid_lay.addWidget(self.max_y_sbx, 3, 2)
        return grid_lay

    def _create_x_rotation_ui(self, grid_lay):
        """creates X axis rotation spinboxes"""
        self.min_x_sbx = QtWidgets.QSpinBox()
        self.min_x_sbx.setValue(0)
        self.min_x_sbx.setSingleStep(5)
        self.max_x_sbx = QtWidgets.QSpinBox()
        self.max_x_sbx.setValue(0)
        self.max_x_sbx.setSingleStep(5)
        self.min_x_sbx.setRange(0, 359)
        self.max_x_sbx.setRange(0, 359)
        grid_lay.addWidget(self.min_x_sbx, 2, 0)
        grid_lay.addWidget(self.max_x_sbx, 3, 0)
        return grid_lay

    def _create_xyz_labels(self, grid_lay):
        """Creates labels for xyz spinboxes"""
        x_lbl = QtWidgets.QLabel("x-axis")
        y_lbl = QtWidgets.QLabel("y-axis")
        z_lbl = QtWidgets.QLabel("z-axis")
        x_min_lbl = QtWidgets.QLabel("min")
        x_max_lbl = QtWidgets.QLabel("max")
        y_min_lbl = QtWidgets.QLabel("min")
        y_max_lbl = QtWidgets.QLabel("max")
        z_min_lbl = QtWidgets.QLabel("min")
        z_max_lbl = QtWidgets.QLabel("max")
        grid_lay.addWidget(x_lbl, 1, 0)
        grid_lay.addWidget(y_lbl, 1, 2)
        grid_lay.addWidget(z_lbl, 1, 4)
        grid_lay.addWidget(x_min_lbl, 2, 1)
        grid_lay.addWidget(x_max_lbl, 3, 1)
        grid_lay.addWidget(y_min_lbl, 2, 3)
        grid_lay.addWidget(y_max_lbl, 3, 3)
        grid_lay.addWidget(z_min_lbl, 2, 5)
        grid_lay.addWidget(z_max_lbl, 3, 5)
        return grid_lay

    def create_connections(self):
        """Connect widget signal to slot"""
        self.vertex_button.clicked.connect(self.launch_scatter_ver)
        self.faces_button.clicked.connect(self.launch_scatter_faces)

    @QtCore.Slot()
    def launch_scatter_ver(self):
        """launches scatter to vertices"""
        sc = Scatter(rotate_x_min=self.min_x_sbx.value(), rotate_x_max=self.max_x_sbx.value(),
                     rotate_y_min=self.min_y_sbx.value(), rotate_y_max=self.max_y_sbx.value(),
                     rotate_z_min=self.min_z_sbx.value(), rotate_z_max=self.max_z_sbx.value(),
                     scale_min=self.min_scale_sbx.value(), scale_max=self.max_scale_sbx.value(),
                     density=self.density_sbx.value(), vertex=True, faces=False)
        sc.scatter()

    @QtCore.Slot()
    def launch_scatter_faces(self):
        """launches scatter faces"""
        sc = Scatter(rotate_x_min=self.min_x_sbx.value(), rotate_x_max=self.max_x_sbx.value(),
                     rotate_y_min=self.min_y_sbx.value(), rotate_y_max=self.max_y_sbx.value(),
                     rotate_z_min=self.min_z_sbx.value(), rotate_z_max=self.max_z_sbx.value(),
                     scale_min=self.min_scale_sbx.value(), scale_max=self.max_scale_sbx.value(),
                     vertex=False, faces=True)
        sc.scatter()


def swap(a, b):
    """swaps two items - returns array of them reversed"""
    swap = a
    a = b
    b = swap
    return [a, b]


class Scatter:
    """A class for scattering copies of maya transform objects onto other objects"""

    def __init__(self, density=100, rotate_x_min=0, rotate_x_max=0, rotate_y_min=0, rotate_y_max=0, rotate_z_min=0,
                 rotate_z_max=0, scale_min=1, scale_max=1, vertex=True, faces=False):
        self.density = density
        self.rotate_x_min = rotate_x_min
        self.rotate_x_max = rotate_x_max
        self.rotate_y_min = rotate_y_min
        self.rotate_y_max = rotate_y_max
        self.rotate_z_min = rotate_z_min
        self.rotate_z_max = rotate_z_max
        self.scale_min = scale_min
        self.scale_max = scale_max
        self.faces = faces
        self.vertex = vertex

    def scatter(self):
        """main. Scatters the objects."""
        #get faces or vertices
        selection = cmds.ls(sl=True, fl=True)
        if self.faces:
            pattern = "{obj}.f[*]".format(obj=selection[1])
        if self.vertex:
            pattern = "{obj}.vtx[*]".format(obj=selection[1])
        target_names = cmds.ls(pattern, flatten=True)
        #use density to calculate how many targets to scatter to
        size_targets = len(target_names)
        target_names = random.sample(target_names, int(float(size_targets) / 100 * self.density))
        object_to_instance = selection[0]

        if cmds.objectType(object_to_instance) == "transform":
            self.instance_objects(object_to_instance, target_names)
        else:
            log.error("Please select a transform object for your first object")

    def instance_objects(self, object_to_instance, target_names):
        """instances an object to each target, scaling and rotating it appropriately"""
        for target in target_names:
            new_instance = cmds.instance(object_to_instance)
            new_instance = self.scale_instance(new_instance, self.scale_min, self.scale_max)
            new_instance = self.rotate_instance(new_instance, self.rotate_x_min, self.rotate_x_max,
                                                self.rotate_y_min, self.rotate_y_max, self.rotate_z_min,
                                                self.rotate_z_max)
            if self.faces:
                face_center = self.get_face_center(target)
                face_normal = self.get_face_normal(target)
                self.move_align(target, face_normal, face_center)
            if self.vertex:
                position = cmds.pointPosition(target, w=True)
                cmds.move(position[0], position[1], position[2], new_instance, a=True, ws=True)

    def scale_instance(self, inst, min_scale, max_scale):
        """returns a randomly scaled instance according to user preference"""
        # instead of erroring out, if the user specifies a min > max, just swap them, it should work as expected
        if min_scale > max_scale:
            swap_arr = swap(min_scale, max_scale)
            min_scale = swap_arr[0]
            max_scale = swap_arr[1]
        scale_factor = random.uniform(min_scale, max_scale)
        cmds.scale(scale_factor, scale_factor, scale_factor, inst, relative=True)
        return inst

    def rotate_instance(self, inst, x_min, x_max, y_min, y_max, z_min, z_max):
        """Randomly rotates the instance and returns it"""
        # instead of erroring out, if the user specifies a min > max, just swap them, it should work as expected
        if x_min > x_max:
            swap_arr = swap(x_min, x_max)
            x_min, x_max = [swap_arr[i] for i in swap_arr]
        if y_min > y_max:
            swap_arr = swap(y_min, y_max)
            y_min, y_max = [swap_arr[i] for i in swap_arr]
        if z_min > z_max:
            swap_arr = swap(z_min, z_max)
            z_min, z_max = [swap_arr[i] for i in swap_arr]
        x = random.randint(x_min, x_max)
        y = random.randint(y_min, y_max)
        z = random.randint(z_min, z_max)
        cmds.rotate(x, inst, rotateX=True, relative=True)
        cmds.rotate(y, inst, rotateY=True, relative=True)
        cmds.rotate(z, inst, rotateZ=True, relative=True)
        return inst

    def get_face_center(self, face_name):
        """returns numpy array of face center"""
        cmds.select(face_name)
        #get all vertices in face
        ver_positions = cmds.xform(q=True, ws=True, t=True)
        # all vector-like arrays start with v
        v_sum = [0, 0, 0]
        #total each dimension
        for v in ver_positions:
            for i in range (0, 3):
                v_sum[i] += v
                v += 1
        v_avg = [0, 0, 0]
        #get avg of each dimension
        num_ver = len(ver_positions)
        v_avg[0] = v_sum[0] / num_ver
        v_avg[1] = v_sum[1] / num_ver
        v_avg[2] = v_sum[2] / num_ver
        return v_avg

    def get_face_normal(self, face_name):
        """returns the unit normal vector of the face"""
        #get the face's normal vector in LOCAL coordinates
        cmds.select(face_name)
        poly_info_result = cmds.polyInfo(fn=True)
        # convert results to floats
        items = poly_info_result[0].split()
        x = float(items[2])
        y = float(items[3])
        z = float(items[4])
        v_normal = [x, y, z]
        #rest of function converts the local coordinate to world coordinates
        #get the transform matrix
        parent_shape = cmds.listRelatives(face_name, parent=True)
        parent_trans = cmds.listRelatives(parent_shape[0], parent=True)
        #multiply transform by the local-space vector to get the world space vector
        cmds.select(parent_trans)
        transform_matrix = cmds.xform(q=True, m=True, ws=True)
        v_world_normal = self.point_matrix_mult(v_normal, transform_matrix)
        # make it a unit vector
        v_world_unit = self.unitize_vector(v_world_normal)
        #    return $unitWorldNormal;
        return v_world_unit

    def move_align(self, obj_name, v_normal, position):
        """positions object based on a given normal and position"""
        v_normal = self.unitize_vector(v_normal)
        # compute the first tangent
        v_tangent_1 = self.cross_mult_vector(v_normal, [0, 1, 0])
        # make it into a unit
        v_tangent_1 = self.unitize_vector(v_tangent_1)
        if v_tangent_1 == [0, 0, 0]:
            v_tangent_1 = [1, 0, 0]
        #compute the second tangent
        v_tangent_2 = self.cross_mult_vector(v_normal, v_tangent_1)
        # make it a unit
        v_tangent_2 = self.unitize_vector(v_tangent_2)
        matrix = [
            v_tangent_2[0], v_tangent_2[1], v_tangent_2[2], 0.0,
            v_normal[0], v_normal[1], v_normal[2], 0.0,
            v_tangent_1[0], v_tangent_1[1], v_tangent_1[2], 0.0,
            position[0], position[1], position[2], 1.0
        ]
        cmds.select(obj_name)
        #this is one of two possibilities for the error, i think, but i can't figure it out.
        #this command is poorly documented and i can't figure out what it should be doing
        cmds.xform(ws=True, m=matrix)

    def point_matrix_mult(self, v_point, matrix):
        """multiplies a 1x3 point matrix by a 4x4 transform matrix"""
        # i'm 80% sure this is what mel's pointMatrixMult() is doing
        #this is likely where the error is? But i can't for the life of me figure out what it is
        product = [0, 0, 0]
        product[0] = v_point[0] * matrix[0] + v_point[1] * matrix[4] + v_point[2] * matrix[8]
        product[1] = v_point[0] * matrix[1] + v_point[1] * matrix[5] + v_point[2] * matrix[9]
        product[2] = v_point[0] * matrix[2] + v_point[1] * matrix[6] + v_point[2] * matrix[10]
        return product

    def unitize_vector(self, vector):
        """returns the unit form of a vector"""
        mag = self.mag_vector(vector)
        length = len(vector)
        if mag == 0:
           vector = (1, 0, 0)
           mag = 1
        else:
            for c in range (0, length):
                vector[c] = vector[c] / mag
        return vector

    def cross_mult_vector(self, vector_1, vector_2):
        """cross multiplies two vectors and returns the result"""
        cross = [0, 0, 0]
        cross[0] = vector_1[1] * vector_2[2] - vector_1[2] * vector_2[1]
        cross[1] = vector_1[2] * vector_2[0] - vector_1[0] * vector_2[2]
        cross[2] = vector_1[0] * vector_2[1] - vector_1[1] * vector_2[0]
        return cross

    def mag_vector(self, vector):
        """returns the magnitude of a vector"""
        total = 0
        for c in vector:
            total += c * c
        magnitude = math.sqrt(total)
        return magnitude
