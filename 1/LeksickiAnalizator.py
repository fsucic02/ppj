import sys

uniznakovi = ['=', '+', '-', '*', '/', '(', ')', 'za', 'od', 'do', 'az']
znakovi = { '=': 'OP_PRIDRUZI',
            '+': 'OP_PLUS',
            '-': 'OP_MINUS',
            '*': 'OP_PUTA',
            '/': 'OP_DIJELI',
            '(': 'L_ZAGRADA',
            ')': 'D_ZAGRADA', 
            'za': 'KR_ZA', 
            'od': 'KR_OD', 
            'do': 'KR_DO', 
            'az': 'KR_AZ' }

def process(str):
    result = str
    i = result.find('//')
    if i != -1:
        result = result[:i]
    for znak in uniznakovi[:7]:
        result = result.replace(znak, ' ' + znak + ' ')
    return result

for linenum, line in enumerate(sys.stdin, 1):
    line = process(line)
    for token in line.strip().split(' '):
        token = token.strip()
        if token == '':
            continue
        if token[0].isdigit() and not all(char.isdigit() for char in token): # 3asd
            idx = next((index for index, char in enumerate(token) if char.isalpha()), -1)
            print(f'BROJ {linenum} {token[:idx]}')
            print(f'IDN {linenum} {token[idx::]}')
        elif token.isdigit():
            print(f'BROJ {linenum} {token}')
        elif token in uniznakovi:
            print(f'{znakovi[token]} {linenum} {token}')
        else:
            print(f'IDN {linenum} {token}')
            