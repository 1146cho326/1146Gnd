# led_blink_main.py

import sys
from pathlib import Path

from sys_keys_v001p0 import SysKeys as SysKey
from led_blink_keys import AppKeys as AppKey

from sys_json_read_v001p0 import sys_json_read
from sys_operating_v001p0 import main_loop

# json_path = Path(__file__).with_name("led_blink_1hz_with_json.json")
# json_path = Path(__file__).with_name("led_blinktest.json")
# json_path = Path(__file__).with_name("led_blinktest-work.json")
json_path = Path(__file__).with_name("led_blink_1146GndCode.json")

# -----
def main():

    times = None # default
    argv_len = len(sys.argv)
    if argv_len < 2:
        pass
    else:
        temp_str = sys.argv[1]
        if temp_str.isdecimal():
            temp_float = float(temp_str)
            times = int(temp_float)
    
    print(f"times:[{times}]")

    atom_table = sys_json_read(json_path)

    # start
    # JSON で初期化するようにした。
    #   {"addGrain.sys.clock_tick.idle_to_run_fg": 1},
    #
    # v old
    # # とりあえず決め打ち。正解が不明^^;;;(001p0_osd-led-blink-0p1hz)
    # start_atom_class = atom_table.get(AppKey.CLOCK_TICK)
    # start_atom_class.sys[SysKey.IDLE_TO_RUN_FG] = 1 # do idle to run

    # 繰り返し回数
    if times is not None:
        start_atom_class = atom_table.get(AppKey.CLOCK_TICK)
        start_atom_class.mem[AppKey.TIMES] = times

    main_loop(atom_table)

# -----

# Pythonのif __name__ == '__main__'の意味と使い方
# https://note.nkmk.me/python-if-name-main/#google_vignette

if __name__ == '__main__':
    main()
