from instructions import Instruction
from scoreboard import Scoreboard

if __name__ == '__main__':

    with open('input.txt', 'r') as inst_file:
        insts = [Instruction(inst) for inst in inst_file]

        scoreboard = Scoreboard(insts)