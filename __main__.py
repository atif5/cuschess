import sys
from cuschess.computer.__main__ import main as comp
from cuschess.chess.__main__ import main as twoplayer
from cuschess.cusonline.__main__ import main as online

map_ = {
    "--online": online,
    "--2player": twoplayer,
    "--computer": comp
}

if __name__ == '__main__':
    try:
        map_[sys.argv[1]]()
    except IndexError:
        print("specify mode.")
        print("possible mods:", list(map_.keys()))
    except KeyError:
        print("no such mode.")
        print("possible mods:", list(map_.keys()))
        