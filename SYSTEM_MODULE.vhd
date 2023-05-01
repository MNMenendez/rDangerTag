----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    15:11:48 05/01/2023 
-- Design Name: 
-- Module Name:    SYSTEM_MODULE - SYSTEM_FUNC 
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

entity SYSTEM_MODULE is
    Port ( POWER_STATE : in  STD_LOGIC;
           MODE_STATE : in  STD_LOGIC_VECTOR (1 downto 0);
           COMMAND_STATE : in  STD_LOGIC_VECTOR (1 downto 0);
           SENSOR_STATE : in  STD_LOGIC_VECTOR (1 downto 0);
			  ALL_OK			: out STD_LOGIC;
           SYSTEM_STATE : out  STD_LOGIC_VECTOR (1 downto 0));
end SYSTEM_MODULE;

architecture SYSTEM_FUNC of SYSTEM_MODULE is

begin


end SYSTEM_FUNC;

