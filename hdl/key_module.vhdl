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
library work;
use work.Utilities.all;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity key_module is
    Port ( KEY : in  STD_LOGIC;
           KEY_A_I : in  STD_LOGIC;
           KEY_B_I : in  STD_LOGIC;
           KEY_A_O : out  STD_LOGIC;
           KEY_B_O : out  STD_LOGIC;
           MODE_STATE : out  mode_states);
end key_module;

architecture key_func of key_module is

begin

	MODE_PROCESS: process (KEY,KEY_A_I,KEY_B_I) is
	begin	
		if (KEY = '0') then
			MODE_STATE <= REMOTE;
		else
			if (KEY_A_I = '0' and KEY_B_I = '0') then
				MODE_STATE <= REMOTE;
			end if;
			if (KEY_A_I = '0' and KEY_B_I = '1') then
				MODE_STATE <= LOCAL_APPLY;
			end if;
			if (KEY_A_I = '1' and KEY_B_I = '0') then
				MODE_STATE <= LOCAL_REMOVE;
			end if;
			if (KEY_A_I = '1' and KEY_B_I = '1') then
				MODE_STATE <= MODE_ERROR;
			end if;
		end if;
	end process;
	
	KEY_A_O <= KEY_A_I;
	KEY_B_O <= KEY_B_I;
	
end key_func;

