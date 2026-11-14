---
tag: FCVE23
kind: algorithm
slug: tseng-siewiorek-clique-partitioning
name: Tseng-Siewiorek clique partitioning
aliases:
- clique partitioning binding
- Facet algorithm
area: eda/high-level-synthesis-and-scheduling
level: core
summary: Tseng and Siewiorek's greedy heuristic that merges the pair of compatible nodes with the most common neighbours until the compatibility graph is split into cliques.
solves: [resource-binding, register-binding, clique-cover]
model: word-ram
complexity:
  vars: {n: the number of vertices of the compatibility graph, m: the number of its edges}
  time: {worst: O(n^2 m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1986
  people: [Chia-Jeng Tseng, Daniel P. Siewiorek]
  note: Tseng and Siewiorek published the greedy clique partitioning of compatibility graphs in IEEE Transactions on Computer-Aided Design in 1986, for unit, register and bus allocation in the Facet system at Carnegie Mellon.
prereqs: [resource-compatibility-graph, clique-cover, greedy-algorithm]
see_also: [left-edge-algorithm, interval-partitioning, resource-binding, register-binding, interconnect-binding, weighted-bipartite-matching-binding, chordal-graph-coloring, dsatur]
sources:
  - paper: doi:10.1109/TCAD.1986.1270207
    title: Chia-Jeng Tseng and Daniel P. Siewiorek, Automated synthesis of data paths in digital systems, IEEE Transactions on Computer-Aided Design 5(3), 379 to 395, 1986
    locator: the clique partitioning heuristic (merge the pair with the most common neighbours, ties by the fewest deleted edges) and its use for units, registers and buses
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 6, Resource Sharing and Binding (the clique partitioning heuristic of Tseng and Siewiorek)
---

Tseng-Siewiorek clique partitioning is a greedy heuristic for the [clique cover problem](/clique-cover/) on a [resource compatibility graph](/resource-compatibility-graph/), published by Tseng and Siewiorek in 1986 for [high-level synthesis](/high-level-synthesis/). Each vertex starts as its own group. While two groups are joined by an edge, the algorithm merges the pair with the most common neighbours, breaking ties by the fewest edges lost, and keeps only the edges to the common neighbours. Each final group is a clique, and so one shared unit, register or bus. The result is always a valid binding in which no two groups can be merged, in $O(n^2 m)$ time. It is not optimal in general, and it is not optimal even on the interval graphs of straight-line code, where the [left-edge algorithm](/left-edge-algorithm/) is.

## In plain words

Think of each operation as a person, and draw a line between two people who could share a desk because they are never in the office at the same time. We want few desks. Start with one desk per person. Then pick two people who could share and who have the most other possible deskmates in common, and seat them together. From then on, the pair counts as one, and it can only take in someone who could share with both. Repeat until no pair can be joined. Choosing the pair with the most shared friends keeps many options open for later merges. It is fast and usually good, but it can miss the fewest desks.

## The problem

Given an undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, partition $V$ into the fewest cliques. In binding, $G$ is the compatibility graph of the operations of one unit type, of the values that need registers, or of the data transfers that need buses, and each clique is one shared unit, register or bus. See [resource binding](/resource-binding/), [register binding](/register-binding/) and [interconnect binding](/interconnect-binding/). The problem is NP-hard in general, so the algorithm is a heuristic.

## The algorithm

A *supernode* is a group of vertices, with a list of member vertices and a set $N(i)$ of neighbouring supernodes. Merging two adjacent supernodes $i$ and $j$ removes the edges at $i$ and $j$ and gives the new supernode an edge to each common neighbour. The number of edges lost is
$$\mathrm{del}(i, j) = |N(i)| + |N(j)| - 1 - |N(i) \cap N(j)|,$$
since the edges at $i$ or $j$ number $|N(i)| + |N(j)| - 1$, and the common neighbours keep one edge each.

```pseudo id=main
TSENG-SIEWIOREK(G)
L1  make one supernode per vertex v, with members {v} and N(v) the neighbours of v in G
L2  while some supernode has a neighbour do
L3      for each pair of adjacent supernodes i < j do
L4          key(i, j) ← (−|N(i) ∩ N(j)|, del(i, j), i, j); keep the pair (i, j) with the least key
L5      members(i) ← members(i) ∪ members(j)
L6      N(i) ← (N(i) ∩ N(j)) \ {i, j}; delete j and update the neighbour sets of the others
L7  return the member lists of the supernodes
```

Line L4 takes the most common neighbours first, then the fewest lost edges, then the smallest pair of indices, so the run is deterministic. Line L6 keeps an edge from the new supernode only to supernodes that were joined to both $i$ and $j$.

## Example

Take the values of the straight-line example on the [register binding](/register-binding/) page, with lifetimes $a = \{1, 2\}$, $b = \{1\}$, $c = \{2, 3\}$, $d = \{3, 4, 5\}$, $e = \{4\}$, $f = \{5\}$ and $g = \{2, 3\}$, numbered $0$ to $6$ in this order. Two values are compatible when their lifetimes do not meet. The compatibility graph has 13 edges:
$$ad,\ ae,\ af,\ bc,\ bd,\ be,\ bf,\ bg,\ ce,\ cf,\ ef,\ eg,\ fg.$$

| merge | pair | common neighbours | edges lost | groups after the merge |
|---|---|---|---|---|
| 1 | $e, f$ | $a, b, c, g$ (4) | 5 | $\{e, f\}$ |
| 2 | $b, ef$ | $c, g$ (2) | 5 | $\{b, e, f\}$ |
| 3 | $a, d$ | none (0) | 1 | $\{a, d\}$, $\{b, e, f\}$ |
| 4 | $bef, c$ | none (0) | 2 | $\{a, d\}$, $\{b, c, e, f\}$ |

In merge 1, $e$ and $f$ share four neighbours, more than any other pair. After merges 1 and 2, the edges left are $ad$, $\{b, e, f\} c$ and $\{b, e, f\} g$, each pair with no common neighbour. Merge 3 takes $ad$, which loses only 1 edge. Merge 4 has a tie between $c$ and $g$, both losing 2 edges, and takes $c$ by its smaller index. Then $c$ and $g$ are left with no edge, since their lifetimes are equal. The result is $\{a, d\}$, $\{b, c, e, f\}$ and $\{g\}$, three registers. Three values are live in step 2, so three is the least, and the left-edge algorithm gives the same groups here.

## Correctness

What is proved, in the [full proof](proofs/correctness.md):

- **Each group is a clique, and the groups are fully joined exactly when they are adjacent.** Two supernodes are adjacent exactly when every member of one is adjacent in $G$ to every member of the other. This holds at L1 and is kept by L5 and L6, so each merge at L5 joins two cliques with all edges between them into one clique.
- **Termination.** Each pass of the loop removes one supernode, so there are at most $n - 1$ merges.
- **Valid and maximal.** The output partitions $V$ into cliques, so it is a valid binding. No two output groups can be merged into a larger clique.
- **Exact on unions of cliques.** If $G$ is a disjoint union of cliques, the output is exactly those cliques, which is optimal.

What is not proved, and is false: that the number of groups is the least.

- On the graph made of a triangle $\{0, 1, 2\}$ with one pendant vertex on each corner, the algorithm merges the triangle first and ends with 4 groups, while the 3 pendant edges are a partition into 3 cliques.
- On the interval lifetimes $u_0, \ldots, u_7 = [0, 0], [0, 2], [1, 1], [1, 3], [1, 3], [2, 4], [3, 3], [4, 4]$, at most 4 intervals share a point, so 4 registers suffice, for example $\{u_0, u_3, u_7\}$, $\{u_1, u_6\}$, $\{u_2, u_5\}$, $\{u_4\}$. The algorithm merges $u_0$ with $u_7$ (4 common neighbours), then $u_2$ with $u_6$, then the two pairs, and ends with 5 groups. Every order of breaking the ties ends with 5.

These failures are measured as well, as tests and not as bounds. Over all $2^{15} = 32768$ graphs on 6 labelled vertices, the algorithm misses the optimum on 180, and it is optimal on every graph with at most 5 vertices. On 1000 random graphs with 2 to 9 vertices, it uses one extra clique on 11 of them and is optimal on the rest. On 1000 random interval instances with at most 9 intervals, it reached the depth every time, so the interval failure above is rare.

## Complexity

Each pass of the loop scans the adjacent pairs, at most $m$, and intersects two neighbour sets of size at most $n$, for $O(nm)$ time per pass. There are at most $n - 1$ passes, so the time is $O(n^2 m)$. Keeping the number of common neighbours of each edge up to date after each merge lowers the cost of a pass. The space is $O(n + m)$ for the members and the neighbour sets.

## Properties

- **Deterministic.** The tie rule of L4 fixes the run. Other tie rules give other partitions, sometimes of a different size.
- **Not exact.** It can use more cliques than needed, also on interval graphs.
- **Maximal output.** No two output groups can be joined, so the output is never improved by merging alone.
- **Uses only the graph.** The rule looks at common neighbours, not at lifetimes or schedules, so it applies to conditional code and loops, where the conflict graph is not an interval graph.

## Variants and improvements

- **Weighted merges.** Weight each edge by the interconnect two operations save when they share a unit, such as common operand sources, and merge the heaviest edge first. This trades unit count for multiplexer inputs, see [interconnect binding](/interconnect-binding/).
- **Faster bookkeeping.** Keep the number of common neighbours for each edge, and update only the edges near the merged pair.
- **Bus allocation.** The same greedy on the compatibility graph of data transfers groups transfers into buses.
- **Coloring the conflict graph instead.** A partition into cliques of $G$ is a coloring of its complement, so coloring heuristics such as [DSatur](/dsatur/) are an alternative.

## When to use it

Use it when the compatibility graph has no special structure, for example with mutually exclusive branches or loop lifetimes, and the graph is small enough for $O(n^2 m)$. For straight-line code, where the conflict graph is an interval graph, use the [left-edge algorithm](/left-edge-algorithm/) or [interval partitioning](/interval-partitioning/), which are exact and faster. For chordal conflict graphs, [chordal graph coloring](/chordal-graph-coloring/) is exact. When interconnect matters as much as the count, [weighted bipartite matching binding](/weighted-bipartite-matching-binding/) is a common choice for registers.

## Pitfalls

- **Assuming it is optimal on straight-line code.** It is not, as the interval example shows. An implementation that checks its result against the largest number of values live in one step must allow a larger count.
- **Mixing unit types in one graph.** The graph must be built for one unit type, or a clique may contain operations that no single unit can run, see the non-examples on the [resource compatibility graph](/resource-compatibility-graph/) page.
- **Forgetting to drop edges.** After a merge, the new supernode may only stay adjacent to common neighbours. Keeping the union of the neighbour sets produces groups that are not cliques.
- **Missed mutual exclusion.** Fewer detected exclusions means fewer edges, and so more units.

## Implementations

## History

Tseng and Siewiorek (1986) described data path synthesis as three clique partitioning problems, for functional units, registers and buses, and gave this greedy for all three. Their system at Carnegie Mellon was called Facet. Kurdahi and Parker (1987) showed that for registers in straight-line code the left-edge algorithm is exact and faster, and later binders added interconnect weights, or replaced the greedy by matching, as in the binder of Huang, Chen, Lin and Hsu (1990).

## References
