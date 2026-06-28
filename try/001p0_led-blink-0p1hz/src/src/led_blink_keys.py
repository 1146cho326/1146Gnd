# led_blink_keys.py

class AppKeys:

    # -----
    # for LED enum
    ENUM_OFF = "off"
    ENUM_ON = "on"

    # -----
    # atoms name
    CLOCK_TICK = "clock_tick"
    BLINK_PATTERN = "blink_pattern"
    LED_DRIVER = "led_driver"

    # -----
    # working memory? func name?
    # -----
    # mem.clock_tick
    SPAN_MSEC = "span_msec"
    TIMES = "times"
    TIMES_CURRENT = "times_current"
    BLINK_TICK = "blink_tick"
    NEXT_WAKEUP_TIME_MS = "next_wakeup_time_ms"
    # -----
    # mem.blink_pattern
    BLINK_TICK_IS_USED = "blink_tick_is_used"
    LED_STATE = "led_state"
    REQUESTED_OUTPUT = "requested_output"
    # -----
    # mem.led_driver
    # requested_output = "requested_output" ---> blink_patternと同じ名前なのでコメントアウト
    APPLIED_OUTPUT = "applied_output"
