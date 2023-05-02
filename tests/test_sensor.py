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
    from models import enum,Modes,sensor_model

@cocotb.test()
async def sensor_error_test(dut):
    """Test sensor error"""
        
    SENSOR_1 = False
    SENSOR_2 = False
    SENSOR_3 = False
    SENSOR_4 = False
    
    dut.SENSOR_1.value = SENSOR_1
    await Timer(2, units="ns")     
    assert dut.SENSOR_SIGNAL.value == Sensors.ERROR_SENSOR, f'result is incorrect: {dut.SENSOR_SIGNAL.value} != {Sensors.ERROR_SENSOR}'


def test_sensor_runner():
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
        verilog_sources = [proj_path / "hdl" / "sensor_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "sensor_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="sensor_module",
        always=True,
    )
    runner.test(hdl_toplevel="sensor_module", test_module="test_sensor")


if __name__ == "__main__":
    test_sensor_runner()
