---
tag: TAC0AY
kind: algorithm
slug: lin-kernighan
name: Lin-Kernighan heuristic
aliases:
- LK heuristic
- Lin-Kernighan-Helsgaun
- variable-depth k-opt
area: approximation/tsp-approximation
level: advanced
summary: A variable-depth k-opt local search that grows a chain of edge exchanges while the partial gain stays positive; it gives tours within about 2 percent of OPT in practice.
solves: [metric-tsp]
model: real-ram
complexity:
  vars: {n: the number of cities, k: the length of a candidate list}
  time: {step: O(k + n), search: O(n(k + n))}
  space: {extra: Θ(n k)}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 1973
  people: [Shen Lin, Brian W. Kernighan]
  note: Lin and Kernighan (1973) built k-opt moves step by step with a gain criterion, after the variable-depth idea of Kernighan and Lin (1970) for graph partitioning.
prereqs: [two-opt, three-opt, local-search, neighborhood-structure]
see_also: [lin-kernighan-helsgaun, two-opt, three-opt, or-opt, kernighan-lin, iterated-local-search, large-neighborhood-search, local-optimum]
sources:
  - paper: doi:10.1287/opre.21.2.498
    title: Shen Lin and Brian W. Kernighan, An effective heuristic algorithm for the traveling-salesman problem, Operations Research 21(2), 1973
    locator: pages 498 to 516 (the gain criterion, the tabu rules, the backtracking breadth and the results)
  - title: David S. Johnson and Lyle A. McGeoch, The traveling salesman problem, a case study in local optimization, in Aarts and Lenstra (eds.), Local Search in Combinatorial Optimization, Wiley, 1997
    locator: Section 4 (an LK implementation, candidate lists, don't-look bits, and tours about 2 percent above the Held-Karp bound on random uniform instances)
  - title: Christos H. Papadimitriou, The complexity of the Lin-Kernighan heuristic for the traveling salesman problem, SIAM Journal on Computing 21(3), 1992
    locator: pages 450 to 465 (finding a local optimum of a version of LK is PLS-complete)
---

The Lin-Kernighan heuristic (LK) is a [local search](/local-search/) for the [TSP](/metric-tsp/) that does not fix the number of edges a move changes. It removes one tour edge, which leaves a path, and then makes a chain of steps. Each step adds an edge from the free end of the path and removes one edge, so after $j$ steps the closed path is a $(j+1)$-opt move. The chain goes on while the sum of the gains so far stays positive, and the best closed tour on the chain is kept. This lets LK find improvements that need a bad first exchange, which [2-opt](/two-opt/) and [3-opt](/three-opt/) cannot see. LK and its descendants, such as [LKH](/lin-kernighan-helsgaun/), give the best tours in practice of all simple local searches.

## In plain words

Take out one road of the tour. Now the trip is a line with a fixed start and a loose end.

From the loose end, build a new road to some city. That city now has three roads, so take out one of them, the one that keeps the trip a line. The loose end moves to a new city.

Keep score: what you took out minus what you built. Go on while the score is positive, even if closing the line now would not help. At each stage, check how good the tour is if you close the line back to the start, and remember the best one.

If the best one is shorter than the old tour, keep it and start again. When no start gives a shorter tour, stop.

## The problem

The input is a set $V$ of $n$ cities with costs $d(u, v) = d(v, u) \ge 0$, a start tour, and for each city a candidate list of $k$ other cities, usually its nearest ones. The output is a tour on which no LK search gains. OPT is the least cost of a tour and ALG is the cost of the returned tour. The convention is ALG $\le \rho \cdot$ OPT for a minimization problem. A ratio is proved here only when the candidate lists hold all cities.

## The algorithm

The search keeps a Hamiltonian path from a fixed city $t_1$ to a free end $y$ and the partial gain $G$, which is the cost removed minus the cost added so far.

```pseudo id=main
LIN-KERNIGHAN(d, T)
L1  repeat
L2      for each city t1 and each tour edge {t1, y} do
L3          G = d(t1, y); search from the path T minus {t1, y}, where one step is:
L4              pick a candidate z of the free end y, w after z, with G - d(y, z) > 0 and no tabu edge
L5              add {y, z}, remove {z, w}, reverse the path from w to y, G = G - d(y, z) + d(z, w)
L6              record the tour closed by {w, t1} if its gain G - d(w, t1) is the best so far
L7              step again from w while G is above the best recorded gain
L8          if the search recorded a gain then apply the best tour; go to L1
L9  until no search gains; return T
```

Here $w$ is the city after $z$ on the path, on the side of $y$, so the new path runs from $t_1$ to $z$, then from $y$ back to $w$. The tabu rules are the ones of Lin and Kernighan: an added edge is never removed, and a removed edge is never added again. Line L4 is the gain criterion. The implementation tries the 5 best candidates at the first step, 3 at the second and 1 after that, ranked by $d(z, w) - d(y, z)$, and backtracks only until it finds a gain. The default candidate lists hold the 8 nearest cities.

## Example

Take the seven cities of the [3-opt](/three-opt/) page, $A(1,2)$, $B(0,5)$, $C(3,3)$, $D(1,0)$, $E(0,0)$, $F(3,4)$ and $G(2,6)$, with the Euclidean distance, and the tour $A\,C\,F\,G\,B\,E\,D$ of length 15.708. It is 2-optimal, so no 2-opt move helps. Start at $t_1 = B$ and remove $BE$. The path is $B\,G\,F\,C\,A\,D\,E$ with free end $E$ and $G = 5$.

| step | add | remove | new path | $G$ | close with | closing gain |
|---|---|---|---|---|---|---|
| 1 | $EA$, 2.236 | $AD$, 2 | $B\,G\,F\,C\,A\,E\,D$ | 4.764 | $DB$, 5.099 | $-0.335$ |
| 2 | $DC$, 3.606 | $CA$, 2.236 | $B\,G\,F\,C\,D\,E\,A$ | 3.394 | $AB$, 3.162 | 0.232 |

After step 1 the closed tour would be longer, but $G$ is still positive, so the search goes on. After step 2 the closed tour $B\,G\,F\,C\,D\,E\,A$ has length 15.476, which is OPT. The search tries one more step that gives the same tour, and then returns the gain 0.232. The result is a 3-opt move that LK found as a 2-opt move with a loss followed by a step that repairs it.

**Measured behavior.** On 300 seeded instances of 10 uniform random points in the unit square, with OPT from the Held-Karp program, LK with the default settings from a random tour gave tours 0.01 percent above OPT on average, at most 1.017 times OPT, and the optimum in 298 cases, with 3.8 improvements on average. On the same instances 2-opt gave 1.05 percent, 3-opt 0.04 percent and Or-opt 0.06 percent. Johnson and McGeoch (1997) report LK tours about 2 percent above the Held-Karp bound on large random uniform instances, against about 5 percent for 2-opt and 3 percent for 3-opt. These are measured values, not bounds.

## Correctness

**Theorem.** Each LK step gives a Hamiltonian path whose cost is the tour cost minus $G$, the search stops, and the loop ends at a tour on which no search gains. If the candidate lists hold all cities and the first step tries all choices, the result is 2-optimal, so for metric costs ALG $\le 2\sqrt{2} \sum_{i=1}^{n} 1/\sqrt{i} \cdot$ OPT $< 4\sqrt{2}\,\sqrt{n} \cdot$ OPT.

The proof has three steps.

1. **Steps are exact.** Removing $\{z, w\}$ and adding $\{y, z\}$ turns a path into a path, and the cost changes by exactly the gain terms.
2. **Finite search.** Every removed edge is an old tour edge and none is removed twice, so a chain has fewer than $n$ steps. Each accepted search makes the tour strictly shorter.
3. **2-optimality.** For a 2-opt move with gain $g > 0$ there are two LK searches that find it in one step, and their first partial gains add up to $g$. So one of them passes the gain criterion.

The full proof is in the proof file.

**Lower bounds.** With full lists the bounds of [2-opt](/two-opt/) apply from above. No worst-case ratio is proved here for short candidate lists. Papadimitriou (1992) showed that finding a local optimum for a version of LK is PLS-complete, so no polynomial bound on the number of improvements is expected.

**Hardness.** No polynomial algorithm has a ratio below $123/122$ for metric TSP unless P = NP (Karpinski, Lampis and Schmied 2015; see [metric TSP inapproximability](/metric-tsp-inapproximability/)). Without the triangle inequality no constant ratio is possible unless P = NP ([general TSP inapproximability](/general-tsp-inapproximability/)).

## Complexity

- **One step.** $O(k)$ candidates, each tested in $O(1)$, plus the reversal of a part of the path. The reversal is $O(n)$ in an array, $O(\sqrt{n})$ with two-level doubly linked lists, and $O(\log n)$ amortized with a [splay tree](/splay-tree/).
- **One search.** With breadth 5, 3 and then 1, a search makes at most $15$ chains of fewer than $n$ steps each, so it costs $O(n(k + n))$ time.
- **Number of improvements.** Not bounded by a polynomial on this page; see the PLS result above.
- **Space.** $\Theta(n)$ for the tour and the tabu sets, and $\Theta(nk)$ for the candidate lists.

## Properties

- **Variable depth.** One search can make a $k$-opt move for any $k$, chosen by the data, not fixed in advance.
- **Gain criterion.** The test is on the partial sum $G$, not on the closed tour, so a step that makes the closed tour longer is allowed while $G > 0$.
- **Sequential moves only.** Each step shares a city with the one before it. Moves such as the double bridge, which is a non-sequential 4-opt move, are out of reach. This is why [chained LK](/iterated-local-search/) uses the double bridge as its kick.
- **Contains 2-opt.** With full lists the one-step searches cover all 2-opt moves; see the theorem.

## Variants and improvements

- **The original rules.** Lin and Kernighan (1973) also allow a special alternative choice at the second step and a lookahead rule. This implementation keeps only the standard step and the lookahead.
- **Don't-look bits.** Skip start cities near which nothing changed. With neighbor lists this makes LK run in about $O(n \log n)$ time per run in practice, a measured value.
- **Chained LK.** Apply a random double-bridge kick to the LK tour, run LK again and keep the better tour. This is [iterated local search](/iterated-local-search/) with LK inside, due to Martin, Otto and Felten (1991).
- **[LKH](/lin-kernighan-helsgaun/).** Helsgaun (2000) uses 5-opt basic steps and candidate lists from alpha-nearness, and gets tours much closer to OPT.
- **Graph partitioning.** The same variable-depth idea is the [Kernighan-Lin](/kernighan-lin/) algorithm for graph bisection.

## When to use it

Use LK, or better a chained LK or LKH code, when you need tours within a few percent of OPT or better on large instances and an exact solver is too slow. For a quick result on small instances, [2-opt](/two-opt/) with [Or-opt](/or-opt/) is simpler. When you need a proved ratio, use [Christofides](/christofides-algorithm/) for metric costs.

## Pitfalls

- **Testing the closed tour instead of $G$.** The search must go on when the closed tour is worse but $G > 0$. Stopping there gives only 2-opt.
- **The wrong $w$.** The removed edge must be the one from $z$ to its neighbor on the side of the free end. The other neighbor does not give a path.
- **Missing tabu rules.** Without them the search can undo its own steps and the depth is not bounded.
- **Both tour edges of $t_1$.** A search from $t_1$ must try both of its tour edges as the first removed edge, or some moves are never found.
- **Short candidate lists.** They give speed, but the proved 2-optimality needs full lists. With short lists the result can have a gaining 2-opt move.
- **Array reversals.** On large instances the $O(n)$ reversal dominates; use a better tour data structure.

## Implementations

## History

Kernighan and Lin (1970) introduced variable-depth search for graph partitioning at Bell Labs. Lin had studied 3-opt in 1965. Lin and Kernighan (1973) applied the idea to the TSP and found optimal tours of their test instances of up to 110 cities in most runs. Johnson and McGeoch (1997) gave a careful implementation and study. Martin, Otto and Felten (1991) added the double-bridge kick, which gave chained LK, and Applegate, Cook and Rohe (2003) made chained LK fast for very large instances. Papadimitriou (1992) proved that a version of the LK local search is PLS-complete. Helsgaun (2000) gave [LKH](/lin-kernighan-helsgaun/).

## References
