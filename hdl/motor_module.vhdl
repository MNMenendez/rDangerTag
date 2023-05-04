----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    15:28:38 05/01/2023 
-- Design Name: 
-- Module Name:    MOTOR_MODULE - MOTOR_FUNC 
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

entity MOTOR_MODULE is
    Port ( LOCK   	 		: in    std_logic;
           MODE_STATE 		: in  mode_states;
           COMMAND_STATE 	: in  command_states;
           SENSOR_STATE 	: in  sensor_states;
		   MOTOR_STATE		: out motors_states);
end MOTOR_MODULE;

architecture MOTOR_FUNC of MOTOR_MODULE is

begin


end MOTOR_FUNC;

