from instructions import Instruction

if __name__ == '__main__':

    with open('input.txt', 'r') as inst_file:
        insts = (Instruction(inst) for inst in inst_file)
        for inst in insts:
            print('{}, {}, {}'.format(inst.op, inst.dest, inst.src))