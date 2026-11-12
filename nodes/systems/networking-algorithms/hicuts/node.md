---
tag: RAB6MQ
kind: algorithm
slug: hicuts
name: HiCuts
aliases:
- hierarchical intelligent cuttings
- HiCuts decision tree
area: systems/networking-algorithms
level: research
summary: "A packet classifier that cuts the header space into equal pieces, one field at a time, until each leaf holds a few rules. A lookup walks down the tree and then scans one small leaf."
solves: [packet-classification]
model: word-ram
complexity:
  vars: {n: the number of rules, d: the number of fields, D: the depth of the tree, b: the leaf size bound binth, c: the larger of 2 and spfac}
  time: {worst: O(D + d b)}
  space: {extra: O(c^D n)}
properties: {deterministic: true, online: false}
history:
  year: 1999
  people: [Pankaj Gupta, Nick McKeown]
  note: Presented at Hot Interconnects VII in August 1999, and in IEEE Micro in 2000.
prereqs: [packet-classification, kd-tree-range-search]
see_also: [tuple-space-search, longest-prefix-match, kd-tree, orthogonal-point-enclosure, range-tree, tree-bitmap]
sources:
  - paper: "Pankaj Gupta and Nick McKeown, Packet classification using hierarchical intelligent cuttings, Hot Interconnects VII, Stanford, August 1999"
    locator: Sections 3 and 4 (the tree, the parameters binth and spfac, the heuristics, Table 1 and Figure 2, the results on real classifiers)
  - paper: doi:10.1109/40.820051
    title: Pankaj Gupta and Nick McKeown, Classifying packets with hierarchical intelligent cuttings, IEEE Micro 20(1), 2000
    locator: pages 34 to 41
  - paper: doi:10.1145/863955.863980
    title: Sumeet Singh, Florin Baboescu, George Varghese and Jia Wang, Packet classification using multidimensional cutting, ACM SIGCOMM 2003
    locator: pages 213 to 224 (HyperCuts)
  - paper: doi:10.1145/1851182.1851208
    title: Balajee Vamanan, Gwendolyn Voskuilen and T. N. Vijaykumar, EffiCuts, optimizing packet classification for memory and throughput, ACM SIGCOMM 2010
    locator: pages 207 to 218
  - paper: doi:10.1109/INFCOM.2009.5061972
    title: Yaxuan Qi, Lianghong Xu, Baohua Yang, Yibo Xue and Jun Li, Packet classification algorithms, from theory to practice, IEEE INFOCOM 2009
    locator: pages 648 to 656 (HyperSplit)
  - book: isbn:9780120884773
    title: George Varghese, Network Algorithmics, Morgan Kaufmann, 2005
    locator: Chapter 12, Packet Classification (the section on decision tree approaches)
---

HiCuts (hierarchical intelligent cuttings) is a decision tree for [packet classification](/packet-classification/), by Pankaj Gupta and Nick McKeown (1999). Each node of the tree owns a box of the header space and the rules that meet that box. If a node has more than $\mathit{binth}$ rules, it cuts its box along one field into $np$ equal pieces, one child for each piece. A lookup walks down the tree, at each node computing the child from one field of the packet with one division, and then tests the few rules of the leaf in priority order. Two parameters set the trade-off: $\mathit{binth}$ bounds the leaf size, and $\mathit{spfac}$ bounds how much the rule count may grow at each cut. On real classifiers of up to 1733 rules, the paper reports trees of depth at most 12 in under 1 MB.

## In plain words

Think of a big map with many overlapping shaded areas, one for each rule. You want to know which area a given point falls into first. Instead of testing every area, you cut the map into a few equal strips. Each strip keeps only the areas that touch it. If a strip still has too many areas, you cut it again, maybe the other way. You stop when each small piece has only a handful of areas.

To look up a point, you go to its strip, then to its piece inside the strip, and so on. At the end you test only the few areas of that small piece. The work is in choosing good cuts, so that the pieces stay small without copying the same areas into too many pieces.

## The problem

The input is a classifier: rules $R_1, \ldots, R_n$, each a box $[\mathit{lo}_1, \mathit{hi}_1] \times \cdots \times [\mathit{lo}_d, \mathit{hi}_d]$ over $d$ header fields of widths $W_1, \ldots, W_d$, in priority order. For a packet $x$, return the first rule that contains $x$. See [packet classification](/packet-classification/) for the problem and its bounds. HiCuts builds a static structure for a fixed classifier and is rebuilt when the rules change.

## The algorithm

**The tree.** Each node $v$ has a box $B(v)$, at the root the whole header space. Its rule list $R(v)$ holds the rules that meet $B(v)$, in priority order. A node is a leaf when $|R(v)| \le \mathit{binth}$. Otherwise it stores a cut $C(v)$: a field $j$ and a number of pieces $np$, a power of two. Its children own the $np$ equal pieces of $B(v)$ along field $j$.

**Lookup.**

```pseudo id=main
HICUTS-LOOKUP(root, x)                     ▷ x is a packet
L1  v ← root
L2  while v is not a leaf do
L3      (j, np) ← the cut of v; [b, b + s − 1] ← the side of B(v) along field j
L4      k ← ⌊(x_j − b) · np / s⌋
L5      v ← child k of v
L6  for each rule R in R(v), in priority order do
L7      if x ∈ R then return R
L8  return no match
```

**Build.** For a node with box $B$ and list $R$, the space measure of a cut $C$ into $np$ pieces is

$$\mathit{sm}(C) = \sum_{\text{children } c} |R(c)| + np,$$

the rule references plus the child pointers. The build accepts a cut only while $\mathit{sm}(C) \le \mathit{spfac} \cdot |R|$. The paper finds the largest such $np$ by a binary search; the version here starts at $np = 2$ and doubles while the bound holds.

```pseudo id=build
HICUTS-BUILD(B, R)                         ▷ R: the rules that meet box B
 1  if |R| ≤ binth then return a leaf with R
 2  for each field j whose side in B has more than one value do
 3      np_j ← 2
 4      while 2 · np_j ≤ side of B along j and sm(j, 2 · np_j) ≤ spfac · |R| do
 5          np_j ← 2 · np_j
 6  choose a field j by a heuristic (below), with np = np_j
 7  for k ← 0 to np − 1 do
 8      B_k ← piece k of B along j
 9      R_k ← the rules of R that meet B_k, without the redundant ones
10      child k ← HICUTS-BUILD(B_k, R_k)
```

**Choice of the field.** The paper lists four heuristics: (a) the field whose cut gives the smallest largest child, (b) the field with the largest entropy of the rule distribution over the children, (c) the field with the smallest $\mathit{sm}(C)$, and (d) the field with the most distinct range components among the rules of the node. The implementation uses (d) and breaks ties by (a).

**Two space savers from the paper.** Children with the same rule list share one node. A rule is *redundant* in a box if an earlier rule contains its part of the box, because no packet of the box can reach it; such rules are dropped. In particular, once a rule covers the whole box, all later rules are dropped.

## Example

The paper uses the 2-field classifier of its Table 1, with 8-bit fields $X$ and $Y$, $\mathit{binth} = 2$ and $\mathit{spfac} = 4$.

| rule | $X$ | $Y$ |
|---|---|---|
| R1 | 0 to 31 | 0 to 255 |
| R2 | 0 to 255 | 128 to 131 |
| R3 | 64 to 71 | 128 to 255 |
| R4 | 67 | 0 to 127 |
| R5 | 64 to 71 | 0 to 15 |
| R6 | 128 to 191 | 4 to 131 |
| R7 | 192 | 0 to 255 |

*The root.* $X$ and $Y$ each have 6 distinct ranges, so the tie goes to the smaller largest child, and that is $X$. A cut of $X$ into 8 pieces of 32 values gives the children

| $X$ piece | rules |
|---|---|
| 0 to 31 | R1 (R1 covers the piece, so R2 is redundant) |
| 32 to 63 | R2 |
| 64 to 95 | R2, R3, R4, R5 |
| 96 to 127 | R2 |
| 128 to 159 | R2, R6 |
| 160 to 191 | R2, R6 (shares the node of 128 to 159) |
| 192 to 223 | R2, R7 |
| 224 to 255 | R2 |

so $\mathit{sm} = 14 + 8 = 22 \le 4 \cdot 7 = 28$. A cut into 16 pieces would give $\mathit{sm} = 24 + 16 = 40 > 28$, so $np = 8$.

*The node for $X$ 64 to 95.* It has 4 rules, more than $\mathit{binth}$. Inside it, $Y$ has 4 distinct ranges and $X$ only 3 (R3 and R5 have the same $X$ range), so it cuts $Y$. Four pieces of 64 give R4 and R5; R4; R2 and R3; R3. That is $\mathit{sm} = 6 + 4 = 10 \le 16$, while 8 pieces would give $10 + 8 = 18 > 16$.

The tree has 12 nodes, 10 leaves, depth 2 and 14 rule references. The lookup of $x = (70, 140)$ computes $k = \lfloor 70 \cdot 8 / 256 \rfloor = 2$ at the root and $k = \lfloor 140 \cdot 4 / 256 \rfloor = 2$ at the next node, and reaches the leaf with R2 and R3. R2 fails ($Y = 140$ is not in 128 to 131) and R3 matches, which is also the answer of a linear search.

The paper's Figure 2 builds a different tree for the same rules: it cuts $X$ into 4 pieces at the root and $Y$ into 2 pieces below $X$ 64 to 127. In that tree the leaf for $X$ 64 to 127 and $Y$ 128 to 255 holds R2 and R3, because R6 does not meet $X$ 64 to 127.

## Correctness

The [proof](proofs/correctness.md) shows three facts. First, a rule is dropped as redundant in a box exactly when an earlier rule contains its part of the box, so computing a child's list from its parent's list gives the same result as computing it from all rules. Second, for any packet $x$ in a box, the first rule of the box's list that matches $x$ is the first rule of the whole classifier that matches $x$: that rule meets the box at $x$, and it cannot be redundant, because an earlier rule that contains its part of the box would contain $x$. Third, line L4 sends $x$ to the piece that contains $x_j$, because the pieces have equal size $s / np$. By induction the walk stays inside boxes that contain $x$, and the leaf scan returns the right answer. Each cut divides one side by a power of two, so the depth is at most $W = \sum_j W_j$ and the build ends.

## Complexity

A lookup visits at most $D + 1$ nodes, where $D \le W$ is the depth of the tree, and does one subtraction, one multiplication and one shift (since $s$ and $np$ are powers of two) at each. Then it tests at most $\mathit{binth}$ rules of $d$ fields. So a lookup costs $O(D + d \cdot \mathit{binth})$ time and $D + 1$ node reads plus the rule reads. This does not depend on $n$ directly, only through the depth.

The space has no good worst-case bound. Each cut keeps the sum of the children's rule counts below $\mathit{spfac}$ times the parent's count (or $2$ times for a 2-way cut), so depth $k$ holds at most $c^k n$ rule references with $c = \max(2, \mathit{spfac})$, and the total is $O(c^D n)$. On real classifiers the tree is far smaller. Gupta and McKeown report, with $\mathit{binth} = 8$ and $\mathit{spfac} = 4$, that 40 real 4-field classifiers with 100 to 1733 rules give trees of depth at most 12 (about 8 on average) in less than 1 MB.

On a synthetic 5-field classifier of 1000 rules (made by `random_classifier` with seed 7: addresses are prefixes of length 16, 24 or 32, the source is a wildcard in 30% of the rules, and ports and protocols take a few common values), the build gives these trees. A packet is drawn inside a random rule, 5000 times; linear search tests 493.2 rules on average for the same packets.

| $\mathit{binth}$ | $\mathit{spfac}$ | nodes | rule references | child pointers | depth | nodes visited, mean and max |
|---|---|---|---|---|---|---|
| 8 | 1 | 603 | 1671 | 602 | 14 | 9.40, 15 |
| 8 | 2 | 367 | 1400 | 370 | 6 | 2.34, 7 |
| 8 | 4 | 753 | 1762 | 1048 | 2 | 2.03, 3 |
| 8 | 8 | 985 | 1982 | 2096 | 2 | 2.02, 3 |
| 4 | 4 | 1145 | 2166 | 1692 | 6 | 2.44, 7 |
| 16 | 4 | 730 | 1708 | 1024 | 1 | 2.00, 2 |

A larger $\mathit{spfac}$ allows wider cuts: the tree gets flatter and the pointer count grows. A small $\mathit{spfac}$ forces 2-way cuts and a deep tree. This synthetic set separates well on the destination address, so it is easier than many real rule sets.

## Properties

- **Static.** The tree is built for a fixed rule set. An update can change many nodes, so classifiers that change often are rebuilt or use another method such as [tuple space search](/tuple-space-search/).
- **Arbitrary ranges.** Cuts work on ranges directly, so port ranges need no expansion into prefixes.
- **Tunable.** $\mathit{binth}$ and $\mathit{spfac}$ trade the lookup time against the memory, and the depth gives a known worst-case number of memory reads for a built tree.
- **Simple lookup.** Each step is a few arithmetic operations and one read, which suits hardware pipelines and network processors.

## Variants and improvements

- **HyperCuts** (Singh, Baboescu, Varghese and Wang, 2003) cuts several fields at one node, so it needs fewer levels. It also shrinks each node's box to the bounding box of its rules (region compaction) and pushes rules that all children share up into the node.
- **HyperSplit** (Qi, Xu, Yang, Xue and Li, 2009) splits each node in two at a rule endpoint instead of into equal pieces, which gives a binary tree that is deeper but much smaller.
- **EffiCuts** (Vamanan, Voskuilen and Vijaykumar, 2010) separates the rules into groups by which fields are wide, and builds one tree for each group. Wide rules, such as rules with a wildcard source, are the main cause of copies, and separating them cuts the memory by a large factor.
- **Leaf search.** The leaves can be searched in parallel in hardware, which allows a larger $\mathit{binth}$.
- **Learned cuts.** Later work chooses the cuts with reinforcement learning (NeuroCuts, 2019) instead of a fixed heuristic.

## When to use it

Use HiCuts or a descendant when the rule set is static or changes slowly, has a few thousand rules or fewer, and the lookup must have a known number of memory reads, as in a network processor or a hardware pipeline. Real firewall and access control lists have much structure, and decision trees use it well.

Do not use it when rules change all the time, as in a software switch under an SDN controller: [tuple space search](/tuple-space-search/) has $O(1)$ updates. Do not use it when many rules are wide in several fields at once: the copies grow fast, and EffiCuts or a TCAM does better.

## Pitfalls

- **Replication.** A rule that is wide in a field is copied into every piece of a cut along that field. Rules with wildcards in both address fields, combined with many narrow rules, can make the tree grow very fast. A build that only checks $\mathit{sm}$ per node can still produce a huge tree.
- **Useless cuts.** If every child of a cut gets every rule, the cut adds a level and saves nothing. A build must detect this case and stop with a larger leaf, or it can cut until each box is one point.
- **Redundant rules.** Without redundancy removal, a rule that covers a box still leaves all the later rules in it, and the tree never shrinks them below $\mathit{binth}$. Removing at least the rules behind a covering rule is needed for the tree to stay finite in practice.
- **Shared nodes.** Sharing a node between pieces is safe for leaves with equal lists. An internal node that is shared must compute its child indices relative to its own box, not the box of one particular parent piece.
- **Non-power-of-two cuts.** With $np$ and the box sides powers of two, line L4 is a shift. Other values need a real division, or the pieces are not equal.

## Implementations

## History

Gupta and McKeown presented HiCuts at Hot Interconnects VII in August 1999 and published it in IEEE Micro in 2000. In the same year, at SIGCOMM 1999, they also gave Recursive Flow Classification, and Srinivasan, Suri and Varghese gave [tuple space search](/tuple-space-search/). HiCuts was the first of many decision tree classifiers: HyperCuts (2003), HyperSplit (2009) and EffiCuts (2010) all keep its idea of cutting the header space and change how the cuts are chosen.

## References
