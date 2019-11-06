from instructions import Instruction
from scoreboard import *

class Processor:
    """
    This class is the top level processor for executing the instructions
    from input.txt

    Attributes:
        fu_list (list(str)): List of functional units in processor
        reg_list (list(str)): List of registers available

        ---Used during program run
        clock_cycles (int): Current clock cycle
        program_finished (bool): Set to True when program is complete
    """

    def __init__(self):
        self.fu_list = ['INTEGER', 'ADD', 'MULT', 'MULT', 'DIV']
        self.reg_list = ['R1', 'R2', 'R3', 'F0', 'F2', 'F4', 'F6', 'F8', 'F10']

        # Status tracking of instruction processing
        self.clock_cycles = 0
        self.program_finished = False

    def run(self, insts):
        scoreboard = Scoreboard(insts, self.fu_list, self.reg_list)

        while not self.program_finished:
            self.clock_cycles += 1
            scoreboard.update(self.clock_cycles)
            self.program_finished = scoreboard.is_prgm_complete()

        print('Program completed in {} clock cycles'.format(self.clock_cycles))
        scoreboard.get_inst_stats()

if __name__ == '__main__':
    with open('input.txt', 'r') as inst_file:
        insts = [Instruction(inst) for inst in inst_file]

    cpu = Processor()
    cpu.run(insts)