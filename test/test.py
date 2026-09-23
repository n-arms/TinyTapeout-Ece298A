# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Timer


@cocotb.test()
async def test_counter(dut):
  cocotb.start_soon(Clock(dut.clk, 10, unit="us").start())
  dut.ena.value = 1
  dut.ui_in.value = 2
  dut.uio_in.value = 0
  dut.rst_n.value = 0
  await Timer(15, unit="us")
  dut.rst_n.value = 1
  await RisingEdge(dut.clk)
  await Timer(1, unit="us")
  assert int(dut.uio_out.value) == 1
  assert int(dut.uo_out.value) == 0

  await ClockCycles(dut.clk, 4)
  await Timer(1, unit="us")
  assert int(dut.uio_out.value) == 5

  dut.rst_n.value = 0
  await Timer(1, unit="us")
  assert int(dut.uio_out.value) == 0
  dut.rst_n.value = 1
  await RisingEdge(dut.clk)
  await Timer(1, unit="us")

  dut.ui_in.value = 1
  dut.uio_in.value = 0xA5
  await Timer(2, unit="us")
  assert int(dut.uio_out.value) == 1
  await RisingEdge(dut.clk)
  await Timer(1, unit="us")
  assert int(dut.uio_out.value) == 0xA5

  dut.ui_in.value = 0
  await Timer(1, unit="us")
  assert int(dut.uio_oe.value) == 0x00
  await ClockCycles(dut.clk, 2)
  await Timer(1, unit="us")
  assert int(dut.uio_out.value) == 0xA7

  dut.ui_in.value = 1
  dut.uio_in.value = 0xFF
  await RisingEdge(dut.clk)
  await Timer(1, unit="us")
  dut.ui_in.value = 2
  await Timer(1, unit="us")
  assert int(dut.uio_oe.value) == 0xFF
  await RisingEdge(dut.clk)
  await Timer(1, unit="us")
  assert int(dut.uio_out.value) == 0
  assert int(dut.uo_out.value) == 0
