---
tag: WJY5MZ
kind: algorithm
slug: or-opt
name: Or-opt
aliases:
- Or-2opt
- Or-opt local search
- segment insertion
area: approximation/tsp-approximation
level: core
summary: Moves a run of 1, 2 or 3 consecutive cities to another place in the tour while this makes the tour shorter; a fast part of the 3-opt neighborhood.
solves: [metric-tsp]
model: real-ram
complexity:
  vars: {n: the number of cities}
  time: {pass: Θ(n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1976
  people: [Ilhan Or]
  note: Or (1976) proposed moving short segments of the tour in his thesis on routing for regional blood banking.
prereqs: [three-opt, two-opt, local-search, neighborhood-structure]
see_also: [three-opt, two-opt, lin-kernighan, cheapest-insertion, iterated-local-search, local-optimum]
sources:
  - title: Ilhan Or, Traveling salesman-type combinatorial problems and their relation to the logistics of regional blood banking, PhD thesis, Northwestern University, 1976
    locator: the segment insertion procedure (segments of 3, 2 and 1 cities)
  - title: Gilbert Babin, Stéphanie Deneault and Gilbert Laporte, Improvements to the Or-opt heuristic for the symmetric travelling salesman problem, Journal of the Operational Research Society 58(3), 2007
    locator: pages 402 to 407 (the move, its variants and measured results)
  - title: David S. Johnson and Lyle A. McGeoch, The traveling salesman problem, a case study in local optimization, in Aarts and Lenstra (eds.), Local Search in Combinatorial Optimization, Wiley, 1997
    locator: Section 3 (Or-opt as a part of 3-opt)
---

Or-opt is a [local search](/local-search/) for the [TSP](/metric-tsp/) that moves a short run of the tour. It takes 1, 2 or 3 consecutive cities out of the tour, joins the two cities that were next to them, and puts the run between two other neighbors, in the old direction or reversed. It repeats while some such move makes the tour shorter. Each move changes three edges, so it is a [3-opt](/three-opt/) move, but there are only $\Theta(n^2)$ of them instead of $\Theta(n^3)$. In practice Or-opt gets most of the gain of 3-opt, and it is often used together with [2-opt](/two-opt/), a combination called Or-2opt.

## In plain words

Look at a few cities in a row on the tour, at most three. Maybe they would fit better somewhere else.

Take them out, and join the two cities on each side. Then put the little group between two other cities that are next to each other on the tour, the right way round or turned. If the trip is now shorter, keep the change.

Repeat until no small group fits better anywhere. This is the [cheapest insertion](/cheapest-insertion/) idea applied again and again to a finished tour.

## The problem

The input is a set $V$ of $n$ cities with costs $d(u, v) = d(v, u) \ge 0$ and a start tour. The output is an Or-optimal tour: no Or-opt move makes it shorter. OPT is the least cost of a tour and ALG is the cost of the returned tour. The convention is ALG $\le \rho \cdot$ OPT for a minimization problem. This page proves no ratio for Or-optimal tours; the ratio results are measured.

## The algorithm

A move takes a segment $S = s_1, \ldots, s_L$ with $L \le 3$, with the tour neighbors $p$ before and $q$ after it, and a tour edge $\{u, v\}$ that does not touch $S$. Its gain is

$$g = d(p, s_1) + d(s_L, q) + d(u, v) - d(p, q) - d(u, h) - d(t, v),$$

where $(h, t) = (s_1, s_L)$, or $(s_L, s_1)$ for the reversed segment.

```pseudo id=main
OR-OPT(d, T)
L1  repeat
L2      for each segment S of 1, 2 or 3 cities, each edge {u, v} away from S, and each direction do
L3          if the gain g of moving S between u and v is positive then
L4              move S; go to L1
L5  until no move gains; return T
```

The implementation takes the first move that gains, in a fixed order, and accepts it only if $g > 10^{-12}$.

## Example

Take the seven cities of the [3-opt](/three-opt/) page, $A(1,2)$, $B(0,5)$, $C(3,3)$, $D(1,0)$, $E(0,0)$, $F(3,4)$ and $G(2,6)$, with the Euclidean distance, and the tour $A\,C\,F\,G\,B\,E\,D$ of length 15.708. It is 2-optimal.

Move the segment $S = E\,D$, with $p = B$ and $q = A$, between $u = A$ and $v = C$, in the old direction.

| | edges | cost |
|---|---|---|
| removed | $BE$, $DA$, $AC$ | $5 + 2 + \sqrt{5} = 9.236$ |
| added | $BA$, $AE$, $DC$ | $\sqrt{10} + \sqrt{5} + \sqrt{13} = 9.004$ |

The gain is 0.232. The new tour $A\,E\,D\,C\,F\,G\,B$ has length 15.476, which is OPT. This is the same tour change as the pure 3-opt move of the 3-opt page.

**Measured behavior.** On 300 seeded instances of 10 uniform random points in the unit square, with OPT from the Held-Karp program, Or-opt from a random tour gave tours 0.06 percent above OPT on average, at most 1.055 times OPT, and the optimum in 287 cases, with 13.3 moves on average. Adding 2-opt moves did not change these results on these small instances. 2-opt alone gave 1.05 percent, and full 3-opt gave 0.04 percent. These are measured values, not bounds.

## Correctness

**Theorem.** The Or-opt search stops at an Or-optimal tour. Each Or-opt move is a 3-opt move, so every 3-optimal tour is Or-optimal.

The proof has three steps.

1. **A move gives a tour.** Taking $S$ out and joining $p$ to $q$ leaves a cycle on the other cities that still holds $\{u, v\}$. Putting $S$ into that edge gives a tour, and the cost goes down by $g$.
2. **Inside 3-opt.** The move removes three tour edges and adds three, so it joins the same three paths in a new way, which is a 3-opt move.
3. **Termination.** Each accepted move makes the tour strictly shorter, and there are finitely many tours.

The full proof is in the proof file.

**No ratio for Or-opt alone.** An Or-optimal tour need not be 2-optimal. The test file holds 16 points in two rows, $(x, 10)$ and $(x, 0)$ for $x = 0, \ldots, 7$, and the tour that runs along the top row, crosses to the bottom left, runs along the bottom row and crosses back. It costs 38.413 against OPT 34, its two diagonals cross, and no Or-opt move gains. So the $O(\sqrt{n})$ bound for [2-optimal tours](/two-opt/) does not transfer to Or-opt. A tour that is both Or-optimal and 2-optimal does satisfy that bound, since the proof uses only 2-optimality. That is one reason to use Or-opt with 2-opt.

**Hardness.** No polynomial algorithm has a ratio below $123/122$ for metric TSP unless P = NP (Karpinski, Lampis and Schmied 2015; see [metric TSP inapproximability](/metric-tsp-inapproximability/)). Without the triangle inequality no constant ratio is possible unless P = NP ([general TSP inapproximability](/general-tsp-inapproximability/)).

## Complexity

- **One pass.** There are $3n$ segments, about $n$ edges $\{u, v\}$ for each, and 2 directions, so a pass without a move tests $\Theta(n^2)$ moves at $O(1)$ each.
- **One move.** $O(n)$ in an array, $O(1)$ in a [doubly linked list](/doubly-linked-list/) when only the position matters and the segment is short.
- **Neighbor lists.** Try only edges $\{u, v\}$ where $u$ or $v$ is among the $k$ nearest cities of an end of $S$. A pass then costs $O(nk)$.
- **Number of moves.** Not bounded on this page. With integer costs up to $W$, at most $nW$ moves.

## Properties

- **A subset of 3-opt.** The move is the 3-opt form that moves one piece, with pieces of at most 3 cities.
- **Short reversals only.** Only the segment itself can be reversed, so on asymmetric costs the move without reversal keeps all directions. This makes Or-opt useful for the [asymmetric TSP](/asymmetric-tsp/) and for routes with time windows.
- **Not the same as 2-opt.** The example is 2-optimal but not Or-optimal, and the two-row tour is Or-optimal but not 2-optimal.

## Variants and improvements

- **Or-2opt.** Alternate Or-opt and 2-opt until neither gains. The result is 2-optimal, so the 2-opt bound holds.
- **Longer segments.** Segments of up to $k$ cities give a larger part of 3-opt at the cost $\Theta(kn^2)$ per pass.
- **Babin, Deneault and Laporte (2007).** Better scan orders and the reversed insertion, with measured gains.
- **Vehicle routing.** The same move between routes, or inside a route, is a standard move for routing problems; see [Clarke-Wright savings](/clarke-wright-savings/) for a start solution.
- **[3-opt](/three-opt/) and [Lin-Kernighan](/lin-kernighan/).** Larger neighborhoods that contain all Or-opt moves.

## When to use it

Use Or-opt with 2-opt as a quick improvement of a construction tour, in particular when costs are asymmetric or when the routes have side conditions such as time windows, where long reversals are a problem. When you need better tours, use [Lin-Kernighan](/lin-kernighan/).

## Pitfalls

- **Inserting next to the segment.** The edge $\{u, v\}$ must not touch $S$. The edge $\{p, s_1\}$ is the old place of the segment, and inserting there gives the same tour or a 2-opt move, not an Or-opt move.
- **The edge $\{p, q\}$ in the gain.** The gain must subtract the new edge $d(p, q)$. Code that forgets it overestimates the gain.
- **Small $n$.** A segment of $L$ cities needs $n \ge L + 3$, so that the rest of the tour is a cycle with an edge away from the segment.
- **Expecting a ratio.** Or-opt alone has no proved worst-case ratio here, and its tours can have crossings.

## Implementations

## History

Or (1976) proposed the move in his PhD thesis at Northwestern University on the logistics of regional blood banking, as a cheap part of 3-opt. It moved segments of 3, then 2, then 1 cities. Johnson and McGeoch (1997) and many routing codes use it with 2-opt. Babin, Deneault and Laporte (2007) studied faster forms of the scan.

## References
