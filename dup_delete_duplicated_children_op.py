import bpy

from . import dup_duplicate_utils


class DUP_DeleteDuplicatedChildrenOperator(bpy.types.Operator):
    bl_idname = "object.delete_duplicated_children"
    bl_label = "Delete duplicated children"
    bl_description = "Delete the duplicated children of selected objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        dup_duplicate_utils.delete_duplicated_children_for_selected()
        return {"FINISHED"}
