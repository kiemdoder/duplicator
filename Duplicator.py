import bpy

from .dup_duplicate_faces_op import DUP_DuplicateToFacesOperator
from .dup_duplicate_vertices_op import DUP_DuplicateToVerticesOperator
from .dup_panel import DUP_PT_Panel

classes = (
    DUP_DuplicateToFacesOperator,
    DUP_DuplicateToVerticesOperator,
    DUP_PT_Panel
)

register, unregister = bpy.utils.register_classes_factory(classes)
