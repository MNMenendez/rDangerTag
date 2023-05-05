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
    from models import enum,Powers,Modes,Sensors,Commands,Systems,Rights,power_model,key_model,system_model,output_model,tuple_create

@cocotb.test()
async def output_test(dut):
    """Testing output"""
    
    SYSTEM_MODE = tuple(x.value for x in Systems)
    
    message_old = ''
    message_new = ''
    for i in range(len(Systems)):
        dut.SYSTEM_SIGNAL.value = BinaryValue(value=SYSTEM_MODE[(i//1)%5],bits=8,bigEndian=False)
        await Timer(1, units="ns")
        
        message_new = f'{Systems(dut.SYSTEM_SIGNAL.value).name} > {output_model(dut.SYSTEM_SIGNAL.value)}'
        if message_old != message_new:
            message_old =  message_new
            print(message_old)
        #print(f'{Systems(dut.SYSTEM_SIGNAL.value).name} > {output_model(dut.SYSTEM_SIGNAL.value)}')
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
