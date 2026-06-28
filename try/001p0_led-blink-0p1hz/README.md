# 001p0 OSD LED blink 0.1Hz

## 概要

5秒ごとに "LED ON" / "LED OFF" をトグルで表示するプログラム(Lチカ)である。

- 1146GndCode の思考実験である
- 1146GndCode(JSON + (Python-module))でLチカを書き表した。
- 1146GndCode(JSON + (Python-module))を処理するPythonコードを書いた。

## 実行方法

- try/001p0_led-blink-0p1hz/src/src/ へ移動。
- python3 led_blink_main.py (デフォルトの10回トグル表示を指定する) もしくは、
- python3 led_blink_main.py 20 (20回トグル表示を指定する)

## 終了方法

- control + cキー で強制停止する。

## 期待する出力

```text:console
% python3 led_blink_main.py
times:[None]
[clock_tick]:drop_atom_name_func_name:[blink_pattern.tick_500ms_is_used]
[blink_pattern]:drop_atom_name_func_name:[clock_tick.tick_500ms]
[led_driver]:drop_atom_name_func_name:[blink_pattern.requested_output]
start!
debug:times:0
debug:difference:1782608819130msec
[led_driver:LED=ON]
debug:difference:-3994msec
debug:difference:-2991msec
debug:difference:-1986msec
debug:difference:-981msec
debug:times:1
debug:difference:24msec
[led_driver:LED=OFF]
debug:difference:-3970msec
...
debug:difference:-814msec
debug:times:9
debug:difference:192msec
[led_driver:LED=OFF]
debug:difference:-3805msec
debug:difference:-2804msec
debug:difference:-1799msec
debug:difference:-797msec
type "control + c" debug:times:10
debug:difference:208msec
debug:difference:-3789msec
debug:difference:-2783msec
...
```

## Lチカ 各ファイルの役割

### led_blink_main.py

- 実行用のPython。
- 各種？pythonファイルを呼び出している。
- 中身はスカスカ

### led_blink_modules.py

- 各 atom の run で呼び出される Python-module。
- Grain の一つ。

### led_blink_keys.py

- Lチカ用のJSONを読むのに使用する文字列。
- class AppKeys:

### led_blink_1146GndCode.json

- Lチカ用のJSONファイル。
- 1146GndCode で Lチカを表した JSON のコード

### sys_operating_v001p0.py

- ここで無限ループし、各 atom のクラスを順番に呼び出す。
- class AtomBaseClass: も、ここに定義している。

### sys_json_read_v001p0.py

- Lチカの JSONファイルを読み込む。
- atom_table[atom_name] が 各atom の インスタンス。

### sys_keys_v001p0.py

- Lチカアプリ以外でも必要な文字列を集めた。
- class SysKeys:

### led_blink_memory_map.txt

- FPGA を想定した、アドレスマップ的なものを作った。
- toolを使わず手書きした。
- system memory と working memory の初期化テーブルについては検討中。
- toolでの自動生成は今後の課題とする。

## JSONの構造

人間が読みやすいように、atom の記述内に table を直書きしている。

- clock_tick(atom)
- blink_pattern(atom)
- led_driver(atom)

```JSON:led_blink_1146GndCode.json
{    
  "JSON_1146Gnd_Code": { <--- このkeyの中に書く
    "addAMB_atom_wc_res_table": { <--- dummy

      "addAMB.atom.clock_tick.res": [ <--- clock_tick 先頭
        {"header_reserved": "header_reserved"},
        {"operating": "addGrain.mod.wc.dummy"},
        {"init": "addGrain.mod.wc.dummy"},
        {"idle": "addGrain.mod.wc.dummy"},

        {"run": "addGrain.mod.clock_tick.run"}, <--- python-module
        {"branch": {"addBranch.branch.clock_tick.res": [ <--- 分岐テーブル
          "header_reserved",
          "addAMB.atom.blink_pattern.res" <--- Lチカ clock_tick は一箇所
          ]}},

        {"delete": "addGrain.mod.wc.dummy"},

        {"sys": {"addMemory.sys.clock_tick.res": [ <--- system memory と 初期値
            ...
          {"addGrain.sys.clock_tick.branch_to_addAMB": ""}
        ]}},
        {"mem": {"addMemory.mem.clock_tick.res": [ <--- working memory と 初期値
            ...
          {"addGrain.mem.clock_tick.next_wakeup_time_ms": 0}
        ]}},
        {"scoop": {"addMemory.scoop.clock_tick.res": [ <--- scoopする(出力) memory
          "header_reserved",
          "addGrain.mem.clock_tick.tick_500ms"
        ]}},
        {"drop": {"addMemory.drop.clock_tick.res": [ <--- dropする（入力） memory
          "header_reserved",
          "addGrain.mem.blink_pattern.tick_500ms_is_used"
        ]}}
      ],

      "addAMB.atom.blink_pattern.res": [ <--- blink_pattern 先頭
        ...
      ],

      "addAMB.atom.led_driver.res": [ <--- led_driver 先頭
        ...
      ]
    }
  }
}
```

## 現在未実装のもの

- 初期値はJSONでの表現だけで、FPGAでの実アドレスへの展開は未検討である。
- call/return

## 次に直すこと

- system memory の再検討。
- operating は AtomBaseClass内 じゃない...と思うので、検討の上、外に出す。

## 注意: experimental / draft

- これは、完成した仕様ではなく、思考実験の進行ログとして更新していきます。
