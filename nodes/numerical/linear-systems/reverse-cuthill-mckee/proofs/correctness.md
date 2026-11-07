---
title: Reverse Cuthill-McKee returns a permutation whose bandwidth is below twice the level width, and Cholesky fill stays in its envelope
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be the graph of a symmetric pattern, $|V| = n$, $|E| = m$. Line numbers refer to the pseudocode. Write $\pi$ for the list built by lines L1 to L8 (the Cuthill-McKee order) and $\pi^R$ for its reverse, returned at line L10. For an ordering $\sigma$, $f_\sigma(v)$ is the position of $v$.

**Lemma 1 (each vertex is appended exactly once).** A vertex is appended only at lines L5 and L8, and only when it is not yet numbered, and it is marked as numbered at the same moment. So no vertex is appended twice. Every vertex $s$ is examined by the loop at line L2; if it is unnumbered then, line L4 picks a root $r$ in the component of $s$ (the pseudo-peripheral search only moves along BFS levels of that component), and the breadth-first search of lines L6 to L8 appends every vertex reachable from $r$, which includes $s$. Hence $\pi$ and $\pi^R$ are permutations of $V$. $\square$

**Termination.** The pseudo-peripheral search of line L4 moves to a new root only when the eccentricity strictly increases; eccentricities are below $n$, so it stops after at most $n$ breadth-first searches. The queue of line L6 receives each vertex at most once by Lemma 1, so each search ends. The loop of line L2 has $n$ iterations.

**Lemma 2 (CM numbers by levels).** Within one component with root $r$, the breadth-first search appends the vertices in order of nondecreasing distance from $r$, so the component occupies a contiguous block of $\pi$, and within it the level $L_i$ (vertices at distance $i$) occupies a contiguous sub-block, after $L_0, \ldots, L_{i-1}$.

*Proof.* Standard property of breadth-first search with a FIFO queue: the queue holds vertices of at most two consecutive distances, with the smaller first, so vertices are appended in nondecreasing distance. Components are processed one after another by the loop at line L2. $\square$

**Theorem 1 (bandwidth).** Let $w$ be the largest level width over the level structures of the roots chosen at line L4. Then $\beta(\pi) = \beta(\pi^R) \le 2w - 1$.

*Proof.* Reversal maps positions $k \mapsto n - 1 - k$, which preserves every difference $|f(v) - f(u)|$, so the two bandwidths are equal. For an edge $\{v, u\}$, both ends lie in one component and their distances from $r$ differ by at most 1, so by Lemma 2 both lie in the union of two consecutive level blocks $L_i \cup L_{i+1}$, a contiguous range of at most $2w$ positions. Hence $|f(v) - f(u)| \le 2w - 1$. $\square$

**Theorem 2 (fill stays in the envelope; any ordering).** Let $B = P A P^T$ be symmetric positive definite with Cholesky factor $L$, and for row $i$ let $\phi_i = \min\{j : b_{ij} \ne 0\}$ be the column of its first nonzero. Then $l_{ij} = 0$ for $j < \phi_i$.

*Proof.* The Cholesky recurrence gives $l_{ij} = \big(b_{ij} - \sum_{k < j} l_{ik} l_{jk}\big)/l_{jj}$ for $j < i$. Fix $i$ and use induction on $j < \phi_i$: $b_{ij} = 0$ by the definition of $\phi_i$, and $l_{ik} = 0$ for every $k < j$ by the induction hypothesis, so $l_{ij} = 0$. $\square$

Hence the nonzeros of $L$ lie in the envelope $\{(i, j) : \phi_i \le j \le i\}$, which has $\mathrm{Env}(\sigma) + n$ entries, and an envelope (profile) solver that stores exactly this set loses nothing. The same holds symbolically: the graph elimination used by the implementation adds an edge $\{i, k\}$ with $i, k > j$ only between later neighbours of an eliminated vertex $j$, and such an edge has $\phi_i \le j < k$.

**Theorem 3 (envelope of the reversal; cited).** For every Cuthill-McKee ordering $\pi$, $\mathrm{Env}(\pi^R) \le \mathrm{Env}(\pi)$, and the work of envelope Cholesky in the order $\pi^R$ is at most that in the order $\pi$. This is the theorem of Liu and Sherman (1976); its proof compares, for each $j$, the number of vertices among the first $j$ that still have an unnumbered neighbour with the number of unnumbered vertices adjacent to the first $j$, using the breadth-first structure of $\pi$. We do not reproduce it; the tests check the inequality on random graphs.

A useful identity behind it: for any ordering $\sigma$, an entry $(v, j)$ lies in the envelope exactly when $v$ is numbered after position $j$ and has a neighbour at a position $\le j$. Counting by $j$,
$$\mathrm{Env}(\sigma) = \sum_{j} \big|\{v : f_\sigma(v) > j,\ \exists u \sim v,\ f_\sigma(u) \le j\}\big|,$$
the sum of the wavefront sizes. Applied to $\pi^R$ and rewritten in terms of $\pi$, $\mathrm{Env}(\pi^R)$ becomes the sum over $j$ of the number of vertices among the first $j$ of $\pi$ that have a neighbour after position $j$.
