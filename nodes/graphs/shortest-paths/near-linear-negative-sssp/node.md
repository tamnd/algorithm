---
tag: KXQB8V
kind: algorithm
slug: near-linear-negative-sssp
name: Near-linear-time negative-weight SSSP
aliases:
- Bernstein-Nanongkai-Wulff-Nilsen algorithm
area: graphs/shortest-paths
level: research
summary: Computes SSSP with negative integer weights in O(m log^8 n log W) expected time by weight scaling, low-diameter decompositions and a Dijkstra and Bellman-Ford hybrid.
solves: [single-source-shortest-paths]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs, W: the largest absolute value of a negative weight}
  time: {expected: O(m log^8 n log W)}
  space: {extra: O(m + n)}
properties: {deterministic: false, recursive: true}
prereqs: [bellman-ford, dijkstra, potential-function-reduced-costs, low-diameter-decomposition, strongly-connected-components]
see_also: [bellman-ford, goldberg-scaling-sssp, potential-function-reduced-costs, low-diameter-decomposition, negative-cycle-detection, johnson, spfa, sorting-barrier]
sources:
  - url: https://arxiv.org/abs/2203.03456
    title: Aaron Bernstein, Danupon Nanongkai and Christian Wulff-Nilsen, Negative-weight single-source shortest paths in near-linear time (FOCS 2022)
    locator: Section 3 (SPMain, ScaleDown, ElimNeg and FixDAGEdges), Section 4 (the directed low-diameter decomposition) and the handling of negative cycles
  - paper: "Karl Bringmann, Alejandro Cassis and Nick Fischer, Negative-weight single-source shortest paths in near-linear time, now faster!, Proceedings of the 64th IEEE Symposium on Foundations of Computer Science (FOCS), 2023"
    locator: the improvement to O(m log^2 n log(nW) log log n) expected time and the Las Vegas negative-cycle output
  - paper: "Andrew V. Goldberg, Scaling algorithms for the shortest paths problem, SIAM Journal on Computing 24(3), 494 to 504 (1995)"
    locator: the scaling framework and the O(m sqrt(n) log W) bound that the new algorithm improves
  - paper: "Li Chen, Rasmus Kyng, Yang P. Liu, Richard Peng, Maximilian Probst Gutenberg and Sushant Sachdeva, Maximum flow and minimum-cost flow in almost-linear time, Proceedings of the 63rd IEEE Symposium on Foundations of Computer Science (FOCS), 2022"
    locator: the m^(1+o(1)) log W bound for negative-weight SSSP as a special case of min-cost flow
  - paper: "Jeremy T. Fineman, Single-source shortest paths with negative real weights in O~(m n^(8/9)) time, Proceedings of the 56th ACM Symposium on Theory of Computing (STOC), 2024"
    locator: the first strongly subcubic bound for real weights
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 22.1, The Bellman-Ford algorithm (the example graph and the O(VE) baseline)
---

The algorithm of Bernstein, Nanongkai and Wulff-Nilsen solves [single-source shortest paths](/single-source-shortest-paths/) with negative integer weights in $O(m \log^8 n \log W)$ expected time, where $-W$ is the most negative weight. Before 2022, the best simple bound was $O(m \sqrt{n} \log W)$ by [Goldberg's scaling algorithm](/goldberg-scaling-sssp/). The algorithm is combinatorial: it uses only [Dijkstra](/dijkstra/), a little [Bellman-Ford](/bellman-ford/), [strongly connected components](/strongly-connected-components/) and a random [low-diameter decomposition](/low-diameter-decomposition/). It finds a [potential](/potential-function-reduced-costs/) that makes every reduced weight nonnegative and then runs Dijkstra once. Weight scaling reduces the problem to halving the most negative weight, and that step recurses on the pieces of the decomposition, where shortest paths use few negative arcs.

## In plain words

Dijkstra's method is fast, but it fails when some roads have negative cost. Bellman-Ford handles negative costs but is slow.

This method first changes the costs in a way that keeps every best route the best, until no cost is negative. Then Dijkstra finishes the job. To change the costs, it makes the most negative cost half as bad again and again. Each halving cuts the map into pieces that are close together inside, fixes each piece by itself, then fixes the roads between pieces. A mix of Dijkstra and Bellman-Ford cleans up what is left. The random cuts make sure this mix has little work to do.

## The problem

Given a directed graph $G = (V, E)$ with $n$ vertices, $m$ arcs, integer weights $w : E \to \mathbb{Z}$ and a source $s$, compute $\delta(s, v)$ for every $v$, or report that a [negative cycle](/negative-cycle/) is reachable from $s$.

**Weight assumptions.** Weights are integers of any sign, with $w(e) \ge -W$. Integrality is used: the final step multiplies the weights by $2n$ and adds 1 to each, and only integer weights keep the shortest paths the same. Real weights need other methods. A negative cycle reachable from $s$ is reported; one that $s$ cannot reach is ignored. Vertices not reachable from $s$ get $\delta(s, v) = +\infty$.

**Notation.** For a potential $\phi : V \to \mathbb{Z}$, the reduced weight is $w_\phi(u, v) = w(u, v) + \phi(u) - \phi(v)$. Every cycle has the same weight under $w$ and $w_\phi$, and every path from $a$ to $b$ changes by $\phi(a) - \phi(b)$. For $B > 0$, $w_B$ adds $B$ to every negative weight and leaves the others unchanged. $\eta(v)$ is the least number of negative arcs on a shortest path to $v$.

## The algorithm

```pseudo id=main
SPMAIN(G, w, s)
L1  keep only the vertices reachable from s; n ← their number
L2  w̄ ← 2n·w;  B ← the least power of 2 with B ≥ 2n·max(1, W);  φ ← 0
L3  for i ← 1 to log2 B do
L4      φ ← φ + SCALEDOWN(G, w̄_φ, n, B / 2^i); if it reports a negative cycle then return "negative cycle"
L5  w*(e) ← w̄_φ(e) + 1 for every arc e; if some w*(e) < 0 then return "negative cycle"
L6  T ← DIJKSTRA(G, w*, s); return the distances along T measured by w

SCALEDOWN(H, w, Δ, B)                ▷ needs w ≥ −2B; returns φ with w_φ ≥ −B
L7  φ₂ ← 0
L8  if Δ > 2 then
L9      E_rem ← LDD(H with the weights max(0, w_B), ΔB/4)
L10     V_1, ..., V_q ← the SCCs of H − E_rem in topological order
L11     φ₁ ← the union over j of SCALEDOWN(H[V_j], w, Δ/2, B)
L12     φ₂ ← φ₁ + FIXDAGEDGES(H, (w_B)_φ₁, V_1, ..., V_q)
L13 ψ ← ELIMNEG(H, (w_B)_φ₂); if it reports a negative cycle then return "negative cycle"
L14 return φ₂ + ψ

ELIMNEG(H, w)                        ▷ distances from a virtual source with an arc of weight 0 to every vertex
L15 d(v) ← 0 for every v; Q ← all vertices; r ← 0
L16 while Q is not empty do
L17     r ← r + 1; if r > |V(H)| then return "negative cycle"
L18     Dijkstra phase: extract the v of least d(v) until Q is empty; mark v and relax each arc (v, x) with w ≥ 0, adding x to Q when d(x) drops
L19     Bellman-Ford phase: for each marked v, relax each arc (v, x) with w < 0, adding x to Q when d(x) drops; unmark all vertices
L20 return d
```

**FIXDAGEDGES.** For each component $V_j$ in topological order, let $\mu_j$ be the least reduced weight of an arc entering $V_j$ from an earlier component, or 0 if there is none or all are nonnegative. Set $M_j = \sum_{i \le j} \min(0, \mu_i)$ and give every vertex of $V_j$ the potential $M_j$. Arcs inside a component keep their weight, and an arc from $V_i$ to $V_j$ with $i < j$ gets $w + M_i - M_j \ge w - \min(0, \mu_j) \ge 0$.

**LDD.** The low-diameter decomposition takes a graph with nonnegative weights and a bound $D$ and returns a random set $E_{\mathrm{rem}}$ of arcs such that every strongly connected component of $H - E_{\mathrm{rem}}$ has weak diameter at most $D$, and each arc $e$ is in $E_{\mathrm{rem}}$ with probability $O(w(e) \log^2 n / D)$, plus a tiny term. Bernstein, Nanongkai and Wulff-Nilsen build it from random balls grown around vertices.

**Why each phase is there.** Line L9 cuts $H$ into pieces of small diameter. Inside a piece, a shortest path has at most about $\Delta / 2$ negative arcs, because with diameter at most $\Delta B / 4$ there is no room for more arcs of weight about $-B$; so the recursion in line L11 is called with $\Delta / 2$. After line L11, arcs inside the pieces have reduced weight at least $-B$, and in $w_B$ they lose most of their negative weight. Line L12 makes the arcs between pieces nonnegative. What is left negative is mostly the cut arcs of $E_{\mathrm{rem}}$, and the cut probability bounds how many of them lie on a shortest path, so ELIMNEG in line L13 needs few rounds.

## Example

Take the CLRS graph with $s \to t$ (6), $s \to y$ (7), $t \to x$ (5), $t \to y$ (8), $t \to z$ ($-4$), $x \to t$ ($-2$), $y \to x$ ($-3$), $y \to z$ (9), $z \to s$ (2) and $z \to x$ (7). All five vertices are reachable from $s$, and $W = 4$.

**Scaling.** Line L2 sets $\bar{w} = 10 w$, so the most negative weight is $-40$, and $B = 64$. Lines L3 and L4 call SCALEDOWN with $B/2^i = 32, 16, 8, 4, 2, 1$. After the call with 32 every reduced weight is at least $-32$, after the call with 16 at least $-16$, and so on, until after the last call every reduced weight is at least $-1$.

**ELIMNEG on the original weights.** To see the hybrid at work, run lines L15 to L20 on $w$ itself.

| round | after the Dijkstra phase $(s, t, x, y, z)$ | after the Bellman-Ford phase | $Q$ |
|---|---|---|---|
| 1 | $(0, 0, 0, 0, 0)$ | $(0, -2, -3, 0, -4)$ | $t, x, z$ |
| 2 | $(-2, -2, -3, 0, -4)$ | $(-2, -5, -3, 0, -9)$ | $t, z$ |
| 3 | $(-7, -5, -3, 0, -9)$ | $(-7, -5, -3, 0, -9)$ | empty |

The loop ends after 3 rounds, because the shortest path $y \to x \to t \to z$ from the virtual source uses 3 negative arcs. With $\phi = d$, every reduced weight is nonnegative: for example $w_\phi(t, z) = -4 - 5 + 9 = 0$ and $w_\phi(x, t) = -2 - 3 + 5 = 0$.

**Result.** Lines L5 and L6 give $\delta(s, \cdot) = (0, 2, 4, 7, -2)$ for $(s, t, x, y, z)$, with the tree $s \to y \to x \to t \to z$.

**A negative cycle.** Change $x \to t$ to $-6$. The cycle $t \to x \to t$ has weight $-1$. Under $\bar{w}$ it has weight $-10$, and under $w^*$ it has weight $-10 + 2 = -8$ for every $\phi$, so line L4 or line L5 reports it.

**Unreachable vertices.** If a vertex $u$ has no path from $s$, line L1 removes it, and its distance is $+\infty$. A negative cycle among such vertices is removed with them and not reported.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). In short:

1. **ELIMNEG.** Each label is the weight of a walk from the virtual source. After the Dijkstra phase of round $i$, every $v$ with $\eta(v) \le i - 1$ has its exact distance. If there is no negative cycle, $\eta(v) \le |V(H)| - 1$, so the loop ends within $|V(H)|$ rounds, and at the end $d$ satisfies $d(x) \le d(v) + w(v, x)$ on every arc. So line L17 fires only when there is a negative cycle, and otherwise $w_d \ge 0$.
2. **SCALEDOWN.** Since $w_B \ge w$, a graph without negative cycles under $w$ has none under $w_B$. So line L13 returns $\psi$ with $(w_B)_{\phi_2 + \psi} \ge 0$, and then $w_{\phi} \ge -B$, since $w$ and $w_B$ differ by at most $B$ on every arc. Lines L8 to L12 only change the running time, not this argument.
3. **SPMAIN.** By induction, before the call with $B/2^i$ every reduced weight is at least $-2 \cdot B/2^i$, so in the end $w^* \ge 0$. For a path $P$ from $s$ to $v$, $w^*(P) = 2n\, w(P) + \phi(s) - \phi(v) + |P|$ with $|P| \le n - 1 < 2n$, so a path that is shortest under $w^*$ is shortest under $w$, by integrality. With a negative cycle $C$, $w^*(C) \le -2n + n < 0$, so line L5 cannot pass.

## Complexity

- **Time.** $O(m \log^8 n \log W)$ in expectation. The $\log W$ factor counts the scaling rounds. In SCALEDOWN, the recursion has depth $O(\log n)$, each level costs one LDD and one ELIMNEG per piece, and the LDD guarantee bounds the expected number of negative arcs on shortest paths in line L13 by a polylogarithm, so ELIMNEG runs $O(\log^{O(1)} n)$ rounds of Dijkstra. The analysis in the paper multiplies these factors to $\log^8 n$.
- **Space.** $O(m + n)$ besides the recursion stack.
- **Negative cycles.** The time bound assumes no negative cycle. The paper runs the algorithm with a time limit and, if it stops early, uses a further procedure to find a cycle; the round limit in line L17 and the check in line L5 make this implementation report the cycle directly but without the time guarantee.

## Properties

- **Randomized, Las Vegas style.** Only the LDD is random. The answer is always correct; the running time is random.
- **Combinatorial.** No linear algebra, no interior point method, no min-cost flow.
- **Output.** A potential $\phi$ with $w_\phi \ge 0$ on the reachable part, which can be reused like the potential of [Johnson's algorithm](/johnson/).
- **Integer weights only.** The scaling and the final rounding need integers.

## Variants and improvements

- **Bringmann, Cassis and Fischer (2023).** A simpler decomposition and analysis give $O(m \log^2 n \log(nW) \log \log n)$ expected time, and they return a negative cycle in the same time when one exists.
- **Min-cost flow.** The almost-linear min-cost flow algorithm of Chen, Kyng, Liu, Peng, Probst Gutenberg and Sachdeva also solves negative SSSP in $m^{1 + o(1)} \log W$ time, by very different methods.
- **Real weights.** Without integrality, Fineman (2024) gave $\tilde{O}(m n^{8/9})$ time, the first bound below $O(mn)$, and later work improved the exponent.
- **Simple decomposition.** The implementation on this site carves random balls with geometric radii as its LDD. This keeps the answers correct, since correctness does not depend on the decomposition, but it does not have the proven guarantee.

## When to use it

It is mainly of theoretical interest: it settles that negative-weight SSSP with integer weights takes near-linear time. The constants and the logarithmic factors are large. In practice, for sparse graphs with few negative arcs, [Bellman-Ford](/bellman-ford/) with a queue ([SPFA](/spfa/)) or Goldberg's scaling algorithm are usually faster. For all-pairs distances, compute one potential and then run Dijkstra from each source as in Johnson's algorithm.

## Pitfalls

- **Forgetting integrality.** The final step adds 1 to every arc after multiplying by $2n$; with fractional weights this can change which path is shortest.
- **Applying the scaling to unreachable parts.** A negative cycle that $s$ cannot reach makes the potential impossible on the whole graph. Remove the unreachable vertices first, as line L1 does.
- **No limit on ELIMNEG.** With a negative cycle, the Dijkstra and Bellman-Ford phases alternate forever. The round limit of line L17 or a time limit is needed.
- **Mixing $w$ and $w_B$.** The recursion in line L11 uses $w$, so that its precondition $w \ge -2B$ holds, while lines L9, L12 and L13 use $w_B$. Running ELIMNEG on $w_{\phi_2}$ in line L13 instead would still give a correct potential, but the arcs inside the pieces would stay negative and ELIMNEG would need many more rounds.
- **Expecting speed from the simple LDD.** A decomposition without the cut probability guarantee gives correct answers but can make ELIMNEG run many rounds.

## Implementations

## History

Shortest paths with negative weights were solved in $O(nm)$ time by Bellman, Ford and Moore in the 1950s, and this stood for strongly polynomial algorithms. For integer weights, the scaling algorithms of Gabow (1985), Gabow and Tarjan (1989) and Goldberg (1995) reached $O(m \sqrt{n} \log W)$. From 2017 on, interior point methods for flows gave $\tilde{O}(m^{10/7} \log W)$, then $\tilde{O}(m^{4/3} \log W)$, and in 2022 Chen and others reached $m^{1 + o(1)} \log W$ through almost-linear min-cost flow. In the same year Bernstein, Nanongkai and Wulff-Nilsen gave the combinatorial near-linear algorithm on this page, which received a best paper award at FOCS 2022. Bringmann, Cassis and Fischer simplified and sped it up in 2023.

## References
