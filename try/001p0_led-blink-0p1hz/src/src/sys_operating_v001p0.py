# sys_operating_v001p0.py

import time

from sys_keys_v001p0 import SysKeys as SysKey

# -----
class AtomBaseClass:

    def __init__(self, name, run_function, branch_list, sys_list, mem_list, scoop_list, drop_list):
        self.name = name
        self.mod_run_main = run_function
        self.branch_list = next(iter(branch_list))  # list <--- dict_value # 「list(d.items())[0]」と同じ
        self.sys = {}
        self.mem = {}
        self.scoop = {}
        self.drop = {}
        self.my_properties = {
            SysKey.SYS: self.sys,
            SysKey.MEM: self.mem,
            SysKey.SCOOP: self.scoop,
            SysKey.DROP: self.drop,
        }

        # propaty 生成 (初期値付きsys, 初期値付きmem)
        my_list = [sys_list, mem_list]
        key_address_type_str = [SysKey.SYS, SysKey.MEM]
        for i, wc_list in enumerate(my_list):
            for l in wc_list:
                for d in l:
                    addGrain_str, init_value = next(iter(d.items())) # 「list(d.items())[0]」と同じ
                    func_name_composition = addGrain_str.split(".")
                    if len(func_name_composition) < 4:
                        continue
                    # address_type = func_name_composition[1] # mem (or sys)
                    address_type = key_address_type_str[i]
                    key = f"{func_name_composition[3]}"
                    self.my_properties[address_type][key] = init_value
                pass
            pass
        pass

        # propaty 生成 (scoop, list)
        my_list = [scoop_list, drop_list]
        key_address_type_str = [SysKey.SCOOP, SysKey.DROP]
        for i, wc_list in enumerate(my_list):
            for l in wc_list:
                for addGrain_str in l:
                    func_name_composition = addGrain_str.split(".")
                    if len(func_name_composition) < 4:
                        continue
                    # x address_type = func_name_composition[1] # mem or sys
                    address_type = key_address_type_str[i]
                    if address_type == SysKey.DROP:
                        key = f"{func_name_composition[2]}.{func_name_composition[3]}" # 他のatomのmem参照するため
                    else:
                        key = f"{func_name_composition[3]}"
                    self.my_properties[address_type][key] = None
                pass
            pass
        pass

    def operating_main(self):
        my_state = self.my_properties[SysKey.SYS][SysKey.STATE]
        my_to_run_fg = self.my_properties[SysKey.SYS][SysKey.IDLE_TO_RUN_FG]
        if my_state == SysKey.ENUM_IDLE:
            if my_to_run_fg == 1:
                my_state = SysKey.ENUM_RUNNING
                self.my_properties[SysKey.SYS][SysKey.STATE] = my_state
                my_to_run_fg = 0
                self.my_properties[SysKey.SYS][SysKey.IDLE_TO_RUN_FG] = my_to_run_fg

        if my_state == SysKey.ENUM_RUNNING:
            # 処理
            temp_branch_table_num = self.run_main()

            self.my_properties[SysKey.SYS][SysKey.BRANCH_TABLE_NUM] = temp_branch_table_num
            if temp_branch_table_num is not None: # None(Don't care)は分岐しない

                my_state = SysKey.ENUM_BRANCHING
                self.my_properties[SysKey.SYS][SysKey.STATE] = my_state

        if my_state == SysKey.ENUM_BRANCHING:
            # 分岐 と 次の状態
            (temp_next_state, temp_branch_to_addAMB) = self.branch_main()

            self.my_properties[SysKey.SYS][SysKey.NEXT_STATE] = temp_next_state # "idle" or "run" or "delete"

            self.my_properties[SysKey.SYS][SysKey.BRANCH_TO_ADDAMB] = temp_branch_to_addAMB # Classの外側で他のclassのto_run_fgを立てる。
            temp_branch_table_num = None
            self.my_properties[SysKey.SYS][SysKey.BRANCH_TABLE_NUM] = temp_branch_table_num

            # あれ？なんか変だ^^;;; SysKey.NEXT_STATEを使ってない^^;;; (001p0_osd-led-blink-0p1hz)
            temp_next_state = self.my_properties[SysKey.SYS][SysKey.NEXT_STATE]
            if temp_next_state == SysKey.DELETE:
                my_state = SysKey.ENUM_DELETED
            elif temp_next_state == SysKey.RUN:
                my_state = SysKey.ENUM_RUNNING
            else: # temp_next_state == SysKey.IDLE
                my_state = SysKey.ENUM_IDLE
            self.my_properties[SysKey.SYS][SysKey.STATE] = my_state
            temp_next_state = ""
            self.my_properties[SysKey.SYS][SysKey.NEXT_STATE] = temp_next_state

    def init_main(self):
        pass

    def idle_main(self):
        pass

    def run_main(self):
        # 処理
        temp_branch_table_num = self.mod_run_main(self, self.name, self.my_properties)
        return temp_branch_table_num

    def branch_main(self):
        # 分岐
        # clear
        ret_next_state = "" # default
        ret_atom_name = "" # default

        # branch atom name
        temp_list = self.branch_list
        temp_num = self.my_properties[SysKey.SYS][SysKey.BRANCH_TABLE_NUM]
        if len(temp_list) > temp_num:
            ret_atom_name = temp_list[temp_num]

        # next state
        # とりあえず決め打ち。正解が不明^^;;;(001p0_osd-led-blink-0p1hz)
        # deleteは未対応なので返さないこと(001p0_osd-led-blink-0p1hz)
        if self.name == "clock_tick": # AppKey.CLOCK_TICK:
            ret_next_state = SysKey.RUN # 5000msecごとにrequestを出し続ける。
        else:
            ret_next_state = SysKey.IDLE # 5000msecごとにrequestを受けて動く。

        return (ret_next_state, ret_atom_name) # ex.("run", "addAMB.atom.blink_pattern.res")

    def delete_main(self):
        pass

    pass # class end



def main_loop(atom_table):
    # Lチカ の 3つのatom(clock_tick, blink_pattern, led_driver) の処理
    py_scoop_memory = {} # py_scoop_memory[atom_name][func_name]
    debug_first_loop_fg = True # やっつけでなおす。後で考える！ for dropの初期化。(001p0_osd-led-blink-0p1hz)
    while(True):
        for atom_name, atom_class in atom_table.items():


            # drop <--- scoop
            # drop: atom_class.drop[f"{scoop_atom_name}.{scoop_func_name}"] in other atom(name)
            # c.f. other: atom_class.other[f"{func_name}"] in own atom(name)
            for drop_atom_name_func_name in atom_class.drop.keys():
                temp_drop_atom_name_func_name_list = drop_atom_name_func_name.split(".")
                if len(temp_drop_atom_name_func_name_list) < 2:
                    pass
                else:
                    scoop_atom_name = temp_drop_atom_name_func_name_list[0]
                    scoop_func_name = temp_drop_atom_name_func_name_list[1]

                    scoop_to_dorop_value = None # default # getできなければ None
                    py_temp_dict = py_scoop_memory.get(scoop_atom_name)
                    if py_temp_dict is not None:
                        scoop_to_dorop_value = py_temp_dict.get(scoop_func_name) # getできなければ None
                    atom_class.drop[drop_atom_name_func_name] = scoop_to_dorop_value # getできなければ None

            pass


            # os or runtime or ... main() calling
            if debug_first_loop_fg: # やっつけでなおす。後で考える！ for dropの初期化。(001p0_osd-led-blink-0p1hz)
                # debug_first_loop_fg = False
                pass
            else:
                atom_class.operating_main()


            # scoop <--- mem(working memory)
            for func_name in atom_class.scoop.keys():
                value = atom_class.mem.get(func_name)
                if atom_name in py_scoop_memory:
                    py_scoop_memory[atom_name][func_name] = value
                else:
                    py_scoop_memory[atom_name] = {func_name: value}
            pass


            # branch (sys.branch_to_addAMB)
            temp_branch_to_addAMB = atom_class.sys[SysKey.BRANCH_TO_ADDAMB]
            func_name_composition = temp_branch_to_addAMB.split(".")
            if len(func_name_composition) < 4:
                pass
            else:
                branch_atom_name = f"{func_name_composition[2]}"
                temp_class = atom_table.get(branch_atom_name)
                if temp_class is not None:
                    temp_idle_to_run_fg = 1 # do idle to run
                    temp_class.sys[SysKey.IDLE_TO_RUN_FG] = temp_idle_to_run_fg
                # clear
                temp_branch_to_addAMB = ""
                atom_class.sys[SysKey.BRANCH_TO_ADDAMB] = temp_branch_to_addAMB


        pass # last line atom_table for-loop

        if debug_first_loop_fg: # やっつけでなおす。後で考える！ for dropの初期化。(001p0_osd-led-blink-0p1hz)
            debug_first_loop_fg = False # 一回forが回った。

        time.sleep(1) # 1000msec for kari(仮)(001p0_led-blink-0p1hz)

        # print(f"{atom_name}-----")
        # print(json.dumps(py_scoop_memory, indent=4)) # for debug

    pass # last line while loop forever
