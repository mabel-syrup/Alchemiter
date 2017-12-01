from AlchemyObjects import Item
from treelib import tree, node
from AlchemyGlobal import get_seed, get_one_from_list


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

def alchemizeAND(itemA, itemB):
    treeA = itemA.c_tree
    treeB = itemB.c_tree
    anchors = itemA.get_open_anchors()
    # New object's tree.
    treeC = tree.Tree(treeA, deep=True)
    itemC = Item("Temp_Name", None)
    itemC.c_tree = treeC
    comps = itemB.get_components()
    for comp in comps:
        seed = get_seed(comp)
        anchor_c = comp.get_an_anchor(seed)
        parent_comp = get_parent(anchors, seed)
        anchor_p = get_one_from_list(anchors[parent_comp])
        print("Anchors: Parent-{} Child-{}".format(anchor_p,anchor_c))

def get_parent(anchors, seed):
    comps = list(anchors.keys())
    index = seed % len(comps)
    return comps[index]

