import bpy

from . import dup_duplicate_utils


class DUP_DuplicateToCursorOperator(bpy.types.Operator):
    bl_idname = "object.duplicate_to_cursor"
    bl_label = "Duplicate to cursor"
    bl_description = "Duplicate the selected object to the cursor"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        dup_duplicate_utils.duplicate_selected()
        return {"FINISHED"}
