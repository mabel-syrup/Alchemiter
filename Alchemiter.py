import AlchemyObjects
import AlchemyTypes
from AlchemyGlobal import items, components
from Loader import load


def main():
    load()
    for item in items:
        print(item.get_construct())
        print(item.get_ability_set())
    items[0].get_save_json()
    item_name = input('Item Name?\n>')
    item = AlchemyObjects.Item(item_name, None)
    done = False
    while not done:
        name = input('Part Name?\n>')
        if name == 'done':
            done = True
            continue
        if item.has_root():
            parent = input('Attached to?\n>')
            parent_id = item.get_id_from_name(parent)
            if parent_id is not None:
                item.add_component(name, parent_id, 'DEBUG', 'DEBUG', [])
            else:
                continue
        else:
            item.add_component(name, None, 'DEBUG', 'DEBUG', [])
    print(item.get_component_info_list())

main()
