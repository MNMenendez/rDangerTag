# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0
# Simple tests for an dummy module
import os
import random
import sys
from pathlib import Path

import cocotb
import itertools
import warnings
from decimal import Decimal
from numbers import Real
from typing import Union

from cocotb.log import SimLog
from cocotb.runner import get_runner
from cocotb.triggers import Timer, FallingEdge, RisingEdge
from cocotb.types import Bit, Logic
from cocotb.binary import BinaryValue
from cocotb.clock import Clock
from cocotb.utils import get_sim_steps, get_time_from_sim_steps, lazy_property

if cocotb.simulator.is_running():
    from models import *

@cocotb.test()
async def movement_test(dut):
    """Testing movement"""

    clock = Clock(dut.SLOWEST_CLOCK, 32, units="ms")  # Create a 30us period clock on port clk
    cocotb.start_soon(clock.start(start_high = False))  # Start the clock
    
    powerStates = [Powers.POWER_OFF,Powers.POWER_ON,Powers.BATTERY,Powers.BATTERY_LOW]
    systemStates = [Systems.SYSTEM_ERROR,Systems.SYSTEM_DANGER,Systems.SYSTEM_BLANK,Systems.SYSTEM_TRANSITION,Systems.SYSTEM_TIMEOUT,Systems.SYSTEM_IDLE]
    
    dut.POWER_STATE.value = BinaryValue(value=Powers.POWER_OFF.value,bits=8,bigEndian=False)
    dut.SYSTEM_STATE.value = BinaryValue(value=Systems.SYSTEM_IDLE.value,bits=8,bigEndian=False)
    
    j = 0
    k = 0
    
    for i in range(10000):
        if ( i % 50 == 0 ):  
            #print(f'{i} -> {j % len(powerStates)} {k % len(systemStates)}')
            if ( (j+1) % 5*len(powerStates) == 0 ):
                k = k + 1
            j = j + 1
            
            dut.POWER_STATE.value = BinaryValue( value = j % len(powerStates) , bits = 8 , bigEndian = False )
            dut.SYSTEM_STATE.value = BinaryValue( value = k % len(systemStates) , bits = 8 , bigEndian = False )
        
        await FallingEdge(dut.SLOWEST_CLOCK)  # Synchronize with the clock
        output = output_model(dut.POWER_STATE.value,dut.SYSTEM_STATE.value,dut.SLOWEST_CLOCK.value)
        await Timer(1, units="ns")
        
   
        #assert( [output[0],2*output[1]+output[2]] == [dut.MOTOR_PWM.value,dut.MOTOR_UPDOWN.value] ), f'{output} != [{dut.MOTOR_PWM.value},{dut.MOTOR_UPDOWN.value}]'
               
        await RisingEdge(dut.SLOWEST_CLOCK)          
        output = output_model(dut.POWER_STATE.value,dut.SYSTEM_STATE.value,dut.SLOWEST_CLOCK.value)
        await Timer(1, units="ns")
        #assert( output[0] == dut.MOTOR_PWM.value ), f'{output[0]} != {dut.MOTOR_PWM.value}'
        #assert( [output[0],2*output[1]+output[2]] == [dut.MOTOR_PWM.value,dut.MOTOR_UPDOWN.value] ), f'{output} != [{dut.MOTOR_PWM.value},{dut.MOTOR_UPDOWN.value}]'
        
            
    
        await FallingEdge(dut.SLOWEST_CLOCK)
        output = output_model(dut.POWER_STATE.value,dut.SYSTEM_STATE.value,dut.SLOWEST_CLOCK.value)
        #print(f'[{Powers(dut.POWER_STATE.value).name},{Systems(dut.SYSTEM_STATE.value).name}] > [{Outputs(2*output[0][0]+output[0][1]).name},{Leds(2*output[1][0]+output[1][1]).name},{Leds(2*output[2][0]+output[2][1]).name}]')
        
        if ( i % 50 == 0 ):
            print(f'[{Powers(dut.POWER_STATE.value).name},{Systems(dut.SYSTEM_STATE.value).name}] > Py:[{Outputs(2*output[0][0]+output[0][1]).name},{Leds(2*output[1][0]+output[1][1]).name},{Leds(2*output[2][0]+output[2][1]).name}] vs VHDL: [{Outputs(dut.OUTPUT.value).name},{Leds(dut.OK_LED.value).name},{Leds(dut.PWR_LED.value).name}]')
    '''
    for i in range(100000):
        if ( i % 5000 == 0 ):
            j = random.randint(0 , len(motorStates)-1)
            dut.MOTOR_STATE.value = BinaryValue(value=j,bits=8,bigEndian=False)
            output = movement_model(dut.PWM.value,dut.MOTOR_STATE.value)
            #print(f'{motorStates[j]} > Py:[{1*output[0]},{1*output[1]}{1*output[2]}] vs VHDL:[{dut.MOTOR_PWM.value},{dut.MOTOR_UPDOWN.value}]') 
                
        await FallingEdge(dut.PWM)  # Synchronize with the clock
        output = movement_model(dut.PWM.value,dut.MOTOR_STATE.value)
        await Timer(1, units="ns")
        #assert( output[0] == dut.MOTOR_PWM.value ), f'{output[0]} != {dut.MOTOR_PWM.value}'
        assert( [output[0],2*output[1]+output[2]] == [dut.MOTOR_PWM.value,dut.MOTOR_UPDOWN.value] ), f'{output} != [{dut.MOTOR_PWM.value},{dut.MOTOR_UPDOWN.value}]'
               
        await RisingEdge(dut.PWM)          
        output = movement_model(dut.PWM.value,dut.MOTOR_STATE.value)
        await Timer(1, units="ns")
        #assert( output[0] == dut.MOTOR_PWM.value ), f'{output[0]} != {dut.MOTOR_PWM.value}'
        assert( [output[0],2*output[1]+output[2]] == [dut.MOTOR_PWM.value,dut.MOTOR_UPDOWN.value] ), f'{output} != [{dut.MOTOR_PWM.value},{dut.MOTOR_UPDOWN.value}]'
    '''
    
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
