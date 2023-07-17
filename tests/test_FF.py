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
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

if cocotb.simulator.is_running():
    from models import *

@cocotb.test()

@cocotb.test()
async def FF_test(dut):
    """Test that d propagates to q"""

    clock = Clock(dut.CLOCK, 30, units="us")  # Create a 30us period clock on port clk
    cocotb.start_soon(clock.start())  # Start the clock

    await FallingEdge(dut.CLOCK)  # Synchronize with the clock
    for i in range(50000):
        reset = True if ((i % 10000) > 50 and (i % 10000) < 100) else False
        dut.RESET.value = reset
        await FallingEdge(dut.CLOCK)
        output = not clock
        #print(f'{reset}-> {output} vs {dut.CLOCK_OUT.value}')
        
        #assert ( dut.CLOCK_OUT.value == output ), f'output q was incorrect on the {i}th cycle - {val}|{reset}> {output} vs {dut.CLOCK_OUT.value}' 
    
'''
async def FF_test(dut):
    """Test FF"""
    
    RESET   = tuple_create(12,2**11)+(False,)
    D       = tuple_create(12,2**8)+(False,)
    CLOCK   = tuple_create(12,1)+(False,)
    
    
    for i in range(len(CLOCK)):
        dut.CLOCK.value = CLOCK[i]
        dut.RESET.value = RESET[i]
        dut.D.value     = D[i]
        
        await Timer(15, units="us")
        
        output = ff_model(CLOCK[i],RESET[i],D[i])
        
        print(f'{dut.CLOCK.value}|{dut.RESET.value}|{dut.D.value}-{dut.Q}  > {output}')
   
        #assert ( dut.Q  == output ), f'{dut.Q} != {output}'
        
    print('')
'''
def test_ff_runner():
    """Simulate the interlock example using the Python runner.

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
        verilog_sources = [proj_path / "hdl" / "ff_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "ff_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="ff_module",
        always=True,
    )
    runner.test(hdl_toplevel="ff_module", test_module="test_FF")


if __name__ == "__main__":
    test_ff_runner()
