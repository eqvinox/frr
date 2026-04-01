#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=no-self-argument,unsupported-assignment-operation

from __future__ import annotations

import sys
import os
import subprocess
import re
from dataclasses import dataclass, field
import typing as T

import ply.lex as lex  # type: ignore[import-untyped]
import ply.yacc as yacc  # type: ignore[import-untyped]

if T.TYPE_CHECKING:
    from ply.yacc import YaccProduction


class LexerBase:
    def new_line(self, lexer, n=1):
        lexer.lineno += n

    def t_ANY_error(self, t):
        def indstr(line, pos):
            return "".join([" " if i != "\t" else "\t" for i in line[:pos]])

        ldata = t.lexer.lexdata
        line_start = ldata.rfind("\n", 0, t.lexpos) + 1
        line = ldata[line_start:].split("\n", 1)[0]
        relpos = t.lexpos - line_start

        raise ValueError(
            "<input>:%d:%d: Illegal character '%s'\n> %s\n> %s^- here"
            % (t.lexer.lineno, relpos + 1, t.value[0], line, indstr(line, relpos))
        )

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


class MakeLexer(LexerBase):
    states = (("autoconf", "exclusive"), ("make", "exclusive"), ("makefunc", "exclusive"))
    tokens = []
    keywords = []

    tokens += ["ACVAR", "MAKEVAR", "MAKEFUNC", "MAKEFUNCARG", "NORMAL", "WHITESPACE"]

    def t_makevar_single(self, t):
        r"\$[^$({]"
        t.value = t.value[1]
        t.type = "MAKEVAR"
        return t

    def t_begin_make(self, t):
        r"\$[({]"
        t.lexer.push_state("make")
        t.lexer.value = ""
        t.lexer.make_end = { "(": ")", "{": "}" }[t.value[1]]

    def t_make_normal(self, t):
        r"[a-zA-Z0-9_]+[)}]"
        t.lexer.pop_state()
        assert t.value[-1] == t.lexer.make_end
        t.value = t.value[:-1]
        t.type = "MAKEVAR"
        return t

    def t_make_func(self, t):
        r"[a-zA-Z0-9_]+[ \t\n]"
        t.value = t.value[:-1]
        t.type = "MAKEFUNC"
        t.lexer.pop_state()
        t.lexer.push_state("makefunc")
        return t

    def t_makefunc_arg(self, t):
        r"[^)}]*[)}]"
        t.lexer.pop_state()
        assert t.value[-1] == t.lexer.make_end
        t.value = t.value[:-1]
        t.type = "MAKEFUNCARG"
        return t

    def t_begin_autoconf(self, t):
        r"@"
        t.lexer.push_state("autoconf")
        t.lexer.value = ""

    def t_autoconf_arg(self, t):
        r"[a-zA-Z0-9_]+"
        t.lexer.value += t.value

    def t_autoconf_end(self, t):
        r"@"
        t.lexer.pop_state()
        t.value = t.lexer.value
        t.type = "ACVAR"
        return t

    def t_normal(self, t):
        r"[^$@ \t\n]+"
        t.type = "NORMAL"
        return t

    def t_escaped_dollar(self, t):
        r"\$\$"
        t.value = "$"
        t.type = "NORMAL"
        return t

    def t_wsp(self, t):
        r"[ \t\n]+"
        t.type = "WHITESPACE"
        return t

if __name__ == "__main__" and (sys.argv + [""])[1] == "lextest":
    lexer = MakeLexer().build()
    lexer.test(sys.argv[2])
    sys.exit(0)

class AMLexer(LexerBase):
    states = (("value", "exclusive"),)
    tokens = []
    keywords = []

    val_keywords = ["if", "include"]
    keywords += val_keywords + ["else", "endif"]
    tokens += list([x.upper() for x in keywords])
    tokens += ["NAME", "VALUE", "EQ", "TARGET", "BUILD"]
    literals = ""

    def t_doc(self, t):
        r"[ \t]*\#([^\n]*)\n"
        self.new_line(t.lexer, 1)

    def t_newline(self, t):
        r"\n+"
        self.new_line(t.lexer, len(t.value))

    def t_space_nl(self, t):
        r"\s+\n"
        self.new_line(t.lexer, 1)
        sys.stderr.write("stray whitespace\n")

    def t_target(self, t):
        r"[-a-zA-Z_\%\$\(\)@/\.0-9 ]*:"
        t.value = t.value[:-1]
        t.type = "TARGET"
        self.start_value(t)
        return t

    def t_build(self, t):
        r"\t"
        self.start_value(t, "BUILD")

    def t_name(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*(?!:)"
        t.type = t.value.upper() if t.value in self.keywords else "NAME"
        if t.value in self.val_keywords:
            self.start_value(t)
        return t

    def t_equals(self, t):
        r"\s*[\+\?]?="
        t.value = t.value.lstrip()
        t.type = "EQ"
        self.start_value(t)
        return t

    def start_value(self, t, token="VALUE"):
        t.lexer.push_state("value")
        t.lexer.value = ""
        t.lexer.val_token = token

    def t_value_basic(self, t):
        r"[^\\\n\#]+"
        t.lexer.value += t.value

    def t_value_bsl(self, t):
        r"\\(?!\n)"
        t.lexer.value += t.value

    def t_value_wrap(self, t):
        r"\\\n"
        self.new_line(t.lexer, 1)

    def t_value_end(self, t):
        r"(\#[^\n]*)?\n"
        t.value = t.lexer.value.lstrip()
        t.type = t.lexer.val_token

        self.new_line(t.lexer, 1)
        t.lexer.pop_state()
        return t


class ParserBase:
    def __init__(self, tokens):
        self.tokens = tokens

    def rule(self, func):
        setattr(self, func.__name__, func)
        return staticmethod(func)

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, start="exprs", **kwargs)
        return self

    def __call__(self, *args, **kwargs):
        return self.parser.parse(*args, tracking=True, **kwargs)


class CondStack(list[T.Tuple["AMConditional", bool]]):
    def short(self):
        def item(cond, arc):
            return ("" if arc else "!") + cond.cond
        return " && ".join(item(cond, arc) for cond, arc in self)

    def possible(self):
        conds = {}
        for cond, arc in self:
            if conds.get(cond.cond, arc) != arc:
                return False
            conds[cond.cond] = arc
        return True

    def __add__(self, other):
        return CondStack(list(self) + other)

    def __sub__(self, other):
        new = CondStack()
        for cond, arc in self:
            if (cond, arc) in other:
                continue
            new.append((cond, arc))
        return new

AMParser = ParserBase(tokens=AMLexer.tokens)
#CondStack: T.TypeAlias = list[T.Tuple["AMConditional", bool]]
Walker: T.TypeAlias = T.Callable[["AMAssign | AMTarget", CondStack], None]

class AMExpr:
    _args: list[str]

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        if not hasattr(cls, "_args"):
            cls._args = list(cls.__annotations__.keys())

    def __init__(self, p, argidx, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if p is None:
            return

        for arg, idx in zip(self._args, argidx + [None] * len(self._args)):
            val = None
            if idx is not None and idx < len(p):
                val = p[idx]
            setattr(self, arg, val)

        self.lineno = p.lineno(0)
        self.lexspan = p.lexspan(0)

    @staticmethod
    def pretty_maybe(val):
        if hasattr(val, "pretty"):
            return val.pretty().replace("\n", "\n  ")
        else:
            return repr(val)

    def pretty(self):
        return "<%s%s>" % (
            self.__class__.__name__,
            "".join(
                [
                    " %s=%s" % (k, self.pretty_maybe(getattr(self, k)))
                    for k in self._args
                ]
            ),
        )

    def recurse(self, parser):
        pass

    def _walk(self, cb: Walker, condstack: CondStack) -> None:
        raise NotImplemented("override this")

I = T.TypeVar("I", bound=AMExpr)


class AMExprsBase(AMExpr, list[I]):
    _list: list[I] | None
    _item: I | None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._list:
            self.extend(self._list)
        if self._item is not None:
            self.append(self._item)

    def pretty(self):
        name = " name='%s'" % (self.name) if hasattr(self, "name") else ""
        if hasattr(self, "lineno"):
            lineno = " #%d" % (self.lineno) if self.lineno else ""
        else:
            lineno = ""
        return "<%s%s%s (%d)%s%s>" % (
            self.__class__.__name__,
            lineno,
            name,
            len(self),
            "\n" if len(self) > 0 else "",
            "".join(["  %s\n" % self.pretty_maybe(i) for i in self]),
        )

    def recurse(self, parser):
        for item in self:
            item.recurse(parser)


class AMAssign(AMExpr):
    mode: str
    var: str
    value: str

    @AMParser.rule
    def p_expr_assign(p: YaccProduction):
        """expr : NAME EQ VALUE"""
        p[0] = AMAssign(p, [2, 1, 3])

    def _walk(self, cb: Walker, condstack: CondStack) -> None:
        cb(self, condstack)

    def str_inc(self):
        return f"{self.mode} {self.value!r}"

class AMConditional(AMExpr):
    cond: str
    it_true: AMExprs
    it_false: AMExprs | None

    @AMParser.rule
    def p_expr_cond(p: YaccProduction):
        """expr : IF VALUE exprs ENDIF
        | IF VALUE exprs ELSE exprs ENDIF"""
        p[0] = AMConditional(p, [2, 3, 5])

    def _walk(self, cb: Walker, condstack: CondStack) -> None:
        self.it_true._walk(cb, condstack + [(self, True)])
        if self.it_false is not None:
            self.it_false._walk(cb, condstack + [(self, False)])

    def __eq__(self, other):
        return self.cond == other.cond


class AMExprs(AMExprsBase[AMExpr]):
    @AMParser.rule
    def p_exprs_empty(p: YaccProduction):
        """exprs :"""
        p[0] = AMExprs(p, [])

    @AMParser.rule
    def p_exprs_one(p: YaccProduction):
        """exprs : exprs expr"""
        p[0] = AMExprs(p, [1, 2])

    def _walk(self, cb: Walker, condstack: CondStack) -> None:
        for item in self:
            item._walk(cb, condstack)


class AMBuildCmd(AMExpr):
    cmd: str

    @AMParser.rule
    def p_build(p: YaccProduction):
        """buildcmd : BUILD"""
        p[0] = AMBuildCmd(p, [1])


class AMBuild(AMExprsBase[AMBuildCmd]):
    @AMParser.rule
    def p_builds_empty(p: YaccProduction):
        """builds :"""
        p[0] = AMBuild(p, [])

    @AMParser.rule
    def p_builds_build(p: YaccProduction):
        """builds : builds buildcmd"""
        p[0] = AMBuild(p, [1, 2])


class AMTarget(AMExpr):
    target: str
    deps: str
    builds: AMBuild

    @AMParser.rule
    def p_expr_target(p: YaccProduction):
        """expr : TARGET VALUE builds"""
        p[0] = AMTarget(p, [1, 2, 3])

    def _walk(self, cb: Walker, condstack: CondStack) -> None:
        cb(self, condstack)


class AMInclude(AMExpr, list):
    filename: str

    @AMParser.rule
    def p_expr_incl(p: YaccProduction):
        """expr : INCLUDE VALUE"""
        p[0] = AMInclude(p, [2])

    def pretty(self):
        name = " filename='%s'" % (self.filename)
        return "<%s%s (%d)%s%s>" % (
            self.__class__.__name__,
            name,
            len(self),
            "\n" if len(self) > 0 else "",
            "".join(["  %s\n" % i.pretty() for i in self]),
        )

    def recurse(self, parser):
        with open(self.filename, encoding="UTF-8") as fd:
            data = fd.read()
        self.extend(parser(data))
        for item in self:
            item.recurse(parser)

    def _walk(self, cb: Walker, condstack: CondStack) -> None:
        for item in self:
            item._walk(cb, condstack)


class AMFile(AMInclude):
    lexer = AMLexer().build()
    parser = AMParser.build()

    def __init__(self, filename):
        super().__init__(None, [])
        self.filename = filename

    def load(self):
        self.recurse(self.parser)

    def walk(self, cb: Walker) -> None:
        super()._walk(cb, CondStack())


@dataclass
class ATarget:
    mode: str
    name: str
    dirvar: str | None
    dstflags: set[str]
    conds: CondStack

    _arg_names: T.ClassVar[set[str]] = set()
    args: dict[str, list[tuple[AMAssign, CondStack]]] = field(init=False, default_factory=dict)

    def process(self, mvars: T.Mapping[str, list[tuple[AMAssign, CondStack]]]):
        canon = re_canon.sub("_", self.name)

        for arg_name in self._arg_names:
            for prefix in ["", "nodist_"]:
                arg_fullname = prefix + canon + "_" + arg_name
                if arg_fullname in mvars:
                    self.args[prefix + arg_name] = mvars[arg_fullname]
            
        #def __init__(self, name: str, dirvar: str | None, dstflags: set[str], conds: CondStack):

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name!r} ({self.dirvar!r}, {self.conds.short() or '<always>'}, {len(self.args)} args)>"

    def dump(self):
        print(repr(self))

class ATOther(ATarget):
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.mode} {self.name!r} ({self.dirvar!r}, {self.conds.short() or '<always>'}, {len(self.args)} args)>"

never_expand = {
    "AM_CFLAGS",
    "AM_CPPFLAGS",
    "CPPFLAGS_BASE",
}

class ATCompiledBase(ATarget):
    _flag_names = {
        "CFLAGS",
        "CPPFLAGS",
        "CXXFLAGS",
        "LIBADD",
        "LDADD",
        "LDFLAGS",
        "LFLAGS",
        "YFLAGS",
    }
    _arg_names = {
        "SOURCES",
    } | _flag_names

    def process(self, mvars: T.Mapping[str, list[tuple[AMAssign, CondStack]]]):
        super().process(mvars)

        self.sources = []
        self.process_sources(mvars, "")
        self.process_sources(mvars, "nodist_")

        self.flags = {}
        for flag in self._flag_names:
            if flag not in self.args:
                continue
            self.flags[flag] = list(self._flatten_var(mvars, self.args[flag], recurse=True))

    def _flatten_var(self, mvars, values, recurse=False):
        def process(element):
            if not element:
                return
            if len(element) == 1 and element[0].type == "NORMAL":
                yield (element[0].value, conds)
            elif recurse and len(element) == 1 and element[0].type == "MAKEVAR":
                #print("recursing into variable")
                if element[0].value in never_expand:
                    print(f"\033[36mnever_expand {element[0].value!r}\033[m")
                    return
                try:
                    values.extend((assign, varconds + conds) for assign, varconds in mvars[element[0].value])
                    print(f"\033[32mexpand {element[0].value!r}\033[m")
                except KeyError:
                    print(f"\033[33mreference to undefined {element[0].value!r}\033[m")
                    yield ("${" + element[0].value + "}", conds)
            else:
                yield (element, conds)

        while values:
            assign, conds = values.pop(0)
            if not (conds + self.conds).possible():
                print(f"\033[91mimpossible condition for {assign.value!r}: {conds.short()} + {self.conds.short()}\033[m")
                continue
            conds = conds - self.conds

            vlex = MakeLexer().build()
            vlex.lexer.input(assign.value)

            element = []
            while tok := vlex.lexer.token():
                #if tok.value == "MODULE_LDFLAGS":
                    #    breakpoint()
                if element and tok.type == "NORMAL" and element[-1].type == "NORMAL":
                    element[-1].value += tok.value
                    continue
                if tok.type == "WHITESPACE":
                    yield from process(element)
                    element = []
                    continue
                element.append(tok)

            yield from process(element)

    def process_sources(self, mvars, prefix):
        nodist = prefix == "nodist_"
        sources = self.args.get(prefix + "SOURCES", [])

        self.sources.extend(self._flatten_var(mvars, sources))

    def dump(self):
        super().dump()
        for src, conds in self.sources:
            print(f"\tsrc: [{conds.short()}] {src}")
        for k, v in self.flags.items():
            for item, conds in v:
                print(f"\t{k}: [{conds.short()}] {item}")
            #if k == "SOURCES":
            #    continue
        print("")

class ATProgram(ATCompiledBase):
    pass

class ATLibrary(ATCompiledBase):
    pass

class ATLibtoolLibrary(ATCompiledBase):
    pass

mainkeys = {
    "PROGRAMS": ATProgram,
    "SCRIPTS": ATOther,
    "HEADERS": ATOther,
    "LIBRARIES": ATLibrary,
    "LTLIBRARIES": ATLibtoolLibrary,
    "MANS": ATOther,
    "DATA": ATOther,
}

prefixes = ["noinst", "nodist", "nobase", "dist", "inst", "check", "EXTRA"]
re_canon = re.compile("[^a-zA-Z0-9]")
re_fixrefs = re.compile(r"""\$\(([^\)]+)\)""")


def fixrefs(d):
    return re_fixrefs.sub("$\\1", d)

class Formatter(list):
    def __init__(self):
        self.lens = []

    def __call__(self, *args):
        if len(self.lens) < len(args[:-1]):
            self.lens.extend([0] * (len(args) - len(self.lens)))
        for i, arg in enumerate(args[:-1]):
            self.lens[i] = max(self.lens[i], len(arg))
        self.append(args)

    def out(self, stream=sys.stdout, prefix=""):
        for row in self:
            stream.write(prefix)
            for i, width, val in zip(range(0, len(self.lens)), self.lens, row):
                if i != 0:
                    stream.write(" ")
                if i == len(self.lens) - 1:
                    stream.write(val)
                else:
                    stream.write(val.ljust(width))
            stream.write("\n")

KT = T.TypeVar("KT")
VT = T.TypeVar("VT")

class DictUsageProxy: #(T.Mapping[KT, VT]):
    _target: T.Mapping[KT, VT]
    used: set[KT]

    def __init__(self, target: T.Mapping[KT, VT]):
        self._target = target
        self.used = set()

    def __contains__(self, key: KT) -> bool:
        return key in self._target

    def __getitem__(self, key: KT) -> VT:
        self.used.add(key)
        return self._target[key]

class Collector:
    phonies: set[str]

    mvars: dict[str, list[tuple[AMAssign, CondStack]]]
    am_items: dict[str, list[tuple[str, str, str]]]

    def __init__(self):
        self.targets = {}
        self.mvars = {}
        self.am_items = {}
        self.mainkeys = set()
        self.phonies = set()

    def _walk_assign(self, item: AMAssign, condstack: CondStack) -> None:
        name = item.var.strip()
        if name.startswith("AM_V_") or name.startswith("am__v_"):
            return

        self.mvars.setdefault(name, []).append((item, condstack))

        suffix = name.rsplit("_", 1)[-1]
        if suffix in mainkeys:
            self.mainkeys.add(name)

        #print("===")
        #for cond, arc in condstack:
        #    print(f"\t{cond.cond}={arc}")
        #print(item.pretty())

    _ignore_targets = frozenset([
        ".PRECIOUS",
        ".SILENT",
        ".DEFAULT_GOAL",

        "all-am",
        "yorn",
        "indent",
        "redistclean",
        "topotests",
        "topotests-build",
        "copy_script",
        "check",
        "test",
        "doc",
        "clippy-only",
    ])
    _ignore_targets_re = [re.compile(expr) for expr in [
        r"(^|-)coverage$",
        r"^clean-",
        r"^install-",
        r"-(info|html|pdf)$",
        r"^(info|html|pdf)-",
    ]]

    def _walk_target(self, item: AMTarget, condstack: CondStack) -> None:
        target = item.target.strip()

        if target in self._ignore_targets:
            #print(f"ignored target {item.target}")
            return
        for ignore_re in self._ignore_targets_re:
            if ignore_re.search(target):
                #print(f"ignored target {item.target} (rex {ignore_re})")
                return

        if target == ".PHONY":
            deps = item.deps.strip().split()
            self.phonies.update(deps)
            for phony in deps:
                if phony in self.targets:
                    del self.targets[phony]
                    #print(f"removed .PHONY target {phony}")
            return

        if target in self.phonies:
            #print(f"ignored .PHONY target {item.target}")
            return

        self.targets.setdefault(target, []).append((item, condstack))
        #print("===")
        #for cond, arc in condstack:
        #    print(f"\t{cond.cond}={arc}")
        #print(item.pretty())
        #print(f"target: {item.target!r}")

    def walk(self, item: AMAssign | AMTarget, condstack: CondStack) -> None:
        if isinstance(item, AMTarget):
            self._walk_target(item, condstack)
        else:
            self._walk_assign(item, condstack)

    def am_targets(self):
        mvars = DictUsageProxy(self.mvars)
        dirvars = set()

        for mainkey in sorted(self.mainkeys):
            category, mode = mainkey.rsplit("_", 1)
            modeitems = self.am_items.setdefault(mode, [])
            modeclass = mainkeys[mode]

            dstflags = set()
            dirvar = category
            while (s := dirvar.split("_", 1))[0] in prefixes:
                dstflags.add(s[0])
                if len(s) == 1:
                    dirvar = None
                    break
                dirvar = s[1]
            else:
                dirvars.add(dirvar)

            assert mvars[mainkey][0][0].mode == "="

            for assign, conds in mvars[mainkey]:
                vals = assign.value.strip().split()

                for val in vals:
                    modeitems.append(modeclass(mode, val, dirvar, dstflags, conds))

        print("== automake destination directories:")
        for dirvar in sorted(dirvars):
            if dirvar + "dir" in mvars:
                dirval = mvars[dirvar + 'dir']
                assert len(dirval) == 1
                val, conds = dirval[0]

                print(f"\t{dirvar:20} = {val.value!r} [{conds.short()}]")
            else:
                print(f"\t{dirvar:20} =   <unspecified>")
        print("")

        for mode, targets in self.am_items.items():
            for target in targets:
                target.process(mvars)
                target.dump()

        def show(vals, rmconds=CondStack()):
            ret = []
            for assign, vconds in vals:
                value = " ".join(assign.value.strip().split())
                realconds = vconds - rmconds
                if realconds:
                    ret.append(f"\033[33m[{realconds.short()}]?(\033[m {value} \033[33m)\033[m")
                else:
                    ret.append(value)
            return ", ".join(ret)

        print("unused:")
        for k, v in self.mvars.items():
            if k in mvars.used:
                continue
            print(f"\t{k} = {show(v)}")
            for assign, conds in v:
                print(f"\t++ {conds.short()}")
                vlex = MakeLexer().build()
                try:
                    vlex.lexer.input(assign.value)
                    while tok := vlex.lexer.token():
                        print(f"\t\t{tok}")
                except ValueError as e:
                    print("FAILED:", e)
        #print("\n".join(c.mvars.keys()))

if __name__ == "__main__":
    for fn in sys.argv[1:]:
        sys.stderr.write("\033[33m%s\033[m\n" % fn)
        file = AMFile(fn)
        file.load()
        if False:
            p = file.pretty()
            print(p)
            print(f"# lines: {p.count('\n')}")

        c = Collector()
        file.walk(c.walk)
        c.am_targets()

        #print("\n".join(c.mvars.keys()))

        # with open(fn, encoding="UTF-8") as fd:
        #    data = fd.read()

        # x = parser(data)
        # x.recurse(parser)
        # print(x.pretty())
