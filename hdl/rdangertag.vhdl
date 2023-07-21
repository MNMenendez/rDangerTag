--------------------------------------------------------------------------------
-- Copyright (c) 1995-2013 Xilinx, Inc.  All rights reserved.
--------------------------------------------------------------------------------
--   ____  ____ 
--  /   /\/   / 
-- /___/  \  /    Vendor: Xilinx 
-- \   \   \/     Version : 14.7
--  \   \         Application : sch2hdl
--  /   /         Filename : rDangerTag.vhf
-- /___/   /\     Timestamp : 07/04/2023 14:57:27
-- \   \  /  \ 
--  \___\/\___\ 
--
--Command: sch2hdl -intstyle ise -family xc9500xl -flat -suppress -vhdl "Z:/Projects/4201 - 4300/4209 - ART - eDanger Tag/02_Project and Engineering/02_Design/Electronics/CPLD/rDangerTag/rDangerTag.vhf" -w "Z:/Projects/4201 - 4300/4209 - ART - eDanger Tag/02_Project and Engineering/02_Design/Electronics/CPLD/rDangerTag/rDangerTag.sch"
--Design Name: rDangerTag
--Device: xc9500xl
--Purpose:
--    This vhdl netlist is translated from an ECS schematic. It can be 
--    synthesized and simulated, but it should not be modified. 
--

library ieee;
use ieee.std_logic_1164.ALL;
use ieee.numeric_std.ALL;
--library UNISIM;
--use UNISIM.Vcomponents.ALL;
library work;
use work.Utilities.all;

entity rDangerTag is
   port ( BATT_STATE   : in    std_logic; 
          CLOCK        : in    std_logic; 
          CLOCK_STATE : in    std_logic; 
          KEY_ENABLE   : in    std_logic; 
          KEY_I        : in    std_logic_vector (1 downto 0); 
          LOCK_ENABLE  : in    std_logic; 
          LOCK_I       : in    std_logic_vector (1 downto 0); 
          PLC          : in    std_logic_vector (1 downto 0); 
          POWER_MODE   : in    std_logic; 
          SENSORS      : in    std_logic_vector (3 downto 0)	:= "0000"; 
          KEY_O        : out   std_logic_vector (1 downto 0); 
          LOCK_O       : out   std_logic_vector (1 downto 0); 
          MOTOR        : out   std_logic_vector (1 downto 0); 
          MOTOR_PWM    : out   std_logic; 
          OK_LED       : out   std_logic_vector (1 downto 0); 
          OUTPUT       : out   std_logic_vector (1 downto 0); 
          PWR_LED      : out   std_logic_vector (1 downto 0); 
          TBD_O        : out   std_logic;
		  WATCHDOG     : out   std_logic);
end rDangerTag;

architecture BEHAVIORAL of rDangerTag is
   signal COMMAND_STATE : command_states;
   signal DATA_O        : std_logic_vector (1 downto 0);
   signal KEY_STATE     : key_states;
   signal LOCK_STATE    : lock_states;
   signal MOTOR_STATE   : motor_states;
   signal PLC_STATE     : plc_states;
   signal POWER_STATE   : power_states;
   signal PWM_SIGNAL    : std_logic;
   signal SENSOR_STATE  : sensor_states;
   signal SLOWEST_CLOCK : std_logic;
   signal SLOW_CLOCK    : std_logic;
   signal SYSTEM_STATE  : system_states;
   component clock_module
      port ( CLOCK         : in    std_logic; 
             CLOCK_STATE   : in    std_logic; 
             SLOW_CLOCK    : out   std_logic; 
             SLOWEST_CLOCK : out   std_logic; 
             PWM           : out   std_logic);
   end component;
   
   component command_module
      port ( COMMAND_STATE : out   command_states; 
             KEY_STATE     : in    key_states; 
             PLC_STATE     : in    plc_states; 
             LOCK_STATE    : in    lock_states);
   end component;
   
   component debounce_module
      port ( CLOCK_STATE : in    std_logic; 
             DATA_I      : in    std_logic_vector (1 downto 0); 
             DATA_O      : out   std_logic_vector (1 downto 0); 
             CLOCK       : in    std_logic);
   end component;
   
   component dummy_module
      port ( TBD_O : out   std_logic);
   end component;
   
   component key_module
      port ( KEY_ENABLE : in    std_logic; 
             KEY_I      : in    std_logic_vector (1 downto 0); 
             KEY_O      : out   std_logic_vector (1 downto 0); 
             KEY_STATE  : out   key_states);
   end component;
   
   component lock_module
      port ( LOCK_ENABLE : in    std_logic; 
             LOCK_STATE  : out   lock_states; 
             LOCK_I      : in    std_logic_vector (1 downto 0); 
             LOCK_O      : out   std_logic_vector (1 downto 0));
   end component;
   
   component movement_module
      port ( MOTOR_STATE  : in    motor_states; 
             MOTOR_UPDOWN : out   std_logic_vector (1 downto 0); 
             MOTOR_PWM    : out   std_logic; 
             PWM          : in    std_logic);
   end component;
   
   component output_module
      port ( POWER_STATE   : in    power_states; 
             SYSTEM_STATE  : in    system_states; 
             SLOWEST_CLOCK : in    std_logic; 
             OK_LED        : out   std_logic_vector (1 downto 0); 
             PWR_LED       : out   std_logic_vector (1 downto 0); 
             OUTPUT        : out   std_logic_vector (1 downto 0));
   end component;
   
   component PLC_module
      port ( PLC_I     : in    std_logic_vector (1 downto 0); 
             PLC_STATE : out   plc_states);
   end component;
   
   component power_module
      port ( POWER_MODE    : in    std_logic; 
             BATTERY_STATE : in    std_logic; 
             POWER_STATE   : out   power_states);
   end component;
   
   component sensor_module
      Port ( SENSORS : in  STD_LOGIC_VECTOR(3 downto 0)	:= "0000";
           SENSOR_STATE : out  sensor_states := TRANSITION);
   end component;
   
   component system_module
      port ( CLOCK         : in    std_logic; 
             CLOCK_STATE   : in    std_logic; 
             COMMAND_STATE : in    command_states; 
             SENSOR_STATE  : in    sensor_states; 
             SYSTEM_STATE  : out   system_states; 
             MOTOR_STATE   : out   motor_states);
   end component;
   
begin
   WATCHDOG <= SLOW_CLOCK;
   clock_process : clock_module
      port map (CLOCK=>CLOCK,
                CLOCK_STATE=>CLOCK_STATE,
                PWM=>PWM_SIGNAL,
                SLOWEST_CLOCK=>SLOWEST_CLOCK,
                SLOW_CLOCK=>SLOW_CLOCK);
   
   command_process : command_module
      port map (KEY_STATE=>KEY_STATE,
                LOCK_STATE=>LOCK_STATE,
                PLC_STATE=>PLC_STATE,
                COMMAND_STATE=>COMMAND_STATE);
   
   debounce_process : debounce_module
      port map (CLOCK=>SLOWEST_CLOCK,
                CLOCK_STATE=>CLOCK_STATE,
                DATA_I(1 downto 0)=>KEY_I(1 downto 0),
                DATA_O(1 downto 0)=>DATA_O(1 downto 0));
   
   dummy_process : dummy_module
      port map (TBD_O=>TBD_O);
   
   key_process : key_module
      port map (KEY_ENABLE=>KEY_ENABLE,
                KEY_I(1 downto 0)=>DATA_O(1 downto 0),
                KEY_O(1 downto 0)=>KEY_O(1 downto 0),
                KEY_STATE=>KEY_STATE);
   
   lock_process : lock_module
      port map (LOCK_ENABLE=>LOCK_ENABLE,
                LOCK_I(1 downto 0)=>LOCK_I(1 downto 0),
                LOCK_O(1 downto 0)=>LOCK_O(1 downto 0),
                LOCK_STATE=>LOCK_STATE);
   
   movement_process : movement_module
      port map (MOTOR_STATE=>MOTOR_STATE,
                PWM=>PWM_SIGNAL,
                MOTOR_PWM=>MOTOR_PWM,
                MOTOR_UPDOWN(1 downto 0)=>MOTOR(1 downto 0));
   
   output_process : output_module
      port map (POWER_STATE=>POWER_STATE,
                SLOWEST_CLOCK=>SLOWEST_CLOCK,
                SYSTEM_STATE=>SYSTEM_STATE,
                OK_LED(1 downto 0)=>OK_LED(1 downto 0),
                OUTPUT(1 downto 0)=>OUTPUT(1 downto 0),
                PWR_LED(1 downto 0)=>PWR_LED(1 downto 0));
   
   PLC_process : PLC_module
      port map (PLC_I(1 downto 0)=>PLC(1 downto 0),
                PLC_STATE=>PLC_STATE);
   
   power_process : power_module
      port map (BATTERY_STATE=>BATT_STATE,
                POWER_MODE=>POWER_MODE,
                POWER_STATE=>POWER_STATE);
   
   sensor_process : sensor_module
      port map (SENSORS(3 downto 0)=>SENSORS(3 downto 0),
                SENSOR_STATE=>SENSOR_STATE);
   
   system_process : system_module
      port map (CLOCK=>SLOWEST_CLOCK,
                CLOCK_STATE=>CLOCK_STATE,
                COMMAND_STATE=>COMMAND_STATE,
                SENSOR_STATE=>SENSOR_STATE,
                MOTOR_STATE=>MOTOR_STATE,
                SYSTEM_STATE=>SYSTEM_STATE);
   
end BEHAVIORAL;


