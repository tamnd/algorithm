---
tag: ADCC0B
kind: algorithm
slug: three-opt
name: 3-opt
aliases:
- 3-opt local search
area: approximation/tsp-approximation
level: core
summary: Removes three edges of the tour and reconnects the three paths in a shorter way while one exists; better tours than 2-opt, Θ(n^3) moves to test in each pass.
solves: [metric-tsp]
model: real-ram
complexity:
  vars: {n: the number of cities}
  time: {pass: Θ(n^3)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1965
  people: [Shen Lin, Barun Chandra, Howard Karloff, Craig Tovey]
  note: Lin (1965) introduced the 3-opt moves and the notion of a k-optimal tour; Chandra, Karloff and Tovey (1999) bounded the ratio of k-optimal tours.
prereqs: [two-opt, local-search, neighborhood-structure, local-optimum]
see_also: [or-opt, lin-kernighan, lin-kernighan-helsgaun, iterated-local-search, hill-climbing, pls]
sources:
  - paper: doi:10.1002/j.1538-7305.1965.tb04146.x
    title: Shen Lin, Computer solutions of the traveling salesman problem, Bell System Technical Journal 44(10), 1965
    locator: pages 2245 to 2269 (k-optimal tours, the 3-opt moves and the measured results)
  - paper: doi:10.1137/S0097539793251244
    title: Barun Chandra, Howard Karloff and Craig Tovey, New results on the old k-opt algorithm for the traveling salesman problem, SIAM Journal on Computing 28(6), 1999
    locator: pages 1998 to 2029 (the lower bound (1/4) n^(1/(2k)) for k-optimal tours)
  - title: David S. Johnson and Lyle A. McGeoch, The traveling salesman problem, a case study in local optimization, in Aarts and Lenstra (eds.), Local Search in Combinatorial Optimization, Wiley, 1997
    locator: Section 3 (3-opt with neighbor lists, results on random uniform instances)
---

3-opt is a [local search](/local-search/) for the [metric TSP](/metric-tsp/). A move removes three edges of the tour, which cuts it into three paths, and joins the paths again in another way. The search makes moves that shorten the tour until no move does. The result is a 3-optimal tour. Each 3-optimal tour is also [2-optimal](/two-opt/), so it is within $O(\sqrt{n})$ of OPT on metric instances, and its tours are better than those of 2-opt in practice. The price is the size of the [neighborhood](/neighborhood-structure/): $\Theta(n^3)$ moves instead of $\Theta(n^2)$.

## In plain words

Cut the tour in three places. Now you have three pieces of trip. Keep one piece where it is, and put the other two pieces back in another order, or turn one of them around, or both.

There are seven new ways to do this. Three of them are only the 2-opt repair, where one cut is put back. The other four are new: they can move a whole piece to another place in the trip, which 2-opt cannot do in one step.

Repeat while one of these changes makes the trip shorter.

## The problem

The input is a set $V$ of $n$ cities with costs $d(u, v) = d(v, u) \ge 0$ that satisfy the [triangle inequality](/triangle-inequality/), and a start tour. The output is a 3-optimal tour: no 3-opt move makes it shorter. OPT is the least cost of a tour and ALG is the cost of the returned tour. The convention is ALG $\le \rho \cdot$ OPT for a minimization problem. The bound holds in the worst case for each 3-optimal tour.

## The algorithm

For positions $i < j < k$ of the tour array $T$, let $a = T[i]$, $X = T[i+1..j]$, $Y = T[j+1..k]$, and $f = T[k+1]$, modulo $n$. A move writes the tour again as $a$, then $X$ and $Y$ in one of 7 new forms, then $f$ and the rest. With $\bar X$ for $X$ reversed, the 7 forms are $\bar X Y$, $X \bar Y$, $\bar Y \bar X$ (three 2-opt moves) and $\bar X \bar Y$, $Y X$, $Y \bar X$, $\bar Y X$ (four pure 3-opt moves).

```pseudo id=main
THREE-OPT(d, T)
L1  repeat
L2      for each triple i < j < k of positions do
L3          for each of the 7 forms do
L4              if the three old joint edges cost more than the three new joint edges then
L5                  rewrite T in this form; go to L1
L6  until no triple and no form gains; return T
```

Line L4 compares six costs, so a test is $O(1)$. The implementation takes the first move that gains, in this scan order, and requires a gain above $10^{-12}$.

## Example

The six cities of the [2-opt](/two-opt/) page are too easy: their only 2-optimal tour is optimal. Take instead seven cities in the plane, $A(1,2)$, $B(0,5)$, $C(3,3)$, $D(1,0)$, $E(0,0)$, $F(3,4)$ and $G(2,6)$, with the Euclidean distance, and the tour $A\,C\,F\,G\,B\,E\,D$ of length 15.708. No 2-opt move improves it, so 2-opt stops here.

The 3-opt move with $a = A$, $X = C\,F\,G\,B$, $Y = E\,D$ and $f = A$ takes the form $Y X$:

| | edges | cost |
|---|---|---|
| removed | $AC$, $BE$, $DA$ | $\sqrt{5} + 5 + 2 = 9.236$ |
| added | $AE$, $DC$, $BA$ | $\sqrt{5} + \sqrt{13} + \sqrt{10} = 9.004$ |

The gain is 0.232, and the new tour $A\,E\,D\,C\,F\,G\,B$ has length 15.476, which is OPT. The move takes the piece $E\,D$ from the end of the tour and puts it between $A$ and $C$.

**Measured behavior.** On 300 seeded instances of 10 uniform random points in the unit square, with OPT from the Held-Karp program, 3-opt from a random tour gave tours 0.04 percent above OPT on average, at most 1.025 times OPT, and the optimum in 292 cases. 2-opt on the same starts gave 1.05 percent, at most 1.212, and the optimum in 203 cases. On large random uniform instances, Johnson and McGeoch (1997) report 3-opt tours about 3 percent above the Held-Karp bound, against about 5 percent for 2-opt. These are measured values, not bounds.

## Correctness

The search stops, because each move makes the tour strictly shorter and there are finitely many tours.

**Theorem.** For metric costs, every 3-optimal tour satisfies

$$\text{ALG} \le 2\sqrt{2} \sum_{i=1}^{n} \frac{1}{\sqrt{i}} \cdot \text{OPT} < 4\sqrt{2}\,\sqrt{n} \cdot \text{OPT}.$$

The proof has three steps.

1. **The 8 forms.** After three cuts, the two pieces $X$ and $Y$ can come back in 2 orders and 4 directions. One of the 8 forms is the old tour. Three keep one old edge and are 2-opt moves, and four use three new edges.
2. **2-opt is inside 3-opt.** Each 2-opt move is one of the three forms, for a suitable triple, so a 3-optimal tour is 2-optimal.
3. **The 2-opt bound.** The bound for 2-optimal tours, proved on the [2-opt](/two-opt/) page, applies.

The full proof is in the proof file.

**Lower bound.** Chandra, Karloff and Tovey (1999) gave metric instances with $k$-optimal tours of ratio $\frac{1}{4} n^{1/(2k)}$, which is $\frac{1}{4} n^{1/6}$ for 3-opt. So 3-opt has no constant worst-case ratio. That result is quoted here, and the true order for 3-opt between $n^{1/6}$ and $\sqrt{n}$ is not settled on this page.

**Running time.** This page gives no bound on the number of moves. Krentel (1989) showed that for some fixed large $k$, finding a $k$-optimal tour is [PLS](/pls/)-complete, and the 2-opt search can take exponentially many moves (see [2-opt](/two-opt/)).

**Hardness.** No polynomial algorithm has a ratio below $123/122$ for metric TSP unless P = NP (Karpinski, Lampis and Schmied 2015; see [metric TSP inapproximability](/metric-tsp-inapproximability/)). Without the triangle inequality no constant ratio is possible unless P = NP ([general TSP inapproximability](/general-tsp-inapproximability/)).

## Complexity

- **One pass.** There are $\binom{n}{3}$ triples and 7 forms, so a pass without a move costs $\Theta(n^3)$.
- **One move.** Rewriting the array costs $O(n)$.
- **Neighbor lists.** With $k$ nearest neighbors for each city, choose the first new edge from the list of $a$ and the second from the list of the city at the other end. A pass then tests $O(n k^2)$ moves. This is the form used in practice.
- **Space.** $\Theta(n)$ besides the costs.

## Properties

- **A larger neighborhood than 2-opt.** Each 3-optimal tour is 2-optimal, but not conversely, as the example shows.
- **Segment moves.** The form $Y X$ moves a piece of the tour to another place. With pieces of at most 3 cities this is [Or-opt](/or-opt/).
- **No direction change in $Y X$.** On asymmetric costs, the form $Y X$ keeps all directions, so it is the only pure 3-opt move that does not reverse a path. This is why it is used for the [asymmetric TSP](/asymmetric-tsp/).
- **Deterministic.** With a fixed scan order and a fixed start.

## Variants and improvements

- **Or-opt.** Only the form $Y X$ and $Y$ with at most 3 cities: $O(n^2)$ moves per pass and most of the gain of 3-opt.
- **Sequential 3-opt with the gain criterion.** Choose the new edges in order and keep the partial gain positive, as in [Lin-Kernighan](/lin-kernighan/). This prunes most triples.
- **$k$-opt for $k > 3$.** Better tours, $\Theta(n^k)$ moves per pass. [LKH](/lin-kernighan-helsgaun/) uses sequential 5-opt moves with good candidate lists.
- **Iterated 3-opt.** Restart from a perturbed tour, as in [iterated local search](/iterated-local-search/).

## When to use it

Use 3-opt with neighbor lists when 2-opt tours are not good enough and [Lin-Kernighan](/lin-kernighan/) is not available. On small instances, plain 3-opt is easy to code and often finds the optimum. On large instances, full 3-opt is too slow; use neighbor lists, Or-opt or Lin-Kernighan.

## Pitfalls

- **Only 2-opt moves.** Code that tries only the forms with reversed pieces misses $Y X$, the segment move.
- **Short pieces.** When a piece has one city, some forms are the same tour. This is harmless, but count moves with care.
- **The joint edges.** The gain counts only the three joints. If the triple includes the last position, $f$ is $T[0]$, and the edge from the last city to $T[0]$ is one of the three.
- **A cubic pass.** On 1000 cities a full pass tests more than $10^9$ moves.

## Implementations

## History

Lin (1965) defined $k$-optimal tours, studied 3-opt in detail and found that 3-optimal tours were often optimal on the test instances of that time. Lin and Kernighan (1973) then replaced the fixed $k$ by a variable depth search. Johnson and McGeoch (1997) measured 3-opt with neighbor lists and don't-look bits on large instances. Chandra, Karloff and Tovey (1999) proved the worst-case bounds for $k$-optimal tours.

## References
