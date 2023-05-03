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
    Port ( 
           INPUT_A : in  STD_LOGIC := '0';
           INPUT_B : in  STD_LOGIC := '0';
           MODE_STATE : in  mode_states := MODE_ERROR;
           COMMAND_STATE : out  command_states);
end command_module;

architecture command_func of command_module is

begin
	COMMAND_PROCESS : process (INPUT_A , INPUT_B , MODE_STATE ) is
	begin
		COMMAND_STATE <= COMMAND_ERROR;
		if ( MODE_STATE /= REMOTE ) then
			COMMAND_STATE <= COMMAND_IGNORE;
		else
			if ( INPUT_A = '0' and INPUT_B = '0' ) then
				COMMAND_STATE <= COMMAND_ERROR;
			end if;
			if ( INPUT_A = '0' and INPUT_B = '1' ) then
				COMMAND_STATE <= COMMAND_APPLY;
			end if;
			if ( INPUT_A = '1' and INPUT_B = '0' ) then
				COMMAND_STATE <= COMMAND_REMOVE;
			end if;
			if ( INPUT_A = '1' and INPUT_B = '1' ) then
				COMMAND_STATE <= COMMAND_ERROR;
			end if;
		end if;
	end process;
end command_func;

