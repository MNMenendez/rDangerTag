# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))),**named)
    return type('Enum',(),enums)

Modes = enum('ERROR_MODE','REMOTE','LOCAL_APPLY','LOCAL_REMOVE')
Sensors = enum('ERROR_SENSOR','DANGER','BLANK')


def dummy_model(TBD_I: int) -> int:
    """model of dummy"""
    return TBD_I
    
def power_model(POWER_MODE: int) -> int:
    """model of power"""
    if POWER_MODE:
        return True
    else:
        return False
        
def key_model(KEY: bool, KEY_A_I: bool = False, KEY_B_I: bool = False):
    """model of key"""
    
    KEY_A_O = KEY_A_I
    KEY_B_O = KEY_B_I
    
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
            MODE_STATE = Modes.ERROR_MODE    
    
    return KEY_A_O,KEY_B_O,MODE_STATE

