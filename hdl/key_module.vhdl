----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    14:43:36 05/01/2023 
-- Design Name: 
-- Module Name:    KEY_MODULE - Behavioral 
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

entity key_module is
    Port ( KEY_ENABLE : in  STD_LOGIC;
           KEY_I : in  STD_LOGIC_VECTOR(1 downto 0);
           KEY_O : out  STD_LOGIC_VECTOR(1 downto 0);
           KEY_STATE : out  key_states);
end key_module;

architecture key_func of key_module is

begin
		
	KEY_PROCESS: process ( KEY_ENABLE , KEY_I ) is
	variable KEY_AB : std_logic_vector(2 downto 0);
	begin	
		KEY_AB	  := KEY_ENABLE & KEY_I;
		case KEY_AB is
			when "000" | "100" | "101" | "110" | "111" =>
				KEY_STATE <= NO_KEY;
			when "001" =>
				KEY_STATE <= KEY_APPLY;
			when "010" =>
				KEY_STATE <= KEY_REMOVE;
			when "011" =>
				KEY_STATE <= KEY_ERROR;
			when others =>
				KEY_STATE <= KEY_ERROR;
		end case;
	end process;
	
	KEY_O <= KEY_I;
	
end key_func;

