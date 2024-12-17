import re

class ProgramState:
    def __init__(self, regA, regB, regC):
        self.regA = int(regA)
        self.regB = int(regB)
        self.regC = int(regC)
        self.res = []
    
    def setA(self, n):
        self.regA = n
    
    def setB(self, n):
        self.regB = n
    
    def setC(self, n):
        self.regC = n
    
    def get_register_value(self, op):
        LITERAL = {0, 1, 2, 3}
        if op in LITERAL:
            return op
        elif op == 4:
            return self.regA
        elif op == 5:
            return self.regB
        elif op == 6:
            return self.regC
        return 0
    
    def adv(self, op):
        self.regA = int(self.regA / (2 ** self.get_register_value(op)))
    
    def bxl(self, op):
        self.regB = self.regB ^ op
    
    def bst(self, op):
        self.regB = self.get_register_value(op) % 8
    
    def jnz(self, ip, op):
        return op if self.regA != 0 else ip + 1
    
    def bxc(self):
        self.regB = self.regB ^ self.regC
    
    def out(self, op):
        self.res.append(str(self.get_register_value(op) % 8))
    
    def bdv(self, op):
        self.regB = int(self.regA / (2 ** self.get_register_value(op)))
    
    def cdv(self, op):
        self.regC = int(self.regA / (2 ** self.get_register_value(op)))
    
    def call_instruction(self, opcode, operand, ip):
        if opcode == 0:
            self.adv(operand)
        elif opcode == 1:
            self.bxl(operand)
        elif opcode == 2:
            self.bst(operand)
        elif opcode == 3:
            return self.jnz(ip, operand)
        elif opcode == 4:
            self.bxc()
        elif opcode == 5:
            self.out(operand)
        elif opcode == 6:
            self.bdv(operand)
        elif opcode == 7:
            self.cdv(operand)
        return ip + 1

filename = 'day17.txt'

with open(filename, 'r') as file:
    content = file.read()

pattern = re.compile(
    r'Register A:\s*(\d+)\s*'
    r'Register B:\s*(\d+)\s*'
    r'Register C:\s*(\d+)\s*'
    r'Program:\s*((?:\d+,)*\d+)',
    re.IGNORECASE | re.MULTILINE
)

matches = pattern.findall(content)

regA, regB, regC = matches[0][0], matches[0][1], matches[0][2]
p = matches[0][3]

program = []
for i in range(2, len(p), 4):
    program.append((int(p[i-2]), int(p[i])))
    
state = ProgramState(regA, regB, regC)

ip = 0
while ip < len(program):
    ip = state.call_instruction(program[ip][0], program[ip][1], ip)

print(f"Part 1: {",".join(state.res)}")

##########################
######### Part 2 #########
##########################

goal = [int(i) for i in p.split(",")]

def solve(goal, n=0, d=15):
    res = [1E20]
    if d == -1:
        return n
    for i in range(8):
        nn = n + i * (8 ** d)
        new_state = ProgramState(nn, 0, 0)

        ip = 0
        while ip < len(program):
            ip = new_state.call_instruction(program[ip][0], program[ip][1], ip)
        
        if len(new_state.res) != len(goal):
            continue
        if new_state.res[d] == str(goal[d]):
            candidate = solve(goal, nn, d - 1)
            res.append(candidate)
    return min(res)

print(f"Part 2: {solve(goal)}")


# F if you tried to brute force (like me)
