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
    from models import enum,Powers,Modes,Sensors,Commands,Systems,Rights,power_model,key_model,system_model,output_model,tuple_create

@cocotb.test()
async def output_test(dut):
    """Testing output"""
    
    POWER_MODE  = tuple_create(10,512)+(False,)
    KEY         = tuple_create(10,256)+(False,)
    KEY_A_I     = tuple_create(10,128)+(False,)
    KEY_B_I     = tuple_create(10,64)+(False,)
    INPUT_A     = tuple_create(10,32)+(False,)
    INPUT_B     = tuple_create(10,16)+(False,)
    SENSOR_1    = tuple_create(10,8)+(False,)
    SENSOR_2    = tuple_create(10,4)+(False,)
    SENSOR_3    = tuple_create(10,2)+(False,)
    SENSOR_4    = tuple_create(10,1)+(False,)
    
    for i in range(len(POWER_MODE)):
        dut.POWER_MODE.value = POWER_MODE[i]
        dut.KEY.value = KEY[i]
        dut.KEY_A_I.value = KEY_A_I[i]
        dut.KEY_B_I.value = KEY_B_I[i]
        dut.INPUT_A.value = INPUT_A[i]
        dut.INPUT_B.value = INPUT_B[i]
        dut.SENSOR_1.value = SENSOR_1[i]
        dut.SENSOR_2.value = SENSOR_2[i]
        dut.SENSOR_3.value = SENSOR_3[i]
        dut.SENSOR_4.value = SENSOR_4[i]
        await Timer(1, units="ns")
        print(f'{Systems(dut.SYSTEM_SIGNAL.value).name} > {output_model(dut.SYSTEM_SIGNAL.value)}')
        assert ([dut.OUTPUT_A.value,dut.OUTPUT_B.value] == output_model(dut.SYSTEM_SIGNAL.value)), f'result is incorrect: [{dut.OUTPUT_A.value},{dut.OUTPUT_B.value}] ! {output_model(dut.SYSTEM_SIGNAL.value)}'
    print('')
    
def test_output_runner():
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
        verilog_sources = [proj_path / "hdl" / "ouput_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "ouput_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="ouput_module",
        always=True,
    )
    runner.test(hdl_toplevel="ouput_module", test_module="test_output")


if __name__ == "__main__":
    test_output_runner()
