----------------------------------------------------------------------------------
-- J8 Course - Laboratory 3
-- Checkpoint 3 extension: an ALU with seven operations
--
-- op = "000" : result = A + B          carry = carry-out of the 4-bit sum
-- op = "001" : result = A - B          carry = 1 when A >= B (no borrow)
-- op = "010" : result = A AND B        carry = 0
-- op = "011" : result = A OR  B        carry = 0
-- op = "100" : result = A XOR B        carry = 0
-- op = "101" : result = A >> 1         carry = 0
-- op = "110" : result = A << 1         carry = 0
-- op = "111" : reserved, result = 000  carry = 0
--
-- The extra op bit is SW8 (pin V2) on the Basys 3.
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity ALU_7ops is
    Port ( A          : in  STD_LOGIC_VECTOR (2 downto 0);
           B          : in  STD_LOGIC_VECTOR (2 downto 0);
           op         : in  STD_LOGIC_VECTOR (2 downto 0);
           result     : out STD_LOGIC_VECTOR (2 downto 0);
           carry      : out STD_LOGIC;
           dup_result : out STD_LOGIC_VECTOR (2 downto 0);
           dup_carry  : out STD_LOGIC);
end ALU_7ops;

architecture Behavioral of ALU_7ops is
    signal result_t : STD_LOGIC_VECTOR (2 downto 0);
    signal carry_t  : STD_LOGIC;
    signal sum      : STD_LOGIC_VECTOR (3 downto 0);
    signal diff     : STD_LOGIC_VECTOR (3 downto 0);
begin
    -- Addition: bit 3 of the 4-bit sum is the carry-out.
    sum <= ('0' & A) + ('0' & B);

    -- Subtraction in two's complement: A + (not B) + 1.
    -- diff(2 downto 0) is the 3-bit difference; diff(3) is its sign bit.
    -- For A >= B the sign bit is 0, so "not diff(3)" is the no-borrow flag.
    diff <= ('0' & A) + (not ('0' & B)) + "0001";

    with op select
        result_t <= sum(2 downto 0)  when "000",
                    diff(2 downto 0) when "001",
                    A and B          when "010",
                    A or  B          when "011",
                    A xor B          when "100",
                    to_stdlogicvector(to_bitvector(A) srl 1) when "101",
                    A(1 downto 0) & '0' when "110",
                    "000"            when others;

    with op select
        carry_t <= sum(3)      when "000",
                   not diff(3) when "001",
                   '0'         when others;

    result     <= result_t;
    carry      <= carry_t;
    dup_result <= result_t;
    dup_carry  <= carry_t;
end Behavioral;
