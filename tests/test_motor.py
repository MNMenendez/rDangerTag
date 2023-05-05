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
    from models import enum,Powers,Modes,Sensors,Commands,Systems,Rights,Motors,power_model,key_model,system_model,output_model,motor_model,tuple_create

@cocotb.test()
async def motor_test(dut):
    """Testing output"""
    
    LOCK            = tuple_create(7,2**6)+(False,)
    MODE_STATE      = tuple(x.value for x in Modes)
    COMMAND_STATE   = tuple(x.value for x in Commands)
    SENSOR_STATE    = tuple(x.value for x in Sensors)
    
    message_old = ''
    message_new = ''
    for i in range(len(LOCK)):
        dut.LOCK.value = LOCK[i]
        dut.MODE_SIGNAL.value = BinaryValue(value=MODE_STATE[(i//16)%4],bits=8,bigEndian=False)
        dut.COMMAND_SIGNAL.value = BinaryValue(value=COMMAND_STATE[(i//4)%4],bits=8,bigEndian=False)
        dut.SENSOR_SIGNAL.value = BinaryValue(value=SENSOR_STATE[(i//1)%4],bits=8,bigEndian=False)
        await Timer(1, units="ns")
        
        message_new = f'Lock {"Enable" if dut.LOCK.value else "Disable"}|{Modes(dut.MODE_SIGNAL.value).name}|{Commands(dut.COMMAND_SIGNAL.value).name}|{Sensors(dut.SENSOR_SIGNAL.value).name} > {Motors(motor_model(dut.LOCK.value,dut.MODE_SIGNAL.value,dut.COMMAND_SIGNAL.value,dut.SENSOR_SIGNAL.value)).name}'
        if message_old != message_new:
            message_old =  message_new
            print(message_old)
        assert dut.MOTOR_SIGNAL.value == motor_model(dut.LOCK.value,dut.MODE_SIGNAL.value,dut.COMMAND_SIGNAL.value,dut.SENSOR_SIGNAL.value), f'result is incorrect: {Motors(dut.MOTOR_SIGNAL.value).name} ! {Motors(motor_model(dut.LOCK.value,dut.MODE_SIGNAL.value,dut.COMMAND_SIGNAL.value,dut.SENSOR_SIGNAL.value)).name}'
    print('')

def test_motor_runner():
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
        verilog_sources = [proj_path / "hdl" / "motor_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "motor_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="motor_module",
        always=True,
    )
    runner.test(hdl_toplevel="motor_module", test_module="test_motor")


if __name__ == "__main__":
    test_motor_runner()
