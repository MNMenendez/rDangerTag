-- This file is public domain, it can be freely copied without restrictions.
-- SPDX-License-Identifier: CC0-1.0
-- Adder DUT
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

package utilities is
	Type power_states is (POWER_OFF,POWER_ON,BATTERY,BATTERY_LOW);
	Type key_states is (KEY_ERROR,KEY_APPLY,KEY_REMOVE,NO_KEY);
	Type lock_states is (LOCK_ERROR,LOCK_APPLY,LOCK_REMOVE,NO_LOCK);
	Type plc_states is (PLC_ERROR,PLC_APPLY,PLC_REMOVE,PLC_IDLE);
	Type command_states is (COMMAND_ERROR,COMMAND_APPLY,COMMAND_REMOVE,COMMAND_IDLE);
	Type sensor_states is (SENSOR_ERROR,DANGER,BLANK,TRANSITION);
	Type system_states is (SYSTEM_ERROR,SYSTEM_DANGER,SYSTEM_BLANK,SYSTEM_TRANSITION,SYSTEM_TIMEOUT,SYSTEM_IDLE);
	Type general_states is (STATE_ERROR,STATE_MOVING,STATE_STOP);
	Type motor_states is (STOP,MoveToDanger,MoveToBlank);
	Type led_states is (RED,AMBER,FLASHING,GREEN);
end package;
