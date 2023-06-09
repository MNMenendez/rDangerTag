----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    16:04:52 05/01/2023 
-- Design Name: 
-- Module Name:    MOVEMENT_MODULE - MOVEMENT_FUNC 
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

entity movement_module is
    Port ( MOTOR_STATE 	: in  motor_states;
			  PWM 			: in  STD_LOGIC;
           MOTOR_PWM 	: out  STD_LOGIC;
           MOTOR_UPDOWN	: out  STD_LOGIC_VECTOR(1 downto 0) := (others => '0')
			  );
end movement_module;

architecture movement_func of movement_module is

begin
	MOTOR_PWM 			<= PWM when ( MOTOR_STATE /= STOP ) else '0';
	MOTOR_UPDOWN(0)	<= '1' when ( MOTOR_STATE = MoveToBlank ) else '0';
	MOTOR_UPDOWN(1) 	<= '1' when ( MOTOR_STATE = MoveToDanger ) else '0';
end movement_func;

