----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    15:49:25 07/03/2023 
-- Design Name: 
-- Module Name:    debounce - Behavioral 
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

entity debounce_module is
	 Generic ( SIZE : integer := 2 );
    Port ( CLOCK : in  STD_LOGIC								:= '0';
           CLOCK_STATE : in  STD_LOGIC							:= '1';
           DATA_I : in  STD_LOGIC_VECTOR (SIZE-1 downto 0)		:= (others => '0');
           DATA_O : out  STD_LOGIC_VECTOR (SIZE-1 downto 0) 	:= (others => '0')
	 );
end debounce_module;

architecture Behavioral of debounce_module is
	--signal counter: integer := 0;
	signal DATA_R: STD_LOGIC_VECTOR(SIZE-1 downto 0) := (others => '0');
	signal RESET_SIGNAL : STD_LOGIC := '0';
	signal DONE : STD_LOGIC := '0';
	component ff_module is
	Port ( CLOCK : in  STD_LOGIC;
		   RESET: in STD_LOGIC;
           CLOCK_OUT : out  STD_LOGIC);
	end component;
	
	signal Q : std_logic_vector(5 downto 0) := (others => '1');
begin
	
	gen: for i in 0 to 5-1 generate
		inst : ff_module port map( Q(i) , RESET_SIGNAL , Q(i+1) );
	end generate;
		
	Q(0) <= CLOCK;
	
	DEBOUNCE: process ( CLOCK , CLOCK_STATE  ) is
	begin	
		if ( CLOCK_STATE = '0' ) then
			DATA_O <= (others => '0');
			RESET_SIGNAL <= '1';
		else
			if ( rising_edge ( CLOCK ) ) then
				if ( DATA_I = DATA_R ) then
					RESET_SIGNAL <= '0';
					if ( Q = "001000" ) then
						DATA_O <= DATA_I;
						DONE <= '1';
					else
						DONE <= '0';
					end if;
				else
					RESET_SIGNAL <= '1';
					--DATA_O <= (others => '0');
				end if;
				DATA_R <= DATA_I;
			end if;
		end if;
	end process;

	
	
		
end Behavioral;

