from sys import stdout

class SynacoreVM:
    def __init__(self,filename):
        self.filename = filename
        self.oper = {
            0:self.halt,
            6:self.jmp,
            7:self.jt,
            8:self.jf,
            19:self.out,
            21:self.noop
        }
        self.stack = []
        self.memory = []
    def __enter__(self):
        try:
            self.handler = open(self.filename,'rb')
            self.memory.append(self.handler.read(1))
            self.cursor = 1
        except FileNotFoundError:
            print('Could not find file, executing program.')
            #TO ADD: how to execute properly? call __exit__?
        return self
    
    def __exit__(self,typed,value,traceback):
        self.handler.flush()
        self.handler.close()
    
    def read(self, byte):
        self.cursor+=byte
        if len(self.memory)<self.cursor:
            byte = self.cursor-len(self.memory)
            self.memory.extend([int(x) for i,x in enumerate(self.handler.read(byte*2)) if i%2])
        return self.memory[self.cursor-byte:self.cursor]
    
    def execute(self, howMany = 1):
        for _ in range(howMany):
            self.opqueue = self.read(1)
            while self.opqueue[0]:
                try:
                    do_this = self.opqueue.pop(0)
                    self.oper[do_this]()
                except KeyError:
                    print("Could not find operation(%d), exitting program"%do_this)
                    return False
                self.opqueue.append(*self.read(1))
            self.opqueue.clear
            self.cacheSum = len(self.memory)
            stdout.flush()
            return True
    def halt(self):
        '''
        halt: 0
          stop execution and terminate the program
        '''
        pass
    
    def jmp(self):
        '''
        jmp: 6 a
          jump to <a>
        '''
        jmp_to = self.read(1)[0]*8
        self.read((jmp_to-self.cursor,0)[jmp_to-self.cursor<0])
        self.cursor = jmp_to
    
    def jt(self):
        '''
        jt: 7 a b
          if <a> is nonzero, jump to <b>
        '''
        x = self.read(1)[0]
        print(x)
        if x:
            self.jmp()
        else:
            self.read(1)
            
    def jf(self):
        '''
        jf: 8 a b
          if <a> is zero, jump to <b>
        '''
        if not self.read(1)[0]:
            self.jmp()
        else:
            self.read(1)
            
    def out(self):
        '''
        out: 19 a
          write the character represented by ascii code <a> to the terminal       
        '''        
        print(chr(*self.read(1)),end='')
    
    
    def noop(self):
        '''
        noop: 21
          no operation      
        '''
        pass
    

if __name__ == '__main__':
    with SynacoreVM(r'C:\Users\arthurd\Documents\challenge.bin') as vm:
        while input('e to exit: ') != 'e' and vm.execute():
            pass
        
