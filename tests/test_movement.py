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

class CustomBaseClock:
    """Base class to derive from."""

    def __init__(self, signal):
        self.signal = signal

    @lazy_property
    def log(self):
        return SimLog("cocotb.{}.{}".format(type(self).__qualname__, self.signal._name))

class CustomClock(CustomBaseClock):

    def __init__(
        self, signal, period: Union[float, Real, Decimal], units: str = "step"
    ):
        CustomBaseClock.__init__(self, signal)
        if units is None:
            warnings.warn(
                'Using units=None is deprecated, use units="step" instead.',
                DeprecationWarning,
                stacklevel=2,
            )
            units = "step"  # don't propagate deprecated value
        self.period = get_sim_steps(period, units)
        self.half_period = get_sim_steps(period / 2, units)
        self.frequency = 1 / get_time_from_sim_steps(self.period, units="us")
        self.hdl = None
        self.signal = signal
        self.coro = None
        self.mcoro = None


    async def start(self, cycles=None, start_high=True, pwm = 50):
        t = int(self.half_period)
        t_high = Timer(round(t*pwm/100,0))
        t_low =  Timer(round(t*(1-pwm/100),0))
        if cycles is None:
            it = itertools.count()
        else:
            it = range(cycles)

        # branch outside for loop for performance (decision has to be taken only once)
        if start_high:
            for _ in it:
                self.signal.value = True
                await t_high
                self.signal.value = False
                await t_low
        else:
            for _ in it:
                self.signal.value = False
                await t_low
                self.signal.value = True
                await t_high

@cocotb.test()
async def movement_test(dut):
    """Testing movement"""

    clock = CustomClock(dut.PWM, 30, units="us")  # Create a 30us period clock on port clk
    cocotb.start_soon(clock.start(start_high = False, pwm = 80))  # Start the clock
    
    motorStates = [Motors.STOP,Motors.toDANGER,Motors.toBLANK]
    dut.MOTOR_STATE.value = BinaryValue(value=Motors.STOP.value,bits=8,bigEndian=False)
    
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
