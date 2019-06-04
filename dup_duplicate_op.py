import bpy

import dup_duplicate_utils


class DUP_DuplicateToFacesOperator(bpy.types.Operator):
    bl_idname = "object.duplicate_to_faces"
    bl_label = "Duplicate to faces"
    bl_description = "Duplicate the selected object to the active object's faces"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        dup_duplicate_utils.duplicate_selected_to_faces()
        return {"FINISHED"}
