# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dsp-unfolding/. The authors are listed in prov/SNB59C.jsonl.

"""Unfolding transformation of a data flow graph (Parhi and Messerschmitt).

A graph has nodes with a kind: "in" (the host, which emits a sample of x
in each iteration), "add" (sum of the inputs) or "mul" (a constant times
the product of the inputs). Arithmetic is modulo MOD, and every node maps
all zero inputs to zero, so delays that start at zero stand for samples
before time 0. Edges are (u, v, w) with w >= 0 delays, and every cycle has
at least one delay. A host node may carry a phase i and a factor J; it then
emits x(J k + i) in iteration k. A plain host has phase 0 and factor 1.
"""

MOD = 1_000_003


def node_value(kind, coef, inputs):
    if kind == "add":
        return sum(inputs) % MOD
    prod = coef
    for a in inputs:
        prod = prod * a % MOD
    return prod


def topo_zero_delay(nodes, edges):
    indeg = {v: 0 for v in nodes}
    for u, v, w in edges:
        if w == 0:
            indeg[v] += 1
    order = [v for v in nodes if indeg[v] == 0]
    for v in order:
        for a, b, w in edges:
            if a == v and w == 0:
                indeg[b] -= 1
                if indeg[b] == 0:
                    order.append(b)
    if len(order) != len(nodes):
        raise ValueError("a cycle with no delay")
    return order


def simulate(graph, x, iterations):
    """Run the graph for the given number of iterations; return all values."""
    nodes, edges, kind, coef = graph["nodes"], graph["edges"], graph["kind"], graph["coef"]
    phase = graph.get("phase", {})
    order = topo_zero_delay(nodes, edges)
    ins_of = {v: [(u, w) for (u, b, w) in edges if b == v] for v in nodes}
    val = {v: [] for v in nodes}
    for k in range(iterations):
        for v in order:
            if kind[v] == "in":
                i, J = phase.get(v, (0, 1))
                n = J * k + i
                val[v].append(x[n] % MOD if n < len(x) else 0)
                continue
            ins = [val[u][k - w] if k - w >= 0 else 0 for (u, w) in ins_of[v]]
            val[v].append(node_value(kind[v], coef.get(v, 1), ins))
    return val


def unfold(graph, J):
    """The J-unfolded graph.

    Node U becomes U_0, ..., U_{J-1}, where U_i in iteration k computes U
    in iteration J k + i. Edge U -> V with w delays becomes, for each i,
    the edge U_i -> V_{(i + w) mod J} with floor((i + w) / J) delays. The
    edges keep the order of the input slots of each node.
    """
    if J < 1:
        raise ValueError("J must be at least 1")
    nodes, edges, kind, coef = graph["nodes"], graph["edges"], graph["kind"], graph["coef"]
    name = lambda v, i: f"{v}_{i}"
    new_nodes = [name(v, i) for v in nodes for i in range(J)]  # @line L1
    # Each edge into V gives exactly one edge into each copy V_j, and the
    # copies list them in the order of the original edges, so the input
    # slots of every node keep their order.
    new_edges = []
    for u, v, w in edges:  # @line L2
        for i in range(J):  # @line L3
            new_edges.append((name(u, i), name(v, (i + w) % J), (i + w) // J))  # @line L4 L5
    new_kind = {name(v, i): kind[v] for v in nodes for i in range(J)}
    new_coef = {name(v, i): coef[v] for v in nodes for i in range(J) if v in coef}
    new_phase = {}
    for v in nodes:  # @line L6
        if kind[v] == "in":
            p, K = graph.get("phase", {}).get(v, (0, 1))
            for i in range(J):
                new_phase[name(v, i)] = (K * i + p, K * J)
    return {"nodes": new_nodes, "edges": new_edges, "kind": new_kind, "coef": new_coef, "phase": new_phase}  # @line L7
