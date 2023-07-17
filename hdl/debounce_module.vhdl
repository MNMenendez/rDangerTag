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
    Port ( CLOCK : in  STD_LOGIC;
           CLOCK_STATE : in  STD_LOGIC;
           DATA_I : in  STD_LOGIC_VECTOR (SIZE-1 downto 0);
           DATA_O : out  STD_LOGIC_VECTOR (SIZE-1 downto 0) := (others => '0')
	 );
end debounce_module;

architecture Behavioral of debounce_module is
	--signal counter: integer := 0;
	signal DATA_R: STD_LOGIC_VECTOR(SIZE-1 downto 0) := (others => '0');
	signal RESET_SIGNAL : STD_LOGIC := '0';
	
	component FF_module is
	Port ( CLOCK : in  STD_LOGIC;
			  RESET: in STD_LOGIC;
           D : in  STD_LOGIC;
           Q : out  STD_LOGIC);
	end component;
	
	signal Q : std_logic_vector(4 downto 0) := (others => '0');
begin
	
	gen: for i in 0 to 4-1 generate
		inst : FF_module port map( CLOCK , RESET_SIGNAL , Q(i), Q(i+1) );
	end generate;
		
	DEBOUNCE: process ( CLOCK  ) is
	begin	
		if ( CLOCK_STATE = '0' ) then
			DATA_O <= (others => '0');
		else
			if ( rising_edge ( CLOCK ) ) then
				if ( DATA_I = DATA_R ) then
					RESET_SIGNAL <= '0';
					Q(0) 	<= CLOCK;
					if ( Q = "11111" ) then
						DATA_O <= DATA_I;
					end if;
				else
					RESET_SIGNAL <= '1';
					DATA_O <= (others => '0');
				end if;
				DATA_R <= DATA_I;
			end if;
		end if;
	end process;

	
	
		
end Behavioral;

