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
    from models import enum,Sensors,sensor_model

@cocotb.test()
async def sensor_1and3_different_test(dut):
    """Sensor 1 and Sensor 3 are different : Error expected"""
    
    SENSOR_2 = Logic('-')
    SENSOR_4 = Logic('-')
    dut.SENSOR_2.value = SENSOR_2
    dut.SENSOR_4.value = SENSOR_4
    
    SENSOR_1 = False
    SENSOR_3 = True
    dut.SENSOR_1.value = SENSOR_1
    dut.SENSOR_3.value = SENSOR_3
    
    await Timer(2, units="ns")   
    print(f'{dut.SENSOR_1.value}|{dut.SENSOR_2.value}|{dut.SENSOR_3.value}|{dut.SENSOR_4.value} > {sensor_model(SENSOR_1,SENSOR_3)}')
    assert dut.SENSOR_SIGNAL.value == sensor_model(SENSOR_1,SENSOR_3), f'result is incorrect: {dut.SENSOR_SIGNAL.value} != {Sensors.ERROR_SENSOR}'

    SENSOR_1 = True
    SENSOR_3 = False
    dut.SENSOR_1.value = SENSOR_1
    dut.SENSOR_3.value = SENSOR_3

    await Timer(2, units="ns")   
    print(f'{dut.SENSOR_1.value}|{dut.SENSOR_2.value}|{dut.SENSOR_3.value}|{dut.SENSOR_4.value} > {sensor_model(SENSOR_1,SENSOR_3)}')  
    assert dut.SENSOR_SIGNAL.value == sensor_model(SENSOR_1,SENSOR_3), f'result is incorrect: {dut.SENSOR_SIGNAL.value} != {Sensors.ERROR_SENSOR}'

@cocotb.test()
async def sensor_2and4_different_test(dut):
    """Sensor 2 and Sensor 4 are different : Error expected"""
    
    SENSOR_1 = Logic('-')
    SENSOR_3 = Logic('-')
    dut.SENSOR_1.value = SENSOR_1
    dut.SENSOR_3.value = SENSOR_3
    
    SENSOR_2 = False
    SENSOR_4 = True 
    dut.SENSOR_2.value = SENSOR_2
    dut.SENSOR_4.value = SENSOR_4

    await Timer(2, units="ns")   
    print(f'{dut.SENSOR_1.value}|{dut.SENSOR_2.value}|{dut.SENSOR_3.value}|{dut.SENSOR_4.value} > {sensor_model(SENSOR_2,SENSOR_4)}') 
    assert dut.SENSOR_SIGNAL.value == sensor_model(SENSOR_2,SENSOR_4), f'result is incorrect: {dut.SENSOR_SIGNAL.value} != {Sensors.ERROR_SENSOR}'
 
    SENSOR_2 = True
    SENSOR_4 = False
    dut.SENSOR_2.value = SENSOR_2
    dut.SENSOR_4.value = SENSOR_4

    await Timer(2, units="ns")   
    print(f'{dut.SENSOR_1.value}|{dut.SENSOR_2.value}|{dut.SENSOR_3.value}|{dut.SENSOR_4.value} > {sensor_model(SENSOR_2,SENSOR_4)}')   
    assert dut.SENSOR_SIGNAL.value == sensor_model(SENSOR_2,SENSOR_4), f'result is incorrect: {dut.SENSOR_SIGNAL.value} != {Sensors.ERROR_SENSOR}'

@cocotb.test()
async def sensor_danger_test(dut):
    """Sensor 1 and 3 are True, sensors 2 and 4 are False : Danger expected"""
    SENSOR_1 = True
    SENSOR_2 = False
    SENSOR_3 = True
    SENSOR_4 = False
    dut.SENSOR_1.value = SENSOR_1
    dut.SENSOR_2.value = SENSOR_2
    dut.SENSOR_3.value = SENSOR_3
    dut.SENSOR_4.value = SENSOR_4
    
    await Timer(2, units="ns")   
    print(f'{dut.SENSOR_1.value}|{dut.SENSOR_2.value}|{dut.SENSOR_3.value}|{dut.SENSOR_4.value} > {dut.SENSOR_SIGNAL.value} | {sensor_model(SENSOR_1,SENSOR_2,SENSOR_3,SENSOR_4)}')  
    assert dut.SENSOR_SIGNAL.value == sensor_model(SENSOR_1,SENSOR_2,SENSOR_3,SENSOR_4), f'result is incorrect: {dut.SENSOR_SIGNAL.value} != {Sensors.DANGER}'

@cocotb.test()
async def sensor_blank_test(dut):
    """Sensor 1 and 3 are False, sensors 2 and 4 are True : Blank expected"""
    SENSOR_1 = False
    SENSOR_2 = True
    SENSOR_3 = False
    SENSOR_4 = True
    dut.SENSOR_1.value = SENSOR_1
    dut.SENSOR_2.value = SENSOR_2
    dut.SENSOR_3.value = SENSOR_3
    dut.SENSOR_4.value = SENSOR_4
    
    await Timer(2, units="ns")   
    print(f'{dut.SENSOR_1.value}|{dut.SENSOR_2.value}|{dut.SENSOR_3.value}|{dut.SENSOR_4.value} > {dut.SENSOR_SIGNAL.value} | {sensor_model(SENSOR_1,SENSOR_2,SENSOR_3,SENSOR_4)}')  
    assert dut.SENSOR_SIGNAL.value == sensor_model(SENSOR_1,SENSOR_2,SENSOR_3,SENSOR_4), f'result is incorrect: {dut.SENSOR_SIGNAL.value} != {Sensors.BLANK}'

@cocotb.test()
async def sensor_transition_test(dut):
    """All sensors are the same : Transition expected"""
    SENSOR_1 = True
    SENSOR_2 = True
    SENSOR_3 = True
    SENSOR_4 = True
    dut.SENSOR_1.value = SENSOR_1
    dut.SENSOR_2.value = SENSOR_2
    dut.SENSOR_3.value = SENSOR_3
    dut.SENSOR_4.value = SENSOR_4
    
    await Timer(2, units="ns")   
    print(f'{dut.SENSOR_1.value}|{dut.SENSOR_2.value}|{dut.SENSOR_3.value}|{dut.SENSOR_4.value} > {dut.SENSOR_SIGNAL.value} | {sensor_model(SENSOR_1,SENSOR_2,SENSOR_3,SENSOR_4)}')  
    assert dut.SENSOR_SIGNAL.value == sensor_model(SENSOR_1,SENSOR_2,SENSOR_3,SENSOR_4), f'result is incorrect: {dut.SENSOR_SIGNAL.value} != {Sensors.TRANSITION}'

    SENSOR_1 = False
    SENSOR_2 = False
    SENSOR_3 = False
    SENSOR_4 = False
    dut.SENSOR_1.value = SENSOR_1
    dut.SENSOR_2.value = SENSOR_2
    dut.SENSOR_3.value = SENSOR_3
    dut.SENSOR_4.value = SENSOR_4
    
    await Timer(2, units="ns")   
    print(f'{dut.SENSOR_1.value}|{dut.SENSOR_2.value}|{dut.SENSOR_3.value}|{dut.SENSOR_4.value} > {dut.SENSOR_SIGNAL.value} | {sensor_model(SENSOR_1,SENSOR_2,SENSOR_3,SENSOR_4)}')  
    assert dut.SENSOR_SIGNAL.value == sensor_model(SENSOR_1,SENSOR_2,SENSOR_3,SENSOR_4), f'result is incorrect: {dut.SENSOR_SIGNAL.value} != {Sensors.TRANSITION}'



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
