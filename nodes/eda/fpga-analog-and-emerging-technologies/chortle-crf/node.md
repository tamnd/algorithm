---
tag: H1WBNA
kind: algorithm
slug: chortle-crf
name: Chortle-crf
aliases: []
area: eda/fpga-analog-and-emerging-technologies
level: advanced
summary: Francis, Rose and Vranesic's LUT mapper that decomposes each tree of the network by bin packing of fanins and maps it by dynamic programming for the fewest LUTs.
solves: [lut-mapping]
model: word-ram
complexity:
  vars: {n: the number of gates, m: the number of gate inputs, d: the largest fanin of a gate, K: the number of LUT inputs}
  time: {this implementation: O(m d), with heaps: O(m log m)}
  space: {total: O(n + m)}
properties: {deterministic: true, recursive: true, exact: false}
history:
  year: 1991
  people: [Robert J. Francis, Jonathan Rose, Zvonko Vranesic]
  note: Chortle-crf replaced the exhaustive search over gate decompositions of the 1990 Chortle mapper with first-fit decreasing bin packing, and added the use of reconvergent fanout and logic replication at fanout nodes.
prereqs: [lut-mapping, bin-packing, first-fit-decreasing, tree-dynamic-programming]
see_also: [flowmap, cutmap, daomap, cut-enumeration, priority-cuts, tree-covering-technology-mapping, bin-packing-np-hardness, fpga-packing]
sources:
  - paper: doi:10.1145/127601.127670
    title: "Robert J. Francis, Jonathan Rose and Zvonko Vranesic, Chortle-crf, fast technology mapping for lookup table-based FPGAs, Proceedings of the 28th ACM/IEEE Design Automation Conference (DAC 1991), San Francisco, pages 227 to 233"
    locator: the decomposition of a node by first-fit decreasing bin packing of the fanin LUTs, the dynamic program over each fanout-free tree, the claim that the result is optimal for a tree when K is at most 5, and the handling of reconvergent fanout and replication
  - paper: doi:10.1145/233539.233540
    title: "Jason Cong and Yuzheng Ding, Combinational logic synthesis for LUT based field programmable gate arrays, ACM Transactions on Design Automation of Electronic Systems 1(2), 145 to 204, 1996"
    locator: Section 3.1.3 (the two conditions on the decomposition of a node, the bin packing and closing steps, the statement that first-fit decreasing is optimal for the restricted bin packing problem when K is at most 5, and the O(m log m) bound)
  - paper: "Alberto Sangiovanni-Vincentelli, Abbas El Gamal and Jonathan Rose, Synthesis methods for field programmable gate arrays, Proceedings of the IEEE 81(7), 1057 to 1083, 1993"
    title: Synthesis methods for field programmable gate arrays
    locator: the section on Chortle and Chortle-crf (the bin packing of cubes, the claim of a minimum for disjoint-support cubes, the speed against Chortle)
  - paper: "Robert J. Francis, Jonathan Rose and Kevin Chung, Chortle, a technology mapping program for lookup table-based field programmable gate arrays, Proceedings of the 27th ACM/IEEE Design Automation Conference (DAC 1990), pages 613 to 619"
    title: Chortle, a technology mapping program for lookup table-based field programmable gate arrays
    locator: the forest of trees and the exhaustive search over decompositions that Chortle-crf replaces (general locator)
  - paper: "Robert J. Francis, Jonathan Rose and Zvonko Vranesic, Technology mapping of lookup table-based FPGAs for performance, Proceedings of the IEEE International Conference on Computer-Aided Design (ICCAD 1991), pages 568 to 571"
    title: Technology mapping of lookup table-based FPGAs for performance
    locator: Chortle-d, the depth version of the same decomposition (general locator)
---

Chortle-crf is an algorithm for [LUT mapping](/lut-mapping/), a step of FPGA CAD: it turns a network of AND, OR and similar gates into a network of $K$-input lookup tables (LUTs) and tries to use as few LUTs as possible. It cuts the network into fanout-free trees and maps each tree bottom up. At each gate it packs the LUTs that come from the fanins into LUTs of size $K$ with the [first-fit decreasing](/first-fit-decreasing/) rule for [bin packing](/bin-packing/), and then joins the packed LUTs into one root LUT. Francis, Rose and Vranesic gave it at DAC 1991. For a tree, they state that the result has the fewest LUTs when $K \le 5$.

## In plain words

A lookup table with $K$ inputs can compute any function of $K$ signals. An FPGA builds a circuit from many such tables, so the mapper cuts the logic into pieces of at most $K$ inputs, and fewer pieces means a smaller circuit.

Chortle-crf works on trees of gates, from the inputs up. When it reaches a gate, the subtrees below it are already in tables, and each subtree has one top table that is still open. Chortle-crf treats each top table and each plain input as a box whose size is the number of inputs it uses. It puts the boxes into bins of capacity $K$, the largest box first, and each bin becomes one table. Then it chains the bins together until one bin is left at the top. That bin is the open table of the gate, and the next gate up continues from it.

## The problem

**Input.** A [Boolean network](/boolean-network/) of gates, each with an operator that is associative and commutative (AND, OR or XOR; inverters on the edges can go into the LUTs), and an integer $K \ge 2$.

**Output.** A network of $K$-input LUTs that computes the same outputs. Each LUT has at most $K$ distinct inputs and computes any function of them.

**Goal.** Few LUTs. For a fanout-free tree, the search space of Chortle-crf is every way to split each gate into a tree of smaller gates with the same operator, together with every cover of the result by LUTs that are subtrees. Chortle-crf is exact in this space for trees when $K \le 5$, as stated in the next sections. On a network with fanout it is a heuristic, because cutting the network into trees already fixes a part of the answer.

## The algorithm

The network is first cut into fanout-free trees: every gate that drives an output or more than one gate input is the root of a tree, and its output is a plain input of the trees that read it. Each tree is then mapped by the procedure below, called on its root. A *wire* is an item of size 1: a primary input, a tree root, or the output of a LUT that is already closed. An *open LUT* is the root LUT of a child, with size equal to the number of its inputs; it is not yet a separate LUT, because the parent may still merge it into a larger one.

```pseudo id=main
MAP-GATE(v, K)
L1  items ← empty list
L2  for each fanin f of v:
L3      if f is a gate inside this tree then append MAP-GATE(f, K) to items   ▷ an open LUT
L4      else append the wire f to items
L5  sort items by size, largest first
L6  for each item x in this order: put x into the first bin with room for x, or into a new bin
L7  while there is more than one bin:
L8      remove the fullest bin B and close it: B becomes a LUT that computes op(v) of its items
L9      put the output wire of B into the fullest bin that has room for 1, or into a new bin
L10 return the last bin as the open LUT of v, of size equal to its content
```

The LUT of the tree root is the last bin returned for the root. Ties are broken by the order in which the bins were opened. Each gate keeps only one solution, the one that this procedure builds.

The decision at each gate follows the rule that Cong and Ding state for Chortle-crf in their survey: decompose the gate so that (1) the number of LUTs in its subtree is least, and (2) under (1), the open root LUT is as small as possible. The second condition matters because a small open LUT leaves more room in the bins of the parent.

## Example

Take $K = 4$ and the tree $f = \mathrm{OR}(x, y, g, h)$ with $x = \mathrm{AND}(a, b, c)$ and $y = \mathrm{AND}(d, e)$. The trace below is the output of the implementation.

| step | content |
|---|---|
| gate $x$ | three wires $a, b, c$ go into one bin; $x$ returns an open LUT of size 3 |
| gate $y$ | two wires go into one bin; $y$ returns an open LUT of size 2 |
| gate $f$, line L5 | items: $x$ (3), $y$ (2), $g$ (1), $h$ (1) |
| line L6 | $x$ opens bin A (3); $y$ does not fit in A and opens bin B (2); $g$ goes to A (4); $h$ goes to B (3) |
| line L8 | A is the fullest, so it closes as LUT $\ell_1 = \mathrm{OR}(\mathrm{AND}(a, b, c), g)$ with 4 inputs |
| line L9 | the wire $\ell_1$ goes to B, which now has 4 |
| line L10 | B is the root LUT $f = \mathrm{OR}(\mathrm{AND}(d, e), h, \ell_1)$ with inputs $d, e, h, \ell_1$ |

The result has 2 LUTs. No mapping can use 1, because the tree has 7 distinct inputs and one LUT has 4. In general, a tree of $L$ LUTs of size $K$ has at most $LK - (L - 1)$ free inputs, because $L - 1$ inputs carry outputs of other LUTs; with 7 inputs and $K = 4$ this gives $L \ge 2$.

The fullest bin closes first because its output then costs only one slot in a bin that still has room. If bin B closed first here, its wire would not fit in the full bin A, and a third LUT would be needed.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows three things. Every LUT has at most $K$ inputs, because a bin never holds items whose sizes add up to more than $K$, and the size of an item bounds its distinct inputs. The LUT network computes the same function, because each bin computes the operator of the gate over its items, and an associative and commutative operator can be split over the bins in any grouping. The loop at line L7 stops after at most twice the number of bins, because a step at line L9 that opens a new bin is always followed by a step that does not.

The claim that the LUT count is least for a tree when $K \le 5$ is not proved here. It rests on two results of Francis, Rose and Vranesic: that the two conditions above, applied at every gate, give a mapping of the tree with the fewest LUTs, and that first-fit decreasing is optimal for the restricted bin packing problem at a gate when $K \le 5$. The proof file states both precisely and gives the sources.

## Complexity

Let $d_v$ be the fanin of gate $v$ and $m = \sum_v d_v$. At $v$ the sort costs $O(d_v \log d_v)$, the first-fit pass $O(d_v b_v)$ with $b_v \le d_v$ bins, and the closing loop $O(b_v)$ steps of $O(b_v)$ each. This implementation therefore runs in $O(\sum_v d_v^2) = O(m d)$ time, where $d$ is the largest fanin. With the bins kept in a heap keyed by content, each first-fit step and each closing step costs $O(\log d_v)$, which gives the $O(m \log m)$ bound that Cong and Ding state. Space is $O(n + m)$ for the network and the LUTs. The number of LUTs is at most $m$, since every closed LUT holds at least one item.

## Properties

**What is proved.** The output is a valid LUT network: each LUT has at most $K$ inputs and the outputs are unchanged (proof file). The method is deterministic and runs in polynomial time.

**What is cited.** For a fanout-free tree and $K \le 5$, the number of LUTs is the least over all decompositions of the gates and all covers by LUTs (Francis, Rose and Vranesic 1991, as stated by Cong and Ding 1996, Section 3.1.3). The survey of Sangiovanni-Vincentelli, El Gamal and Rose (1993) states the bound as $k \le 6$ for disjoint-support cubes; the two surveys disagree, and this page follows the more conservative $K \le 5$.

**What is measured.** The tests compare the LUT count with an exhaustive search over every split of every gate and every cover, on random trees of up to 5 gates with fanin up to 4. The counts are equal for every tree tried with $K = 2, 3, 4, 5$. For $K = 6$ and $K = 7$ the tests check only that the count is never below the optimum. A separate search over single gates with up to 6 child LUTs of every size found no tree where Chortle-crf is worse for $K$ from 3 to 8; this does not prove optimality for larger $K$, it only says that small cases do not show a gap.

**Not optimal on networks with fanout.** Cutting at fanout nodes means that a gate with two readers always ends a LUT. A mapper that duplicates that gate into both readers can use fewer LUTs, which is what the replication step of the paper and the cut-based mappers do.

## Variants and improvements

- **Reconvergent fanout.** When two fanins of a gate share inputs, putting them into the same bin needs fewer pins than their sizes add up to. Chortle-crf tries the pairings of such fanins before the bin packing (exhaustively for few fanins). The implementation on this page does not do this, so it treats the sizes as if the supports were disjoint.
- **Replication.** At a fanout gate, the paper can copy the root LUT of a small tree into each reader, when this saves LUTs. This implementation does not replicate.
- **Chortle-d** (Francis, Rose and Vranesic, ICCAD 1991) uses the same bin packing view to minimize the depth of the LUT network instead of the count.
- **Cut-based mappers.** [FlowMap](/flowmap/) finds the least depth for any network with [K-feasible cuts](/k-feasible-cut/), and [CutMap](/cutmap/) and [DAOmap](/daomap/) reduce the LUT count at that depth. [Cut enumeration](/cut-enumeration/) and [priority cuts](/priority-cuts/) are the basis of most later mappers, and they handle fanout without cutting the network into trees.

## When to use it

Use Chortle-crf to learn how a mapper can use the freedom to split a wide gate, and as a fast area mapper for networks that are close to trees. For real FPGA flows, cut-based mappers give better results because they do not fix the tree boundaries and they control depth. The bin packing view is still useful inside other mappers whenever a wide associative gate must be split into $K$-input pieces.

## Pitfalls

- **Closing the wrong bin.** The closing loop must close the fullest bin first and put its output into the fullest bin with room. The example shows that the other order can cost an extra LUT.
- **Keeping only the least count.** If each gate keeps any solution with the fewest LUTs and not the one with the smallest open root, the parent can need more LUTs. Both conditions are needed.
- **Shared inputs.** A size is an upper bound on the distinct inputs only when the fanins have disjoint supports. If the network repeats an input inside a tree, the LUTs are still valid but may be larger than needed.
- **Operators.** The split of a gate over bins is only correct for associative and commutative operators. A gate such as a multiplexer must be decomposed into AND and OR gates first.
- **Optimality for larger K.** Do not quote the tree optimality for $K \ge 6$ as a theorem; the sources state the bound as $K \le 5$ (or $k \le 6$ in one survey).

## Implementations

## History

Francis, Rose and Chung's Chortle (DAC 1990, pages 613 to 619) was the first mapper for lookup-table FPGAs; it cut the network into trees and searched all decompositions of each gate, which grows exponentially with the fanin. In 1991 Francis, Rose and Vranesic gave Chortle-crf at DAC, which replaced that search with first-fit decreasing bin packing and added the use of reconvergent fanout and replication; the survey of Sangiovanni-Vincentelli, El Gamal and Rose reports that it ran up to 28 times faster than Chortle. In the same year, Chortle-d targeted depth. FlowMap (1992) then gave the least depth for general networks in polynomial time, and the later mappers moved from trees to cuts.

## References
