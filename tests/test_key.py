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
    from models import enum,Modes,key_model

@cocotb.test()
async def key_test(dut):
    """Test key"""
    
    KEY     = (False,False,False,False,True,True,True,True)
    KEY_A_I = (False,False,True,True,False,False,True,True)
    KEY_B_I = (False,True,False,True,False,True,False,True)
    
    for i in range(len(KEY)):
        dut.KEY.value = KEY[i]
        dut.KEY_A_I.value = KEY_A_I[i]
        dut.KEY_B_I.value = KEY_B_I[i]
        await Timer(2, units="ns")
        print(f'Key {"Enable" if dut.KEY.value else "Disable"} | {bool(dut.KEY_A_I.value)} | {bool(dut.KEY_B_I.value)} > {Modes(key_model(KEY[i],KEY_A_I[i],KEY_B_I[i])[2]).name}')
        assert ((dut.KEY_A_O.value,dut.KEY_B_O.value,dut.MODE_SIGNAL.value) == key_model(KEY[i],KEY_A_I[i],KEY_B_I[i])), f'result is incorrect: {dut.KEY_A_O.value} {dut.KEY_B_O.value} {dut.MODE_SIGNAL.value} != {key_model(KEY[i],KEY_A_I[i],KEY_B_I[i])}'   
    
def test_key_runner():
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
        verilog_sources = [proj_path / "hdl" / "key_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "key_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="key_module",
        always=True,
    )
    runner.test(hdl_toplevel="key_module", test_module="test_key")


if __name__ == "__main__":
    test_key_runner()
