----------------------------------------------------------------------------------
-- Verification-only testbench (not shipped in src/).
-- Applies all 256 A/B/op combinations to ALU and prints one line per case:
--   CASE <a> <b> <op> <result> <carry>
-- _src/verify/check.py compares the lines with _src/model.py.
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity alu_exhaustive_tb is
end alu_exhaustive_tb;

architecture Behavioral of alu_exhaustive_tb is
    component ALU is
        Port ( A          : in  STD_LOGIC_VECTOR (2 downto 0);
               B          : in  STD_LOGIC_VECTOR (2 downto 0);
               op         : in  STD_LOGIC_VECTOR (1 downto 0);
               result     : out STD_LOGIC_VECTOR (2 downto 0);
               carry      : out STD_LOGIC;
               dup_result : out STD_LOGIC_VECTOR (2 downto 0);
               dup_carry  : out STD_LOGIC);
    end component;

    signal A          : STD_LOGIC_VECTOR (2 downto 0) := (others => '0');
    signal B          : STD_LOGIC_VECTOR (2 downto 0) := (others => '0');
    signal op         : STD_LOGIC_VECTOR (1 downto 0) := (others => '0');
    signal result     : STD_LOGIC_VECTOR (2 downto 0);
    signal carry      : STD_LOGIC;
    signal dup_result : STD_LOGIC_VECTOR (2 downto 0);
    signal dup_carry  : STD_LOGIC;
begin
    uut: ALU port map (A => A, B => B, op => op,
                       result => result, carry => carry,
                       dup_result => dup_result, dup_carry => dup_carry);

    process
        variable c : integer;
    begin
        for ai in 0 to 7 loop
            for bi in 0 to 7 loop
                for oi in 0 to 3 loop
                    A <= std_logic_vector(to_unsigned(ai, 3));
                    B <= std_logic_vector(to_unsigned(bi, 3));
                    op <= std_logic_vector(to_unsigned(oi, 2));
                    wait for 1 ns;

                    if carry = '1' then
                        c := 1;
                    else
                        c := 0;
                    end if;

                    assert dup_result = result and dup_carry = carry
                        report "duplicate outputs differ from result/carry"
                        severity failure;

                    report "CASE " & integer'image(ai) & " " & integer'image(bi) & " "
                        & integer'image(oi) & " "
                        & integer'image(to_integer(unsigned(result))) & " "
                        & integer'image(c);
                end loop;
            end loop;
        end loop;
        wait;
    end process;
end Behavioral;
