# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0
# Simple tests for an dummy module
import os
import random
import sys
from pathlib import Path

import cocotb
from cocotb.runner import get_runner
from cocotb.triggers import Timer, FallingEdge, RisingEdge
from cocotb.types import Bit, Logic
from cocotb.binary import BinaryValue
from cocotb.clock import Clock
from cocotb.utils import get_sim_steps, get_time_from_sim_steps, lazy_property
from cocotb.handle import Force, Release, Deposit	
			
if cocotb.simulator.is_running():
    from models import *

def startClock(dut,freq):
    clock = Clock(dut.CLOCK, round(1000/freq,4), units="us")  # Create a 30us period clock on port clk
    cocotb.start_soon(clock.start(start_high = False))  # Start the clock
    
def initialize_rDT(dut):
    #inputs
    dut.CLOCK_STATE.value  = True
    dut.POWER_MODE.value    = True
    dut.BATT_STATE.value    = True
    dut.KEY_ENABLE.value    = False     # Negative logic
    dut.LOCK_ENABLE.value   = False     # Negative logic
    dut.SENSORS.value       = 0
    dut.KEY_I.value         = 0
    dut.LOCK_I.value        = 1
    dut.PLC.value           = 1

def reset_rDT(dut):
    #inputs
    initialize_rDT(dut)

    #outputs
    #dut.TBD_O.value         =   Deposit(0)
    #dut.KEY_O.value         =   Deposit(0)
    #dut.LOCK_O.value        =   Deposit(0)
    #dut.OUTPUT.value        =   Deposit(0)
    #dut.PWR_LED.value       =   Deposit(0)
    #dut.OK_LED.value        =   Deposit(0)
    #dut.MOTOR.value         =   Deposit(0)
    #dut.MOTOR_PWM.value     =   Deposit(0)
    #dut.WATCHDOG.value      =   Deposit(0)
    
def each_X_seconds(sec,T,i):
    
    cycle = round(sec*1000000/T,0)+1
    #print(f'{T}us {sec}s {i}={i*T/1000000}|{cycle}')
    #if ( i % cycle == 0 ):
        #print(f'\t{round(i*T/1000000,2)}sec')
 
    return (i % cycle == 0)
    
@cocotb.test()
async def test_00(dut):
    """Clock test"""
    freq = 32.5
    startClock(dut,freq)
    
    initialize_rDT(dut)
    await Timer(100, units="ms")
    
    T = round(1000/freq,4)
    print(f'Frequency:{freq}kHz | Period:{T}us')
    
    sec     = 3
    cycle   = int(round(sec*1000000/T,0)+1)
    
    for i in range(cycle):
        print(f'Clock test progress: {i/(cycle-1):2.1%}\r', end="\r")
        await RisingEdge(dut.CLOCK)
        
        if ( each_X_seconds(0.5,T,i) ):
            dut.KEY_I.value = random.randint(0 , 2)
        if ( each_X_seconds(0.25,T,i) ):
            dut.LOCK_I.value = random.randint(1 , 2) 
        if ( each_X_seconds(0.4,T,i) ):
            dut.PLC.value = random.randint(1 , 2) 
        if ( each_X_seconds(0.3,T,i) ):
            dut.SENSORS.value = random.randint(0 , 3)*5  
            
        '''
        if ( each_X_seconds(0.5,T,i) ):
            dut.POWER_MODE.value = True if random.randint(1 , 100) < 99 else False
        dut.CLOCK_ENABLE.value = not dut.CLOCK_ENABLE.value
        dut.POWER_MODE.value = not dut.POWER_MODE.value
        dut.BATT_STATE.value = not dut.BATT_STATE.value
        dut.KEY_ENABLE.value = not dut.KEY_ENABLE.value
        dut.LOCK_ENABLE.value = not dut.LOCK_ENABLE.value
        
        sensor = random.randint(0 , 16-1)
        dut.SENSORS.value = sensor
        
        key = random.randint(0 , 4-1)
        dut.KEY_I.value = key
        
        lock = random.randint(0 , 4-1)
        dut.LOCK_I.value = lock
        
        plc = random.randint(0 , 4-1)
        dut.PLC.value = plc
        '''
        
    print('')
    reset_rDT(dut)
    
    
    await Timer(100, units="ms")
  
@cocotb.test()
async def test_01(dut):
    """Clock test"""
    startClock(dut,32.5)
    
    initialize_rDT(dut)
    await Timer(100, units="ms")
    
    for i in range(10000):
        print(f'Clock test progress: {i/(10000-1):2.1%}\r', end="\r")
        await RisingEdge(dut.CLOCK)
        
        sensor = random.randint(0 , 16-1)
        dut.SENSORS.value = sensor
        
        
    print('')
    reset_rDT(dut)
    
    
    await Timer(100, units="ms")  
  
  
    
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
        verilog_sources = [proj_path / "hdl" / "rdangertag.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "rdangertag.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="rdangertag",
        always=True,
    )
    runner.test(hdl_toplevel="rdangertag", test_module="test_general")


if __name__ == "__main__":
    test_general_runner()
