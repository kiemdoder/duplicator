import bpy


class DUP_PT_Panel(bpy.types.Panel):
    bl_idname = "DUP_PT_Panel"
    bl_label = "Duplicator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Duplicator"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('object.duplicate_to_faces', text="Duplicate to faces")
        row = layout.row()
        row.operator('object.duplicate_to_vertices', text="Duplicate to vertices")
