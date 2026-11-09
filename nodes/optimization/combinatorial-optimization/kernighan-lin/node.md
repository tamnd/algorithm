---
tag: NEYJA8
kind: algorithm
slug: kernighan-lin
name: Kernighan-Lin algorithm
aliases:
- KL algorithm
- Kernighan-Lin heuristic
- Kernighan-Lin bisection
area: optimization/combinatorial-optimization
level: core
summary: Improve a bisection by swapping vertex pairs in passes of tentative gain sequences.
solves: [graph-partitioning-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, p: the number of passes}
  time: {worst: Θ(p n^3), average: Θ(p n^3), best: Θ(n^3)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1970
  people: [Brian W. Kernighan, Shen Lin]
  note: Kernighan and Lin published the method in the Bell System Technical Journal in 1970, for the placement of circuit components on boards.
prereqs: [graph-partitioning-problem, local-search, cut]
see_also: [graph-partitioning-problem, fiduccia-mattheyses, lin-kernighan, local-search, local-optimum, pls, spectral-clustering, simulated-annealing]
sources:
  - paper: doi:10.1002/j.1538-7305.1970.tb01770.x
    title: B. W. Kernighan and S. Lin, An efficient heuristic procedure for partitioning graphs, Bell System Technical Journal 49(2), 291 to 307, 1970
    locator: the gain formula, the pass of tentative swaps with locking, and the choice of the best prefix
  - paper: doi:10.1109/DAC.1982.1585498
    title: C. M. Fiduccia and R. M. Mattheyses, A linear-time heuristic for improving network partitions, 19th Design Automation Conference, 175 to 181, 1982
    locator: the single-vertex variant with bucket lists
  - paper: doi:10.1287/opre.37.6.865
    title: David S. Johnson, Cecilia R. Aragon, Lyle A. McGeoch and Catherine Schevon, Optimization by simulated annealing, an experimental evaluation, part I, graph partitioning, Operations Research 37(6), 865 to 892, 1989
    locator: the experimental comparison of Kernighan-Lin and simulated annealing on random and geometric graphs
  - paper: "David S. Johnson, Christos H. Papadimitriou and Mihalis Yannakakis, How easy is local search?, Journal of Computer and System Sciences 37(1), 79 to 100, 1988"
    locator: the class PLS and the PLS-completeness of the Kernighan-Lin neighborhood for graph partitioning
  - paper: doi:10.1137/S1064827595287997
    title: George Karypis and Vipin Kumar, A fast and high quality multilevel scheme for partitioning irregular graphs, SIAM Journal on Scientific Computing 20(1), 359 to 392, 1998
    locator: the use of Kernighan-Lin style refinement in the multilevel method
---

The Kernighan-Lin algorithm is a [local search](/local-search/) heuristic for the [graph partitioning problem](/graph-partitioning-problem/). It improves a given bisection $(A, B)$ in *passes*. In each pass it swaps a pair $a \in A$, $b \in B$ of greatest gain, locks the two vertices, and repeats until every vertex on the smaller side is locked, even when the gains become negative. Then it applies only the best prefix of these tentative swaps. Because a pass may go through bad swaps to reach a good state, the method escapes many [local optima](/local-optimum/) of the simple swap neighborhood. The sizes of the sides never change, each applied pass lowers the cut, and the result is a local optimum for single swaps, but there is no guarantee of quality relative to the optimum. With the direct pair search one pass takes $\Theta(n^3)$ time.

## In plain words

You have split the vertices of a graph into two equal groups, and you want fewer edges between the groups. Moving one vertex would break the balance, so you trade one vertex from each group.

A pass works like this. Find the trade that helps the most, or hurts the least, do it on paper, and freeze the two traded vertices. Find the best trade among the vertices that are not frozen, do it on paper, and freeze them. Go on until nothing is left to trade. Then look back over the list of trades and keep only the first few that together helped the most. Throw away the rest.

A trade that hurts may open the way for a trade that helps a lot, and the look back finds this. Repeat passes until a pass helps nothing.

## The problem

The input is a graph with non-negative edge weights $w(u, v)$ and a partition $(A, B)$ of its vertices, usually with $|A| = |B| = n/2$. The output is a partition $(A^*, B^*)$ with $|A^*| = |A|$ and $|B^*| = |B|$ and a small *cut*, the total weight of the edges between the sides. Finding the least cut is the [minimum bisection](/graph-partitioning-problem/) problem, which is NP-hard, so the algorithm aims at a good cut, not the best one.

For a vertex $v$, let $E(v)$ be the weight of its edges to the other side, $I(v)$ the weight of its edges to its own side, and $D(v) = E(v) - I(v)$. Swapping $a \in A$ with $b \in B$ lowers the cut by the *gain*
$$ g(a, b) = D(a) + D(b) - 2 w(a, b). $$
The term $2 w(a, b)$ is there because the edge between $a$ and $b$ stays cut.

## The algorithm

```pseudo id=main
KERNIGHAN-LIN(G, w, A, B)
L1  repeat
L2      compute D(v) = E(v) − I(v) for every vertex v, and unlock all vertices
L3      for p ← 1 to min(|A|, |B|) do                   ▷ tentative swaps on copies A′, B′
L4          choose unlocked a ∈ A′ and b ∈ B′ that maximize g = D(a) + D(b) − 2w(a, b)
L5          record g_p ← g and the pair (a_p, b_p); lock a and b; swap them in A′ and B′
L6          for each unlocked x ∈ A′ do D(x) ← D(x) + 2w(x, a) − 2w(x, b)
L7          for each unlocked y ∈ B′ do D(y) ← D(y) + 2w(y, b) − 2w(y, a)
L8      choose the smallest k ≥ 0 that maximizes G_k = g_1 + ⋯ + g_k  (G_0 = 0)
L9      if G_k ≤ 0 then exit the loop
L10     swap a_1, …, a_k with b_1, …, b_k in A and B
L11 return (A, B)
```

Lines L6 and L7 keep $D$ correct for the tentative partition $(A', B')$ without recomputing it from scratch: when $a$ leaves the side of $x$, the edge $\{x, a\}$ becomes external, and when $b$ joins it, the edge $\{x, b\}$ becomes internal. Ties in line L4 go to the pair found first, so the method is deterministic.

## Example

Take the graph of the [graph partitioning](/graph-partitioning-problem/) page: two triangles $a, b, c$ and $d, e, f$, joined by the edges $cd$ and $be$, all of weight 1. Start from $A = \{a, b, d\}$, $B = \{c, e, f\}$, with cut 6. Line L2 gives $D(a) = 0$, $D(b) = 1$, $D(d) = 3$, $D(c) = 3$, $D(e) = 1$, $D(f) = 0$.

| step | unlocked $D$ values before the step | pair | gain $g_p$ | $G_p$ | tentative cut |
| --- | --- | --- | --- | --- | --- |
| 1 | $a\,0, b\,1, d\,3 \mid c\,3, e\,1, f\,0$ | $(d, c)$ | $3 + 3 - 2 = 4$ | 4 | 2 |
| 2 | $a\,{-2}, b\,{-1} \mid e\,{-1}, f\,{-2}$ | $(a, e)$ | $-3$ | 1 | 5 |
| 3 | $b\,{-1} \mid f\,0$ | $(b, f)$ | $-1$ | 0 | 6 |

Line L8 picks $k = 1$ with $G_1 = 4$, and line L10 swaps only $d$ and $c$. The new partition $\{a, b, c\}, \{d, e, f\}$ has cut $6 - 4 = 2$. The second pass finds the gains $-2, 0, 2$, so its best prefix is $k = 0$ and line L9 stops. The result is optimal here, which the graph partitioning page shows by a spectral bound. The gains of the first pass add up to 0, because after a full pass the two sides have changed places.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Gain formula.** Swapping $a$ and $b$ lowers the cut by exactly $D(a) + D(b) - 2 w(a, b)$, and lines L6 and L7 give the exact $D$ values of the tentative partition.
- **Balance.** Each swap moves one vertex out of each side and one into it, so the sides keep their sizes.
- **Progress.** The tentative partition after $k$ swaps has cut $\mathrm{cut}(A, B) - G_k$. So line L10 lowers the cut by $G_k > 0$.
- **Termination.** The cut strictly falls with every applied pass, so no partition repeats. With integer weights there are at most $\mathrm{cut}(A, B) + 1$ passes.
- **Local optimality.** In the last pass, $g_1$ is the best gain of any single swap and $G_1 = g_1 \le 0$. So no single swap improves the output.

## Complexity

Let $n$ be the number of vertices, with sides of size $n/2$, and let $p$ be the number of passes.

- **Per pass.** Line L2 takes $\Theta(n^2)$ time with an adjacency matrix. Step $p$ of the inner loop searches $(n/2 - p + 1)^2$ pairs in line L4, and these add up to $\Theta(n^3)$. Lines L6 and L7 take $O(n)$ per step. So one pass takes $\Theta(n^3)$ time.
- **Faster pair search.** Kernighan and Lin sort the $D$ values of each side in decreasing order and scan pairs in that order, stopping when $D(a) + D(b)$ is at most the best gain found, because $w(a, b) \ge 0$. They reported $O(n^2 \log n)$ time per pass in practice with this rule.
- **Number of passes.** With integer weights $p \le \mathrm{cut}(A, B) + 1$. No polynomial bound on $p$ is known for general weights. Kernighan and Lin observed that few passes are needed in practice. In our measurement below the mean was 2.2 passes, counting the last pass that changes nothing.
- **Space.** Besides the graph, the algorithm stores $D$, the lock flags, the tentative sides and the list of pairs and gains, which is $\Theta(n)$.

## Properties

- **Heuristic.** Kernighan-Lin is not exact and has no proved approximation ratio. Its output is a local optimum of a large neighborhood: no prefix of a pass improves it.
- **Hardness of local optima.** Johnson, Papadimitriou and Yannakakis (1988) showed that finding a partition that is locally optimal for the Kernighan-Lin neighborhood is complete for the class [PLS](/pls/). So no polynomial-time method to find such a local optimum is expected, by this or any other algorithm.
- **Balance is exact.** The algorithm never changes the sizes of the sides. This is a strength for bisection, but it also means that it cannot use a small imbalance to escape a local optimum.
- **Measured quality.** On 300 random graphs $G(14, 0.3)$ (Python `random.Random(2026)`), each started from a random bisection, the cut found was on average 1.021 times the minimum bisection width found by brute force, with median 1.000 and maximum 1.5. It was optimal in 88 percent of the graphs, while the random start was on average 1.99 times the optimum. These are small graphs, so this measures behavior, not a bound.

## Variants and improvements

- **[Fiduccia-Mattheyses](/fiduccia-mattheyses/).** Move one vertex at a time under a balance tolerance, and keep the gains in buckets. A pass then takes time linear in the number of edges, and the method extends to hypergraphs.
- **Unequal sides.** Kernighan and Lin add dummy vertices without edges to get sides of equal size, or limit the number of swaps to the smaller side, as above.
- **k-way partitioning.** Apply the method to pairs of parts in turn, or use a direct $k$-way version.
- **Multilevel refinement.** In METIS and similar tools (Karypis and Kumar, 1998), Kernighan-Lin or Fiduccia-Mattheyses refines the partition at each level of a hierarchy of coarser graphs. This gives much better results on large graphs than one run on the full graph.
- **[Lin-Kernighan](/lin-kernighan/).** Lin and Kernighan used the same idea of a chain of tentative moves with the best prefix for the traveling salesman problem in 1973.

## When to use it

- To refine a bisection of a small or medium graph that comes from another method, such as a spectral split or a random start.
- As the refinement step of a multilevel partitioner, where each level needs only a few cheap passes.
- When the sides must have exactly equal sizes.

For large sparse graphs, prefer [Fiduccia-Mattheyses](/fiduccia-mattheyses/) or a multilevel tool, because the $\Theta(n^2)$ cost of line L2 and the pair search are too slow. For a proof of optimality, use exact methods.

## Pitfalls

- **Stopping at the first negative gain.** The point of a pass is to continue through negative gains. A version that stops at the first $g_p \le 0$ is simple hill climbing on swaps and finds worse cuts.
- **Forgetting the edge between the pair.** The gain is $D(a) + D(b) - 2 w(a, b)$, not $D(a) + D(b)$. The edge $\{a, b\}$ is cut before and after the swap.
- **Updating locked vertices.** Lines L6 and L7 update only unlocked vertices. The $D$ values of locked vertices are not needed and are not correct after later swaps.
- **Applying the full pass.** The partition at the end of a pass is not the result. For equal sides it is the start with the sides exchanged.
- **Ties at zero.** Line L9 must stop when the best prefix sum is 0, else the algorithm can cycle among partitions of equal cut.

## Implementations

## History

Brian Kernighan and Shen Lin published the method in 1970 in the Bell System Technical Journal, as a way to assign the components of electronic circuits to boards with few connections between boards. The idea of a chain of tentative moves with the best prefix, often called *variable depth search*, became one of the most successful ideas in local search: Lin and Kernighan used it for the traveling salesman problem in 1973. Fiduccia and Mattheyses (1982) made a pass run in linear time by moving single vertices. Johnson, Aragon, McGeoch and Schevon (1989) compared it with simulated annealing on many graph classes, and Johnson, Papadimitriou and Yannakakis (1988) used its neighborhood as a central example of the class PLS. Since the 1990s it has been used mainly as the refinement step of multilevel partitioners.

## References
