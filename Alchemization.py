from AlchemyObjects import Item


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
    anchors = itemA.get_open_anchors()

