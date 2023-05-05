----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    09:34:25 05/02/2023 
-- Design Name: 
-- Module Name:    CLOCK_MODULE - CLOCK_FUNC 
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
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity clock_module is
	Generic( pwm_setting : integer := 12 );
    Port ( CLOCK 		: in  STD_LOGIC;
           CLOCK_STATE 	: in  STD_LOGIC;
           WATCHDOG 	: out  STD_LOGIC;
           PWM 			: out  STD_LOGIC);
end clock_module;

architecture clock_func of clock_module is

	signal counter : integer range 0 to 16 := 0;
begin
	CLOCK_PROCESS: process ( CLOCK , CLOCK_STATE ) is
	begin
		WATCHDOG <= CLOCK_STATE;

		if CLOCK_STATE = '0' then
			counter <= 0;
		else
			if rising_edge (CLOCK) then
				if counter = 16 then
					counter <= 0;
				else
					counter <= counter + 1;
				end if;
			end if;
		end if;
	end process;

	PWM <= '1' when (CLOCK_STATE = '1' and counter < pwm_setting) else '0';

end clock_func;

