----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    14:54:05 05/01/2023 
-- Design Name: 
-- Module Name:    COMMAND_PROCESS - Behavioral 
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

entity COMMAND_PROCESS is
    Port ( MODE_STATE : in  STD_LOGIC_VECTOR (1 downto 0);
           INPUT_A : in  STD_LOGIC;
           INPUT_B : in  STD_LOGIC;
           COMMAND_STATE : out  STD_LOGIC_VECTOR (1 downto 0));
end COMMAND_PROCESS;

architecture COMMAND_FUNC of COMMAND_PROCESS is

begin


end COMMAND_FUNC;

