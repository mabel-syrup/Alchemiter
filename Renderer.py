import VisualEngine as V
from RenderObjects import Cube, Vector, create_camera, create_sun, draw_camera, X, Y, Z
from treelib import tree as Tree, node as Node
from AlchemyGlobal import FONT

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
TOP = 4
BOTTOM = 5


def render_item(canvas, render_objects, diagram=False):
    # TEST
    #render_object.rotate(22, 45, 12)
    #render_object.rotate(0, 0, 0)
    print("RENDERING ITEM")
    lowest_layer = 0
    highest_layer = 0
    obj_dict = {}
    for render_object in render_objects:
        layer = render_object.layer
        print("Object is on layer {}".format(layer))
        if layer < lowest_layer:
            lowest_layer = layer
        if layer > highest_layer:
            highest_layer = layer
        if layer not in obj_dict:
            obj_dict[layer] = []
        obj_dict[layer].append(render_object)
        #render_object.draw(canvas)
    for layer in range(lowest_layer, highest_layer + 1):
        print("Rendering layer {}".format(layer))
        if layer in obj_dict:
            print("Layer {} has {} objects".format(layer, len(obj_dict[layer])))
            for obj in obj_dict[layer]:
                obj.draw(canvas)
                if diagram:
                    obj.draw_name(canvas)
    #draw_camera(canvas, 25, 25)

def create_object(item, x, y, rotation=0, zoom=1):
    create_camera()
    create_sun()
    objects = []
    c_tree = item.c_tree
    root = c_tree.get_node(c_tree.root)
    root_comp = root.data
    root_obj = RenderObject(root_comp, "", x, y, 0)
    root_obj.scale(zoom)
    root_obj.rotate(0, 0, rotation)
    objects.append(root_obj)
    recursive = recursive_add_objects(c_tree, root_obj, x, y, 0)
    for render_object in recursive:
        objects.append(render_object)
    return objects

def recursive_add_objects(tree, parent, x, y, layer):
    objects = []
    this_comp = tree.get_node(tree.root)
    children = tree.children(tree.root)
    print("Getting children for {}...".format(this_comp.data.name))
    for child in children:
        child_id = child.identifier
        child_comp = child.data
        print("Processing {}...".format(child_comp.name))
        print("{} is on layer {}".format(child_comp.name, layer))
        parent_vector_name = child_comp.anchor_to_parent_p
        child_vector_name = child_comp.anchor_to_parent_c
        child_obj = RenderObject(child_comp, parent_vector_name, x, y, layer)
        parent_vector = parent.get_normal(get_id_from_name(parent_vector_name))
        child_vector = child_obj.get_normal(get_id_from_name(child_vector_name))

        parent_attachment = parent.geometry.get_attachment_for_face(get_id_from_name(parent_vector_name))
        child_attachment = child_obj.geometry.get_attachment_for_face(get_id_from_name(child_vector_name))
        factor = parent_attachment / child_attachment
        print("Child attachment size: {} Parent Attachment size: {}".format(child_attachment, parent_attachment))

        child_obj.scale(factor)
        p_x, p_z = parent_vector.get_new_angle()
        c_x, c_z = child_vector.get_new_angle()
        print("Parent Vector: {} ({}, {})\nChild Vector: {} ({}, {})".format(parent_vector_name, p_x, p_z, child_vector_name, c_x, c_z))

        #child_obj.rotate(p_x, 0, p_z)
        #child_obj.rotate_local(X, p_x)
        #child_obj.rotate_local(Z, p_z)
        child_obj.rotate_local(X, c_x)
        child_obj.rotate_local(Z, c_z)
        child_obj.rotate_local(X, p_x)
        child_obj.rotate(0, 0, p_z)

        #r_x = (180 - (p_x - c_x)) % 360
        #r_z = (180 - (p_z + c_z)) % 360
        #print("Rotating child by ({}, {})".format(r_x, r_z))
        #child_obj.rotate(r_x, 0, r_z)
        child_vector = child_obj.get_normal(get_id_from_name(child_vector_name))
        c_v_x, c_v_y, c_v_z = parent_vector.get()

        if int(c_v_x * 100) / 100 < 0 or int(c_v_y * 100) / 100 > 0 or int(c_v_z * 100) / 100 < 0:
            child_layer = layer - 1
        else:
            child_layer = layer + 1
        print("{}: ({}, {}, {}): {}".format(child_comp.name, int(c_v_x * 100) / 100, int(c_v_y * 100) / 100, int(c_v_z * 100) / 100, child_layer - layer))
        child_obj.set_layer(child_layer)
        child_obj.translate_by_vector(parent_vector)
        child_obj.translate_by_vector(child_vector, True)


        child_coords = child_obj.get_position()
        objects.append(child_obj)
        child_children = recursive_add_objects(tree.subtree(child_id), child_obj, child_coords[0], child_coords[1], child_layer)
        for child_child in child_children:
            objects.append(child_child)
    return objects


def get_id_from_name(name):
    if name == "north":
        return NORTH
    elif name == "east":
        return EAST
    elif name == "south":
        return SOUTH
    elif name == "west":
        return WEST
    elif name == "top":
        return TOP
    elif name == "bottom":
        return BOTTOM
    else:
        return 6


def clear_canvas(canvas):
    items = canvas.find_all()
    for item in items:
        canvas.delete(item)


class RenderObject:

    def __init__(self, component, parent_normal, offset_x, offset_y, layer):
        self.component = component
        self.parent_normal = parent_normal
        self.x = offset_x
        self.y = offset_y
        self.layer = layer
        self.name = component.name

        primitive = component.primitive_shape
        length = primitive.scale_x
        width = primitive.scale_y
        height = primitive.scale_z

        self.geometry = Cube(length, width, height)

    def set_layer(self, layer):
        self.layer = layer

    def get_position(self):
        return [self.x, self.y]

    def get_normal(self, normal_ID):
        if normal_ID == 6:
            return Vector(0, 0, 0)
        return self.geometry.get_face_anchor(normal_ID)

    def translate_by_vector(self, vector, inverse=False):
        x, y, z = vector.get()
        if inverse:
            x = -x
            y = -y
            z = -z
        self.translate(x, y, z)

    def translate(self, x, y, z):
        translation = Vector(x, y, z)
        print("Translating {}, {}, {}".format(x, y, z))
        coords = translation.get_dimetric_coord()
        self.x += coords[0]
        self.y += coords[1]

    def rotate_local(self, axis, amount):
        self.geometry.rot_local(axis, amount)

    def rotate(self, x, y, z):
        self.geometry.rotate(x, y, z)
        #self.geometry.rot_local(Z, 180)

    def scale(self, factor):
        self.geometry.scale(factor)

    def draw(self, canvas):
        self.geometry.draw(canvas, self.x, self.y)

    def draw_name(self, canvas):
        canvas.create_text(self.x, self.y, text=self.name, fill="blue", font=FONT)
