---
title: Long division returns the unique quotient and remainder
proves: [correctness]
status: full
---

Let $R$ be a commutative ring, $f, g \in R[x]$, $g \ne 0$, and let the leading coefficient of $g$ be a unit. After line L1, $f = \sum_{i=0}^{m} f_i x^i$ and $g = \sum_{j=0}^{n} g_j x^j$ with $g_n \ne 0$, and $u = g_n^{-1}$ after line L3. For a coefficient array $r$ we write $r$ also for the polynomial $\sum_i r_i x^i$.

**Case $m < n$.** Line L2 returns $(0, f)$. Then $f = 0 \cdot g + f$ and $\deg f < n$. This also covers $f = 0$, where $m = -1$.

**Case $m \ge n$.** We use this invariant of the loop of line L5. Before the step for $k$, with $-1 \le k \le m - n$ (the value $k = -1$ stands for the state after the last step):

$$\text{(I1)}\quad f = Q_k\, g + r, \qquad Q_k = \sum_{i = k+1}^{m-n} q_i x^i, \qquad\qquad \text{(I2)}\quad r_i = 0 \text{ for all } i > n + k .$$

*Initialization.* Before the step for $k = m - n$, line L4 gives $r = f$ and $Q_{m-n} = 0$, so (I1) holds. (I2) says $r_i = 0$ for $i > m$, which is true because $r = f$ has degree $m$.

*Maintenance.* Assume (I1) and (I2) before the step for $k$. Line L6 sets $c = r_{n+k} u$, and line L7 sets $q_k = c$, so $Q_{k-1} = Q_k + c\, x^k$. Lines L8 and L9 replace $r_{j+k}$ by $r_{j+k} - c\, g_j$ for $0 \le j \le n - 1$. Line L10 replaces $r_{n+k}$ by $0$. Since

$$r_{n+k} - c\, g_n = r_{n+k} - r_{n+k}\, u\, g_n = 0,$$

line L10 writes the value $r_{n+k} - c\, g_n$. So the step replaces $r_{j+k}$ by $r_{j+k} - c\, g_j$ for each $0 \le j \le n$ and does not change the other entries, that is, it replaces the polynomial $r$ by $r' = r - c\, x^k g$. Then

$$Q_{k-1}\, g + r' = (Q_k + c\, x^k) g + r - c\, x^k g = Q_k\, g + r = f,$$

which is (I1) for $k - 1$. For (I2) at $k - 1$ we need $r'_i = 0$ for $i > n + k - 1$. For $i > n + k$, the step does not change $r_i$, which is $0$ by (I2). For $i = n + k$, line L10 sets $r'_{n+k} = 0$.

*Termination.* The loop runs exactly $m - n + 1$ times. After the step for $k = 0$, (I1) and (I2) with $k = -1$ give

$$f = q\, g + r, \qquad q = \sum_{i=0}^{m-n} q_i x^i, \qquad r_i = 0 \text{ for } i \ge n .$$

So $r = \sum_{i=0}^{n-1} r_i x^i$, which line L11 returns, and $\deg r < n = \deg g$. Stripping zero top coefficients in line L11 does not change the polynomials $q$ and $r$.

**Uniqueness.** If also $f = q' g + r'$ with $\deg r' < n$, then $(q - q') g = r' - r$ has degree less than $n$. If $q \ne q'$, the coefficient of $x^{\deg(q - q') + n}$ in $(q - q') g$ is $\operatorname{lc}(q - q')\, g_n$, which is not zero because $g_n$ is a unit. So $\deg((q - q')g) \ge n$, a contradiction. Hence $q = q'$ and $r = r'$, and the algorithm returns the unique quotient and remainder of $f$ by $g$.

**Operation count.** Line L3 does one inversion. Each step does one multiplication in line L6 and $n$ multiplications and $n$ subtractions in line L9. Line L10 does no arithmetic. With $m - n + 1$ steps, the total is $(2n + 1)(m - n + 1)$ operations in $R$ and one inversion. $\blacksquare$
