---
title: Welsh-Powell gives the greedy coloring of the degree order
proves: [correctness, termination]
status: full
---

Let $\sigma = (\sigma_1, \ldots, \sigma_n)$ be the order of line L1. For a vertex $v$ write $\mathrm{pos}(v)$ for its position in $\sigma$, and call a neighbor $w$ of $v$ *earlier* if $\mathrm{pos}(w) < \mathrm{pos}(v)$. Define the greedy color $g(v)$ by induction along $\sigma$: $g(\sigma_i)$ is the smallest positive integer that is not $g(w)$ for an earlier neighbor $w$ of $\sigma_i$. The map $g$ is a proper coloring, because for an edge $\{u, v\}$ with $u$ earlier, $g(v) \ne g(u)$ by the choice of $g(v)$.

**Termination.** The loops of lines L4 and L7 are for loops with fixed bounds, and line L11 scans a finite list. So the algorithm stops after at most $n^2 + 2m$ steps of the inner loops.

**Claim.** When the algorithm returns, $c(v) = g(v)$ for each vertex $v$.

We prove by induction on $k \ge 0$:

> **(P$_k$)** After the pass with color $k$ ends (for $k = 0$: before the first pass), each vertex $v$ with $g(v) \le k$ has $c(v) = g(v)$, and each vertex with $g(v) > k$ has $c(v) = 0$.

**Base.** Before the first pass, $c(v) = 0$ for all $v$ (line L2), and no vertex has $g(v) \le 0$. So (P$_0$) holds.

**Step.** Assume (P$_{k-1}$) and that pass $k$ starts at position $i$, that is, $\sigma_i$ is the first vertex with $c = 0$. By (P$_{k-1}$), the vertices with $c = 0$ are exactly those with $g \ge k$. In pass $k$, line L11 sets $\mathrm{blocked}[w] = k$ only for neighbors of vertices that get color $k$ in this pass. No earlier pass wrote the value $k$, because pass $j$ writes only the value $j$. So during pass $k$, $\mathrm{blocked}[v] = k$ holds exactly when some neighbor of $v$ got color $k$ earlier in this pass.

We show by induction on $j = i, i + 1, \ldots, n$ that when position $j$ is scanned, $\sigma_j$ gets color $k$ if and only if $g(\sigma_j) = k$. Let $v = \sigma_j$.

- If $c(v) \ne 0$ before the scan, then $g(v) \le k - 1$ by (P$_{k-1}$), and line L9 does not color $v$. Both sides of the equivalence are false.
- Otherwise $g(v) \ge k$. Every vertex before position $i$ has $c \ne 0$, and every vertex scanned so far in this pass comes before $v$ in $\sigma$. So the neighbors of $v$ with color $k$ at this moment are earlier neighbors of $v$, and by the inner induction hypothesis they are exactly the earlier neighbors $w$ of $v$ with $g(w) = k$ (a later neighbor has not been scanned yet, so it has no color $k$). Hence line L9 colors $v$ if and only if no earlier neighbor of $v$ has greedy color $k$.
- Since $g(v) \ge k$, the colors $1, \ldots, k - 1$ all occur on earlier neighbors of $v$ (by the definition of $g$ as the smallest free value). So $g(v) = k$ if and only if no earlier neighbor has greedy color $k$. This matches the condition of the previous point.

So after pass $k$, the vertices with $c = k$ are exactly those with $g = k$, the vertices with $g < k$ keep their colors, and the vertices with $g > k$ still have $c = 0$. This is (P$_k$).

**End.** Each pass colors $\sigma_i$, since $\mathrm{blocked}[\sigma_i] \ne k$ at the start of the pass. So each pass colors at least one new vertex, there are at most $n$ passes, and the loop of line L4 ends with every vertex colored. If the last pass has color $K$, then (P$_K$) and $c(v) \ne 0$ for all $v$ give $c = g$. Since $g$ is a proper coloring, so is $c$. The colors used are $1, \ldots, K$, each one by at least one vertex.

**The bound.** The vertex $\sigma_i$ has at most $i - 1$ earlier neighbors, and at most $d(\sigma_i)$ neighbors in all. Its greedy color exceeds the number of distinct colors among its earlier neighbors by at most one, so $c(\sigma_i) = g(\sigma_i) \le \min(d(\sigma_i), i - 1) + 1$. With $d_i = d(\sigma_i)$, this gives $K \le \max_i \min(d_i + 1, i)$. $\blacksquare$
