import bpy
from bpy.props import BoolProperty, FloatProperty

from .dup_duplicate_cursor_op import DUP_DuplicateToCursorOperator
from .dup_duplicate_faces_op import DUP_DuplicateToFacesOperator
from .dup_duplicate_vertices_op import DUP_DuplicateToVerticesOperator
from .dup_delete_duplicated_children_op import DUP_DeleteDuplicatedChildrenOperator
from .dup_panel import DUP_PT_Panel

bpy.types.Scene.dup_duplicate_tree = BoolProperty(
    name="Duplicate tree",
    description="Duplicate parent and siblings",
    default=True)

bpy.types.Scene.dup_randomise_duplicated = BoolProperty(
    name="Randomise rotation",
    description="Randomise the rotation of an object when it is duplicated",
    default=True)

bpy.types.Scene.dup_random_rotation_factor = FloatProperty(
    name="Random rotation",
    description="The amount of random rotation to be applied to duplicates",
    default=1.0,
    min=0.0,
    max=1.0)

bpy.types.Scene.dup_randomise_displacement = BoolProperty(
    name="Randomise displacement",
    description="Randomise the displacement of an object when it is duplicated",
    default=True)

bpy.types.Scene.dup_random_displacement = FloatProperty(
    name="Random displacement",
    description="The amount of random displacement to be applied to duplicates",
    default=0.5,
    min=0.0,
    max=1.0)

bpy.types.Scene.dup_density = FloatProperty(
    name="Density",
    description="The fraction of the faces/vertices that must be covered",
    default=1.0,
    min=0.0,
    max=1.0)

classes = (
    DUP_DuplicateToCursorOperator,
    DUP_DuplicateToFacesOperator,
    DUP_DuplicateToVerticesOperator,
    DUP_DeleteDuplicatedChildrenOperator,
    DUP_PT_Panel
)

register, unregister = bpy.utils.register_classes_factory(classes)
