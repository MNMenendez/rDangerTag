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

if cocotb.simulator.is_running():
    from models import *

@cocotb.test()
async def system_states_test(dut):
    """Testing system states"""
    
    # Clock used is the slowest clock -> 31.25 Hz
    clock = Clock(dut.CLOCK, 32, units="ms")  # Create a 32ms period clock on port clk
    cocotb.start_soon(clock.start(start_high = False))  # Start the clock    
    
    for i in range (10000):
        print(f'System test progress: {i/(10000-1):2.1%}\r', end="\r")
        
        reset = True if ((i % 2000) > 50 and (i % 2000) < 100) else False
        dut.CLOCK_STATE.value = not reset  
        if ( i % 30 == 0 ):
            j = random.randint(0 , 3)
            dut.COMMAND_STATE.value = BinaryValue(value=j,bits=8,bigEndian=False)
        if ( i % 100 == 0 ):
            k = random.randint(0 , 3)
            dut.SENSOR_STATE.value = BinaryValue(value=k,bits=8,bigEndian=False)  
        
        await FallingEdge(dut.CLOCK)
               
        await RisingEdge(dut.CLOCK) 
        
    
    '''
    aux              =   tuple_create(7,2**6)+(False,)
    POWER_STATE      =   tuple(x.value for x in Powers)
    MODE_STATE       =   tuple(x.value for x in Modes)
    COMMAND_STATE    =   tuple(x.value for x in Commands)
    SENSOR_STATE     =   tuple(x.value for x in Sensors)

    message_old = ''
    message_new = ''
    for i in range(len(aux)):
        dut.POWER_SIGNAL.value = BinaryValue(value=POWER_STATE[(i//64)%2],bits=8,bigEndian=False)
        dut.MODE_SIGNAL.value = BinaryValue(value=MODE_STATE[(i//16)%4],bits=8,bigEndian=False)
        dut.COMMAND_SIGNAL.value = BinaryValue(value=COMMAND_STATE[(i//4)%4],bits=8,bigEndian=False)
        dut.SENSOR_SIGNAL.value = BinaryValue(value=SENSOR_STATE[(i//1)%4],bits=8,bigEndian=False)
        await Timer(1, units="ns")
        
        message_new = f'{Powers(dut.POWER_SIGNAL.value).name}|{Modes(dut.MODE_SIGNAL.value).name}|{Commands(dut.COMMAND_SIGNAL.value).name}|{Sensors(dut.SENSOR_SIGNAL.value).name} > [{Systems(system_model(dut.POWER_SIGNAL.value,dut.MODE_SIGNAL.value,dut.COMMAND_SIGNAL.value,dut.SENSOR_SIGNAL.value)[0]).name},{Rights(system_model(dut.POWER_SIGNAL.value,dut.MODE_SIGNAL.value,dut.COMMAND_SIGNAL.value,dut.SENSOR_SIGNAL.value)[1]).name}]'
        if message_old != message_new:
            message_old =  message_new
            print(message_old)
        assert ([dut.SYSTEM_SIGNAL.value,dut.ALL_OK.value] == system_model(dut.POWER_SIGNAL.value,dut.MODE_SIGNAL.value,dut.COMMAND_SIGNAL.value,dut.SENSOR_SIGNAL.value)), f'result is incorrect: [{Systems(dut.SYSTEM_SIGNAL.value).name},{Rights(dut.ALL_OK.value).name}] ! [{Systems(system_model(dut.POWER_SIGNAL.value,dut.MODE_SIGNAL.value,dut.COMMAND_SIGNAL.value,dut.SENSOR_SIGNAL.value)[0]).name},{Rights(system_model(dut.POWER_SIGNAL.value,dut.MODE_SIGNAL.value,dut.COMMAND_SIGNAL.value,dut.SENSOR_SIGNAL.value)[1]).name}]'
    '''
    print('')

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
