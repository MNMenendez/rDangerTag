LIBRARY ieee;

USE ieee.std_logic_1164.all;
USE ieee.std_logic_unsigned.all;
USE ieee.numeric_std.all;

ENTITY WATCHDOG IS 
	GENERIC(
		WTD_SETTING : INTEGER := 230
    );
	PORT( 
		CLK 	: 	IN 	STD_LOGIC; 
		WTD 	: 	OUT 	STD_LOGIC
		);
			
END WATCHDOG; 

ARCHITECTURE Behavioral OF WATCHDOG IS  

	SIGNAL COUNT			:	INTEGER 			:= 1;
	SIGNAL TMP				:	STD_LOGIC		:= '0';

	BEGIN 
		WTD_PROCESS: PROCESS ( CLK ) IS
		BEGIN
			IF ( rising_edge(CLK) AND CLK = '1' ) THEN
				COUNT <= COUNT + 1;
				IF ( COUNT = 25000 ) THEN
					TMP <= NOT TMP;
					COUNT <= 1;
				END IF;
			END IF;
		END PROCESS;

		WTD <= TMP;
END Behavioral; 