import bpy
import mathutils
import math
import random
import sys


def generic_copy(source, target, string=""):
    """Copy attributes from source to target that have string in them"""
    for attr in dir(source):
        if attr.find(string) > -1:
            try:
                setattr(target, attr, getattr(source, attr))
            except:
                pass
    return


def copy_modifiers(src_obj, dest_obj):
    for modifier in src_obj.modifiers:
        new_modifier = dest_obj.modifiers.new(
            type=modifier.type,
            name=modifier.name
        )
        generic_copy(modifier, new_modifier)


def deselect_all():
    selected = bpy.context.selected_objects
    for obj in selected:
        obj.select_set(False)

    return selected


def select_objects(objects):
    for obj in objects:
        obj.select_set(True)


def root_parent(obj):
    if obj.parent:
        return root_parent(obj.parent)
    else:
        return obj


def sub_tree_hide_viewport(obj, hidden):
    for child in obj.children:
        child.hide_viewport = hidden
        sub_tree_hide_viewport(child, hidden)


def copy_particle_systems(from_obj, to_obj):
    selected = deselect_all()
    active = bpy.context.object

    to_obj.select_set(True)
    from_obj.select_set(True)
    bpy.context.view_layer.objects.active = from_obj

    bpy.ops.particle.copy_particle_systems()

    to_obj.select_set(False)
    from_obj.select_set(False)

    # restore selected + active
    select_objects(selected)
    if active:
        bpy.context.view_layer.objects.active = active


def rotate_obj_z(obj):
    if bpy.context.scene.dup_randomise_duplicated:
        factor = bpy.context.scene.dup_random_rotation_factor
        left_right = -1 if random.random() < 0.5 else 1
        angle = random.random() * factor * (math.pi / 2) * left_right
        obj.rotation_mode = 'ZXY'
        obj.rotation_euler.rotate_axis("Z", angle)


def scale_obj(obj):
    if bpy.context.scene.dup_randomise_scale:
        (sx, sy, sz) = obj.scale
        up_down = 0.5 if random.random() < 0.5 else -0.5
        scale_delta = 1.0 + (random.random() *
                             bpy.context.scene.dup_random_scale * up_down)
        obj.scale = (sx * scale_delta, sy * scale_delta, sz * scale_delta)


def duplicate_obj(name, src_obj, col=None):
    if not col:
        col = bpy.context.collection

    new_obj = bpy.data.objects.new(name, src_obj.data)
    new_obj['duplicated'] = {
        'bounding_box': False
    }

    # add to collection
    col.objects.link(new_obj)

    # copy attributes
    copy_modifiers(src_obj, new_obj)

    if src_obj.particle_systems:
        copy_particle_systems(src_obj, new_obj)

    new_obj.instance_type = src_obj.instance_type
    new_obj.use_instance_faces_scale = src_obj.use_instance_faces_scale
    new_obj.show_instancer_for_viewport = src_obj.show_instancer_for_viewport
    new_obj.show_instancer_for_render = src_obj.show_instancer_for_render
    new_obj.instance_faces_scale = src_obj.instance_faces_scale

    new_obj.display_type = src_obj.display_type
    new_obj.hide_render = src_obj.hide_render

    return new_obj


def duplicate_tree(name, src_obj, col=None, offset=mathutils.Vector((0, 0, 0))):
    new_obj = duplicate_obj(name, src_obj, col)
    for child in src_obj.children:
        loc_offset = child.location - src_obj.location + offset
        new_child = duplicate_tree(child.name, child, col, loc_offset)
        new_child.parent = new_obj
        if src_obj.instance_type == 'NONE':
            new_child.location = new_child.location + loc_offset

    return new_obj


def duplicate_selected(col=None):
    src_obj = bpy.context.object
    if bpy.context.scene.dup_duplicate_tree:
        src_obj = root_parent(src_obj)

    if src_obj:
        new_obj = duplicate_tree(src_obj.name, src_obj, col)
        new_obj.location = bpy.context.scene.cursor.location


def align_obj_with_normal(obj, normal):
    rot_diff = mathutils.Vector((0, 0, 1)).rotation_difference(normal)
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = obj.rotation_quaternion @ rot_diff


def move_to_face(obj, face):
    obj.location = face.center
    align_obj_with_normal(obj, face.normal)

    if bpy.context.scene.dup_randomise_displacement:
        local_x_axis = mathutils.Vector((0, 0, 1)).cross(face.normal)
        if local_x_axis.length == 0:
            local_x_axis = mathutils.Vector((1, 0, 0))
        local_y_axis = local_x_axis.cross(face.normal)
        square_face_width = math.sqrt(face.area)
        displace_factor = bpy.context.scene.dup_random_displacement

        if random.random() > 0.5:
            local_x_axis.negate()

        if random.random() > 0.5:
            local_y_axis.negate()

        local_x_axis.length = random.random() * (square_face_width / 2) * displace_factor
        local_y_axis.length = random.random() * (square_face_width / 2) * displace_factor

        obj.location = obj.location + local_x_axis + local_y_axis


def move_to_vertex(obj, vertex):
    obj.location = vertex.co
    align_obj_with_normal(obj, vertex.normal)


def selected_src_obj():
    for obj in bpy.context.selected_objects:
        if obj.name != bpy.context.object.name:
            return obj

    return None


def rand_elements(collection, max=sys.maxsize):
    num_elements = min(
        round(len(collection) * bpy.context.scene.dup_density), max)
    return random.choices(collection, k=num_elements)


def duplicate_to_faces(src_obj, target, col=None):
    """Duplicate the selected object to the faces of the active object"""
    if bpy.context.scene.dup_duplicate_tree:
        src_obj = root_parent(src_obj)

    target.instance_type = 'NONE'

    max_duplications = bpy.context.scene.dup_max_duplications if bpy.context.scene.dup_limit_num_duplications else sys.maxsize
    for face in rand_elements(target.data.polygons, max_duplications):
        new_obj = duplicate_tree(target.name, src_obj, col)
        new_obj.parent = target
        move_to_face(new_obj, face)
        rotate_obj_z(new_obj)
        scale_obj(new_obj)


def duplicate_selected_to_faces(col=None):
    if len(bpy.context.selected_objects) > 1:
        source = selected_src_obj()
        target = bpy.context.object
        if source:
            duplicate_to_faces(source, target, col)


def duplicate_to_vertices(src_obj, target, col=None):
    if bpy.context.scene.dup_duplicate_tree:
        src_obj = root_parent(src_obj)

    max_duplications = bpy.context.scene.dup_max_duplications if bpy.context.scene.dup_limit_num_duplications else sys.maxsize
    for vertex in rand_elements(target.data.vertices, max_duplications):
        if random.random() < bpy.context.scene.dup_density:
            new_obj = duplicate_tree(target.name, src_obj, col)
            new_obj.parent = target
            move_to_vertex(new_obj, vertex)
            rotate_obj_z(new_obj)
            scale_obj(new_obj)


def duplicate_selected_to_vertices(col=None):
    if len(bpy.context.selected_objects) > 1:
        source = selected_src_obj()
        target = bpy.context.object
        if source:
            duplicate_to_vertices(source, target, col)


def delete_duplicated_children(obj):
    for child in obj.children:
        if 'duplicated' in child:
            delete_duplicated_children(child)
            bpy.data.objects.remove(child, do_unlink=True)


def delete_duplicated_children_for_selected():
    for obj in bpy.context.selected_objects:
        delete_duplicated_children(obj)


def toggle_duplicated_children_bounding_box_view(obj):
    for child in obj.children:
        if 'duplicated' in child:
            duplicated = child['duplicated']
            show_bounding_box = not duplicated['bounding_box']

            sub_tree_hide_viewport(child, show_bounding_box)

            duplicated['bounding_box'] = show_bounding_box
            if child.display_type == 'BOUNDS' and not show_bounding_box:
                child.display_type = 'TEXTURED'
            elif child.display_type == 'TEXTURED' and show_bounding_box:
                child.display_type = 'BOUNDS'


def toggle_duplicated_children_bounding_box_view_for_selected():
    for obj in bpy.context.selected_objects:
        toggle_duplicated_children_bounding_box_view(obj)
