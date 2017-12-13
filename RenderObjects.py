
from math import cos, sin, atan2, sqrt, degrees, radians, acos, tan, atan, asin

SCALE = 20
CAMERA_VECTOR = None
SUN = None

X = 0
Y = 1
Z = 2

class Cube:
    length = 0
    width = 0
    height = 0
    faces = []
    vertices = []

    def __init__(self, l, w, h):
        self.length = l
        self.width = w
        self.height = h

        self.vertices = self.calculate_vertices(self.length / 2, self.width / 2, self.height / 2)

        # NESWTB
        # North
        self.add_face("North", 1, 2, 6, 5)
        # East
        self.add_face("East", 2, 3, 7, 6)
        # South
        self.add_face("South", 3, 0, 4, 7)
        # West
        self.add_face("West", 0, 1, 5, 4)
        # Top
        self.add_face("Top", 4, 5, 6, 7)
        # Bottom
        self.add_face("Bottom", 0, 1, 2, 3)

    def rotate(self, r_x, r_y, r_z):
        for vert in self.vertices:
            vert.rotate(r_x, r_y, r_z)
        for face in self.faces:
            normal = face.get_normal()
            x, z = normal.get_new_angle()
            print("{}: ({}, {})".format(face.name[0], x, z))

    def rot_local(self, axis, amount):
        axes = self.get_local_axes()
        amount = (amount // 90) * 90
        try:
            normal = axes[axis]
        except IndexError:
            return
        rot_x, rot_z = normal.get_new_angle()
        self.rotate(0, 0, -rot_z)
        self.rotate(-rot_x, 0, 0)
        if axis == X:
            print("Rotating object by {} on its local X axis...".format(amount))
            #self.rotate(amount, 0, 0)
        elif axis == Y:
            print("Rotating object by {} on its local Y axis...".format(amount))
            #self.rotate(0, amount, 0)
        elif axis == Z:
            self.rotate(90, 0, 0)
            print("Rotating object by {} on its local Z axis...".format(amount))
            self.rotate(0, 0, amount)
            self.rotate(-90, 0, 0)

        self.rotate(rot_x, 0, rot_z)
        #rot_x, rot_z = north_normal.get_new_angle()
        #self.rotate(0, 0, -rot_z)
        #self.rotate(-rot_x, 0, 0)

    def rotate_local(self, r_x, r_y, r_z):
        axes = self.get_local_axes()



        # Rotate X
        x_align, y_align, z_align = self.get_axis_offset("x")
        print("X's offset angle: ({}, {}, {})".format(x_align, y_align, z_align))

        self.rotate(0, 0, -x_align)

        x_align, y_align, z_align = self.get_axis_offset("x")

        print("X's offset angle: ({}, {}, {})".format(x_align, y_align, z_align))

        self.rotate(-(y_align), 0, 0)

        x_align, y_align, z_align = self.get_axis_offset("x")

        #print("X's offset angle: ({}, {}, {})".format(x_align, y_align, z_align))

        #self.rotate(0, -z_align, 0)

        #x_align, y_align, z_align = self.get_axis_offset("x")

        print("X's offset angle after global rotation: ({}, {}, {})".format(x_align, y_align, z_align))

        return

    def get_north(self):
        north = self.get_local_axes()[1]
        return north

    def get_axis_offset(self, axis):
        axes = self.get_local_axes()
        if axis == "x":
            local_x = axes[0]
            x_align, y_align, z_align = local_x.get_angle()
            return x_align, y_align, z_align

    def get_local_axes(self):
        x = self.faces[1].get_normal()
        y = self.faces[0].get_normal()
        z = self.faces[4].get_normal()
        return [x, y, z]

    def draw(self, canvas, x, y):
        for face in self.faces:
            face.draw(canvas, x, y)
            #face.draw_two_axis(canvas)

    def add_face(self, name, vert_a, vert_b, vert_c, vert_d):
        v = self.vertices
        verts = [v[vert_a], v[vert_b], v[vert_c], v[vert_d]]
        self.faces.append(Face(verts, name))

    def calculate_vertices(self, x, y, z):
        vertices = list()
        vertices.append(Vector(-x, -y, -z))
        vertices.append(Vector(-x, y, -z))
        vertices.append(Vector(x, y, -z))
        vertices.append(Vector(x, -y, -z))
        vertices.append(Vector(-x, -y, z))
        vertices.append(Vector(-x, y, z))
        vertices.append(Vector(x, y, z))
        vertices.append(Vector(x, -y, z))
        return vertices



class Face:
    vertices = []

    def __init__(self, vertices, name):
        self.vertices = vertices
        self.name = name

    def get_anchor(self):
        total_x = 0
        total_y = 0
        total_z = 0
        for vertex in self.vertices:
            x, y, z = vertex.get()
            total_x += x
            total_y += y
            total_z += z
        verts = len(self.vertices)
        anchor = Vector(total_x / verts, total_y / verts, total_z / verts)
        return anchor

    def get_normal(self):
        anchor = self.get_anchor()
        x, y, z = anchor.get()
        greatest = get_greatest([x, y, z])
        factor = 1 / greatest

        x += (x * 1) * factor
        y += (y * 1) * factor
        z += (z * 1) * factor
        #if x > 0:
        #    x += 1
        #if x < 0:
        #    x -= 1
        #if y > 0:
        #    y += 1
        #if y < 0:
        #    y -= 1
        #if z > 0:
        #    z += 1
        #if z < 0:
        #    z -= 1
        normal = Vector(x, y, z)
        return normal

    def draw(self, canvas, x, y):
        #for line in range(4):
        #    this_index = line
        #    next_index = (line + 1) % 4
        #    a = self.vertices[this_index].get_dimetric_coord()
        #    b = self.vertices[next_index].get_dimetric_coord()
        #    a_x = a[0] + x
        #    a_y = a[1] + y
        #    b_x = b[0] + x
        #    b_y = b[1] + y
        #    canvas.create_line(a_x, a_y, b_x, b_y)

        self.draw_face(canvas, x, y)

    def draw_two_axis(self, canvas):
        normal = self.get_anchor()
        #p, t
        x, z = normal.get_new_angle()
        x_nineties = x // 90
        x_remainder = x % 90
        #y_nineties = y // 90
        #y_remainder = y % 90

        #print("({}, \t{}, \t{}) \t{}".format(int(x),int(y),int(z), self.name))
        print("({}, {}) {}".format(int(x),int(z), self.name))
        new_normal = Vector(0, 1, 0)
        new_normal.rotate(x, 0, z)
        #new_normal.rotate(0, y, 0)
        #new_normal.rotate(x, 0, 0)

        #y, x = new_normal.get_new_angle()
        #print("({}, {}) {}".format(int(y), int(x), self.name))

        normal_coords = new_normal.get_dimetric_coord()
        angle = get_vector_difference(new_normal, CAMERA_VECTOR)
        color = "red" if angle <= 90 else "black"
        canvas.create_line(100, 100, 100 + normal_coords[0], 100 + normal_coords[1], fill=color)
        canvas.create_text(100 + normal_coords[0], 100 + normal_coords[1], text=self.name, fill=color)

    def draw_face(self, canvas, x, y):
        normal = self.get_normal()
        color = "green"
        faces_camera = self.faces_camera(normal)
        if not faces_camera:
            color = "purple"
        coords = []
        for vertex in self.vertices:
            vert_coords = vertex.get_dimetric_coord()
            coords.append([vert_coords[0] + x, vert_coords[1] + y])
        if faces_camera:
            away_from_sun = get_vector_difference(normal, SUN)
            percent_shade = away_from_sun / 180
            color = shader(percent_shade)
            canvas.create_polygon(coords[0][0], coords[0][1],
                              coords[1][0], coords[1][1],
                              coords[2][0], coords[2][1],
                              coords[3][0], coords[3][1],
                              fill=color)

            #self.draw_normal(canvas, x, y, "blue")
        #else:
            #self.draw_normal(canvas, x, y, "red")

    def draw_normal(self, canvas, x, y, color="red"):
        anchor = self.get_anchor()
        anchor_coord = anchor.get_dimetric_coord()
        a_x = anchor_coord[0] + x
        a_y = anchor_coord[1] + y
        canvas.create_text(a_x, a_y, text=self.name)
        ax, ay, az = anchor.get_angle()

        #print("{}'s normal: ({}, {}, {})".format(self.name, ax, ay, az))


        #canvas.create_line(a_x - 2, a_y - 2, a_x + 2, a_y + 2)
        #canvas.create_line(a_x - 2, a_y + 2, a_x + 2, a_y - 2)
        normal = self.get_normal()
        normal_coord = normal.get_dimetric_coord()
        n_x = normal_coord[0] + x
        n_y = normal_coord[1] + y
        canvas.create_line(a_x, a_y, n_x, n_y, fill=color)

    def faces_camera(self, normal):
        facing = True
        angle = get_vector_difference(normal, CAMERA_VECTOR)

        #print("{}'s angle to camera is {}".format(self.name, angle))

        if angle <= 90:
            facing = False

        return facing

        x_neg = get_negative(x)
        y_neg = get_negative(y)
        z_neg = get_negative(z)

        #print("{} -x: {} -y: {} -z: {}".format(self.name, x_neg, y_neg, z_neg))

        x_angle = (degrees(atan2(sqrt((y * y) + (z * z)), x)) * y_neg) % 360
        y_angle = (degrees(atan2(sqrt((z * z) + (x * x)), y)) * x_neg) % 360
        z_angle = (degrees(atan2(sqrt((x * x) + (y * y)), z)) * z_neg) % 360

        print("{}'s normal is rotated ({},{},{})".format(self.name, int(x_angle), int(y_angle), int(z_angle)))

        if z_angle >= 210 or z_angle <= 30:
            facing = False

        if y_angle >= 45 and y_angle <= 225:
            facing = False

        if x_angle >= 45 and x_angle <= 225:
            facing = False


        #if y_angle >= 225 or y_angle < 45:
        #    facing = False
        #
        #if x_angle >= 180:
        #    facing = False

        #if x_angle > 60 and x_angle < 300:
        #    facing = False
        #if y_angle > 60 or y_angle < -60:
        #    facing = False

        #print("{} faces camera: {}".format(self.name, facing))

        return facing


class Vector:
    x = 0
    y = 0
    z = 0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def rotate(self, r_x, r_y, r_z):
        r_x = radians(r_x)
        r_y = radians(r_y)
        r_z = radians(r_z)

        #print("Rotating by ({}, {}, {})".format(degrees(r_x), degrees(r_y), degrees(r_z)))
        #print("Rotating by ({}, {}, {})".format(r_x, r_y, r_z))

        x = self.x
        y = self.y
        z = self.z

        #Rotate x
        x_sub = x
        y_sub = (y * cos(r_x)) - (z * sin(r_x))
        z_sub = (y * sin(r_x)) + (z * cos(r_x))

        x = x_sub
        y = y_sub
        z = z_sub

        # Rotate y
        x_sub = (z * sin(r_y)) + (x * cos(r_y))
        y_sub = y
        z_sub = (z * cos(r_y)) - (x * sin(r_y))

        x = x_sub
        y = y_sub
        z = z_sub

        # Rotate z
        x_sub = (x * cos(r_z)) - (y * sin(r_z))
        y_sub = (x * sin(r_z)) + (y * cos(r_z))
        z_sub = z

        x = x_sub
        y = y_sub
        z = z_sub

        self.x = x
        self.y = y
        self.z = z

    def rot_90(self, r_x, r_y, r_z):
        x = self.x
        y = self.y
        z = self.z
        #Rotate x
        for rot_x in range(r_x // 90):
            y_sub = z
            z_sub = -y
            y = y_sub
            z = z_sub
        # Rotate y
        for rot_y in range(r_y // 90):
            x_sub = -z
            z_sub = x
            x = x_sub
            z = z_sub
        # Rotate z
        for rot_z in range(r_z // 90):
            x_sub = -y
            y_sub = x
            x = x_sub
            y = y_sub
        self.x = x
        self.y = y
        self.z = z
        return

    def get_dimetric_coord(self):
        dx = int((2 * self.x + 2 * self.y) * SCALE)
        dy = int(((self.y - self.x) + 2 * self.z) * -SCALE)
        return [dx, dy]

    def get(self):
        return self.x, self.y, self.z

    def get_angle(self):
        x = self.x
        y = self.y
        z = self.z
        #x_neg = get_negative(x)
        #y_neg = get_negative(y)
        #z_neg = get_negative(z)
        x_neg = 1
        y_neg = 1
        z_neg = 1

        # print("{} -x: {} -y: {} -z: {}".format(self.name, x_neg, y_neg, z_neg))

        #x_angle = degrees(atan2(sqrt((y * y) + (z * z)), z))
        #y_angle = degrees(atan2(sqrt((z * z) + (x * x)), z))
        #z_angle = degrees(atan2(sqrt((x * x) + (y * y)), z))
        #print("X: {}, Y: {}, Z: {}".format(x, y, z))

        x_angle = (degrees(atan2(sqrt((y * y) + (z * z)), x)) * y_neg) % 360
        y_angle = (degrees(atan2(sqrt((z * z) + (x * x)), y)) * x_neg) % 360
        z_angle = (degrees(atan2(sqrt((x * x) + (y * y)), z)) * z_neg) % 360

        return x_angle, y_angle, z_angle

    def get_new_angle(self):
        x = round(self.x, 4)
        y = round(self.y, 4)
        z = round(self.z, 4)
        x_neg = 180 if get_negative(x) == -1 else 0
        y_neg = radians(180) if get_negative(y) == -1 else 0
        z_neg = 180 if get_negative(z) == -1 else 0

        if y != 0:
            r_x = atan(z / y)
        else:
            # Exactly on the origin axis.
            if z != 0:
                r_x = radians(90) * get_negative(z)
            else:
                # 0,0
                r_x = 0
        if y != 0:
            r_z = atan(x / y) + y_neg
        else:
            if x != 0:
                r_z = radians(90) * get_negative(x)
            else:
                r_z = 0

        r_x = (degrees(r_x)) % 360
        r_z = (degrees(r_z)) % 360

        print("P({},{},{}) R({},{})".format(x, y, z, r_x, r_z))

        return r_x, -r_z


        n = sqrt(x * x + y * y)
        if n != 0:
            r = sqrt(x * x + y * y + z * z)
            t = asin(x/n)
            #t = atan(y / x) if x != 0 else radians(90)
            p = acos(z / r)
            #print("T: {}, P: {}".format(int((x/n) * 100) / 100, int((z/r) * 100) / 100))
            #print("T: {}, P: {}".format(int(t * 100) / 100, int(p * 100) / 100))
            #print("T: {}, P: {}".format(int(degrees(t)), int(degrees(p))))
            #t = (degrees(t) * y_neg) % 360
            p = (degrees(p) * y_neg) % 360
            t = degrees(t) % 360
            #p = degrees(p) % 360
        else:
            t = -90 + (90 * z_neg)
            p = 0

        #print("Angle on X-Y Plane: {}, Angle off Z-Axis: {}".format(t, p))

        return p, t

    def __copy__(self):
        return Vector(self.x, self.y, self.z)


def get_negative(number):
    if number == 0:
        return 1
    return number / abs(number)


def get_greatest(in_list):
    greatest = 0
    for number in in_list:
        if abs(number) > greatest:
            greatest = abs(number)
    #print("Of {}, greatest value is {}".format(in_list, greatest))
    return greatest

def create_camera():
    opp_over_adj = tan(30)
    opp = opp_over_adj * 10
    x = sqrt(50)
    y = sqrt(50)
    camera = Vector(-x, y, opp)
    camera_b = create_vector_coords_from_angle(-30, 45)
    ax, ay, az = camera.get()
    bx, by, bz = camera_b.get()
    print("Cameras:\nAX:{} BX:{},\nAY:{} BY:{},\nAZ:{} BZ:{}".format(ax, bx, ay, by, az, bz))
    global CAMERA_VECTOR
    CAMERA_VECTOR = camera_b

def draw_camera(canvas, x, y):
    coords = CAMERA_VECTOR.get_dimetric_coord()
    canvas.create_line(x, y, coords[0] + x, coords[1] + y)
    canvas.create_text(x, y, text="Camera")

def create_sun():
    opp_over_adj = tan(30)
    opp = opp_over_adj * 10
    x = 10
    y = 0
    sun = Vector(-x, y, opp)
    global SUN
    SUN = sun


def create_vector_coords_from_angle(x, z):
    y_axis = Vector(0, 1, 0)
    y_axis.rotate(x, 0, z)
    return y_axis
    #pos_z = tan(z) * 10
    #pos_x = tan(x) * pos_z
    #pos_y = sqrt(100 - pos_x)
    #x = sqrt(50)
    #y = sqrt(50)

def get_vector_difference(vector_a, vector_b):
    x, y, z = vector_a.get()
    a, b, c = vector_b.get()

    angle = degrees(
        acos(((a * x) + (b * y) + (c * z)) / (sqrt((a * a) + (b * b) + (c * c)) * sqrt((x * x) + (y * y) + (z * z)))))
    return angle

def shader(percent):
    red = int(50 * percent)
    blue = int(50 * percent)
    green = int(255 * percent)
    return "#%02x%02x%02x" % (red, green, blue)
