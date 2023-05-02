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

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity MOTOR_MODULE is
    Port ( LOCK : in  STD_LOGIC;
           PWR_STATE : in  STD_LOGIC;
           MODE_STATE : in  STD_LOGIC_VECTOR (1 downto 0);
           COMMAND_STATE : in  STD_LOGIC_VECTOR (1 downto 0);
           SENSOR_STATE : in  STD_LOGIC_VECTOR (1 downto 0);
           MOTOR_STATE : out  STD_LOGIC_VECTOR (1 downto 0));
end MOTOR_MODULE;

architecture MOTOR_FUNC of MOTOR_MODULE is

begin


end MOTOR_FUNC;

