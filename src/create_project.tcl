# -----------------------------------------------------------------------------
# J8 Course - Laboratory 3
# Create a Vivado project for the 3-bit ALU and add all source files.
#
# Usage (Vivado):
#   Tools > Run Tcl Script... > select this file
#
# The project is created next to this script (lab3/src/lab3_alu).
# -----------------------------------------------------------------------------

set here [file dirname [file normalize [info script]]]

create_project lab3_alu [file join $here lab3_alu] -part xc7a35tcpg236-1 -force

set_property target_language VHDL [current_project]

add_files -norecurse [list \
    [file join $here alu.vhd] \
    [file join $here alu_tb.vhd] \
]

add_files -fileset constrs_1 -norecurse [file join $here alu.xdc]

set_property top ALU [current_fileset]
update_compile_order -fileset sources_1

puts "J8 Lab 3 project created at [file join $here lab3_alu]"
puts "Top module: ALU    Part: xc7a35tcpg236-1"
