----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    12:47:31 02/20/2023 
-- Design Name: 
-- Module Name:    debounceKey - Behavioral 
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

ENTITY debounceKey IS
	GENERIC (                       -- ADDED GENERICS to speed up simulation
        CLKP:   time := 10 ns;
        DEBT:   time := 6.5 ms
    );
    PORT ( 
			CLK 				: IN	 STD_LOGIC;
         preKEY_A_I 		: IN 	 STD_LOGIC;
         preKEY_B_I 		: IN 	 STD_LOGIC;
         KEY_A_I 			: OUT  STD_LOGIC;
         KEY_B_I 			: OUT  STD_LOGIC
			);
END debounceKey;

ARCHITECTURE Behavioral OF debounceKey IS

	TYPE state_type IS (IDLE, WAIT_TIME); --state machine

	CONSTANT DELAY: INTEGER := 65000;
	CONSTANT BTN_ACTIVE : STD_LOGIC := '1';



	SIGNAL count_A : INTEGER := 0;
	SIGNAL count_B : INTEGER := 0;
	SIGNAL state_A : state_type := IDLE;
	SIGNAL state_B : state_type := IDLE;
	
BEGIN
	
	
	KEYS: PROCESS( CLK )
	BEGIN
		IF( RISING_EDGE ( CLK ) ) THEN

			IF ( count_A = 0 ) THEN
				IF( preKEY_A_I = BTN_ACTIVE ) THEN
					count_A <= 1;
				ELSE
					KEY_A_I <= '0';
				END IF;
			END IF;
			
			IF ( count_A > 0 ) THEN
				count_A <= count_A + 1;
			END IF;
			
			IF ( count_A = DELAY AND preKEY_A_I = BTN_ACTIVE ) THEN
				count_A <= 0;
				KEY_A_I <= '1';
			END IF;
		  
--		  CASE (state_A) IS			
--            WHEN IDLE =>
--                IF (preKEY_A_I = BTN_ACTIVE) THEN  
--                    state_A <= wait_time;
--                ELSE
--                    state_A <= idle; --wait until button is pressed.
--                END IF;
--                KEY_A_I <= '0';
--            WHEN WAIT_TIME =>
--                IF(count_A = DELAY) THEN
--                    count_A <= 0;
--                    IF(preKEY_A_I = BTN_ACTIVE) THEN
--                        KEY_A_I <= '1';
--                    END IF;
--                    state_A <= idle;  
--                ELSE
--                    count_A <= count_A + 1;
--                END IF; 
--			END CASE;  
		  
--		  CASE (state_B) IS
--            WHEN IDLE =>
--                IF (preKEY_B_I = BTN_ACTIVE) THEN  
--                    state_B <= wait_time;
--                ELSE
--                    state_B <= idle; --wait until button is pressed.
--                END IF;
--                KEY_B_I <= '0';
--            WHEN WAIT_TIME =>
--                IF(count_B = COUNT_MAX) THEN
--                    count_B <= 0;
--                    IF(preKEY_B_I = BTN_ACTIVE) THEN
--                        KEY_B_I <= '1';
--                    END IF;
--                    state_B <= idle;  
--                ELSE
--                    count_B <= count_B + 1;
--                END IF; 
--        END CASE; 
		END IF;
	END PROCESS;	

END Behavioral;

