----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    14:54:05 05/01/2023 
-- Design Name: 
-- Module Name:    COMMAND_PROCESS - Behavioral 
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

entity command_module is
    Port ( KEY_STATE : in  key_states;
           PLC_STATE : in  plc_states;
			  LOCK_STATE : in lock_states;
           COMMAND_STATE : out  command_states := COMMAND_IDLE);
end command_module;

architecture command_func of command_module is
signal COMMAND_SIGNAL : command_states := COMMAND_IDLE;
signal COMMAND : std_logic_vector(2 downto 0);
signal APPLY_VALID 	: STD_LOGIC := '0';
signal REMOVE_VALID 	: STD_LOGIC := '0';
signal CMD_INVALID 	: STD_LOGIC := '1';
begin

	APPLY_VALID 	<= '1' when (LOCK_STATE = LOCK_APPLY) and ( KEY_STATE = KEY_APPLY or ( KEY_STATE = NO_KEY and PLC_STATE = PLC_APPLY )) else '0';
	REMOVE_VALID	<= '1' when (LOCK_STATE = LOCK_REMOVE) and ( KEY_STATE = KEY_REMOVE or ( KEY_STATE = NO_KEY and PLC_STATE = PLC_REMOVE )) else '0';
	CMD_INVALID 	<= '1' when (LOCK_STATE = LOCK_ERROR) or (KEY_STATE = KEY_ERROR or (KEY_STATE = NO_KEY and PLC_STATE = PLC_ERROR)) else '0';
	COMMAND	  		<= APPLY_VALID & REMOVE_VALID & CMD_INVALID;
	
	COMMAND_PROCESS : process ( COMMAND , COMMAND_SIGNAL ) is
	begin
	case COMMAND_SIGNAL is
		when COMMAND_IDLE =>
			case COMMAND is
				when "000" =>
					COMMAND_SIGNAL <= COMMAND_IDLE;
				when "100" =>
					COMMAND_SIGNAL <= COMMAND_APPLY;
				when "010" =>
					COMMAND_SIGNAL <= COMMAND_REMOVE;
				when others =>
					COMMAND_SIGNAL <= COMMAND_ERROR;
			end case;
		when COMMAND_APPLY =>
			case COMMAND is
				when "000" =>
					COMMAND_SIGNAL <= COMMAND_IDLE;
				when "100" =>
					COMMAND_SIGNAL <= COMMAND_APPLY;
				when "010" =>
					COMMAND_SIGNAL <= COMMAND_REMOVE;
				when others =>
					COMMAND_SIGNAL <= COMMAND_ERROR;
			end case;
		when COMMAND_REMOVE =>
			case COMMAND is
				when "000" =>
					COMMAND_SIGNAL <= COMMAND_IDLE;
				when "100" =>
					COMMAND_SIGNAL <= COMMAND_APPLY;
				when "010" =>
					COMMAND_SIGNAL <= COMMAND_REMOVE;
				when others =>
					COMMAND_SIGNAL <= COMMAND_ERROR;
			end case;
		when COMMAND_ERROR =>
			NULL;
		when others =>
			COMMAND_SIGNAL <= COMMAND_ERROR;
		end case;
	end process;
	COMMAND_STATE <= COMMAND_SIGNAL;
end command_func;

