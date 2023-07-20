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
async def PLC_test(dut):
    """Test PLC"""
    
    PLC_A_I = tuple_create(2,2)+(False,)
    PLC_B_I = tuple_create(2,1)+(False,)
        
    for i in range(len(PLC_A_I)):
        dut.PLC_I.value = 2*PLC_A_I[i]+PLC_B_I[i]
        await Timer(1, units="sec")
        
        output = plc_model(PLC_A_I[i],PLC_B_I[i])
        
        print(f'{PLCs(dut.PLC_I.value).name} > {PLCs(output).name}')
   
        assert ( dut.PLC_STATE.value  == output ), f'{PLCs(dut.PLC_STATE.value).name} != {PLCs(output).name}'
    print('')

def test_plc_runner():
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
        verilog_sources = [proj_path / "hdl" / "plc_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "plc_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="plc_module",
        always=True,
    )
    runner.test(hdl_toplevel="plc_module", test_module="test_PLC")


if __name__ == "__main__":
    test_plc_runner()
