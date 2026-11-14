# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/devgan-noise-metric/. The authors are listed in prov/6FQBVC.jsonl.
"""Devgan's coupled noise metric on an RC tree (Devgan, ICCAD 1997).

The victim net is a tree of n nodes. Node 0 is the driver output and the
others satisfy parent[k] < k. r[0] is the holding resistance of the quiet
driver to ground, and r[k] for k > 0 is the wire resistance from parent[k]
to k. coupling[k] is a list of pairs (cc, a): a coupling capacitance cc from
node k to aggressor a. slope[a] is the largest absolute slew rate |du_a/dt|
of aggressor a.

devgan_noise(...) returns V with V[i] = sum over k of R_ik I_k, where R_ik is
the resistance of the common part of the paths from ground to i and to k,
and I_k = sum of cc * slope[a] over the couplings of node k. Under the model
on the page, |v_i(t)| <= V[i] for all t. Two passes, O(n + couplings) time.
"""


def devgan_noise(parent, r, coupling, slope):
    n = len(parent)
    current = [0] * n
    for k in range(n):  # @line L1
        current[k] = sum((cc * slope[a] for cc, a in coupling[k]), 0)
    for k in range(n - 1, 0, -1):  # @line L2
        current[parent[k]] += current[k]  # @line L3
    noise = [0] * n
    noise[0] = r[0] * current[0]  # @line L4
    for k in range(1, n):  # @line L5
        noise[k] = noise[parent[k]] + r[k] * current[k]  # @line L6
    return noise  # @line L7


def ramp_slopes(swing, rise_times):
    """Slew rates of ramp aggressors: swing / rise time for each aggressor."""
    return [swing / t for t in rise_times]
