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
library work;
use work.Utilities.all;
-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity clock_module is
    Port ( CLOCK 				: in  STD_LOGIC;
           CLOCK_STATE 		: in  STD_LOGIC;
           SLOW_CLOCK 		: out STD_LOGIC;
			  SLOWEST_CLOCK 	: out STD_LOGIC;
           PWM 				: out STD_LOGIC);
end clock_module;

architecture clock_func of clock_module is
	component FF is
	Port ( CLOCK : in  STD_LOGIC;
			  RESET : in STD_LOGIC;
           D : in  STD_LOGIC;
           Q : out  STD_LOGIC);
	end component;
	
	signal Q : std_logic_vector(10 downto 0) := (others => '0');
	
	-- Q(00) -> 32 KHz
	-- Q(01) -> 16 KHz	
	-- Q(02) -> 8 KHz
	-- Q(03) -> 4 KHz
	-- Q(04) -> 2 KHz
	-- Q(05) -> 1 KHz
	-- Q(06) -> 500 Hz
	-- Q(07) -> 250 Hz
	-- Q(08) -> 125 Hz
	-- Q(09) -> 62.5 Hz
	-- Q(10) -> 31.25 Hz
	
	begin
		
		gen: for i in 0 to 10-1 generate
			inst : FF port map( CLOCK , '0', Q(i), Q(i+1) );
		end generate;
		
		Q(0) 				<= CLOCK;
		SLOW_CLOCK 		<= Q(10-1) and CLOCK_STATE;
		SLOWEST_CLOCK 	<= Q(10) and CLOCK_STATE;
				
		PWM				<= CLOCK_STATE;
		
end clock_func;