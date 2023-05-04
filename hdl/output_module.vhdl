----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    15:18:03 05/01/2023 
-- Design Name: 
-- Module Name:    OUTPUT_MODULE - OUTPUT_FUNC 
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

entity output_module is
    Port ( SYSTEM_STATE : in  system_states;
           OUTPUT_A : out  STD_LOGIC;
           OUTPUT_B : out  STD_LOGIC);
end output_module;

architecture output_func of output_module is

begin
	OUTPUT_PROCESS: process ( SYSTEM_STATE ) is
	begin
		case SYSTEM_STATE is
			WHEN SYSTEM_ERROR =>
				OUTPUT_A <= '0';
				OUTPUT_B <= '0';
			WHEN SYSTEM_DANGER =>
				OUTPUT_A <= '1';
				OUTPUT_B <= '0';
			WHEN SYSTEM_BLANK =>
				OUTPUT_A <= '0';
				OUTPUT_B <= '1';
			WHEN SYSTEM_TRANSITION =>
				OUTPUT_A <= '1';
				OUTPUT_B <= '1';
			WHEN SYSTEM_BATTERY =>
				OUTPUT_A <= '0';
				OUTPUT_B <= '0';
			WHEN OTHERS =>
				OUTPUT_A <= '0';
				OUTPUT_B <= '0';
		end case;
	end process;

end output_func;

