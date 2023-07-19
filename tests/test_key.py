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

if cocotb.simulator.is_running():
    from models import *

@cocotb.test()
async def key_test(dut):
    """Test key"""
    
    dut.KEY_ENABLE.value = False
    
    for i in range (600):
        #print(f'Key test progress: {i/5000:2.1%}\r', end="\r")
        j = random.randint(0 ,3)
        k = BinaryValue(value=j,bits=2,bigEndian=False)
        dut.KEY_I.value = k
        
        reset = True if ((i % 100) > 20 and (i % 100) < 30) else False
        dut.KEY_ENABLE.value = reset 
        
        await Timer(1, units="sec")
        output = key_model(dut.KEY_ENABLE.value,(k//2)%2,k%2)
        
        print(f'{(k//2)%2}{k%2} > Py:[{output[0]}{output[1]},{Keys(output[2]).name}] vs VHDL:[{dut.KEY_O.value},{Keys(dut.KEY_STATE.value).name}]')
        
        assert ([2*output[0]+output[1],output[2]] == [dut.KEY_O.value,dut.KEY_STATE.value]), f'result is incorrect: [{output[0]}{output[1]},{Keys(output[2]).name}] != [{dut.KEY_O.value},{Keys(dut.KEY_STATE.value).name}]'
    
    print('')
    
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
