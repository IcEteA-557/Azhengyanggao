## ---------------------------------------------------------------------------
## J8 Course - Laboratory 3
## Basys 3 I/O constraints for the 3-bit ALU
##
## Switches : A on SW0-SW2, B on SW3-SW5, op on SW6-SW7
## LEDs     : result on LD0-LD2, carry on LD3
## PMOD JA  : dup_result on JA1-JA3, dup_carry on JA4
##
## The IOSTANDARD is LVCMOS33 on every pin, as required by the Basys 3.
## ---------------------------------------------------------------------------

set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]

## Operand A ----------------------------------------------------------------
set_property -dict { PACKAGE_PIN V17 IOSTANDARD LVCMOS33 } [get_ports {A[0]}]
set_property -dict { PACKAGE_PIN V16 IOSTANDARD LVCMOS33 } [get_ports {A[1]}]
set_property -dict { PACKAGE_PIN W16 IOSTANDARD LVCMOS33 } [get_ports {A[2]}]

## Operand B ----------------------------------------------------------------
set_property -dict { PACKAGE_PIN W17 IOSTANDARD LVCMOS33 } [get_ports {B[0]}]
set_property -dict { PACKAGE_PIN W15 IOSTANDARD LVCMOS33 } [get_ports {B[1]}]
set_property -dict { PACKAGE_PIN V15 IOSTANDARD LVCMOS33 } [get_ports {B[2]}]

## Operation select ---------------------------------------------------------
set_property -dict { PACKAGE_PIN W14 IOSTANDARD LVCMOS33 } [get_ports {op[0]}]
set_property -dict { PACKAGE_PIN W13 IOSTANDARD LVCMOS33 } [get_ports {op[1]}]

## Result on the LEDs -------------------------------------------------------
set_property -dict { PACKAGE_PIN U16 IOSTANDARD LVCMOS33 } [get_ports {result[0]}]
set_property -dict { PACKAGE_PIN E19 IOSTANDARD LVCMOS33 } [get_ports {result[1]}]
set_property -dict { PACKAGE_PIN U19 IOSTANDARD LVCMOS33 } [get_ports {result[2]}]

## Carry on LD3 -------------------------------------------------------------
set_property -dict { PACKAGE_PIN V19 IOSTANDARD LVCMOS33 } [get_ports {carry}]

## Logic analyser outputs on PMOD JA ---------------------------------------
set_property -dict { PACKAGE_PIN J1 IOSTANDARD LVCMOS33 } [get_ports {dup_result[0]}]
set_property -dict { PACKAGE_PIN L2 IOSTANDARD LVCMOS33 } [get_ports {dup_result[1]}]
set_property -dict { PACKAGE_PIN J2 IOSTANDARD LVCMOS33 } [get_ports {dup_result[2]}]
set_property -dict { PACKAGE_PIN G2 IOSTANDARD LVCMOS33 } [get_ports {dup_carry}]
