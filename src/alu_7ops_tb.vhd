----------------------------------------------------------------------------------
-- J8 Course - Laboratory 3
-- Testbench for the seven-operation ALU (Checkpoint 3 extension)
--
-- Each segment uses different operands so that the seven results are all
-- different and easy to identify in the waveform:
--
--   0 - 10 ns : ADD  6 + 3 = 9  -> result 001, carry 1
--  10 - 20 ns : SUB  7 - 2 = 5  -> result 101, carry 1 (no borrow)
--  20 - 30 ns : AND  6 and 5    -> result 100, carry 0
--  30 - 40 ns : OR   5 or  2    -> result 111, carry 0
--  40 - 50 ns : XOR  6 xor 5    -> result 011, carry 0
--  50 - 60 ns : SHR  5 >> 1     -> result 010, carry 0
--  60 - 70 ns : SHL  3 << 1     -> result 110, carry 0
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity ALU_7ops_tb is
end ALU_7ops_tb;

architecture Behavioral of ALU_7ops_tb is

    COMPONENT ALU_7ops is
        Port ( A          : in  STD_LOGIC_VECTOR (2 downto 0);
               B          : in  STD_LOGIC_VECTOR (2 downto 0);
               op         : in  STD_LOGIC_VECTOR (2 downto 0);
               result     : out STD_LOGIC_VECTOR (2 downto 0);
               carry      : out STD_LOGIC;
               dup_result : out STD_LOGIC_VECTOR (2 downto 0);
               dup_carry  : out STD_LOGIC);
    end COMPONENT;

    SIGNAL A          : STD_LOGIC_VECTOR (2 downto 0) := "110";
    SIGNAL B          : STD_LOGIC_VECTOR (2 downto 0) := "011";
    SIGNAL op         : STD_LOGIC_VECTOR (2 downto 0) := "000";
    SIGNAL result     : STD_LOGIC_VECTOR (2 downto 0);
    SIGNAL carry      : STD_LOGIC;
    SIGNAL dup_result : STD_LOGIC_VECTOR (2 downto 0);
    SIGNAL dup_carry  : STD_LOGIC;

begin
    uut: ALU_7ops PORT MAP (A          => A,
                            B          => B,
                            op         => op,
                            result     => result,
                            carry      => carry,
                            dup_result => dup_result,
                            dup_carry  => dup_carry);

    siggen: PROCESS
    begin
        -- ADD  6 + 3 = 9
        A <= "110"; B <= "011"; op <= "000";
        wait for 10 ns;

        -- SUB  7 - 2 = 5
        A <= "111"; B <= "010"; op <= "001";
        wait for 10 ns;

        -- AND  6 and 5
        A <= "110"; B <= "101"; op <= "010";
        wait for 10 ns;

        -- OR   5 or 2
        A <= "101"; B <= "010"; op <= "011";
        wait for 10 ns;

        -- XOR  6 xor 5
        A <= "110"; B <= "101"; op <= "100";
        wait for 10 ns;

        -- SHR  5 >> 1
        A <= "101"; B <= "000"; op <= "101";
        wait for 10 ns;

        -- SHL  3 << 1
        A <= "011"; B <= "000"; op <= "110";
        wait for 10 ns;

        wait;
    end PROCESS siggen;

end Behavioral;
