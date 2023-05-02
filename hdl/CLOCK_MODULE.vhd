----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    09:34:25 05/02/2023 
-- Design Name: 
-- Module Name:    CLOCK_MODULE - CLOCK_FUNC 
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

entity CLOCK_MODULE is
    Port ( CLOCK : in  STD_LOGIC;
           CLOCK_STATE : in  STD_LOGIC;
           WATCHDOG : out  STD_LOGIC;
           PWM : out  STD_LOGIC);
end CLOCK_MODULE;

architecture CLOCK_FUNC of CLOCK_MODULE is

begin


end CLOCK_FUNC;

