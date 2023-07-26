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
library work;
use work.Utilities.all;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity output_module is
    Port ( 	SYSTEM_STATE 	: in  system_states							:= SYSTEM_IDLE;
			POWER_STATE		: in power_states							:= POWER_ON;
			SLOWEST_CLOCK 	: in STD_LOGIC								:= '0';		
			OK_LED		   	: out STD_LOGIC_VECTOR(1 downto 0) 			:= "00";
			PWR_LED	   		: out STD_LOGIC_VECTOR(1 downto 0) 			:= "00";
           	OUTPUT 			: out  STD_LOGIC_VECTOR(1 downto 0) 		:= "00");
end output_module;

architecture output_func of output_module is
signal PWR_LED_SIGNAL:	led_states 							:= RED;
signal OK_LED_SIGNAL:	led_states 							:= RED;
signal PWR_LED_COLOR_A:	STD_LOGIC_VECTOR(1 downto 0) 		:= "00";
signal PWR_LED_COLOR_B:	STD_LOGIC_VECTOR(1 downto 0) 		:= "00";
signal OK_LED_COLOR_A:	STD_LOGIC_VECTOR(1 downto 0) 		:= "00";
signal OK_LED_COLOR_B:	STD_LOGIC_VECTOR(1 downto 0) 		:= "00";
begin
	OUTPUT_PROCESS: process ( SYSTEM_STATE ) is
	begin
		case SYSTEM_STATE is
			WHEN SYSTEM_ERROR =>
				OUTPUT <= "00";
			WHEN SYSTEM_DANGER =>
				OUTPUT <= "01";
			WHEN SYSTEM_BLANK =>
				OUTPUT <= "10";
			WHEN SYSTEM_TRANSITION =>
				NULL;
			WHEN SYSTEM_TIMEOUT =>
				OUTPUT <= "00";
			WHEN SYSTEM_IDLE =>
				OUTPUT <= "11";
			WHEN OTHERS =>
				OUTPUT <= "00";
		end case;
	end process;

	LED_STATE_PROCESS: process ( POWER_STATE , SYSTEM_STATE ) is
	begin
		case POWER_STATE is
			WHEN POWER_OFF =>					-- No power, no battery
				PWR_LED_SIGNAL 			<= OFF;	
				PWR_LED_COLOR_A			<= "00";
			WHEN POWER_ON =>					-- Power and battery
				PWR_LED_SIGNAL 			<= GREEN;
				PWR_LED_COLOR_A			<= "10";
			WHEN BATTERY =>						-- No power, but battery
				PWR_LED_SIGNAL 			<= FLASHING;
			WHEN BATTERY_LOW =>					-- Power, but battery flat
				PWR_LED_SIGNAL 			<= AMBER;
				PWR_LED_COLOR_A			<= "11";
			WHEN OTHERS =>						-- No power, no battery
				PWR_LED_SIGNAL <= RED;
				PWR_LED_COLOR_A			<= "01";
		end case;
		
		if ( SYSTEM_STATE = SYSTEM_ERROR ) then
        	OK_LED_SIGNAL 				<= RED;
        	OK_LED_COLOR_A				<= "01";
        else 
        	if ( POWER_STATE = POWER_ON or POWER_STATE = BATTERY ) then
        		OK_LED_SIGNAL 			<= GREEN;
        		OK_LED_COLOR_A			<= "10";
        	elsif ( POWER_STATE = BATTERY_LOW ) then
        		OK_LED_SIGNAL  			<= FLASHING;
        	else
        		OK_LED_SIGNAL 			<= RED;
        		OK_LED_COLOR_A			<= "01";
        	end if;
        end if;
	end process;
	
	LED_COLOR_PROCESS: process ( SLOWEST_CLOCK ) is
	begin
		if SLOWEST_CLOCK = '1' then
			PWR_LED_COLOR_B <= "11";
			OK_LED_COLOR_B <= "11";
		else
			PWR_LED_COLOR_B <= "00";
			OK_LED_COLOR_B <= "00";
		end if;
	end process;
	
	PWR_LED <= PWR_LED_COLOR_A when ( POWER_STATE /= BATTERY ) else PWR_LED_COLOR_B;
	OK_LED <= OK_LED_COLOR_A when ( POWER_STATE /= BATTERY_LOW ) else OK_LED_COLOR_B;
	
	--LED_PROCESS : process ( SLOWEST_CLOCK ) is
	--begin
	--	if ( rising_edge( SLOWEST_CLOCK ) ) then
	--		case PWR_LED_SIGNAL is
	--			WHEN RED =>
	--				PWR_LED_COLOR <= "00";
	--			WHEN AMBER =>
	--				PWR_LED_COLOR <= "01";
	--			WHEN FLASHING =>
	--				PWR_LED_COLOR <= PWR_LED_COLOR(1) & not PWR_LED_COLOR(0);
	--			WHEN GREEN =>
	--				PWR_LED_COLOR <= "11";
	--			WHEN others =>
	--				NULL;
	--		end case;
	--	
	--		case OK_LED_SIGNAL is
	--			WHEN RED =>
	--				OK_LED_COLOR <= "00";
	--			WHEN AMBER =>
	--				OK_LED_COLOR <= "01";
	--			WHEN FLASHING =>
	--				OK_LED_COLOR <= OK_LED_COLOR(1) & not OK_LED_COLOR(0);
	--			WHEN GREEN =>
	--				OK_LED_COLOR <= "11";
	--			WHEN others =>
	--				NULL;
	--		end case;
	--	end if;
	--end process;
	
	--PWR_LED <= PWR_LED_COLOR;
	--OK_LED <= OK_LED_COLOR;
end output_func;

