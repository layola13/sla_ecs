#!/usr/bin/env python3
"""Fix SLA `while { ... };` -> `while { ... }` while keeping `if/else { ... };`.

SLA rule: `while` blocks end with `}` (no semicolon).
`if`/`else` blocks end with `};` (semicolon required).
Stand-alone `} else {` lines mix close+open and must NOT be modified.
"""
import re, sys

def fix(path):
    with open(path) as f:
        lines = f.readlines()
    stack = []  # kinds: 'while' | 'if' | 'else' | 'fn' | 'struct' | 'test'
    out = []
    for i, line in enumerate(lines):
        s = line.rstrip('\n')
        indent = len(s) - len(s.lstrip())
        body = s.lstrip()

        # Case A: mixed close+open line like `} else {` or `} else if .. {`:
        # Pop the opener first (the close consumes whatever block was open),
        # then push the next opener (else).
        m_mixed = re.match(r'^(\}+)(\s*(?:else\b|else\s+if\b)?.*?\{)\s*$', body)
        if m_mixed:
            for _ in range(len(m_mixed.group(1))):
                kind = stack.pop() if stack else None
            kind = None
            if 'else' in m_mixed.group(2) and 'if' not in m_mixed.group(2):
                kind = 'else'
            elif 'while' in m_mixed.group(2):
                kind = 'while'
            elif 'if' in m_mixed.group(2):
                kind = 'if'
            if kind:
                stack.append(kind)
            out.append(line)
            continue

        # Case B: pure close `^}+;?$`
        m_close = re.fullmatch(r'( *)(\}+)(;?)', s)
        if m_close:
            n_close = len(m_close.group(2))
            had_semi = m_close.group(3) == ';'
            closing_kinds = []
            for _ in range(n_close):
                k = stack.pop() if stack else None
                closing_kinds.append(k)
            outer = closing_kinds[0] if closing_kinds else None
            rebuild = ' ' * indent + '}' * n_close
            # Keep semicolon if outer is if/else (and not if outer is while/fn/struct|test)
            if had_semi and outer in ('if', 'else'):
                rebuild += ';'
            out.append(rebuild + '\n')
            continue

        # Case C: opener line ending in `{`
        if s.rstrip().endswith('{'):
            kind = None
            if re.search(r'\bwhile\b', s):
                kind = 'while'
            elif re.search(r'\belse\b', s) and not re.search(r'\bif\b', s):
                kind = 'else'
            elif re.search(r'\bif\b', s):
                kind = 'if'
            elif re.search(r'\bfn\b', s):
                kind = 'fn'
            elif re.search(r'\bstruct\b', s):
                kind = 'struct'
            elif re.search(r'\btest\b', s) and '@test' not in s:
                # @test "name"() { handled separately below
                pass
            if '@test' in s:
                kind = 'test'
            if kind:
                stack.append(kind)
        out.append(line)

    with open(path, 'w') as f:
        f.write(''.join(out))
    return path

if __name__ == '__main__':
    for p in sys.argv[1:]:
        fix(p)
        print('fixed', p)
