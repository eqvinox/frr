import sys
import os
from importlib.machinery import PathFinder, ModuleSpec

from mesonbuild import mesonmain

_selfpath = os.path.dirname(os.path.abspath(__file__))
#sys.path.remove(_selfpath)
sys.path.append(os.path.join(_selfpath, "python"))

class MesonextPathFinder(PathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname != "mesonbuild.modules.clippymeson":
            return None

        inh = super().find_spec("clippymeson", None, target)
        return inh

sys.meta_path.append(MesonextPathFinder())

sys.exit(mesonmain.main())
