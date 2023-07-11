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
library work;
use work.Utilities.all;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity PLC_module is
    Port ( PLC_I : in  STD_LOGIC_VECTOR(1 downto 0);
           PLC_STATE : out  plc_states := PLC_IDLE);
end PLC_module;

architecture PLC_func of PLC_module is

begin
	PLC_PROCESS : process ( PLC_I ) is
	begin
		case PLC_I is
			when "01" =>
				PLC_STATE <= PLC_APPLY;
			when "10" =>
				PLC_STATE <= PLC_REMOVE;
			when others =>
				PLC_STATE <= PLC_ERROR;
		end case;
	end process;
end PLC_func;

