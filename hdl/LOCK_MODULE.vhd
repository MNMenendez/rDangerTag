----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    16:24:18 05/01/2023 
-- Design Name: 
-- Module Name:    LOCK_MODULE - LOCK_FUNC 
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

entity LOCK_MODULE is
    Port ( LOCK : in  STD_LOGIC;
           LOCK_A_I : in  STD_LOGIC;
           LOCK_B_I : in  STD_LOGIC;
           LOCK_A_O : out  STD_LOGIC;
           LOCK_B_O : out  STD_LOGIC);
end LOCK_MODULE;

architecture LOCK_FUNC of LOCK_MODULE is

begin


end LOCK_FUNC;

