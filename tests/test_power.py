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
    from models import enum,Powers,power_model
    
@cocotb.test()
async def power_mode_test(dut):
    """Test power"""

    POWER_MODE = (False,True,False,True,False)
    
    for i in range(len(POWER_MODE)):
        dut.POWER_MODE.value = POWER_MODE[i]
        await Timer(2, units="ns")
        print(f'Power {"Connected" if dut.POWER_MODE.value else "Disconnected"} > {Powers(power_model(POWER_MODE[i])).name}')
        assert dut.POWER_SIGNAL.value == power_model(POWER_MODE[i]), f'result is incorrect: {dut.POWER_SIGNAL.value} != {dut.POWER_MODE.value}'    

def test_power_runner():
    """Simulate the power example using the Python runner.

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
        verilog_sources = [proj_path / "hdl" / "power_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "power_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="power_module",
        always=True,
    )
    runner.test(hdl_toplevel="power_module", test_module="test_power")


if __name__ == "__main__":
    test_power_runner()
