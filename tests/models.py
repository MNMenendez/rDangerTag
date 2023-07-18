# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0


import cocotb
from cocotb.types import Bit, Logic
import enum

class Powers(enum.Enum):
    POWER_OFF           = 0
    POWER_ON            = 1
    BATTERY             = 2
    BATTERY_LOW         = 3
class PLCs(enum.Enum):
    PLC_ERROR           = 0
    PLC_APPLY           = 1
    PLC_REMOVE          = 2
    PLC_IDLE            = 3
class Keys(enum.Enum):
    KEY_ERROR           = 0
    KEY_APPLY           = 1
    KEY_REMOVE          = 2
    NO_KEY              = 3
class Sensors(enum.Enum):
    SENSOR_ERROR        = 0
    DANGER              = 1
    BLANK               = 2
    TRANSITION          = 3
class Commands(enum.Enum):
    COMMAND_ERROR       = 0
    COMMAND_APPLY       = 1
    COMMAND_REMOVE      = 2
    COMMAND_IDLE        = 3
class Systems(enum.Enum):
    SYSTEM_ERROR        = 0
    SYSTEM_DANGER       = 1
    SYSTEM_BLANK        = 2
    SYSTEM_TRANSITION   = 3
    SYSTEM_TIMEOUT      = 4
    SYSTEM_IDLE         = 5 
class Rights(enum.Enum):
    FAULT               = 0
    ALIVE               = 1
class Motors(enum.Enum):
    STOP               = 0
    toDANGER           = 1
    toBLANK            = 2
class Locks(enum.Enum):
    LOCK_ERROR         = 0
    LOCK_APPLY         = 1
    LOCK_REMOVE        = 2
    NO_LOCK            = 3
class Leds(enum.Enum):
    RED                = 0
    AMBER              = 1
    FLASHING           = 2
    GREEN              = 3
class Outputs(enum.Enum):
    ERROR              = 0
    DANGER             = 1
    BLANK              = 2
    CATASTROPHIC_FAILURE = 3

def tuple_create(n_inputs,n):
    return ((False,)*n+(True,)*n)*((2**n_inputs)//(2*n))
    
def dummy_model(TBD_I: Logic = Logic('-')) -> int:
    """model of dummy"""
    return TBD_I
    
def power_model(POWER_MODE: Logic = Logic('-'), BATTERY_STATE: Logic = Logic('-')) -> int:
    """model of power"""
    POWER_STATE = Powers.POWER_OFF
    if ( not POWER_MODE and not BATTERY_STATE):
        POWER_STATE = Powers.POWER_OFF
    if ( not POWER_MODE and BATTERY_STATE):
        POWER_STATE = Powers.BATTERY
    if ( POWER_MODE and not BATTERY_STATE):
        POWER_STATE = Powers.BATTERY_LOW
    if ( POWER_MODE and BATTERY_STATE):
        POWER_STATE = Powers.POWER_ON
        
    return POWER_STATE.value

def lock_model(LOCK: Logic = Logic('-'), LOCK_A_I: Logic = Logic('-'), LOCK_B_I: Logic = Logic('-')):
    """model of lock"""
    
    LOCK_STATE = Locks.NO_LOCK 
    
    if (LOCK):
        LOCK_STATE = Locks.NO_LOCK 
        LOCK_A_O = LOCK_A_I
        LOCK_B_O = LOCK_B_I
    else:
        if ( not LOCK_A_I and not LOCK_B_I ):
            LOCK_STATE = Locks.LOCK_ERROR
            LOCK_A_O = LOCK_A_I
            LOCK_B_O = LOCK_B_I
        if ( not LOCK_A_I and LOCK_B_I ):
            LOCK_STATE = Locks.LOCK_APPLY
            LOCK_A_O = LOCK_A_I
            LOCK_B_O = LOCK_B_I
        if ( LOCK_A_I and not LOCK_B_I ):
            LOCK_STATE = Locks.LOCK_REMOVE
            LOCK_A_O = LOCK_A_I
            LOCK_B_O = LOCK_B_I
        if ( LOCK_A_I and LOCK_B_I ):
            LOCK_STATE = Locks.LOCK_ERROR  
            LOCK_A_O = LOCK_A_I
            LOCK_B_O = LOCK_B_I
    
    return LOCK_A_O,LOCK_B_O,LOCK_STATE.value
    
def key_model(KEY: Logic = Logic('-'), KEY_A_I: Logic = Logic('-'), KEY_B_I: Logic = Logic('-')):
    """model of key"""
    
    KEY_A_O = KEY_A_I
    KEY_B_O = KEY_B_I
    KEY_STATE = Keys.KEY_ERROR 
    
    if (KEY):
        KEY_STATE = Keys.NO_KEY
    else:
        if ( not KEY_A_I and not KEY_B_I ):
            KEY_STATE = Keys.NO_KEY
        if ( not KEY_A_I and KEY_B_I ):
            KEY_STATE = Keys.KEY_APPLY
        if ( KEY_A_I and not KEY_B_I ):
            KEY_STATE = Keys.KEY_REMOVE
        if ( KEY_A_I and KEY_B_I ):
            KEY_STATE = Keys.KEY_ERROR    
    
    return KEY_A_O,KEY_B_O,KEY_STATE.value

def sensor_model(SENSOR_1: Logic = Logic('-'), SENSOR_2: Logic = Logic('-'), SENSOR_3: Logic = Logic('-'), SENSOR_4: Logic = Logic('-')):
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
    
def plc_model(PLC_I_A: Logic = Logic('-'), PLC_I_B: Logic = Logic('-')):
    """model of plcs"""
        
    PLC_STATE = PLCs.PLC_IDLE
    
    if (not PLC_I_A and PLC_I_B):
        PLC_STATE = PLCs.PLC_APPLY
    if (PLC_I_A and not PLC_I_B):
        PLC_STATE = PLCs.PLC_REMOVE    
    if (PLC_I_A == PLC_I_B):
        PLC_STATE = PLCs.PLC_ERROR
        
    return PLC_STATE.value
 
def ff_model(CLOCK: Logic = Logic('-'), RESET: Logic = Logic('-')):
    """model of flip flop D"""
        
    Q : LOGIC = Logic('u')
    
    if ( CLOCK ):
        if RESET:
            Q = False
        else:
            Q = not CLOCK       
        
    return Q
    
def command_model( KEY: int = Keys.NO_KEY, PLC: int = PLCs.PLC_IDLE, LOCK: int = Locks.NO_LOCK , PREVCOMMAND: int = Commands.COMMAND_IDLE ):
    """model of commands"""
     
    APPLY_VALID = True if ((LOCK == Locks.LOCK_APPLY or LOCK == Locks.NO_LOCK) and ( KEY == Keys.KEY_APPLY or ( KEY == Keys.NO_KEY and PLC == PLCs.PLC_APPLY ) ) ) else False
    REMOVE_VALID = True if ((LOCK == Locks.LOCK_REMOVE or LOCK == Locks.NO_LOCK) and ( KEY == Keys.KEY_REMOVE or ( KEY == Keys.NO_KEY and PLC == PLCs.PLC_REMOVE ) ) ) else False
    CMD_INVALID = True if (LOCK == Locks.LOCK_ERROR or KEY == Keys.KEY_ERROR or ( KEY == Keys.NO_KEY and PLC == PLCs.PLC_ERROR ) ) else False   
    
    #print(KEY,PLC,LOCK,PREVCOMMAND,APPLY_VALID,REMOVE_VALID,CMD_INVALID)
    
    if ( PREVCOMMAND == Commands.COMMAND_ERROR ):
        COMMAND_STATE = Commands.COMMAND_ERROR
        return COMMAND_STATE.value
        
    if ( CMD_INVALID ):
        COMMAND_STATE = Commands.COMMAND_ERROR
    else:
        if ( not APPLY_VALID and not REMOVE_VALID ):
            COMMAND_STATE = Commands.COMMAND_IDLE
        if ( not APPLY_VALID and REMOVE_VALID ):
            COMMAND_STATE = Commands.COMMAND_REMOVE
        if ( APPLY_VALID and not REMOVE_VALID ):
            COMMAND_STATE = Commands.COMMAND_APPLY
        if ( APPLY_VALID and REMOVE_VALID ):
            COMMAND_STATE = Commands.COMMAND_ERROR
 
     
    return COMMAND_STATE.value
    
'''        
def system_model(POWER_STATE: int = Powers.POWER_OFF, MODE_STATE: int = Modes.MODE_ERROR, COMMAND_STATE: int = Commands.COMMAND_ERROR, SENSOR_STATE: int = Sensors.SENSOR_ERROR):

    SYSTEM_STATE = Systems.SYSTEM_ERROR
    ALL_OK = Rights.FAULT
    
    if (POWER_STATE == Powers.POWER_BATTERY.value):
        SYSTEM_STATE = Systems.SYSTEM_BATTERY
    else:
        if (MODE_STATE == Modes.MODE_ERROR.value or COMMAND_STATE == Commands.COMMAND_ERROR.value or SENSOR_STATE == Sensors.SENSOR_ERROR.value):
            SYSTEM_STATE = Systems.SYSTEM_ERROR
            ALL_OK       = Rights.FAULT
        else:
            ALL_OK       = Rights.ALIVE
            match SENSOR_STATE:
                case Sensors.DANGER.value:
                    SYSTEM_STATE = Systems.SYSTEM_DANGER
                case Sensors.BLANK.value:
                    SYSTEM_STATE = Systems.SYSTEM_BLANK 
                case Sensors.TRANSITION.value:
                    SYSTEM_STATE = Systems.SYSTEM_TRANSITION
                case _:
                    SYSTEM_STATE = Systems.SYSTEM_ERROR
            
    return [SYSTEM_STATE.value,ALL_OK.value]
'''

def output_model(SYSTEM_STATE: int = Systems.SYSTEM_IDLE, POWER_STATE: int = Powers.POWER_OFF, SLOWEST_CLOCK: Logic = Logic('-'), PREV_OUTPUT = [False,False],PREV_PWR_LED =[False,False],PREV_OK_LED=[False,False]):
    
    
    PWR_LED_SIGNAL = Leds.RED
    OK_LED_SIGNAL  = Leds.RED
    
    match SYSTEM_STATE:
        case Systems.SYSTEM_ERROR.value:
            OUTPUT = [False,False]
        case Systems.SYSTEM_DANGER.value:
            OUTPUT = [False,True]
        case Systems.SYSTEM_BLANK.value:
            OUTPUT = [True,False]
        case Systems.SYSTEM_TRANSITION.value:
            OUTPUT = PREV_OUTPUT
        case Systems.SYSTEM_TIMEOUT.value:
            OUTPUT = [False,False]
        case Systems.SYSTEM_IDLE.value:
            OUTPUT = [False,False]
        case _:
            OUTPUT = [True,True]
    
    match POWER_STATE:
        case Powers.POWER_OFF.value:
            PWR_LED_SIGNAL = Leds.RED.value
        case Powers.POWER_ON.value:
            PWR_LED_SIGNAL = Leds.GREEN.value
        case Powers.BATTERY.value:
            PWR_LED_SIGNAL = Leds.AMBER.value
        case Powers.BATTERY_LOW.value:
            PWR_LED_SIGNAL = Leds.GREEN.value
        case _:
            PWR_LED_SIGNAL = Leds.RED.value
    
    if SYSTEM_STATE == Systems.SYSTEM_ERROR.value:
        OK_LED_SIGNAL  = Leds.RED.value
    else:
        if POWER_STATE == Powers.POWER_ON.value or POWER_STATE == Powers.BATTERY.value:
            OK_LED_SIGNAL  = Leds.GREEN.value
        elif POWER_STATE == Powers.BATTERY_LOW.value:
            OK_LED_SIGNAL  = Leds.FLASHING.value
        else:
            OK_LED_SIGNAL  = Leds.RED.value
    
    if SLOWEST_CLOCK:
        match PWR_LED_SIGNAL:
            case Leds.RED.value:
                PREV_PWR_LED = [False,False]
            case Leds.AMBER.value:
                PREV_PWR_LED = [True,False]
            case Leds.FLASHING.value:
                PREV_PWR_LED = [PREV_PWR_LED[1] , not PREV_PWR_LED[0]]
            case Leds.GREEN.value:
                PREV_PWR_LED = [True,True]
            case _:
                PREV_PWR_LED = PREV_PWR_LED
        
        match OK_LED_SIGNAL:
            case Leds.RED.value:
                PREV_OK_LED = [False,False]
            case Leds.AMBER.value:
                PREV_OK_LED = [True,False]
            case Leds.FLASHING.value:
                PREV_OK_LED = [PREV_OK_LED[0], not PREV_OK_LED[1]]
            case Leds.GREEN.value:
                PREV_OK_LED = [True,True]
            case _:
                PREV_OK_LED = PREV_OK_LED
                
    PWR_LED = PREV_PWR_LED
    OK_LED = PREV_OK_LED
    
    return [OUTPUT,PWR_LED,OK_LED]

counter = 0
def clock_model(CLOCK: Logic = Logic('-'), CLOCK_STATE: Logic = Logic('-')):
    
    global counter
    PWM = False
    WATCHDOG = True if CLOCK_STATE else False
    
    if CLOCK_STATE == False:
        counter = 0
    else:
        if CLOCK:
            counter = counter + 1
        if counter > 16:
            counter = 0
            PWM = True
        if counter >= 12:
            PWM = False
        else:
            PWM = True

    #print(CLOCK_STATE,CLOCK,counter,WATCHDOG,PWM)
    
    return [WATCHDOG,PWM]
    
def movement_model(PWM: Logic = Logic('-'), MOTOR_STATE: int = Motors.STOP):
    
    #print(f'Receive: {PWM} {Motors(int(MOTOR_STATE))}')
    
    match MOTOR_STATE:
        case Motors.STOP.value:
            MOTOR_PWM = False
            MOTOR_UP = False
            MOTOR_DOWN = False
        case Motors.toDANGER.value:
            MOTOR_PWM = PWM
            MOTOR_UP = True
            MOTOR_DOWN = False
        case Motors.toBLANK.value:
            MOTOR_PWM = PWM
            MOTOR_UP = False
            MOTOR_DOWN = True
        case _:
            MOTOR_PWM = False
            MOTOR_UP = False
            MOTOR_DOWN = False
    
    return [MOTOR_PWM,MOTOR_UP,MOTOR_DOWN]
    
def general_model(POWER_MODE: Logic = Logic('-'),KEY: Logic = Logic('-'), KEY_A_I: Logic = Logic('-'), KEY_B_I: Logic = Logic('-'),SENSOR_1: Logic = Logic('-'), SENSOR_2: Logic = Logic('-'), SENSOR_3: Logic = Logic('X'), SENSOR_4: Logic = Logic('-'),INPUT_A: Logic = Logic('-'), INPUT_B: Logic = Logic('-'),LOCK: Logic = Logic('-'),LOCK_A_I: Logic = Logic('-'), LOCK_B_I: Logic = Logic('-'),CLOCK: Logic = Logic('-'), CLOCK_STATE: Logic = Logic('-'),TBD_I: Logic = Logic('-')):

    POWER_STATE                     = power_model(POWER_MODE)
    TBD_O                           = dummy_model(TBD_I)
    KEY_A_O,KEY_B_O,MODE_STATE      = key_model(KEY, KEY_A_I, KEY_B_I)
    SENSOR_STATE                    = sensor_model(SENSOR_1, SENSOR_2, SENSOR_3, SENSOR_4)
    COMMAND_STATE                   = command_model(INPUT_A, INPUT_B, MODE_STATE)
    SYSTEM_STATE,ALL_OK             = system_model(POWER_STATE, MODE_STATE, COMMAND_STATE, SENSOR_STATE)
    WATCHDOG,PWM                    = clock_model(CLOCK, CLOCK_STATE)
    LOCK_A_O,LOCK_B_O               = lock_model(LOCK, LOCK_A_I, LOCK_B_I)
    OUTPUT_A,OUTPUT_B               = output_model(SYSTEM_STATE)
    MOTOR_STATE                     = motor_model(LOCK, MODE_STATE, COMMAND_STATE, SENSOR_STATE)
    MOTOR_PWM,MOTOR_UP,MOTOR_DOWN   = movement_model(PWM, MOTOR_STATE)
    
    return [KEY_A_O,KEY_B_O,LOCK_A_O,LOCK_B_O,ALL_OK,WATCHDOG,OUTPUT_A,OUTPUT_B,MOTOR_PWM,MOTOR_UP,MOTOR_DOWN,TBD_O]
