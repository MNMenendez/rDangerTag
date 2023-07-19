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
		   CLOCK_STATE		: in std_logic;
           COMMAND_STATE 	: in  command_states;
           SENSOR_STATE 	: in  sensor_states;
           SYSTEM_STATE 	: out system_states;
		   MOTOR_STATE		: out motor_states);
end system_module;

architecture system_func of system_module is

signal STATE : system_states := SYSTEM_IDLE;
signal MOTOR : motor_states := STOP;

signal timer : integer := 0;
signal TIMEOUT : STD_LOGIC := '0';
signal toBLANK : STD_LOGIC := '0';
signal toDANGER : STD_LOGIC := '0';
signal stateERROR : STD_LOGIC := '0';

begin

	stateERROR 		<= '1' when ((SENSOR_STATE = SENSOR_ERROR) or (COMMAND_STATE = COMMAND_ERROR) or (CLOCK_STATE = '0')) else '0';
	toBLANK 		<= '1' when ((stateERROR = '0') and (COMMAND_STATE = COMMAND_REMOVE) and (SENSOR_STATE = DANGER or SENSOR_STATE = TRANSITION)) else '0';
	toDANGER 		<= '1' when ((stateERROR = '0') and (COMMAND_STATE = COMMAND_APPLY) and (SENSOR_STATE = BLANK or SENSOR_STATE = TRANSITION)) else '0';
	SYSTEM_STATE 	<= STATE when (TIMEOUT = '0') else SYSTEM_ERROR;
	MOTOR_STATE		<= MOTOR when (TIMEOUT = '0') else STOP;
	
	TIMEOUT_PROCESS: process ( CLOCK , SENSOR_STATE ) is
	begin
		if ( rising_edge ( CLOCK ) ) then
			if ( SENSOR_STATE = TRANSITION ) then
				if ( timer < 160 ) then
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
	
	STATE_PROCESS: process ( CLOCK , toDANGER, toBLANK , SENSOR_STATE ) is
	begin
		case SENSOR_STATE is
			when SENSOR_ERROR =>
				STATE <= SYSTEM_ERROR;
				MOTOR <= STOP;
			when BLANK =>
				STATE <= SYSTEM_BLANK;
				if ( toDANGER = '1' ) then -- stateOK and COMMAND_APPLY and (SENSOR_BLANK or SENSOR_TRANSITION);
					MOTOR <= MoveToDanger;
				else
					MOTOR <= STOP;
				end if;
			when DANGER =>
				STATE <= SYSTEM_DANGER;
				if ( toBLANK = '1' ) then -- stateOK and COMMAND_REMOVE and (SENSOR_DANGER or SENSOR_TRANSITION);
					MOTOR <= MoveToBLANK;
				else
					MOTOR <= STOP;
				end if;
			when TRANSITION =>
				STATE <= SYSTEM_TRANSITION;
			when others =>
				STATE <= SYSTEM_ERROR;
				MOTOR <= STOP;
		end case;
	end process;

end system_func;
