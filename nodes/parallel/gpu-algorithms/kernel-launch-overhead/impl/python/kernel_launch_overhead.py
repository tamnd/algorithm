# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-launch-overhead/. The authors are listed in prov/EGK2KC.jsonl.
"""Cost models of kernel launch overhead, in exact arithmetic.

Times are Fractions in microseconds.  The numbers in the tests are either
taken from a cited measurement (Gray 2019, a V100 with CUDA 10.1) or are
stated assumptions.  No CUDA code is run.
"""
from fractions import Fraction as F


def sequence_time(k, tau, o):
    """k kernels of tau each, each with a fixed overhead o that is not hidden."""
    return k * (F(tau) + F(o))


def efficiency(tau, o):
    """Fraction of the time that the GPU spends in kernel bodies."""
    return F(tau) / (F(tau) + F(o))


def overhead_per_kernel(per_kernel_time, tau):
    """The overhead implied by a measured time per kernel."""
    return F(per_kernel_time) - F(tau)


def async_schedule(k, tau, cpu_issue, gpu_gap, first_latency=0):
    """Start and end times of k kernels launched back to back without a sync.

    The host issues launch i at time i * cpu_issue.  Kernel i starts at
    max(issue_i + first_latency, end_{i-1} + gpu_gap) and runs for tau.
    """
    tau, c, g, d = F(tau), F(cpu_issue), F(gpu_gap), F(first_latency)
    starts, ends = [], []
    prev_end = None
    for i in range(k):
        ready = i * c + d
        s = ready if prev_end is None else max(ready, prev_end + g)
        starts.append(s)
        prev_end = s + tau
        ends.append(prev_end)
    return starts, ends


def steady_per_kernel(tau, cpu_issue, gpu_gap):
    """Time per kernel in a long asynchronous sequence: the slower of host and device."""
    return max(F(cpu_issue), F(tau) + F(gpu_gap))


def graph_break_even(instantiate, kernels, saving_per_kernel):
    """Smallest number of graph launches whose savings pay for the instantiation."""
    per_launch = kernels * F(saving_per_kernel)
    q = F(instantiate) / per_launch
    return -(-q.numerator // q.denominator), q


def min_useful_elements(o, bytes_per_element, bandwidth_bytes_per_us):
    """Elements for which a memory-bound kernel body takes as long as the overhead o."""
    return F(o) * F(bandwidth_bytes_per_us) / bytes_per_element
