----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    15:11:48 05/01/2023 
-- Design Name: 
-- Module Name:    SYSTEM_MODULE - SYSTEM_FUNC 
-- Project Name: 
-- Target Devices: 
-- Tool versions: 
-- Description: 
--
-- Dependencies: 
--
-- Revision: 
-- Revision 0.01 - File Created
-- Additional Comments: 
--
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
library work;
use work.Utilities.all;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity system_module is
    Port ( POWER_STATE 		: in  power_states;
           MODE_STATE 		: in  mode_states;
           COMMAND_STATE 	: in  command_states;
           SENSOR_STATE 	: in  sensor_states;
		   ALL_OK			: out right_states;
           SYSTEM_STATE 	: out system_states);
end system_module;

architecture system_func of system_module is

begin
	SYSTEM_PROCESS: process (POWER_STATE , MODE_STATE , COMMAND_STATE , SENSOR_STATE ) is
	begin
		SYSTEM_STATE <= SYSTEM_ERROR;
		ALL_OK 		 <= FAULT;
		
		if (POWER_STATE = POWER_OFF) then
			SYSTEM_STATE <= SYSTEM_BATTERY;
		else
			if ( MODE_STATE = MODE_ERROR or COMMAND_STATE = COMMAND_ERROR or SENSOR_STATE = SENSOR_ERROR ) then
				SYSTEM_STATE <= SYSTEM_ERROR;
				ALL_OK 		 <= FAULT;
			else
				ALL_OK			<= ALIVE;
				if ( SENSOR_STATE = DANGER ) then
					SYSTEM_STATE <= SYSTEM_DANGER;
				end if;
				if ( SENSOR_STATE = BLANK ) then
					SYSTEM_STATE <= SYSTEM_BLANK;
				end if;
				if ( SENSOR_STATE = TRANSITION ) then
					SYSTEM_STATE <= SYSTEM_TRANSITION;
				end if;
			end if;
		end if;
	end process;
end system_func;
