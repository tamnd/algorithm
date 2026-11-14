---
tag: RFE075
kind: algorithm
slug: symmetric-feasible-sequence-pair
name: Symmetric-feasible sequence pair
aliases:
- Balasa-Lampaert symmetric placement
area: eda/fpga-analog-and-emerging-technologies
level: advanced
summary: Balasa and Lampaert's condition on a sequence pair under which a symmetric packing exists, letting annealing search only placements that meet symmetry constraints.
solves: [floorplanning]
model: word-ram
complexity:
  vars: {n: the number of cells, g: the number of cells in the symmetric set}
  time: {check: O(n), repair: O(n), relations_and_y: O(n^2)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 2000
  people: [Florin Balasa, Koen Lampaert]
  note: Balasa and Lampaert gave the condition, the proof that it allows a symmetric placement, and an annealing placer over these pairs in IEEE Transactions on CAD in 2000.
prereqs: [sequence-pair, analog-symmetry-constraint, dag-longest-path, linear-programming-problem]
see_also: [asf-b-star-tree, common-centroid-layout, simulated-annealing-placement, floorplan-constraint-graphs, difference-constraints, b-star-tree-floorplan, permutation, topological-sort]
sources:
  - paper: doi:10.1109/43.851988
    title: Florin Balasa and Koen Lampaert, Symmetry within the sequence-pair representation in the context of placement for analog design, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 19(7), 721 to 731, 2000
    locator: the definition of a symmetric-feasible sequence pair, the theorem that such a pair has a symmetric placement, the size of the reduced search space, and the annealing placer
  - paper: "Florin Balasa, Sarat C. Maruvada and Karthik Krishnamoorthy, On the exploration of the solution space in analog placement with symmetry constraints, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 23(2), 177 to 191, 2004"
    title: F. Balasa, S. C. Maruvada and K. Krishnamoorthy, On the exploration of the solution space in analog placement with symmetry constraints, IEEE TCAD 23(2), 177 to 191, 2004
    locator: the exploration of the space of symmetric-feasible codes
  - paper: doi:10.1109/43.552084
    title: Hiroshi Murata, Kunihiro Fujiyoshi, Shigetoshi Nakatake and Yoji Kajitani, VLSI module placement based on rectangle-packing by the sequence-pair, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 15(12), 1518 to 1524, 1996
    locator: the sequence pair and its decoding by constraint graphs
  - paper: doi:10.1109/5.899053
    title: Georges G. E. Gielen and Rob A. Rutenbar, Computer-aided design of analog and mixed-signal integrated circuits, Proceedings of the IEEE 88(12), 1825 to 1854, 2000
    locator: the section on analog placement under symmetry constraints
---

A symmetric-feasible sequence pair is a [sequence pair](/sequence-pair/) whose two orders treat a symmetric set the same way as its mirror image does, so that the packing can place the group mirror-symmetric about one vertical axis. Its topic is analog sizing and layout, one of the five topics of this sub-area. Balasa and Lampaert gave the condition in 2000 and proved that every such pair has a symmetric placement. The condition is cheap to test and to restore after a move, so an annealing placer can search only these pairs, and every pair it sees meets the [symmetry constraint](/analog-symmetry-constraint/).

## In plain words

A sequence pair is two lists of the blocks. Two blocks in the same order in both lists sit side by side; two blocks in opposite orders sit one above the other.

In analog layout, some blocks come in matched pairs that must be mirror images about one vertical line, and some blocks must sit on that line. Most pairs of lists cannot give such a picture: they might ask a matched pair to sit one above the other.

The rule says: read the group's blocks in the first list, swap each block for its partner, and reverse. That must be the order in which the group's blocks appear in the second list. If the lists obey this, a mirror picture exists. If a move breaks it, rewrite the group's slots of the second list in this order to fix it. So the search only visits good lists.

## The problem

Given rectangular cells with widths $w_u$ and heights $h_u$, and one symmetric set $G$ with a pairing $\mathrm{sym} : G \to G$ (pairs of cells of equal size, and self-symmetric cells with $\mathrm{sym}(s) = s$), find a placement without overlap, of small area, in which the cells of each pair have the same $y$ and centers mirrored about a common vertical axis $x = X$, and each self-symmetric cell has its center on the axis. This is [floorplanning](/floorplanning/) with the symmetry constraint. Cells outside $G$ are free.

A sequence pair $(\Gamma^+, \Gamma^-)$ is two orders of the cells, with positions $p^+$ and $p^-$. As on the sequence-pair page, $u$ is left of $v$ when $u$ is before $v$ in both orders, and $u$ is below $v$ when $u$ is after $v$ in $\Gamma^+$ and before $v$ in $\Gamma^-$. The pair is *symmetric-feasible* when

$$p^+(x) < p^+(y) \iff p^-(\mathrm{sym}(y)) < p^-(\mathrm{sym}(x)) \quad \text{for all distinct } x, y \in G.$$

## The algorithm

The search is [simulated annealing](/simulated-annealing-placement/) over sequence pairs, as for plain floorplans. Each move changes one or both orders. REPAIR then restores the condition: it takes the group cells in their $\Gamma^+$ order, maps each to its partner, reverses this list, and writes it into the slots that the group cells take in $\Gamma^-$. The free cells keep their slots. The cost of a pair is the area (and wire length) of SYM-PACK.

```pseudo id=main
SYM-PACK(Γ+, Γ−, w, h, sym)        ▷ one symmetric set, axis vertical
L1  if the pair is not symmetric-feasible then return NONE
L2  for all cells u ≠ v, find whether u is left of v or below v
L3  merge the two cells of each pair into one node of the vertical graph
L4  order the nodes topologically along the below arcs
L5  y(node) ← the longest path to it, with arc weight h_u; each cell takes the y of its node
L6  constraints on x_u ≥ 0, X and W: x_u + w_u ≤ x_v for u left of v; x_u + w_u ≤ W;
        x_s + w_s / 2 = X for a self-symmetric s; x_u + x_sym(u) + w_u = 2X for a pair
L7  solve the linear program: minimize W subject to the constraints of L6
L8  return x, y, the axis X, the width W and the height max (y_u + h_u)
```

Line L1 takes $O(n)$ time: list the group cells in the order of $\Gamma^-$, and compare with the reversed list of mirrors in the order of $\Gamma^+$. Line L3 is what gives the two cells of a pair one $y$. Line L6 is not a system of difference constraints, because a pair adds a sum $x_u + x_{\mathrm{sym}(u)}$. So the code solves a small linear program, with an exact simplex method in fractions.

## Example

Take four cells: a pair $a, a'$ of size $1 \times 1$, a self-symmetric cell $s$ of size $2 \times 1$ (width by height), and a free cell $f$ of size $1 \times 2$. Let $\Gamma^+ = (f, a', a, s)$ and $\Gamma^- = (f, s, a', a)$.

The group cells in $\Gamma^+$ are $a', a, s$. Their mirrors are $a, a', s$, and reversed this is $s, a', a$, which is the order of the group in $\Gamma^-$. So the pair is symmetric-feasible.

| cells | order in $\Gamma^+$ | order in $\Gamma^-$ | relation |
|---|---|---|---|
| $f$, any other | $f$ first | $f$ first | $f$ left of it |
| $a'$, $a$ | $a'$ first | $a'$ first | $a'$ left of $a$ |
| $a'$, $s$ | $a'$ first | $s$ first | $s$ below $a'$ |
| $a$, $s$ | $a$ first | $s$ first | $s$ below $a$ |

So $s$ is at $y = 0$, the node $\{a, a'\}$ at $y = 1$, and $f$ at $y = 0$. For $x$: $f$ is at 0, $a'$ is at least 1, $a$ is at least 2, and $s$ is at least 1. The program gives $x_{a'} = 1$, $x_a = 2$ and the axis $X = 2$. The centers of the pair are at 1.5 and 2.5, and $x_s = X - 1 = 1$. The width is 3 and the height is 2, so the area 6 equals the total area of the cells, with no gap.

The order $\Gamma^- = (f, s, a, a')$ breaks the condition: $a'$ is before $a$ in $\Gamma^+$ but $a$ is before $a'$ in $\Gamma^-$, so $a$ would be below $a'$, and the two cells of a pair could not share one $y$. REPAIR rewrites the group slots as $s, a', a$ and gives back the order above.

## Correctness

The full proofs are in the proof file. The key lemma: if the condition holds and $u \ne v$ are in the group, then $u$ left of $v$ implies $\mathrm{sym}(v)$ left of $\mathrm{sym}(u)$, and $u$ below $v$ implies $\mathrm{sym}(u)$ below $\mathrm{sym}(v)$. Each follows from two uses of the condition. The same condition, read for $y = \mathrm{sym}(x)$, says that the two cells of a pair are in the same order in both lists, so they are side by side and never one above the other. For two self-symmetric cells it says the orders are opposite, so they are stacked on the axis and never side by side.

From the lemma, the merged vertical graph of line L3 has no cycle: the potential $f(x) = p^-(x) + p^-(\mathrm{sym}(x))$ rises along every below relation between group cells, and is the same for the two cells of a pair. So lines L4 and L5 give the least $y$ that keeps every below relation and gives each pair one $y$.

For a group with no free cells, the proof file builds a symmetric $x$ directly: average the least placement with its mirror image. The mirror keeps the relations by the key lemma, so the average keeps them too, and it has the same width. With free cells, Balasa and Lampaert prove that a symmetric placement that keeps the relations always exists. This page cites that result and does not prove it. Given that it exists, line L7 finds the one of least width. The $x$ and $y$ constraints share no variable, so SYM-PACK gives the least area among the symmetric placements that keep the relations of the pair.

## Complexity

- **The test and the repair.** $O(n)$ time with the position arrays.
- **The search space.** For each $\Gamma^+$, exactly $n!/g!$ orders $\Gamma^-$ pass the test, so there are $(n!)^2/g!$ symmetric-feasible pairs among the $(n!)^2$ pairs. With several groups of sizes $g_1, g_2, \ldots$, the conditions fix the relative orders of disjoint sets, and the count is $(n!)^2 / \prod_k g_k!$.
- **The packing.** Lines L2 to L5 take $O(n^2)$ time. The program of line L7 has $n + 2$ variables and $O(n^2)$ rows. Interior-point methods solve it in polynomial time. The exact simplex method of the code has no polynomial bound, but it is fast at the sizes of an analog placement.

These counts are proved. The time of a whole annealing run depends on the schedule, and there is no bound on the quality it reaches.

## Properties

- **Every visited placement is symmetric.** A placer that applies REPAIR after each move never needs a penalty for broken symmetry.
- **No loss of optimality for the relations.** By Theorem 6 of the proof file, the packing is the least symmetric one for its pair. In the two exhaustive tests of the implementation, the best packing over all symmetric-feasible pairs equals the best symmetric placement found by a grid search. This is measured on small instances; it is not a theorem of this page.
- **Symmetry without width cost for a group alone.** For a group with no free cells, the least symmetric width equals the least width without symmetry.
- **One axis per group.** Different groups have their own axes, which the program can tie together if the circuit needs one axis for all.

## Variants and improvements

- **Several symmetric sets.** The condition is applied to each group, and the program has one axis variable for each.
- **A horizontal axis.** Swap the roles of the left-of and below relations.
- **The solution space.** Balasa, Maruvada and Krishnamoorthy study how a placer explores the space of symmetric-feasible codes.
- **Symmetry islands.** The [ASF-B*-tree](/asf-b-star-tree/) keeps a group in a compact region with a tree whose every packing is symmetric by construction.
- **Common centroid.** Matched devices made of many unit cells use a [common-centroid layout](/common-centroid-layout/), which mirror symmetry about one axis does not give.

## When to use it

Use it in an annealing placer for analog blocks with mirror symmetry, when the placer already uses sequence pairs. It is a good fit for a few symmetric sets among tens of cells. For tight proximity of a group, or for a group that must form one connected region, a tree that builds islands is a better fit.

## Pitfalls

- **Testing only the pairs.** The condition must hold for every two distinct cells of the group, not only for the cells of each pair. A test that only checks partners passes pairs that have no symmetric placement. For two pairs $a, a'$ and $b, b'$, the orders $\Gamma^+ = (b, a, a', b')$ and $\Gamma^- = (a, b, b', a')$ keep each pair side by side, but put $a$ below $b$ and $b'$ below $a'$. As each pair shares one $y$, the pair $a, a'$ would be both below and above the pair $b, b'$.
- **Plain longest paths for $x$.** The least $x$ of each cell is in general not symmetric. Moving each cell to the mirror position after the longest path can create overlaps with free cells. The $x$ step must solve the symmetry equations and the relations together.
- **Half units.** The axis and the cell positions can be at half units, as for a self-symmetric cell of odd width with its center on an axis at a whole unit. Round to the manufacturing grid only after the whole group is placed, and round the two cells of a pair together.
- **Cells of different size in a pair.** The condition does not check sizes. The two cells of a pair must have the same width and height, or no mirror placement exists.

## Implementations

## History

Murata, Fujiyoshi, Nakatake and Kajitani gave the sequence pair in 1995. Balasa and Lampaert gave the symmetric-feasible condition, with the proof that every such pair has a symmetric placement and an annealing placer that keeps the condition, in IEEE Transactions on CAD in 2000. Balasa, Maruvada and Krishnamoorthy studied the search space in 2004. Later analog placers moved to trees, such as the ASF-B*-tree of Lin and Lin in 2007, which also keep a group in one region.

## References
