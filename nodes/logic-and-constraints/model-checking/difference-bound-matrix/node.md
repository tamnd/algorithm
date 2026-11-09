---
tag: 0E95QY
kind: data-structure
slug: difference-bound-matrix
name: Difference bound matrix
aliases:
- DBM
- Zone
- Clock zone
area: logic-and-constraints/model-checking
level: advanced
summary: A matrix of bounds on clock differences that stores a convex clock zone. Its canonical form is all-pairs shortest paths, computed by Floyd-Warshall in O(n^3).
model: word-ram
complexity:
  vars: {n: the number of clocks}
  time: {worst: Θ(n^3)}
  space: {extra: Θ(n^2)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [timed-automata, floyd-warshall, difference-constraints]
see_also: [region-graph, negative-cycle-detection, bellman-ford, abstract-interpretation, symbolic-reachability, state-explosion-problem, hybrid-automata, all-pairs-shortest-paths]
sources:
  - paper: "David L. Dill, Timing assumptions and verification of finite-state concurrent systems, Automatic Verification Methods for Finite State Systems 1989, Lecture Notes in Computer Science 407, Springer, 1990, pages 197 to 212"
    title: Timing assumptions and verification of finite-state concurrent systems
    locator: the representation of clock zones by matrices of difference bounds and their use in state-space search
  - paper: "Johan Bengtsson and Wang Yi, Timed automata: semantics, algorithms and tools, Lectures on Concurrency and Petri Nets, Lecture Notes in Computer Science 3098, Springer, 2004, pages 87 to 124"
    title: "Timed automata: semantics, algorithms and tools"
    locator: DBMs, the canonical form, the operations up, reset, constrain and inclusion, the incremental closure after one constraint, and k-normalization
  - paper: "Patricia Bouyer, Forward analysis of updatable timed automata, Formal Methods in System Design 24(3), 2004, pages 281 to 320"
    title: Forward analysis of updatable timed automata
    locator: the correctness of the extrapolation operator for diagonal-free timed automata, and its failure with diagonal constraints
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 9 (timed automata, clock constraints and clock regions)
  - paper: doi:10.1016/0304-3975(94)90010-8
    title: Rajeev Alur and David L. Dill, A theory of timed automata, Theoretical Computer Science 126(2), 1994, pages 183 to 235
    locator: clock constraints, regions and the decidability of reachability, against which zone-based search is proved correct
---

A *difference bound matrix* (DBM) stores a *zone*: a convex set of clock valuations of a [timed automaton](/timed-automata/), given by constraints $x_i - x_j \prec c$ with $\prec \in \{<, \le\}$. With $n$ clocks and a reference clock $x_0$ that is always 0, it is an $(n+1) \times (n+1)$ matrix, and entry $(i, j)$ is the bound on $x_i - x_j$. The constraints form a weighted graph. The zone is empty exactly when the graph has a negative cycle. The tightest form of the matrix, called the *canonical form*, is the all-pairs shortest path matrix. [Floyd-Warshall](/floyd-warshall/) computes it in $O(n^3)$ time. On canonical DBMs, letting time pass, resetting a clock, adding a guard and testing inclusion are simple matrix operations. With an *extrapolation* step that forgets bounds above the largest constants, a forward search over zones terminates. For diagonal-free automata it decides reachability exactly, as Bouyer proved in 2004. Dill introduced DBMs in 1989, and tools such as UPPAAL use them as their main data structure.

## In plain words

A timed automaton has clocks that move together. A set of clock settings that can occur at some point is often a simple shape. It can be described by rules of the form "clock x minus clock y is at most 3". A table with one row and one column per clock holds one such rule per cell, plus a cell for each clock alone. Many tables describe the same set, because some rules follow from others. If you replace each rule with the tightest rule that follows from the table, you get one standard table per set. This is the same work as finding the shortest routes between all pairs of points in a road map. With the standard table it is easy to let time pass, to set a clock to zero, to add a test, and to check whether one set lies inside another.

## The abstract type

A *bound* is a pair $(c, \prec)$ with $c \in \mathbb{Z} \cup \{\infty\}$ and $\prec \in \{<, \le\}$. Bounds are ordered by $c$ first, and $(c, <)$ is smaller than $(c, \le)$. They are added by $(c, \prec) + (d, \prec') = (c + d, \prec'')$, where $\prec''$ is $\le$ only when both are $\le$. A DBM is a matrix $D = (D_{ij})_{0 \le i, j \le n}$ of bounds. It stands for the zone

$$[\![D]\!] = \{\, v \in \mathbb{R}_{\ge 0}^n : v_i - v_j \prec_{ij} c_{ij} \text{ for all } i, j \,\}, \qquad v_0 = 0,$$

where $D_{ij} = (c_{ij}, \prec_{ij})$. Entry $D_{i0}$ is an upper bound on $x_i$, and $D_{0j}$ is a lower bound on $x_j$ with the sign reversed. The operations are:

- **canonical**$(D)$: the tightest equivalent matrix, or *empty*;
- **up**$(D)$: the zone $\{v + t : v \in [\![D]\!], t \ge 0\}$;
- **reset**$(D, x)$: the zone $\{v[x := 0] : v \in [\![D]\!]\}$;
- **constrain**$(D, x_i - x_j \prec c)$: the intersection with one constraint, as used for guards and invariants;
- **includes**$(D, E)$: whether $[\![E]\!] \subseteq [\![D]\!]$;
- **extrapolate**$(D, k)$: a larger zone that only remembers bounds up to the constants $k$.

## Representation

The matrix is stored as $(n+1)^2$ bounds. A bound fits in one machine word: encode $(c, \le)$ as $2c + 1$, $(c, <)$ as $2c$, and $\infty$ as a large value. Then the order of bounds is the integer order. Addition is done on the halves, with the strictness bit kept only when both bits are 1. Read the matrix as a graph with nodes $0, \ldots, n$ and an edge from $j$ to $i$ with weight $D_{ij}$. A path of weights $D_{i k_1}, D_{k_1 k_2}, \ldots$ adds the constraints along it, so its total weight bounds $x_i - x_j$.

A DBM is *canonical* when $D_{ij} \le D_{ik} + D_{kj}$ for all $i, j, k$. For a nonempty zone, the canonical DBM is unique, and each entry is the tightest bound that holds on the zone. Every operation below takes and returns canonical DBMs, except where it says otherwise.

## Operations

```pseudo id=main
CANONICAL(D)            ▷ D is (n + 1) × (n + 1); index 0 is the clock that is always 0
L1  for k ← 0 to n do
L2      for i ← 0 to n do
L3          for j ← 0 to n do
L4              if D[i][k] + D[k][j] < D[i][j] then
L5                  D[i][j] ← D[i][k] + D[k][j]
L6  for i ← 0 to n do
L7      if D[i][i] < (0, ≤) then return empty      ▷ a negative cycle: no valuation fits
L8  return D
```

```pseudo id=ops
UP(D)
U1  for i ← 1 to n do D[i][0] ← ∞     ▷ no upper bounds; differences are unchanged

RESET(D, x)
R1  for j ← 0 to n do D[x][j] ← D[0][j], D[j][x] ← D[j][0]
R2  D[x][x] ← (0, ≤)

TIGHTEN(D, i, j, b)        ▷ add x_i − x_j ≺ b; O(n^2) time
T1  if D[j][i] + b < (0, ≤) then return empty
T2  if b < D[i][j] then
T3      D[i][j] ← b
T4      for p ← 0 to n do for q ← 0 to n do
T5          D[p][q] ← min(D[p][q], D[p][i] + b + D[j][q])

INCLUDES(D, E)            ▷ is [[E]] ⊆ [[D]]?
I1  return E[i][j] ≤ D[i][j] for all i, j

EXTRAPOLATE(D, k)          ▷ k[0] = 0, k[x] the largest constant of x
E1  for each i ≠ j do
E2      if D[i][j] > (k[i], ≤) then D[i][j] ← ∞
E3      else if D[i][j] < (−k[j], <) then D[i][j] ← (−k[j], <)
E4  return CANONICAL(D)
```

CANONICAL is Floyd-Warshall on the bound arithmetic. The lines L6 and L7 are the usual [negative cycle detection](/negative-cycle-detection/). UP drops the upper bounds of each clock. RESET copies row 0 and column 0 into the row and column of $x$, because $x$ now equals the reference clock. Both keep canonical form. TIGHTEN adds one constraint in $O(n^2)$ time. A new shortest path uses the new edge at most once, so line T5 is enough. A guard $x \le c$ is TIGHTEN$(D, x, 0, (c, \le))$, and a guard $x > c$ is TIGHTEN$(D, 0, x, (-c, <))$. EXTRAPOLATE, also called $\mathrm{Extra}_M$ or $k$-normalization, removes upper bounds above $k[i]$. It also weakens lower bounds below $-k[j]$ to "$x_j > k[j]$", and then restores canonical form.

A forward search keeps a list of zones for each location. From a zone $Z$ in location $\ell$ and an edge with guard $g$, resets $Y$ and target $\ell'$, it computes this zone:

$$\mathrm{extrapolate}\big(\mathrm{up}(\mathrm{reset}(Z \wedge g, Y) \wedge \mathrm{Inv}(\ell')) \wedge \mathrm{Inv}(\ell')\big).$$

It drops the new zone if an old zone of $\ell'$ includes it.

## Example

Take clocks $x = x_1$ and $y = x_2$, and the zone $1 \le x \le 3$, $0 \le y \le 2$, $x - y \le 2$. Write $\le c$ for $(c, \le)$ and $< c$ for $(c, <)$. The input matrix and its canonical form are below. Rows are $x_0, x, y$, and entry $(i, j)$ bounds $x_i - x_j$.

| Input | $x_0$ | $x$ | $y$ |
|---|---|---|---|
| $x_0$ | $\le 0$ | $\le -1$ | $\le 0$ |
| $x$ | $\le 3$ | $\le 0$ | $\le 2$ |
| $y$ | $\le 2$ | $\infty$ | $\le 0$ |

Only one entry changes. The path $y \to x_0 \to x$ gives $y - x \le 2 + (-1) = 1$, so $D_{yx}$ becomes $\le 1$. All other entries are already the shortest. No diagonal entry is negative, so the zone is not empty.

Now add the guard $y < 1$ with TIGHTEN$(D, y, 0, < 1)$. Line T1 checks $D_{0y} + (<1) = (<1) \ge (\le 0)$, so the zone stays nonempty. Line T5 then finds two tighter entries:

- $D_{x0} = \min(\le 3, D_{xy} + (<1)) = \min(\le 3, <3) = (<3)$, since $x - y \le 2$ and $y < 1$ give $x < 3$;
- $D_{yx} = \min(\le 1, (<1) + D_{0x}) = \min(\le 1, <0) = (<0)$, since $y < 1$ and $x \ge 1$ give $y - x < 0$.

Adding $x - y \ge 3$ instead, as TIGHTEN$(D, y, x, \le -3)$, fails at line T1: $D_{xy} + (\le -3) = (\le -1) < (\le 0)$. The cycle $x \to y \to x$ is negative, because $x - y \le 2$ and $x - y \ge 3$ cannot both hold.

Last, apply UP, and then EXTRAPOLATE with $k = (0, 1, 1)$. UP sets $D_{x0} = D_{y0} = \infty$. Extrapolation sees $D_{xy} = \le 2 > (\le 1)$ and replaces it with $\infty$. It keeps $D_{0x} = \le -1$, since $x \ge 1$ is not below $x > 1$. The result is the zone $x \ge 1$, $y - x < 0$. The zone grew: it now also has points with $x - y > 2$, such as $x = 3.5$, $y = 1$. Each new point is region equivalent to a point of the exact zone, here $x = 2.5$, $y = 1$. So with constants at most 1, no guard can tell the two zones apart.

## Correctness

The proof file shows these facts:

- **CANONICAL.** Each entry after CANONICAL is the weight of some walk in the constraint graph, and it is at most the weight of every path. So the zone does not change. A negative diagonal entry shows a negative cycle, which means the zone is empty. If there is no negative cycle, the zone is nonempty. The proof builds a point from shortest path potentials, with a small slack for strict bounds, as in the theory of [difference constraints](/difference-constraints/).
- **Tightness and inclusion.** In a canonical nonempty DBM, each finite entry is reached or approached by points of the zone. So inclusion is the entrywise order.
- **UP, RESET and TIGHTEN.** These compute their zones and keep canonical form.
- **EXTRAPOLATE.** It only grows a zone, so a search with it never misses a reachable state. Each extrapolated canonical entry is $\infty$ or a bound with $|c| \le \max_x k[x]$, so there are finitely many such DBMs, and the search ends.

The last claim is that extrapolation adds no false reachable locations. For diagonal-free automata, Bouyer proved that $\mathrm{Extra}_M(Z)$ lies inside the union of the regions that meet $Z$. Regions form a time-abstract bisimulation (see the [region graph](/region-graph/)), so every location reached from the larger zone is also reached from $Z$. The proof file states this result and gives its outline.

## Complexity

- **CANONICAL:** $\Theta(n^3)$ time.
- **TIGHTEN:** $O(n^2)$ time. A guard with $m$ atomic constraints costs $O(m n^2)$.
- **UP:** $O(n)$ time.
- **RESET:** $O(n)$ time per clock.
- **INCLUDES:** $O(n^2)$ time.
- **EXTRAPOLATE:** $O(n^3)$ time, because of the closure at the end.
- **Space:** $\Theta(n^2)$ bounds per zone.

The number of zones a search stores can still be exponential. In the worst case it can be as large as the number of regions, but in practice it is usually much smaller.

## Variants

- **LU extrapolation.** Behrmann, Bouyer, Larsen and Pelánek use separate maximal lower-bound and upper-bound constants. This gives coarser zones that are still exact for diagonal-free automata.
- **Minimal constraint form.** Larsen, Larsson, Pettersson and Yi store only the edges that are not implied by others. This saves memory in the passed list.
- **Federations.** A federation is a union of DBMs, used to represent non-convex sets and to subtract zones.
- **Octagons.** Miné's octagon domain for [abstract interpretation](/abstract-interpretation/) uses the same closure on constraints $\pm x \pm y \le c$.
- **Diagonal constraints.** With guards $x - y \sim c$, the plain $\mathrm{Extra}_M$ can claim that unreachable locations are reachable. Bouyer showed this, and later work splits zones along the diagonal constraints to restore exactness.
- **Hybrid systems.** For [hybrid automata](/hybrid-automata/) with general linear flows, zones are replaced by convex polyhedra, and termination is lost.

## When to use it

Use DBMs to represent sets of clock valuations in any search over a timed automaton: reachability, [safety properties](/safety-property/), and Büchi conditions with zone-based nested search. They are much smaller than the [region graph](/region-graph/) in practice, and every operation is a short matrix loop. Use the region graph instead to prove decidability or to test a zone implementation, as the tests here do. For constraints on sums of clocks, or for clocks with different rates, DBMs cannot represent the sets. Use polyhedra there, and accept that reachability may not terminate.

## Pitfalls

- **Comparing non-canonical matrices.** Two different matrices can describe the same zone. Inclusion and equality tests are only correct on canonical forms.
- **Ignoring strictness.** Treating $<$ as $\le$ loses emptiness. For example, $x < 1$ together with $x > 1$ is empty, but $x \le 1$ together with $x \ge 1$ is not.
- **Forgetting to close after extrapolation.** EXTRAPOLATE changes single entries, so the result is in general not canonical. A later inclusion test would then be wrong.
- **Extrapolating with diagonal guards.** The standard extrapolation is wrong for automata with $x - y \sim c$ guards. It can report unreachable locations as reachable.
- **Overflow with infinity.** With the integer encoding, $\infty + \infty$ and $\infty + c$ must stay $\infty$.

## Implementations

## History

Dill proposed in 1989 to represent sets of clock values by matrices of difference bounds. The canonical form is the all-pairs shortest path matrix that the algorithm of Floyd and Warshall computes. Alur and Dill's 1994 paper on timed automata made regions the reference semantics. The tools Kronos and UPPAAL, built in the 1990s, made zones and DBMs the standard in practice. Bengtsson and Yi's 2004 tutorial is the usual reference for the operations. Bouyer's 2004 paper settled when extrapolation is exact: it is exact for diagonal-free automata, and it can fail with diagonal constraints.

## References
