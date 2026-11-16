----------------------------------------------------------------------------------
-- J8 Course - Laboratory 3
-- Simple 3-bit ALU
--
-- op = "00" : result = A + B       carry = carry-out of the 4-bit sum
-- op = "01" : result = A AND B     carry = 0
-- op = "10" : result = A XOR B     carry = 0
-- op = "11" : result = A >> 1      carry = 0  (logical shift, MSB filled with 0)
--
-- dup_result and dup_carry are copies of result and carry.  They drive the
-- PMOD header JA so that a logic analyser can observe the same values that
-- the LEDs show.
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity ALU is
    Port ( A          : in  STD_LOGIC_VECTOR (2 downto 0);
           B          : in  STD_LOGIC_VECTOR (2 downto 0);
           op         : in  STD_LOGIC_VECTOR (1 downto 0);
           result     : out STD_LOGIC_VECTOR (2 downto 0);
           carry      : out STD_LOGIC;
           dup_result : out STD_LOGIC_VECTOR (2 downto 0);
           dup_carry  : out STD_LOGIC);
end ALU;

architecture Behavioral of ALU is
    signal result_t : STD_LOGIC_VECTOR (2 downto 0);
    signal carry_t  : STD_LOGIC;
    signal tmp      : STD_LOGIC_VECTOR (3 downto 0);
begin
    -- 4-bit sum: tmp(3) is the carry-out, tmp(2 downto 0) is the 3-bit result.
    tmp <= ('0' & A) + ('0' & B);

    with op select
        result_t <= tmp(2 downto 0) when "00",
                    A and B        when "01",
                    A xor B        when "10",
                    to_stdlogicvector(to_bitvector(A) srl 1) when others;

    with op select
        carry_t <= tmp(3) when "00",
                   '0'    when others;

    result     <= result_t;
    carry      <= carry_t;
    dup_result <= result_t;
    dup_carry  <= carry_t;
end Behavioral;
