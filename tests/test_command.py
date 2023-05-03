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

if cocotb.simulator.is_running():
    from models import enum,Modes,Commands,command_model

@cocotb.test()
async def command_ignore_if_error_mode_test(dut):
    """Whatever INPUT A or B, ignore commands if error mode: Ignore expected"""
    
    INPUT_A = Logic('-')
    INPUT_B = Logic('-')
    dut.INPUT_A.value = INPUT_A
    dut.INPUT_B.value = INPUT_B
    
    dut.KEY.value = True
    dut.KEY_A_I.value = True
    dut.KEY_B_I.value = True
    
    await Timer(2, units="ns") 
    MODE_SIGNAL = dut.MODE_SIGNAL.value
    print(f'{dut.INPUT_A.value}|{dut.INPUT_B.value}|{dut.MODE_SIGNAL.value}|{MODE_SIGNAL} > {dut.COMMAND_SIGNAL.value} | {command_model(INPUT_A,INPUT_B,MODE_SIGNAL)}')
    assert dut.COMMAND_SIGNAL.value == command_model(INPUT_A,INPUT_B,MODE_SIGNAL), f'result is incorrect: {dut.COMMAND_SIGNAL.value} != {Commands.COMMAND_IGNORE}'

@cocotb.test()
async def command_ignore_if_local_apply_mode_test(dut):
    """Whatever INPUT A or B, ignore commands if local apply mode: Ignore expected"""
    
    INPUT_A = Logic('-')
    INPUT_B = Logic('-')
    dut.INPUT_A.value = INPUT_A
    dut.INPUT_B.value = INPUT_B
    
    dut.KEY.value = True
    dut.KEY_A_I.value = False
    dut.KEY_B_I.value = True
    
    await Timer(2, units="ns") 
    MODE_SIGNAL = dut.MODE_SIGNAL.value
    print(f'{dut.INPUT_A.value}|{dut.INPUT_B.value}|{dut.MODE_SIGNAL.value}|{MODE_SIGNAL} > {dut.COMMAND_SIGNAL.value} | {command_model(INPUT_A,INPUT_B,MODE_SIGNAL)}')
    assert dut.COMMAND_SIGNAL.value == command_model(INPUT_A,INPUT_B,MODE_SIGNAL), f'result is incorrect: {dut.COMMAND_SIGNAL.value} != {Commands.COMMAND_IGNORE}'
  
@cocotb.test()
async def command_ignore_if_local_remove_mode_test(dut):
    """Whatever INPUT A or B, ignore commands if local remove mode: Ignore expected"""
    
    INPUT_A = Logic('-')
    INPUT_B = Logic('-')
    dut.INPUT_A.value = INPUT_A
    dut.INPUT_B.value = INPUT_B
        
    dut.KEY.value = True
    dut.KEY_A_I.value = True
    dut.KEY_B_I.value = False
    
    await Timer(2, units="ns") 
    MODE_SIGNAL = dut.MODE_SIGNAL.value  
    print(f'{dut.INPUT_A.value}|{dut.INPUT_B.value}|{dut.MODE_SIGNAL.value}|{MODE_SIGNAL} > {dut.COMMAND_SIGNAL.value} | {command_model(INPUT_A,INPUT_B,MODE_SIGNAL)}')
    assert dut.COMMAND_SIGNAL.value == command_model(INPUT_A,INPUT_B,MODE_SIGNAL), f'result is incorrect: {dut.COMMAND_SIGNAL.value} != {Commands.COMMAND_IGNORE}'

@cocotb.test()
async def command_error_if_equal_commands_in_remote_mode_test(dut):
    """If INPUT A = Input B in remote mode: Error expected"""
    
    INPUT_A = True
    INPUT_B = True
    dut.INPUT_A.value = INPUT_A
    dut.INPUT_B.value = INPUT_B
        
    dut.KEY.value = False
    dut.KEY_A_I.value = Logic('-')
    dut.KEY_B_I.value = Logic('-')
    
    await Timer(2, units="ns") 
    MODE_SIGNAL = dut.MODE_SIGNAL.value  
    print(f'{dut.INPUT_A.value}|{dut.INPUT_B.value}|{dut.MODE_SIGNAL.value}|{MODE_SIGNAL} > {dut.COMMAND_SIGNAL.value} | {command_model(INPUT_A,INPUT_B,MODE_SIGNAL)}')
    assert dut.COMMAND_SIGNAL.value == command_model(INPUT_A,INPUT_B,MODE_SIGNAL), f'result is incorrect: {dut.COMMAND_SIGNAL.value} != {Commands.COMMAND_ERROR}'

    dut.KEY.value = True
    dut.KEY_A_I.value = False
    dut.KEY_B_I.value = False
    
    await Timer(2, units="ns") 
    MODE_SIGNAL = dut.MODE_SIGNAL.value  
    print(f'{dut.INPUT_A.value}|{dut.INPUT_B.value}|{dut.MODE_SIGNAL.value}|{MODE_SIGNAL} > {dut.COMMAND_SIGNAL.value} | {command_model(INPUT_A,INPUT_B,MODE_SIGNAL)}')
    assert dut.COMMAND_SIGNAL.value == command_model(INPUT_A,INPUT_B,MODE_SIGNAL), f'result is incorrect: {dut.COMMAND_SIGNAL.value} != {Commands.COMMAND_ERROR}'

    INPUT_A = False
    INPUT_B = False
    dut.INPUT_A.value = INPUT_A
    dut.INPUT_B.value = INPUT_B
        
    dut.KEY.value = False
    dut.KEY_A_I.value = Logic('-')
    dut.KEY_B_I.value = Logic('-')
    
    await Timer(2, units="ns") 
    MODE_SIGNAL = dut.MODE_SIGNAL.value  
    print(f'{dut.INPUT_A.value}|{dut.INPUT_B.value}|{dut.MODE_SIGNAL.value}|{MODE_SIGNAL} > {dut.COMMAND_SIGNAL.value} | {command_model(INPUT_A,INPUT_B,MODE_SIGNAL)}')
    assert dut.COMMAND_SIGNAL.value == command_model(INPUT_A,INPUT_B,MODE_SIGNAL), f'result is incorrect: {dut.COMMAND_SIGNAL.value} != {Commands.COMMAND_ERROR}'

    dut.KEY.value = True
    dut.KEY_A_I.value = False
    dut.KEY_B_I.value = False
    
    await Timer(2, units="ns") 
    MODE_SIGNAL = dut.MODE_SIGNAL.value  
    print(f'{dut.INPUT_A.value}|{dut.INPUT_B.value}|{dut.MODE_SIGNAL.value}|{MODE_SIGNAL} > {dut.COMMAND_SIGNAL.value} | {command_model(INPUT_A,INPUT_B,MODE_SIGNAL)}')
    assert dut.COMMAND_SIGNAL.value == command_model(INPUT_A,INPUT_B,MODE_SIGNAL), f'result is incorrect: {dut.COMMAND_SIGNAL.value} != {Commands.COMMAND_ERROR}'

@cocotb.test()
async def command_apply_in_remote_mode_test(dut):
    """INPUT A = False and INPUT B = True in remote mode: Apply expected"""
    
    INPUT_A = False
    INPUT_B = True
    dut.INPUT_A.value = INPUT_A
    dut.INPUT_B.value = INPUT_B
        
    dut.KEY.value = False
    dut.KEY_A_I.value = Logic('-')
    dut.KEY_B_I.value = Logic('-')
    
    await Timer(2, units="ns") 
    MODE_SIGNAL = dut.MODE_SIGNAL.value  
    print(f'{dut.INPUT_A.value}|{dut.INPUT_B.value}|{dut.MODE_SIGNAL.value}|{MODE_SIGNAL} > {dut.COMMAND_SIGNAL.value} | {command_model(INPUT_A,INPUT_B,MODE_SIGNAL)}')
    assert dut.COMMAND_SIGNAL.value == command_model(INPUT_A,INPUT_B,MODE_SIGNAL), f'result is incorrect: {dut.COMMAND_SIGNAL.value} != {Commands.COMMAND_APPLY}'

    dut.KEY.value = True
    dut.KEY_A_I.value = False
    dut.KEY_B_I.value = False
    
    await Timer(2, units="ns") 
    MODE_SIGNAL = dut.MODE_SIGNAL.value  
    print(f'{dut.INPUT_A.value}|{dut.INPUT_B.value}|{dut.MODE_SIGNAL.value}|{MODE_SIGNAL} > {dut.COMMAND_SIGNAL.value} | {command_model(INPUT_A,INPUT_B,MODE_SIGNAL)}')
    assert dut.COMMAND_SIGNAL.value == command_model(INPUT_A,INPUT_B,MODE_SIGNAL), f'result is incorrect: {dut.COMMAND_SIGNAL.value} != {Commands.COMMAND_APPLY}'

@cocotb.test()
async def command_remove_in_remote_mode_test(dut):
    """INPUT A = True and INPUT B = False in remote mode: Remove expected"""
    
    INPUT_A = True
    INPUT_B = False
    dut.INPUT_A.value = INPUT_A
    dut.INPUT_B.value = INPUT_B
        
    dut.KEY.value = False
    dut.KEY_A_I.value = Logic('-')
    dut.KEY_B_I.value = Logic('-')
    
    await Timer(2, units="ns") 
    MODE_SIGNAL = dut.MODE_SIGNAL.value  
    print(f'{dut.INPUT_A.value}|{dut.INPUT_B.value}|{dut.MODE_SIGNAL.value}|{MODE_SIGNAL} > {dut.COMMAND_SIGNAL.value} | {command_model(INPUT_A,INPUT_B,MODE_SIGNAL)}')
    assert dut.COMMAND_SIGNAL.value == command_model(INPUT_A,INPUT_B,MODE_SIGNAL), f'result is incorrect: {dut.COMMAND_SIGNAL.value} != {Commands.COMMAND_REMOVE}'

    dut.KEY.value = True
    dut.KEY_A_I.value = False
    dut.KEY_B_I.value = False
    
    await Timer(2, units="ns") 
    MODE_SIGNAL = dut.MODE_SIGNAL.value  
    print(f'{dut.INPUT_A.value}|{dut.INPUT_B.value}|{dut.MODE_SIGNAL.value}|{MODE_SIGNAL} > {dut.COMMAND_SIGNAL.value} | {command_model(INPUT_A,INPUT_B,MODE_SIGNAL)}')
    assert dut.COMMAND_SIGNAL.value == command_model(INPUT_A,INPUT_B,MODE_SIGNAL), f'result is incorrect: {dut.COMMAND_SIGNAL.value} != {Commands.COMMAND_REMOVE}'












def test_command_runner():
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
        verilog_sources = [proj_path / "hdl" / "command_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "command_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="command_module",
        always=True,
    )
    runner.test(hdl_toplevel="command_module", test_module="test_command")


if __name__ == "__main__":
    test_command_runner()
