import bpy

from . import dup_duplicate_utils


class DuplicatorToggleDuplicatedBoundingBoxOperator(bpy.types.Operator):
    bl_idname = "object.toggle_duplicated_children_bounding_box"
    bl_label = "Toggle duplicates bounding box"
    bl_description = "Toggle bounding box for duplicated children"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        dup_duplicate_utils.toggle_duplicated_children_bounding_box_view_for_selected()
        return {"FINISHED"}
