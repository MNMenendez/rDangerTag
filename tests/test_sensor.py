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
    from models import enum,Sensors,sensor_model,tuple_create

@cocotb.test()
async def sensor_test(dut):
    """Sensor test"""
    
    SENSOR_1 = tuple_create(4,8)+(False,)
    SENSOR_2 = tuple_create(4,4)+(False,)
    SENSOR_3 = tuple_create(4,2)+(False,)
    SENSOR_4 = tuple_create(4,1)+(False,)
    
    for i in range(len(SENSOR_1)):
        dut.SENSOR_1.value = SENSOR_1[i]
        dut.SENSOR_2.value = SENSOR_2[i]
        dut.SENSOR_3.value = SENSOR_3[i]
        dut.SENSOR_4.value = SENSOR_4[i]
        
        await Timer(1, units="ns")
        print(f'{dut.SENSOR_1.value}|{dut.SENSOR_2.value}|{dut.SENSOR_3.value}|{dut.SENSOR_4.value} > {Sensors(sensor_model(SENSOR_1[i],SENSOR_2[i],SENSOR_3[i],SENSOR_4[i])).name}')
    assert dut.SENSOR_SIGNAL.value == sensor_model(SENSOR_1[i],SENSOR_2[i],SENSOR_3[i],SENSOR_4[i]), f'result is incorrect: {dut.SENSOR_SIGNAL.value} != {sensor_model(SENSOR_1[i],SENSOR_2[i],SENSOR_3[i],SENSOR_4[i])}'   
    print('')

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
