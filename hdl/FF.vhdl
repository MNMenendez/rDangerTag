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

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity FF is
    Port ( CLOCK : in  STD_LOGIC;
			  RESET : in STD_LOGIC;
           D : in  STD_LOGIC;
           Q : out  STD_LOGIC);
end FF;

architecture Behavioral of FF is

begin
	process ( CLOCK )
	begin
		if ( rising_edge ( CLOCK ) ) then
			if ( RESET = '1' ) then
				Q <= '0';
			else
				Q <= not D;
			end if;
		end if;	
	end process;
end Behavioral;

