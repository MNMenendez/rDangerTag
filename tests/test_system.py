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
    from models import enum,Powers,Modes,Sensors,Commands,Systems,Rights,system_model

@cocotb.test()
async def system_power_off_test(dut):
    """If power is off: system running on battery expected"""
            
    await Timer(2, units="ns")
    print(f'{dut.POWER_SIGNAL.value}|{dut.MODE_SIGNAL.value}|{dut.COMMAND_SIGNAL.value}|{dut.SENSOR_SIGNAL.value}  > {dut.SYSTEM_SIGNAL.value} | {dut.OK_SIGNAL.value} & {system_model(Powers.POWER_OFF)}')
    assert ([dut.SYSTEM_SIGNAL.value,dut.OK_SIGNAL.value] == system_model(Powers.POWER_OFF)), f'result is incorrect: [{dut.SYSTEM_SIGNAL.value},{dut.OK_SIGNAL.value}] ! {system_model(Powers.POWER_OFF)}'







def test_system_runner():
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
        verilog_sources = [proj_path / "hdl" / "system_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "system_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="system_module",
        always=True,
    )
    runner.test(hdl_toplevel="system_module", test_module="test_system")


if __name__ == "__main__":
    test_system_runner()
