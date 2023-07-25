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

entity sensor_module is
    Port ( SENSORS 		: in  STD_LOGIC_VECTOR(3 downto 0)	:= "0000";
           SENSOR_STATE : out  sensor_states 				:= TRANSITION);
end sensor_module;

architecture sensor_func of sensor_module is

begin
	SENSOR_PROCESS: process ( SENSORS ) is
	begin
		case SENSORS is
			when "0000" | "1111" =>
				SENSOR_STATE <= TRANSITION;
			when "0101" =>
				SENSOR_STATE <= BLANK;
			when "1010" =>
				SENSOR_STATE <= DANGER;
			when others =>
				SENSOR_STATE <= SENSOR_ERROR;
		end case;
	end process;
end sensor_func;
