---
title: The threshold algorithm returns a tour of bottleneck at most 2 OPT
proves: [correctness]
status: full
---

The costs $c$ on $V$, with $|V| = n \ge 3$, are symmetric, non-negative and satisfy the triangle inequality. For a threshold $x$, $G(x)$ is the graph on $V$ with the edges $\{u, v\}$, $u \ne v$, with $c(u, v) \le x$. A graph is biconnected if it is connected and it stays connected after the removal of any one vertex. The proof uses one theorem that it does not prove.

**Fleischner's theorem (1974, cited).** If a graph with at least three vertices is biconnected, its square has a Hamiltonian cycle.

**Lemma 1 (monotone).** If $G(x)$ is biconnected and $x \le x'$, then $G(x')$ is biconnected.

*Proof.* $G(x')$ has the same vertices as $G(x)$ and a superset of its edges. Adding edges keeps a graph connected, also after the removal of a vertex. $\square$

**Lemma 2 (the search).** Lines L1 to L5 return the least cost $t$ in the list $t[1] < \cdots < t[q]$ such that $G(t)$ is biconnected.

*Proof.* $G(t[q])$ is the complete graph on $n \ge 3$ vertices, which is biconnected. By Lemma 1, the predicate "$G(t[i])$ is biconnected" is false for $i < i^*$ and true for $i \ge i^*$, for some $i^*$. The loop keeps the invariant $lo \le i^* \le hi$: at the start $lo = 1$ and $hi = q$; if $G(t[mid])$ is biconnected then $i^* \le mid$, and if not then $i^* > mid$. Each step makes $hi - lo$ smaller, because $lo \le mid < hi$. At the end $lo = hi = i^*$. $\square$

**Lemma 3 (the lower bound).** $t \le \text{OPT}$.

*Proof.* Let $H^*$ be an optimal tour. Each of its edges costs at most OPT, so $H^*$ is a Hamiltonian cycle in $G(\text{OPT})$. Removing one vertex from a cycle through all $n$ vertices leaves a path through the other $n - 1$ vertices, so $G(\text{OPT})$ is biconnected. OPT is the cost of an edge of $H^*$, so it is one of the $t[i]$, and by Lemma 2, $t \le \text{OPT}$. $\square$

**Lemma 4 (the edges of the square).** Each edge $\{u, v\}$ of the square $S$ of $G(t)$ has $c(u, v) \le 2t$.

*Proof.* If $\{u, v\}$ is an edge of $G(t)$, then $c(u, v) \le t \le 2t$, because costs are non-negative. Otherwise $u$ and $v$ have distance 2 in $G(t)$, so there is a vertex $w$ with $c(u, w) \le t$ and $c(w, v) \le t$. By the triangle inequality, $c(u, v) \le c(u, w) + c(w, v) \le 2t$. $\square$

**Theorem.** BOTTLENECK-TSP-2 returns a tour $H$ whose bottleneck is at most $2t \le 2 \cdot \text{OPT}$.

*Proof.* By Lemma 2, $G(t)$ is biconnected, and it has $n \ge 3$ vertices. By Fleischner's theorem, $S$ has a Hamiltonian cycle, so line L7 succeeds, and $H$ is a tour. Each edge of $H$ is an edge of $S$, so by Lemma 4 it costs at most $2t$. By Lemma 3, $2t \le 2 \cdot \text{OPT}$. $\blacksquare$
