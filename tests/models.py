# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0


import cocotb
from cocotb.types import Bit, Logic

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))),**named)
    return type('Enum',(),enums)

Modes = enum('MODE_ERROR','REMOTE','LOCAL_APPLY','LOCAL_REMOVE')
Sensors = enum('SENSOR_ERROR','DANGER','BLANK','TRANSITION')
Commands = enum('COMMAND_ERROR','COMMAND_IGNORE','COMMAND_APPLY','COMMAND_REMOVE')

def dummy_model(TBD_I: Logic = Logic('-')) -> int:
    """model of dummy"""
    return TBD_I
    
def power_model(POWER_MODE: Logic = Logic('-')) -> int:
    """model of power"""
    if POWER_MODE:
        return True
    else:
        return False
        
def key_model(KEY: Logic = Logic('-'), KEY_A_I: Logic = Logic('-'), KEY_B_I: Logic = Logic('-')):
    """model of key"""
    
    KEY_A_O = KEY_A_I
    KEY_B_O = KEY_B_I
    MODE_STATE = Modes.MODE_ERROR 
    
    if (not KEY):
        MODE_STATE = Modes.REMOTE
    else:
        if ( not KEY_A_I and not KEY_B_I ):
            MODE_STATE = Modes.REMOTE
        if ( not KEY_A_I and KEY_B_I ):
            MODE_STATE = Modes.LOCAL_APPLY
        if ( KEY_A_I and not KEY_B_I ):
            MODE_STATE = Modes.LOCAL_REMOVE
        if ( KEY_A_I and KEY_B_I ):
            MODE_STATE = Modes.MODE_ERROR    
    
    return KEY_A_O,KEY_B_O,MODE_STATE

def sensor_model(SENSOR_1: Logic = Logic('-'), SENSOR_2: Logic = Logic('-'), SENSOR_3: Logic = Logic('X'), SENSOR_4: Logic = Logic('-')):
    """model of sensors"""
        
    SENSOR_STATE = Sensors.SENSOR_ERROR
    
    if (SENSOR_1 != SENSOR_3 or SENSOR_2 != SENSOR_4):
        SENSOR_STATE = Sensors.SENSOR_ERROR
    if (SENSOR_1 == True and SENSOR_2 == False and SENSOR_3 == True and SENSOR_4 == False):
        SENSOR_STATE = Sensors.DANGER
    if (SENSOR_1 == False and SENSOR_2 == True and SENSOR_3 == False and SENSOR_4 == True):
        SENSOR_STATE = Sensors.BLANK   
    if (SENSOR_1 == SENSOR_3 == SENSOR_2 == SENSOR_4):
        SENSOR_STATE = Sensors.TRANSITION
    return SENSOR_STATE
    
def command_model(INPUT_A: Logic = Logic('-'), INPUT_B: Logic = Logic('-'), MODE_STATE: int = Modes.MODE_ERROR ):
    """model of commands"""
    
    COMMAND_STATE = Commands.COMMAND_ERROR
    
    if ( MODE_STATE != Modes.REMOTE ):
        COMMAND_STATE = Commands.COMMAND_IGNORE
    else:
        if ( INPUT_A == INPUT_B ):
            COMMAND_STATE = Commands.COMMAND_ERROR
        if ( INPUT_A == False and INPUT_B == True ):
            COMMAND_STATE = Commands.COMMAND_APPLY
        if ( INPUT_A == True and INPUT_B == False ):
            COMMAND_STATE = Commands.COMMAND_REMOVE
            
    return COMMAND_STATE
    
def lock_model(LOCK: Logic = Logic('-'), LOCK_A_I: Logic = Logic('-'), LOCK_B_I: Logic = Logic('-')):
    """model of lock"""

    if LOCK == True:
        LOCK_A_O = LOCK_A_I
        LOCK_B_O = LOCK_B_I
    else:
        LOCK_A_O = False
        LOCK_B_O = False
        
    return [LOCK_A_O,LOCK_B_O]
