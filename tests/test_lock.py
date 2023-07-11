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
async def interlocking_test(dut):
    """Test interlocking"""
    
    LOCK     = tuple_create(3,4)+(False,)
    LOCK_A_I = tuple_create(3,2)+(False,)
    LOCK_B_I = tuple_create(3,1)+(False,)
        
    for i in range(len(LOCK)):
        dut.LOCK_ENABLE.value = LOCK[i]
        dut.LOCK_I.value = 2*LOCK_A_I[i]+LOCK_B_I[i]
        await Timer(1, units="sec")
        
        print(f'Lock {"Enable" if dut.LOCK_ENABLE.value else "Disable"} | {Locks(dut.LOCK_I.value).name} > {lock_model(LOCK[i],LOCK_A_I[i],LOCK_B_I[i])[:2]} {Locks(lock_model(LOCK[i],LOCK_A_I[i],LOCK_B_I[i])[2]).name}')
   
        output = lock_model(LOCK[i],LOCK_A_I[i],LOCK_B_I[i])
        assert ( [dut.LOCK_O.value,dut.LOCK_STATE.value]  == [2*output[0]+output[1],output[2]]), f'{[dut.LOCK_O.value,dut.LOCK_STATE.value]} != {output}'
    print('')

def test_lock_runner():
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
        verilog_sources = [proj_path / "hdl" / "lock_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "lock_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="lock_module",
        always=True,
    )
    runner.test(hdl_toplevel="lock_module", test_module="test_lock")


if __name__ == "__main__":
    test_lock_runner()
