# sys_keys_v001p0.py

class SysKeys: # System Keys

    # -----
    JSON_1146GND_CODE = "JSON_1146Gnd_Code"

    # -----
    # address_for_human_name
    ADDGRAIN = "addGrain" # for_Python_Memory_and_Module_name
    ADDAMB = "addAMB" # for_Atom_and_Molecule_and_Block_name
    ADDBRANCH = "addBranch" # for_BranchTable_name
    ADDMEMORY = "addMemory" # for_Memory_system_working_scoop_and_drop_name
    ADDNOP = "addNop" # for_comment_to_human

    # -----
    # address_type_name
    MOD = "mod" # python_module
    SYS = "sys" # python_memory_operating_system_memories
    MEM = "mem" # python_memory_working_memories
    SCOOP = "scoop" # output_memories
    DROP = "drop" # input_memories
    BRANCH = "branch" # branch_table
    ATOM = "atom" # atom
    MOLECULE = "molecule" # molecule
    BLOCK = "block" # block

    # -----
    # wild card and reserve
    WC = "wc" # name_wild_card
    RES = "res" # reserve_for_name

    # -----
    # address_composition_name
    ADDRESS_FOR_HUMAN_NAME = "address_for_human_name"
    ADDRESS_TYPE_NAME = "address_type_name"
    ATOM_OR_MOLECULE_OR_BLOCK_NAME = "atom_or_molecule_or_block_name"
    ATOM_OR_MOLECULE_OR_BLOCK_FUNCTION_NAME = "atom_or_molecule_or_block_function_name"
    # -----
    ADDRESS_COMPOSITION_NAME_LIST = [
        ADDRESS_FOR_HUMAN_NAME,
        ADDRESS_TYPE_NAME,
        ATOM_OR_MOLECULE_OR_BLOCK_NAME,
        ATOM_OR_MOLECULE_OR_BLOCK_FUNCTION_NAME,
        ]

    # -----
    # atom_molecule_composition_names
    HEADER_RESERVED = "header_reserved"
    OPERATING = "operating"
    INIT = "init"
    IDLE = "idle"

    RUN = "run"
    BRANCH = "branch"

    DELETE = "delete"

    SYS = "sys"
    MEM = "mem"
    SCOOP = "scoop"
    DROP = "drop"
    # -----
    ATOM_MOLECULE_COMPOSITION_NAMES_LIST = [
        HEADER_RESERVED,
        OPERATING,
        INIT,
        IDLE,

        RUN,
        BRANCH,

        DELETE,

        SYS,
        MEM,
        SCOOP,
        DROP,
        ]

    # -----
    # atom/moleclue state name
    # key_sys_state = "sys_state"
    # key_state's enum (value)
    ENUM_RESERVED = "enum_reserved"
    ENUM_CREATED = "enum_created" # 初期化(enum_initialized)されるまでの状態(state)
    ENUM_INITIALIZED = "enum_initialized"
    ENUM_IDLE = "enum_idle"

    ENUM_RUNNING = "enum_running"
    ENUM_BRANCHING = "enum_branching"

    ENUM_DELETED = "enum_deleted"

    # -----
    # system memory? func name?
    # sys.wc
    STATE = "state"
    IDLE_TO_RUN_FG = "idle_to_run_fg"
    BRANCH_TABLE_NUM = "branch_table_num"
    NEXT_STATE = "next_state" # "", "idle", "run", "delete" ---> not used??? (001p0_osd-led-blink-1hz)
    BRANCH_TO_ADDAMB = "branch_to_addAMB" # ret_atom_name # ex."", "addAMB.atom.blink_pattern.res",...
