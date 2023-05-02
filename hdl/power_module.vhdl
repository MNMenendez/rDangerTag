----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    14:27:43 05/01/2023 
-- Design Name: 
-- Module Name:    POWER - POWER_FUNC 
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

entity power_module is
    Port ( POWER_MODE : in  STD_LOGIC;
           POWER_STATE : out  power_states);
end power_module;

architecture power_func of power_module is

begin

POWER_PROCESS: process (POWER_MODE) is
begin
	if (POWER_MODE = '0') then
		POWER_STATE <= POWER_OFF;
	else
		POWER_STATE <= POWER_ON;
	end if;
end process;

end power_func;

