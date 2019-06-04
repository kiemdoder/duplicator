import bpy


class DUP_PT_Panel(bpy.types.Panel):
    bl_idname = "DUP_PT_Panel"
    bl_label = "Center"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Object Snapping"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('object.duplicate_to_faces', text="Duplicate")
