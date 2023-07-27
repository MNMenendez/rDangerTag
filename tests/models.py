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
    OFF                = 0
    RED                = 1
    GREEN              = 2
    AMBER              = 3
    FLASHING           = 4
class Outputs(enum.Enum):
    ERROR              = 0
    DANGER             = 1
    BLANK              = 2
    IDLE               = 3

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
    
    if ( PREVCOMMAND == Commands.COMMAND_ERROR.value ):
        COMMAND_STATE = Commands.COMMAND_ERROR
        #print(f'{Locks(LOCK).name}+{Keys(KEY).name}+{PLCs(PLC).name}+{Commands(PREVCOMMAND).name} >> {Commands(COMMAND_STATE)}')
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
 
    #print(f'{Locks(LOCK).name}+{Keys(KEY).name}+{PLCs(PLC).name}+{Commands(PREVCOMMAND).name} >> {Commands(COMMAND_STATE)}')
    return COMMAND_STATE.value
    
def system_model(CLOCK: Logic = Logic('-'), CLOCK_STATE: Logic = Logic('-'), COMMAND_STATE: int = Commands.COMMAND_IDLE, SENSOR_STATE: int = Sensors.SENSOR_ERROR, timeout: int = 0, oldMotor: int = Motors.STOP, oldState: int = Systems.SYSTEM_ERROR):

    sensor      = SENSOR_STATE.value
    command     = COMMAND_STATE.value
    
    stateERROR  = True if ((sensor == Sensors.SENSOR_ERROR.value) or (command == Commands.COMMAND_ERROR.value) or (CLOCK_STATE == False)) else False
    toBLANK     = True if ((stateERROR == False) and (command == Commands.COMMAND_REMOVE.value) and (sensor == Sensors.DANGER.value or sensor == Sensors.TRANSITION.value)) else False
    toDANGER    = True if ((stateERROR == False) and (command == Commands.COMMAND_APPLY.value) and (sensor == Sensors.BLANK.value or sensor == Sensors.TRANSITION.value)) else False
        
    #print(f'{Sensors(sensor).name}|{Commands(command).name}|{timeout}||{1*stateERROR} {1*toBLANK} {1*toDANGER}')    
    
    STATE       = Systems.SYSTEM_IDLE
    MOTOR       = Motors(oldMotor)
    
    match sensor:
        case Sensors.SENSOR_ERROR.value:
            STATE = Systems.SYSTEM_ERROR
            MOTOR = Motors.STOP
        case Sensors.BLANK.value:
            STATE = Systems.SYSTEM_BLANK
            if toDANGER:
                MOTOR = Motors.toDANGER
            else:
                MOTOR = Motors.STOP
        case Sensors.DANGER.value:
            STATE = Systems.SYSTEM_DANGER
            if toBLANK:
                MOTOR = Motors.toBLANK
            else:
                MOTOR = Motors.STOP
        case Sensors.TRANSITION.value:
            STATE = Systems.SYSTEM_TRANSITION
        case _:
            STATE = Systems.SYSTEM_ERROR
            MOTOR = Motors.STOP

    
    SYSTEM_STATE = STATE if (timeout < 160 and oldState != Systems.SYSTEM_ERROR.value) else Systems.SYSTEM_ERROR
    MOTOR_STATE  = MOTOR if (timeout < 160 and oldState != Systems.SYSTEM_ERROR.value) else Motors.STOP
    
    #print(MOTOR,MOTOR_STATE,timeout)
    
    return [SYSTEM_STATE,MOTOR_STATE,stateERROR,toBLANK,toDANGER]

def output_model(SYSTEM_STATE: int = Systems.SYSTEM_IDLE, POWER_STATE: int = Powers.POWER_OFF, SLOWEST_CLOCK: Logic = Logic('-'), PREV_OUTPUT = [False,False],PREV_PWR_LED: int = Leds.RED, PREV_OK_LED: int = Leds.RED):
    
    PWR_LED_SIGNAL = Leds.RED.value
    OK_LED_SIGNAL  = Leds.RED.value
        
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
            OUTPUT = [True,True]
        case _:
            OUTPUT = [False,False]

    match POWER_STATE:
        case Powers.POWER_OFF.value:
            PWR_LED_SIGNAL = Leds.OFF.value
        case Powers.POWER_ON.value:
            PWR_LED_SIGNAL = Leds.GREEN.value
        case Powers.BATTERY.value:
            PWR_LED_SIGNAL = Leds.AMBER.value if SLOWEST_CLOCK else Leds.OFF.value
        case Powers.BATTERY_LOW.value:
            PWR_LED_SIGNAL = Leds.AMBER.value
        case _:
            PWR_LED_SIGNAL = Leds.RED.value

    #print(f'>>{Powers(POWER_STATE).name} {PWR_LED_SIGNAL} {PREV_PWR_LED}')
    
    if SYSTEM_STATE == Systems.SYSTEM_ERROR.value:
        OK_LED_SIGNAL  = Leds.RED.value
    else:
        if POWER_STATE == Powers.POWER_ON.value or POWER_STATE == Powers.BATTERY.value:
            OK_LED_SIGNAL  = Leds.GREEN.value
        elif POWER_STATE == Powers.BATTERY_LOW.value:
            OK_LED_SIGNAL  = Leds.AMBER.value if SLOWEST_CLOCK else Leds.OFF.value
        else:
            OK_LED_SIGNAL  = Leds.RED.value

    PWR_LED = Leds(PWR_LED_SIGNAL).value      #PREV_PWR_LED
    OK_LED = Leds(OK_LED_SIGNAL).value
        
    #PWR_LED = PREV_PWR_LED
    #OK_LED = PREV_OK_LED
    
    #print(f'<<{SLOWEST_CLOCK} {Powers(POWER_STATE).name} {PWR_LED_SIGNAL} {PWR_LED}')
    
    return [OUTPUT,PWR_LED,OK_LED]

counter = 0
SLOW_CLOCK = False
SLOWEST_CLOCK = False

def clock_model(CLOCK: Logic = Logic('-'), CLOCK_STATE: Logic = Logic('-')):
    
    global counter
    global SLOW_CLOCK
    global SLOWEST_CLOCK
    PWM = 1
    
    if CLOCK_STATE == False:
        counter = 0
        SLOW_CLOCK = False
        SLOWEST_CLOCK = False
    else:
        if CLOCK:
            if ( ( counter % 2**8 -1 ) == 0 ):
                SLOW_CLOCK = (not SLOW_CLOCK)
            if ( ( counter % 2**9 -1 ) == 0 ):
                SLOWEST_CLOCK = (not SLOWEST_CLOCK)
            counter = counter + 1

    return [1*SLOW_CLOCK,1*SLOWEST_CLOCK,PWM]
    
def movement_model(PWM: Logic = Logic('-'), MOTOR_STATE: int = Motors.STOP):
    
    #print(f'Receive: {PWM} {MOTOR_STATE}')
    
    match MOTOR_STATE:
        case Motors.STOP:
            MOTOR_PWM = False
            MOTOR_UP = False
            MOTOR_DOWN = False
        case Motors.toDANGER:
            MOTOR_PWM = PWM
            MOTOR_UP = True
            MOTOR_DOWN = False
        case Motors.toBLANK:
            MOTOR_PWM = PWM
            MOTOR_UP = False
            MOTOR_DOWN = True
        case _:
            MOTOR_PWM = False
            MOTOR_UP = False
            MOTOR_DOWN = False
    
    return [MOTOR_PWM,MOTOR_UP,MOTOR_DOWN]
    
timer = 0

def general_model(POWER_MODE: Logic = Logic('-'), BATTERY_STATE: Logic = Logic('-'),KEY: Logic = Logic('-'), KEY_A_I: Logic = Logic('-'), KEY_B_I: Logic = Logic('-'),LOCK: Logic = Logic('-'), LOCK_A_I: Logic = Logic('-'), LOCK_B_I: Logic = Logic('-'),PLC_I_A: Logic = Logic('-'), PLC_I_B: Logic = Logic('-'),PREVCOMMAND: int = Commands.COMMAND_IDLE,SENSOR_1: Logic = Logic('-'), SENSOR_2: Logic = Logic('-'), SENSOR_3: Logic = Logic('-'), SENSOR_4: Logic = Logic('-'),CLOCK: Logic = Logic('-'), CLOCK_STATE: Logic = Logic('-'),oldMotor: int = Motors.STOP, PREV_OUTPUT = [False,False], PREV_PWR_LED = [False,False], PREV_OK_LED = [False,False], CLOCK_B: Logic = Logic('-'), oldState: int = Systems.SYSTEM_ERROR):

    global timer
    
    POWER_STATE                     = power_model(POWER_MODE,BATTERY_STATE)
    LOCK_A_O,LOCK_B_O,LOCK_STATE    = lock_model(LOCK, LOCK_A_I, LOCK_B_I)
    KEY_A_O,KEY_B_O,KEY_STATE       = key_model(KEY, KEY_A_I, KEY_B_I)
    PLC_STATE                       = plc_model(PLC_I_A,PLC_I_B)
    COMMAND_STATE                   = command_model(Keys(KEY_STATE), PLCs(PLC_STATE), Locks(LOCK_STATE), PREVCOMMAND)
    SENSOR_STATE                    = sensor_model(SENSOR_1, SENSOR_2, SENSOR_3, SENSOR_4)
    SLOW_CLOCK,SLOWEST_CLOCK,PWM    = clock_model(CLOCK,CLOCK_STATE)
    
    if ( SENSOR_STATE == Sensors.TRANSITION.value ):
        timer = timer + 1
    else:
        timer = 0
            
    SYSTEM_STATE,MOTOR_STATE,stateERROR,toBLANK,toDANGER = system_model(CLOCK_B, CLOCK_STATE, Commands(COMMAND_STATE), Sensors(SENSOR_STATE), int(round(timer//(2**9),0)), oldMotor,oldState)
    OUTPUT,PWR_LED,OK_LED           = output_model(SYSTEM_STATE.value,POWER_STATE,CLOCK_B,PREV_OUTPUT,PREV_PWR_LED,PREV_OK_LED)
    MOTOR_PWM,MOTOR_UP,MOTOR_DOWN   = movement_model(PWM, MOTOR_STATE)
    
    #print(Systems(SYSTEM_STATE).name)
    #TBD_O                           = dummy_model(TBD_I)
       
    #print (f'{Powers(POWER_STATE).name}|{Locks(LOCK_STATE).name}|{Keys(KEY_STATE).name}|{PLCs(PLC_STATE).name}|{Commands(COMMAND_STATE).name}|{Sensors(SENSOR_STATE).name}>{Systems(SYSTEM_STATE).name}|{Motors(MOTOR_STATE).name}>>{Outputs(2*OUTPUT[0]+OUTPUT[1]).name}|{Leds(2*PWR_LED[0]+PWR_LED[1]).name}|{Leds(2*OK_LED[0]+OK_LED[1]).name}|{Motors(2*MOTOR_DOWN+MOTOR_UP).name}')
    
    
    return [2*OUTPUT[0]+OUTPUT[1],PWR_LED,OK_LED,2*MOTOR_DOWN+1*MOTOR_UP,MOTOR_STATE,timer]
