----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    16:04:52 05/01/2023 
-- Design Name: 
-- Module Name:    MOVEMENT_MODULE - MOVEMENT_FUNC 
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

entity MOVEMENT_MODULE is
    Port ( MOTOR_STATE : in  STD_LOGIC_VECTOR (1 downto 0);
			  PWM : in  STD_LOGIC;
           MOTOR_PWM : out  STD_LOGIC;
           MOTOR_UP : out  STD_LOGIC;
           MOTOR_DOWN : out  STD_LOGIC);
end MOVEMENT_MODULE;

architecture MOVEMENT_FUNC of MOVEMENT_MODULE is

begin


end MOVEMENT_FUNC;

