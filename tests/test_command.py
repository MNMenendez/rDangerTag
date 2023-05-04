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
    from models import enum,Modes,Commands,key_model,command_model,tuple_create

@cocotb.test()
async def command_test(dut):
    """Test commands"""
    
    KEY     = tuple_create(5,16)+(False,)
    KEY_A_I = tuple_create(5,8)+(False,)
    KEY_B_I = tuple_create(5,4)+(False,)
    INPUT_A = tuple_create(5,2)+(False,)
    INPUT_B = tuple_create(5,1)+(False,)
    
    for i in range(len(KEY)):
        dut.KEY.value     = KEY[i]
        dut.KEY_A_I.value = KEY_A_I[i]
        dut.KEY_B_I.value = KEY_B_I[i]
        dut.INPUT_A.value = INPUT_A[i]
        dut.INPUT_B.value = INPUT_B[i]
        
        await Timer(1, units="ns")
        print(f'{Modes(dut.MODE_SIGNAL.value).name}|{dut.INPUT_A.value}|{dut.INPUT_B.value} > {Commands(dut.COMMAND_SIGNAL.value).name}')
        assert dut.COMMAND_SIGNAL.value == command_model(INPUT_A[i],INPUT_B[i],dut.MODE_SIGNAL.value), f'result is incorrect: {dut.COMMAND_SIGNAL.value} != {command_model(INPUT_A[i],INPUT_B[i],dut.MODE_SIGNAL.value)}'   
    print('')
    
def test_command_runner():
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
