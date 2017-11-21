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

    def __init__(self, name, north, east, south, west, top, bottom):
        self.name = name
        self.node_north = north
        self.node_south = east
        self.node_east = south
        self.node_west = west
        self.node_top = top
        self.node_bottom = bottom


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

    def meets_requirements(self, in_mechs):
        acceptable = False
        acceptable_list = []
        for req in self.requirements:
            if req.is_acceptable(in_mechs):
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
        self.caveats = caveats

    def is_acceptable(self, in_mechs):
        acceptable = False
        for req in self.req_all:
            if req not in in_mechs:
                return False
        for req in self.req_any:
            if req in in_mechs:
                acceptable = True
        # TODO: Implement Caveats
        return acceptable

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


def get_ability_name(ability):
    if ability in abilities:
        return abilities[ability]
    else:
        return 'ERROR!'
