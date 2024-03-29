import bpy
from bpy.props import BoolProperty, FloatProperty, IntProperty

from .dup_toggle_bounding_box_op import DuplicatorToggleDuplicatedBoundingBoxOperator
from .dup_duplicate_cursor_op import DUP_DuplicateToCursorOperator
from .dup_duplicate_faces_op import DUP_DuplicateToFacesOperator
from .dup_duplicate_vertices_op import DUP_DuplicateToVerticesOperator
from .dup_delete_duplicated_children_op import DUP_DeleteDuplicatedChildrenOperator
from .dup_panel import DuplicationPanel, DuplicationOptionsPanel, DuplicationTargetPanel

bpy.types.Scene.dup_duplicate_tree = BoolProperty(
    name="Duplicate tree",
    description="Duplicate parent and siblings",
    default=True)

bpy.types.Scene.dup_randomise_duplicated = BoolProperty(
    name="Rotation",
    description="Randomise the rotation of an object when it is duplicated",
    default=True)

bpy.types.Scene.dup_random_rotation_factor = FloatProperty(
    name="Random rotation:",
    description="The amount of random rotation to be applied to duplicates",
    default=1.0,
    min=0.0,
    max=1.0)

bpy.types.Scene.dup_randomise_displacement = BoolProperty(
    name="Displace",
    description="Randomise the displacement of an object when it is duplicated",
    default=True)

bpy.types.Scene.dup_random_displacement = FloatProperty(
    name="Random displacement:",
    description="The amount of random displacement to be applied to duplicates",
    default=0.5,
    min=0.0,
    max=1.0)

bpy.types.Scene.dup_randomise_scale = BoolProperty(
    name="Scale",
    description="Randomise the scale of an object when it is duplicated",
    default=False)

bpy.types.Scene.dup_random_scale = FloatProperty(
    name="Random scale",
    description="The amount of random scale to be applied to duplicates",
    default=0.0,
    min=0.0,
    max=1.0)

bpy.types.Scene.dup_density = FloatProperty(
    name="Density",
    description="The fraction of the faces/vertices that must be covered",
    default=1.0,
    min=-0.5,
    max=0.5)

bpy.types.Scene.dup_limit_num_duplications = BoolProperty(
    name="Limit",
    description="Limit the number of objects to be duplicated",
    default=False)

bpy.types.Scene.dup_max_duplications = IntProperty(
    name="Max",
    description="Maximum number of objects to be duplicated",
    default=20,
    min=0)

classes = (
    DUP_DuplicateToCursorOperator,
    DUP_DuplicateToFacesOperator,
    DUP_DuplicateToVerticesOperator,
    DUP_DeleteDuplicatedChildrenOperator,
    DuplicatorToggleDuplicatedBoundingBoxOperator,
    DuplicationPanel,
    DuplicationOptionsPanel,
    DuplicationTargetPanel
)

register, unregister = bpy.utils.register_classes_factory(classes)
