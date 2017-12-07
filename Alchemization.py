from AlchemyObjects import Item, Component
from treelib import tree, node
from AlchemyGlobal import get_seed, get_one_from_list, get_item_from_name


# Combination steps &&:
# "Functional Combination"
# 1) Get open anchor points
# 2) Get all functions and their requirements
# 3) Attach components preserving functions

# Combination steps ||:
# Aesthetic Combination
# 1) Get open anchor points
# 2) Get icons and figures
# 3) If the object has none, add a few to the anchor points
# 4) Theme the object with the second object

def alchemize(name_a, name_b):
    item_a = get_item_from_name(name_a)
    item_b = get_item_from_name(name_b)
    if item_a is None or item_b is None:
        return None
    return alchemizeAND(item_a, item_b)


def alchemizeAND(itemA, itemB):
    treeA = itemA.c_tree
    treeB = itemB.c_tree
    anchors = itemA.get_open_anchors()
    # New object's tree.
    treeC = tree.Tree(treeA, deep=True)
    itemC = Item("Temp_Name", None)
    itemC.c_tree = treeC
    nodes_b = treeB.all_nodes()
    nodes_b = merge_from_primitive_overlap(itemC, treeC, nodes_b)
    nodes_b = merge_from_mechanism_overlap(itemC, treeC, nodes_b)
    comps = []
    for node_b in nodes_b:
        comps.append(node_b.data)
    for comp in comps:
        seed = get_seed(comp.get_seed_data())
        anchor_c = comp.get_an_anchor(seed)
        parent_id = get_parent(anchors, seed)
        anchor_p = get_one_from_list(anchors[parent_id])
        itemC.add_component(comp.name, comp.file_id, parent_id, anchor_p,
                            anchor_c, comp.mechanisms, comp.primitive_shape)
        anchors.clear()
        anchors = itemC.get_open_anchors()
    print(itemC.get_construct())
    print(itemC.get_ability_set())
    return itemC

        #print("Anchors: Parent-{} Child-{} Seed-{}".format(anchor_p, anchor_c, seed))


def merge_from_mechanism_overlap(item, tree_a, nodes_b):
    print("Merging mechanisms...")
    mech_duplicates = get_mechanism_duplicates(tree_a, nodes_b)
    print("-Found {} obsolete components.\n-Merging...".format(len(mech_duplicates)))
    deletion = merge_components(item, mech_duplicates)
    print("-Removing {} dead components...".format(len(deletion)))
    out_comps = remove_flagged(nodes_b, deletion)
    return out_comps


def merge_from_primitive_overlap(item, tree_a, nodes_b):
    print("Merging primitives...")
    primitive_duplicates = get_primitive_duplicates(tree_a, nodes_b)
    print("-Found {} identical primitives.\n-Merging...".format(len(primitive_duplicates)))
    deletion = merge_components(item, primitive_duplicates)
    print("-Removing {} dead components...".format(len(deletion)))
    out_comps = remove_flagged(nodes_b, deletion)
    return out_comps


def remove_flagged(in_comps, flags):
    out_comps = []
    print("Deletion: {}".format(flags))
    for node in in_comps:
        print("Checking flags for {}...".format(node.data.file_id))
        if node.data.file_id not in flags:
            print("Not flagged.")
            out_comps.append(node)
        else:
            print("{} flagged for deletion.  Removing...".format(node.data.name))
    print("List after deletion: {}".format(out_comps))
    return out_comps


def get_parent(anchors, seed):
    comps = list(anchors.keys())
    index = seed % len(comps)
    return comps[index]


def merge_components(item, duplicates):
    c_tree = item.c_tree
    duplicates_in_tree = list(duplicates.keys())
    marked_for_deletion = []
    for duplicate in duplicates_in_tree:
        node_a = c_tree.get_node(duplicate)
        node_b = duplicates[duplicate]
        print("Merging {} and {}...".format(node_a.data.name, node_b.data.name))
        #TODO: Prioritize components whose primitive is required
        comp_c_data, dead = merge_duplicate(node_a, node_b)
        marked_for_deletion.append(node_b.data.file_id)
        item.replace_component(
            comp_c_data['name'],
            comp_c_data['id'],
            duplicate,
            comp_c_data['mechanisms'],
            comp_c_data['primitive']
        )
    return marked_for_deletion


def get_mechanism_duplicates(treeA, compsB):
    duplicates = {}
    compsA = treeA.all_nodes()
    for comp in compsB:
        mechs = comp.data.mechanisms
        if len(mechs) < 1:
            continue
        for comp_a in compsA:
            duplicate = True
            mechs_a = comp_a.data.mechanisms
            for mech in mechs:
                #print("Checking for obsolescence: {} -> {}".format(comp.data.name, comp_a.data.name))
                if mech not in mechs_a:
                    #print("Not found: {} ({} -> {})".format(mech, comp.data.name, comp_a.data.name))
                    duplicate = False
            if duplicate:
                print("Obsolescence: {} -> {}".format(comp.data.name, comp_a.data.name))
                duplicates[comp_a.identifier] = comp
    return duplicates


def get_primitive_duplicates(tree_a, comps_b):
    duplicates = {}
    comps_a = tree_a.all_nodes()
    for comp in comps_b:
        primitive = comp.data.primitive_shape.name
        for comp_a in comps_a:
            #print("Checking primitive: {} -> {} ({})...".format(comp.data.name, comp_a.data.name, primitive))
            if comp_a.data.primitive_shape.name == primitive:
                print("Identical primitive: {} ({} -> {})".format(primitive, comp.data.name, comp_a.data.name))
                duplicates[comp_a.identifier] = comp
    return duplicates


def merge_duplicate(node_a, node_b):
    component_a = node_a.data
    component_b = node_b.data
    seed = get_seed("{}{}".format(component_a.name, component_b.name))
    keep_a = seed % 12 < 7
    merged_mechs = []
    for mech in component_a.mechanisms:
        if mech not in merged_mechs:
            merged_mechs.append(mech)
    for mech in component_b.mechanisms:
        if mech not in merged_mechs:
            merged_mechs.append(mech)
    return_data = {}
    if keep_a:
        name = component_a.name
        comp_id = name + node_a.identifier
        primitive = component_a.primitive_shape
        dead = component_b.file_id
        print("Flagging {} for death...".format(component_b.name))
    else:
        name = component_b.name
        comp_id = name + node_b.identifier
        primitive = component_b.primitive_shape
        dead = component_a.file_id
        print("Flagging {} for death...".format(component_a.name))
    return_data['name'] = name
    return_data['id'] = comp_id
    return_data['primitive'] = primitive
    return_data['mechanisms'] = merged_mechs
    return return_data, dead
