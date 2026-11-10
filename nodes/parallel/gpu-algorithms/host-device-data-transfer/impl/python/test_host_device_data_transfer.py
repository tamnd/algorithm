# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/host-device-data-transfer/. The authors are listed in prov/J2CVHF.jsonl.
from fractions import Fraction as F

from host_device_data_transfer import (
    effective_bandwidth, half_bandwidth_size, matmul_transfer_intensity, min_intensity,
    offload_time, pcie_rate, separate_vs_batched, transfer_time,
)

L = F(10, 10 ** 6)          # assumed latency: 10 microseconds
BETA = 25 * 10 ** 9         # assumed bandwidth: 25 GB/s


def test_transfer_times_of_the_example():
    assert transfer_time(L, BETA, 4000) == F(1016, 10 ** 8)            # 10.16 us
    assert transfer_time(L, BETA, 10 ** 6) == F(50, 10 ** 6)           # 50 us
    assert effective_bandwidth(L, BETA, 4000) == F(4000) / F(1016, 10 ** 8)
    assert round(float(effective_bandwidth(L, BETA, 4000)) / 1e9, 3) == 0.394
    assert effective_bandwidth(L, BETA, 10 ** 6) == 20 * 10 ** 9
    assert half_bandwidth_size(L, BETA) == 250000
    assert effective_bandwidth(L, BETA, 250000) == F(BETA, 2)


def test_batching():
    sep, one = separate_vs_batched(L, BETA, 4000, 1000)
    assert sep == F(1016, 10 ** 5)                                     # 10.16 ms
    assert one == F(170, 10 ** 6)                                      # 170 us
    assert sep / one > 59


def test_effective_bandwidth_formula():
    for s in (1, 1000, 10 ** 5, 10 ** 7):
        assert effective_bandwidth(L, BETA, s) == F(BETA) * s / (s + L * BETA)


def test_pcie_rates():
    assert pcie_rate(8, 16) == F(16384, 1040)
    assert round(float(pcie_rate(8, 16)), 2) == 15.75
    assert round(float(pcie_rate(16, 16)), 2) == 31.51
    assert round(float(pcie_rate(32, 16)), 2) == 63.02


def test_work_per_byte_rule():
    gpu = 10 * 10 ** 12                                                # assumed 10 TFLOP/s
    assert min_intensity(gpu, BETA) == 400
    assert matmul_transfer_intensity(2400) == 400
    assert matmul_transfer_intensity(6) == 1
    # vector add: 1 FLOP per 12 bytes over the bus
    n = 10 ** 8
    t = offload_time(n, 12 * n, gpu, BETA)
    assert t == F(12 * n, BETA) + F(n, gpu) == F(4801, 100000)          # 48.01 ms
