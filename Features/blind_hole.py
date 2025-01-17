import math
import numpy as np
import Utils.occ_utils as occ_utils
import random
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.gp import gp_Circ, gp_Ax2, gp_Pnt, gp_Dir
from Features.machining_features import MachiningFeature


class BlindHole(MachiningFeature):
    def __init__(self, shape, label_map, min_len, clearance, feat_names):
        super().__init__(shape, label_map, min_len, clearance, feat_names)
        self.shifter_type = 4
        self.bound_type = 4
        self.depth_type = "blind"
        self.feat_type = "blind_hole"

    def _add_sketch(self, bound):
        dir_w = bound[2] - bound[1]
        dir_h = bound[0] - bound[1]
        width = np.linalg.norm(dir_w)
        height = np.linalg.norm(dir_h)

        dir_w = dir_w / width
        dir_h = dir_h / height
        normal = np.cross(dir_w, dir_h)

        # radius = min(width / 2, height / 2)
        radius = random.randint(5, 10)

        center = (bound[0] + bound[1] + bound[2] + bound[3]) / 4
        # print(center)

        circ = gp_Circ(gp_Ax2(gp_Pnt(center[0], center[1], center[2]), occ_utils.as_occ(normal, gp_Dir)), radius)
        edge = BRepBuilderAPI_MakeEdge(circ, 0., 2 * math.pi).Edge()
        outer_wire = BRepBuilderAPI_MakeWire(edge).Wire()

        face_maker = BRepBuilderAPI_MakeFace(outer_wire)


        circ1 = gp_Circ(gp_Ax2(gp_Pnt(center[0], center[1], center[2]), occ_utils.as_occ(normal, gp_Dir)), radius+3)
        edge1 = BRepBuilderAPI_MakeEdge(circ1, 0., 2 * math.pi).Edge()
        outer_wire1 = BRepBuilderAPI_MakeWire(edge1).Wire()
        face_maker1 = BRepBuilderAPI_MakeFace(outer_wire1)

        return face_maker.Face()