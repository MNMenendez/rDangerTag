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
    from models import dummy_model,tuple_create
    
@cocotb.test()
async def TBD_test(dut):
    """Test tbd input"""

    TBD_I = tuple_create(1,1)+tuple_create(1,1)+(False,)
    
    for i in range(len(TBD_I)):
        dut.TBD_I.value = TBD_I[i]
        await Timer(1, units="ns")
        print(f'{bool(dut.TBD_I.value)} > {bool(dut.TBD_O.value)}')
        assert dut.TBD_O.value == dummy_model(TBD_I[i]), f'result is incorrect: {dut.TBD_O.value} != {dut.TBD_I.value}'
    print('')

def test_dummy_runner():
    """Simulate the dummy example using the Python runner.

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
        verilog_sources = [proj_path / "hdl" / "dummy_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "dummy_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="dummy_module",
        always=True,
    )
    runner.test(hdl_toplevel="dummy_module", test_module="test_dummy")


if __name__ == "__main__":
    test_dummy_runner()
