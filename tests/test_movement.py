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
    from models import *

@cocotb.test()
async def movement_test(dut):
    """Testing movement"""

    PWM         = 2**8*(False,)+tuple_create(8,1)+(False,)
    MOTOR_STATE = tuple(x.value for x in Motors)
    
    message_old = ''
    message_new = ''
    for i in range(len(PWM)):
        dut.PWM_SIGNAL.value = PWM[i]
        dut.MOTOR_SIGNAL.value = BinaryValue(value=MOTOR_STATE[(i//16)%3],bits=8,bigEndian=False)
   
        await Timer(1, units="ns")
        message_new = f'{dut.PWM_SIGNAL.value}|{Motors(dut.MOTOR_SIGNAL.value).name} > {movement_model(dut.PWM_SIGNAL.value,dut.MOTOR_SIGNAL.value)}'
        if message_old != message_new:
            message_old =  message_new
            print(message_old)
        assert [dut.MOTOR_PWM.value,dut.MOTOR_UP.value,dut.MOTOR_DOWN.value] == movement_model(dut.PWM_SIGNAL.value,dut.MOTOR_SIGNAL.value), f'result is incorrect: [{dut.MOTOR_PWM.value},{dut.MOTOR_UP.value},{dut.MOTOR_DOWN.value}] ! {movement_model(dut.PWM_SIGNAL.value,dut.MOTOR_SIGNAL.value)}'
    print('')

    
def test_movement_runner():
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
        verilog_sources = [proj_path / "hdl" / "movement_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "movement_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="movement_module",
        always=True,
    )
    runner.test(hdl_toplevel="movement_module", test_module="test_movement")


if __name__ == "__main__":
    test_movement_runner()
