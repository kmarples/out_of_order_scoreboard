class Scoreboard:
    """ This class implements a simple out-of-order scoreboard for executing
        processor instructions  

        Attributes:
            
    """
    __instance = None


    @staticmethod
    def get_instnace():
        if Scoreboard.__instance == None:
            Scoreboard()
        return Scoreboard.__instance

    def __init__(self, inst_seq):
        if Scoreboard.__instance != None:
            raise Exception('There can only be one scoreboard!')
        else:
            Scoreboard.__instance = self
            self.name = 'Out of Order Scoreboard'

            self.inst_seq = inst_seq

            self.func_units = {
                               'INTEGER': [None], 
                               'ADD':     [None], 
                               'MULT':    [None, None], 
                               'DIVIDE':  [None]
                              }

            # TODO: Attach to each instruction - instruction status, flags indicating when
            #       functional units are ready and not ready (Set to NO after operands are read)

    def __str__(self): 
        return self.name

    



if __name__ == '__main__':
    pass
