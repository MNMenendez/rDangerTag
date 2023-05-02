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

if cocotb.simulator.is_running():
    from models import dummy_model
    
@cocotb.test()
async def TBD_rising_test(dut):
    """Test rising input"""

    TBD_I = False
    dut.TBD_I.value = TBD_I
    await Timer(2, units="ns")
    assert dut.TBD_O.value == dummy_model(TBD_I), f"dummy result is incorrect: {dut.TBD_O.value} != {dut.TBD_I.value} "

    TBD_I = True
    dut.TBD_I.value = TBD_I
    await Timer(2, units="ns")
    assert dut.TBD_O.value == dummy_model(TBD_I), f"dummy result is incorrect: {dut.TBD_O.value} != {dut.TBD_I.value} "
    
@cocotb.test()
async def TBD_falling_test(dut):
    """Test negative input"""

    TBD_I = True
    dut.TBD_I.value = TBD_I
    await Timer(2, units="ns")
    assert dut.TBD_O.value == dummy_model(TBD_I), f"dummy result is incorrect: {dut.TBD_O.value} != {dut.TBD_I.value} "
    
    TBD_I = False
    dut.TBD_I.value = TBD_I
    await Timer(2, units="ns")
    assert dut.TBD_O.value == dummy_model(TBD_I), f"dummy result is incorrect: {dut.TBD_O.value} != {dut.TBD_I.value} "
    

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
