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
    Port ( CLOCK			: in std_logic;
		   CLOCK_STATE		: in std_logic			:= '1';
           COMMAND_STATE 	: in  command_states	:= COMMAND_IDLE;
           SENSOR_STATE 	: in  sensor_states		:= TRANSITION;
           SYSTEM_STATE 	: out system_states		:= SYSTEM_IDLE;
		   MOTOR_STATE		: out motor_states		:= STOP);
end system_module;

architecture system_func of system_module is

signal STATE : system_states 	:= SYSTEM_IDLE;
signal MOTOR : motor_states 	:= STOP;

signal timer : integer 			:= 0;
signal TIMEOUT : STD_LOGIC 		:= '0';
signal toBLANK : STD_LOGIC		:= '0';
signal toDANGER : STD_LOGIC 	:= '0';
signal stateERROR : STD_LOGIC 	:= '0';

signal HELP	: STD_LOGIC := '0';

begin

	stateERROR 		<= '1' when ((COMMAND_STATE = COMMAND_ERROR) or (CLOCK_STATE = '0') ) else '0';
	--stateERROR 		<= '1' when ((SENSOR_STATE = SENSOR_ERROR) or (COMMAND_STATE = COMMAND_ERROR) or (CLOCK_STATE = '0')) else '0';
	toBLANK 		<= '1' when ((stateERROR = '0') and (COMMAND_STATE = COMMAND_REMOVE) and (SENSOR_STATE = DANGER or SENSOR_STATE = TRANSITION)) else '0';
	toDANGER 		<= '1' when ((stateERROR = '0') and (COMMAND_STATE = COMMAND_APPLY) and (SENSOR_STATE = BLANK or SENSOR_STATE = TRANSITION)) else '0';
	SYSTEM_STATE 	<= STATE when (TIMEOUT = '0') else SYSTEM_ERROR;
	MOTOR_STATE		<= MOTOR when (TIMEOUT = '0') else STOP;
	
	TIMEOUT_PROCESS: process ( CLOCK , SENSOR_STATE ) is
	begin
		if ( rising_edge ( CLOCK ) ) then
			if ( SENSOR_STATE = TRANSITION ) then
				if ( timer < 160-1 ) then
					timer <= timer + 1;	
				else
					TIMEOUT <= '1';
				end if;
			else
				timer <= 0;
				TIMEOUT <= '0';
			end if;
		end if;
	end process;
	
	STATE_PROCESS: process ( STATE , toDANGER, toBLANK , SENSOR_STATE ) is
	begin
		--case STATE is
		--	when SYSTEM_IDLE =>
		--		MOTOR <= STOP;
		--		if ( toDANGER = '1' ) then
		--			STATE <= SYSTEM_TRANSITION;
		--		end if;
		--	when SYSTEM_DANGER =>
		--		MOTOR <= MoveToDanger;
		--	when SYSTEM_BLANK =>
		--		MOTOR <= MoveToBLANK;
		--	when SYSTEM_TRANSITION =>
		--		if (SENSOR_STATE = SENSOR_ERROR) then
		--			HELP <= '1';
		--		end if;
		--		if ( stateERROR = '1') then
		--			STATE <= SYSTEM_DANGER;
		--		end if;
		--	when SYSTEM_ERROR =>
	--			MOTOR <= STOP;
	--		when others =>
	--			MOTOR <= STOP;
	--	end case;
		
		if (SENSOR_STATE = SENSOR_ERROR) then
			HELP <= '1';
		end if;
	
		case SENSOR_STATE is
			when SENSOR_ERROR =>
				STATE <= SYSTEM_ERROR;
				MOTOR <= STOP;
			when BLANK =>
				if ( STATE /= SYSTEM_ERROR ) then
					STATE <= SYSTEM_BLANK;
					if ( toDANGER = '1' ) then -- stateOK and COMMAND_APPLY and (SENSOR_BLANK or SENSOR_TRANSITION);
						MOTOR <= MoveToDanger;
					else
						MOTOR <= STOP;
					end if;
				end if;
			when DANGER =>
				if ( STATE /= SYSTEM_ERROR ) then
					STATE <= SYSTEM_DANGER;
					if ( toBLANK = '1' ) then -- stateOK and COMMAND_REMOVE and (SENSOR_DANGER or SENSOR_TRANSITION);
						MOTOR <= MoveToBLANK;
					else
						MOTOR <= STOP;
					end if;
				end if;
			when TRANSITION =>
				if ( STATE /= SYSTEM_ERROR ) then
					STATE <= SYSTEM_TRANSITION;
				end if;
			when others =>
				STATE <= SYSTEM_BLANK;--SYSTEM_ERROR;
				MOTOR <= STOP;
		end case;
		
		
	end process;

end system_func;
