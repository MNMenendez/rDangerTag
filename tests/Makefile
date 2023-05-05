###############################################################################
# Copyright (c) 2013 Potential Ventures Ltd
# Copyright (c) 2013 SolarFlare Communications Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Potential Ventures Ltd,
#       SolarFlare Communications Inc nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL POTENTIAL VENTURES LTD BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################

TOPLEVEL_LANG ?= vhdl
SIM ?= ghdl
SIM_ARGS ?= --wave=waveform.ghw

PWD=$(shell pwd)

export PYTHONPATH := $(PWD)/../model:$(PYTHONPATH)

VHDL_SOURCES += $(PWD)/../hdl/utilities.vhdl
VHDL_SOURCES += $(PWD)/../hdl/general.vhdl
VHDL_SOURCES += $(PWD)/../hdl/dummy_module.vhdl
VHDL_SOURCES += $(PWD)/../hdl/power_module.vhdl
VHDL_SOURCES += $(PWD)/../hdl/key_module.vhdl
VHDL_SOURCES += $(PWD)/../hdl/sensor_module.vhdl
VHDL_SOURCES += $(PWD)/../hdl/command_module.vhdl
VHDL_SOURCES += $(PWD)/../hdl/lock_module.vhdl
VHDL_SOURCES += $(PWD)/../hdl/system_module.vhdl
VHDL_SOURCES += $(PWD)/../hdl/output_module.vhdl
VHDL_SOURCES += $(PWD)/../hdl/motor_module.vhdl
VHDL_SOURCES += $(PWD)/../hdl/clock_module.vhdl
VHDL_SOURCES += $(PWD)/../hdl/movement_module.vhdl

TOPLEVEL := general
MODULE ?= test_dummy,test_power,test_key,test_sensor,test_command,test_lock,test_system,test_output,test_motor,test_clock,test_movement

#MODULE ?= test_clock

include $(shell cocotb-config --makefiles)/Makefile.sim
