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
		CLK         : in    std_logic; 
  	  	CLK_STATE   : in    std_logic;
  	  	INPUT_A     : in    std_logic;
  	  	INPUT_B     : in    std_logic;
        KEY         : in    std_logic; 
        KEY_A_I     : in    std_logic; 
        KEY_B_I     : in    std_logic; 
        LOCK        : in    std_logic; 
        LOCK_A_I    : in    std_logic; 
        LOCK_B_I    : in    std_logic; 
        POWER_MODE  : in    std_logic; 
        SENSOR_1    : in    std_logic; 
        SENSOR_2    : in    std_logic; 
        SENSOR_3    : in    std_logic; 
        SENSOR_4    : in    std_logic; 
        TBD_I       : in    std_logic; 
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
   signal XLXN_21	: std_logic_vector (1 downto 0);
   signal POWER_SIGNAL	: power_states;
   signal XLXN_88	: std_logic_vector (1 downto 0);
   signal XLXN_89	: std_logic_vector (1 downto 0);
   signal XLXN_90	: std_logic_vector (1 downto 0);
   signal XLXN_167	: std_logic;
   signal XLXN_201	: std_logic_vector (1 downto 0);
   
   component power_module
      Port ( POWER_MODE : in  STD_LOGIC;
           POWER_STATE : out  power_states);
   end component;
   
   component dummy_module
      port ( TBD_I    : in    std_logic;  
             TBD_O    : out   std_logic);
   end component;
   
begin
   XLXI_9 : power_module
      port map (POWER_MODE	=>	POWER_MODE,
                POWER_STATE	=>	POWER_SIGNAL);
   
   XLXI_34 : dummy_module
      port map (TBD_I	=>	TBD_I,
                TBD_O	=>	TBD_O);
   
end BEHAVIORAL;

