from __future__ import annotations

import dataclasses

import typing as T

from mesonbuild.modules import ExtensionModule, ModuleInfo
from mesonbuild.interpreter import Interpreter
from mesonbuild.interpreterbase import (
        InterpreterObject,
        ObjectHolder,
        typed_pos_args,
        noKwargs,
)
from mesonbuild.utils.core import HoldableObject
from mesonbuild import mesonlib
from mesonbuild.build import Executable

@dataclasses.dataclass
class ClippyGenerator(HoldableObject):
    executable: Executable

    def command(self) -> CommandList:
        return T.cast('CommandList', [self.executable]) + T.cast('CommandList', [])

    def found(self) -> bool:
        return self.executable.found()

class ClippyHolder(ObjectHolder[ClippyGenerator]):
    @typed_pos_args('clippymeson.clippy.process', str)
    @noKwargs
    @InterpreterObject.method('process')
    def process_method(self, args: T.Tuple, kwargs): #: FindLexKwargs):
        #breakpoint()
        #return ClippyGenerator(args[0])
        return args[0]

class ClippyModule(ExtensionModule):
    """FRRouting clippy"""

    INFO = ModuleInfo('clippymeson', '1.10.1', unstable=False)

    def __init__(self, interpreter: Interpreter) -> None:
        super().__init__(interpreter)
        self.methods.update({
            'setup': self.setup_method,
        })

    @typed_pos_args('clippymeson.setup', Executable)
    @noKwargs
    def setup_method(self, state: ModuleState, args: T.Tuple, kwargs: FindLexKwargs) -> ClippyGenerator:
        #breakpoint()
        return ClippyGenerator(args[0])

def initialize(interpreter: Interpreter) -> CodeGenModule:
    interpreter.append_holder_map(ClippyGenerator, ClippyHolder)
    return ClippyModule(interpreter)
