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
           SENSOR_STATE : out  STD_LOGIC_VECTOR (1 downto 0));
end SENSOR_MODULE;

architecture SENSOR_FUNC of SENSOR_MODULE is

begin


end SENSOR_FUNC;

