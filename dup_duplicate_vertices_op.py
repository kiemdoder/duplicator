import bpy

from . import dup_duplicate_utils


class DUP_DuplicateToVerticesOperator(bpy.types.Operator):
    bl_idname = "object.duplicate_to_vertices"
    bl_label = "Duplicate to vertices"
    bl_description = "Duplicate the selected object to the active object's vertices"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        dup_duplicate_utils.duplicate_selected_to_vertices()
        return {"FINISHED"}
