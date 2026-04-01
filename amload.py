#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import sys
import os
import subprocess
import re
import typing as T

import ply.lex as lex # type: ignore[import-untyped]
import ply.yacc as yacc # type: ignore[import-untyped]

if T.TYPE_CHECKING:
    from ply.yacc import YaccProduction

class LexerBase:
    def new_line(self, lexer, n = 1):
        lexer.lineno += n

    def t_ANY_error(self, t):
        def indstr(line, pos):
            return ''.join([' ' if i != '\t' else '\t' for i in line[:pos]])

        ldata = t.lexer.lexdata
        line_start = ldata.rfind('\n', 0, t.lexpos) + 1
        line = ldata[line_start:].split('\n', 1)[0]
        relpos = t.lexpos - line_start

        raise ValueError("<input>:%d:%d: Illegal character '%s'\n> %s\n> %s^- here" % (
                t.lexer.lineno, relpos + 1, t.value[0], line, indstr(line, relpos)))

    def build(self, **kwargs):
        self.lexer = lex.lex(module = self, **kwargs)
        return self

    def test(self, data):
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok:
                 break
             print(tok)

class AMLexer(LexerBase):
    states = (
        ('value', 'exclusive'),
    )
    tokens = []
    keywords = []

    val_keywords = ['if', 'include']
    keywords += val_keywords + ['else', 'endif']
    tokens += list([x.upper() for x in keywords])
    tokens += ['NAME', 'VALUE', 'EQ', 'TARGET', 'BUILD']
    literals = ''

    def t_doc(self, t):
        r'[ \t]*\#([^\n]*)\n'
        self.new_line(t.lexer, 1)

    def t_newline(self, t):
        r'\n+'
        self.new_line(t.lexer, len(t.value))

    def t_space_nl(self, t):
        r'\s+\n'
        self.new_line(t.lexer, 1)
        sys.stderr.write('stray whitespace\n')

    def t_target(self, t):
        r'[-a-zA-Z_\%\$\(\)@/\.0-9 ]*:'
        t.value = t.value[:-1]
        t.type = 'TARGET'
        self.start_value(t)
        return t

    def t_build(self, t):
        r'\t'
        self.start_value(t, 'BUILD')

    def t_name(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*(?!:)'
        t.type = t.value.upper() if t.value in self.keywords else 'NAME'
        if t.value in self.val_keywords:
            self.start_value(t)
        return t

    def t_equals(self, t):
        r'\s*[\+\?]?='
        t.value = t.value.lstrip()
        t.type = 'EQ'
        self.start_value(t)
        return t

    def start_value(self, t, token = 'VALUE'):
        t.lexer.push_state('value')
        t.lexer.value = ''
        t.lexer.val_token = token

    def t_value_basic(self, t):
        r'[^\\\n\#]+'
        t.lexer.value += t.value

    def t_value_bsl(self, t):
        r'\\(?!\n)'
        t.lexer.value += t.value

    def t_value_wrap(self, t):
        r'\\\n'
        self.new_line(t.lexer, 1)

    def t_value_end(self, t):
        r'(\#[^\n]*)?\n'
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
        self.parser = yacc.yacc(module = self, start = 'exprs', **kwargs)
        return self

    def __call__(self, *args, **kwargs):
        return self.parser.parse(*args, tracking=True, **kwargs)

AMParser = ParserBase(tokens=AMLexer.tokens)

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
        if hasattr(val, 'pretty'):
            return val.pretty().replace('\n', '\n  ')
        else:
            return repr(val)

    def pretty(self):
        return '<%s%s>' % (self.__class__.__name__,
                ''.join([" %s=%s" % (k, self.pretty_maybe(getattr(self, k))) for k in self._args]))

    def recurse(self, parser):
        pass

I = T.TypeVar('I', bound=AMExpr)

class AMExprsBase(AMExpr, list[I]):
    _list: list[I] | None
    _item: I | None

    def __init__(self, *args, **kwargs): #items = [], append = None, **kwa):
        super().__init__(*args, **kwargs)
        if self._list:
            self.extend(self._list)
        if self._item is not None:
            self.append(self._item)

    def pretty(self):
        name = " name='%s'" % (self.name) if hasattr(self, 'name') else ''
        if hasattr(self, "lineno"):
            lineno = " #%d" % (self.lineno) if self.lineno else ""
        else:
            lineno = ""
        return '<%s%s%s (%d)%s%s>' % (self.__class__.__name__, lineno, name, len(self),
                '\n' if len(self) > 0 else '',
                ''.join(['  %s\n' % self.pretty_maybe(i) for i in self]))

    def recurse(self, parser):
        for item in self:
            item.recurse(parser)

class AMAssign(AMExpr):
    mode: str
    var: str
    value: str

    @AMParser.rule
    def p_expr_assign(p: YaccProduction):
        '''expr : NAME EQ VALUE'''
        p[0] = AMAssign(p, [2, 1, 3])

class AMConditional(AMExpr):
    cond: str
    it_true: AMExprs
    it_false: AMExprs | None

    @AMParser.rule
    def p_expr_cond(p: YaccProduction):
        '''expr : IF VALUE exprs ENDIF
                | IF VALUE exprs ELSE exprs ENDIF'''
        p[0] = AMConditional(p, [2, 3, 5])

class AMExprs(AMExprsBase[AMExpr]):
    @AMParser.rule
    def p_exprs_empty(p: YaccProduction):
        '''exprs : '''
        p[0] = AMExprs(p, [])

    @AMParser.rule
    def p_exprs_one(p: YaccProduction):
        '''exprs : exprs expr'''
        p[0] = AMExprs(p, [1, 2])


class AMBuildCmd(AMExpr):
    cmd: str

    @AMParser.rule
    def p_build(p: YaccProduction):
        '''buildcmd : BUILD'''
        p[0] = AMBuildCmd(p, [1])


class AMBuild(AMExprsBase[AMBuildCmd]):
    @AMParser.rule
    def p_builds_empty(p: YaccProduction):
        '''builds : '''
        p[0] = AMBuild(p, [])

    @AMParser.rule
    def p_builds_build(p: YaccProduction):
        '''builds : builds buildcmd'''
        p[0] = AMBuild(p, [1, 2])


class AMTarget(AMExpr):
    target: str
    deps: str
    builds: AMBuild

    @AMParser.rule
    def p_expr_target(p: YaccProduction):
        '''expr : TARGET VALUE builds'''
        p[0] = AMTarget(p, [1, 2, 3])


class AMInclude(AMExpr, list):
    filename: str

    @AMParser.rule
    def p_expr_incl(p: YaccProduction):
        '''expr : INCLUDE VALUE'''
        p[0] = AMInclude(p, [2])

    def pretty(self):
        name = " filename='%s'" % (self.filename)
        return '<%s%s (%d)%s%s>' % (self.__class__.__name__, name, len(self),
                '\n' if len(self) > 0 else '',
                ''.join(['  %s\n' % i.pretty() for i in self]))

    def recurse(self, parser):
        with open(self.filename, encoding="UTF-8") as fd:
            data = fd.read()
        self.extend(parser(data))
        for item in self:
            item.recurse(parser)


class AMFile(AMInclude):
    lexer = AMLexer().build()
    parser = AMParser.build()

    def __init__(self, filename):
        super().__init__(None, [])
        self.filename = filename

    def load(self):
        self.recurse(self.parser)


prefixes = ['noinst', 'nodist', 'dist', 'inst', 'check', 'EXTRA']
re_canon = re.compile('[^a-zA-Z0-9]')
re_fixrefs = re.compile(r"""\$\(([^\)]+)\)""")
flagnames = ['CFLAGS', 'CPPFLAGS', 'LIBADD', 'LDADD', 'LDFLAGS', 'LFLAGS', 'YFLAGS']
def fixrefs(d):
    return re_fixrefs.sub('$\\1', d)

if __name__ == "__main__":
    for fn in sys.argv[1:]:
        sys.stderr.write('\033[33m%s\033[m\n' % fn)
        file = AMFile(fn)
        file.load()
        p = file.pretty()
        print(p)
        print(f"# lines: {p.count('\n')}")
        #with open(fn, encoding="UTF-8") as fd:
        #    data = fd.read()

        #x = parser(data)
        #x.recurse(parser)
        #print(x.pretty())

