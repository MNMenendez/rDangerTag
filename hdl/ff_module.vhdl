----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    14:35:08 07/06/2023 
-- Design Name: 
-- Module Name:    FF - Behavioral 
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
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity ff_module is
    Port ( CLOCK : in  STD_LOGIC		:= '0'; 
		   RESET : in STD_LOGIC			:= '0';	
           CLOCK_OUT : out  STD_LOGIC	:= '0');
end ff_module;

architecture ff_func of ff_module is

signal CLOCK_AUX : STD_LOGIC := '0';
begin
	process ( CLOCK , RESET )
	begin
		if ( RESET = '1' ) then
			CLOCK_AUX <= '0';
		elsif ( rising_edge ( CLOCK ) ) then
			CLOCK_AUX <= not CLOCK_AUX;
		end if;
	end process;
	CLOCK_OUT <= CLOCK_AUX;
end ff_func;

