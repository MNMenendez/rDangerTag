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
    dut.CLOCK_STATE.value   = True
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
    dut.SYSTEM_STATE.value  = Deposit(Systems.SYSTEM_IDLE.value)
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
    
message = ""


@cocotb.test()
async def test_00(dut):
    """Functional test"""
    global message
    freq = 32.5
    startClock(dut,freq)
    
    initialize_rDT(dut)
    await Timer(100, units="ms")
    
    T = round(1000/freq,4)
    print(f'Frequency:{freq}kHz | Period:{T}us')
    
    sec     = 1
    cycle   = int(round(sec*1000000/T,0)+1)
    
    #print(dir(dut))
    
    for i in range(cycle):
        print(f'Functional test progress: {i/(cycle-1):2.1%}\r', end="\r")
        await RisingEdge(dut.CLOCK)
        
        if ( each_X_seconds(0.55,T,i) ):
            dut.KEY_I.value = random.randint(0 , 2)
        if ( each_X_seconds(0.25,T,i) ):
            dut.LOCK_I.value = random.randint(1 , 2) 
        if ( each_X_seconds(0.4,T,i) ):
            dut.PLC.value = random.randint(1 , 2) 
        if ( each_X_seconds(0.3,T,i) ):
            dut.SENSORS.value = random.randint(0 , 3)*5  
            
        CLOCK           =   dut.CLOCK
        CLOCK_STATE     =   dut.CLOCK_STATE.value
        POWER_MODE      =   dut.POWER_MODE.value
        BATT_STATE      =   dut.BATT_STATE.value
        KEY_ENABLE      =   dut.KEY_ENABLE.value
        KEY_I_A         =   (dut.KEY_I.value//2)%2
        KEY_I_B         =   dut.KEY_I.value%2
        KEY_O_A         =   (dut.KEY_O.value//2)%2
        KEY_O_B         =   dut.KEY_O.value%2
        LOCK_ENABLE     =   dut.LOCK_ENABLE.value
        LOCK_I_A        =   (dut.LOCK_I.value//2)%2
        LOCK_I_B        =   dut.LOCK_I.value%2
        PLC_I_A         =   (dut.PLC.value//2)%2
        PLC_I_B         =   dut.PLC.value%2
        PREVCOMMAND     =   dut.COMMAND_STATE.value
        SENSOR_1        =   (dut.SENSORS.value//8)%2
        SENSOR_2        =   (dut.SENSORS.value//4)%2
        SENSOR_3        =   (dut.SENSORS.value//2)%2
        SENSOR_4        =   dut.SENSORS.value%2
        oldMotor        =   dut.MOTOR_STATE.value
        oldState        =   dut.SYSTEM_STATE.value
        PREV_OUTPUT     =   dut.OUTPUT.value
        PREV_PWR_LED    =   dut.PWR_LED.value
        PREV_OK_LED     =   dut.OK_LED.value
        
        SLOWEST_CLOCK   =   dut.slowest_clock.value
         
        pyOUTPUT,pyPWR_LED,pyOK_LED,pyMOTOR,MOTOR_STATE,timer = general_model(
        POWER_MODE,BATT_STATE,
        KEY_ENABLE,KEY_O_A,KEY_O_B,
        LOCK_ENABLE,LOCK_I_A,LOCK_I_B,
        PLC_I_A,PLC_I_B,PREVCOMMAND,
        SENSOR_1,SENSOR_2,SENSOR_3,SENSOR_4,
        CLOCK,CLOCK_STATE,oldMotor,
        PREV_OUTPUT,PREV_PWR_LED,PREV_OK_LED,SLOWEST_CLOCK,oldState)           
        
        #await Timer(1, units="ns")
        
        OUTPUT_PASS     = pyOUTPUT  == dut.OUTPUT.value
        PWR_LED_PASS    = pyPWR_LED == dut.PWR_LED.value
        OK_LED_PASS     = pyOK_LED  == dut.OK_LED.value
        MOTOR_PASS      = pyMOTOR   == dut.MOTOR.value
        
        new_message = f'{Powers(dut.POWER_STATE.value).name}|{Locks(dut.LOCK_STATE.value).name}|{Keys(dut.KEY_STATE.value).name}|{PLCs(dut.PLC_STATE.value).name}|{Commands(dut.COMMAND_STATE.value).name}|{Sensors(dut.SENSOR_STATE.value).name}> Py: [{Outputs(pyOUTPUT).name}|{Leds(pyPWR_LED).name}|{Leds(pyOK_LED).name}|{Motors(pyMOTOR).name}] vs VHDL: [{Outputs(dut.OUTPUT.value).name}|{Leds(dut.PWR_LED.value).name}|{Leds(dut.OK_LED.value).name}|{Motors(dut.MOTOR.value).name}] --> <{1*OUTPUT_PASS},{1*PWR_LED_PASS},{1*OK_LED_PASS},{1*MOTOR_PASS}>'
        
        #if new_message != message:
        #    print(f'<{i/(cycle-1):2.1%}> {new_message}')
        #    message = new_message
            
        assert ( OUTPUT_PASS ), f'Py: {pyOUTPUT} != VHDL: {dut.OUTPUT.value}'
        assert ( PWR_LED_PASS ), f'Py: {pyPWR_LED} != VHDL: {dut.PWR_LED.value}'
        assert ( OK_LED_PASS ), f'Py: {pyOK_LED} != VHDL: {dut.OK_LED.value}'
        assert ( MOTOR_PASS ), f'Py: {pyMOTOR} != VHDL: {dut.MOTOR.value}'
                
    print(f'Functional test progress: {i/(cycle-1):2.1%}')
    reset_rDT(dut)
    
    await Timer(100, units="ms")

@cocotb.test()
async def test_01(dut):
    """Blackout test"""
    global message
    freq = 32.5
    startClock(dut,freq)
    
    initialize_rDT(dut)
    await Timer(100, units="ms")
    
    T = round(1000/freq,4)
    print(f'Frequency:{freq}kHz | Period:{T}us')
    
    sec     = 1
    cycle   = int(round(sec*1000000/T,0)+1)
    
   
    #print(dir(dut))
    
    for i in range(cycle):
        print(f'Blackout test progress: {i/(cycle-1):2.1%}\r', end="\r")
        await RisingEdge(dut.CLOCK)
        
        if ( each_X_seconds(0.55,T,i) ):
            dut.KEY_I.value = random.randint(0 , 2)
        if ( each_X_seconds(0.25,T,i) ):
            dut.LOCK_I.value = random.randint(1 , 2) 
        if ( each_X_seconds(0.4,T,i) ):
            dut.PLC.value = random.randint(1 , 2) 
        if ( each_X_seconds(0.3,T,i) ):
            dut.SENSORS.value = random.randint(0 , 3)*5  
        
        if ( each_X_seconds(0.5,T,i) ):
            dut.POWER_MODE.value = True if random.randint(1 , 100) < 50 else False
        if ( each_X_seconds(0.5,T,i) ):
            dut.BATT_STATE.value = True if random.randint(1 , 100) < 50 else False
            
        CLOCK           =   dut.CLOCK
        CLOCK_STATE     =   dut.CLOCK_STATE.value
        POWER_MODE      =   dut.POWER_MODE.value
        BATT_STATE      =   dut.BATT_STATE.value
        KEY_ENABLE      =   dut.KEY_ENABLE.value
        KEY_I_A         =   (dut.KEY_I.value//2)%2
        KEY_I_B         =   dut.KEY_I.value%2
        KEY_O_A         =   (dut.KEY_O.value//2)%2
        KEY_O_B         =   dut.KEY_O.value%2
        LOCK_ENABLE     =   dut.LOCK_ENABLE.value
        LOCK_I_A        =   (dut.LOCK_I.value//2)%2
        LOCK_I_B        =   dut.LOCK_I.value%2
        PLC_I_A         =   (dut.PLC.value//2)%2
        PLC_I_B         =   dut.PLC.value%2
        PREVCOMMAND     =   dut.COMMAND_STATE.value
        SENSOR_1        =   (dut.SENSORS.value//8)%2
        SENSOR_2        =   (dut.SENSORS.value//4)%2
        SENSOR_3        =   (dut.SENSORS.value//2)%2
        SENSOR_4        =   dut.SENSORS.value%2
        oldMotor        =   dut.MOTOR_STATE.value
        oldState        =   dut.SYSTEM_STATE.value
        PREV_OUTPUT     =   dut.OUTPUT.value
        PREV_PWR_LED    =   dut.PWR_LED.value
        PREV_OK_LED     =   dut.OK_LED.value
        
        SLOWEST_CLOCK   =   dut.slowest_clock.value
     
        pyOUTPUT,pyPWR_LED,pyOK_LED,pyMOTOR,MOTOR_STATE,timer = general_model(
        POWER_MODE,BATT_STATE,
        KEY_ENABLE,KEY_O_A,KEY_O_B,
        LOCK_ENABLE,LOCK_I_A,LOCK_I_B,
        PLC_I_A,PLC_I_B,PREVCOMMAND,
        SENSOR_1,SENSOR_2,SENSOR_3,SENSOR_4,
        CLOCK,CLOCK_STATE,oldMotor,
        PREV_OUTPUT,PREV_PWR_LED,PREV_OK_LED,SLOWEST_CLOCK,oldState)           
        
        #await Timer(1, units="ns")
        
        OUTPUT_PASS     = pyOUTPUT  == dut.OUTPUT.value
        PWR_LED_PASS    = pyPWR_LED == dut.PWR_LED.value
        OK_LED_PASS     = pyOK_LED  == dut.OK_LED.value
        MOTOR_PASS      = pyMOTOR   == dut.MOTOR.value
        
        new_message = f'{Powers(dut.POWER_STATE.value).name}|{Locks(dut.LOCK_STATE.value).name}|{Keys(dut.KEY_STATE.value).name}|{PLCs(dut.PLC_STATE.value).name}|{Commands(dut.COMMAND_STATE.value).name}|{Sensors(dut.SENSOR_STATE.value).name}> Py: [{Outputs(pyOUTPUT).name}|{Leds(pyPWR_LED).name}|{Leds(pyOK_LED).name}|{Motors(pyMOTOR).name}] vs VHDL: [{Outputs(dut.OUTPUT.value).name}|{Leds(dut.PWR_LED.value).name}|{Leds(dut.OK_LED.value).name}|{Motors(dut.MOTOR.value).name}] --> <{1*OUTPUT_PASS},{1*PWR_LED_PASS},{1*OK_LED_PASS},{1*MOTOR_PASS}>'
        
        #if new_message != message:
        #    print(f'<{i/(cycle-1):2.1%}> {new_message}')
        #    message = new_message
            
        assert ( OUTPUT_PASS ), f'Py: {pyOUTPUT} != VHDL: {dut.OUTPUT.value}'
        assert ( PWR_LED_PASS ), f'Py: {pyPWR_LED} != VHDL: {dut.PWR_LED.value}'
        assert ( OK_LED_PASS ), f'Py: {pyOK_LED} != VHDL: {dut.OK_LED.value}'
        assert ( MOTOR_PASS ), f'Py: {pyMOTOR} != VHDL: {dut.MOTOR.value}'
        
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
        
    print(f'Blackout test progress: {i/(cycle-1):2.1%}')
    reset_rDT(dut)
    
    await Timer(100, units="ms")
  
@cocotb.test()
async def test_02(dut):
    """Sensor fault test"""
    global message
    freq = 32.5
    startClock(dut,freq)
    
    initialize_rDT(dut)
    await Timer(100, units="ms")
    
    T = round(1000/freq,4)
    print(f'Frequency:{freq}kHz | Period:{T}us')
    
    sec     = 1
    cycle   = int(round(sec*1000000/T,0)+1)
    
   
    #print(dir(dut))
    
    for i in range(cycle):
        print(f'Sensor fault test progress: {i/(cycle-1):2.1%}\r', end="\r")
        await RisingEdge(dut.CLOCK)
        
        if ( each_X_seconds(0.55,T,i) ):
            dut.KEY_I.value = random.randint(0 , 2)
        if ( each_X_seconds(0.25,T,i) ):
            dut.LOCK_I.value = random.randint(1 , 2) 
        if ( each_X_seconds(0.4,T,i) ):
            dut.PLC.value = random.randint(1 , 2) 
        if ( each_X_seconds(0.3,T,i) ):
            SENSORS_GOOD= random.randint(0 , 3)*5  
        
        if ( each_X_seconds(0.35,T,i) ):
            dut.SENSORS.value = SENSORS_GOOD if random.randint(1 , 100) < 50 else random.randint(0 , 15)
            
        CLOCK           =   dut.CLOCK
        CLOCK_STATE     =   dut.CLOCK_STATE.value
        POWER_MODE      =   dut.POWER_MODE.value
        BATT_STATE      =   dut.BATT_STATE.value
        KEY_ENABLE      =   dut.KEY_ENABLE.value
        KEY_I_A         =   (dut.KEY_I.value//2)%2
        KEY_I_B         =   dut.KEY_I.value%2
        KEY_O_A         =   (dut.KEY_O.value//2)%2
        KEY_O_B         =   dut.KEY_O.value%2
        LOCK_ENABLE     =   dut.LOCK_ENABLE.value
        LOCK_I_A        =   (dut.LOCK_I.value//2)%2
        LOCK_I_B        =   dut.LOCK_I.value%2
        PLC_I_A         =   (dut.PLC.value//2)%2
        PLC_I_B         =   dut.PLC.value%2
        PREVCOMMAND     =   dut.COMMAND_STATE.value
        SENSOR_1        =   (dut.SENSORS.value//8)%2
        SENSOR_2        =   (dut.SENSORS.value//4)%2
        SENSOR_3        =   (dut.SENSORS.value//2)%2
        SENSOR_4        =   dut.SENSORS.value%2
        oldMotor        =   dut.MOTOR_STATE.value
        oldState        =   dut.SYSTEM_STATE.value
        PREV_OUTPUT     =   dut.OUTPUT.value
        PREV_PWR_LED    =   dut.PWR_LED.value
        PREV_OK_LED     =   dut.OK_LED.value
        
        SLOWEST_CLOCK   =   dut.slowest_clock.value
     
        pyOUTPUT,pyPWR_LED,pyOK_LED,pyMOTOR,MOTOR_STATE,timer = general_model(
        POWER_MODE,BATT_STATE,
        KEY_ENABLE,KEY_O_A,KEY_O_B,
        LOCK_ENABLE,LOCK_I_A,LOCK_I_B,
        PLC_I_A,PLC_I_B,PREVCOMMAND,
        SENSOR_1,SENSOR_2,SENSOR_3,SENSOR_4,
        CLOCK,CLOCK_STATE,oldMotor,
        PREV_OUTPUT,PREV_PWR_LED,PREV_OK_LED,SLOWEST_CLOCK,oldState)           
        
        #await Timer(1, units="ns")
        
        OUTPUT_PASS     = pyOUTPUT  == dut.OUTPUT.value
        PWR_LED_PASS    = pyPWR_LED == dut.PWR_LED.value
        OK_LED_PASS     = pyOK_LED  == dut.OK_LED.value
        MOTOR_PASS      = pyMOTOR   == dut.MOTOR.value
        
        new_message = f'{Powers(dut.POWER_STATE.value).name}|{Locks(dut.LOCK_STATE.value).name}|{Keys(dut.KEY_STATE.value).name}|{PLCs(dut.PLC_STATE.value).name}|{Commands(dut.COMMAND_STATE.value).name}|{Sensors(dut.SENSOR_STATE.value).name}> Py: [{Outputs(pyOUTPUT).name}|{Leds(pyPWR_LED).name}|{Leds(pyOK_LED).name}|{Motors(pyMOTOR).name}] vs VHDL: [{Outputs(dut.OUTPUT.value).name}|{Leds(dut.PWR_LED.value).name}|{Leds(dut.OK_LED.value).name}|{Motors(dut.MOTOR.value).name}] --> <{1*OUTPUT_PASS},{1*PWR_LED_PASS},{1*OK_LED_PASS},{1*MOTOR_PASS}>'
        
        #if new_message != message:
        #    print(f'<{i/(cycle-1):2.1%}> {new_message}')
        #    message = new_message
            
        assert ( OUTPUT_PASS ), f'Py: {pyOUTPUT} != VHDL: {dut.OUTPUT.value}'
        assert ( PWR_LED_PASS ), f'Py: {pyPWR_LED} != VHDL: {dut.PWR_LED.value}'
        assert ( OK_LED_PASS ), f'Py: {pyOK_LED} != VHDL: {dut.OK_LED.value}'
        assert ( MOTOR_PASS ), f'Py: {pyMOTOR} != VHDL: {dut.MOTOR.value}'
        
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
        
    print(f'Sensor fault test progress: {i/(cycle-1):2.1%}')
    reset_rDT(dut)
    
    await Timer(100, units="ms")
 
@cocotb.test()
async def test_03(dut):
    """Key fault test"""
    global message
    freq = 32.5
    startClock(dut,freq)
    
    initialize_rDT(dut)
    await Timer(100, units="ms")
    
    T = round(1000/freq,4)
    print(f'Frequency:{freq}kHz | Period:{T}us')
    
    sec     = 10
    cycle   = int(round(sec*1000000/T,0)+1)
    
    for i in range(cycle):
        print(f'Key fault test progress: {i/(cycle-1):2.1%}\r', end="\r")
        await RisingEdge(dut.CLOCK)
        
        if ( each_X_seconds(0.55,T,i) ):
            KEY_GOOD = random.randint(0 , 2)
        if ( each_X_seconds(0.25,T,i) ):
            dut.LOCK_I.value = random.randint(1 , 2) 
        if ( each_X_seconds(0.4,T,i) ):
            dut.PLC.value = random.randint(1 , 2) 
        if ( each_X_seconds(0.3,T,i) ):
             dut.SENSORS.value= random.randint(0 , 3)*5  
        
        if ( each_X_seconds(0.35,T,i) ):
            dut.KEY_I.value = KEY_GOOD if random.randint(1 , 100) < 50 else 3
            
        CLOCK           =   dut.CLOCK
        CLOCK_STATE     =   dut.CLOCK_STATE.value
        POWER_MODE      =   dut.POWER_MODE.value
        BATT_STATE      =   dut.BATT_STATE.value
        KEY_ENABLE      =   dut.KEY_ENABLE.value
        KEY_I_A         =   (dut.KEY_I.value//2)%2
        KEY_I_B         =   dut.KEY_I.value%2
        KEY_O_A         =   (dut.KEY_O.value//2)%2
        KEY_O_B         =   dut.KEY_O.value%2
        LOCK_ENABLE     =   dut.LOCK_ENABLE.value
        LOCK_I_A        =   (dut.LOCK_I.value//2)%2
        LOCK_I_B        =   dut.LOCK_I.value%2
        PLC_I_A         =   (dut.PLC.value//2)%2
        PLC_I_B         =   dut.PLC.value%2
        PREVCOMMAND     =   dut.COMMAND_STATE.value
        SENSOR_1        =   (dut.SENSORS.value//8)%2
        SENSOR_2        =   (dut.SENSORS.value//4)%2
        SENSOR_3        =   (dut.SENSORS.value//2)%2
        SENSOR_4        =   dut.SENSORS.value%2
        oldMotor        =   dut.MOTOR_STATE.value
        oldState        =   dut.SYSTEM_STATE.value
        PREV_OUTPUT     =   dut.OUTPUT.value
        PREV_PWR_LED    =   dut.PWR_LED.value
        PREV_OK_LED     =   dut.OK_LED.value
        
        SLOWEST_CLOCK   =   dut.slowest_clock.value
     
        pyOUTPUT,pyPWR_LED,pyOK_LED,pyMOTOR,MOTOR_STATE,timer = general_model(
        POWER_MODE,BATT_STATE,
        KEY_ENABLE,KEY_O_A,KEY_O_B,
        LOCK_ENABLE,LOCK_I_A,LOCK_I_B,
        PLC_I_A,PLC_I_B,PREVCOMMAND,
        SENSOR_1,SENSOR_2,SENSOR_3,SENSOR_4,
        CLOCK,CLOCK_STATE,oldMotor,
        PREV_OUTPUT,PREV_PWR_LED,PREV_OK_LED,SLOWEST_CLOCK,oldState)           
        
        #await Timer(1, units="ns")
        
        OUTPUT_PASS     = pyOUTPUT  == dut.OUTPUT.value
        PWR_LED_PASS    = pyPWR_LED == dut.PWR_LED.value
        OK_LED_PASS     = pyOK_LED  == dut.OK_LED.value
        MOTOR_PASS      = pyMOTOR   == dut.MOTOR.value
        
        new_message = f'{Powers(dut.POWER_STATE.value).name}|{Locks(dut.LOCK_STATE.value).name}|{Keys(dut.KEY_STATE.value).name}|{PLCs(dut.PLC_STATE.value).name}|{Commands(dut.COMMAND_STATE.value).name}|{Sensors(dut.SENSOR_STATE.value).name}> Py: [{Outputs(pyOUTPUT).name}|{Leds(pyPWR_LED).name}|{Leds(pyOK_LED).name}|{Motors(pyMOTOR).name}] vs VHDL: [{Outputs(dut.OUTPUT.value).name}|{Leds(dut.PWR_LED.value).name}|{Leds(dut.OK_LED.value).name}|{Motors(dut.MOTOR.value).name}] --> <{1*OUTPUT_PASS},{1*PWR_LED_PASS},{1*OK_LED_PASS},{1*MOTOR_PASS}>'
        
        if new_message != message:
            print(f'<{i/(cycle-1):2.1%}> {new_message}')
            message = new_message
            
        assert ( OUTPUT_PASS ), f'Py: {pyOUTPUT} != VHDL: {dut.OUTPUT.value}'
        assert ( PWR_LED_PASS ), f'Py: {pyPWR_LED} != VHDL: {dut.PWR_LED.value}'
        assert ( OK_LED_PASS ), f'Py: {pyOK_LED} != VHDL: {dut.OK_LED.value}'
        assert ( MOTOR_PASS ), f'Py: {pyMOTOR} != VHDL: {dut.MOTOR.value}'
        
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
        
    print(f'Key fault test progress: {i/(cycle-1):2.1%}')
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
