---
title: Capacity scaling makes at most 2m augmentations per phase
proves: [time.worst]
status: full
---

Use the notation of the correctness proof, let $F$ be the maximum flow value, and assume $m \ge n - 1$ (otherwise add $O(n)$ per search).

**Lemma 1.** At the end of a $\Delta$-phase, $F - |f| < m \Delta$.

*Proof.* Let $S$ be the set of vertices reachable from $s$ in $G_f(\Delta)$; $t \notin S$ because the phase has ended. For every s-t flow $g$, $|g| - |f| \le \sum (c(e) - f(e)) + \sum f(e)$, where the first sum is over edges from $S$ to $\bar S$ and the second over edges from $\bar S$ to $S$, since $|g| = g(S, \bar S) - g(\bar S, S) \le c(S, \bar S)$ and $|f| = f(S, \bar S) - f(\bar S, S)$. An edge $e$ from $S$ to $\bar S$ has $c(e) - f(e) = c_f(e^+) < \Delta$, else its head would be reachable in $G_f(\Delta)$; an edge from $\bar S$ to $S$ has $f(e) = c_f(e^-) < \Delta$ for the same reason. Each edge is in at most one of the two sums, so $|g| - |f| < m\Delta$ when some edge crosses the cut, and $|g| - |f| \le 0$ otherwise. Take $g$ maximum. $\square$

**Lemma 2.** Each phase performs fewer than $2m$ augmentations, or none.

*Proof.* The first threshold $\Delta_0$ is a power of 2, and line L7 halves it, so every threshold is a power of 2 and each later threshold $\Delta$ follows a phase with threshold exactly $2\Delta$. For the first phase, $\Delta_0 \le U < 2\Delta_0$ by the choice in line L2, so $F \le c(\{s\}, V \setminus \{s\}) \le mU < 2m\Delta_0$. For a later phase with threshold $\Delta$, Lemma 1 for the previous phase says that the missing value at the start is less than $2m\Delta$. In every phase each augmentation carries at least $\Delta$, so the phase has fewer than $2m\Delta / \Delta = 2m$ augmentations. $\square$

**Theorem.** The algorithm runs in $O(m^2 \log U)$ time and $\Theta(n + m)$ space.

*Proof.* There are $\lfloor \log_2 U \rfloor + 1$ phases. Each phase has fewer than $2m$ augmentations, each preceded by one search, plus one failing search; a search costs $O(n + m) = O(m)$ and an augmentation $O(n)$. So a phase costs $O(m^2)$ and the total is $O(m^2 \log U)$, plus $O(m)$ for lines L1, L2, L8 and L9. The arrays of residual capacities, the adjacency lists, the queue and the parent arcs take $\Theta(n + m)$ space. $\blacksquare$
