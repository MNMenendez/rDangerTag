library ieee;

use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;

entity PWM_GENERATOR is 
	Generic(
		pwm_setting : integer := 230
    );
	Port( 
		clk : in STD_LOGIC; 
		pwm : out STD_LOGIC
		);
			
end PWM_GENERATOR; 

architecture Behavioral of PWM_GENERATOR is  
signal counter : STD_LOGIC_VECTOR (8-1 downto 0) := (others => '0'); 

signal setting : STD_LOGIC_VECTOR (8-1 downto 0) := (others => '0'); 



begin 
	process (clk) begin 
		if rising_edge(clk) then 
			counter <= counter + 1; 
   		end if; 
	end process; 

setting <= std_logic_vector( to_unsigned( pwm_setting, setting'length));
pwm <= '1' when counter < setting else '0'; 
end Behavioral; 