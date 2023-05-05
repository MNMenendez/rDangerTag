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

if cocotb.simulator.is_running():
    from models import *

@cocotb.test()
async def clock_test(dut):
    """Testing clock"""
    
    CLOCK_STATE   = tuple_create(12,1024)+(False,)
    CLOCK         = tuple_create(12,1)+(False,)
    
    message_old = ''
    message_new = ''
    for i in range(len(CLOCK_STATE)):
        dut.CLOCK_STATE.value = CLOCK_STATE[i]
        dut.CLOCK.value = CLOCK[i]
        await Timer(1, units="ns")
        message_new = f'Clock {"Alive" if dut.CLOCK_STATE.value else "Dead"}|{dut.CLOCK.value} > Clock {"Alive" if dut.WATCHDOG.value else "Dead"}|{dut.PWM_SIGNAL.value}'
        if message_old != message_new:
            message_old =  message_new
            #print(message_old)
        assert [dut.WATCHDOG.value,dut.PWM_SIGNAL.value] == clock_model(dut.CLOCK.value,dut.CLOCK_STATE.value), f'result is incorrect: [{dut.WATCHDOG.value},{dut.PWM_SIGNAL.value}] ! {clock_model(dut.CLOCK.value,dut.CLOCK_STATE.value)}'
    print('')

    
def test_clock_runner():
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
    test_clock_runner()
