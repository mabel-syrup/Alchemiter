import json
from AlchemyTypes import Mechanism, Primitive, Ability
from AlchemyObjects import Item
from AlchemyGlobal import items, components, mechanisms, primitives, abilities


def load():
    items_json = load_items()
    components_json = load_components()
    #mech_json = load_mechanisms()
    primitives_json = load_primitives()
    abilities_json = load_abilities()
    # Load Mechanisms
    #mech_names = mech_json.keys()
    #for mech_name in mech_names:
    #    json_mech = mech_json[mech_name]
    #    mechanisms[mech_name] = \
    #        Mechanism(mech_name, json_mech['requires_any'], json_mech['requires_all'], json_mech['allows'])
    # Load Primitives
    prim_names = primitives_json.keys()
    for prim_name in prim_names:
        json_prim = primitives_json[prim_name]
        primitives[prim_name] = \
            Primitive(prim_name, json_prim['x'], json_prim['y'], json_prim['z'], json_prim['north'], json_prim['east'], json_prim['south'], json_prim['west'], json_prim['top'], json_prim['bottom'])
    # Load Abilities
    ability_names = abilities_json.keys()
    for ability_name in ability_names:
        json_ability = abilities_json[ability_name]
        abilities[ability_name] = Ability(json_ability['flavor'], json_ability['requirements'], json_ability['behaviors'])
    # Load Items
    item_names = items_json.keys()
    for item_name in item_names:
        print("Loading {}...".format(item_name))
        json_item = items_json[item_name]
        item = Item(item_name, None)
        tree = json_item['tree']
        component_dict = recursive_component_search([tree], 'Root')
        ids = component_dict.keys()
        for cid in ids:
            print('Processing component "{}" of "{}"'.format(cid, item_name))
            comp_json = components_json[cid]
            parent_ID = component_dict[cid][0]
            parent_name = None
            if parent_ID != "Root":
                parent_name = components_json[parent_ID]['name']
            parent_id = item.get_id_from_name(parent_name)
            print("Adding component '{}' to '{}' (id:{})...".format(comp_json['name'], parent_name, parent_id))
            attachment_data = component_dict[cid][1]
            json_prim = comp_json['primitive']
            primitive = primitives[json_prim]
            item.add_component(
                comp_json['name'], cid, parent_id, attachment_data[0], attachment_data[1], comp_json['mechanisms'], primitive)
        items.append(item)


def recursive_component_search(tree, parent):
    comp_dict = {}

    for comp_bracket in tree:
        comp_id = list(comp_bracket.keys())[0]
        print('Processing {}...'.format(comp_id))
        comp_dict[comp_id] = [parent, comp_bracket[comp_id]['data']]
        if 'children' in comp_bracket[comp_id] and len(comp_bracket[comp_id]['children']) > 0:
            comp_dict.update(recursive_component_search(comp_bracket[comp_id]['children'], comp_id))
    return comp_dict


def load_items():
    with open("items.json") as items_json:
        json_items = json.load(items_json)
        return json_items


def load_components():
    with open("components.json") as components_json:
        json_components = json.load(components_json)
        return json_components


def load_mechanisms():
    with open("mechanisms.json") as mechanisms_json:
        json_mechanisms = json.load(mechanisms_json)
        return json_mechanisms


def load_primitives():
    with open("primitives.json") as primitives_json:
        json_primitives = json.load(primitives_json)
        return json_primitives


def load_abilities():
    with open("abilities.json") as abilities_json:
        json_abilities = json.load(abilities_json)
        return json_abilities


def load_themes():
    with open("themes.json") as themes_json:
        json_themes = json.load(themes_json)
        return json_themes


def load_colorschemes():
    with open("colorschemes.json") as colorschemes_json:
        json_colorschemes= json.load(colorschemes_json)
        return json_colorschemes