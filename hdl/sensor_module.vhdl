----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    15:08:18 05/01/2023 
-- Design Name: 
-- Module Name:    SENSOR_MODULE - SENSOR_FUNC 
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

entity SENSOR_MODULE is
    Port ( SENSOR_1 : in  STD_LOGIC;
           SENSOR_2 : in  STD_LOGIC;
           SENSOR_3 : in  STD_LOGIC;
           SENSOR_4 : in  STD_LOGIC;
           SENSOR_STATE : out  sensor_states);
end SENSOR_MODULE;

architecture SENSOR_FUNC of SENSOR_MODULE is

begin
	SENSOR_PROCESS: process (SENSOR_1,SENSOR_2,SENSOR_3,SENSOR_4) is
	begin
		SENSOR_STATE <= SENSOR_ERROR;
		if ( SENSOR_1 /= SENSOR_3 or SENSOR_2 /= SENSOR_4 ) then
			SENSOR_STATE <= SENSOR_ERROR;
		end if;
		if ( SENSOR_1 = '1' and SENSOR_2 = '0' and SENSOR_3 = '1' and SENSOR_4 = '0' ) then
			SENSOR_STATE <= DANGER;
		end if;
		if ( SENSOR_1 = '0' and SENSOR_2 = '1' and SENSOR_3 = '0' and SENSOR_4 = '1' ) then
			SENSOR_STATE <= BLANK;
		end if;
		if ( SENSOR_1 = SENSOR_2  and SENSOR_2 = SENSOR_3 and SENSOR_3 = SENSOR_4 ) then
			SENSOR_STATE <= TRANSITION;
		end if;
	end process;

end SENSOR_FUNC;

