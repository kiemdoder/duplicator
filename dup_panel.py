import bpy


class DUP_PT_Panel(bpy.types.Panel):
    bl_idname = "DUP_PT_Panel"
    bl_label = "Duplicate selected to:"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Duplicator"

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.operator('object.duplicate_to_faces', text="Faces")
        row.operator('object.duplicate_to_vertices', text="Vertices")
        row.operator('object.duplicate_to_cursor', text="Cursor")

        layout.row()
        layout.prop(context.scene, "dup_duplicate_tree")
        layout.row()
        layout.prop(context.scene, "dup_randomise_duplicated")
        layout.row()
        layout.prop(context.scene, "dup_random_rotation_factor")
        layout.row()
        layout.prop(context.scene, "dup_density")

        row = layout.row()
        row.operator('object.delete_duplicated_children', text="Remove duplicated children")