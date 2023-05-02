----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    15:18:03 05/01/2023 
-- Design Name: 
-- Module Name:    OUTPUT_MODULE - OUTPUT_FUNC 
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

entity OUTPUT_MODULE is
    Port ( SYSTEM_STATE : in  STD_LOGIC_VECTOR (1 downto 0);
           OUTPUT_A : out  STD_LOGIC;
           OUTPUT_B : out  STD_LOGIC);
end OUTPUT_MODULE;

architecture OUTPUT_FUNC of OUTPUT_MODULE is

begin


end OUTPUT_FUNC;

