# led_blink_modules.py

from datetime import datetime, timezone

from sys_keys_v001p0 import SysKeys as SysKey
from led_blink_keys import AppKeys as AppKey

# -----
# for addGrain.mod

def clock_tick_run_main(proc, atom_name, my_properties):

    ret_branch_table_num = None # default # None(Don't care)は分岐しない
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)

    temp_drop_val = my_properties[SysKey.DROP]["blink_pattern.blink_tick_is_used"]
    if temp_drop_val != 0:
        my_properties[SysKey.MEM][AppKey.BLINK_TICK] = 0
        # # いらないはず...一応clear
        # temp_drop_val = 0
        # my_properties[AppKey.DROP]["blink_pattern.blink_tick_is_used"] = temp_drop_val

    if my_properties[SysKey.MEM][AppKey.BLINK_TICK] != 0: # すでに500msec経ってるけど、外部で未処理なので、何もしない。
        pass # ---> return
    else:
        wakeup_ms = my_properties[SysKey.MEM][AppKey.NEXT_WAKEUP_TIME_MS]
        MY_SPAN_MSEC = my_properties[SysKey.MEM][AppKey.SPAN_MSEC]
        if now_ms >= wakeup_ms:
            my_properties[SysKey.MEM][AppKey.BLINK_TICK] = 1 # request
            if ((now_ms - wakeup_ms) >= MY_SPAN_MSEC * 10): # 10回以上更新がなかったか？
                my_properties[SysKey.MEM][AppKey.NEXT_WAKEUP_TIME_MS] = now_ms + MY_SPAN_MSEC # may be wakeup_ms == 0 true
            else:
                my_properties[SysKey.MEM][AppKey.NEXT_WAKEUP_TIME_MS] = wakeup_ms + MY_SPAN_MSEC # 次は5sec後

            TEMP_TIMES = my_properties[SysKey.MEM][AppKey.TIMES]
            temp_times_current = my_properties[SysKey.MEM][AppKey.TIMES_CURRENT]
            if temp_times_current >= TEMP_TIMES:
                ret_branch_table_num = None # 分岐! は、無しよ。

                print(f'type "control + c" debug:times:{temp_times_current}')
            else:
                ret_branch_table_num = 1 # 分岐! 現在飛び先テーブルは一箇所なので、1を直書き。

                print(f'debug:times:{temp_times_current}')
                temp_times_current += 1
                my_properties[SysKey.MEM][AppKey.TIMES_CURRENT] = temp_times_current

    
    print(f"debug:difference:{now_ms - wakeup_ms}msec") # for debug

    return ret_branch_table_num


def blink_pattern_run_main(proc, atom_name, my_properties):

    ret_branch_table_num = None # default # None(Don't care)は分岐しない

    temp_drop_val = my_properties[SysKey.DROP]["clock_tick.blink_tick"]
    if temp_drop_val == 0:
        # not use!
        my_properties[SysKey.MEM][AppKey.BLINK_TICK_IS_USED] = 0

    else:
        # used!
        my_properties[SysKey.MEM][AppKey.BLINK_TICK_IS_USED] = 1

        # toggle
        if my_properties[SysKey.MEM][AppKey.LED_STATE] == AppKey.ENUM_OFF:
            my_properties[SysKey.MEM][AppKey.LED_STATE] = AppKey.ENUM_ON
        else:
            my_properties[SysKey.MEM][AppKey.LED_STATE] = AppKey.ENUM_OFF

        # set request
        my_properties[SysKey.MEM][AppKey.REQUESTED_OUTPUT] \
        = my_properties[SysKey.MEM][AppKey.LED_STATE]

    ret_branch_table_num = 1 # 分岐! 現在飛び先テーブルは一箇所なので、1を直書き。
    return ret_branch_table_num


def led_driver_run_main(proc, atom_name, my_properties):

    ret_branch_table_num = None # default # None(Don't care)は分岐しない

    temp_drop_val = my_properties[SysKey.DROP]["blink_pattern.requested_output"]

    # do display output
    if temp_drop_val == AppKey.ENUM_OFF:
        LED_str = "OFF"
    else:
        LED_str = "ON"
    print(f"[{AppKey.LED_DRIVER}:LED={LED_str}]")

    ret_branch_table_num = 1 # 分岐! 現在飛び先テーブルは一箇所なので、1を直書き。
    return ret_branch_table_num


def wc_wc_dummy():
    pass


# module-s name
# ここ(defの後)に移動。
key_addGrain_mod_clock_tick_run = "addGrain.mod.clock_tick.run"
key_addGrain_mod_blink_pattern_run = "addGrain.mod.blink_pattern.run"
key_addGrain_mod_led_driver_run = "addGrain.mod.led_driver.run"
key_addGrain_mod_wc_dummy = "addGrain.mod.wc.dummy"
modules_addGrain_mod_dict = {
    key_addGrain_mod_clock_tick_run: clock_tick_run_main,
    key_addGrain_mod_blink_pattern_run: blink_pattern_run_main,
    key_addGrain_mod_led_driver_run: led_driver_run_main,
    key_addGrain_mod_wc_dummy: wc_wc_dummy,
}
