import bpy


class DuplicationPanel(bpy.types.Panel):
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


class DuplicationOptionsPanel(bpy.types.Panel):
    bl_idname = "Duplication_Options_Panel"
    bl_label = "Duplication options"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Duplicator"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "dup_duplicate_tree")

        row = layout.row()
        row.label(text='Randomise rotation:')
        row = layout.row(align=True)
        row.prop(context.scene, "dup_randomise_duplicated")
        row.prop(context.scene, "dup_random_rotation_factor")

        row = layout.row()
        row.label(text='Randomise displacement:')
        row = layout.row(align=True)
        row.prop(context.scene, "dup_randomise_displacement")
        row.prop(context.scene, "dup_random_displacement")

        row = layout.row()
        row.label(text='Randomise scale:')
        row = layout.row(align=True)
        row.prop(context.scene, "dup_randomise_scale")
        row.prop(context.scene, "dup_random_scale")

        layout.row()
        layout.prop(context.scene, "dup_density")

        row = layout.row()
        row.label(text='Limit duplications:')
        row = layout.row(align=True)
        row.prop(context.scene, "dup_limit_num_duplications")
        row.prop(context.scene, "dup_max_duplications")


class DuplicationTargetPanel(bpy.types.Panel):
    bl_idname = "Duplication_Target_Panel"
    bl_label = "Duplication Target"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Duplicator"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('object.delete_duplicated_children', text="Remove duplicated children")
