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
			KEY_A_I 		:		IN		STD_LOGIC;
         KEY_B_I 		: 		IN		STD_LOGIC;
			LOCK_A_I 	:		IN		STD_LOGIC;
         LOCK_B_I 	: 		IN		STD_LOGIC;
         INPUT_A 		: 		IN		STD_LOGIC;
         INPUT_B 		: 		IN		STD_LOGIC;
         SENSOR_A 	: 		IN		STD_LOGIC;
			SENSOR_B 	: 		IN		STD_LOGIC;
         PWR 			: 		IN		STD_LOGIC;
         PWM 			: 		IN		STD_LOGIC;
			KEY 			:		IN		STD_LOGIC;
			LOCK 			:		IN		STD_LOGIC;
			TBD_1 		:		IN		STD_LOGIC;
			TBD_2 		:		OUT	STD_LOGIC;
         ALL_OK 		: 		OUT	STD_LOGIC;
			KEY_A_O 		:		OUT	STD_LOGIC;
         KEY_B_O		: 		OUT	STD_LOGIC;
         MOTOR_ON 	: 		OUT	STD_LOGIC;
         MOTOR_UP 	: 		OUT	STD_LOGIC;
         MOTOR_DOWN 	: 		OUT	STD_LOGIC;
			LOCK_A_O 	:		OUT	STD_LOGIC;
         LOCK_B_O		: 		OUT	STD_LOGIC;
			OUTPUT_A		:		OUT	STD_LOGIC;
			OUTPUT_B		:		OUT	STD_LOGIC
	);
END System_logic;

ARCHITECTURE Behavioral OF System_logic IS

	TYPE SENSOR_STATES 	IS	(DANGER , BLANK , ERROR);
	TYPE MODE_STATES 		IS (REMOTE , LOCAL_APPLY , LOCAL_REMOVE , ERROR);
	TYPE COMMAND_STATES	IS	(APPLY , REMOVE , ERROR);
	TYPE POWER_STATES		IS (POWER_ON , POWER_OFF);
	TYPE MOTOR_STATES		IS (toDANGER , toBLANK , STOP);
	TYPE SYSTEM_STATES	IS (DANGER , BLANK , OFF , ERROR);
	TYPE KEY_STATES		IS (USED , NOT_USED);
	TYPE LOCK_STATES		IS (USED , NOT_USED);

	SIGNAL SENSOR_STATE	: 	SENSOR_STATES	:=	ERROR;
	SIGNAL MODE_STATE 	:	MODE_STATES		:=	ERROR;
	SIGNAL COMMAND_STATE	:	COMMAND_STATES	:=	ERROR;
	SIGNAL POWER_STATE	:	POWER_STATES	:= POWER_OFF;
	SIGNAL MOTOR_STATE	:	MOTOR_STATES	:=	STOP;
	SIGNAL SYSTEM_STATE	:	SYSTEM_STATES	:= OFF;
	SIGNAL KEY_STATE		:	KEY_STATES		:= NOT_USED;
	SIGNAL LOCK_STATE		:	LOCK_STATES		:= NOT_USED;
	
	BEGIN
	
		POWER_PROCESS: PROCESS( PWR ) IS
		BEGIN
			IF ( PWR = '0' ) THEN				-- No energy
				POWER_STATE <= POWER_OFF;
			ELSE										-- Energy
				POWER_STATE <= POWER_ON;
			END IF;
		END PROCESS;
		
		KEY_PROCESS: PROCESS( KEY ) IS
		BEGIN
			IF ( KEY = '1' ) THEN				-- No KEY jumper solded
				KEY_STATE <= USED;
			ELSE										-- KEY jumper solded
				KEY_STATE <= NOT_USED;
			END IF;
		END PROCESS;
		
		LOCK_PROCESS: PROCESS( LOCK ) IS
		BEGIN
			IF ( LOCK = '1' ) THEN				-- No LOCK jumper solded
				LOCK_STATE <= USED;
			ELSE										-- LOCK jumper solded
				LOCK_STATE <= NOT_USED;
			END IF;
		END PROCESS;
		
		--TYPE MODE_STATES 		IS (REMOTE , LOCAL_APPLY , LOCAL_REMOVE , ERROR);			
		MODE_PROCESS: PROCESS( KEY , KEY_A_I , KEY_B_I ) IS
		BEGIN
			IF ( KEY = '0' ) THEN				
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
		COMMAND_PROCESS: PROCESS( INPUT_A , INPUT_B ) IS
		BEGIN
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
		END PROCESS;
		
		--TYPE SENSOR_STATES 	IS	(DANGER , BLANK , ERROR);
		SENSOR_PROCESS: PROCESS( SENSOR_A , SENSOR_B ) IS
		BEGIN
			IF ( SENSOR_A = '0' AND SENSOR_B = '0' ) THEN
				SENSOR_STATE <= ERROR;
			END IF;
			IF ( SENSOR_A = '0' AND SENSOR_B = '1' ) THEN
				SENSOR_STATE <= DANGER;
			END IF;
			IF ( SENSOR_A = '1' AND SENSOR_B = '0' ) THEN
				SENSOR_STATE <= BLANK;
			END IF;
			IF ( SENSOR_A = '1' AND SENSOR_B = '1' ) THEN
				SENSOR_STATE <= ERROR;
			END IF;
		END PROCESS;
		
		--TYPE MOTOR_STATES		IS (toDANGER , toBLANK , STOP);
		MOTOR_PROCESS: PROCESS ( POWER_STATE , LOCK_STATE , MODE_STATE , COMMAND_STATE , SENSOR_STATE ) IS
		BEGIN
			IF ( LOCK_STATE = NOT_USED OR POWER_STATE = POWER_OFF OR MODE_STATE = ERROR OR COMMAND_STATE = ERROR OR SENSOR_STATE = ERROR ) THEN
				MOTOR_STATE 	<= STOP;
			ELSE
				IF ( MOTOR_STATE = toBLANK AND SENSOR_STATE = BLANK ) THEN
					MOTOR_STATE <= STOP;
				END IF;
				IF ( MOTOR_STATE = toDANGER AND SENSOR_STATE = DANGER ) THEN
					MOTOR_STATE <= STOP;
				END IF;
				IF ( MOTOR_STATE = STOP ) THEN
					IF ( SENSOR_STATE = BLANK AND ( ( MODE_STATE = REMOTE AND COMMAND_STATE = APPLY ) OR MODE_STATE = LOCAL_APPLY ) ) THEN
						MOTOR_STATE <= toDANGER;
					END IF;
					IF ( SENSOR_STATE = DANGER AND ( ( MODE_STATE = REMOTE AND COMMAND_STATE = REMOVE ) OR MODE_STATE = LOCAL_REMOVE ) ) THEN
						MOTOR_STATE <= toBLANK;
					END IF;
				END IF;
			END IF;
		END PROCESS;
		
		--TYPE SYSTEM_STATES	IS (DANGER , BLANK , OFF , ERROR)
		SYSTEM_PROCESS: PROCESS ( POWER_STATE , MODE_STATE , COMMAND_STATE , SENSOR_STATE ) IS
		BEGIN
			IF ( POWER_STATE = POWER_OFF ) THEN
				SYSTEM_STATE <= OFF;
			ELSE
				IF ( MODE_STATE = ERROR OR COMMAND_STATE = ERROR OR SENSOR_STATE = ERROR ) THEN
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
			CASE SYSTEM_STATE IS
				WHEN OFF =>
					OUTPUT_A <= '0';
					OUTPUT_B <= '0';
				WHEN ERROR =>
					OUTPUT_A <= '1';
					OUTPUT_B <= '1';
				WHEN DANGER =>
					OUTPUT_A <= '0';
					OUTPUT_B <= '1';
				WHEN BLANK =>
					OUTPUT_A <= '1';
					OUTPUT_B <= '0';
				WHEN OTHERS =>
					OUTPUT_A <= '1';
					OUTPUT_B <= '1';
			END CASE;
		END PROCESS;
		
		
		
		ALL_OK 			<= '1' WHEN (SYSTEM_STATE /= ERROR AND SYSTEM_STATE /= OFF) ELSE '0';
		MOTOR_ON 		<= PWM WHEN ( MOTOR_STATE /= STOP ) ELSE '0';
		MOTOR_UP 		<= '1' WHEN ( MOTOR_STATE = toDANGER ) ELSE '0';
		MOTOR_DOWN 		<= '1' WHEN ( MOTOR_STATE = toBLANK ) ELSE '0';
		KEY_A_O 			<= KEY_A_I;
		KEY_B_O 			<= KEY_B_I;
			
		LOCK_A_O 		<= LOCK_A_I;
		LOCK_B_O 		<= LOCK_B_I;
		TBD_2 			<= TBD_1 AND RST;

END Behavioral;

