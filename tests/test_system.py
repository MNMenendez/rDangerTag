# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0
# Simple tests for an dummy module
import os
import random
import sys
from pathlib import Path

import cocotb
from cocotb.runner import get_runner
from cocotb.triggers import Timer, FallingEdge, RisingEdge
from cocotb.types import Bit, Logic
from cocotb.binary import BinaryValue
from cocotb.clock import Clock
from cocotb.handle import Force, Release, Deposit

if cocotb.simulator.is_running():
    from models import *

@cocotb.test()
async def system_states_test(dut):
    """Testing system states"""
    
    # Clock used is the slowest clock -> 31.25 Hz
    clock = Clock(dut.CLOCK, 32, units="ms")  # Create a 32ms period clock on port clk
    cocotb.start_soon(clock.start(start_high = False))  # Start the clock    
    
    counter = 0
    oldMotor = Motors.STOP.value
    for i in range (100000):
        print(f'System test progress: {i/(100000-1):2.1%}\r', end="\r")
        
        reset = True if ((i % 2000) > 50 and (i % 2000) < 100) else False
        dut.CLOCK_STATE.value = not reset  
        if ( i % 50 == 0 ):
            if (random.randint(0 , 99) < 97):
                j = random.randint(1 , 2)
            else:
                j = random.randint(0 , 1)*3
            #print(f'{Commands(j).name}')    
            dut.COMMAND_STATE.value = BinaryValue(value=j,bits=8,bigEndian=False)
        if ( i % 120 == 0 ):
            if (random.randint(0 , 99) < 97):
                k = random.randint(1 , 3)
            else:
                k = 0
            dut.SENSOR_STATE.value = BinaryValue(value=k,bits=8,bigEndian=False)  
            #print(f'{Sensors(k).name}')  
        
        stateERROR  = True if ((k == Sensors.SENSOR_ERROR.value) or (j == Commands.COMMAND_ERROR.value) or (reset != False)) else False
        toBLANK     = True if ((stateERROR == False) and (j == Commands.COMMAND_REMOVE.value) and (k == Sensors.DANGER.value or k == Sensors.TRANSITION.value)) else False
        toDANGER    = True if ((stateERROR == False) and (j == Commands.COMMAND_APPLY.value) and (k == Sensors.BLANK.value or k == Sensors.TRANSITION.value)) else False
        
        if ( k == Sensors.TRANSITION.value ):
            counter += 1
        else:
            counter = 0
        
        #await Timer(15, units="us")  
        await RisingEdge(dut.CLOCK)
        oldMotor = dut.MOTOR_STATE.value
        output = system_model(dut.CLOCK.value, dut.CLOCK_STATE.value, dut.COMMAND_STATE.value, dut.SENSOR_STATE.value,counter,oldMotor)
        #await RisingEdge(dut.CLOCK) 
         
        #print(f'R{1*dut.CLOCK_STATE.value}|{Commands(dut.COMMAND_STATE.value).name}|{Sensors(dut.SENSOR_STATE.value).name}[{counter}] > Py:[{Systems(output[0]).name},{Motors(output[1]).name}] vs VHDL:[{Systems(dut.SYSTEM_STATE.value).name},{Motors(dut.MOTOR_STATE.value).name}]')
        
        #await Timer(15, units="us")  
        #oldMotor = dut.MOTOR_STATE.value
        #output = system_model(dut.CLOCK.value, dut.CLOCK_STATE.value, dut.COMMAND_STATE.value, dut.SENSOR_STATE.value,counter,oldMotor)
        await FallingEdge(dut.CLOCK) 
        assert ([Systems(output[0]).name,Motors(output[1]).name] == [Systems(dut.SYSTEM_STATE.value).name,Motors(dut.MOTOR_STATE.value).name]), f' [{Systems(output[0]).name},{Motors(output[1]).name}] != [{Systems(dut.SYSTEM_STATE.value).name},{Motors(dut.MOTOR_STATE.value).name}]'
        
        #print(f'F{1*dut.CLOCK_STATE.value}|{Commands(dut.COMMAND_STATE.value).name}|{Sensors(dut.SENSOR_STATE.value).name}[{counter}] > Py:[{Systems(output[0]).name},{Motors(output[1]).name}] vs VHDL:[{Systems(dut.SYSTEM_STATE.value).name},{Motors(dut.MOTOR_STATE.value).name}]')
        
        
    print('')
    dut.CLOCK_STATE.value = False
    dut.COMMAND_STATE.value = BinaryValue(value=Commands.COMMAND_IDLE.value,bits=8,bigEndian=False)
    dut.SENSOR_STATE.value = BinaryValue(value=Sensors.DANGER.value,bits=8,bigEndian=False)
    dut.SYSTEM_STATE.value = Deposit(BinaryValue(value=Systems.SYSTEM_IDLE.value,bits=8,bigEndian=False))
    dut.MOTOR_STATE.value = Deposit(BinaryValue(value=Motors.STOP.value,bits=8,bigEndian=False))
    await Timer(100, units="ms")
    
    
def test_system_runner():
    """Simulate the key example using the Python runner.

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
        verilog_sources = [proj_path / "hdl" / "system_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "system_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="system_module",
        always=True,
    )
    runner.test(hdl_toplevel="system_module", test_module="test_system")


if __name__ == "__main__":
    test_system_runner()
