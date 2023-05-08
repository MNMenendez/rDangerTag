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
    from models import *

@cocotb.test()
async def general_test(dut):
    """Integration test"""
    
    POWER_MODE      = tuple_create(17,2**16)+(False,)
    CLOCK_STATE     = tuple_create(17,2**16)+(False,)
    LOCK            = tuple_create(17,2**15)+(False,)
    KEY             = tuple_create(17,2**14)+(False,)
    KEY_A_I         = tuple_create(17,2**13)+(False,)
    KEY_B_I         = tuple_create(17,2**12)+(False,)
    INPUT_A         = tuple_create(17,2**11)+(False,)
    INPUT_B         = tuple_create(17,2**10)+(False,)
    SENSOR_1        = tuple_create(17,2**9)+(False,)
    SENSOR_2        = tuple_create(17,2**8)+(False,)
    SENSOR_3        = tuple_create(17,2**7)+(False,)
    SENSOR_4        = tuple_create(17,2**6)+(False,)
    LOCK_A_I        = tuple_create(17,2**5)+(False,)
    LOCK_B_I        = tuple_create(17,2**4)+(False,)
    TBD_I           = tuple_create(17,2**3)+(False,)
    CLOCK           = tuple_create(17,2**0)+(False,)    
    
    message_old = ''
    message_new = ''
    for i in range(len(CLOCK)):
        dut.CLOCK_STATE.value   = CLOCK_STATE[i]
        dut.POWER_MODE.value    = POWER_MODE[i]
        dut.KEY.value           = KEY[i]
        dut.KEY_A_I.value       = KEY_A_I[i]
        dut.KEY_B_I.value       = KEY_B_I[i]
        dut.SENSOR_1.value      = SENSOR_1[i]
        dut.SENSOR_2.value      = SENSOR_2[i]
        dut.SENSOR_3.value      = SENSOR_3[i]
        dut.SENSOR_4.value      = SENSOR_4[i]
        dut.INPUT_A.value       = INPUT_A[i]
        dut.INPUT_B.value       = INPUT_B[i]
        dut.LOCK.value          = LOCK[i]
        dut.LOCK_A_I.value      = LOCK_A_I[i]
        dut.LOCK_B_I.value      = LOCK_B_I[i]
        dut.TBD_I.value         = TBD_I[i]
        dut.CLOCK.value         = CLOCK[i]
        await Timer(1, units="ns")
        [KEY_A_O,KEY_B_O,LOCK_A_O,LOCK_B_O,ALL_OK,WATCHDOG,OUTPUT_A,OUTPUT_B,MOTOR_PWM,MOTOR_UP,MOTOR_DOWN,TBD_O] = general_model(POWER_MODE[i], KEY[i], KEY_A_I[i], KEY_B_I[i],SENSOR_1[i], SENSOR_2[i], SENSOR_3[i], SENSOR_4[i],INPUT_A[i], INPUT_B[i], LOCK[i], LOCK_A_I[i], LOCK_B_I[i], CLOCK[i], CLOCK_STATE[i], TBD_I[i])
        
        message_new = f'{Powers(dut.POWER_SIGNAL.value).name}|Clock {"Alive" if dut.CLOCK_STATE.value else "Dead"}|Lock {"Enable" if dut.LOCK.value else "Disable"}|Key {"Enable" if dut.KEY.value else "Disable"}|{Modes(dut.MODE_SIGNAL.value).name}|{Commands(dut.COMMAND_SIGNAL.value).name}|{Sensors(dut.SENSOR_SIGNAL.value).name}|{Systems(dut.SYSTEM_SIGNAL.value).name} > K_[{1 if KEY_A_O else 0},{1 if KEY_B_O else 0}] L_[{1 if LOCK_A_O else 0},{1 if LOCK_B_O else 0}] | {Rights(ALL_OK).name} W_{1 if WATCHDOG else 0} | O_[{1 if OUTPUT_A else 0},{1 if OUTPUT_B else 0}] | PWM_{MOTOR_PWM} M_[{1 if MOTOR_UP else 0},{1 if MOTOR_DOWN else 0}] {1 if TBD_O else 0} | {Motors(dut.MOTOR_SIGNAL.value).name}'
        if message_old != message_new:
            message_old =  message_new
            print(message_old)
        assert [dut.KEY_A_O.value,dut.KEY_B_O.value] == [KEY_A_O,KEY_B_O], f'Keys are incorrect: [{dut.KEY_A_O.value},{dut_KEY_B_O.value}] != [{KEY_A_O},{KEY_B_O}]'
        assert [dut.LOCK_A_O.value,dut.LOCK_B_O.value] == [LOCK_A_O,LOCK_B_O], f'Locks are incorrect: [{dut.LOCK_A_O.value},{dut.LOCK_B_O.value}] != [{LOCK_A_O},{LOCK_B_O}]'
        assert [dut.ALL_OK.value,dut.WATCHDOG.value] == [ALL_OK,WATCHDOG], f'Watchdogs are incorrect: [{dut.ALL_OK.value},{dut.WATCHDOG.value}] != [{ALL_OK},{WATCHDOG}]'
        assert [dut.OUTPUT_A.value,dut.OUTPUT_B.value] == [OUTPUT_A,OUTPUT_B], f'Outputs are incorrect: [{dut.OUTPUT_A.value},{dut.OUTPUT_B.value}] != [{OUTPUT_A},{OUTPUT_B}]'
        assert dut.TBD_O.value == TBD_O, f'TBD are incorrect: {dut.TBD_O.value} != {TBD_O}'
        assert [dut.MOTOR_PWM.value,dut.MOTOR_UP.value,dut.MOTOR_DOWN.value] == [MOTOR_PWM,MOTOR_UP,MOTOR_DOWN], f'Motor is incorrect: [{dut.MOTOR_PWM.value},{dut.MOTOR_UP.value},{dut.MOTOR_DOWN.value}] != [{MOTOR_PWM},{MOTOR_UP},{MOTOR_DOWN}]'
    print('')

    
def test_general_runner():
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
        verilog_sources = [proj_path / "hdl" / "general.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "general.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="general",
        always=True,
    )
    runner.test(hdl_toplevel="general", test_module="test_general")


if __name__ == "__main__":
    test_general_runner()
