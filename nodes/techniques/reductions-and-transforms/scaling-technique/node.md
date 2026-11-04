---
tag: V762YG
kind: technique
slug: scaling-technique
name: Scaling technique
aliases:
- bit scaling
- capacity scaling
area: techniques/reductions-and-transforms
level: core
summary: Solving a problem on rounded or coarse values first, then refining the solution one bit or scale at a time.
prereqs: [flow-network, residual-graph, ford-fulkerson, max-flow-min-cut-theorem, dijkstra]
see_also: [capacity-scaling, gabow-scaling-sssp, goldberg-scaling-sssp, cost-scaling, successive-shortest-path, edmonds-karp, pseudo-polynomial-time, rounding-and-scaling]
sources:
  - paper: doi:10.1145/321694.321699
    title: "Jack Edmonds and Richard M. Karp, Theoretical improvements in algorithmic efficiency for network flow problems, Journal of the ACM 19(2) (1972), 248-264"
    locator: the scaling method for the minimum-cost flow (transportation) problem, and the analysis of augmenting path rules for maximum flow
  - paper: doi:10.1016/0022-0000(85)90039-X
    title: "Harold N. Gabow, Scaling algorithms for network problems, Journal of Computer and System Sciences 31(2) (1985), 148-168"
    locator: bit scaling for shortest paths with nonnegative integer lengths, and its use for other network problems
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 7.3, Choosing good augmenting paths (the scaling max-flow algorithm and its O(m^2 log C) bound)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 24, Maximum flow (the chapter problem on maximum flow by scaling)
---

The scaling technique solves a problem with integer data in a sequence of phases, from a coarse view of the numbers to the exact numbers. Each phase starts from the solution of the phase before, which is already almost right, so a cheap correction makes it right at the new scale. It has two common forms: *threshold scaling*, which allows only moves of size at least $\Delta$ and halves $\Delta$ after each phase, as in the [capacity scaling](/capacity-scaling/) max-flow algorithm; and *bit scaling*, which adds one more bit of each number in each phase, as in [Gabow's shortest path algorithm](/gabow-scaling-sssp/). Both turn a running time that grows with the size of the numbers into one that grows with the number of bits, the $\log C$ factor.

## In plain words

Some algorithms make progress in small steps, and the size of a step depends on the numbers in the input. When the numbers are large, such an algorithm can take a very long time. Scaling avoids this. First look only at the big part of each number and solve that rough problem. Then look a little more closely and repair the old answer. The repair is cheap, because the old answer was already close to the new one. Repeat until you see the numbers exactly. The number of rounds is the number of digits in the largest number, not the number itself. So the work grows with the length of the input, as it should, and not with the size of the values.

## When it applies

- The data are integers (or rationals with a common denominator), and the largest one is $C$.
- A simple algorithm is correct but [pseudo-polynomial](/pseudo-polynomial-time/): its running time depends on $C$ itself, for example through the number of unit improvements, as in [Ford-Fulkerson](/ford-fulkerson/) with $O(m \cdot v^*)$ time.
- An optimal solution for the numbers rounded at one scale gives a good start at the next finer scale. "Good" means that the remaining gap or error is bounded by a quantity that does not depend on $C$, such as $2m$ augmentations or distances at most $n - 1$.
- The correction step is faster than solving from scratch when the gap is small. Typical cases: few augmenting paths, or small integer distances that a bucket queue handles in linear time.

## The template

Fix a scale parameter $\Delta$, a power of two. A *$\Delta$-move* is an improving step that changes the objective by at least $\Delta$. The template has two holes: START, which gives a feasible solution for the coarsest scale, and $\Delta$-MOVE, which finds one $\Delta$-move or reports that none exists.

```pseudo id=main
SCALING(I)                    ▷ I has integer data, the largest number is C ≥ 1
L1  Δ ← 2^⌊lg C⌋               ▷ the largest power of two that is at most C
L2  x ← START(I)               ▷ hole: a feasible solution
L3  while Δ ≥ 1 do             ▷ one phase for each scale
L4      while Δ-MOVE(I, x) finds a move μ do
L5          x ← apply μ to x    ▷ the objective improves by at least Δ
L6      Δ ← Δ / 2
L7  return x
```

The analysis always has the same two parts. First, a *gap lemma*: when the phase with parameter $\Delta$ ends (no $\Delta$-move exists), the distance of $x$ from the optimum is at most $B \cdot \Delta$ for a bound $B$ that does not depend on $C$. Second, a *phase count*: the next phase uses $\Delta/2$, and each move gains at least $\Delta/2$, so the next phase has at most $B \cdot \Delta / (\Delta/2) = 2B$ moves. With $\lfloor \lg C \rfloor + 1$ phases, the total is $O(B \log C)$ moves. The last phase has $\Delta = 1$, and for integer data a $1$-move is any improving step, so when it ends, $x$ is optimal.

### Threshold scaling for maximum flow

In a [flow network](/flow-network/) $G = (V, E)$ with $n$ vertices, $m$ edges, source $s$, sink $t$ and integer capacities $c(e) \ge 1$, let $C = \max_e c(e)$. START is the zero flow. For a flow $f$, the [residual graph](/residual-graph/) $G_f$ has, for each edge $e = (u, v)$, a forward arc $u \to v$ with residual capacity $c(e) - f(e)$ and a backward arc $v \to u$ with residual capacity $f(e)$. Let $G_f(\Delta)$ keep only the arcs with residual capacity at least $\Delta$. $\Delta$-MOVE searches $G_f(\Delta)$ for an $s$-$t$ path with BFS and pushes the bottleneck amount along it. All flow values stay integers.

**Lemma (gap).** Let $f$ be a flow such that $G_f(\Delta)$ has no $s$-$t$ path. Then every flow $g$ has $v(g) \le v(f) + m\Delta$.

*Proof.* Let $A$ be the set of vertices that $G_f(\Delta)$ reaches from $s$, and $B = V \setminus A$. Then $s \in A$ and $t \in B$. Let $E^+$ be the edges from $A$ to $B$ and $E^-$ the edges from $B$ to $A$. For $e = (u, v) \in E^+$ the forward arc $u \to v$ leaves $A$, so it is not in $G_f(\Delta)$, and $c(e) - f(e) < \Delta$. For $e = (u, v) \in E^-$ the backward arc $v \to u$ leaves $A$, so $f(e) < \Delta$. By flow conservation, the value of a flow equals its net flow across any $s$-$t$ cut, so

$$v(f) = \sum_{e \in E^+} f(e) - \sum_{e \in E^-} f(e) \ \ge\ \sum_{e \in E^+} \bigl(c(e) - \Delta\bigr) - |E^-| \Delta \ \ge\ c(A, B) - m\Delta.$$

Every flow $g$ has $v(g) \le c(A, B)$ (the weak duality half of the [max-flow min-cut theorem](/max-flow-min-cut-theorem/)). So $v(g) \le v(f) + m\Delta$. $\square$

**Lemma (phase count).** Each phase has at most $2m$ augmentations.

*Proof.* Let $v^*$ be the maximum flow value. In the first phase, $\Delta_0 = 2^{\lfloor \lg C \rfloor} > C/2$, and $v^* \le \sum_{e \text{ out of } s} c(e) \le mC < 2m\Delta_0$. In a later phase with parameter $\Delta$, the phase before used $2\Delta$ and ended with no $2\Delta$-move, so by the gap lemma $v^* - v(f) \le 2m\Delta$ when the phase starts. In both cases the gap at the start of the phase is at most $2m\Delta$. Each augmentation of the phase pushes at least $\Delta$, since every arc of the path has residual capacity at least $\Delta$. The gap never goes below $0$, so there are at most $2m$ augmentations. $\square$

**Theorem.** Capacity scaling returns a maximum flow after at most $2m(\lfloor \lg C \rfloor + 1)$ augmentations, in $O(m^2 \log C)$ time when every vertex lies on some $s$-$t$ path (so $m \ge n - 1$).

*Proof.* There are $\lfloor \lg C \rfloor + 1$ phases, with $\Delta = 2^{\lfloor \lg C \rfloor}, \ldots, 2, 1$, and at most $2m$ augmentations in each. Each augmentation and each failed search is one BFS of $O(n + m) = O(m)$ time, and each phase has one failed search. In the last phase $\Delta = 1$, and $G_f(1)$ is the residual graph without its arcs of capacity $0$. When the phase ends, $G_f$ has no augmenting path, so $f$ is maximum by the max-flow min-cut theorem. $\square$

### Bit scaling for shortest paths

Let $G$ be a directed graph with $n$ vertices, $m$ edges, a source $s$ that reaches every vertex, and integer lengths $0 \le w(e) \le W$. Let $K = \lfloor \lg W \rfloor + 1$, the number of bits of $W$. For $k = 0, 1, \ldots, K$ let $w_k(e) = \lfloor w(e) / 2^{K-k} \rfloor$, the top $k$ bits of $w(e)$. Then $w_0 = 0$, $w_K = w$, and $w_k(e) = 2 w_{k-1}(e) + b_k(e)$ with $b_k(e) \in \{0, 1\}$. Let $d_k(v)$ be the distance from $s$ to $v$ under $w_k$.

```pseudo id=bit
BIT-SCALING-SSSP(G, w, s)
L1  d(v) ← 0 for every vertex v           ▷ d = d_0
L2  for k ← 1 to K do
L3      r(u, v) ← w_k(u, v) + 2d(u) − 2d(v) for every edge (u, v)
L4      δ ← distances from s under r       ▷ Dijkstra with buckets 0 .. n − 1
L5      d(v) ← 2d(v) + δ(v) for every vertex v
L6  return d
```

**Lemma (one bit).** In phase $k$, $r(e) \ge 0$ for every edge, $d_k(v) = 2d_{k-1}(v) + \delta(v)$, and $\delta(v) \le n - 1$.

*Proof.* Since $d_{k-1}$ is a distance function, $d_{k-1}(v) \le d_{k-1}(u) + w_{k-1}(u, v)$ for every edge. So $r(u, v) \ge 2 w_{k-1}(u, v) + 2d_{k-1}(u) - 2d_{k-1}(v) \ge 0$. For any path $P$ from $s$ to $v$, the sum of $r$ telescopes: $r(P) = w_k(P) - 2d_{k-1}(v)$, because $d_{k-1}(s) = 0$. So the shortest paths under $r$ and under $w_k$ are the same, and $\delta(v) = d_k(v) - 2d_{k-1}(v)$. Now take a simple path $P$ from $s$ to $v$ that is shortest under $w_{k-1}$. It has at most $n - 1$ edges, so $w_k(P) \le 2 w_{k-1}(P) + (n - 1) = 2d_{k-1}(v) + n - 1$, and $\delta(v) \le r(P) \le n - 1$. $\square$

Because all values of $\delta$ are integers in $0 \ldots n - 1$, line L4 runs [Dijkstra](/dijkstra/) with an array of $n$ buckets ([Dial's algorithm](/dial-algorithm/)) in $O(n + m)$ time. The total is $O((n + m) \log W)$, against $O(m + nW)$ for Dial's algorithm on the original lengths. This is the shortest path algorithm of Gabow (1985).

### Worked example: capacity scaling

The network has vertices $s, a, b, c, t$ and $m = 8$ edges with capacities $s{\to}a\ 13$, $s{\to}b\ 10$, $a{\to}b\ 6$, $a{\to}c\ 9$, $b{\to}c\ 4$, $b{\to}t\ 7$, $c{\to}t\ 15$, $a{\to}t\ 2$. So $C = 15$ and the first $\Delta$ is $8$. Each search is a BFS in $G_f(\Delta)$.

| $\Delta$ | augmenting path | bottleneck | value after | gap $v^* - v(f)$ after the phase | bound $m\Delta$ |
|---|---|---|---|---|---|
| 8 | $s, a, c, t$ | 9 | 9 | 13 | 64 |
| 4 | $s, b, t$ | 7 | 16 | | |
| 4 | $s, a, b, c, t$ | 4 | 20 | 2 | 32 |
| 2 | $s, b, a, t$ (uses the backward arc $b \to a$) | 2 | 22 | 0 | 16 |
| 1 | none | | 22 | 0 | 8 |

After the phase $\Delta = 8$, the set reached from $s$ in $G_f(8)$ is $A = \{s, b\}$. Its cut has capacity $13 + 4 + 7 = 24$, and the gap lemma gives $v^* \le 24$, which is within $m\Delta = 64$ of $v(f) = 9$. At the end, the set reached from $s$ in $G_f$ is $\{s, a, b\}$, whose cut has capacity $9 + 4 + 7 + 2 = 22$. So the flow of value $22$ is maximum. The run uses 4 augmentations. For generic Ford-Fulkerson the only bound is $v^* = 22$ augmentations.

### Worked example: bit scaling

Take vertices $s, a, b, c, t$ and lengths $s{\to}a\ 5$, $s{\to}b\ 2$, $b{\to}a\ 2$, $a{\to}c\ 3$, $b{\to}c\ 7$, $c{\to}t\ 1$, $b{\to}t\ 9$. Then $W = 9$ and $K = 4$. In phase 3 the lengths $w_3$ are $2, 1, 1, 1, 3, 0, 4$ (in the order above), and the distances of $s, a, b, c, t$ are $d_3 = (0, 2, 1, 3, 3)$. In phase 4 the lengths $w_4 = w$ give the reduced lengths $r = 1, 0, 0, 1, 3, 1, 5$. For example $r(s, a) = 5 + 2 \cdot 0 - 2 \cdot 2 = 1$. Dijkstra under $r$ gives $\delta = (0, 0, 0, 1, 2)$, all at most $n - 1 = 4$, and $d_4 = 2d_3 + \delta = (0, 4, 2, 7, 8)$, the true distances.

## Classic examples

- **[Capacity scaling](/capacity-scaling/) for maximum flow.** Threshold scaling on residual capacities, as above: $O(m \log C)$ augmentations instead of $O(v^*)$.
- **[Gabow's scaling algorithm for shortest paths](/gabow-scaling-sssp/).** Bit scaling on nonnegative integer lengths, with distances from the previous phase as potentials, as above.
- **Scaling for [minimum-cost flow](/min-cost-flow-problem/).** Edmonds and Karp (1972) scaled the numbers of the problem and ran [successive shortest paths](/successive-shortest-path/) in each phase. Each phase needs few shortest path computations, and the total time is polynomial in the bit length of the input.
- **[Cost scaling](/cost-scaling/).** The scale is on the costs instead of the capacities: a flow is kept $\varepsilon$-optimal (there are prices under which every residual arc has reduced cost at least $-\varepsilon$), and $\varepsilon$ is halved in each phase. For integer costs, $\varepsilon < 1/n$ implies that the flow is optimal.
- **[Goldberg's scaling algorithm](/goldberg-scaling-sssp/).** Bit scaling for shortest paths with negative integer lengths, where each phase starts with reduced lengths of at least $-1$ and makes them all nonnegative.
- **[Assignment problem](/assignment-problem/).** Scaling on the weights gives assignment algorithms whose time depends on $\log$ of the largest weight, in contrast with the [Hungarian algorithm](/hungarian-algorithm/), whose time does not depend on the weights at all.

## Variations

- **Threshold or rounded data.** Capacity scaling keeps the true capacities and limits the moves. A related form solves the problem with capacities $\lfloor c(e)/\Delta \rfloor$ and doubles the solution when it goes to the next scale. The analysis is the same.
- **Scaling by a factor other than 2.** Dividing $\Delta$ by a factor $q \ge 2$ gives $O(\log_q C)$ phases with up to $qm$ moves each.
- **Scaling the error instead of the data.** Cost scaling and some interior point methods keep a solution that is optimal up to an error $\varepsilon$ and halve $\varepsilon$. The template is the same, with $\varepsilon$ in place of $\Delta$.

## Pitfalls

- **Integer data are needed.** The last phase relies on "an improvement of less than $1$ is no improvement", which holds for integers. With rational data, multiply by a common denominator first; this increases $\log C$. With irrational data the method does not end with an exact answer.
- **The $\log C$ factor is real.** Capacity scaling is polynomial in the input length, but its time grows with $\log C$. It is not strongly polynomial. The [Edmonds-Karp](/edmonds-karp/) rule (shortest augmenting paths) needs $O(nm)$ augmentations whatever the capacities are. For small $C$, plain Ford-Fulkerson can be faster than scaling.
- **The first scale must be large enough.** The phase count lemma needs $v^* \le 2m\Delta_0$ in the first phase. Starting at $\Delta = 1$ gives Ford-Fulkerson again, and starting far above $C$ only adds empty phases.
- **Reuse the old solution.** The speed comes from the small gap at the start of each phase. A phase that solves its instance from scratch gives $\log C$ times the cost of one solve, which is worse than no scaling at all.
- **The potentials must be exact.** In bit scaling, the reduced lengths are nonnegative only because $d_{k-1}$ are the exact distances of the previous phase. Approximate distances can make some $r(e)$ negative, and then Dijkstra is wrong.
- **This is not the scaling of approximation schemes.** In an [FPTAS](/fptas/), [rounding and scaling](/rounding-and-scaling/) drops the low bits of the numbers for good and accepts a small loss in quality. The scaling technique on this page brings all bits back and returns an exact optimum.

## Exercises

1. Run capacity scaling on the network with edges $s{\to}a$, $s{\to}b$, $a{\to}t$, $b{\to}t$ of capacity $100$ and $a{\to}b$ of capacity $1$. How many augmentations does it use, and how many can generic Ford-Fulkerson use?
2. Prove that capacity scaling with $\Delta$ divided by $q \ge 2$ in each phase does at most $qm$ augmentations per phase.
3. Show that the bound $2m$ in the phase count lemma can be replaced by twice the number of edges between $A$ and $B$ (in either direction), where $(A, B)$ is the cut found at the end of the previous phase.
4. In the bit-scaling example, compute $d_1$ and $d_2$ by hand and check that the reduced lengths of phase 3 are nonnegative.
5. Give an instance where the distances $\delta$ of some phase of bit scaling reach $n - 1$.
6. Bit scaling as written needs $s$ to reach every vertex. Change it so that it works when some vertices are unreachable.

## References
