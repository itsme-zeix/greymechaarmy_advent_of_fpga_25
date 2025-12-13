module coprocessor #(
    parameter WIDTH_DIN  = 18*8,
    parameter WIDTH_DOUT = 18*8
)(
    input clk, 
    input rst, 

    input [WIDTH_DIN-1:0] din,
    input din_valid,

    output [WIDTH_DIN-1:0] dout,
    output dout_valid, 

    inout [5:0] control
);

    assign dout_valid = 1'b0;
    assign dout = { din[7:0], "asdfghjkl"};

endmodule