# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0
# Simple tests for an dummy module
import os
import random
import sys
from pathlib import Path

import cocotb
import itertools
import warnings
from decimal import Decimal
from numbers import Real
from typing import Union

from cocotb.log import SimLog
from cocotb.runner import get_runner
from cocotb.triggers import Timer, FallingEdge, RisingEdge
from cocotb.types import Bit, Logic
from cocotb.binary import BinaryValue
from cocotb.clock import Clock
from cocotb.utils import get_sim_steps, get_time_from_sim_steps, lazy_property

if cocotb.simulator.is_running():
    from models import *

@cocotb.test()
async def debounce_test(dut):
    """Testing debouncing"""

    # Clock used is the slowest clock -> 31.25 Hz
    clock = Clock(dut.CLOCK, 32, units="ms")  # Create a 32ms period clock on port clk
    cocotb.start_soon(clock.start(start_high = False))  # Start the clock
    
    dut.CLOCK_STATE.value = True
    
    counter = 0
    output = "00"
    
    for i in range(20000):
        print(f'Debouncing test progress: {i/20000:2.1%}\r', end="\r")
        
        reset = True if ((i % 5000) > 50 and (i % 5000) < 250) else False
        dut.CLOCK_STATE.value = not reset   
        
        if ( i % 20 == 0 ):
            j = random.randint(0 , 3)
            k = BinaryValue(value=j,bits=2,bigEndian=False)
            #print(f'{j//2}{j%2} {dut.DATA_I.value}')
            
        if reset:
            counter = 0
            output = "00"
        else:  
            counter += 1 
            
            if counter == 30:
                output = str(dut.DATA_I.value)#str(j//2)+str(j%2)
            if ( str(j//2)+str(j%2) != str(dut.DATA_I.value) ):
                counter = 0
            
            dut.DATA_I.value = k       
   
        await FallingEdge(dut.CLOCK)  # Synchronize with the clock
        assert( output == str(dut.DATA_O.value) ), f' {output} != {str(dut.DATA_O.value)} {j}'     
       
        
        await RisingEdge(dut.CLOCK)          
        assert( output == str(dut.DATA_O.value) ), f' {output} != {str(dut.DATA_O.value)} {j}'           
        
        #if ( output != str(dut.DATA_O.value)):
        #    print('x'*50+' '+str(j))
        #print(f'{dut.DATA_I.value}|{counter}[{1*reset}|{dut.CLOCK_STATE.value}] >> Py:{output} vs VHDL:{str(dut.DATA_O.value)}')
        
    print('')
    
def test_debounce_runner():
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
        verilog_sources = [proj_path / "hdl" / "debounce_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "debounce_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="debounce_module",
        always=True,
    )
    runner.test(hdl_toplevel="debounce_module", test_module="test_debounce")


if __name__ == "__main__":
    test_movement_runner()
