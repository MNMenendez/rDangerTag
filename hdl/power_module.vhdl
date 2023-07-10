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
			  BATTERY_STATE: in STD_LOGIC;
           POWER_STATE : out  power_states);
end power_module;

architecture power_func of power_module is

begin

	POWER_PROCESS: process ( POWER_MODE , BATTERY_STATE ) is
	variable POWER : std_logic_vector(1 downto 0);
	begin
		POWER	  := POWER_MODE & BATTERY_STATE;
			case POWER is
				when "00" =>
					POWER_STATE <= POWER_OFF;
				when "01" =>
					POWER_STATE <= BATTERY;
				when "10" =>
					POWER_STATE <= BATTERY_LOW;
				when "11" =>
					POWER_STATE <= POWER_ON;
				when others =>
					POWER_STATE <= POWER_OFF;
			end case;
	end process;

end power_func;

