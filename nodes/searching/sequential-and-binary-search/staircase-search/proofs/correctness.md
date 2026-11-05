---
title: Staircase search finds x when it occurs, returns NIL otherwise, and reads at most m + n - 1 cells
proves: [correctness, termination, complexity]
status: full
---

Let $M$ be an $m \times n$ matrix, $m, n \ge 0$, with $M[i][j] \le M[i][j+1]$ and $M[i][j] \le M[i+1][j]$ for all indices in range, and let $x$ be a key. Write $X = \{(k, l) : M[k][l] = x\}$ for the set of cells that hold $x$. We prove three things about STAIRCASE-SEARCH$(M, x)$: it stops after at most $m + n - 1$ passes of the loop, a returned pair is in $X$, and NIL is returned only when $X$ is empty.

**Invariant.** Before each test of line L2, every $(k, l) \in X$ has $k \ge i$ and $l \le j$. Also $0 \le i \le m$ and $-1 \le j \le n - 1$.

*Start.* Line L1 sets $i = 0$ and $j = n - 1$. Every cell has $k \ge 0$ and $l \le n - 1$, so the first statement holds. The bounds hold since $m, n \ge 0$.

*Step.* A pass runs only when $i < m$ and $j \ge 0$, so $(i, j)$ is a cell. If $M[i][j] = x$, line L3 returns. Otherwise there are two cases.

- *Case $M[i][j] > x$.* Line L4 sets $j' = j - 1$. Take $(k, l) \in X$. By the invariant $k \ge i$ and $l \le j$. Assume $l = j$. Since column $j$ is sorted and $k \ge i$, $M[k][j] \ge M[i][j] > x$, which contradicts $M[k][l] = x$. So $l \le j - 1 = j'$. The new bounds hold, since $j \ge 0$ gives $j' \ge -1$.
- *Case $M[i][j] < x$.* Line L5 sets $i' = i + 1$. Take $(k, l) \in X$, with $k \ge i$ and $l \le j$. Assume $k = i$. Since row $i$ is sorted and $l \le j$, $M[i][l] \le M[i][j] < x$, a contradiction. So $k \ge i + 1 = i'$. The new bounds hold, since $i < m$ gives $i' \le m$.

So the invariant holds before the next test.

**A returned pair is correct.** Line L3 returns $(i, j)$ only when $M[i][j] = x$, so $(i, j) \in X$.

**NIL is correct.** Line L6 runs only when the test of line L2 fails, that is $i \ge m$ or $j < 0$. If $(k, l) \in X$, the invariant gives $k \ge i \ge m$ or $l \le j < 0$. Both contradict that $(k, l)$ is a cell, so $X$ is empty.

**Termination and the bound.** Let $p = i - j$. At the start $p = -(n - 1)$. Each pass that does not return raises $i$ by one or lowers $j$ by one, so it raises $p$ by exactly one. A pass runs only when $i \le m - 1$ and $j \ge 0$, so $p \le m - 1$ at the start of each pass. The values of $p$ at the starts of the passes are distinct integers in $[-(n-1), m-1]$, and there are $m + n - 1$ such integers. So the loop makes at most $m + n - 1$ passes, and each pass reads one cell. When $m = 0$ or $n = 0$ the test of line L2 fails at once and no cell is read.

**Which copy is returned.** Assume $X$ is not empty and the walk returns $(i, j)$. By the invariant, every cell of $X$ has row $\ge i$, so $i$ is the smallest row that holds $x$, and every cell of $X$ in row $i$ has column $\le j$, so $j$ is the largest column of $x$ in row $i$. $\blacksquare$
