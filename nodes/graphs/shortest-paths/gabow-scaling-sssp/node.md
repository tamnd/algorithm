---
tag: N36TQW
kind: algorithm
slug: gabow-scaling-sssp
name: Gabow's scaling algorithm
aliases:
- Gabow scaling shortest paths
area: graphs/shortest-paths
level: research
summary: Bit-scaling SSSP for integer weights. Each bit costs one bucket-based Dijkstra pass, so nonnegative weights take O(m log N) time; the negative-weight versions reach O(sqrt(n) m log(nN)).
solves: [single-source-shortest-paths]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, N: the largest edge weight}
  time: {worst: O((n + m) log N), best: Θ(n + m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [dijkstra, dial-algorithm, potential-function-reduced-costs, scaling-technique]
see_also: [goldberg-scaling-sssp, radix-heap, thorup-undirected-sssp, cost-scaling, assignment-problem, johnson, bellman-ford, single-source-shortest-paths]
sources:
  - paper: doi:10.1016/0022-0000(85)90039-X
    title: Harold N. Gabow, Scaling algorithms for network problems, Journal of Computer and System Sciences 31(2), 148 to 168 (1985)
    locator: the shortest-path section (bit scaling with the previous distances as potentials, the bound n - 1 on the scaled distances, and the O(m log_d N) time), and the O(n^(3/4) m log N) bound for negative weights
  - paper: doi:10.1137/0218069
    title: Harold N. Gabow and Robert E. Tarjan, Faster scaling algorithms for network problems, SIAM Journal on Computing 18(5), 1013 to 1036 (1989)
    locator: the scaling algorithm for the assignment problem and its application to shortest paths with negative integer weights in O(sqrt(n) m log(nN)) time
  - paper: "Andrew V. Goldberg, Scaling algorithms for the shortest paths problem, SIAM Journal on Computing 24(3), 494 to 504 (1995)"
    locator: the introduction, which compares the bounds of the scaling algorithms of Gabow and of Gabow and Tarjan
---

Gabow's scaling algorithm computes [single-source shortest paths](/single-source-shortest-paths/) for integer edge weights by looking at the weights one bit at a time, from the most significant bit down. After each bit it knows the exact distances for the weights cut off at that bit. Doubling those distances gives [potentials](/potential-function-reduced-costs/) under which the next, finer weights have nonnegative reduced costs and all reduced distances are below $n$. So each bit costs one run of [Dijkstra's algorithm](/dijkstra/) with $n$ buckets, as in [Dial's algorithm](/dial-algorithm/), in $O(n + m)$ time. For weights up to $N$ the total is $O((n + m) \log N)$, against $O(m + nN)$ for Dial's algorithm on the full weights. Harold Gabow published it in 1985 as one of several bit-scaling algorithms for network problems; the same paper and a later one with Robert Tarjan used scaling for negative weights too.

## In plain words

Rounding every road length down to a coarse unit makes the problem easy: with lengths 0 and 1 only, distances are small. Gabow starts with the coarsest rounding and refines it one binary digit at a time.

When one more digit is added, every length roughly doubles, plus 0 or 1. So the new distances are roughly the old ones doubled, plus a small correction, less than $n$. The algorithm computes only these corrections. Small whole numbers can be sorted into $n$ buckets, so finding them is a single fast sweep, and the sweep is repeated once per digit.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, a source $s$, and an integer weight $w(u, v)$ on each edge. The output is the distance $\delta(s, v)$ for every vertex $v$ and a [shortest-path tree](/shortest-path-tree/).

**Weight assumptions.** This version needs every weight to be an integer with $0 \le w(u, v) \le N$; the input is rejected otherwise. Zero weights, zero-weight cycles, parallel edges and self-loops are allowed. With nonnegative weights there is no negative cycle, so every distance is well defined; any negative cycle contains a negative edge and is rejected with it. Vertices that $s$ does not reach get $\delta = +\infty$ and no parent. Negative integer weights need the variants below, which detect negative cycles.

## The algorithm

Let $b$ be the number of bits of $N$, and for $i = 0, \ldots, b$ let $w_i(e) = \lfloor w(e) / 2^{b - i} \rfloor$, the weight cut to its top $i$ bits. Then $w_0 = 0$, $w_b = w$, and $2 w_{i-1}(e) \le w_i(e) \le 2 w_{i-1}(e) + 1$. Let $d_i$ be the distances under $w_i$.

```pseudo id=main
GABOW-SCALING(G, w, s)
L1  b ← the number of bits of the largest weight; d(v) ← 0 if s reaches v, else ∞
L2  for i ← 1 to b do
L3      w_i(e) ← ⌊w(e) / 2^(b−i)⌋ for every edge e
L4      r(u, v) ← w_i(u, v) + 2 d(u) − 2 d(v) for every edge (u, v)       ▷ r ≥ 0
L5      δ ← distances from s with the lengths r, by Dial's algorithm with buckets 0 .. n − 1
L6      d(v) ← 2 d(v) + δ(v) for every v with d(v) < ∞
L7  return d
```

Line L1 is $d_0$: with all weights 0, the distance is 0 to every reachable vertex. Line L4 uses $2 d_{i-1}$ as a potential. Line L5 sweeps the buckets in increasing order, scans each vertex once from the bucket of its final label, and drops tentative labels of $n$ or more, which the analysis shows can never be final. The parent pointers of the last sweep form the shortest-path tree.

## Example

The vertices are $s, a, b, c$ and the edges $s \to a$ (5), $s \to b$ (3), $b \to a$ (1), $a \to c$ (2), $b \to c$ (7). The largest weight is $7 = 111_2$, so $b = 3$ scales.

| scale | $s{\to}a$ | $s{\to}b$ | $b{\to}a$ | $a{\to}c$ | $b{\to}c$ | $d$ for $s, a, b, c$ |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 | 0, 0, 0, 0 |
| 1 | 1 | 0 | 0 | 0 | 1 | 0, 0, 0, 0 |
| 2 | 2 | 1 | 0 | 1 | 3 | 0, 1, 1, 2 |
| 3 | 5 | 3 | 1 | 2 | 7 | 0, 4, 3, 6 |

In scale 3 the potentials are $2 d_2 = (0, 2, 2, 4)$, and the reduced lengths are $r(s, a) = 5 - 2 = 3$, $r(s, b) = 3 - 2 = 1$, $r(b, a) = 1 + 2 - 2 = 1$, $r(a, c) = 2 + 2 - 4 = 0$ and $r(b, c) = 7 + 2 - 4 = 5$, all nonnegative. The sweep gives $\delta = (0, 2, 1, 2)$, all below $n = 4$, and $d_3 = 2 d_2 + \delta = (0, 4, 3, 6)$, with the tree $s \to b \to a \to c$.

**Unreachable vertices.** With the extra edges $x \to y$ (1) and $y \to s$ (1), $x$ and $y$ get $\infty$ in line L1 and are never put in a bucket.

**Negative weights.** With $a \to c$ ($-2$) the input is rejected before any scale. So is a negative cycle such as $a \to c$ ($-3$), $c \to a$ (1).

## Correctness

**Theorem.** For nonnegative integer weights, after the scale $i$ loop, $d(v) = d_i(v)$ for every $v$. In particular the algorithm returns $\delta(s, v)$, $+\infty$ for unreachable $v$.

The proof is an induction on $i$. Since $w_i(u, v) \ge 2 w_{i-1}(u, v)$ and $d_{i-1}(v) \le d_{i-1}(u) + w_{i-1}(u, v)$, the reduced length $r(u, v) = w_i(u, v) + 2 d_{i-1}(u) - 2 d_{i-1}(v) \ge 0$. The weight of any path under $r$ is its weight under $w_i$ minus $2 d_{i-1}(v) - 2 d_{i-1}(s)$, so the reduced distance is $\delta_r(v) = d_i(v) - 2 d_{i-1}(v)$. A shortest $w_{i-1}$ path to $v$ can be taken simple, with at most $n - 1$ edges, and $w_i \le 2 w_{i-1} + 1$ on each, so $d_i(v) \le 2 d_{i-1}(v) + n - 1$, that is $\delta_r(v) \le n - 1$. Dijkstra's algorithm with nonnegative integer lengths is correct with buckets, and dropping labels of $n$ or more loses nothing: the final label of $v$ arrives by relaxing the last edge of a shortest path, from a vertex whose final label is at most $\delta_r(v) \le n - 1$. So line L6 sets $d(v) = d_i(v)$. The full proof is in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/), with weights of $O(\log N)$ bits in a word.

- **Time.** Line L1 is a graph search, $O(n + m)$. Each scale computes the reduced lengths in $O(m)$ and sweeps $n$ buckets with at most $m + 1$ insertions, $O(n + m)$. There are $b = \lfloor \log_2 N \rfloor + 1$ scales, so the total is $O((n + m) \log N)$, which is $O(m \log N)$ when every vertex is reachable.
- **Best case.** If $N \le 1$ there is at most one scale, and the time is $\Theta(n + m)$.
- **Space.** Labels, potentials and parents take $\Theta(n)$; the buckets hold up to $m + 1$ entries, so the extra space is $O(n + m)$. Buckets as doubly linked lists, with a vertex moved instead of inserted again, bring it to $\Theta(n)$.
- **Compared with other integer methods.** Dial's algorithm alone takes $O(m + nN)$, and Dijkstra's algorithm with a [radix heap](/radix-heap/) takes $O(m + n \log N)$, which is better for dense graphs; scaling is simplest when $N$ is large and the graph is sparse.

## Properties

- **Exact at every scale.** After scale $i$ the labels are the exact distances for the weights cut to $i$ bits, so the algorithm can be stopped early for an approximation within $n 2^{b - i}$.
- **Small reduced distances.** The potentials from the previous scale make every reduced distance at most $n - 1$, independent of $N$.
- **Integer weights only.** The bound $n - 1$ comes from the rounding error of one bit per edge; real weights have no bits to scale.
- **Monotone across scales.** $d_i(v) \ge 2 d_{i-1}(v)$, so the labels at least double from one scale to the next.

## Variants and improvements

- **Larger base.** Gabow scales in base $\Delta = \max(2, \lceil m/n \rceil)$ instead of 2. Each scale then has reduced distances below $(\Delta - 1)(n - 1) + 1$ and still costs $O(m)$, and there are $O(\log_\Delta N)$ scales, so the time is $O(m \log_{m/n} N)$ for $m \ge 2n$.
- **Negative weights.** With negative integer weights, the reduced lengths of a new scale are at least $-1$ rather than 0, and each scale must remove the $-1$ edges or find a negative cycle. Gabow (1985) did this in $O(n^{3/4} m)$ per scale, for $O(n^{3/4} m \log N)$. Gabow and Tarjan (1989) reduced the problem to the [assignment problem](/assignment-problem/) and solved it by their scaling algorithm in $O(\sqrt n\, m \log(nN))$. [Goldberg's scaling algorithm](/goldberg-scaling-sssp/) (1995) reaches $O(\sqrt n\, m \log N)$ directly on the graph.
- **Cost scaling for flows.** The same idea, with costs refined bit by bit and potentials carried between scales, is the basis of [cost scaling](/cost-scaling/) for minimum-cost flow.

## When to use it

Use it for integer weights that are large compared with $n$, on sparse graphs, when a simple bucket-based method is wanted instead of a heap. For moderate weights, Dial's algorithm or a radix heap is simpler and faster; for real weights, use Dijkstra's algorithm with a heap. With negative integer weights, use a negative-weight scaling algorithm such as Goldberg's.

## Pitfalls

- **Rounding up instead of down.** The bounds $2 w_{i-1} \le w_i \le 2 w_{i-1} + 1$ hold for rounding down. Rounding to nearest can make reduced lengths negative.
- **Forgetting to double.** The potential at scale $i$ is $2 d_{i-1}$, not $d_{i-1}$. Without the factor 2, reduced lengths go negative.
- **Unreachable vertices.** Their labels are $\infty$, and $2 \infty - 2 \infty$ is undefined. They can never be reached, so leave them out of every scale.
- **Too few buckets.** Labels up to $n - 1$ are needed. A sweep with fewer buckets loses vertices whose reduced distance is exactly $n - 1$, as on a path of $n$ vertices with all weights 1 at the last scale.

## Implementations

The Python version checks the weights, computes scale 0 by a depth-first search, and runs one bucket sweep per bit with the shifted weights $w \gg (b - i)$, dropping tentative labels of $n$ or more. It returns the distances and the parents of the last sweep, and can record the labels after each scale.

## History

Edmonds and Karp introduced scaling for network flows in 1972. Gabow (1985) applied bit scaling to shortest paths, matching and other network problems, which gave the bound $O(m \log_{m/n} N)$ for nonnegative shortest paths and the first scaling bound for negative weights. Gabow and Tarjan (1989) improved the negative-weight bound to $O(\sqrt n\, m \log(nN))$, and Goldberg (1995) to $O(\sqrt n\, m \log N)$. For nonnegative integer weights, later work moved away from scaling, to radix heaps and to Thorup's linear-time algorithm for undirected graphs.

## References
