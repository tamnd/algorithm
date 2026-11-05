---
title: Hopcroft-Karp runs in O((n + m) n^(1/2)) time
proves: [time.worst]
status: full
---

Let $G = (X \cup Y, E)$ be bipartite with $n$ vertices and $m$ edges, and let $\nu = \nu(G)$. Each operation on an index, a label or a queue costs $O(1)$ on the [word RAM](/word-ram/).

**One phase costs $O(n + m)$.** Line L3 costs $O(|X|)$. In the search of lines L5 to L8, each vertex of $X$ enters the queue at most once, because it is enqueued only when its label changes from $\infty$, and its edges are scanned once when it leaves the queue: $O(n + m)$. Lines L10 and L11 cost $O(|X|)$ outside the calls. A call DFS($x$) sets $\text{dist}[x] = \infty$ in line L12 before it looks at any edge, and no call enters a vertex whose label is $\infty$, so each vertex of $X$ is entered at most once per phase. Each edge $xy$ is scanned at most once, in the single call on $x$, and the work of line L14 outside the inner call is $O(1)$ per edge. Line L15 runs once per vertex of $X$ on a found path, so at most $|X|$ times. The total is $O(n + m)$.

**The number of phases.** Let $D_t$ be the value $D$ of phase $t$. By Claim 4 of the correctness proof, a shortest augmenting path after phase $t$ has more than $2D_t - 1$ edges, and the length is odd, so $D_{t+1} \ge D_t + 1$. As $D_1 \ge 1$, phase $t$ has $D_t \ge t$ whenever it augments.

Let $M_t$ be the matching after phase $t$ and $M^*$ a maximum matching. The symmetric difference $M_t \triangle M^*$ contains $\nu - |M_t|$ vertex-disjoint $M_t$-augmenting paths ([augmenting path](/augmenting-path/)). Each of them has at least $D_{t+1} \ge t + 1$ vertices of $Y$, hence at least $t + 1$ edges of $M^*$, and they are disjoint, so $(t + 1)(\nu - |M_t|) \le |M^*| = \nu$, that is, $\nu - |M_t| \le \nu / (t + 1)$.

If $\nu = 0$, the first phase has $D = \infty$ and is the only one. Otherwise take $t = \lfloor \sqrt \nu \rfloor$. If phase $t$ is reached and augments, then $\nu - |M_t| \le \nu / (\lfloor \sqrt \nu \rfloor + 1) < \sqrt \nu$, and each later phase that augments adds at least one edge, so fewer than $\sqrt \nu$ augmenting phases follow. In all cases there are at most $2\sqrt \nu$ augmenting phases, and one more phase that returns. Since $\nu \le n / 2$, the number of phases is at most $\sqrt{2n} + 1$.

**Total.** $O(\sqrt n)$ phases of $O(n + m)$ time give $O((n + m)\sqrt n)$ time, which is $O(m \sqrt n)$ when no vertex is isolated. The space is $\Theta(n + m)$: the adjacency lists, the arrays $\text{mate}$ and $\text{dist}$, the queue, and the path stack of at most $|X|$ entries. $\blacksquare$
