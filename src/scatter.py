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
        self.button = QtWidgets.QPushButton("Scatter!")
        self.main_lay.addWidget(self.button)
        self.setLayout(self.main_lay)

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
        self.button.clicked.connect(self.launch_scatter)

    @QtCore.Slot()
    def launch_scatter(self):
        """launches scatter"""
        sc = Scatter(rotate_x_min=self.min_x_sbx.value(), rotate_x_max=self.max_x_sbx.value(),
                     rotate_y_min=self.min_y_sbx.value(), rotate_y_max=self.max_y_sbx.value(),
                     rotate_z_min=self.min_z_sbx.value(), rotate_z_max=self.max_z_sbx.value(),
                     scale_min=self.min_scale_sbx.value(), scale_max=self.max_scale_sbx.value())
        sc.scatter()


def swap(a, b):
    """swaps two items - returns array of them reversed"""
    swap = a
    a = b
    b = swap
    return [a, b]


class Scatter:

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

    def scatter(self):
        selection = cmds.ls(sl=True, fl=True)
        pattern = "{obj}.f[*]".format(obj=selection[1])
        face_names = cmds.ls(pattern, flatten=True)
        object_to_instance = selection[0]

        if cmds.objectType(object_to_instance) == "transform":
            self.instance_objects(object_to_instance, face_names)
        else:
            log.error("Please select a transform object for your first object")

    def instance_objects(self, object_to_instance, target_names, vertex=False, face=False):
        """instances an object to each target, scaling and rotating it appropriately"""
        for target in target_names:
            print("uwu")
            new_instance = cmds.instance(object_to_instance)
            new_instance = self.scale_instance(new_instance, self.scale_min, self.scale_max)
            new_instance = self.rotate_instance(new_instance, self.rotate_x_min, self.rotate_x_max,
                                                self.rotate_y_min, self.rotate_y_max, self.rotate_z_min,
                                                self.rotate_z_max)
            # position = cmds.pointPosition(vertex, w=True)
            # cmds.move(position[0], position[1], position[2], new_instance, a=True, ws=True)
            face_center = self.get_face_center(target)
            face_normal = self.get_face_normal(target)
            self.move_align(target, face_normal, face_center)

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

    # proc vector getFaceCenter(string $pFaceName){
    def get_face_center(self, face_name):
        """returns numpy array of face center"""
        # vector $vertexPositions[] = `xform - q - ws - t $pFaceName`;
        cmds.select(face_name)
        ver_positions = cmds.xform(q=True, ws=True, t=True)  # vector $sum = << 0, 0, 0 >>;
        # all vector-like arrays start with v
        v_sum = [0, 0, 0]
        #  vector $v;
        #   for ($v in $vertexPositions){
        for v in ver_positions:
            #       $sum = $sum + $v;
            for i in range (0, 3):
                v_sum[i] += v
                v += 1
        # }
        # vector $average;
        v_avg = [0, 0, 0]
        #  int $numVertices = size($vertexPositions);
        num_ver = len(ver_positions)
        #  $average = $sum / $numVertices;
        v_avg[0] = v_sum[0] / num_ver
        v_avg[1] = v_sum[1] / num_ver
        v_avg[2] = v_sum[2] / num_ver
        #   return $average;
        return v_avg

    #    proc vector getFaceNormal(string $pFaceName) {
    def get_face_normal(self, face_name):
        """returns the unit normal vector of the face"""
        #get the face's normal vector in LOCAL coordinates
        cmds.select(face_name)
        poly_info_result = cmds.polyInfo(fn=True)
        # convert results to floats
        items = poly_info_result[0].split(" ")
        x = float(items[7])
        y = float(items[8])
        z = float(items[9])
        v_normal = [x, y, z]
        #rest of function converts the local coordinate to world coordinates
        #get the transform matrix
        parent_shape = cmds.listRelatives(face_name, parent=True)
        parent_trans = cmds.listRelatives(parent_shape[0], parent=True)
        #multiply transform by the local-space vector to get the world space vector
        cmds.select(parent_trans)
        transform_matrix = cmds.xform(q=True, m=True, ws=True)
        #    vector $worldNormal = `pointMatrixMult $normal $transformMatrix`;
        v_world_normal = self.point_matrix_mult(v_normal, transform_matrix)
        # make it a unit vector
        v_world_unit = self.unitize_vector(v_world_normal)
        #    return $unitWorldNormal;
        return v_world_unit

    # proc moveAlign(string $pObjectName, vector $pNormal, vector $pPosition){
    def move_align(self, obj_name, v_normal, position):
        """positions object based on a given normal and position"""
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
        # matrix $m[4][4] = <<
        # ($tangent2.x), ($tangent2.y), ($tangent2.z), 0.0;
        # ($pNormal.x), ($pNormal.y), ($pNormal.z), 0.0;
        # ($tangent1.x), ($tangent1.y), ($tangent1.z), 0.0;
        # ($pPosition.x), ($pPosition.y), ($pPosition.z), 1.0 >>;
        matrix = [
            v_tangent_2[0], v_tangent_2[1], v_tangent_2[2], 0.0,
            v_normal[0], v_normal[1], v_normal[2], 0.0,
            v_tangent_1[0], v_tangent_1[1], v_tangent_1[2], 0.0,
            position[0], position[1], position[2], 0.0
        ]
        # xform - ws - m
        # ($m[0][0])($m[0][1]) ($m[0][2])($m[0][3])
        # ($m[1][0])($m[1][1]) ($m[1][2])($m[1][3])
        # ($m[2][0])($m[2][1]) ($m[2][2])($m[2][3])
        # ($m[3][0])($m[3][1]) ($m[3][2])($m[3][3])
        cmds.select(obj_name)
        cmds.xform(ws=True, m=matrix)

    # $pObjectName;#}#string $selection[] = `ls - os - fl`;
    # string $faceNames[] = `filterExpand - selectionMask34 - expand true $selection`;
    # string $objectToInstance = $selection[0];
    # if (`objectType $objectToInstance` == "transform")
    # {

    def point_matrix_mult(self, v_point, matrix):
        # i'm 80% sure this is what mel's pointMatrixMult() is doing
        product = [0, 0, 0]
        product[0] = v_point[0] * matrix[0] + v_point[1] * matrix[1] + v_point[2] * matrix[2]
        product[1] = v_point[0] * matrix[4] + v_point[1] * matrix[5] + v_point[2] * matrix[6]
        product[2] = v_point[0] * matrix[8] + v_point[1] * matrix[9] + v_point[2] * matrix[10]
        return product

    def unitize_vector(self, vector):
        print(vector)
        print("unitized!")
        mag = self.mag_vector(vector)
        length = len(vector)
        for c in range (0,length):
            vector[c] = vector[c] / mag
        print(vector)
        return vector

    def cross_mult_vector(self, vector_1, vector_2):
        cross = [0, 0, 0]
        cross[0] = vector_1[1] * vector_2[2] - vector_1[2] * vector_2[1]
        cross[1] = vector_1[2] * vector_2[0] - vector_1[0] * vector_2[2]
        cross[2] = vector_1[0] * vector_2[1] - vector_1[1] * vector_2[0]
        return cross

    def mag_vector(self, vector):
        total = 0
        for c in vector:
            total += c * c
        magnitude = math.sqrt(total)
        return magnitude
