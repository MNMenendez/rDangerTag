----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    14:24:22 10/05/2022 
-- Design Name: 
-- Module Name:    System_logic - Behavioral 
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

ENTITY System_logic IS
	PORT( 
			RST			:		IN 	STD_LOGIC;	
			PWR 			: 		IN		STD_LOGIC;
         PWM 			: 		IN		STD_LOGIC;
			INPUT_A 		: 		IN		STD_LOGIC;
         INPUT_B 		: 		IN		STD_LOGIC;
			KEY 			:		IN		STD_LOGIC;
			KEY_A_I 		:		IN		STD_LOGIC;
         KEY_B_I 		: 		IN		STD_LOGIC;
			LOCK 			:		IN		STD_LOGIC;
			LOCK_A_I 	:		IN		STD_LOGIC;
         LOCK_B_I 	: 		IN		STD_LOGIC; 
         SENSOR_1 	: 		IN		STD_LOGIC;
			SENSOR_2 	: 		IN		STD_LOGIC;
			SENSOR_3 	: 		IN		STD_LOGIC;
			SENSOR_4 	: 		IN		STD_LOGIC;
			TBD_I 		:		IN		STD_LOGIC;
			TBD_O 		:		OUT	STD_LOGIC;
			MOTOR_ON 	: 		OUT	STD_LOGIC;
         MOTOR_UP 	: 		OUT	STD_LOGIC;
         MOTOR_DOWN 	: 		OUT	STD_LOGIC;
			OUTPUT_A		:		OUT	STD_LOGIC;
			OUTPUT_B		:		OUT	STD_LOGIC;
			KEY_A_O 		:		OUT	STD_LOGIC;
         KEY_B_O		: 		OUT	STD_LOGIC;
			LOCK_A_O 	:		OUT	STD_LOGIC;
         LOCK_B_O		: 		OUT	STD_LOGIC;
			ALL_OK 		: 		OUT	STD_LOGIC
	);
END System_logic;

ARCHITECTURE Behavioral OF System_logic IS

	TYPE SENSOR_STATES 	IS	(DANGER , BLANK , TRANSITION, ERROR);
	TYPE MODE_STATES 		IS (REMOTE , LOCAL_APPLY , LOCAL_REMOVE , ERROR);
	TYPE COMMAND_STATES	IS	(APPLY , REMOVE , ERROR , IGNORE);
	TYPE POWER_STATES		IS (POWER_ON , POWER_OFF);
	TYPE MOTOR_STATES		IS (toDANGER , toBLANK , STOP);
	TYPE SYSTEM_STATES	IS (DANGER , BLANK , OFF , ERROR);
	TYPE KEY_FEATURES		IS (USED , NOT_USED);
	TYPE LOCK_FEATURES	IS (USED , NOT_USED);

	SIGNAL SENSOR_STATE	: 	SENSOR_STATES	:=	TRANSITION;
	SIGNAL MODE_STATE 	:	MODE_STATES		:=	ERROR;
	SIGNAL COMMAND_STATE	:	COMMAND_STATES	:=	IGNORE;
	SIGNAL POWER_STATE	:	POWER_STATES	:= POWER_OFF;
	SIGNAL MOTOR_STATE	:	MOTOR_STATES	:=	STOP;
	SIGNAL SYSTEM_STATE	:	SYSTEM_STATES	:= OFF;
	SIGNAL KEY_FEATURE	:	KEY_FEATURES	:= NOT_USED;
	SIGNAL LOCK_FEATURE	:	LOCK_FEATURES	:= NOT_USED;
	
	BEGIN
	
		--TYPE POWER_STATES 		IS  (POWER_ON , POWER_OFF);
		POWER_PROCESS: PROCESS( PWR ) IS
		BEGIN
			IF ( PWR = '0' ) THEN				-- No energy
				POWER_STATE <= POWER_OFF;
			ELSE										-- Energy
				POWER_STATE <= POWER_ON;
			END IF;
		END PROCESS;
		
		--TYPE KEY_FEATURES		IS (USED , NOT_USED);
		KEY_PROCESS: PROCESS( KEY ) IS
		BEGIN
			IF ( KEY = '1' ) THEN				-- No KEY jumper solded
				KEY_FEATURE <= USED;
			ELSE										-- KEY jumper solded
				KEY_FEATURE <= NOT_USED;
			END IF;
		END PROCESS;
		
		--TYPE LOCK_FEATURES	IS (USED , NOT_USED);
		LOCK_PROCESS: PROCESS( LOCK ) IS
		BEGIN
			IF ( LOCK = '1' ) THEN				-- No LOCK jumper solded
				LOCK_FEATURE <= USED;
			ELSE										-- LOCK jumper solded
				LOCK_FEATURE <= NOT_USED;
			END IF;
		END PROCESS;
		
		--TYPE MODE_STATES 		IS (REMOTE , LOCAL_APPLY , LOCAL_REMOVE , ERROR);			
		MODE_PROCESS: PROCESS( KEY_FEATURE , KEY_A_I , KEY_B_I ) IS
		BEGIN
			IF ( KEY_FEATURE = NOT_USED ) THEN				
				MODE_STATE <= REMOTE;
			ELSE										
				IF ( KEY_A_I = '0' AND KEY_B_I = '0' ) THEN
					MODE_STATE <= REMOTE;
				END IF;
				IF ( KEY_A_I = '0' AND KEY_B_I = '1' ) THEN
					MODE_STATE <= LOCAL_APPLY;
				END IF;
				IF ( KEY_A_I = '1' AND KEY_B_I = '0' ) THEN
					MODE_STATE <= LOCAL_REMOVE;
				END IF;
				IF ( KEY_A_I = '1' AND KEY_B_I = '1' ) THEN
					MODE_STATE <= ERROR;
				END IF;
			END IF;
		END PROCESS;
		
		--TYPE COMMAND_STATES	IS	(APPLY , REMOVE , ERROR)	
		COMMAND_PROCESS: PROCESS( MODE_STATE , INPUT_A , INPUT_B ) IS
		BEGIN
			IF ( MODE_STATE /= REMOTE ) THEN
				COMMAND_STATE <= IGNORE;
			ELSE
				IF ( INPUT_A = '0' AND INPUT_B = '0' ) THEN
					COMMAND_STATE <= ERROR;
				END IF;
				IF ( INPUT_A = '0' AND INPUT_B = '1' ) THEN
					COMMAND_STATE <= APPLY;
				END IF;
				IF ( INPUT_A = '1' AND INPUT_B = '0' ) THEN
					COMMAND_STATE <= REMOVE;
				END IF;
				IF ( INPUT_A = '1' AND INPUT_B = '1' ) THEN
					COMMAND_STATE <= ERROR;
				END IF;
			END IF;
		END PROCESS;
		
		--TYPE SYSTEM_STATES	IS (DANGER , BLANK , OFF , ERROR)
		SYSTEM_PROCESS: PROCESS ( POWER_STATE , MODE_STATE , COMMAND_STATE , SENSOR_STATE ) IS
		BEGIN
			IF ( POWER_STATE = POWER_OFF ) THEN
				SYSTEM_STATE <= OFF;
			ELSE
				IF ( MODE_STATE = ERROR OR COMMAND_STATE = ERROR OR SENSOR_STATE = ERROR) THEN
					SYSTEM_STATE <= ERROR;
				ELSE
					IF ( SENSOR_STATE = DANGER ) THEN
						SYSTEM_STATE <= DANGER;
					END IF;
					IF ( SENSOR_STATE = BLANK ) THEN
						SYSTEM_STATE <= BLANK;
					END IF;
				END IF;
			END IF;
		END PROCESS;
		
		OUTPUT_PROCESS: PROCESS ( SYSTEM_STATE ) IS
		BEGIN
			CASE (SYSTEM_STATE) IS
				WHEN OFF =>
					OUTPUT_A <= '0';
					OUTPUT_B <= '0';
				WHEN DANGER =>
					OUTPUT_A <= '0';
					OUTPUT_B <= '1';
				WHEN BLANK =>
					OUTPUT_A <= '1';
					OUTPUT_B <= '0';
				WHEN ERROR =>
					OUTPUT_A <= '1';
					OUTPUT_B <= '1';
				WHEN OTHERS =>
					OUTPUT_A <= '1';
					OUTPUT_B <= '1';
			END CASE;
		END PROCESS;		
		
		SENSOR_PROCESS: PROCESS( SENSOR_1 , SENSOR_2 , SENSOR_3 , SENSOR_4 ) IS
		BEGIN	-- Sensor 1&3 vs Sensor 2&4
			IF ( SENSOR_1 /= SENSOR_3 OR SENSOR_2 /= SENSOR_4 ) THEN
				SENSOR_STATE <= ERROR;
			ELSE	--	1 = 3 AND 2 = 4
				IF ( SENSOR_1 = '0' AND SENSOR_2 = '0' ) THEN
					SENSOR_STATE <= TRANSITION;
				END IF;
				IF ( SENSOR_1 = '1' AND SENSOR_2 = '0' ) THEN
					SENSOR_STATE <= DANGER;
				END IF;
				IF ( SENSOR_1 = '0' AND SENSOR_2 = '1' ) THEN
					SENSOR_STATE <= BLANK;
				END IF;
				IF ( SENSOR_1 = '1' AND SENSOR_2 = '1' ) THEN
					SENSOR_STATE <= TRANSITION;
				END IF;
			END IF;
		END PROCESS;

		--TYPE MOTOR_STATES		IS (toDANGER , toBLANK , STOP);
		MOTOR_PROCESS: PROCESS ( POWER_STATE, LOCK_FEATURE, MODE_STATE , COMMAND_STATE, SENSOR_STATE ) IS
		BEGIN
			IF ( LOCK_FEATURE = NOT_USED OR POWER_STATE = POWER_OFF OR MODE_STATE = ERROR OR COMMAND_STATE = ERROR OR SENSOR_STATE = ERROR ) THEN
				MOTOR_STATE <= STOP;
			ELSE
				CASE (MODE_STATE) IS
					WHEN LOCAL_REMOVE =>
						IF (SENSOR_STATE /= BLANK) THEN
							MOTOR_STATE <= toBLANK;
						ELSE
							MOTOR_STATE <= STOP;
						END IF;
					WHEN LOCAL_APPLY =>
						IF (SENSOR_STATE /= DANGER) THEN
							MOTOR_STATE <= toDANGER;
						ELSE
							MOTOR_STATE <= STOP;
						END IF;
					WHEN REMOTE =>
						IF ( SENSOR_STATE /= DANGER AND COMMAND_STATE = APPLY ) THEN
							MOTOR_STATE <= toDANGER;
						ELSE
							MOTOR_STATE <= STOP;
						END IF;
						IF ( SENSOR_STATE /= BLANK AND COMMAND_STATE = REMOVE ) THEN
							MOTOR_STATE <= toBLANK;
						ELSE
							MOTOR_STATE <= STOP;
						END IF;
					WHEN ERROR =>
						MOTOR_STATE <= STOP;
				END CASE;
			END IF;
		END PROCESS;

		MOTOR_MOVEMENT: PROCESS ( MOTOR_STATE ) IS
		BEGIN
			CASE (MOTOR_STATE) IS
				WHEN toBLANK =>			-- >>
					MOTOR_ON 	<= PWM;	--PWM;
					MOTOR_UP 	<= '1';
					MOTOR_DOWN 	<= '0';
				WHEN toDANGER =>			-- <<
					MOTOR_ON 	<= PWM;	--PWM;
					MOTOR_UP 	<= '0';
					MOTOR_DOWN 	<= '1';
				WHEN STOP =>				-- STOP
					MOTOR_ON		<= '0';
					MOTOR_UP 	<= '0';
					MOTOR_DOWN 	<= '0';
			END CASE;
		END PROCESS;		
	
		ALL_OK 			<= '1' WHEN (SYSTEM_STATE /= ERROR AND SYSTEM_STATE /= OFF) ELSE '0';

		KEY_A_O 			<= KEY_A_I;
		KEY_B_O 			<= KEY_B_I;
			
		LOCK_A_O 		<= LOCK_A_I;
		LOCK_B_O 		<= LOCK_B_I;
		TBD_O 			<= TBD_I AND RST;

END Behavioral;

