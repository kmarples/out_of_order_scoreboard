from collections import namedtuple
from collections import OrderedDict

InstStatus = namedtuple('InstStatus',  [
    'inst', 
    'issue', 
    'rd_opd', 
    'execute', 
    'write',
])

class Scoreboard:
    """ 
    This class implements a simple out-of-order scoreboard for
    dynamic scheduling of instructions

    Attributes:
        name (str): Name of scoreboard
        inst_seq (list(<Instruction>)): List of instructions in order to be executed
        pc (int): Acts as the program counter and points to an index of inst_seq
        func_units (list(<FuncUnit>)): Available functional units and associated flags
        pipeline_status (dict): Shows instruction status during processing
        stalled (bool): Set to True if pipeline is stalled
    """

    __instance = None

    @staticmethod
    def get_instnace():
        if Scoreboard.__instance is None:
            Scoreboard()
        return Scoreboard.__instance

    def __init__(self, inst_seq, fu_list, reg_list):
        if Scoreboard.__instance is not None:
            raise Exception('There can only be one scoreboard!')
        else:
            Scoreboard.__instance = self
            self.name = 'Out of Order Scoreboard'

            self.inst_seq = inst_seq
            self.pc = 0
            self.func_units = [FuncUnit(fu) for fu in fu_list]

            # Dict of registers from processor corresponds to FU that will produce the result
            # to be written where <key,value> = <register, FU name>
            self.regs = dict.fromkeys(reg_list, '-')

            self.pipeline = {
            'IS' : None,
            'RO' : None,
            'EX' : None,
            'WR' : None,
            }

            self.inst_stats = OrderedDict()
            for inst in self.inst_seq:
                self.inst_stats[inst.inst_str] = {'is': 0, 'ro': 0, 'ex': 0, 'wr': 0}

            self.stalled = False

    def __str__(self): 
        return self.name

    def get_fu_stats(self):
        fu_stats = [fu.get_status() for fu in self.func_units]
        table_row = '|{:^6}|{:^7}|{:^7}|{:^7}|{:^5}|{:^10}|{:^10}|{:^13}|{:^13}|'
        title = table_row.format('Busy', 'Op', 'Src A', 
            'Src B', 'Dst', 'Src A FU', 'Src B FU', 'Src A Ready', 'Src B Ready')

        print(title)
        for fu in fu_stats:
            print(table_row.format(*fu))

    def get_reg_stats(self):
        table_row = '|{:^9}'*len(self.regs) + '|'
        title = table_row.format(*self.regs)
        status = table_row.format(*self.regs.values())
        print('{}\n{}'.format(title, status))

    def get_inst_stats(self):
        table_row = '|{:^23}|{:^7}|{:^9}|{:^9}|{:^8}|'
        title_u = table_row.format('', '', 'Read', '', 'Write')
        title_l = table_row.format('Instruction', 'Issue', 'Operand', 'Execute', 'Result')

        print('{}\n{}'.format(title_u, title_l))
        for inst, stat in self.inst_stats.items():
            print(table_row.format(inst, *stat.values()))

    def is_prgm_complete(self):
        return True

    def update(self, clock_cycle):
        # Perform instructions in reverse so the upcoming
        # pipeline stage is 'freed' before the next instruction
        # is queued up
        if not self.pipeline['WR']:
            # Move instruction from EX to WR
            self.pipeline['WR'] = self.pipeline['EX']
            self.pipeline['EX'] = None

        if not self.pipeline['EX']:
            # Move instruction from RO to EX
            self.pipeline['EX'] = self.pipeline['RO']
            self.pipeline['RO'] = None

        if not self.pipeline['RO']:
            # Move instruction from IS to RO
            self.pipeline['RO'] = self.pipeline['IS']
            self.pipeline['IS'] = None

        if not self.pipeline['IS']:
            # Issue the next instruction
            self.pipeline['IS'] = self._issue_next(clock_cycle)

    def _issue_next(self, clock_cycle):
        next_inst = self.inst_seq[self.pc]

        # Check if FU is available
        fu = self._get_func_unit(next_inst.fu)
        if fu.busy:
            self.stalled = True
            return False
        else:
            self.inst_stats[next_inst.inst_str]['is'] = clock_cycle

            fu.busy = True
            fu.op = next_inst.op
            fu.dst_reg = next_inst.dst
            for i in range(2):
                fu.src_regs[i] = next_inst.src[i]
                fu.src_flags[i] = True if next_inst.src[i] != '-' else False

            self.regs[next_inst.dst] = fu.name
            self.pc += 1
            return True

    def _get_func_unit(self, func_unit):
        for fu in self.func_units:
            if fu.name == func_unit:
                return fu
        raise Exception('func_unit not in self.func_units')


FuncUnitStatus = namedtuple('FuncUnitStatus',  [
    'busy', 
    'op', 
    'srca', 
    'srcb', 
    'dst',
    'srca_fu', 
    'srcb_fu', 
    'srca_ready', 
    'srcb_ready'
])

class FuncUnit:
    """
    This class stores all registers and flags associated with a
    functional unit

    Attributes:
        name (str): Name of the functional unit
        busy (bool): Busy flag indicating whether unit is in use
        op (str): Operation to perform in the unit
        src_regs (list(str)): Source reigsters
        dst_reg (str): Destination register
        src_fus (list(str)): Functional units producting values in source registers
        fu_flags (list(bool)): Flags indicating when corresponding (by list index) 
            FUs to source registers are ready and not yet read
            Set to False after operands are read
    """

    def __init__(self, name):
        self.name = name
        self.busy = False
        self.op = '-'
        self.src_regs = ['-', '-']
        self.dst_reg = '-'
        self.src_fus = ['-', '-']
        self.src_flags = [False, False]

    def __str__(self):
        return 'Scoreboard - Functional Unit: {}'.format(self.name)


    def get_status(self):
        return FuncUnitStatus(self.busy, self.op,
                              self.src_regs[0], self.src_regs[1], self.dst_reg,
                              self.src_fus[0], self.src_fus[1],
                              self.src_flags[0], self.src_flags[1])


if __name__ == '__main__':
    pass