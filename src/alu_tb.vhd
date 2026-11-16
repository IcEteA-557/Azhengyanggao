----------------------------------------------------------------------------------
-- J8 Course - Laboratory 3
-- Testbench for the 3-bit ALU
--
-- Four stimulus segments, 10 ns each.  The operands stay at A = 101 and
-- B = 011 so that the four operations give four different results:
--
--   0 - 10 ns : op = 00  ADD  5 + 3 = 8   -> result 000, carry 1
--  10 - 20 ns : op = 01  AND  5 and 3 = 1 -> result 001, carry 0
--  20 - 30 ns : op = 10  XOR  5 xor 3 = 6 -> result 110, carry 0
--  30 - 40 ns : op = 11  SHR  5 >> 1 = 2  -> result 010, carry 0
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity ALU_tb is
end ALU_tb;

architecture Behavioral of ALU_tb is

    COMPONENT ALU is
        Port ( A          : in  STD_LOGIC_VECTOR (2 downto 0);
               B          : in  STD_LOGIC_VECTOR (2 downto 0);
               op         : in  STD_LOGIC_VECTOR (1 downto 0);
               result     : out STD_LOGIC_VECTOR (2 downto 0);
               carry      : out STD_LOGIC;
               dup_result : out STD_LOGIC_VECTOR (2 downto 0);
               dup_carry  : out STD_LOGIC);
    end COMPONENT;

    SIGNAL A          : STD_LOGIC_VECTOR (2 downto 0) := "101";
    SIGNAL B          : STD_LOGIC_VECTOR (2 downto 0) := "011";
    SIGNAL op         : STD_LOGIC_VECTOR (1 downto 0) := "00";
    SIGNAL result     : STD_LOGIC_VECTOR (2 downto 0);
    SIGNAL carry      : STD_LOGIC;
    SIGNAL dup_result : STD_LOGIC_VECTOR (2 downto 0);
    SIGNAL dup_carry  : STD_LOGIC;

begin
    -- Named port mapping: the order of the ports in the entity does not matter.
    uut: ALU PORT MAP (A          => A,
                       B          => B,
                       op         => op,
                       result     => result,
                       carry      => carry,
                       dup_result => dup_result,
                       dup_carry  => dup_carry);

    siggen: PROCESS
    begin
        -- 5 + 3 = 8 : result 000, carry 1
        op <= "00";
        wait for 10 ns;

        -- 5 AND 3 = 1
        op <= "01";
        wait for 10 ns;

        -- 5 XOR 3 = 6
        op <= "10";
        wait for 10 ns;

        -- 5 >> 1 = 2
        op <= "11";
        wait for 10 ns;

        -- Stop the process; without this wait the process would run forever.
        wait;
    end PROCESS siggen;

end Behavioral;
