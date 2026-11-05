---
title: The Itai-Rodeh girth algorithm returns a shortest cycle
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a finite undirected graph, with loops and parallel edges allowed, and let $g$ be its girth, the length of a shortest cycle, with $g = \infty$ if $G$ is a forest. Fix one search, with root $r$. Call the edges $\mathrm{pe}[w]$, for the vertices $w \ne r$ that the search reaches, the *tree edges*.

**Fact 1 (the search tree).** Each tree edge $\mathrm{pe}[w]$ joins $w$ to $\mathrm{pv}[w]$, which was reached before $w$, and $\mathrm{dist}[w] = \mathrm{dist}[\mathrm{pv}[w]] + 1$. So the tree edges form a tree $T_r$ on the reached vertices, which are the vertices of the component of $r$; the path in $T_r$ from $r$ to $w$ has $\mathrm{dist}[w]$ edges; and $\mathrm{dist}[w]$ is the distance from $r$ to $w$ in $G$. These are the standard properties of [breadth-first search](/breadth-first-search/). A loop is never a tree edge, since it leads from a reached vertex to itself.

**Fact 2 (non-tree edges are seen).** Let $e = \{u, v\}$ be an edge in the component of $r$ that is not a tree edge, and let $u$ be the end dequeued first (either end, if $u = v$). When $u$ scans $e$ at line L6, $v$ is already reached: otherwise line L7 would make $e = \mathrm{pe}[v]$ a tree edge. And $e \ne \mathrm{pe}[u]$, since $e$ is not a tree edge. So line L8 compares $\mathrm{dist}[u] + \mathrm{dist}[v] + 1$ with $\mathrm{best}$, and afterwards $\mathrm{best} \le \mathrm{dist}[u] + \mathrm{dist}[v] + 1$.

**Fact 3 (recorded edges are non-tree edges).** If line L9 records $(r, e, u, v)$, then $e$ is not a tree edge of this search. *Proof.* $e \ne \mathrm{pe}[u]$ by the test. A tree edge $\mathrm{pe}[w]$ has $w$ as an end, so only $\mathrm{pe}[v]$ is left to exclude, for $u \ne v$. If $\mathrm{pe}[v] = e$, then $v$ was reached at line L7 by a scan of $e$ from its other end $u$. But $u$ has $e$ only once in its list, since $u \ne v$, and in the present scan of that entry $v$ was already reached. So $\mathrm{pe}[v] \ne e$. $\square$

**Lemma A (closed walks).** If a closed walk $W$ of length $k$ uses some edge $e$ exactly once, then $G$ has a cycle through $e$ of length at most $k$.

*Proof.* If $e$ is a loop, it is a cycle of length 1. Otherwise rotate $W$ so that $e$ is its last edge, from $a$ to $b$. The rest of $W$ is a walk from $b$ to $a$ of length $k - 1$ that does not use $e$. A shortest subwalk from $b$ to $a$ formed by its edges is a simple path $P$ (a repeated vertex would give a shorter one). Then $P$ followed by $e$ is a cycle of length at most $k$: its inner vertices are distinct, and its edges are distinct because $e \notin P$. $\square$

**Lemma B (every candidate is at least $g$).** If line L9 sets $\mathrm{best}$ to $c = \mathrm{dist}[u] + \mathrm{dist}[v] + 1$, then $G$ has a cycle of length at most $c$.

*Proof.* The path in $T_r$ from $r$ to $u$, the edge $e$, and the path in $T_r$ from $v$ to $r$ form a closed walk of length $c$ by Fact 1. By Fact 3, $e$ is not a tree edge, so it appears in this walk exactly once. Lemma A gives the cycle. $\square$

**Lemma C (a root on a shortest cycle finds $g$).** Let $C = (c_0, c_1, \ldots, c_{g-1}, c_0)$ be a shortest cycle with $c_0 = r$. After the search from $r$, $\mathrm{best} \le g$.

*Proof.* All of $C$ lies in the component of $r$. The tree $T_r$ has no cycle, so some edge $e$ of $C$, joining $c_i$ and $c_{i+1}$ with indices modulo $g$ and $0 \le i \le g - 1$, is not a tree edge. Walking along $C$ in either direction shows $\mathrm{dist}[c_j] \le \min(j, g - j)$ for $0 \le j \le g$. By Fact 2, after the search $\mathrm{best} \le \mathrm{dist}[c_i] + \mathrm{dist}[c_{i+1}] + 1 \le \min(i, g - i) + \min(i + 1, g - i - 1) + 1$. If $i + 1 \le g/2$, this is at most $i + (i + 1) + 1 \le g$. If $i \ge g/2$, it is at most $(g - i) + (g - i - 1) + 1 = 2g - 2i \le g$. Otherwise $i < g/2 < i + 1$, and it is at most $i + (g - i - 1) + 1 = g$. $\square$

**Termination.** Each search dequeues each vertex at most once and scans each list once, so it ends; there are $n + 1$ searches. The climb at line L12 ends, because each step replaces $a$ or $b$ by its parent and lowers its distance by 1.

**Theorem.** If $G$ is a forest, GIRTH$(G)$ reports it. Otherwise it returns a cycle of length $g$.

*Proof.* If $G$ is a forest, Lemma B shows that line L9 never runs, so $\mathrm{found} = \mathrm{NIL}$ at line L10. Otherwise $g$ is finite. By Lemma C, the search from a vertex of a shortest cycle makes $\mathrm{best} \le g$, and by Lemma B, $\mathrm{best} \ge g$ at all times. So at the end $\mathrm{best} = g$, and $\mathrm{found} = (r, e, u, v)$ was recorded with $\mathrm{dist}[u] + \mathrm{dist}[v] + 1 = g$ in the search from $r$.

Line L11 repeats that search. The search is deterministic, so it rebuilds the same $\mathrm{dist}$, $\mathrm{pv}$ and $\mathrm{pe}$. At line L12, while $a \ne b$, the one with the larger distance (or $a$, on a tie) moves to its parent, so both walk up their paths in $T_r$ towards $r$ and stop at the first common vertex $w$, the lowest common ancestor of $u$ and $v$. The path $Q_u$ in $T_r$ from $w$ to $u$ and the path $Q_v$ from $w$ to $v$ share only $w$. The returned closed walk is $Q_u$, then $e$, then $Q_v$ backwards. Its inner vertices are distinct, its tree edges are distinct, and $e$ is not a tree edge by Fact 3, so it is a cycle (the loop $e$ itself if $u = v$). Its length is $\mathrm{dist}[u] + \mathrm{dist}[v] + 1 - 2\,\mathrm{dist}[w] \le g$, and no cycle is shorter than $g$, so its length is exactly $g$. $\blacksquare$
