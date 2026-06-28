# sys_json_read_v001p0.py

import json

from sys_keys_v001p0 import SysKeys as SysKey
from sys_operating_v001p0 import AtomBaseClass

from led_blink_modules import modules_addGrain_mod_dict as addGrain_mod_dict


def sys_json_read(json_path):
    # read .json and make dict
    atom_table = {}

    with json_path.open(encoding="utf-8") as f:
        dd = json.load(f)

    d = dd.get(SysKey.JSON_1146GND_CODE)
    for temp_key, atoms in d.items():
        atom_dict = {}
        for addAMB_atom_wc_res, atom_value_list in atoms.items():
            for i, atom_molecule_composition_dict in enumerate(atom_value_list):
                key = SysKey.ATOM_MOLECULE_COMPOSITION_NAMES_LIST[i]
                value = atom_molecule_composition_dict.get(key)
                if value is not None:
                    atom_dict[key] = value
            pass

            addAMB_atom_wc_res_list = addAMB_atom_wc_res.split(".")
            atom_name = addAMB_atom_wc_res_list[2]

            run_function_str = atom_dict.get(SysKey.RUN) # ex."addGrain.mod.clock_tick.run"
            run_function = addGrain_mod_dict.get(run_function_str)

            branch_list = atom_dict.get(SysKey.BRANCH).values()

            sys_list = atom_dict.get(SysKey.SYS).values()
            mem_list = atom_dict.get(SysKey.MEM).values()
            scoop_list = atom_dict.get(SysKey.SCOOP).values()
            drop_list = atom_dict.get(SysKey.DROP).values()

            atom_table[atom_name] = AtomBaseClass(
                atom_name, 
                run_function, 
                branch_list,
                sys_list, 
                mem_list, 
                scoop_list, 
                drop_list
            )
        pass
    pass

    # v debug
    for atom_name, atom_class in atom_table.items():
        # drop <--- scoop
        # drop: atom_class.drop[f"{scoop_atom_name}.{scoop_func_name}"] in other atom(name)
        # c.f. other: atom_class.other[f"{func_name}"] in own atom(name)
        for drop_atom_name_func_name in atom_class.drop.keys():
            print(f"[{atom_name}]:drop_atom_name_func_name:[{drop_atom_name_func_name}]")
        pass
    pass
    print(f"start!")
    # ^ debug

    return atom_table
