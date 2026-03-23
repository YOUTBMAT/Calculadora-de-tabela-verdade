"""Calculadora de Tabela Verdade com suporte a infinitas variáveis e sem exigir parênteses.

Uso:
    - Entrada: expressão com variáveis (A, B, C...) e operadores lógicos:
      NOT, !, ~, AND, &, *, OR, |, +, XOR, ^, =>, ->, <=, <-, <->, ==, equivalence.
    - Exemplo: A and B or not C xor D
    - O parser resolve precedência: NOT > AND > XOR > OR > IMPLIES > EQUIV.

Executa tabela verdade para todas combinações de variáveis.
"""

# Importações necessárias para o funcionamento do programa

import re
import itertools

# Dicionário que define os operadores lógicos suportados
# Cada operador tem: (precedência, aridade, função lambda)
# Precedência: maior número = maior prioridade
# Aridade: 1 para unário (NOT), 2 para binário

OPERATORS = {
    'NOT': (4, 1, lambda a: not a),
    '!'  : (4, 1, lambda a: not a),
    '~'  : (4, 1, lambda a: not a),
    'AND': (3, 2, lambda a, b: a and b),
    '&'  : (3, 2, lambda a, b: a and b),
    '*'  : (3, 2, lambda a, b: a and b),
    'OR' : (2, 2, lambda a, b: a or b),
    '|'  : (2, 2, lambda a, b: a or b),
    '+'  : (2, 2, lambda a, b: a or b),
    'XOR': (2, 2, lambda a, b: a ^ b),
    '^'  : (2, 2, lambda a, b: a ^ b),
    '=>' : (1, 2, lambda a, b: (not a) or b),
    '->' : (1, 2, lambda a, b: (not a) or b),
    '<=' : (1, 2, lambda a, b: (not b) or a),
    '<-' : (1, 2, lambda a, b: (not b) or a),
    '<->': (0, 2, lambda a, b: a == b),
    '==' : (0, 2, lambda a, b: a == b),
}

TOKEN_SPEC = [
    ('SKIP', r'[ \t]+'),
    ('VAR', r'[A-Za-z][A-Za-z0-9_]*'),
    ('OP', r'\<\-\>|\<\=|\=\>|\-\>|\^|\&|\||\+|\*|\!|\~'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('MISMATCH', r'.'),
]

TOKEN_RE = re.compile('|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPEC), re.IGNORECASE)


def tokenize(expr):
    tokens = []
    for mo in TOKEN_RE.finditer(expr):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'SKIP':
            continue
        if kind == 'MISMATCH':
            raise ValueError(f'Caractere inválido na expressão: {value}')
        if kind == 'VAR':
            v = value.upper()
            if v in OPERATORS:
                tokens.append(('OP', v))
            else:
                tokens.append(('VAR', v))
        elif kind == 'OP':
            tokens.append(('OP', value.upper()))
        else:
            tokens.append((kind, value))
    return tokens


def shunting_yard(tokens):
    out_q = []
    op_s = []

    def is_op(tok):
        return tok[0] == 'OP' and tok[1] in OPERATORS

    for token in tokens:
        typ, val = token
        if typ == 'VAR':
            out_q.append(token)
        elif is_op(token):
            op_prec, arity, _ = OPERATORS[val]
            while op_s and is_op(op_s[-1]):
                top_prec, _, _ = OPERATORS[op_s[-1][1]]
                if (op_prec <= top_prec):
                    out_q.append(op_s.pop())
                else:
                    break
            op_s.append(token)
        elif typ == 'LPAREN':
            op_s.append(token)
        elif typ == 'RPAREN':
            while op_s and op_s[-1][0] != 'LPAREN':
                out_q.append(op_s.pop())
            if not op_s or op_s[-1][0] != 'LPAREN':
                raise ValueError('Parênteses desbalanceados')
            op_s.pop()
        else:
            raise ValueError('Token desconhecido: %s' % token)

    while op_s:
        if op_s[-1][0] in ('LPAREN', 'RPAREN'):
            raise ValueError('Parênteses desbalanceados')
        out_q.append(op_s.pop())

    return out_q


def evaluate_rpn(rpn, vars_map):
    stack = []
    for token in rpn:
        typ, val = token
        if typ == 'VAR':
            if val not in vars_map:
                raise ValueError(f'Variable não definida: {val}')
            stack.append(vars_map[val])
        elif typ == 'OP':
            prec, arity, func = OPERATORS[val]
            if arity == 1:
                if not stack:
                    raise ValueError('Operador unário sem operando')
                a = stack.pop()
                stack.append(func(a))
            elif arity == 2:
                if len(stack) < 2:
                    raise ValueError('Operador binário sem operandos suficientes')
                b = stack.pop()
                a = stack.pop()
                stack.append(func(a, b))
            else:
                raise ValueError('Aridade inválida')
        else:
            raise ValueError('Token inválido no RPN: %s' % token)
    if len(stack) != 1:
        raise ValueError('Expressão inválida (pilha residual)')
    return stack[0]


def parse_expression(expr):
    cleaned = expr.strip()
    if not cleaned:
        raise ValueError('Expressão vazia')

    expanded = cleaned.upper()

    for k in ['AND', 'OR', 'NOT', 'XOR', 'TRUE', 'FALSE']:
        expanded = re.sub(r'\b' + k + r'\b', k, expanded, flags=re.IGNORECASE)

    tokens = tokenize(expanded)
    if not tokens:
        raise ValueError('Nenhum token encontrado')

    rpn = shunting_yard(tokens)
    return rpn


def find_variables(tokens):
    return sorted({tok[1] for tok in tokens if tok[0] == 'VAR'})


def format_bool(value):
    return '1' if value else '0'


def print_truth_table(expr):
    rpn = parse_expression(expr)
    vars_ = find_variables(tokenize(expr))
    if not vars_:
        resultado = evaluate_rpn(rpn, {})
        print('Sem variáveis, resultado:', format_bool(resultado))
        return

    header = ' | '.join(vars_) + ' | OUT'
    print(header)
    print('-' * len(header))

    for bits in itertools.product([False, True], repeat=len(vars_)):
        env = dict(zip(vars_, bits))
        out = evaluate_rpn(rpn, env)
        line = ' | '.join(format_bool(env[v]) for v in vars_) + ' | ' + format_bool(out)
        print(line)


def main():
    print('Calculadora de Tabela Verdade (sem necessidade de parênteses)')
    print('Operadores válidos: NOT/!, AND/&/*, OR/|/+, XOR/^, =>/->, <->/==')
    print('Digite "sair" ou Ctrl+C para encerrar.')

    while True:
        try:
            expr = input('\nExpressão: ').strip()
            if not expr:
                continue
            if expr.lower() in ('sair', 'exit', 'quit'):
                print('Saindo...')
                break

            print_truth_table(expr)

        except Exception as e:
            print('Erro:', e)


if __name__ == '__main__':
    main()
    