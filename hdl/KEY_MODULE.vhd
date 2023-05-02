----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    14:43:36 05/01/2023 
-- Design Name: 
-- Module Name:    KEY_MODULE - Behavioral 
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

entity KEY_MODULE is
    Port ( KEY : in  STD_LOGIC;
           KEY_A_I : in  STD_LOGIC;
           KEY_B_I : in  STD_LOGIC;
           KEY_A_O : out  STD_LOGIC;
           KEY_B_O : out  STD_LOGIC;
           MODE_STATE : out  STD_LOGIC_VECTOR (1 downto 0));
end KEY_MODULE;

architecture KEY_FUNC of KEY_MODULE is

begin


end KEY_FUNC;

