import VisualEngine as V
from RenderObjects import Cube, create_camera, create_sun, draw_camera, X, Y, Z
from treelib import tree as Tree, node as Node

def render_item(canvas, render_object):
    # TEST
    #render_object.rotate(22, 45, 12)
    render_object.rotate(0, 0, 0)
    render_object.draw(canvas)
    #draw_camera(canvas, 25, 25)

def create_object(item, x, y):
    create_camera()
    create_sun()
    c_tree = item.c_tree
    root = c_tree.get_node(c_tree.root)
    root_comp = root.data
    root_obj = RenderObject(root_comp, "", x, y, 0)
    return root_obj

def recursive_add_objects(tree, x, y):
    this_comp = tree.get_node(tree.root)
    children = tree.children(tree.root)
    for child in children:
        child_comp = child.data

        child_obj = RenderObject(child_comp, child_comp.anchor_to_parent_p, x, y, 0)



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

        primitive = component.primitive_shape
        length = primitive.scale_x
        width = primitive.scale_y
        height = primitive.scale_z

        self.geometry = Cube(length, width, height)

    def rotate(self, x, y, z):
        self.geometry.rotate(x, y, z)
        #self.geometry.rot_local(Z, 180)

    def draw(self, canvas):
        self.geometry.draw(canvas, self.x, self.y)
