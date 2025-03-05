import os
from ghidra.app.decompiler import DecompInterface # type: ignore
from ghidra.util.task import ConsoleTaskMonitor # type: ignore

class Log():
    file_path = './logs/'

    def __init__(self, binary_name):
        self.binary_name = binary_name
        self.file_name = '{}{}.log'.format(self.file_path, str(self.binary_name))
        if os.path.exists(self.file_name):
            os.remove(self.file_path)
        self.file = open(self.file_name, "w+")
        self.file.write('[*] binary Name : ' + str(self.binary_name) + '\n\n')

    def log(self, message):
        self.file.write(message + '\n')

    def close(self):
        self.file.close()

    def loggingFunction(self, function_name, decompile_info):
        self.log("---------------- [*] Function : "+str(function_name) + " ----------------")
        self.log(decompile_info)


class Ghidra():
    def __init__(self):
        self.program = currentProgram # type: ignore
        self.decomp_interface = DecompInterface()
        self.decomp_interface.openProgram(self.program)
        self.program_name = self.program.getName()
        self.functions = self.program.getFunctionManager().getFunctions(True)

    def getProgramName(self):
        return self.program_name
    
    def getFunctions(self):
        return self.functions
    
    def decompileFunctions(self, function):
        tokengrp = self.decomp_interface.decompileFunction(function, 0, ConsoleTaskMonitor())
        decompile_func = tokengrp.getDecompiledFunction().getC()
        return decompile_func

    def calledFunctions(self, function):
        callingFuncs = function.getCalledFunctions(self.monitor)
        return callingFuncs

def main():
    ghidra = Ghidra()
    program_name = ghidra.getProgramName()

    log = Log(program_name)

    for function in ghidra.getFunctions():
        decompile_func = ghidra.decompileFunctions(function)
        log.loggingFunction(function, decompile_func)
    
    log.close()
        
if __name__ == '__main__':
    main()