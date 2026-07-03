#!/usr/bin/env python3
"""Fix SLA `while { ... };` closing semicolons: while block needs `}` without `;`."""
import re, sys

def is_block_open(s):
    s = s.rstrip()
    if not s.endswith('{'):
        return None
    # sort by indentation precedence; return (indent, kind)
    indent = len(s) - len(s.lstrip())
    if re.search(r'\bwhile\b', s):
        return (indent, 'while')
    if re.search(r'\bif\b', s) and not s.rstrip().endswith('}'):
        return (indent, 'if')
    if re.search(r'\belse\b', s):
        return (indent, 'else')
    if re.search(r'\bfn\b', s):
        return (indent, 'fn')
    if re.search(r'\bstruct\b', s):
        return (indent, 'struct')
    if re.search(r'\btest\b', s):
        return (indent, 'test')
    return (indent, 'other')

def fix(path):
    with open(path) as f:
        lines = f.readlines()
    stack = []
    out = []
    for line in lines:
        raw = line.rstrip('\n')
        m = re.fullmatch(r'(\s*)(\}+)(\s*;?)\s*', raw)
        if m:
            indent = len(m.group(1))
            brace_count = len(m.group(2))
            had_semi = m.group(3).strip() == ';'
            # pop brace_count blocks
            kinds = []
            for _ in range(brace_count):
                if stack:
                    kinds.append(stack.pop())
            outer = kinds[0] if kinds else None
            # always strip the semicolon and re-add only if outer closes an if/else
            rebuild = ' ' * indent + '}' * brace_count
            if had_semi and outer in ('if','else'):
                rebuild += ';'
            out.append(rebuild + '\n')
        else:
            ob = is_block_open(raw)
            if ob:
                stack.append(ob[1])
            out.append(line)
    with open(path,'w') as f:
        f.write(''.join(out))
    return path

if __name__ == '__main__':
    for p in sys.argv[1:]:
        fix(p)
        print('fixed', p)
