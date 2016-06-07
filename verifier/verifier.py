#!/usr/env python

import os
import sys
import re
import subprocess
import copy

patterns = [
    ('BEGIN', re.compile(r'.*public void testMe.*')),
    ('END', re.compile(r'}')),
    ('ADD', re.compile(r'[a-zA-Z$_0-9]+ = -?[a-zA-Z0-9$_]+ [+] -?[a-zA-Z0-9$_]+;')),
    ('SUBTRACT', re.compile(r'[a-zA-Z$_0-9]+ = -?[a-zA-Z0-9$_]+ [-] -?[a-zA-Z0-9$_]+;')),
    ('MULTIPLY', re.compile(r'[a-zA-Z$_0-9]+ = -?[a-zA-Z0-9$_]+ [*] -?[a-zA-Z0-9$_]+;')),
    ('DIVIDE', re.compile(r'[a-zA-Z$_0-9]+ = -?[a-zA-Z0-9$_]+ [/] -?[a-zA-Z0-9$_]+;')),
    ('PARA-ASSIGN', re.compile(r'[a-zA-Z$_0-9]+ := @[a-zA-Z0-9$_]+: int;')),
    ('ASSIGN', re.compile(r'[a-zA-Z$_0-9]+ = -?[a-zA-Z$_0-9];')),
    ('IFEQUAL', re.compile(r'if -?[a-zA-Z$_0-9]+ == -?[a-zA-Z$_0-9]+ goto [a-zA-Z$_0-9]+;')),
    ('IFNE', re.compile(r'if -?[a-zA-Z$_0-9]+ != -?[a-zA-Z$_0-9]+ goto [a-zA-Z$_0-9]+;')),
    ('IFGT', re.compile(r'if -?[a-zA-Z$_0-9]+ > -?[a-zA-Z$_0-9]+ goto [a-zA-Z$_0-9]+;')),
    ('IFGTE', re.compile(r'if -?[a-zA-Z$_0-9]+ >= -?[a-zA-Z$_0-9]+ goto [a-zA-Z$_0-9]+;')),
    ('IFLT', re.compile(r'if -?[a-zA-Z$_0-9]+ < -?[a-zA-Z$_0-9]+ goto [a-zA-Z$_0-9]+;')),
    ('IFLTE', re.compile(r'if -?[a-zA-Z$_0-9]+ <= -?[a-zA-Z$_0-9]+ goto [a-zA-Z$_0-9]+;')),
    ('GOTO', re.compile(r'goto [a-zA-Z$_0-9]+;')),
    ('THROW', re.compile(r'throw [a-zA-Z$_0-9]+')),
    ('DECLARE', re.compile(r'int [a-zA-Z$_0-9]+')),
    ('DECLAREBYTE', re.compile(r'byte [a-zA-Z$_0-9]+')),
    ('LABEL', re.compile(r'[a-zA-Z$_0-9]+:')),
    ('NEG', re.compile(r'[a-zA-Z$_0-9]+ = neg -?[a-zA-Z0-9$_]+;')),
]

working = False
jimples = []
variables = {}
current_assert = None

try:
    real_name = filter(None, re.split('/|\.', sys.argv[1]))[-2]
except:
    print '\033[91m' + 'File name is not correct. plz check it.' + '\033[0m'
    sys.exit()
java_name = real_name + '.java'
class_name = real_name + '.class'
jimple_name = real_name + '.jimple'
z3_name = real_name + '.z3'

########## functions ##########
def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

def generate_jimple():
    if os.system('cp ' + sys.argv[1] + ' soot/' + ' 2> /dev/null'):
        print '\033[91m' + 'File name is not correct. plz check it.' + '\033[0m'
        sys.exit()
    os.chdir('soot')
    os.system('rm ' + class_name + ' ' + jimple_name + ' ' + z3_name + ' 2> /dev/null')
    if os.system('javac ' + java_name + ' 2> /dev/null'):
        print '\033[91m' + 'Java compiler error! plz check it.' + '\033[0m'
        sys.exit()
    if os.system('./soot.sh ' + real_name + ' > /dev/null 2> /dev/null'):
        print '\033[91m' + 'Transform(java->jimple) error! plz check it.' + '\033[0m'
        sys.exit()

def generate_z3(label_idx):
    global current_assert
    global variables

    for inst in jimples[label_idx]:
        for key, pattern in patterns:
            if pattern.search(inst):
                if key == 'THROW':
                    # exit condition
                    with open(z3_name, 'a') as z3_stream:
                        z3_stream.write('(assert ' + current_assert + '))\n')
                        z3_stream.write('(check-sat)\n')
                    z3_result = filter(None, re.split(' |\n', subprocess.check_output('z3 -T:10 ' + z3_name, shell=True)))[0]
                   
                    if z3_result == 'timeout':
                        os.system('rm ' + java_name + ' ' + class_name + ' ' + jimple_name + ' ' + z3_name + ' 2> /dev/null')
                        print 'VALID'
                        sys.exit()
                    elif z3_result != 'unsat':
                        with open(z3_name, 'a') as z3_stream:
                            z3_stream.write('(get-model)\n')
                        z3_result = subprocess.check_output('z3 ' + z3_name, shell=True)
                        print z3_result[4:]
                        os.system('rm ' + java_name + ' ' + class_name + ' ' + jimple_name + ' ' + z3_name + ' 2> /dev/null')
                        sys.exit()
                    else:
                        f = open(z3_name, 'r')
                        lines = f.readlines()[:-2]
                        f.close()
                        f = open(z3_name, 'w')
                        f.writelines(lines)
                        f.close()
                    return
                elif key == 'GOTO':
                    next_idx = int(re.findall(r'\d+', filter(None, re.split(' |;', inst))[1])[0])
                    generate_z3(next_idx)
                    return
                elif key == 'END': 
                    return
                elif key == 'PARA-ASSIGN':
                    variables[inst.split()[0]] = inst.split()[0]
                    with open(z3_name, 'a') as z3_stream:
                        z3_stream.write('(declare-const ' + inst.split()[0] + \
                                ' Int)\n')
                elif key == 'ASSIGN':
                    decoded = filter(None, re.split(' |;', inst))
                    if decoded[2] in variables:
                        variables[decoded[0]] = variables[decoded[2]]
                    else:
                        variables[decoded[0]] = decoded[2]
                elif key == 'NEG':
                    decoded = filter(None, re.split(' |;', inst))
                    if decoded[3] in variables:
                        variables[decoded[0]] = variables[decoded[3]]
                    elif decoded[3][0] == '-':
                        variables[decoded[0]] = decoded[3][1:]
                    else:
                        variables[decoded[0]] = '-' + decoded[3]
                elif key == 'ADD' or key == 'SUBTRACT' or \
                        key == 'MULTIPLY' or key == 'DIVIDE':
                    decoded = filter(None, re.split(' |;', inst))
                    op1 = None; op2 = None
                    if decoded[2] in variables:
                        op1 = variables[decoded[2]]
                    else:
                        op1 = decoded[2]
                    if decoded[4] in variables:
                        op2 = variables[decoded[4]]
                    else:
                        op2 = decoded[4]
                    variables[decoded[0]] = '(' + decoded[3] + ' ' + \
                            op1 + ' ' + op2 + ')'
                else: # only if statement
                    # step1: decode instruction
                    decoded = filter(None, re.split(' |;', inst))
                    op1 = None; op2 = None
                    if decoded[1] in variables:
                        op1 = variables[decoded[1]]
                    elif check_int(decoded[1]):
                        op1 = decoded[1]
                    else:
                        # exception case
                        if key == 'IFEQUAL':
                            next_idx = int(re.findall(r'\d+', decoded[5])[0])
                            generate_z3(next_idx)
                            return
                        break
                    if decoded[3] in variables:
                        op2 = variables[decoded[3]]
                    else:
                        op2 = decoded[3]

                    # step2: save current state and make new assert condition
                    this_assert = None; before_assert = current_assert
                    if key == 'IFEQUAL':
                        this_assert = '(= ' + op1 + ' ' + op2 + ')'
                    elif key == 'IFNE':
                        this_assert = '(not (= ' + op1 + ' ' + op2 + '))'
                    else:
                        this_assert = '(' + decoded[2] + ' ' + op1 + ' ' + op2 + ')'
                    if current_assert == None:
                        current_assert = '(and ' + this_assert
                    else:
                        current_assert = current_assert + ' ' + this_assert
                    prev_variables = copy.deepcopy(variables)

                    # step3: go branch
                    next_idx = int(re.findall(r'\d+', decoded[5])[0])
                    generate_z3(next_idx)

                    # step4: not go branch(restore previous state)
                    this_assert = '(not ' + this_assert + ')'
                    if before_assert == None:
                        current_assert = '(and ' + this_assert
                    else:
                        current_assert = before_assert + ' ' + this_assert
                    variables = copy.deepcopy(prev_variables)
                break
    generate_z3(label_idx+1)
###############################

# transform java to jimple
generate_jimple()

# read jimple and save instructions of that to my new data structure
with open(jimple_name, 'r') as jimple_stream:
    for line in jimple_stream:

        for key, pattern in patterns:
            if pattern.match(line.strip()):
                if key == 'BEGIN':
                    working = True
                    jimples.append([])
                    break
                elif working:
                    if key == 'LABEL':
                        jimples.append([])
                    elif key == 'DECLARE':
                        for name in [x for x in re.split(' |;|,', line.strip()) if x != 'int' and len(x) > 0]:
                            variables[name] = None
                    elif key == 'DECLAREBYTE':
                        for name in [x for x in re.split(' |;|,', line.strip()) if x != 'byte' and len(x) > 0]:
                            variables[name] = None
                    else:
                        jimples[len(jimples)-1].append(line.strip())
                        if key == 'END':
                            working = False
                    break

# transform jimple to z3 with running it
# if there is a z3 model of assertion, print it and exit program by force
generate_z3(0)
print 'VALID'   # if all unsat
os.system('rm ' + java_name + ' ' + class_name + ' ' + jimple_name + ' ' + z3_name + ' 2> /dev/null')
