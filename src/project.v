/*
 * Copyright (c) 2026 Nick Armstrong
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

// 8-bit counter: async rst_n, sync LOAD, tri-state uio bus.
module tt_um_example (
  input  wire [7:0] ui_in,
  output wire [7:0] uo_out,
  input  wire [7:0] uio_in,
  output wire [7:0] uio_out,
  output wire [7:0] uio_oe,
  input  wire       ena,
  input  wire       clk,
  input  wire       rst_n
);

  wire load = ui_in[0];
  wire oe = ui_in[1];

  reg [7:0] count;

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
      count <= 8'h00;
    else if (load)
      count <= uio_in;
    else
      count <= count + 1'b1;
  end

  assign uio_out = count;
  assign uio_oe = oe ? 8'hFF : 8'h00;

  // disregard unused I/O
  assign uo_out = 8'h00;
  wire _unused = &{ena, ui_in[7:2], 1'b0};

endmodule
