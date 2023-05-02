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

if cocotb.simulator.is_running():
    from models import enum,Modes,key_model

@cocotb.test()
async def key_not_used_test(dut):
    """Test key not used"""
        
    KEY = False
    dut.KEY.value = KEY
    await Timer(2, units="ns")  
    print(dut.KEY_A_I.value, dut.KEY_B_I.value,dut.MODE_SIGNAL.value, key_model(KEY))
    assert dut.MODE_SIGNAL.value == Modes.REMOTE, f'result is incorrect: {dut.MODE_SIGNAL.value} != {Modes.REMOTE}'

@cocotb.test()
async def key_used_remote_test(dut):
    """Test key used in remote mode"""
        
    KEY = True
    KEY_A_I = False
    KEY_B_I = False
    
    dut.KEY.value = KEY
    dut.KEY_A_I.value = KEY_A_I
    dut.KEY_B_I.value = KEY_B_I
    
    await Timer(2, units="ns")     
    assert (dut.MODE_SIGNAL.value == Modes.REMOTE and dut.KEY_A_O.value == dut.KEY_A_I.value and dut.KEY_B_O.value == dut.KEY_B_I.value), f'result is incorrect: {dut.MODE_SIGNAL.value} != {Modes.REMOTE}'
    
@cocotb.test()
async def key_used_local_apply_test(dut):
    """Test key used in local apply mode"""
        
    KEY = True
    KEY_A_I = False
    KEY_B_I = True
    
    dut.KEY.value = KEY
    dut.KEY_A_I.value = KEY_A_I
    dut.KEY_B_I.value = KEY_B_I
    
    await Timer(2, units="ns")     
    assert (dut.MODE_SIGNAL.value == Modes.LOCAL_APPLY and dut.KEY_A_O.value == dut.KEY_A_I.value and dut.KEY_B_O.value == dut.KEY_B_I.value), f'result is incorrect: {dut.MODE_SIGNAL.value} != {Modes.LOCAL_APPLY}'

@cocotb.test()
async def key_used_local_remove_test(dut):
    """Test key used in local remove mode"""
        
    KEY = True
    KEY_A_I = True
    KEY_B_I = False
    
    dut.KEY.value = KEY
    dut.KEY_A_I.value = KEY_A_I
    dut.KEY_B_I.value = KEY_B_I
    
    await Timer(2, units="ns")     
    assert (dut.MODE_SIGNAL.value == Modes.LOCAL_REMOVE and dut.KEY_A_O.value == dut.KEY_A_I.value and dut.KEY_B_O.value == dut.KEY_B_I.value), f'result is incorrect: {dut.MODE_SIGNAL.value} != {Modes.LOCAL_REMOVE}'
    
@cocotb.test()
async def key_used_error_test(dut):
    """Test key used in local remove mode"""
        
    KEY = True
    KEY_A_I = True
    KEY_B_I = True
    
    dut.KEY.value = KEY
    dut.KEY_A_I.value = KEY_A_I
    dut.KEY_B_I.value = KEY_B_I
    
    await Timer(2, units="ns")     
    assert (dut.MODE_SIGNAL.value == Modes.ERROR_MODE and dut.KEY_A_O.value == dut.KEY_A_I.value and dut.KEY_B_O.value == dut.KEY_B_I.value), f'result is incorrect: {dut.MODE_SIGNAL.value} != {Modes.ERROR_MODE}'
    

def test_key_runner():
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
        verilog_sources = [proj_path / "hdl" / "key_module.sv"]
    else:
        vhdl_sources = [proj_path / "hdl" / "key_module.vhdl"]

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="key_module",
        always=True,
    )
    runner.test(hdl_toplevel="key_module", test_module="test_key")


if __name__ == "__main__":
    test_key_runner()
