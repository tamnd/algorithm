---
tag: J8K07F
kind: algorithm
slug: tsay-zero-skew
name: Tsay's exact zero-skew algorithm
aliases:
- exact zero skew clock routing
- exact zero skew
area: eda/timing-and-verification
level: core
summary: Tsay's bottom-up merge of subtrees that puts each tapping point where the Elmore delays to both sides are equal, so the whole tree has zero skew.
solves: [clock-tree-synthesis]
model: real-ram
complexity:
  vars: {n: the number of clock sinks}
  time: {given_topology: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true, exact: true}
history:
  year: 1991
  people: [Ren-Song Tsay]
  note: Tsay presented exact zero skew at ICCAD 1991, and the journal version appeared in IEEE Transactions on Computer-Aided Design in 1993.
prereqs: [elmore-delay, rc-tree, binary-tree]
see_also: [clock-tree-synthesis, deferred-merge-embedding, method-of-means-and-medians, h-tree-clock, rectilinear-steiner-tree-problem, van-ginneken-buffer-insertion, setup-and-hold-constraints, clock-skew-scheduling]
sources:
  - paper: doi:10.1109/43.205004
    title: Ren-Song Tsay, An exact zero-skew clock routing algorithm, IEEE Transactions on Computer-Aided Design 12(2), 242 to 249, 1993
    locator: the tapping point formula under the Elmore delay, the wire elongation when the point falls outside the segment, and the bottom-up merge
  - paper: "Ren-Song Tsay, Exact zero skew, Proceedings of ICCAD 1991, 336 to 339"
    locator: the conference version of the method
  - book: isbn:9789048195909
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, Springer, 2011
    locator: Chapter 7, Specialized Routing, Section 7.5.1, Constructing Trees with Zero Global Skew (exact zero skew)
  - paper: "Ting-Hai Chao, Yu-Chin Hsu, Jan-Ming Ho, Kenneth D. Boese and Andrew B. Kahng, Zero skew clock routing with minimum wirelength, IEEE Transactions on Circuits and Systems II 39(11), 799 to 814, 1992"
    locator: the comparison with deferred-merge embedding, which keeps zero skew and uses less wire for the same topology
---

Tsay's exact zero-skew algorithm is a clock routing algorithm: it builds a wire tree from a clock source to a set of sinks so that the [Elmore delay](/elmore-delay/) from the root to every sink is exactly the same. It works bottom up over a given binary topology. To join two subtrees whose own skew is already zero, it computes the one point on the wire between their roots where the delays to both sides are equal, from a closed formula. When that point falls outside the wire, it puts the tap at the end of the slower subtree and makes the wire to the faster one longer than the distance. Ren-Song Tsay published it in 1991.

## In plain words

A clock signal must reach every register at the same time. The clock wire forms a tree, and the delay to a register depends on the length of the wire and on the load that each piece of wire must charge.

Start with the registers as single points. Take two subtrees that the topology says to join. Each already has the same delay to all its own registers. Run a wire between their roots and find the point on it where the delay down to the left equals the delay down to the right. One formula gives this point. That point becomes the root of the joined subtree. If one side is much slower, even putting the point at its root is not enough, so the wire to the faster side is made longer, with a detour, until both match.

## The problem

The input is a set of $n$ sinks with points $p_s$ in the plane and load capacitances $c_s > 0$, a full binary tree (the *topology*) whose leaves are the sinks, and the wire resistance $r$ and capacitance $c$ per unit length. Wires run horizontally and vertically, and a wire of length $\ell$ is modeled as an [RC interconnect tree](/rc-tree/) edge in the pi model: a resistor $r \ell$ with $c \ell / 2$ at each end. The output is a point for each internal node of the topology and a wire length for each edge, such that the Elmore delay from the root to every sink is the same. This is the zero-skew case of [clock tree synthesis](/clock-tree-synthesis/).

Each subtree $A$ is summarized by its root point $p_A$, its total capacitance $C_A$ and its delay $t_A$ from $p_A$ to each of its sinks. Two subtrees $A$ and $B$ with $L = |x_A - x_B| + |y_A - y_B| > 0$ are merged at the *tapping point* at wire length $x L$ from $p_A$, where
$$ x = \frac{t_B - t_A + r L \,(C_B + c L / 2)}{r L \,(c L + C_A + C_B)}. $$

## The algorithm

```pseudo id=main
ZERO-SKEW(topology T, sinks, r, c)
L1  if T is a sink s then
L2      return subtree with point p_s, capacitance c_s, delay 0
L3  A ← ZERO-SKEW(left part of T);  B ← ZERO-SKEW(right part of T)
L4  L ← L1 distance from p_A to p_B
L5  x ← (t_B − t_A + r L (C_B + c L / 2)) / (r L (c L + C_A + C_B))
L6  if 0 ≤ x ≤ 1 then ℓ_A ← x L;  ℓ_B ← (1 − x) L;  p ← the point at length ℓ_A from p_A on a shortest path to p_B
L7  else if x < 0 then ℓ_A ← 0;  ℓ_B ← the root ℓ ≥ 0 of t_B + r ℓ (c ℓ / 2 + C_B) = t_A;  p ← p_A
L8  else ℓ_B ← 0;  ℓ_A ← the root ℓ ≥ 0 of t_A + r ℓ (c ℓ / 2 + C_A) = t_B;  p ← p_B
L9  return subtree with point p, capacitance C_A + C_B + c (ℓ_A + ℓ_B), delay t_A + r ℓ_A (c ℓ_A / 2 + C_A)
```

The root in line L7 is $\ell = (\sqrt{(r C_B)^2 + 2 r c (t_A - t_B)} - r C_B) / (r c)$ for $c > 0$. Lines L7 and L8 are the *wire elongation* cases: the wire is longer than the distance it spans, so it is routed with a detour. When $L = 0$ the two roots coincide, and the implementation goes to line L7 or L8 by comparing $t_A$ and $t_B$. The tapping point in line L6 is any point at those two distances; the implementation takes the path that runs horizontally first.

## Example

Take four sinks with $r = c = 1$: $s_1 = (5, 7)$ with load 3, $s_2 = (2, 0)$ with load 2, $s_3 = (6, 2)$ with load 1 and $s_4 = (6, 8)$ with load 2, and the topology $((s_1, s_2), (s_3, s_4))$.

| merge | $L$ | $x$ | $\ell_A$, $\ell_B$ | tapping point | $C$ | $t$ |
| --- | --- | --- | --- | --- | --- | --- |
| $s_1$ with $s_2$ | 10 | $70 / 150 = 7/15$ | $14/3$, $16/3$ | $(2, 16/3)$ | 15 | $224/9$ |
| $s_3$ with $s_4$ | 6 | $30 / 54 = 5/9$ | $10/3$, $8/3$ | $(6, 16/3)$ | 9 | $80/9$ |
| the two results | 4 | $28 / 112 = 1/4$ | $1$, $3$ | $(3, 16/3)$ | 28 | $727/18$ |

In the first merge the tap is closer to $s_1$, the sink with the larger load: from $s_1$ the delay is $\frac{14}{3}(\frac{7}{3} + 3) = \frac{224}{9}$, and from $s_2$ it is $\frac{16}{3}(\frac{8}{3} + 2) = \frac{224}{9}$. In the last merge the left subtree is slower ($224/9$ against $80/9$), so the tap moves toward it: $\frac{224}{9} + 1 \cdot (\frac{1}{2} + 15) = \frac{727}{18}$ and $\frac{80}{9} + 3 \cdot (\frac{3}{2} + 9) = \frac{727}{18}$. The Elmore delay from the root to each of the four sinks, summed as $\sum_k R_{ik} C_k$ over the whole pi model tree, is $727/18 \approx 40.39$. No merge needs elongation, and the total wire length is $10 + 6 + 4 = 20$.

An elongation case: a subtree with $C_A = 1$ and $t_A = 4$ at $(0, 0)$ and a sink with load $C_B = 1$ at $(1, 0)$, with $r = c = 1$. Then $x = (0 - 4 + 1.5) / 3 < 0$, so the tap is at $(0, 0)$ and the wire to the sink has length $\sqrt{1 + 8} - 1 = 2$, twice the distance. Its delay is $2 (1 + 1) = 4$, as needed.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). By the downstream form of the Elmore delay, a wire of length $\ell$ above a subtree whose skew is zero adds $r \ell (c \ell / 2 + C)$ to the delay of all its sinks, so the joined subtree has zero skew if and only if the two sides balance at the tap. The skew as a function of the tap position $s$ is $t_A - t_B - r L (C_B + c L / 2) + r s (c L + C_A + C_B)$: the quadratic terms cancel, so it is linear and strictly increasing, with its only zero at $s = x L$. When $x < 0$ the skew is positive over the whole wire, and the delay of the wire to $B$ grows without bound with its length, so a longer wire balances it.

## Complexity

With the topology given, there are $n - 1$ merges, each with a constant number of arithmetic operations and at most one square root, so the time is $\Theta(n)$ and the extra space is $\Theta(n)$ for the tree. Building the topology is a separate step; a recursive median split or a greedy pairing of near subtrees takes $O(n \log n)$ or more.

## Properties

- Exact zero skew under the Elmore delay with the pi model, for every topology and every choice of sink loads.
- Each merge with $0 \le x \le 1$ uses exactly the distance between the two roots, the least wire that joins them.
- The tree is not of least wire length for the topology. The root of each subtree is fixed when it is built, but the next merge would often be shorter from another root with the same delays. [Deferred-merge embedding](/deferred-merge-embedding/) keeps all such roots as a segment and picks one later.
## Variants and improvements

- **Linear delay.** With the delay equal to the path length, the tap is at $x = (t_B - t_A + L) / (2 L)$, the case that DME solves with least wire.
- **Topology generation.** Tsay's merge needs a topology. It can come from the recursive split of the [method of means and medians](/method-of-means-and-medians/), or from a greedy matching that pairs near subtrees with similar delays, which aims to avoid elongations.
- **Bounded skew.** If a small skew is allowed, the tap can be anywhere in an interval around $x L$, and the freedom can save wire in later merges.
- **Buffered trees.** Real clock trees insert buffers at some merge points. The same balance equation holds when each buffer starts a new stage, with the buffer delay added to $t$ and its input capacitance in place of $C$.

## When to use it

Use it for a clock net with a known topology when the Elmore delay of the wires is an acceptable model, for example to build a zero-skew tree on top of a placement, or as the merge step inside a larger clock tree synthesis flow. When wire length matters, use DME on the same topology instead, which also gives zero skew. For a regular grid of sinks, an [H-tree](/h-tree-clock/) gives equal path lengths with no computation.

## Pitfalls

- The formula assumes that both subtrees already have zero skew. A subtree whose sinks have different delays must be fixed first.
- If $x$ is outside $[0, 1]$, clamping it to 0 or 1 without making the wire longer leaves a skew. The elongation of lines L7 and L8 is needed.
- An elongation wastes wire and capacitance. Many elongations mean a poor topology that pairs subtrees with very different delays.
- Zero Elmore skew is not zero real skew. The Elmore delay is an upper bound on the 50 percent delay, and the error differs from sink to sink.
- The elongated length involves a square root, so it is irrational in general. Rounding it leaves a small skew; exact checks need exact or high precision arithmetic.

## Implementations

## History

Ren-Song Tsay presented exact zero skew at ICCAD 1991 and in IEEE Transactions on Computer-Aided Design in 1993. Before it, clock routers such as the method of means and medians of Jackson, Srinivasan and Kuh (1990) balanced path lengths, which does not give zero skew in general. In 1992 Chao, Hsu, Ho, Boese and Kahng gave deferred-merge embedding, which keeps Tsay's balance and lowers the wire length for a fixed topology.

## References
