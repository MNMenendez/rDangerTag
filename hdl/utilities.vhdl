-- This file is public domain, it can be freely copied without restrictions.
-- SPDX-License-Identifier: CC0-1.0
-- Adder DUT
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

package utilities is
	Type power_states is (POWER_OFF,POWER_ON);
	Type key_states is (NOT_USED,USED);
	Type mode_states is (MODE_ERROR,REMOTE,LOCAL_APPLY,LOCAL_REMOVE);
	Type sensor_states is (SENSOR_ERROR,DANGER,BLANK,TRANSITION);
	Type command_states is (COMMAND_ERROR,COMMAND_IGNORE,COMMAND_APPLY,COMMAND_REMOVE);
	Type system_states is (SYSTEM_ERROR,SYSTEM_DANGER,SYSTEM_BLANK,SYSTEM_BATTERY);
	Type right_states is (FAULT,ALIVE);
end package;
