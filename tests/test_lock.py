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
    from models import enum,Modes,Commands,lock_model

@cocotb.test()
async def output_ignore_if_lock_disable_test(dut):
    """Whatever LOCK A or B, ignore output if lock disable: double false expected"""
    
    LOCK     = False
    LOCK_A_I = Logic('-')
    LOCK_B_I = Logic('-')
    
    dut.LOCK.value = LOCK
    dut.LOCK_A_I.value = LOCK_A_I
    dut.LOCK_B_I.value = LOCK_B_I
    
    await Timer(2, units="ns")
    print(f'{dut.LOCK_A_I.value}|{dut.LOCK_B_I.value}|{dut.LOCK.value} > {dut.LOCK_A_O.value} | {dut.LOCK_B_O.value} | {lock_model(LOCK,LOCK_A_I,LOCK_B_I)}')
    assert ([dut.LOCK_A_O.value,dut.LOCK_B_O.value] == lock_model(LOCK,LOCK_A_I,LOCK_B_I)), f'result is incorrect: {dut.LOCK_A_O.value},{dut.LOCK_B_O.value} ! (False,False)'

@cocotb.test()
async def output_equal_input_if_lock_enable_test(dut):
    """Whatever LOCK A or B, ignore output if lock disable: double false expected"""
    
    LOCK     = True
    LOCK_A_I = False
    LOCK_B_I = False
    
    dut.LOCK.value = LOCK
    dut.LOCK_A_I.value = LOCK_A_I
    dut.LOCK_B_I.value = LOCK_B_I
    
    await Timer(2, units="ns")
    print(f'{dut.LOCK_A_I.value}|{dut.LOCK_B_I.value}|{dut.LOCK.value} > {dut.LOCK_A_O.value} | {dut.LOCK_B_O.value} | {lock_model(LOCK,LOCK_A_I,LOCK_B_I)}')
    assert ([dut.LOCK_A_O.value,dut.LOCK_B_O.value] == lock_model(LOCK,LOCK_A_I,LOCK_B_I)), f'result is incorrect: {dut.LOCK_A_O.value},{dut.LOCK_B_O.value} ! {dut.LOCK_A_I.value},{dut.LOCK_B_I.value}'
    
    LOCK_A_I = False
    LOCK_B_I = True
    
    dut.LOCK_A_I.value = LOCK_A_I
    dut.LOCK_B_I.value = LOCK_B_I
    
    await Timer(2, units="ns")
    print(f'{dut.LOCK_A_I.value}|{dut.LOCK_B_I.value}|{dut.LOCK.value} > {dut.LOCK_A_O.value} | {dut.LOCK_B_O.value} | {lock_model(LOCK,LOCK_A_I,LOCK_B_I)}')
    assert ([dut.LOCK_A_O.value,dut.LOCK_B_O.value] == lock_model(LOCK,LOCK_A_I,LOCK_B_I)), f'result is incorrect: {dut.LOCK_A_O.value},{dut.LOCK_B_O.value} ! {dut.LOCK_A_I.value},{dut.LOCK_B_I.value}'
    
    LOCK_A_I = True
    LOCK_B_I = False
    
    dut.LOCK_A_I.value = LOCK_A_I
    dut.LOCK_B_I.value = LOCK_B_I
    
    await Timer(2, units="ns")
    print(f'{dut.LOCK_A_I.value}|{dut.LOCK_B_I.value}|{dut.LOCK.value} > {dut.LOCK_A_O.value} | {dut.LOCK_B_O.value} | {lock_model(LOCK,LOCK_A_I,LOCK_B_I)}')
    assert ([dut.LOCK_A_O.value,dut.LOCK_B_O.value] == lock_model(LOCK,LOCK_A_I,LOCK_B_I)), f'result is incorrect: {dut.LOCK_A_O.value},{dut.LOCK_B_O.value} ! {dut.LOCK_A_I.value},{dut.LOCK_B_I.value}'

    LOCK_A_I = True
    LOCK_B_I = True
    
    dut.LOCK_A_I.value = LOCK_A_I
    dut.LOCK_B_I.value = LOCK_B_I
    
    await Timer(2, units="ns")
    print(f'{dut.LOCK_A_I.value}|{dut.LOCK_B_I.value}|{dut.LOCK.value} > {dut.LOCK_A_O.value} | {dut.LOCK_B_O.value} | {lock_model(LOCK,LOCK_A_I,LOCK_B_I)}')
    assert ([dut.LOCK_A_O.value,dut.LOCK_B_O.value] == lock_model(LOCK,LOCK_A_I,LOCK_B_I)), f'result is incorrect: {dut.LOCK_A_O.value},{dut.LOCK_B_O.value} ! {dut.LOCK_A_I.value},{dut.LOCK_B_I.value}'

def test_lock_runner():
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
        verilog_sources = [proj_path / "hdl" / "lock_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "lock_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="lock_module",
        always=True,
    )
    runner.test(hdl_toplevel="lock_module", test_module="test_lock")


if __name__ == "__main__":
    test_lock_runner()
