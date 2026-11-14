---
tag: B4M940
kind: algorithm
slug: cut-enumeration
name: Cut enumeration
aliases:
- k-feasible cut enumeration
area: cad/logic-synthesis
level: core
summary: Computes all k-feasible cuts of every node in topological order by merging the cuts of its fanins and dropping those with more than k leaves.
solves: [lut-mapping]
model: word-ram
complexity:
  vars: {N: the number of nodes, d: the largest number of fanins of a node, C: the largest number of cuts of one node, k: the largest number of leaves of a cut}
  time: {worst: O(N k C^(2d))}
  space: {extra: O(N k C)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1998
  people: [Peichen Pan, Chih-Chang Lin, Jason Cong, Chang Wu, Yuzheng Ding]
  note: Pan and Lin (1998) and Cong, Wu and Ding (1999) computed the K-feasible cuts of every node of a network bottom up by combining the cuts of its fanins, for LUT mapping.
prereqs: [k-feasible-cut, topological-sort]
see_also: [priority-cuts, flowmap, lut-mapping, aig-rewriting, and-inverter-graph, technology-mapping, tree-dynamic-programming]
sources:
  - paper: doi:10.1145/275107.275118
    title: Peichen Pan and Chih-Chang Lin, A new retiming-based technology mapping algorithm for LUT-based FPGAs, Proceedings of the 1998 ACM/SIGDA Sixth International Symposium on Field Programmable Gate Arrays (FPGA 98), pages 35 to 42
    locator: the computation of the K-feasible cuts of each node from the cuts of its fanins (general locator, not checked against the paper)
  - paper: "Jason Cong, Chang Wu and Yuzheng Ding, Cut ranking and pruning, enabling a general and efficient FPGA mapping solution, Proceedings of the 1999 ACM/SIGDA Seventh International Symposium on Field Programmable Gate Arrays (FPGA 99), pages 29 to 35"
    title: Cut ranking and pruning, enabling a general and efficient FPGA mapping solution
    locator: the enumeration of all K-feasible cuts by merging fanin cuts, and the ranking and pruning of cuts (general locator, not checked against the paper)
  - paper: "Alan Mishchenko, Sungmin Cho, Satrajit Chatterjee and Robert Brayton, Combinational and sequential mapping with priority cuts, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD 2007), pages 354 to 361"
    title: Combinational and sequential mapping with priority cuts
    locator: the discussion of exhaustive cut enumeration and its cost, which priority cuts avoid (general locator)
---

Cut enumeration lists, for every node of a [Boolean network](/boolean-network/) or an [and-inverter graph](/and-inverter-graph/), all its [$k$-feasible cuts](/k-feasible-cut/): the sets of at most $k$ nodes that every path from the primary inputs to the node passes through. It visits the nodes in [topological order](/topological-sort/). The cuts of a gate are the trivial cut and the unions of one cut of each fanin, kept when they have at most $k$ leaves. Unions that contain another union are dropped, and then the result is exactly the set of minimal $k$-feasible cuts. The cuts are the input of [LUT mapping](/lut-mapping/), where each cut is a possible lookup table, and of local rewriting such as [AIG rewriting](/aig-rewriting/). Pan and Lin (1998) and Cong, Wu and Ding (1999) used this bottom-up computation in FPGA mappers. For large $k$ the number of cuts grows fast, and [priority cuts](/priority-cuts/) keep only a few of them.

## In plain words

Each gate in a circuit gets its value from the gates below it. Pick a small group of wires below a gate such that every route from the circuit inputs to the gate passes through the group. Then the group alone decides the gate's value. Such a group is a cut.

Find the cuts from the inputs upward. An input has one cut, itself. For a gate, take one cut from each of the gates that feed it and join them. If the joined group is small enough, it is a cut of the gate. The gate itself is also a cut. Try every way to pick and join, and throw away a group that holds a smaller group from the same list, because it has a wire it does not need.

## The problem

The input is a directed acyclic graph with $N$ nodes in topological order, whose sources are the primary inputs (PIs), and an integer $k \ge 1$. The output is, for each node $v$, the set $\Phi(v)$ of all minimal $k$-feasible cuts of $v$, the trivial cut $\{v\}$ included. A cut is minimal when no proper subset of it is a cut of $v$. Non-minimal cuts are of no use to a mapper, because a lookup table over a minimal subset computes the same function with fewer inputs.

## The algorithm

```pseudo id=main
CUTS(G, k)
L1  for each node v of G in topological order do
L2      if v is a primary input then
L3          Φ(v) ← { {v} }
L4      else
L5          A ← { ∅ }
L6          for each fanin u of v do
L7              A ← { a ∪ c : a ∈ A, c ∈ Φ(u), |a ∪ c| ≤ k }
L8          A ← the sets of A that contain no other set of A
L9          Φ(v) ← { {v} } ∪ A
L10 return Φ
```

Line L7 merges the partial unions with each cut of the next fanin. Each $\Phi(u)$ holds the trivial cut $\{u\}$, so $v$ can take a fanin itself as a leaf. Line L8 removes the dominated sets. The code of this page sorts $A$ by size and keeps a set only when no kept set is a subset of it.

## Example

Take $k = 3$ and the network with inputs $a, b, c, d$ and the gates $e = (a, b)$, $f = (b, c)$, $g = (e, f)$, $h = (f, d)$ and $o = (g, h)$. Node $f$ feeds both $g$ and $h$, so the network is not a tree.

| node | fanins | unions at line L7 with at most 3 leaves | $\Phi$ |
|---|---|---|---|
| $e$ | $a, b$ | $\{a, b\}$ | $\{e\}, \{a, b\}$ |
| $f$ | $b, c$ | $\{b, c\}$ | $\{f\}, \{b, c\}$ |
| $g$ | $e, f$ | $\{e, f\}, \{b, c, e\}, \{a, b, f\}, \{a, b, c\}$ | $\{g\}$ and the four unions |
| $h$ | $f, d$ | $\{d, f\}, \{b, c, d\}$ | $\{h\}, \{d, f\}, \{b, c, d\}$ |
| $o$ | $g, h$ | $\{g, h\}, \{d, f, g\}, \{e, f, h\}, \{d, e, f\}$ | $\{o\}$ and the four unions |

At $o$, the 5 cuts of $g$ and the 3 cuts of $h$ give 15 unions. Eleven have 4 or 5 leaves and fail the test at line L7, for example $\{a, b, c\} \cup \{h\}$. None of the four that remain contains another, so line L8 keeps all of them. With $k = 4$ the same pass gives 12 cuts for $o$ and 28 cuts in all.

Line L8 matters in the network with inputs $x, y$ and the gates $a = (x, y)$, $b = (x, a)$ and $v = (a, b)$. The cuts of $b$ are $\{b\}, \{a, x\}$ and $\{x, y\}$, since $\{x\} \cup \{x, y\} = \{x, y\}$. At $v$, line L7 makes $\{a, b\}, \{a, x\}, \{a, x, y\}, \{b, x, y\}$ and $\{x, y\}$. The set $\{a, x, y\}$ holds $\{a, x\}$, and $\{b, x, y\}$ holds $\{x, y\}$, so line L8 drops both, and $\Phi(v) = \{\{v\}, \{a, b\}, \{a, x\}, \{x, y\}\}$.

## Correctness

The [full proof](proofs/correctness.md) shows by induction on the topological order that $\Phi(v)$ is exactly the set of minimal $k$-feasible cuts of $v$. Every set made at line L7 is a union of cuts of the fanins, so it is a cut of $v$, and it has at most $k$ leaves. If a set $C$ that line L8 keeps had a smaller cut $C'$ of $v$ inside it, then the minimal cuts of the fanins inside $C'$ would have a union in $A$ that is a proper subset of $C$, and line L8 would have dropped $C$. In the other direction, a minimal cut $C \ne \{v\}$ of $v$ cuts each fanin $u$. A minimal cut of $u$ inside $C$ is in $\Phi(u)$ by induction, and the union of these cuts is a cut of $v$ inside $C$, so it is $C$ itself. Every partial union is a subset of $C$, so line L7 keeps it.

## Complexity

Let $C$ be the largest size of a set $\Phi(u)$ and $d$ the largest fanin count. At a node, $A$ has at most $C^{j}$ sets after the $j$-th fanin, so line L7 makes at most $C^d$ unions over the last fanin and $O(C^d)$ over all fanins, each in $O(k)$ time on sorted lists of leaves. Line L8 compares pairs of sets of $A$, $O(k C^{2d})$ time. Over $N$ nodes this is $O(N k C^{2d})$, and the cuts take $O(N k C)$ space. For an AIG, $d = 2$.

$C$ itself depends on the network. It is at most $\sum_{i \le k} \binom{N}{i}$, which is polynomial in $N$ for a fixed $k$, but large. The root of a complete binary tree of depth 4 has 9 minimal 4-feasible cuts and 49 minimal 6-feasible cuts, and the counts grow quickly with the depth and the amount of reconvergence. Mishchenko, Cho, Chatterjee and Brayton (2007) give the cost of full enumeration of 6-input cuts on large circuits as the reason for [priority cuts](/priority-cuts/). Implementations such as ABC keep a bit signature of the leaves of each cut, so that most subset tests at line L8 take one machine operation.

## Properties

**What is proved.** For each node, the output is exactly the set of minimal $k$-feasible cuts, in finite time, and the result does not depend on the order of the fanins. Without line L8, every output set is still a $k$-feasible cut, but some are not minimal, as the example shows. A node is a function of each of its cuts, so each cut has a truth table, which the code of this page computes by simulation of the cone.

**What is measured.** The test file compares the output with a brute force over all subsets of at most $k$ nodes of the cone of each node, on 150 random networks with up to 4 inputs and 7 gates and with $k$ from 1 to 4 (seed 7). These are checks of the code, not benchmark results.

## Variants and improvements

- **Cut ranking and pruning.** Cong, Wu and Ding (1999) rank the cuts of a node by a cost, such as depth or area, and keep only part of them, so that a mapper can handle large $k$.
- **[Priority cuts](/priority-cuts/).** Keep at most a fixed number $C$ of cuts per node, chosen by the cost of the current mapping pass, and merge only those. The set is then no longer complete.
- **Truth tables with the cuts.** Compute the truth table of each cut at line L7 from the tables of the two merged cuts, after moving their variables to the positions of the union. Rewriting and Boolean matching need these tables.
- **Sequential cuts.** For circuits with registers, a cut may cross register boundaries, so that mapping and [retiming](/retiming/) are done together. Pan and Lin's mapper is of this kind.
- **Cuts for structural choices.** When the network holds several equivalent structures for a node, the cuts of the node are the union of the cuts of all its choices.

## When to use it

Use full enumeration when $k$ is small, about 4 or 5, or when the network is small, and a complete set of cuts is needed, for example for exact rewriting or for a mapper that must see every option. For 6-input LUTs on large circuits, use [priority cuts](/priority-cuts/) instead. For depth alone, [FlowMap](/flowmap/) finds a best cut per node by max-flow without listing cuts.

## Pitfalls

- **Forgetting the trivial cut.** If $\Phi(u)$ does not hold $\{u\}$, a node can never use its fanin as a leaf, and most cuts are lost, including the cut of the two fanins.
- **Keeping dominated cuts.** Without line L8, the list holds cuts with leaves that the function does not need, and the lists grow faster at each level.
- **Pruning too early.** Dropping sets at line L7 before all fanins are merged is safe only for sets that contain a finished cut of $v$. A partial union is not yet a cut of $v$.
- **Shared leaves.** The union of two cuts can be smaller than the sum of their sizes when the fanins share logic. Test the size of the union, not the sum.
- **Blow-up.** The number of cuts can grow very fast with $k$. Put a limit on the cuts per node, or use priority cuts, before running on large designs.

## Implementations

## History

Cong and Ding (1994) defined $K$-feasible cuts for FlowMap, but found one cut per node by max-flow and did not list them. In the late 1990s, mappers began to list all cuts. Pan and Lin (1998) computed the $K$-feasible cuts of each node from the cuts of its fanins in a mapper that also retimes the circuit. Cong, Wu and Ding (1999) studied the enumeration of all cuts, and their ranking and pruning, as a general base for FPGA mapping with several objectives. Mishchenko, Cho, Chatterjee and Brayton (2007) found that full enumeration costs too much for 6-input cuts on large circuits, and kept only a few priority cuts per node. Cut enumeration is also the first step of AIG rewriting in ABC.

## References
