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
from cocotb.binary import BinaryValue

if cocotb.simulator.is_running():
    from models import *

@cocotb.test()
async def sensor_test(dut):
    """Sensor test"""
    
    for i in range (5000):
        print(f'Sensor test progress: {i/5000:2.1%}\r', end="\r")
        j = random.randint(0 , 15)
        k = BinaryValue(value=j,bits=4,bigEndian=False)
        dut.SENSORS_I.value = k
        await Timer(1, units="sec")
        output = sensor_model((k//8)%2,(k//4)%2,(k//2)%2,k%2)
        
        #print(f'{k}-{(k//8)%2}{(k//4)%2}{(k//2)%2}{k%2} > {Sensors(output).name}')
        #print(f'{k} > Py:{Sensors(output).name} vs VHDL:{Sensors(dut.SENSOR_STATE.value).name}')

        assert ( dut.SENSOR_STATE.value == output ), f'result is incorrect: {dut.SENSOR_STATE.value} != {output}' 
    '''
    SENSOR_1 = tuple_create(4,8)+(False,)
    SENSOR_2 = tuple_create(4,4)+(False,)
    SENSOR_3 = tuple_create(4,2)+(False,)
    SENSOR_4 = tuple_create(4,1)+(False,)
    
    for i in range(len(SENSOR_1)):
        dut.SENSORS_I.value = 8*SENSOR_1[i]+4*SENSOR_2[i]+2*SENSOR_3[i]+SENSOR_4[i]
        
        await Timer(1, units="sec")
        print(f'{dut.SENSORS_I.value} > {Sensors(sensor_model(SENSOR_1[i],SENSOR_2[i],SENSOR_3[i],SENSOR_4[i])).name}')
        output = sensor_model(SENSOR_1[i],SENSOR_2[i],SENSOR_3[i],SENSOR_4[i])
        assert ( dut.SENSOR_STATE.value == output ), f'result is incorrect: {dut.SENSOR_STATE.value} != {output}'   
    '''
    print('')

def test_sensor_runner():
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
        verilog_sources = [proj_path / "hdl" / "sensor_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "sensor_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="sensor_module",
        always=True,
    )
    runner.test(hdl_toplevel="sensor_module", test_module="test_sensor")


if __name__ == "__main__":
    test_sensor_runner()
