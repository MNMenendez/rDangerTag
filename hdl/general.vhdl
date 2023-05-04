--------------------------------------------------------------------------------
-- Copyright (c) 1995-2013 Xilinx, Inc.  All rights reserved.
--------------------------------------------------------------------------------
--   ____  ____ 
--  /   /\/   / 
-- /___/  \  /    Vendor: Xilinx 
-- \   \   \/     Version : 14.7
--  \   \         Application : sch2hdl
--  /   /         Filename : General.vhf
-- /___/   /\     Timestamp : 12/19/2022 11:28:40
-- \   \  /  \ 
--  \___\/\___\ 
--
--Command: sch2hdl -intstyle ise -family xpla3 -flat -suppress -vhdl "Z:/Projects/4201 - 4300/4209 - ART - eDanger Tag/02_Project and Engineering/02_Design/Electronics/CPLD/eDangerTag/General.vhf" -w "Z:/Projects/4201 - 4300/4209 - ART - eDanger Tag/02_Project and Engineering/02_Design/Electronics/CPLD/eDangerTag/General.sch"
--Design Name: General
--Device: xpla3
--Purpose:
--    This vhdl netlist is translated from an ECS schematic. It can be 
--    synthesized and simulated, but it should not be modified. 
--

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

library work;
use work.Utilities.all;

entity General is
	port ( 
		CLK         : in    std_logic := '0'; 
  	  	CLK_STATE   : in    std_logic := '0';
  	  	INPUT_A     : in    std_logic := '0';
  	  	INPUT_B     : in    std_logic := '0';
        KEY         : in    std_logic := '0'; 
        KEY_A_I     : in    std_logic := '0'; 
        KEY_B_I     : in    std_logic := '0'; 
        LOCK        : in    std_logic := '0'; 
        LOCK_A_I    : in    std_logic := '0'; 
        LOCK_B_I    : in    std_logic := '0'; 
        POWER_MODE  : in    std_logic := '0'; 
        SENSOR_1    : in    std_logic := '0'; 
        SENSOR_2    : in    std_logic := '0'; 
        SENSOR_3    : in    std_logic := '0'; 
        SENSOR_4    : in    std_logic := '0'; 
        TBD_I       : in    std_logic := '0'; 
        ALL_OK      : out   std_logic; 
        KEY_A_O     : out   std_logic; 
        KEY_B_O     : out   std_logic; 
        LOCK_A_O    : out   std_logic; 
        LOCK_B_O    : out   std_logic; 
        MOTOR_DOWN  : out   std_logic; 
        MOTOR_PWM   : out   std_logic; 
        MOTOR_UP	: out   std_logic; 
        OUTPUT_A	: out   std_logic; 
        OUTPUT_B	: out   std_logic;
		TBD_O		: out   std_logic;
		WATCHDOG	: out	std_logic
);
end General;

architecture BEHAVIORAL of General is
   signal MODE_SIGNAL		: mode_states;
   signal POWER_SIGNAL		: power_states;
   signal SENSOR_SIGNAL		: sensor_states;
   signal COMMAND_SIGNAL	: command_states;
   signal OK_SIGNAL			: right_states;
   signal SYSTEM_SIGNAL		: system_states;
   signal MOTOR_SIGNAL  	: motors_states;
   
   component power_module
      Port ( POWER_MODE : in  STD_LOGIC;
           POWER_STATE : out  power_states);
   end component;
   
   component key_module is
    Port ( KEY : in  STD_LOGIC;
           KEY_A_I : in  STD_LOGIC;
           KEY_B_I : in  STD_LOGIC;
           KEY_A_O : out  STD_LOGIC;
           KEY_B_O : out  STD_LOGIC;
           MODE_STATE : out  mode_states);
   end component;
	
	component command_module is
    Port ( INPUT_A : in  STD_LOGIC;
           INPUT_B : in  STD_LOGIC;
           MODE_STATE : in  mode_states;
           COMMAND_STATE : out  command_states);
   end component;
   
	component sensor_module is
    Port ( SENSOR_1 : in  STD_LOGIC;
           SENSOR_2 : in  STD_LOGIC;
           SENSOR_3 : in  STD_LOGIC;
           SENSOR_4 : in  STD_LOGIC;
           SENSOR_STATE : out  sensor_states);
   end component;

	component system_module is
    Port ( POWER_STATE 		: in  power_states;
           MODE_STATE 		: in  mode_states;
           COMMAND_STATE 	: in  command_states;
           SENSOR_STATE 	: in  sensor_states;
		   ALL_OK			: out right_states;
           SYSTEM_STATE 	: out system_states);
   end component;
   
   component output_module
      port ( SYSTEM_STATE   : in    system_states; 
      		 OUTPUT_A    	: out   std_logic;
      		 OUTPUT_B    	: out   std_logic);
   end component;
   
   component motor_module is
    Port ( LOCK   	 		: in    std_logic;
           MODE_STATE 		: in  mode_states;
           COMMAND_STATE 	: in  command_states;
           SENSOR_STATE 	: in  sensor_states;
		   MOTOR_STATE		: out motors_states);
   end component;
   
   component lock_module
      port ( LOCK   	 : in    std_logic; 
      		 LOCK_A_I    : in    std_logic;
      		 LOCK_B_I    : in    std_logic;
      		 LOCK_A_O    : out   std_logic;
      		 LOCK_B_O    : out   std_logic);
   end component;

   component dummy_module
      port ( TBD_I    : in    std_logic;  
             TBD_O    : out   std_logic);
   end component;
   
begin
   power_process : power_module
      port map (POWER_MODE	=>	POWER_MODE,
                POWER_STATE	=>	POWER_SIGNAL);
   
   key_process : key_module
		port map (KEY						=> KEY,
   	  			KEY_A_I					=> KEY_A_I,
   	  			KEY_B_I					=> KEY_B_I,
   	  			KEY_A_O					=> KEY_A_O,
   	  			KEY_B_O					=> KEY_B_O,
   	  			MODE_STATE  			=> MODE_SIGNAL);
   
   command_process : command_module
   		port map (INPUT_A				=> INPUT_A,
   	  			  INPUT_B				=> INPUT_B,
   	  			  MODE_STATE			=> MODE_SIGNAL,
   	  			  COMMAND_STATE  		=> COMMAND_SIGNAL);
   
   sensor_process : sensor_module
   		port map (SENSOR_1				=> SENSOR_1,
   	  			  SENSOR_2				=> SENSOR_2,
   	  			  SENSOR_3				=> SENSOR_3,
   	  			  SENSOR_4				=> SENSOR_4,
   	  			  SENSOR_STATE  		=> SENSOR_SIGNAL);
   	  			  
   system_process : system_module
   		port map (COMMAND_STATE			=> COMMAND_SIGNAL,
   	  			  MODE_STATE			=> MODE_SIGNAL,
   	  			  POWER_STATE			=> POWER_SIGNAL,
   	  			  SENSOR_STATE			=> SENSOR_SIGNAL,
   	  			  ALL_OK				=> OK_SIGNAL,
   	  			  SYSTEM_STATE  		=> SYSTEM_SIGNAL);
   	  			  
   output_process : output_module
   		port map (SYSTEM_STATE			=> SYSTEM_SIGNAL,
   	  			  OUTPUT_A				=> OUTPUT_A,
   	  			  OUTPUT_B		 		=> OUTPUT_B);
	
	motor_process : motor_module
   		port map (LOCK					=> LOCK,
   				  COMMAND_STATE			=> COMMAND_SIGNAL,
   	  			  MODE_STATE			=> MODE_SIGNAL,
   	  			  SENSOR_STATE			=> SENSOR_SIGNAL,
   	  			  MOTOR_STATE			=> MOTOR_SIGNAL);
   	  			  
   lock_process : lock_module
   		port map (LOCK 					=> LOCK,
   				  LOCK_A_I				=> LOCK_A_I,
   				  LOCK_B_I				=> LOCK_B_I,
   				  LOCK_A_O				=> LOCK_A_O,
   				  LOCK_B_O				=> LOCK_B_O);
   				  
   dummy_process : dummy_module
      port map (TBD_I	=>	TBD_I,
                TBD_O	=>	TBD_O);
   
end BEHAVIORAL;


