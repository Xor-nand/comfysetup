# Copyright (C) 2017  The Comfysetup Authors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import ply.lex
import ply.yacc


class ParsingException(Exception):
    pass


parsed = { }


tokens = ('PKGNAME', 'ASSIGN', 'URL', 'COMMIT')
t_ignore_COMMENT = r'\#.*'
t_ignore = ' \t'


t_ASSIGN = '='
t_PKGNAME = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_URL = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'


def t_COMMIT(t):
    r'@[0-9a-f]+'
    t.value = t.value[1:]  # remove the '@' character
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    raise ParsingException("Illegal character '{}' at line {}".format(
        t.value[0], t.lexer.lineno))
    # t.lexer.skip(1)


lexer = ply.lex.lex()


def p_package(t):
    'package : PKGNAME ASSIGN URL COMMIT'
    parsed[t[1]] = (t[3], t[4])


def p_error(t):
    if t is None:
        return
    raise ParsingException("Syntax error around '{}' <{}> at line {}.".format(
        t.value, t, t.lexer.lineno))


parser = ply.yacc.yacc()


def parse(path):
    global parsed
    parsed = { }
    with open(path, 'r') as f:
        contents = f.read()
    lexer.lineno = 1
    for line in contents.split('\n'):
        parser.parse(line)
        lexer.lineno += 1
    return parsed
