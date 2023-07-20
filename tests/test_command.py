# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0
# Simple tests for an dummy module
import os
import random
import sys
from pathlib import Path

import cocotb
from cocotb.runner import get_runner
from cocotb.triggers import Timer
from cocotb.types import Bit, Logic
from cocotb.binary import BinaryValue
from cocotb.handle import Force, Release, Deposit

if cocotb.simulator.is_running():
    from models import *

combinations = [
    {"lock":Locks.LOCK_ERROR,   "key":Keys.KEY_ERROR,  "plc":PLCs.PLC_ERROR,  "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_ERROR,   "key":Keys.KEY_ERROR,  "plc":PLCs.PLC_APPLY,  "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_ERROR,   "key":Keys.KEY_ERROR,  "plc":PLCs.PLC_REMOVE, "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_ERROR,   "key":Keys.KEY_ERROR,  "plc":PLCs.PLC_IDLE,   "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_ERROR,   "key":Keys.KEY_APPLY,  "plc":PLCs.PLC_ERROR,  "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_ERROR,   "key":Keys.KEY_APPLY,  "plc":PLCs.PLC_APPLY,  "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_ERROR,   "key":Keys.KEY_APPLY,  "plc":PLCs.PLC_REMOVE, "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_ERROR,   "key":Keys.KEY_APPLY,  "plc":PLCs.PLC_IDLE,   "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_ERROR,   "key":Keys.KEY_REMOVE, "plc":PLCs.PLC_ERROR,  "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_ERROR,   "key":Keys.KEY_REMOVE, "plc":PLCs.PLC_APPLY,  "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_ERROR,   "key":Keys.KEY_REMOVE, "plc":PLCs.PLC_REMOVE, "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_ERROR,   "key":Keys.KEY_REMOVE, "plc":PLCs.PLC_IDLE,   "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_ERROR,   "key":Keys.NO_KEY,     "plc":PLCs.PLC_ERROR,  "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_ERROR,   "key":Keys.NO_KEY,     "plc":PLCs.PLC_APPLY,  "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_ERROR,   "key":Keys.NO_KEY,     "plc":PLCs.PLC_REMOVE, "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_ERROR,   "key":Keys.NO_KEY,     "plc":PLCs.PLC_IDLE,   "applyValid":False,"removeValid":False,"cmdValid":False},
    
    {"lock":Locks.LOCK_APPLY,   "key":Keys.KEY_ERROR,  "plc":PLCs.PLC_ERROR,  "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_APPLY,   "key":Keys.KEY_ERROR,  "plc":PLCs.PLC_APPLY,  "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_APPLY,   "key":Keys.KEY_ERROR,  "plc":PLCs.PLC_REMOVE, "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_APPLY,   "key":Keys.KEY_ERROR,  "plc":PLCs.PLC_IDLE,   "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_APPLY,   "key":Keys.KEY_APPLY,  "plc":PLCs.PLC_ERROR,  "applyValid":True,"removeValid":False,"cmdValid":True},
    {"lock":Locks.LOCK_APPLY,   "key":Keys.KEY_APPLY,  "plc":PLCs.PLC_APPLY,  "applyValid":True,"removeValid":False,"cmdValid":True},
    {"lock":Locks.LOCK_APPLY,   "key":Keys.KEY_APPLY,  "plc":PLCs.PLC_REMOVE, "applyValid":True,"removeValid":False,"cmdValid":True},
    {"lock":Locks.LOCK_APPLY,   "key":Keys.KEY_APPLY,  "plc":PLCs.PLC_IDLE,   "applyValid":True,"removeValid":False,"cmdValid":True},
    {"lock":Locks.LOCK_APPLY,   "key":Keys.KEY_REMOVE, "plc":PLCs.PLC_ERROR,  "applyValid":False,"removeValid":False,"cmdValid":True},
    {"lock":Locks.LOCK_APPLY,   "key":Keys.KEY_REMOVE, "plc":PLCs.PLC_APPLY,  "applyValid":False,"removeValid":False,"cmdValid":True},
    {"lock":Locks.LOCK_APPLY,   "key":Keys.KEY_REMOVE, "plc":PLCs.PLC_REMOVE, "applyValid":False,"removeValid":False,"cmdValid":True},
    {"lock":Locks.LOCK_APPLY,   "key":Keys.KEY_REMOVE, "plc":PLCs.PLC_IDLE,   "applyValid":False,"removeValid":False,"cmdValid":True},
    {"lock":Locks.LOCK_APPLY,   "key":Keys.NO_KEY,     "plc":PLCs.PLC_ERROR,  "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_APPLY,   "key":Keys.NO_KEY,     "plc":PLCs.PLC_APPLY,  "applyValid":True,"removeValid":False,"cmdValid":True},
    {"lock":Locks.LOCK_APPLY,   "key":Keys.NO_KEY,     "plc":PLCs.PLC_REMOVE, "applyValid":False,"removeValid":False,"cmdValid":True},
    {"lock":Locks.LOCK_APPLY,   "key":Keys.NO_KEY,     "plc":PLCs.PLC_IDLE,   "applyValid":False,"removeValid":False,"cmdValid":True},
    
    {"lock":Locks.LOCK_REMOVE,   "key":Keys.KEY_ERROR, "plc":PLCs.PLC_ERROR,  "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_REMOVE,   "key":Keys.KEY_ERROR, "plc":PLCs.PLC_APPLY,  "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_REMOVE,   "key":Keys.KEY_ERROR, "plc":PLCs.PLC_REMOVE, "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_REMOVE,   "key":Keys.KEY_ERROR, "plc":PLCs.PLC_IDLE,   "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_REMOVE,   "key":Keys.KEY_APPLY, "plc":PLCs.PLC_ERROR,  "applyValid":False,"removeValid":False,"cmdValid":True},
    {"lock":Locks.LOCK_REMOVE,   "key":Keys.KEY_APPLY, "plc":PLCs.PLC_APPLY,  "applyValid":False,"removeValid":False,"cmdValid":True},
    {"lock":Locks.LOCK_REMOVE,   "key":Keys.KEY_APPLY, "plc":PLCs.PLC_REMOVE, "applyValid":False,"removeValid":False,"cmdValid":True},
    {"lock":Locks.LOCK_REMOVE,   "key":Keys.KEY_APPLY, "plc":PLCs.PLC_IDLE,   "applyValid":False,"removeValid":False,"cmdValid":True},
    {"lock":Locks.LOCK_REMOVE,   "key":Keys.KEY_REMOVE,"plc":PLCs.PLC_ERROR,  "applyValid":False,"removeValid":True,"cmdValid":True},
    {"lock":Locks.LOCK_REMOVE,   "key":Keys.KEY_REMOVE,"plc":PLCs.PLC_APPLY,  "applyValid":False,"removeValid":True,"cmdValid":True},
    {"lock":Locks.LOCK_REMOVE,   "key":Keys.KEY_REMOVE,"plc":PLCs.PLC_REMOVE, "applyValid":False,"removeValid":True,"cmdValid":True},
    {"lock":Locks.LOCK_REMOVE,   "key":Keys.KEY_REMOVE,"plc":PLCs.PLC_IDLE,   "applyValid":False,"removeValid":True,"cmdValid":True},
    {"lock":Locks.LOCK_REMOVE,   "key":Keys.NO_KEY,    "plc":PLCs.PLC_ERROR,  "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.LOCK_REMOVE,   "key":Keys.NO_KEY,    "plc":PLCs.PLC_APPLY,  "applyValid":False,"removeValid":False,"cmdValid":True},
    {"lock":Locks.LOCK_REMOVE,   "key":Keys.NO_KEY,    "plc":PLCs.PLC_REMOVE, "applyValid":False,"removeValid":True,"cmdValid":True},
    {"lock":Locks.LOCK_REMOVE,   "key":Keys.NO_KEY,    "plc":PLCs.PLC_IDLE,   "applyValid":False,"removeValid":False,"cmdValid":True},
 
    {"lock":Locks.NO_LOCK,      "key":Keys.KEY_ERROR,  "plc":PLCs.PLC_ERROR,  "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.NO_LOCK,      "key":Keys.KEY_ERROR,  "plc":PLCs.PLC_APPLY,  "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.NO_LOCK,      "key":Keys.KEY_ERROR,  "plc":PLCs.PLC_REMOVE, "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.NO_LOCK,      "key":Keys.KEY_ERROR,  "plc":PLCs.PLC_IDLE,   "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.NO_LOCK,      "key":Keys.KEY_APPLY,  "plc":PLCs.PLC_ERROR,  "applyValid":True,"removeValid":False,"cmdValid":True},
    {"lock":Locks.NO_LOCK,      "key":Keys.KEY_APPLY,  "plc":PLCs.PLC_APPLY,  "applyValid":True,"removeValid":False,"cmdValid":True},
    {"lock":Locks.NO_LOCK,      "key":Keys.KEY_APPLY,  "plc":PLCs.PLC_REMOVE, "applyValid":True,"removeValid":False,"cmdValid":True},
    {"lock":Locks.NO_LOCK,      "key":Keys.KEY_APPLY,  "plc":PLCs.PLC_IDLE,   "applyValid":True,"removeValid":False,"cmdValid":True},
    {"lock":Locks.NO_LOCK,      "key":Keys.KEY_REMOVE, "plc":PLCs.PLC_ERROR,  "applyValid":False,"removeValid":True,"cmdValid":True},
    {"lock":Locks.NO_LOCK,      "key":Keys.KEY_REMOVE, "plc":PLCs.PLC_APPLY,  "applyValid":False,"removeValid":True,"cmdValid":True},
    {"lock":Locks.NO_LOCK,      "key":Keys.KEY_REMOVE, "plc":PLCs.PLC_REMOVE, "applyValid":False,"removeValid":True,"cmdValid":True},
    {"lock":Locks.NO_LOCK,      "key":Keys.KEY_REMOVE, "plc":PLCs.PLC_IDLE,   "applyValid":False,"removeValid":True,"cmdValid":True},
    {"lock":Locks.NO_LOCK,      "key":Keys.NO_KEY,     "plc":PLCs.PLC_ERROR,  "applyValid":False,"removeValid":False,"cmdValid":False},
    {"lock":Locks.NO_LOCK,      "key":Keys.NO_KEY,     "plc":PLCs.PLC_APPLY,  "applyValid":True,"removeValid":False,"cmdValid":True},
    {"lock":Locks.NO_LOCK,      "key":Keys.NO_KEY,     "plc":PLCs.PLC_REMOVE, "applyValid":False,"removeValid":True,"cmdValid":True},
    {"lock":Locks.NO_LOCK,      "key":Keys.NO_KEY,     "plc":PLCs.PLC_IDLE,   "applyValid":False,"removeValid":False,"cmdValid":True}]
   
'''
@cocotb.test()
async def command_info_test(dut):
    """Test commands"""
    
    for combination in combinations:
        print(f'{Locks(combination["lock"]).name}|{Keys(combination["key"]).name}|{PLCs(combination["plc"]).name}--[{1*combination["applyValid"]},{1*combination["removeValid"]},{1*combination["cmdValid"]}]')
    print(f'Possible commands: {len(combinations)}')
    
    validApplies = [x for x in combinations if x["cmdValid"] and x["applyValid"]]
    print(f'Valid apply commands [{len(validApplies)}]')
    #for validApply in validApplies:
    #    print(f'\t{validApply}')
         
    validRemoves = [x for x in combinations if x["cmdValid"] and x["removeValid"]]
    print(f'Valid remove commands [{len(validRemoves)}]')
    #for validRemove in validRemoves:
    #    print(f'\t{validRemove}')
    
    invalidCommands = [x for x in combinations if x["cmdValid"] and not x["applyValid"] and not x["removeValid"]]
    print(f'Invalid commands [{len(invalidCommands)}]')
    #for invalidCommand in invalidCommands:
    #    print(f'\t{invalidCommand}')
 
    errors = [x for x in combinations if not x["cmdValid"]]
    print(f'Error commands [{len(errors)}]')
    #for error in errors:
    #    print(f'\t{error}')
 
    idleToApplyRetain = (1 + len(validApplies)) * len(invalidCommands) * len(validApplies)
    #for validApply in validApplies:
    #    for invalidCommand in invalidCommands:
    #        print(f'{validApplies.index(validApply)} - {invalidCommands.index(invalidCommand)}')
    idleToRemoveRetain = (1 + len(validRemoves))* len(invalidCommands) * len(validRemoves)
    #for validRemove in validRemoves:
    #    for invalidCommand in invalidCommands:
    #        print(f'{validRemoves.index(validRemove)} - {invalidCommands.index(invalidCommand)}')
    idleToApplyRemoveLoop = (1 +  len(validRemoves)) * len(validApplies) 
    idleToRemoveApplyLoop = (1 +  len(validApplies)) * len(validRemoves) 
    
    idleToError = (1 + len(errors)) * len(errors)
    applyToError = (1+1+len(errors)) * len(errors)
    removeToError = (1+1+len(errors)) * len(errors)
    
    totalValid = idleToApplyRetain+idleToRemoveRetain+idleToApplyRemoveLoop+idleToRemoveApplyLoop
    totalError = idleToError + applyToError + removeToError
    
    print(f'idleToApplyRetain:{idleToApplyRetain}\nidletoRemoveRetain:{idleToRemoveRetain}\nidletoApplyRemoveLoop:{idleToApplyRemoveLoop}\nidletoRemoveApplyLoop:{idleToRemoveApplyLoop}\nidleToError:{idleToError}\napplyToError:{applyToError}\nremoveToError:{removeToError}')
    print('---------')
    print(f'totalValid:{totalValid}\ntotalError:{totalError}\ntotal:{totalValid+totalError}')
'''

@cocotb.test()
async def command_idleToApplyRetain_test(dut):
    """Test commands between idle and apply state, retaining apply state"""

    await Timer(1, units="ms") 
    
    prevOutput = Commands.COMMAND_IDLE  
    
    validApplies = [x for x in combinations if x["cmdValid"] and x["applyValid"]]
    validRemoves = [x for x in combinations if x["cmdValid"] and x["removeValid"]]
    invalidCommands = [x for x in combinations if x["cmdValid"] and not x["applyValid"] and not x["removeValid"]]
    errors = [x for x in combinations if not x["cmdValid"]]
    
    for k in invalidCommands:
        for i in validApplies:
            KEY_STATE = validApplies[validApplies.index(i)]["key"]
            LOCK_STATE = validApplies[validApplies.index(i)]["lock"]
            PLC_STATE = validApplies[validApplies.index(i)]["plc"]

            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
            
            await Timer(15, units="us")  
            #print(f'A_{validApplies.index(i)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')
  
            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
            
            for j in validApplies:
                KEY_STATE = validApplies[validApplies.index(j)]["key"]
                LOCK_STATE = validApplies[validApplies.index(j)]["lock"]
                PLC_STATE = validApplies[validApplies.index(j)]["plc"]

                dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
                dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
                dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
                output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
            
                await Timer(15, units="us")  
                #print(f'\tA_{validApplies.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')
      
                assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
                prevOutput = Commands(output)
            
            KEY_STATE = invalidCommands[invalidCommands.index(k)]["key"]
            LOCK_STATE = invalidCommands[invalidCommands.index(k)]["lock"]
            PLC_STATE = invalidCommands[invalidCommands.index(k)]["plc"]
    
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
            
            await Timer(15, units="us")  
            #print(f'I_{invalidCommands.index(k)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')
  
            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
    
    i = random.randint(0 , len(invalidCommands)-1)
    
    KEY_STATE = invalidCommands[i]["key"]
    LOCK_STATE = invalidCommands[i]["lock"]
    PLC_STATE = invalidCommands[i]["plc"]
    
    dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
    dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
    dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
    output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
    
    await Timer(15, units="us")  
    #print(f'I_{i} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

    assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
    prevOutput = Commands(output)
    
@cocotb.test()
async def command_idleToRemoveRetain_test(dut):
    """Test commands between idle and remove state, retaining remove state"""

    await Timer(1, units="ms") 
    
    prevOutput = Commands.COMMAND_IDLE  
    
    validApplies = [x for x in combinations if x["cmdValid"] and x["applyValid"]]
    validRemoves = [x for x in combinations if x["cmdValid"] and x["removeValid"]]
    invalidCommands = [x for x in combinations if x["cmdValid"] and not x["applyValid"] and not x["removeValid"]]
    errors = [x for x in combinations if not x["cmdValid"]]
    
    for k in invalidCommands:
        for i in validRemoves:
            KEY_STATE = validRemoves[validRemoves.index(i)]["key"]
            LOCK_STATE = validRemoves[validRemoves.index(i)]["lock"]
            PLC_STATE = validRemoves[validRemoves.index(i)]["plc"]
            
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
            
            await Timer(15, units="us")  
            #print(f'R_{validRemoves.index(i)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')
  
            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
            
            for j in validRemoves:
                KEY_STATE = validRemoves[validRemoves.index(j)]["key"]
                LOCK_STATE = validRemoves[validRemoves.index(j)]["lock"]
                PLC_STATE = validRemoves[validRemoves.index(j)]["plc"]
                
                dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
                dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
                dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
                output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
            
                await Timer(15, units="us")  
                #print(f'\tR_{validRemoves.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')
      
                assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
                prevOutput = Commands(output)
            
            KEY_STATE = invalidCommands[invalidCommands.index(k)]["key"]
            LOCK_STATE = invalidCommands[invalidCommands.index(k)]["lock"]
            PLC_STATE = invalidCommands[invalidCommands.index(k)]["plc"]
    
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)

            await Timer(15, units="us")  
            #print(f'I_{invalidCommands.index(k)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')
  
            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
            
    i = random.randint(0 , len(invalidCommands)-1)
    
    KEY_STATE = invalidCommands[i]["key"]
    LOCK_STATE = invalidCommands[i]["lock"]
    PLC_STATE = invalidCommands[i]["plc"]
    
    dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
    dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
    dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
    output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
    
    await Timer(15, units="us")  
    #print(f'I_{i} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

    assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
    prevOutput = Commands(output)
    
@cocotb.test()
async def command_idleToApplyRemoveLoop_test(dut):
    """Test commands between idle and apply state then looping with remove state"""

    await Timer(1, units="ms") 
    
    prevOutput = Commands.COMMAND_IDLE  
    
    validApplies = [x for x in combinations if x["cmdValid"] and x["applyValid"]]
    validRemoves = [x for x in combinations if x["cmdValid"] and x["removeValid"]]
    invalidCommands = [x for x in combinations if x["cmdValid"] and not x["applyValid"] and not x["removeValid"]]
    errors = [x for x in combinations if not x["cmdValid"]]

    i = random.randint(0 , len(validApplies)-1)
    
    KEY_STATE = validApplies[i]["key"]
    LOCK_STATE = validApplies[i]["lock"]
    PLC_STATE = validApplies[i]["plc"]
    
    dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
    dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
    dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
    output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
    
    await Timer(15, units="us")  
    #print(f'A_{i} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

    assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
    prevOutput = Commands(output)
            
    for j in validRemoves:
        KEY_STATE = validRemoves[validRemoves.index(j)]["key"]
        LOCK_STATE = validRemoves[validRemoves.index(j)]["lock"]
        PLC_STATE = validRemoves[validRemoves.index(j)]["plc"]
        
        dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
        dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
        dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
        output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
    
        await Timer(15, units="us")  
        #print(f'\tR_{validRemoves.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

        assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
        prevOutput = Commands(output)
        for k in validApplies:
            KEY_STATE = validApplies[validApplies.index(k)]["key"]
            LOCK_STATE = validApplies[validApplies.index(k)]["lock"]
            PLC_STATE = validApplies[validApplies.index(k)]["plc"]
            
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
            
            await Timer(15, units="us")  
            #print(f'\t\tA_{validApplies.index(k)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')
  
            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
            
            KEY_STATE = validRemoves[validRemoves.index(j)]["key"]
            LOCK_STATE = validRemoves[validRemoves.index(j)]["lock"]
            PLC_STATE = validRemoves[validRemoves.index(j)]["plc"]
            
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
        
            await Timer(15, units="us")  
            #print(f'\tR_{validRemoves.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')
  
            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
            
    i = random.randint(0 , len(invalidCommands)-1)
    
    KEY_STATE = invalidCommands[i]["key"]
    LOCK_STATE = invalidCommands[i]["lock"]
    PLC_STATE = invalidCommands[i]["plc"]
    
    dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
    dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
    dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
    output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
    
    await Timer(15, units="us")  
    #print(f'I_{i} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

    assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
    prevOutput = Commands(output)
    
@cocotb.test()
async def command_idleToRemoveApplyLoop_test(dut):
    """Test commands between idle and remove state then looping with apply state"""

    await Timer(1, units="ms") 
    
    prevOutput = Commands.COMMAND_IDLE  
    
    validApplies = [x for x in combinations if x["cmdValid"] and x["applyValid"]]
    validRemoves = [x for x in combinations if x["cmdValid"] and x["removeValid"]]
    invalidCommands = [x for x in combinations if x["cmdValid"] and not x["applyValid"] and not x["removeValid"]]
    errors = [x for x in combinations if not x["cmdValid"]]
    
    i = random.randint(0 , len(validRemoves)-1)
    
    KEY_STATE = validRemoves[i]["key"]
    LOCK_STATE = validRemoves[i]["lock"]
    PLC_STATE = validRemoves[i]["plc"]
    
    dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
    dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
    dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
    output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
    
    await Timer(15, units="us")  
    #print(f'R_{i} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

    assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
    prevOutput = Commands(output)
            
    for j in validApplies:
        KEY_STATE = validApplies[validApplies.index(j)]["key"]
        LOCK_STATE = validApplies[validApplies.index(j)]["lock"]
        PLC_STATE = validApplies[validApplies.index(j)]["plc"]
        
        dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
        dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
        dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
        output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
    
        await Timer(15, units="us")  
        #print(f'\tA_{validApplies.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

        assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
        prevOutput = Commands(output)
        for k in validRemoves:
            KEY_STATE = validRemoves[validRemoves.index(k)]["key"]
            LOCK_STATE = validRemoves[validRemoves.index(k)]["lock"]
            PLC_STATE = validRemoves[validRemoves.index(k)]["plc"]
            
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
            
            await Timer(15, units="us")  
            #print(f'\t\tR_{validRemoves.index(k)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')
  
            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
            
            KEY_STATE = validApplies[validApplies.index(j)]["key"]
            LOCK_STATE = validApplies[validApplies.index(j)]["lock"]
            PLC_STATE = validApplies[validApplies.index(j)]["plc"]
            
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
        
            await Timer(15, units="us")  
            #print(f'\tA_{validApplies.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')
  
            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
            
    i = random.randint(0 , len(invalidCommands)-1)
    
    KEY_STATE = invalidCommands[i]["key"]
    LOCK_STATE = invalidCommands[i]["lock"]
    PLC_STATE = invalidCommands[i]["plc"]
    
    dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
    dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
    dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
    output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
    
    await Timer(15, units="us")  
    #print(f'I_{i} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

    assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
    prevOutput = Commands(output)
 
@cocotb.test()
async def command_idleToErrorRetain_test(dut):
    """Test commands between idle and error state then retaining error state"""

    await Timer(1, units="ms") 
    
    prevOutput = Commands.COMMAND_IDLE  
    
    validApplies = [x for x in combinations if x["cmdValid"] and x["applyValid"]]
    validRemoves = [x for x in combinations if x["cmdValid"] and x["removeValid"]]
    invalidCommands = [x for x in combinations if x["cmdValid"] and not x["applyValid"] and not x["removeValid"]]
    errors = [x for x in combinations if not x["cmdValid"]]
           
    for i in errors:
        dut.COMMAND_STATE.value = Release()
        dut.COMMAND_SIGNAL.value = Release()
        
        KEY_STATE = errors[errors.index(i)]["key"]
        LOCK_STATE = errors[errors.index(i)]["lock"]
        PLC_STATE = errors[errors.index(i)]["plc"]
        
        dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
        dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
        dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
        output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
    
        await Timer(15, units="us")  
        #print(f'\E_{errors.index(i)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

        assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
        prevOutput = Commands(output)
         
        for j in validApplies:
            KEY_STATE = validApplies[validApplies.index(j)]["key"]
            LOCK_STATE = validApplies[validApplies.index(j)]["lock"]
            PLC_STATE = validApplies[validApplies.index(j)]["plc"]
            
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
        
            await Timer(15, units="us")  
            #print(f'\tA_{validApplies.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
         
        for j in validRemoves:
            KEY_STATE = validRemoves[validRemoves.index(j)]["key"]
            LOCK_STATE = validRemoves[validRemoves.index(j)]["lock"]
            PLC_STATE = validRemoves[validRemoves.index(j)]["plc"]
            
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
        
            await Timer(15, units="us")  
            #print(f'\tR_{validRemoves.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
            
        for j in invalidCommands:
            KEY_STATE = invalidCommands[invalidCommands.index(j)]["key"]
            LOCK_STATE = invalidCommands[invalidCommands.index(j)]["lock"]
            PLC_STATE = invalidCommands[invalidCommands.index(j)]["plc"]
            
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
        
            await Timer(15, units="us")  
            #print(f'\tI_{invalidCommands.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
            
        for j in errors:
            KEY_STATE = errors[errors.index(j)]["key"]
            LOCK_STATE = errors[errors.index(j)]["lock"]
            PLC_STATE = errors[errors.index(j)]["plc"]
            
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
        
            await Timer(15, units="us")  
            #print(f'\tE_{errors.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
        
        i = random.randint(0 , len(invalidCommands)-1)
        
        KEY_STATE = invalidCommands[i]["key"]
        LOCK_STATE = invalidCommands[i]["lock"]
        PLC_STATE = invalidCommands[i]["plc"]
        
        dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
        dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
        dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
        
        dut.COMMAND_STATE.value = Force(BinaryValue(value=Commands.COMMAND_IDLE.value,bits=8,bigEndian=False))
        dut.COMMAND_SIGNAL.value = Force(BinaryValue(value=Commands.COMMAND_IDLE.value,bits=8,bigEndian=False))
        prevOutput = Commands.COMMAND_IDLE
        
        output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
        
        await Timer(15, units="us")  
        #print(f'I_{i} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

        assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
        prevOutput = Commands(output)
    
        await Timer(100, units="us")
    
    dut.COMMAND_STATE.value = Release()
    dut.COMMAND_SIGNAL.value = Release()
    
@cocotb.test()
async def command_applyToErrorRetain_test(dut):
    """Test commands between apply and error state then retaining error state"""
    
    await Timer(1, units="ms") 
    
    prevOutput = Commands.COMMAND_IDLE  
    
    validApplies = [x for x in combinations if x["cmdValid"] and x["applyValid"]]
    validRemoves = [x for x in combinations if x["cmdValid"] and x["removeValid"]]
    invalidCommands = [x for x in combinations if x["cmdValid"] and not x["applyValid"] and not x["removeValid"]]
    errors = [x for x in combinations if not x["cmdValid"]]
    
    i = random.randint(0 , len(validApplies)-1)
    
    KEY_STATE = validApplies[i]["key"]
    LOCK_STATE = validApplies[i]["lock"]
    PLC_STATE = validApplies[i]["plc"]
    
    dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
    dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
    dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
    dut.COMMAND_STATE.value = Deposit(BinaryValue(value=Commands.COMMAND_APPLY.value,bits=8,bigEndian=False))
    dut.COMMAND_SIGNAL.value = Deposit(BinaryValue(value=Commands.COMMAND_APPLY.value,bits=8,bigEndian=False))
    
    output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
    
    await Timer(15, units="us")  
    #print(f'A_{i} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

    assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
    prevOutput = Commands(output)
        
    for i in errors:
        dut.COMMAND_STATE.value = Release()
        dut.COMMAND_SIGNAL.value = Release()
        
        KEY_STATE = errors[errors.index(i)]["key"]
        LOCK_STATE = errors[errors.index(i)]["lock"]
        PLC_STATE = errors[errors.index(i)]["plc"]
        
        dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
        dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
        dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
        output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
    
        await Timer(15, units="us")  
        #print(f'\E_{errors.index(i)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

        assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
        prevOutput = Commands(output)
        
        for j in validApplies:
            KEY_STATE = validApplies[validApplies.index(j)]["key"]
            LOCK_STATE = validApplies[validApplies.index(j)]["lock"]
            PLC_STATE = validApplies[validApplies.index(j)]["plc"]
            
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
        
            await Timer(15, units="us")  
            #print(f'\tA_{validApplies.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
         
        for j in validRemoves:
            KEY_STATE = validRemoves[validRemoves.index(j)]["key"]
            LOCK_STATE = validRemoves[validRemoves.index(j)]["lock"]
            PLC_STATE = validRemoves[validRemoves.index(j)]["plc"]
            
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
        
            await Timer(15, units="us")  
            #print(f'\tR_{validRemoves.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
            
        for j in invalidCommands:
            KEY_STATE = invalidCommands[invalidCommands.index(j)]["key"]
            LOCK_STATE = invalidCommands[invalidCommands.index(j)]["lock"]
            PLC_STATE = invalidCommands[invalidCommands.index(j)]["plc"]
            
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
        
            await Timer(15, units="us")  
            #print(f'\tI_{invalidCommands.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
            
        for j in errors:
            KEY_STATE = errors[errors.index(j)]["key"]
            LOCK_STATE = errors[errors.index(j)]["lock"]
            PLC_STATE = errors[errors.index(j)]["plc"]
            
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
        
            await Timer(15, units="us")  
            #print(f'\tE_{errors.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
        
        i = random.randint(0 , len(validApplies)-1)
        
        KEY_STATE = validApplies[i]["key"]
        LOCK_STATE = validApplies[i]["lock"]
        PLC_STATE = validApplies[i]["plc"]
        
        dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
        dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
        dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
        
        dut.COMMAND_STATE.value = Force(BinaryValue(value=Commands.COMMAND_APPLY.value,bits=8,bigEndian=False))
        dut.COMMAND_SIGNAL.value = Force(BinaryValue(value=Commands.COMMAND_APPLY.value,bits=8,bigEndian=False))
        prevOutput = Commands.COMMAND_APPLY
        
        output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
        
        await Timer(15, units="us")  
        #print(f'A_{i} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

        assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
        prevOutput = Commands(output)
    
        await Timer(100, units="us")
    i = random.randint(0 , len(validApplies)-1)
        
    KEY_STATE = invalidCommands[i]["key"]
    LOCK_STATE = invalidCommands[i]["lock"]
    PLC_STATE = invalidCommands[i]["plc"]
    
    dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
    dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
    dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
    
    dut.COMMAND_STATE.value = Force(BinaryValue(value=Commands.COMMAND_IDLE.value,bits=8,bigEndian=False))
    dut.COMMAND_SIGNAL.value = Force(BinaryValue(value=Commands.COMMAND_IDLE.value,bits=8,bigEndian=False))
    prevOutput = Commands.COMMAND_IDLE
    
    output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
    
    await Timer(15, units="us")  
    #print(f'I_{i} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

    assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
    prevOutput = Commands(output)

    await Timer(100, units="us")
    dut.COMMAND_STATE.value = Release()
    dut.COMMAND_SIGNAL.value = Release()

@cocotb.test()
async def command_removeToErrorRetain_test(dut):
    """Test commands between remove and error state then retaining error state"""
    
    await Timer(1, units="ms") 
    
    prevOutput = Commands.COMMAND_IDLE  
    
    validApplies = [x for x in combinations if x["cmdValid"] and x["applyValid"]]
    validRemoves = [x for x in combinations if x["cmdValid"] and x["removeValid"]]
    invalidCommands = [x for x in combinations if x["cmdValid"] and not x["applyValid"] and not x["removeValid"]]
    errors = [x for x in combinations if not x["cmdValid"]]
    
    i = random.randint(0 , len(validRemoves)-1)
    
    KEY_STATE = validRemoves[i]["key"]
    LOCK_STATE = validRemoves[i]["lock"]
    PLC_STATE = validRemoves[i]["plc"]
    
    dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
    dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
    dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
    dut.COMMAND_STATE.value = Deposit(BinaryValue(value=Commands.COMMAND_REMOVE.value,bits=8,bigEndian=False))
    dut.COMMAND_SIGNAL.value = Deposit(BinaryValue(value=Commands.COMMAND_REMOVE.value,bits=8,bigEndian=False))
    
    output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
    
    await Timer(15, units="us")  
    #print(f'R_{i} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

    assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
    prevOutput = Commands(output)
        
    for i in errors:
        dut.COMMAND_STATE.value = Release()
        dut.COMMAND_SIGNAL.value = Release()
        
        KEY_STATE = errors[errors.index(i)]["key"]
        LOCK_STATE = errors[errors.index(i)]["lock"]
        PLC_STATE = errors[errors.index(i)]["plc"]
        
        dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
        dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
        dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
        output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
    
        await Timer(15, units="us")  
        #print(f'\E_{errors.index(i)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

        assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
        prevOutput = Commands(output)
        
        for j in validApplies:
            KEY_STATE = validApplies[validApplies.index(j)]["key"]
            LOCK_STATE = validApplies[validApplies.index(j)]["lock"]
            PLC_STATE = validApplies[validApplies.index(j)]["plc"]
            
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
        
            await Timer(15, units="us")  
            #print(f'\tA_{validApplies.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
         
        for j in validRemoves:
            KEY_STATE = validRemoves[validRemoves.index(j)]["key"]
            LOCK_STATE = validRemoves[validRemoves.index(j)]["lock"]
            PLC_STATE = validRemoves[validRemoves.index(j)]["plc"]
            
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
        
            await Timer(15, units="us")  
            #print(f'\tR_{validRemoves.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
            
        for j in invalidCommands:
            KEY_STATE = invalidCommands[invalidCommands.index(j)]["key"]
            LOCK_STATE = invalidCommands[invalidCommands.index(j)]["lock"]
            PLC_STATE = invalidCommands[invalidCommands.index(j)]["plc"]
            
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
        
            await Timer(15, units="us")  
            #print(f'\tI_{invalidCommands.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
            
        for j in errors:
            KEY_STATE = errors[errors.index(j)]["key"]
            LOCK_STATE = errors[errors.index(j)]["lock"]
            PLC_STATE = errors[errors.index(j)]["plc"]
            
            dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
            dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
            dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
            output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
        
            await Timer(15, units="us")  
            #print(f'\tE_{errors.index(j)} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

            assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
            prevOutput = Commands(output)
        
        i = random.randint(0 , len(validRemoves)-1)
        
        KEY_STATE = validRemoves[i]["key"]
        LOCK_STATE = validRemoves[i]["lock"]
        PLC_STATE = validRemoves[i]["plc"]
        
        dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
        dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
        dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
        
        dut.COMMAND_STATE.value = Force(BinaryValue(value=Commands.COMMAND_REMOVE.value,bits=8,bigEndian=False))
        dut.COMMAND_SIGNAL.value = Force(BinaryValue(value=Commands.COMMAND_REMOVE.value,bits=8,bigEndian=False))
        prevOutput = Commands.COMMAND_APPLY
        
        output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
        
        await Timer(15, units="us")  
        #print(f'R_{i} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

        assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
        prevOutput = Commands(output)
    
        await Timer(100, units="us")
        
    i = random.randint(0 , len(invalidCommands)-1)
        
    KEY_STATE = invalidCommands[i]["key"]
    LOCK_STATE = invalidCommands[i]["lock"]
    PLC_STATE = invalidCommands[i]["plc"]
    
    dut.KEY_STATE.value = BinaryValue(value=KEY_STATE.value,bits=8,bigEndian=False)
    dut.PLC_STATE.value = BinaryValue(value=PLC_STATE.value,bits=8,bigEndian=False)
    dut.LOCK_STATE.value = BinaryValue(value=LOCK_STATE.value,bits=8,bigEndian=False)
    
    dut.COMMAND_STATE.value = Force(BinaryValue(value=Commands.COMMAND_IDLE.value,bits=8,bigEndian=False))
    dut.COMMAND_SIGNAL.value = Force(BinaryValue(value=Commands.COMMAND_IDLE.value,bits=8,bigEndian=False))
    prevOutput = Commands.COMMAND_IDLE
    
    output = command_model(KEY_STATE,PLC_STATE,LOCK_STATE,prevOutput)
    
    await Timer(15, units="us")  
    #print(f'I_{i} --> {KEY_STATE},{LOCK_STATE},{PLC_STATE} ==> Py:{Commands(output).name} vs VHDL:{Commands(dut.COMMAND_STATE.value).name}')

    assert ( dut.COMMAND_STATE.value == output ), f'Py:{Commands(output).name} != VHDL:{Commands(dut.COMMAND_STATE.value).name}' 
    prevOutput = Commands(output)

def test_command_runner():
    """Simulate the commands using the Python runner.

    This file can be run directly or via pytest discovery.
    """
    hdl_toplevel_lang = os.getenv("HDL_TOPLEVEL_LANG", "verilog")
    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent.parent
    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "model"))

    verilog_sources = []
    vhdl_sources = []

    if hdl_toplevel_lang == "verilog":
        verilog_sources = [proj_path / "hdl" / "command_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "command_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="command_module",
        always=True,
    )
    runner.test(hdl_toplevel="command_module", test_module="test_command")

    

if __name__ == "__main__":
    test_command_runner()
    
