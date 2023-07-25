----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    15:28:38 05/01/2023 
-- Design Name: 
-- Module Name:    MOTOR_MODULE - MOTOR_FUNC 
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

entity motor_module is
    Port ( 
			CLOCK			: in std_logic			:= '0';
			LOCK_STATE 		: in  lock_states		:= NO_LOCK;
           	MODE_STATE 		: in  mode_states		:= STOP;
           	COMMAND_STATE 	: in  command_states	:= COMMAND_IDLE;
           	SENSOR_STATE 	: in  sensor_states		:= TRANSITION;
		    MOTOR_STATE		: out motor_states		:= STOP);
end motor_module;

architecture motor_func of motor_module is
signal STATE : motor_states := STOP;
signal motor_timeout : integer range 0 to 100000000 := 0;
begin
	
	MOTOR_PROCESS: process ( CLOCK )
	begin
	if (rising_edge(CLOCK)) then
		case STATE is
			when STOP =>	
				if ( COMMAND_STATE /= COMMAND_ERROR and COMMAND_STATE = COMMAND_APPLY and SENSOR_STATE /= DANGER ) then
					STATE <= toDANGER;
				end if;
				if ( COMMAND_STATE /= COMMAND_ERROR and COMMAND_STATE = COMMAND_REMOVE and SENSOR_STATE /= BLANK ) then
					STATE <= toBLANK;
				end if;
			when toDANGER =>
				if ( COMMAND_STATE = COMMAND_ERROR or SENSOR_STATE = SENSOR_ERROR or SENSOR_STATE = DANGER ) then
					motor_timeout <= 0;
					STATE <= STOP;
				end if;
			when toBLANK =>
				if ( COMMAND_STATE = COMMAND_ERROR or SENSOR_STATE = SENSOR_ERROR or SENSOR_STATE = BLANK ) then
					motor_timeout <= 0;
					STATE <= STOP;
				end if;
		end case;
		MOTOR_STATE <= STATE;
	end if;
	end process;

--	MOTOR_PROCESS: process ( LOCK_STATE, MODE_STATE, COMMAND_STATE, SENSOR_STATE )
--	begin
--		MOTOR_STATE <= STOP;
--		if ( LOCK = '1' or MODE_STATE = MODE_ERROR or COMMAND_STATE = COMMAND_ERROR ) then
--			MOTOR_STATE <= STOP;
--		else
--			if ( SENSOR_STATE = SENSOR_ERROR ) then
--				MOTOR_STATE <= STOP;
--			else
--				if ( MODE_STATE = LOCAL_APPLY and LOCK_A_I = '1' and LOCK_B_I = '0' ) then
--					if ( SENSOR_STATE /= DANGER ) then
--						MOTOR_STATE <= toDANGER;
--					else
--						MOTOR_STATE <= STOP;
--					end if;
--				end if;
--				if ( MODE_STATE = LOCAL_REMOVE and LOCK_A_I = '0' and LOCK_B_I = '1' ) then
--					if ( SENSOR_STATE /= BLANK ) then
--						MOTOR_STATE <= toBLANK;
--					else
--						MOTOR_STATE <= STOP;
--					end if;
--				end if;
--				if ( MODE_STATE = REMOTE ) then
--					if ( COMMAND_STATE = COMMAND_APPLY and LOCK_A_I = '1' and LOCK_B_I = '0') then
--						if ( SENSOR_STATE /= DANGER ) then
--							MOTOR_STATE <= toDANGER;
--						else
--							MOTOR_STATE <= STOP;
--						end if;
--					end if;				
--					if ( COMMAND_STATE = COMMAND_REMOVE and LOCK_A_I = '0' and LOCK_B_I = '1') then
--						if ( SENSOR_STATE /= BLANK ) then
--							MOTOR_STATE <= toBLANK;
--						else
--							MOTOR_STATE <= STOP;
--						end if;
--					end if;
--				end if;
--		    end if;
--        end if;
--	end process;

end motor_func;
