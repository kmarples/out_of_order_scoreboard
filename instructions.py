import re

_op_dict = {
    'LD':{ 
        'ex_cycs' : 1, 
        'format'  : 'IMM',
        'fu'      : 'INTEGER'
        },
    'ADD.D':{ 
        'ex_cycs' : 2, 
        'format'  : 'REG',
        'fu'      : 'ADD'
        },
    'SUB.D':{ 
        'ex_cycs' : 2, 
        'format'  : 'REG',
        'fu'      : 'ADD'
        },
    'MUL.D':{ 
        'ex_cycs' : 10, 
        'format'  : 'REG',
        'fu'      : 'MULT'
        },
    'DIV.D':{ 
        'ex_cycs' : 40, 
        'format'  : 'REG',
        'fu'      : 'DIVIDE'
        }
    }

class Instruction(object):
    """ This class carries the basic information for an input instruction 

        Attributes:
            inst (str): Raw string of the instruction
    """

    def __init__(self, inst):
        """ Creates an instance of Instruction 

        Arguments:
            inst (str): a raw string representing a single instruction
        """

        self.inst_str = inst.strip('\n')

        # Get instruction operation from inst string
        tmp_list = re.split('[() ]', inst)
        inst_list = list(map(lambda x: x.strip(',\n'), filter(lambda x: x != '', tmp_list) ))
        self.op, self.dst = inst_list[0], inst_list[1]

        # Get the format for the instruction
        try:
            inst_fmt = _op_dict[self.op]['format']
        except:
            raise KeyError("Error: Unknown instruction")

        if inst_fmt == 'IMM':       # Example: LD F6 34 R2
            self.src = [inst_list[3]]
        else:                       # Example: ADD.D F2 F1 F3
            self.src = [inst_list[2], inst_list[3]]

        self.num_cycles = _op_dict[self.op]['ex_cycs']
        self.fu = _op_dict[self.op]['fu']

    def __repr__(self):
        return self.inst_str


    @classmethod
    def get_raw_hazards(cls, inst_seq: list):
        """
        This method finds RAW hazards in a sequence of Instruction objects

        Arguments: 
            inst_seq (list): A list of Instruction objects in order of intended execution

        Returns:
            List of tuples of the form - ((index, <write Instruction>), (index, <dependent Instruction>))
        """
        raw_hazards = []
        for i, inst in enumerate(inst_seq):
            dst_reg = inst.dst
            for j, inst2 in enumerate(inst_seq):
                if j > i:
                    req_safe_cycles = inst.num_cycles + 3
                    if dst_reg in inst2.src and i+j < req_safe_cycles:
                        raw_hazards.append( ((i,inst), (j, inst2)) )
        return raw_hazards



if __name__ == '__main__':
    pass
