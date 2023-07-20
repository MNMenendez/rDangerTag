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
from cocotb.handle import Force, Release, Deposit

if cocotb.simulator.is_running():
    from models import *

@cocotb.test()
async def clock_divider_test(dut):
    """Testing clock divider"""

    clock = Clock(dut.CLOCK, 30.77, units="us")  # Create a 30us period clock on port clk
    cocotb.start_soon(clock.start(start_high = False))  # Start the clock
    
    dut.CLOCK_STATE.value = True
    
    SLOW_CLOCK = False
    SLOWEST_CLOCK = False
    
    #await FallingEdge(dut.CLOCK)  # Synchronize with the clock
    j = 0
    for i in range(100000):
        print(f'Clock test progress: {i/(100000-1):2.1%}\r', end="\r")
        
        reset = True if ((i % 20000) > 50 and (i % 20000) < 500) else False
        dut.CLOCK_STATE.value = not reset   
        
        if ( ( j % 2**8 -1 ) == 0 ):
            SLOW_CLOCK = (not SLOW_CLOCK)
        if ( ( j % 2**9 -1 ) == 0 ):
            SLOWEST_CLOCK = (not SLOWEST_CLOCK)
        
        if reset:
            j = 0
            SLOW_CLOCK = False
            SLOWEST_CLOCK = False
        else:
            j = j + 1
            
        await FallingEdge(dut.CLOCK)  # Synchronize with the clock
        assert( [SLOW_CLOCK,SLOWEST_CLOCK] == [dut.SLOW_CLOCK.value,dut.SLOWEST_CLOCK.value] ), f'[{1*reset} {i} {j}|{1*SLOW_CLOCK},{1*SLOWEST_CLOCK}] != [{dut.SLOW_CLOCK.value},{dut.SLOWEST_CLOCK.value}]'
               
        await RisingEdge(dut.CLOCK)          
        assert( [SLOW_CLOCK,SLOWEST_CLOCK] == [dut.SLOW_CLOCK.value,dut.SLOWEST_CLOCK.value] ), f'[{1*reset}|{1*SLOW_CLOCK},{1*SLOWEST_CLOCK}] != [{dut.SLOW_CLOCK.value},{dut.SLOWEST_CLOCK.value}]'
    
        #print (f'{1*dut.CLOCK.value},{1*SLOW_CLOCK},{1*SLOWEST_CLOCK} ({dut.CLOCK_STATE.value}) > {1*dut.SLOW_CLOCK.value} {1*dut.SLOWEST_CLOCK.value}')
    print('')
    dut.CLOCK_STATE.value = False
    dut.SLOW_CLOCK.value = False
    dut.SLOWEST_CLOCK.value = False
    dut.PWM.value = False
    await Timer(100, units="ms")
    
def test_movement_runner():
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
        verilog_sources = [proj_path / "hdl" / "clock_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "clock_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="clock_module",
        always=True,
    )
    runner.test(hdl_toplevel="clock_module", test_module="test_clock")


if __name__ == "__main__":
    test_movement_runner()
