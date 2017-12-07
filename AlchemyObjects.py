from treelib import tree, node, Tree, Node
from AlchemyTypes import mechanisms, Mechanism, get_ability_name
from AlchemyGlobal import abilities
from json import loads, dumps


ASYMMETRICAL = 0
TWO_WAY_SYMMETRY = 1
FOUR_WAY_SYMMETRY = 2


class Component:
    name = ''
    file_id = ''
    color_scheme_assignment = 0
    material = None
    primitive_shape = None
    mechanisms = []
    properties = []
    anchor_to_parent_p = None
    anchor_to_parent_c = None
    ID = None

    item = None

    # From Above
    image_TNW = None
    image_TNE = None
    image_TSW = None
    image_TSE = None
    # From Below
    image_BNW = None
    image_BNE = None
    image_BSW = None
    image_BSE = None

    def __init__(self, item, component_id, name, file_id, image_path, mode):
        # TODO: Incorporate images
        self.item = item
        self.file_id = file_id
        self.name = name
        self.ID = component_id

    def get_seed_data(self):
        return "{}{}{}".format(self.mechanisms, self.item.name, self.name)

    def get_anchors(self):
        anchor_list = self.primitive_shape.get_anchors()
        if self.anchor_to_parent_c in anchor_list:
            anchor_list.remove(self.anchor_to_parent_c)
        return anchor_list

    def set_material(self, material):
        self.material = material

    def set_primitive(self, primitive):
        self.primitive_shape = primitive

    def set_anchor_points(self, anchor_p, anchor_c):
        self.anchor_to_parent_p = anchor_p
        self.anchor_to_parent_c = anchor_c

    def set_orientation(self, anchor):
        self.anchor_to_parent_c = anchor

    def get_anchor_data(self):
        return [self.anchor_to_parent_p, self.anchor_to_parent_c]

    def set_mechanisms(self, mechs):
        self.mechanisms = mechs

    def add_mechanism(self, mech):
        self.mechanisms.append(mech)

    def combine_mechanisms(self, mechs):
        for mech in mechs:
            self.mechanisms.append(mech)

    def get_mechanisms(self):
        return self.mechanisms

    def get_an_anchor(self, seed, available=None):
        if available is None:
            available = self.get_anchors()
        anchors = self.get_anchors()
        anchor_c = self.anchor_to_parent_c
        if anchor_c not in anchors:
            anchors.append(anchor_c)
        for anchor in available:
            if anchor in self.get_anchors():
                anchors.append(anchor)
        index = seed % len(anchors)
        print("Anchor index is {}".format(index))
        return anchors[index]


class Item:
    name = ''
    color_scheme = None
    theme = None
    c_tree = None

    def __init__(self, name, theme):
        self.name = name
        self.theme = theme
        self.c_tree = Tree()

    def get_component_info_list(self):
        out_string = ''
        components = self.c_tree.all_nodes()
        for c in components:
            parent = self.get_parent(c.identifier)
            if parent is None:
                out_string += '{} is the root object\n'.format(c.data.name)
            else:
                out_string += 'the {} of the {} is attached to the {} of the {}\n'\
                    .format(c.data.anchor_to_parent_c, c.data.name, c.data.anchor_to_parent_p, parent.data.name)
        return out_string

    def get_a_component(self, seed):
        components = self.c_tree.all_nodes()
        index = seed % len(components)
        return components[seed].identifier

    def get_components(self):
        out_comps = []
        nodes = self.c_tree.all_nodes()
        for node in nodes:
            out_comps.append(node.data)
        return out_comps

    def get_construct(self, has_name=True):
        outstring = ''
        this_tree = self.c_tree
        root = this_tree.get_node(this_tree.root)
        if has_name:
            outstring += "The {} ".format(self.name)
        else:
            outstring += "This object "
        outstring += "is a {}".format(root.tag)
        if not root.is_leaf():
            child_list = self.get_child_list(root.identifier)
            outstring += " with {}".format(get_oxford_comma(child_list))
            children = this_tree.children(root.identifier)
            for child in children:
                outstring += "\n{}".format(self.loop_construct(child.identifier, root.tag))
        return outstring

    def get_open_anchors(self):
        print("Getting open anchor points for {}...".format(self.name))
        anchor_dict = {}
        c_tree = self.c_tree
        component_nodes = c_tree.all_nodes()
        for node in component_nodes:
            comp = node.data
            anchors = comp.get_anchors()
            comp_children = c_tree.children(node.identifier)
            for child in comp_children:
                anchor = child.data.anchor_to_parent_p
                if anchor in anchors:
                    anchors.remove(anchor)
            if len(anchors) < 1:
                continue
            anchor_dict[node.identifier] = anchors
            print(str(anchors))
        return anchor_dict


    def get_child_list(self, nid):
        children = self.c_tree.children(nid)
        child_list = []
        for child in children:
            child_list.append("a {}".format(child.tag))
        return child_list

    def loop_construct(self, nid, parent_name):
        this_tree = self.c_tree
        #print("Looking for node of id {}...".format(nid))
        this_node = this_tree.get_node(nid)
        #print("Node retrieved: {}".format(this_node is not None))
        #if this_node is not None:
            #print("Node is of component '{}', child of '{}'".format(this_node.tag, parent_name))
        #print("Accessing data of Node ({})...".format(type(this_node)))
        comp = this_node.data
        #print("Data is of type {}".format(type(comp)))
        outstring = "The {} is on the {} of the {}".format(comp.name, comp.anchor_to_parent_p, parent_name)
        child_list = self.get_child_list(nid)
        #print("Children: {} ({})".format(str(child_list), type(child_list)))
        if len(child_list) > 0:
            child_string = get_oxford_comma(child_list)
            outstring += ", with {}".format(child_string)
            children = this_tree.children(nid)
            for child in children:
                outstring += "\n{}".format(self.loop_construct(child.identifier, comp.name))
        return outstring

    def has_root(self):
        return len(self.c_tree.nodes) > 0

    def get_id_from_name(self, name):
        components = self.c_tree.all_nodes()
        for c in components:
            if c.tag == name:
                return c.identifier
        return None

    def is_root(self, node_id):
        component_node = self.c_tree.get_node(node_id)
        return component_node.is_root()

    def get_parent(self, node_id):
        return self.c_tree.parent(node_id)

    def get_parent_id(self, node_id):
        parent_node = self.c_tree.parent(node_id)
        return parent_node.identifier

    def replace_component(self, name, file_id, node_id, comp_mechanisms, primitive, image_path=None, mode=None):
        this_node = self.c_tree.get_node(node_id)
        this_node.tag = name
        anchor_c = this_node.data.anchor_to_parent_c
        anchor_p = this_node.data.anchor_to_parent_p
        component = Component(self, node_id, name, file_id, image_path, mode)
        component.set_anchor_points(anchor_c, anchor_p)
        component.set_mechanisms(comp_mechanisms)
        component.set_primitive(primitive)
        this_node.data = component

    def add_component(self, name, file_id, parent_id, anchor_p, anchor_c, comp_mechanisms, primitive, image_path=None, mode=None):
        this_node = Node(name)
        component = Component(self, this_node.identifier, name, file_id, image_path, mode)
        component.set_anchor_points(anchor_p, anchor_c)
        component.set_mechanisms(comp_mechanisms)
        component.set_primitive(primitive)
        this_node.data = component
        if parent_id is not None:
            parent = self.c_tree.get_node(parent_id)
            self.c_tree.add_node(this_node, parent)
        else:
            self.c_tree.add_node(this_node)

    def get_abilities(self):
        print("Getting abilities for {}".format(self.name))
        mechs = self.get_mechanism_list()
        this_abilities = {}
        ability_names = list(abilities.keys())
        for ability_name in ability_names:
            ability = abilities[ability_name]
            acceptable = ability.meets_requirements(mechs, self.c_tree)
            if acceptable is not None:
                comp_list = []
                for mech in acceptable:
                    comp = self.get_component_with_mechanism(mech)
                    if comp is not None:
                        comp_list.append(comp)
                this_abilities[ability_name] = [ability.flavor_text, comp_list]
        return this_abilities

    def get_mechanism_list(self):
        component_nodes = self.c_tree.all_nodes()
        mechs = []
        for c_node in component_nodes:
            c = c_node.data
            for mech in c.get_mechanisms():
                mechs.append(mech)
        return mechs

    def get_ability_set(self, has_name=True):
        readout = ""
        this_abilities = self.get_abilities()
        if len(this_abilities) < 1:
            return "\n\n"
        ability_names = list(this_abilities.keys())
        ability_flavors = []
        for ability_name in ability_names:
            ability = this_abilities[ability_name]
            ability_flavors.append(ability[0])
        if has_name:
            readout += "The {} ".format(self.name)
        else:
            readout += "This object "
        readout += "can be used to {}\n\n".format(get_oxford_comma(ability_flavors))
        return readout

    #def get_abilities(self):
    #    mechs = self.get_mechanism_list()
    #    abilities = []
    #    for mech in mechs:
    #        if mech.is_functional(mechs):
    #            for ability in mech.allows:
    #                if not ability in abilities:
    #                    abilities.append(ability)
    #    return abilities

    #def get_ability_set(self):
    #    outstring = ''
    #    mechs = self.get_mechanism_list()
    #    for mech in mechs:
    #        reqs = mech.get_functional(mechs)
    #        req_comps = []
    #        for req in reqs:
    #            comp = self.get_component_with_mechanism(req)
    #            if comp not in req_comps:
    #                req_comps.append(comp)
    #        me = self.get_component_with_mechanism(mech.name)
    #        if me not in req_comps:
    #            req_comps.append(self.get_component_with_mechanism(mech.name))
    #        if mech.is_functional(mechs):
    #            abilities = mech.allows
    #            if len(abilities) > 0:
    #                ability_names = []
    #                for ability in abilities:
    #                    ability_names.append(get_ability_name(ability))
    #                outstring += "The {} can be used to {}\n"\
    #                    .format(get_oxford_comma(req_comps), get_oxford_comma(ability_names))
    #            else:
    #                outstring += "The {} act{} as a functioning {}\n"\
    #                    .format(get_oxford_comma(req_comps), singular_s(req_comps), mech.name)
    #        else:
    #            outstring += "The {} act{} as a nonfunctional {}\n"\
    #                .format(get_oxford_comma(req_comps), singular_s(req_comps), mech.name)
    #    return outstring

    def get_component_with_mechanism(self, mechanism):
        component_nodes = self.c_tree.all_nodes()
        for c_node in component_nodes:
            c = c_node.data
            if mechanism in c.get_mechanisms():
                return c.name
        return None

    def get_save_json(self):
        out_json = {}
        out_json['color scheme'] = self.color_scheme
        out_json['theme'] = self.theme
        out_json['tree'] = self.to_json()
        print('Tree is type {}'.format(type(out_json['tree'])))
        print('"{}": {}'.format(self.name, dumps(out_json)))

    def to_json(self):
        json_tree = tree.Tree(self.c_tree, deep=True)
        json_nodes = json_tree.all_nodes()
        for node in json_nodes:
            node.tag = node.data.file_id
            attach_info = node.data.get_anchor_data()
            node.data = attach_info
        tree_json = json_tree.to_json(with_data=True)
        tree_json_obj = loads(tree_json, encoding='ASCII')
        return tree_json_obj



def get_oxford_comma(in_list):
    outstring = ''
    length = len(in_list)
    for index in range(length):
        outstring += str(in_list[index])
        if index == length - 1:
            return outstring
        if index == length - 2:
            if length < 3:
                outstring += " and "
            else:
                outstring += ", and "
        elif length > 2:
            outstring += ", "
    return outstring


def plural_s(in_list):
    if len(in_list) > 1:
        return 's'
    else:
        return ''


def singular_s(in_list):
    if len(in_list) > 1:
        return ''
    else:
        return 's'
