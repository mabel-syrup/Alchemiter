from AlchemyGlobal import primitives, mechanisms, abilities

class Material:
    name = ''
    roughness = 0
    conductivity = 0
    reflectivity = 0
    weight = 0

    def __init__(self, name, roughness, conductivity, reflectivity, weight):
        """Define the characteristics of the Material.  Scale is 0 to 100."""
        self.name = name
        self.roughness = roughness
        self.conductivity = conductivity
        self.reflectivity = reflectivity
        self.weight = weight


class ColorScheme:
    name = ''
    color_primary = ''
    color_secondary = ''
    color_tertiary = ''

    def __init__(self, name, primary, secondary, tertiatry):
        self.name = name
        self.color_primary = primary
        self.color_secondary = secondary
        self.color_tertiary = tertiatry

    def get_color(self, role):
        if role == 0:
            return self.color_primary
        if role == 1:
            return self.color_secondary
        return self.color_tertiary


class SubTheme:
    name = ''
    color_schemes = []
    icons = []
    figures = []

    def __init__(self, name, color_schemes, icons, figures):
        self.name = name
        self.color_schemes = color_schemes
        self.icons = icons
        self.figures = figures

    def get_color_scheme(self, index):
        index %= len(self.color_schemes)
        return self.color_schemes[index]

    def get_icon(self, index):
        index %= len(self.icons)
        return self.icons[index]

    def get_figure(self, index):
        index %= len(self.figures)
        return self.figures[index]


class Theme:
    name = ''
    subthemes = {}
    imagery = []
    materials = []
    mechanisms = []

    def __init__(self, name, subthemes, imagery, materials, mechanisms):
        self.name = name
        self.subthemes = subthemes
        self.materials = materials
        self.mechanisms = mechanisms
        self.imagery = imagery

    def get_imagery(self, index):
        index %= len(self.imagery)
        return self.imagery[index]

    def get_subtheme(self, index):
        subtheme_names = self.subthemes.keys()
        index %= len(subtheme_names)
        return subtheme_names[index]


class Primitive:
    name = ''
    node_north = False
    node_south = False
    node_east = False
    node_west = False
    node_top = False
    node_bottom = False

    scale_x = 0.0
    scale_y = 0.0
    scale_z = 0.0

    def __init__(self, name, x, y, z, north, east, south, west, top, bottom):
        self.name = name

        self.scale_x = x
        self.scale_y = y
        self.scale_z = z

        self.node_north = north
        self.node_south = east
        self.node_east = south
        self.node_west = west
        self.node_top = top
        self.node_bottom = bottom

    def get_anchors(self):
        anchors = []
        if self.node_north:
            anchors.append("north")
        if self.node_south:
            anchors.append("south")
        if self.node_east:
            anchors.append("east")
        if self.node_west:
            anchors.append("west")
        if self.node_top:
            anchors.append("top")
        if self.node_bottom:
            anchors.append("bottom")
        return anchors

    def get_bounds(self, scale=1):
        return self.scale_x*scale, self.scale_y*scale, self.scale_z*scale


class Mechanism:
    name = ''
    requires_any = []
    requires_all = []
    allows = []

    def __init__(self, name, req_any, req_all, allows):
        self.name = name
        self.requires_any = req_any
        self.requires_all = req_all
        self.allows = allows

    def is_functional(self, mechs_in):
        mechs = []
        for mech in mechs_in:
            mechs.append(mech.name)
        #print("Testing {} is functional...".format(self.name))
        for req in self.requires_all:
            if req not in mechs:
                #print("Not functional.  {} is missing.".format(req))
                return False
        if len(self.requires_any) < 1:
            return True
        for req in self.requires_any:
            if req in mechs:
                return True
        #print("Not functional.  Requires any of {} and has none. ({})".format(self.requires_any, mechs))
        return False

    def get_functional(self, mechs_in):
        mechs = []
        req_out = []
        for mech in mechs_in:
            mechs.append(mech.name)
        for req in self.requires_all:
            if req in mechs:
                req_out.append(req)
        for req in self.requires_any:
            if req in mechs:
                req_out.append(req)
        return req_out


class Ability:
    flavor_text = ''
    requirements = []
    behaviors = []

    def __init__(self, flavor, reqs, behaviors):
        self.flavor_text = flavor
        new_reqs = []
        for req in reqs:
            new_reqs.append(AbilityRequirement(req['all'], req['any'], req['caveats']))
        self.requirements = new_reqs
        self.behaviors = behaviors

    def meets_requirements(self, in_mechs, c_tree):
        print("Checking requirements for {}".format(self.flavor_text))
        acceptable = False
        acceptable_list = []
        for req in self.requirements:
            if req.is_acceptable(in_mechs, c_tree):
                acceptable = True
                acceptable_list = req.get_acceptable_components(in_mechs)
        if acceptable:
            return acceptable_list
        return None


class AbilityRequirement:
    req_all = []
    req_any = []
    caveats = []

    def __init__(self, req_all, req_any, caveats):
        self.req_all = req_all
        self.req_any = req_any
        self.caveats = []
        for caveat in caveats:
            self.caveats.append(Caveat(caveat['part'], caveat['statements']))

    def is_acceptable(self, in_mechs, c_tree):
        acceptable = False
        #print("In mechs: {}".format(in_mechs))
        for req in self.req_all:
            if req not in in_mechs:
                return False
        for req in self.req_any:
            if req in in_mechs:
                acceptable = True
        if len(self.req_any) < 1:
            acceptable = True
        if not acceptable:
            return False
        caveats_acceptable = True
        print("Evaluating caveats...")
        for caveat in self.caveats:
            print("Evaluating {}".format(caveat.statements))
            if not caveat.meets_statements(c_tree):
                caveats_acceptable = False
        if len(self.caveats) < 1:
            print("No caveats.")
            caveats_acceptable = True
        print("Acceptable: {}".format(acceptable and caveats_acceptable))
        return acceptable and caveats_acceptable

    def get_acceptable_components(self, in_mechs):
        optional_list = []
        for req in self.req_any:
            if req in in_mechs:
                optional_list.append(req)
        out_list = []
        for req in self.req_all:
            out_list.append(req)
        for req in optional_list:
            out_list.append(req)
        return out_list


class Caveat:
    part = None
    statements = []

    def __init__(self, part, statements):
        self.part = part
        self.statements = statements

    def meets_statements(self, c_tree):
        print("Getting candidates for '{}'...".format(self.part))
        part_candidates = self.get_candidates(c_tree, mechanism=self.part)
        print("Candidates: {}".format(part_candidates))
        meets_reqs = True
        for statement in self.statements:

            meets_statement = self.evaluate_statement(statement, part_candidates, c_tree)
            if not meets_statement:
                meets_reqs = False
        return meets_reqs

    def get_candidates(self, c_tree, mechanism=None, primitive=None):
        part_candidates = []
        if mechanism is None and primitive is None:
            print("ERROR: Candidate selection cannot be passed NO mechanism AND NO primitive.")
            return part_candidates
        if mechanism is not None and primitive is not None:
            print("ERROR: Candidate selection cannot be passed a mechanism AND a primitive.")
            return part_candidates
        nodes = c_tree.all_nodes()
        for node in nodes:
            if mechanism is not None and mechanism in node.data.mechanisms:
                part_candidates.append(node.identifier)
            if primitive is not None and primitive == node.data.primitive_shape.name:
                part_candidates.append(node.identifier)
        return part_candidates

    def evaluate_statement(self, statement_in, part_candidates, c_tree):
        statement = statement_in['statement']
        value = statement_in['value']

        if statement.startswith("child_of"):
            print("{} must be child of {}".format(self.part, value))
            if statement == "child_of_mech":
                print("Searching mechanisms for {}...".format(value))
                candidates = self.get_candidates(c_tree, mechanism=value)
            else:
                print("Searching primitives for {}...".format(value))
                candidates = self.get_candidates(c_tree, primitive=value)
            if len(candidates) < 1:
                print("Nothing found.".format(value))
                return False
            for candidate in candidates:
                cand_tree = c_tree.subtree(candidate)
                for part in part_candidates:
                    print("Trying '{} is child of {}'...".format(self.part, c_tree.get_node(candidate).data.name))
                    if cand_tree.contains(part) and part != candidate:
                        print("True.")
                        return True
                    else:
                        print("False.")
            print("{} cannot be child of {}.".format(self.part, value))
            return False
        return True



def get_ability_name(ability):
    if ability in abilities:
        return abilities[ability]
    else:
        return 'ERROR!'
