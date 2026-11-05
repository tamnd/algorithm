---
title: The incidence-matrix operations keep the column invariant and answer the graph queries
proves: [correctness]
status: full
---

We use the pseudocode of the page. The graph has the vertices $0, \ldots, n - 1$ and the edges $e_0, \ldots, e_{m-1}$, where edge $e$ has the ends $t(e)$ and $h(e)$ (the tail and the head if the graph is directed). The invariant is:

> **(C)** $B$ has exactly $m$ columns. In the directed case, column $e$ has $B[t(e), e] = -1$, $B[h(e), e] = +1$ and 0 elsewhere, with $t(e) \ne h(e)$. In the undirected case, column $e$ has $B[v, e] = |\{i : x_i = v\}|$ where $(x_1, x_2) = (t(e), h(e))$, that is, 1 at each of two distinct ends, or 2 at the vertex of a self-loop, and 0 elsewhere.

With $m = 0$, the matrix has $n$ empty rows, and (C) holds.

**ADD-EDGE.** Line L1 adds the column $e = m$ with $n$ zeros, and no other column changes. In the directed case, $u \ne v$, and line L2 writes $-1$ in row $u$ and $+1$ in row $v$, two different cells. In the undirected case, line L3 adds 1 to row $u$ and then 1 to row $v$ of the new column. If $u \ne v$ the column has 1 in both rows; if $u = v$ the cell gets $0 + 1 + 1 = 2$. In both cases column $e$ meets (C) for the new edge with $t(e) = u$ and $h(e) = v$, and the matrix has $m + 1$ columns.

**ENDS.** By (C), the nonzero entries of column $e$ are in the rows of the ends of $e$ and nowhere else. Lines L5 and L6 visit each row once and record $v$ with multiplicity $|B[v, e]|$, so in the undirected case they record $t(e)$ and $h(e)$, which is $v$ twice for a self-loop at $v$. In the directed case the entry $-1$ is in row $t(e)$ and the entry $+1$ in row $h(e)$, so line L7 returns the tail and the head.

**INCIDENT.** By (C), $B[v, e] \ne 0$ if and only if $v \in \{t(e), h(e)\}$, so line L8 returns exactly the edges at $v$, each once.

**ADJACENT.** In the directed case, there is an edge from $u$ to $v$ if and only if some column $e$ has $t(e) = u$ and $h(e) = v$, which by (C) is $B[u, e] = -1$ and $B[v, e] = +1$. Lines L9 to L11 test this for each column and return true at the first one, or false after all $m$. In the undirected case with $u \ne v$, an edge joins $u$ and $v$ if and only if some column has nonzero entries in both rows; with $u = v$, a self-loop at $u$ exists if and only if some column has $B[u, e] = 2$, because by (C) the entry 2 occurs only for a self-loop.

**Degrees.** In the undirected case, by (C), $\sum_e B[v, e]$ counts each edge at $v$ once for each of its ends equal to $v$, which is $d(v)$ with a self-loop counted twice. In the directed case each edge leaving $v$ adds $-1$ and each edge entering $v$ adds $+1$, so the row sum is $d^-(v) - d^+(v)$.

**Cost.** ADD-EDGE appends one cell to each of $n$ rows, $\Theta(n)$ amortized. ENDS reads $n$ cells, INCIDENT reads $m$ cells, and ADJACENT reads at most $2m$ cells. The matrix has $nm$ cells. $\square$
