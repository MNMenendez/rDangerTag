# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0


import cocotb
from cocotb.types import Bit, Logic
import enum

class Powers(enum.Enum):
    POWER_BATTERY       = 0
    POWER_ON            = 1

class Modes(enum.Enum):
    MODE_ERROR          = 0
    REMOTE              = 1
    LOCAL_APPLY         = 2
    LOCAL_REMOVE        = 3

class Sensors(enum.Enum):
       SENSOR_ERROR     = 0
       DANGER           = 1
       BLANK            = 2
       TRANSITION       = 3
       
class Commands(enum.Enum):
    COMMAND_ERROR       = 0
    COMMAND_IGNORE      = 1
    COMMAND_APPLY       = 2
    COMMAND_REMOVE      = 3
class Systems(enum.Enum):
    SYSTEM_ERROR        = 0
    SYSTEM_DANGER       = 1
    SYSTEM_BLANK        = 2
    SYSTEM_BATTERY      = 3
class Rights(enum.Enum):
    FAULT               = 0
    ALIVE               = 1

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
    
    return KEY_A_O,KEY_B_O,MODE_STATE.value

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
    return SENSOR_STATE.value
    
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
            
    return COMMAND_STATE.value
    
def lock_model(LOCK: Logic = Logic('-'), LOCK_A_I: Logic = Logic('-'), LOCK_B_I: Logic = Logic('-')):
    """model of lock"""

    if LOCK == True:
        LOCK_A_O = LOCK_A_I
        LOCK_B_O = LOCK_B_I
    else:
        LOCK_A_O = False
        LOCK_B_O = False
        
    return [LOCK_A_O,LOCK_B_O]
    
def system_model(POWER_STATE: int = Powers.POWER_BATTERY, MODE_STATE: int = Modes.MODE_ERROR , COMMAND_STATE: int = Commands.COMMAND_ERROR , SENSOR_STATE: int = Sensors.SENSOR_ERROR):


    SYSTEM_STATE = Systems.SYSTEM_ERROR
    ALL_OK = Rights.FAULT
    
    if (POWER_STATE == Powers.POWER_BATTERY):
        SYSTEM_STATE = Systems.SYSTEM_BATTERY;
    
    
    return [SYSTEM_STATE,ALL_OK]
