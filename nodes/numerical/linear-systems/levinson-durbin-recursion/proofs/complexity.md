---
title: Cost of the Levinson-Durbin recursion
proves: [time.worst, time.best, space.extra, flops.worst]
status: full
---

Count flops for $r_0 = 1$ (otherwise line L6 adds $2 n - 1$ divisions).

**Levinson step $k$** ($1 \le k \le n - 1$). Line L9: $3$ flops. Line L10: $k$ multiplications, $k$ subtractions, $1$ division, so $2k + 1$. Line L11: $k$ multiplications and $k$ additions, $2k$. For $k < n - 1$, lines L12 and L13: $2k + 1$ and $2k$. So steps $1, \ldots, n - 2$ cost $8k + 5$ and step $n - 1$ costs $4(n - 1) + 4$. The total is
$$\sum_{k=1}^{n-2} (8k + 5) + 4n = 4(n - 2)(n - 1) + 5(n - 2) + 4 n = 4 n^2 - 3 n - 2.$$

**Durbin, order $n$.** Step $k$ costs $3 + (2k + 1) + 2k = 4k + 4$, for $k = 1, \ldots, n - 1$: $2n(n - 1) + 4(n - 1) = 2 n^2 + 2 n - 4$.

**Time.** Every step $k$ does $\Theta(k)$ work regardless of the data, so the time is $\Theta(n^2)$ in the best and the worst case.

**Space.** The vectors $x$, $y$ and the new $y$ (and new $x$) have length at most $n$, and $r$ and $b$ are copied once: $\Theta(n)$ extra storage. $\blacksquare$
