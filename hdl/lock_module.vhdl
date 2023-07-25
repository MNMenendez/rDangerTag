----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    16:24:18 05/01/2023 
-- Design Name: 
-- Module Name:    LOCK_MODULE - LOCK_FUNC 
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

entity lock_module is
    Port ( LOCK_ENABLE 	: in  STD_LOGIC							:= '1';
           LOCK_I 		: in  STD_LOGIC_VECTOR(1 downto 0)		:= "00";
           LOCK_O 		: out STD_LOGIC_VECTOR(1 downto 0)		:= "00";
		   LOCK_STATE	: out lock_states						:= NO_LOCK);
end lock_module;

architecture lock_func of lock_module is

begin
	LOCK_PROCESS: process ( LOCK_ENABLE , LOCK_I ) is
	variable INTERLOCK : std_logic_vector(2 downto 0);
	begin
		INTERLOCK	  := LOCK_ENABLE & LOCK_I;
		case INTERLOCK is
			when "100" | "101" | "110" | "111" =>
				LOCK_STATE <= NO_LOCK;
				LOCK_O <= LOCK_I;
			when "001" =>
				LOCK_STATE <= LOCK_APPLY;
				LOCK_O <= LOCK_I;
			when "010" =>
				LOCK_STATE <= LOCK_REMOVE;
				LOCK_O <= LOCK_I;
			when "000" | "011" =>
				LOCK_STATE <= LOCK_ERROR;
				LOCK_O <= LOCK_I;
			when others =>
				LOCK_STATE <= LOCK_ERROR;
				LOCK_O <= (others => '0');
		end case;	
	end process;
end lock_func;
