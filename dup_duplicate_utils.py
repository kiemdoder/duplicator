import bpy
import mathutils
import math
import random


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


def rotate_obj_z(obj, factor=1.0):
    angle = random.random() * factor * math.pi - (math.pi / 2)
    obj.rotation_mode = 'ZXY'
    obj.rotation_euler.rotate_axis("Z", angle)


def duplicate_obj(name, src_obj, col=None, location=(0, 0, 0)):
    if not col:
        col = bpy.context.collection

    new_obj = bpy.data.objects.new(name, src_obj.data)
    new_obj.location = location

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

    for child in src_obj.children:
        new_child = duplicate_obj(child.name, child, col)
        new_child.parent = new_obj

    return new_obj


def duplicate_selected(col=None):
    src_obj = bpy.context.object
    location = bpy.context.scene.cursor.location
    if src_obj:
        duplicate_obj(src_obj.name, src_obj, col, location)


def align_obj_with_normal(obj, normal):
    rot_diff = mathutils.Vector((0, 0, 1)).rotation_difference(normal)
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = obj.rotation_quaternion @ rot_diff


def move_to_face(obj, face):
    obj.location = face.center
    align_obj_with_normal(obj, face.normal)


def move_to_vertex(obj, vertex):
    obj.location = vertex.co
    align_obj_with_normal(obj, vertex.normal)


def duplicate_to_faces(src_obj, target, col=None):
    """Duplicate the selected object to the faces of the active object"""
    for face in target.data.polygons:
        new_obj = duplicate_obj(target.name, src_obj, col)
        new_obj.parent = target
        move_to_face(new_obj, face)
        rotate_obj_z(new_obj)


def duplicate_selected_to_faces(col=None):
    if len(bpy.context.selected_objects) > 1:
        source = bpy.context.selected_objects[1]
        target = bpy.context.object
        if source:
            duplicate_to_faces(source, target, col)


def duplicate_selected_to_vertices(col=None):
    if len(bpy.context.selected_objects) > 1:
        source = bpy.context.selected_objects[1]
        target = bpy.context.object
        if source:
            duplicate_to_vertices(source, target, col)


def duplicate_to_vertices(src_obj, target, col=None):
    for vertex in target.data.vertices:
        new_obj = duplicate_obj(target.name, src_obj, col)
        new_obj.parent = target
        move_to_vertex(new_obj, vertex)


def delete_children(obj):
    for child in obj.children:
        delete_children(child)
        bpy.data.objects.remove(child, do_unlink=True)

# duplicate_obj('takkie2', bpy.data.objects['takkie'])
# duplicate_selected()
# rotate_obj_Z(bpy.data.objects['Cube'])
# duplicate_to_faces(bpy.data.objects['takkie'], bpy.data.objects['copy-target1'])
# duplicate_to_vertices(bpy.data.objects['Cube'], bpy.data.objects['copy-target1'])
# delete_children(bpy.data.objects['copy-target1'])
