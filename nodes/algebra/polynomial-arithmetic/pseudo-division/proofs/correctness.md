---
title: Pseudo-division returns q and r with lc(g)^(m - n + 1) f = q g + r and deg r < n
proves: [correctness]
status: full
---

Let $R$ be a commutative ring, $f, g \in R[x]$ with $g \ne 0$, $m = \deg f$, $n = \deg g$, $\ell = \operatorname{lc}(g)$ and $g = \sum_{j=0}^{n} g_j x^j$, so $g_n = \ell$.

**The case $m < n$.** Line L2 returns $(0, f)$. Here $\delta = 0$, and $\ell^0 f = 0 \cdot g + f$ with $\deg f < n$. If $f = 0$, then $m = -\infty < n$ and the same holds.

**The case $m \ge n$.** Let $d = m - n \ge 0$. Write $r^{(k)}$ for the value of the array $r$, read as a polynomial, before step $k$ of line L4, for $k = d, d - 1, \ldots, 0$, and $r^{(-1)}$ for its value after step $0$. Let

$$Q_k = \sum_{i = k + 1}^{d} t_i\, \ell^{\,i - k - 1} x^i .$$

**Invariant.** For each $k$ from $d$ down to $-1$:

1. $\ell^{d - k} f = Q_k\, g + r^{(k)}$;
2. every coefficient of $r^{(k)}$ at a position $j > n + k$ is $0$.

*Initialization ($k = d$).* $Q_d = 0$ and $r^{(d)} = f$, so part 1 reads $f = f$. Part 2 holds because $\deg f = m = n + d$.

*Maintenance.* Assume the invariant for $k \ge 0$. Line L5 sets $t_k$ to the coefficient of $x^{n + k}$ in $r^{(k)}$. Lines L6 and L7 change the positions $0, \ldots, n + k - 1$, and line L8 sets position $n + k$ to $0$. The positions above $n + k$ are not changed and stay $0$ by part 2.

We claim that $r^{(k-1)} = \ell\, r^{(k)} - t_k x^k g$. At a position $j < n + k$, the coefficient of $\ell\, r^{(k)}$ is $\ell \cdot r^{(k)}_j$, which line L6 computes, and the coefficient of $t_k x^k g$ is $t_k g_{j - k}$ (taken as $0$ when $j < k$), which line L7 subtracts. At position $n + k$, the coefficient of $\ell\, r^{(k)} - t_k x^k g$ is $\ell t_k - t_k g_n = \ell t_k - t_k \ell = 0$, because $R$ is commutative, and line L8 stores this $0$. At positions above $n + k$, both $r^{(k)}$ and $x^k g$ have zero coefficients. This proves the claim and part 2 for $k - 1$, since now position $n + k$ is $0$ too.

For part 1, multiply the invariant for $k$ by $\ell$:

$$\ell^{d - k + 1} f = \ell Q_k\, g + \ell\, r^{(k)} = (\ell Q_k + t_k x^k)\, g + (\ell\, r^{(k)} - t_k x^k g).$$

The second summand is $r^{(k-1)}$ by the claim, and

$$\ell Q_k + t_k x^k = \sum_{i = k + 1}^{d} t_i\, \ell^{\,i - k} x^i + t_k x^k = \sum_{i = k}^{d} t_i\, \ell^{\,i - k} x^i = Q_{k-1}.$$

So $\ell^{d - (k - 1)} f = Q_{k-1}\, g + r^{(k-1)}$.

*End.* For $k = -1$ the invariant gives $\ell^{d + 1} f = Q_{-1}\, g + r^{(-1)}$ with $Q_{-1} = \sum_{i=0}^{d} t_i \ell^i x^i$, and $r^{(-1)}$ has zero coefficients at all positions $j > n - 1$, that is $\deg r^{(-1)} < n$. Line L9 computes the coefficients $q_k = t_k \ell^k$ of $Q_{-1}$, with $\ell^k$ obtained by repeated multiplication, and line L10 returns $r^{(-1)}$ truncated to positions $0, \ldots, n - 1$, which loses only zero coefficients. Stripping zero top coefficients does not change either polynomial. Since $d + 1 = m - n + 1 = \delta$, the output satisfies $\ell^{\delta} f = q g + r$ with $\deg r < n$.

*Termination.* The loop of line L4 runs $d + 1$ times, and each inner loop is finite. $\blacksquare$
