---
tag: QGBZ88
kind: algorithm
slug: tree-covering-technology-mapping
name: Tree covering technology mapping
aliases:
- DAGON
- Keutzer tree covering
area: cad/logic-synthesis
level: core
summary: Keutzer's mapper that splits the subject graph into trees and covers each tree optimally by dynamic programming over pattern matches of library gates.
solves: [technology-mapping]
model: word-ram
complexity:
  vars: {N: the number of nodes of the subject graph, L: the number of library patterns, s: the largest number of nodes in a pattern}
  time: {worst: O(N L s 2^s)}
  space: {extra: O(N)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1987
  people: [Kurt Keutzer]
  note: Keutzer's DAGON took tree pattern matching and dynamic programming from code generation and applied them to technology mapping, after it cut the subject graph into trees.
prereqs: [technology-mapping, tree-dynamic-programming, tree-pattern-matching]
see_also: [boolean-matching, lut-mapping, instruction-selection-problem, burs, maximal-munch, dag-dynamic-programming, gate-sizing, boolean-network]
sources:
  - paper: doi:10.1145/37888.37940
    title: "DAGON: technology binding and local optimization by DAG matching"
    locator: Proceedings of the 24th ACM/IEEE Design Automation Conference (1987), pages 341 to 347; the partition into trees, the tree matching and the dynamic programming
  - book: isbn:9780070163331
    title: Synthesis and Optimization of Digital Circuits
    locator: chapter 10, library binding, tree covering (general locator, not checked)
---

Tree covering technology mapping maps a circuit into the gates of a cell library. The circuit is first written as a subject graph of base gates, for example 2-input NAND gates and inverters, and each library gate is written as one or more pattern trees over the same base gates. The subject graph is cut into trees at every node with more than one fanout. In each tree, a dynamic program from the leaves to the root finds, for every node, the cheapest way to cover the subtree below it with pattern matches, and the cover of the tree root gives the cover of the tree. Keutzer described this method in 1987 in his mapper DAGON, using the tree matching and dynamic programming of code generators. The cover of each tree is optimal for the given subject graph and library. The cover of the whole circuit is optimal only among the covers that respect the cut into trees, and a cover that duplicates logic across a cut can be cheaper.

## In plain words

A cell library offers gates such as NAND, NOR, AND-OR-INVERT and inverters, each with a size. The job is to rebuild a circuit from these gates with the smallest total size.

Write the circuit and every library gate in the same small parts, say 2-input NANDs and inverters. A library gate then looks like a small tree of parts. Covering the circuit means placing these trees over it so that every part is covered once.

Where a wire splits to several places, cut the circuit, so it falls into trees. In a tree, work from the inputs up. At each part, try every library gate that fits there, add the best known cost of whatever is under its inputs, and keep the cheapest. The answer at the top of a tree is its best cover.

## The problem

The input is a subject graph and a library. The subject graph is a directed acyclic graph of primary inputs, inverters and 2-input NAND gates, with a set of outputs. A library gate has an area and a pattern, a tree whose inner nodes are NAND and INV and whose leaves are the inputs of the gate. A pattern matches at node $v$ if the subject graph below $v$ has the same shape, with the two inputs of a NAND taken in either order. The match covers the nodes that the inner nodes of the pattern land on, and its inputs are the nodes that the leaves land on.

A cover is a set of matches such that every output gate is the root of a match and every input of a match is a primary input or the root of a match. The goal of this page is the least total area. This is one form of [technology mapping](/technology-mapping/). The cut into trees adds a rule. Let $R$ be the set of gates that drive an output or have more than one fanout, counted only among the gates that reach an output. The tree of $r \in R$ is $r$ with the gates that reach $r$ through gates outside $R$. A tree cover is a cover whose matches cover only nodes of one tree, so that no match covers a node of $R$ except at its root.

## The algorithm

```pseudo id=main
TREE-COVER(G, library)
L1  R ← the gates of G with more than one fanout, and the output gates, among the gates that reach an output
L2  for each gate v of G in topological order do
L3      cost(v) ← ∞
L4      for each library gate g and each match of g at v whose covered nodes other than v are gates outside R do
L5          c ← area(g) + the sum of leafcost(u) over the inputs u of the match
L6          if c < cost(v) then cost(v) ← c; choice(v) ← (g, the inputs of the match)
L7  leafcost(u) is 0 if u is a primary input or in R, and cost(u) otherwise
L8  cover ← ∅; todo ← the output gates
L9  while todo is not empty do
L10     take v from todo; if v is not in cover then add (v, choice(v)) to cover and add the gates among the inputs of choice(v) to todo
L11 return cover and the sum of the areas of its gates
```

Line L4 is [tree pattern matching](/tree-pattern-matching/): the pattern is walked down from $v$, and at each NAND both orders of the inputs are tried. Lines L5 and L6 are the [dynamic program on a tree](/tree-dynamic-programming/): the cost of a node is the area of its best match plus the costs of the subtrees under the inputs of that match. At an input that is a primary input or the root of another tree, the cost is 0 here, because that tree is paid for once at its own root. Lines L8 to L10 read the cover back from the outputs. The total equals the sum of $\mathrm{cost}(r)$ over $r \in R$.

## Example

The toy library of this page has these gates and areas, made up for the examples: INV 2, NAND2 3, NOR2 3, AND2 4, OR2 4, NAND3 4, AOI21 4, OAI21 4, NAND4 5 and AOI22 5. AND2 is the pattern INV(NAND($x$, $x$)), AOI21 is INV(NAND(NAND($x$, $x$), INV($x$))) and AOI22 is INV(NAND(NAND($x$, $x$), NAND($x$, $x$))).

Take $o = \overline{ab + cd}$, written as $n_4 = \mathrm{NAND}(a, b)$, $n_5 = \mathrm{NAND}(c, d)$, $n_6 = \mathrm{NAND}(n_4, n_5)$ and $o = \mathrm{INV}(n_6)$. No node has more than one fanout, so the whole graph is one tree with root $o$.

| node | matches tried | best cost |
|---|---|---|
| $n_4$ | NAND2 over $a, b$: 3 | 3 |
| $n_5$ | NAND2 over $c, d$: 3 | 3 |
| $n_6$ | NAND2 over $n_4, n_5$: $3 + 3 + 3 = 9$ | 9 |
| $o$ | AOI22 over $a, b, c, d$: 5; AND2 over $n_4, n_5$: $4 + 3 + 3 = 10$; INV over $n_6$: $2 + 9 = 11$ | 5 |

The cover is one AOI22 of area 5. Without AOI22 and NAND4 in the library, the best cover is AND2 over two NAND2 gates, with area 10.

Now take $n = \mathrm{NAND}(a, b)$ with two fanouts, $o_1 = \mathrm{INV}(n) = ab$ and $o_2 = \mathrm{INV}(\mathrm{NAND}(n, \mathrm{INV}(c))) = \overline{ab + c}$. The node $n$ is in $R$, so there are three trees, with roots $n$, $o_1$ and $o_2$. The tree of $n$ costs 3 for a NAND2. The tree of $o_1$ costs 2 for an INV over $n$. In the tree of $o_2$, AOI21 does not fit, because it would cover $n$, so the best is AND2 over $n$ and $\mathrm{INV}(c)$, with $4 + 2 = 6$. The tree cover has area $3 + 2 + 6 = 11$. A cover that duplicates $n$, with AND2 over $a, b$ for $o_1$ and AOI21 over $a, b, c$ for $o_2$, has area 8, so the tree cover is not optimal for the whole graph.

## Correctness

The [full proof](proofs/correctness.md) shows that the trees split the gates that reach an output, that each tree is a rooted tree with fanout 1 inside, and that $\mathrm{cost}(v)$ is the least area of a cover of the subtree below $v$, by induction over the tree, since the subtrees under the inputs of a match are disjoint. The cost of a tree cover is the sum of independent tree costs, so the result is a least area tree cover. Every match computes its node from its inputs, so the cover computes the outputs.

## Complexity

At each of the $N$ nodes, line L4 tries the $L$ patterns. A pattern with $s$ nodes has at most $s/2$ NAND nodes, so at most $2^{s/2}$ orders of inputs, and each order is checked in $O(s)$, which gives $O(N L s 2^s)$ in all, a loose bound. For a fixed library this is linear in the size of the subject graph. The tables cost and choice take $O(N)$ space. Lines L8 to L11 take $O(N)$ time. Real mappers prepare the library patterns once, often as an automaton for tree matching, so that matching at a node costs less.

## Properties

**What is proved.** The result is a valid cover: every output and every input of a match is driven, and the mapped circuit computes the same outputs. Its area is the least among all tree covers of the given subject graph with the given patterns. Each tree is covered without duplicating logic, since inside a tree every gate has one fanout.

**What is not proved.** The result is not the least area cover of the subject graph, as the second example shows. Finding that cover for a general DAG is stated to be NP-hard in the mapping literature, and this page does not prove it. The result also depends on the subject graph: another decomposition of the same function into NAND and INV can lead to a smaller cover, and the algorithm does not search over decompositions. Area is the only cost here, and the optimality says nothing about delay.

**What is measured.** Nothing beyond the examples. The tests of this page compare the dynamic program with an exhaustive search over tree covers on 300 random subject graphs (seed 21), and check that an exhaustive search over all covers of the graph, with duplication, never costs more than the tree cover and costs less on some graphs (seed 22).

## Variants and improvements

- **Delay.** With a delay for each gate that does not depend on its load, the same dynamic program can minimize the arrival time at each node, keeping the best match for each node by arrival time. The mapper of MIS has such a delay mode.
- **Inverter pairs.** Adding a pair of inverters on every wire of the subject graph lets patterns match with either polarity, and the dynamic program removes the pairs it does not need.
- **Several patterns per gate.** A gate such as NAND4 has several decompositions into 2-input NANDs. Listing each as a pattern lets the gate match more subject graphs.
- **Covering across cuts.** Mappers can let a match cover a node with more than one fanout and pay for a copy of its logic, which can find the cheaper cover of the second example at the cost of losing the exact tree result.
- **Boolean matching.** Instead of matching the shape of a pattern, match the function of a cut with [Boolean matching](/boolean-matching/). This finds matches that structural matching misses, and it is the basis of cut-based cell mappers.

## When to use it

Use tree covering for standard cell mapping when a fast mapper with a clear optimality guarantee per tree is enough, and when the subject graph is already well structured, for example after AIG optimization. When duplication across fanout points or matches that do not depend on the structure matter, use a cut-based mapper with Boolean matching. For FPGAs, use [LUT mapping](/lut-mapping/) instead.

## Pitfalls

- **Dead logic in the tree roots.** Count fanouts only among the gates that reach an output. A dead gate that reads a node can make it a tree root for no reason and change the cover.
- **One order of NAND inputs.** Matching only the order of the pattern misses matches. Try both orders at each NAND of the pattern.
- **A library that cannot cover a node.** The library must at least contain INV and NAND2 with their plain patterns, or some node can have no match.
- **Leaf costs of tree roots.** A tree root costs 0 as the input of another tree. If its cost is added in each tree that reads it, its area is paid many times.
- **Reading optimality too widely.** The result is optimal per tree for this subject graph, not for the circuit.

## Implementations

## History

Code generators of the 1970s and 1980s already selected machine instructions for expression trees by tree pattern matching and dynamic programming, after Aho and Johnson (1976). In 1987 Keutzer presented DAGON at the Design Automation Conference. It wrote the circuit and the library in the same base gates, cut the circuit into trees, and covered each tree with the methods of code generation, so that the cover of each tree is optimal. In the same year, Detjens, Gannot, Rudell, Sangiovanni-Vincentelli and Wang described the mapper of MIS, which used the same idea with inverter pairs and later with delay costs. Tree covering stayed the standard way to map into cell libraries for many years, and the cut-based mappers that came later still use its dynamic program.

## References
