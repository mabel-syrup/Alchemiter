
SCALE = 20


def draw_item_bounds(canvas, item, x, y):
    clear_canvas(canvas)
    recursive_comp_render(canvas, item.c_tree, x, y)


def recursive_comp_render(canvas, tree, x, y):
    this_node = tree.get_node(tree.root)
    this_comp = this_node.data

    bounds = BoundingBox(this_comp)
    anchors = bounds.get_anchor_coords()
    offset = get_inverse_offset(this_comp.anchor_to_parent_c, anchors)
    print("Offsetting {} by ({}, {})".format(this_comp.name, offset[0], offset[1]))
    x += offset[0]
    y += offset[1]
    #canvas.create_text(x, y, text=this_comp.anchor_to_parent_c)
    #canvas.create_line(x - 2, y - 2, x + 2, y + 2, fill="green")
    #canvas.create_line(x + 2, y - 2, x - 2, y + 2, fill="green")
    draw_outline(canvas, this_comp, x, y)

    children = tree.children(tree.root)
    for child in children:
        child_comp = child.data

        child_offset = get_offset(child_comp.anchor_to_parent_p, anchors)
        canvas.create_text(x + child_offset[0], y + child_offset[1], text=child_comp.anchor_to_parent_p)
        print("Offsetting {} by ({}, {})".format(child_comp.name, child_offset[0], child_offset[1]))
        c_x = x + child_offset[0]
        c_y = y + child_offset[1]


        #child_bounds = BoundingBox(child_comp)
        #child_anchors = child_bounds.get_anchor_coords()
        #child_offset = get_offset(child_comp.anchor_to_parent_c, child_anchors)
        #parent_offset = get_offset(child_comp.anchor_to_parent_p, anchors)
        #c_x = x + (child_offset[0] + parent_offset[0])
        #c_y = y + (child_offset[1] + parent_offset[1])
        #canvas.create_text(x + parent_offset[0], y + parent_offset[1], text=child_comp.anchor_to_parent_p[0])
        #canvas.create_text(x + child_offset[0], y + child_offset[1], text=child_comp.anchor_to_parent_p[0].upper())


        c_tree = tree.subtree(child.identifier)
        recursive_comp_render(canvas, c_tree, c_x, c_y)


def get_offset(anchor, anchor_coords):
    anchor = anchor.lower()
    if anchor == "north":
        offset = anchor_coords[0]
    elif anchor == "east":
        offset = anchor_coords[1]
    elif anchor == "south":
        offset = anchor_coords[2]
    elif anchor == "west":
        offset = anchor_coords[3]
    elif anchor == "top":
        offset = anchor_coords[4]
    elif anchor == "bottom":
        offset = anchor_coords[5]
    else:
        offset = [0, 0]
    return offset


def get_inverse_offset(anchor, anchor_coords):
    anchor = anchor.lower()
    if anchor == "north":
        offset = anchor_coords[2]
    elif anchor == "east":
        offset = anchor_coords[3]
    elif anchor == "south":
        offset = anchor_coords[0]
    elif anchor == "west":
        offset = anchor_coords[1]
    elif anchor == "top":
        offset = anchor_coords[5]
    elif anchor == "bottom":
        offset = anchor_coords[4]
    else:
        offset = [0, 0]
    return offset


def clear_canvas(canvas):
    items = canvas.find_all()
    for item in items:
        canvas.delete(item)


def draw_outline(canvas, component, x, y):
    bounds = BoundingBox(component)
    corners = bounds.get_eight_corners()

    corner_dict = {}
    corner_dict['BSW'] = corners[0]
    corner_dict['BNW'] = corners[1]
    corner_dict['BNE'] = corners[2]
    corner_dict['BSE'] = corners[3]
    corner_dict['TSW'] = corners[4]
    corner_dict['TNW'] = corners[5]
    corner_dict['TNE'] = corners[6]
    corner_dict['TSE'] = corners[7]

    draw_corner_to_corner(corner_dict, canvas, 'BSW', 'BNW', x, y)
    draw_corner_to_corner(corner_dict, canvas, 'BNW', 'BNE', x, y)
    draw_corner_to_corner(corner_dict, canvas, 'BNE', 'BSE', x, y)
    draw_corner_to_corner(corner_dict, canvas, 'BSE', 'BSW', x, y)

    draw_corner_to_corner(corner_dict, canvas, 'TSW', 'TNW', x, y)
    draw_corner_to_corner(corner_dict, canvas, 'TNW', 'TNE', x, y)
    draw_corner_to_corner(corner_dict, canvas, 'TNE', 'TSE', x, y)
    draw_corner_to_corner(corner_dict, canvas, 'TSE', 'TSW', x, y)

    draw_corner_to_corner(corner_dict, canvas, 'BSW', 'TSW', x, y)
    draw_corner_to_corner(corner_dict, canvas, 'BNW', 'TNW', x, y)
    draw_corner_to_corner(corner_dict, canvas, 'BNE', 'TNE', x, y)
    draw_corner_to_corner(corner_dict, canvas, 'BSE', 'TSE', x, y)

    draw_corner_to_corner(corner_dict, canvas, 'BNE', 'TNW', x, y, "red")     # North
    draw_corner_to_corner(corner_dict, canvas, 'BSE', 'TNE', x, y, "yellow")  # East
    draw_corner_to_corner(corner_dict, canvas, 'BSE', 'TSW', x, y, "green")   # South
    draw_corner_to_corner(corner_dict, canvas, 'BSW', 'TNW', x, y, "blue")    # West
    draw_corner_to_corner(corner_dict, canvas, 'TSW', 'TNE', x, y, "purple")  # Top
    #draw_corner_to_corner(corner_dict, canvas, 'BSW', 'BSE', x, y, "brown")   # Bottom

    return

    top_corners = corners[0:4]
    for index in range(len(top_corners)):
        corner = top_corners[index]
        next_corner = top_corners[(index + 1) % len(top_corners)]
        draw_line(canvas, corner, next_corner, x, y)
    bottom_corners = corners[4:]
    for index in range(len(bottom_corners)):
        corner = bottom_corners[index]
        next_corner = bottom_corners[(index + 1) % len(bottom_corners)]
        draw_line(canvas, corner, next_corner, x, y)
    for index in range(len(bottom_corners)):
        corner = bottom_corners[index]
        next_corner = top_corners[index]
        draw_line(canvas, corner, next_corner, x, y)


def draw_corner_to_corner(corners, canvas, corner_a, corner_b, offset_x=0, offset_y=0, color="black"):
    try:
        a = corners[corner_a]
        b = corners[corner_b]
    except KeyError:
        return
    draw_line(canvas, a, b, offset_x, offset_y, color)


def draw_line(canvas, coord_a, coord_b, offset_x=0, offset_y=0, color="black"):
    a_x = coord_a[0] + offset_x
    a_y = coord_a[1] + offset_y
    b_x = coord_b[0] + offset_x
    b_y = coord_b[1] + offset_y
    canvas.create_line(a_x, a_y, b_x, b_y, fill=color)


def draw_bounds(canvas, component, x, y):
    bounds = BoundingBox(component)
    corners = bounds.get_eight_corners()

    for corner in corners:
        cx = corner[0] + x
        cy = corner[1] + y
        canvas.create_line(cx-2, cy-2, cx+2, cy+2)
        canvas.create_line(cx+2, cy-2, cx-2, cy+2)

    #for corner in corners:
    #    for corner_b in corners:
    #        if corner_b == corner:
    #            continue
    #        x_a = corner[0] + x
    #        y_a = corner[1] + y
    #        x_b = corner_b[0] + y
    #        y_b = corner_b[1] + y
    #        canvas.create_line(x_a, y_a, x_b, y_b)


class BoundingBox:
    component = None
    coord = None
    rot_x = 0
    rot_y = 0
    rot_z = 0

    anchors = []
    corners = []

    def __init__(self, component, coord=None):
        if coord is None:
            coord = Coordinate(0, 0, 0)
        self.component = component
        self.coord = coord
        self.anchors = self.get_anchor_coords()
        self.corners = self.get_eight_corners()

    def get_anchor_coords(self):
        primitive = self.component.primitive_shape
        anchors = []

        x = primitive.scale_x / 2
        y = primitive.scale_y / 2
        z = primitive.scale_z / 2

        anchors.append(self.make_screen_coord(self.coord, 0, y, 0))
        anchors.append(self.make_screen_coord(self.coord, x, 0, 0))
        anchors.append(self.make_screen_coord(self.coord, 0, -y, 0))
        anchors.append(self.make_screen_coord(self.coord, -x, 0, 0))
        anchors.append(self.make_screen_coord(self.coord, 0, 0, z))
        anchors.append(self.make_screen_coord(self.coord, 0, 0, -z))

        return anchors

    def get_eight_corners(self):
        corners = []
        # Bottom: SW, NW, NE, SE
        # Top: SW, NW, NE, SE
        primitive = self.component.primitive_shape
        x = primitive.scale_x / 2
        y = primitive.scale_y / 2
        z = primitive.scale_z / 2



        corners.append(self.make_screen_coord(self.coord, -x, -y, -z))
        corners.append(self.make_screen_coord(self.coord, -x, y, -z))
        corners.append(self.make_screen_coord(self.coord, x, y, -z))
        corners.append(self.make_screen_coord(self.coord, x, -y, -z))
        corners.append(self.make_screen_coord(self.coord, -x, -y, z))
        corners.append(self.make_screen_coord(self.coord, -x, y, z))
        corners.append(self.make_screen_coord(self.coord, x, y, z))
        corners.append(self.make_screen_coord(self.coord, x, -y, z))
        return corners


    def make_screen_coord(self, root, x, y, z):
        coord = self.make_coord(root, x, y, z)
        return coord.get_dimetric_coord()

    def make_coord(self, root, x, y, z):
        coord = Coordinate(0, 0, 0)
        coord.offset(x, y, z, root)
        return coord


class Coordinate:
    x = 0.0
    y = 0.0
    z = 0.0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def offset(self, x, y, z, coord=None):
        if coord is None:
            coord = self
        self.x = coord.x + x
        self.y = coord.y + y
        self.z = coord.z + z

    def get_dimetric_coord(self):
        dx = int((2 * self.x + 2 * self.y) * SCALE)
        dy = int(((self.y - self.x) + 2 * self.z) * -SCALE)
        return [dx, dy]
