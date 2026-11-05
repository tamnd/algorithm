---
title: Hierholzer's algorithm returns an Eulerian trail exactly when one exists
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a finite graph with $m$ edges, directed or undirected, with parallel edges and self-loops allowed. Write $U$ for the set of unused edges at a given moment. For a vertex $v$, the *excess* of $v$ in an edge set $F$ is $\deg_F(v) \bmod 2$ if $G$ is undirected, and $\mathrm{out}_F(v) - \mathrm{in}_F(v)$ if $G$ is directed; a loop adds 2 to $\deg_F(v)$, and 1 to both $\mathrm{out}_F(v)$ and $\mathrm{in}_F(v)$. Call $F$ *balanced* if every vertex has excess 0. For a trail $W$ from $a$ to $b$ with edge set $F$: if $a = b$, $F$ is balanced; if $a \ne b$, the excess is 1 at $a$ and at $b$ (undirected), or $+1$ at $a$ and $-1$ at $b$ (directed), and 0 elsewhere. This holds because each inner visit of a vertex uses one edge in and one edge out.

**Lemma 1 (stuck walks).** Let $p$ be a vertex and let $X \subseteq E$. Extend a trail from $p$ by unused edges of $X$, one at a time, until the last vertex $z$ has no unused edge of $X$ left (leaving $z$, if directed). If $X$ is balanced, then $z = p$. If $X$ has nonzero excess exactly at $p$ and one other vertex $q$, with excess $+1$ at $p$ if directed, then $z = q$.

*Proof.* Suppose $z \ne p$, and let $F$ be the edges of the trail. The trail ends at $z$, so the excess of $z$ in $F$ is 1 (undirected) or $-1$ (directed). All edges of $X$ at $z$ (leaving $z$, if directed) are in $F$. Undirected: then $\deg_X(z) = \deg_F(z)$ is odd. Directed: $\mathrm{out}_X(z) = \mathrm{out}_F(z)$ and $\mathrm{in}_X(z) \ge \mathrm{in}_F(z)$, so the excess of $z$ in $X$ is at most $-1$. In both cases $z$ has nonzero excess in $X$ and $z \ne p$. If $X$ is balanced, this is impossible, so $z = p$. Otherwise $z = q$. The walk stops, because each step uses a new edge. $\square$

**Setup.** Line L1 returns "no" exactly when the degree condition fails; that answer is correct, since by the trail fact above the edge set $E$ of an Eulerian trail has the excess pattern of a trail. From here on the condition holds, so $E$ is balanced, or has nonzero excess exactly at $s$ and one other vertex $t$ (with $+1$ at $s$ if directed), by the choice of $s$ at line L2. In the balanced case put $t = s$.

Write the stack as $(x_0, f_0), (x_1, f_1), \ldots, (x_k, f_k)$ from bottom to top, with $x_0 = s$ and $f_0 = \mathrm{NIL}$, and write $T$ as $(u_1, g_1), \ldots, (u_r, g_r)$ in the order of appending.

**Invariant.** At each test of line L5:

1. $f_1, \ldots, f_k$ are distinct and $f_i$ joins $x_{i-1}$ to $x_i$; so the stack is a trail from $s$ to $x_k$.
2. For $1 \le i < r$, the edge $g_i$ joins $u_{i+1}$ to $u_i$; so $R = (u_r, g_{r-1}, u_{r-1}, \ldots, g_1, u_1)$ is a trail ending at $u_1$.
3. If $r \ge 1$, then $u_1 = t$, and no vertex $u_i$ has an unused edge at it (leaving it, if directed).
4. If $r \ge 1$ and the stack is not empty, let $j$ be the index of the top entry right after the last pop. Then $g_r$ joins $x_j$ to $u_r$, every entry above $x_j$ was pushed after the last pop, the set $U_0$ of edges that were unused right after the last pop is balanced, and the used edges are exactly $f_1, \ldots, f_k, g_1, \ldots, g_r$, each once.
5. If $r = 0$, the used edges are exactly $f_1, \ldots, f_k$.

*Initialization.* The stack is $(s, \mathrm{NIL})$ and $T$ is empty. Parts 1 and 5 hold, and parts 2 to 4 say nothing.

*Push.* Lines L8 to L10 use an unused edge $f$ from the top $x_k$ to $w$ and push $(w, f)$. Parts 1 and 5 hold, parts 2 and 3 are unchanged (an edge became used, which keeps part 3), and part 4 holds with the same $j$ and $U_0$, with $f$ added to the used edges.

*First pop.* While $r = 0$, the algorithm has only pushed, building a walk as in Lemma 1 from $s$ in $X = E$. The first pop happens when the top vertex $x_k$ has no unused edge, so $x_k = t$ by Lemma 1. The pop appends $(u_1, g_1) = (t, f_k)$, and $t$ has no unused edge, so parts 2 and 3 hold. After the pop the top is $x_{k-1}$, so $j = k - 1$ and $g_1 = f_k$ joins $x_j$ to $u_1$. The used edges form the stack trail from $s$ to $t$, which has the same excess pattern as $E$, so $U_0 = E$ minus these edges is balanced. Part 4 holds. If $k = 0$ at the first pop, $s$ has no edge (leaving it, if directed), so $m = 0$ by the choice of $s$, and the stack is now empty.

*Later pops.* Let $r \ge 1$, and let line L11 run with top $x_k$, which has no unused edge. By part 4, the entries above $x_j$ were pushed after the last pop, from the unused edges of the balanced set $U_0$, starting at $x_j$, and the walk is now stuck at $x_k$. By Lemma 1 with $X = U_0$ and $p = x_j$, we get $x_k = x_j$ (if $k = j$ this is trivial). So the edges $F = \{f_{j+1}, \ldots, f_k\}$ form a closed trail and are balanced, and the unused edges $U_0 \setminus F$ are balanced. The pop appends $(u_{r+1}, g_{r+1}) = (x_k, f_k)$. Part 2 for the pair $g_r$: it joins $x_j = x_k = u_{r+1}$ to $u_r$. Part 3: $x_k$ has no unused edge, and $u_1 = t$ is unchanged. Part 4 after the pop: the new top is $x_{k-1}$, the new $j$ is $k - 1$, $g_{r+1} = f_k$ joins $x_{k-1}$ to $x_k$, nothing is above the top, the new $U_0$ is $U_0 \setminus F$, which is balanced, and the used edges did not change. Parts 1 and 5 hold for the shorter stack.

**Termination.** Each iteration pushes a new edge, at most $m$ times in all, or pops one of at most $m + 1$ pushed pairs. So the loop ends after at most $2m + 1$ iterations, with an empty stack.

**Output.** The last pop removes $(x_0, \mathrm{NIL}) = (s, \mathrm{NIL})$, so $u_r = s$ and $g_r = \mathrm{NIL}$. By part 2, $R$ reversed, $(u_r, g_{r-1}, \ldots, g_1, u_1)$, is a trail from $s$ to $u_1 = t$, and by part 4 just before the last pop, its edges $g_1, \ldots, g_{r-1}$ are exactly the used edges, each once. So $|T| = r$ is the number of used edges plus 1.

**Theorem.** HIERHOLZER$(G)$ terminates. It returns an Eulerian trail of $G$ if one exists, and that trail is closed if $G$ has an Eulerian circuit. Otherwise it reports that none exists.

*Proof.* Termination was shown. If line L1 answers no, no Eulerian trail exists. Otherwise, if $|T| = m + 1$, all edges are used, and line L13 returns a trail from $s$ to $t$ that uses every edge once. If an Eulerian circuit exists, $E$ is balanced, so $t = s$ and the trail is closed.

If $|T| < m + 1$, some edge $e$ is unused. Then $m \ge 1$, so line L2 chose $s$ with at least one edge, and that edge is used, because the first push takes an edge at $s$ when one exists (one leaving $s$ when directed: if $E$ is balanced and $s$ has an edge, $s$ has an edge leaving it). By part 3, no vertex of the trail $R$ touches an unused edge. Every used edge has both ends on $R$. So the edges of $G$ split into the used edges and the unused edges with no common vertex, both sets nonempty, so the edges do not lie in one connected component (weakly connected, if directed). By Euler's theorem, no Eulerian trail exists, and line L12 reports that correctly. $\blacksquare$
