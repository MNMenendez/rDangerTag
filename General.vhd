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

library ieee;
use ieee.std_logic_1164.ALL;
use ieee.numeric_std.ALL;
library UNISIM;
use UNISIM.Vcomponents.ALL;

entity General is
   port ( CLK        : in    std_logic; 
          KEY        : in    std_logic; 
          KEY_A_i    : in    std_logic; 
          KEY_B_i    : in    std_logic; 
          LOCK       : in    std_logic; 
          PWR        : in    std_logic; 
          SENSOR_A   : in    std_logic; 
          SENSOR_B   : in    std_logic; 
          TTL_A      : in    std_logic; 
          TTL_B      : in    std_logic; 
          ALL_OK     : out   std_logic; 
          KEY_A_o    : out   std_logic; 
          KEY_B_o    : out   std_logic; 
          MOTOR_DOWN : out   std_logic; 
          MOTOR_ON   : out   std_logic; 
          MOTOR_UP   : out   std_logic; 
          OUTPUT_A   : out   std_logic; 
          OUTPUT_B   : out   std_logic);
end General;

architecture BEHAVIORAL of General is
   signal XLXN_19    : std_logic;
   component PWM_GENERATOR
      port ( clk : in    std_logic; 
             pwm : out   std_logic);
   end component;
   
   component System_logic
      port ( INPUT_A    : in    std_logic; 
             INPUT_B    : in    std_logic; 
             SENSOR_A   : in    std_logic; 
             SENSOR_B   : in    std_logic; 
             PWR        : in    std_logic; 
             PWM        : in    std_logic; 
             KEY        : in    std_logic; 
             LOCK       : in    std_logic; 
             ALL_OK     : out   std_logic; 
             MOTOR_ON   : out   std_logic; 
             MOTOR_UP   : out   std_logic; 
             MOTOR_DOWN : out   std_logic; 
             OUTPUT_A   : out   std_logic; 
             OUTPUT_B   : out   std_logic; 
             KEY_A_I    : in    std_logic; 
             KEY_B_I    : in    std_logic; 
             KEY_A_O    : out   std_logic; 
             KEY_B_O    : out   std_logic);
   end component;
   
begin
   XLXI_6 : PWM_GENERATOR
      port map (clk=>CLK,
                pwm=>XLXN_19);
   
   XLXI_7 : System_logic
      port map (INPUT_A=>TTL_A,
                INPUT_B=>TTL_B,
                KEY=>KEY,
                KEY_A_I=>KEY_A_i,
                KEY_B_I=>KEY_B_i,
                LOCK=>LOCK,
                PWM=>XLXN_19,
                PWR=>PWR,
                SENSOR_A=>SENSOR_A,
                SENSOR_B=>SENSOR_B,
                ALL_OK=>ALL_OK,
                KEY_A_O=>KEY_A_o,
                KEY_B_O=>KEY_B_o,
                MOTOR_DOWN=>MOTOR_DOWN,
                MOTOR_ON=>MOTOR_ON,
                MOTOR_UP=>MOTOR_UP,
                OUTPUT_A=>OUTPUT_A,
                OUTPUT_B=>OUTPUT_B);
   
end BEHAVIORAL;


