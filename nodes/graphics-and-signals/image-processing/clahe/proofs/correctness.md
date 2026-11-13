---
title: CLAHE keeps each tile count, bounds each bin, and blends monotone tables into a valid image
proves: [correctness]
status: full
---

The image $I$ has $W \times H$ pixels with values in $\{0, \ldots, L-1\}$, $L \ge 2$. It is cut into $n_x \times n_y$ tiles of $t_w \times t_h$ pixels, with $W = n_x t_w$ and $H = n_y t_h$, so each tile has $n = t_w t_h$ pixels. The clip limit is $\beta \ge 1$, an integer.

**Claim 1 (the clip keeps the count).** After lines L4 to L6 for one tile, the histogram $h'$ satisfies $\sum_k h'[k] = n$, $h'[k] \ge \min(h[k], \beta)$ for each $k$, and $\max_k h'[k] \le \beta + q + 1$, where $q = \lfloor E/L \rfloor$. If $E = 0$, then $h' = h$.

*Proof.* Line L2 counts each pixel of the tile once, so $\sum_k h[k] = n$. Line L4 sets $E = \sum_k \max(h[k] - \beta, 0)$ and replaces $h[k]$ by $\min(h[k], \beta)$. Since $h[k] = \min(h[k], \beta) + \max(h[k] - \beta, 0)$ for each $k$, the sum after line L4 is $n - E$. Line L5 writes $E = qL + r$ with $0 \le r < L$ and adds $q$ to each of the $L$ bins, so the sum is $n - E + qL$. Line L6 adds 1 at the $r$ indices $j_m = \lfloor mL/r \rfloor$, $0 \le m < r$. These indices lie in $\{0, \ldots, L-1\}$ because $mL/r < L$. They are distinct: for $m < m'$, $m'L/r - mL/r \ge L/r > 1$, because $r < L$, so the floors differ. So line L6 adds exactly $r$, and the sum is $n - E + qL + r = n$.

Each bin is at least $\min(h[k], \beta)$ because lines L5 and L6 only add. After line L4 each bin is at most $\beta$, line L5 adds $q$, and line L6 adds at most 1 to a bin because the indices are distinct, so each bin is at most $\beta + q + 1$. If $E = 0$, then $h[k] \le \beta$ for each $k$, line L4 changes nothing, and $q = r = 0$. $\square$

**Claim 2 (the tile tables).** Each table $T_{ab}$ of line L7 is nondecreasing, has values in $\{0, \ldots, L-1\}$ and has $T_{ab}[L-1] = L - 1$. Its step is bounded: for $1 \le k \le L-1$,

$$T_{ab}[k] - T_{ab}[k-1] < \frac{(L-1)(\beta + q + 1)}{n} + 1.$$

*Proof.* By Claim 1, $h'$ is a histogram with nonnegative bins and total $n \ge 1$. Line L7 is the table of [histogram equalization](/histogram-equalization/), $T[k] = \lfloor (L-1)c'(k)/n + 1/2 \rfloor$ with $c'$ the cumulative sum of $h'$; its correctness proof shows that it is nondecreasing, in range, and that $T[L-1] = L-1$ when the total is $n$. For the step, write $x_k = (L-1)c'(k)/n + 1/2$. Then $T[k] - T[k-1] = \lfloor x_k \rfloor - \lfloor x_{k-1} \rfloor < x_k - x_{k-1} + 1 = (L-1)h'[k]/n + 1$, and Claim 1 bounds $h'[k]$. $\square$

With no clip the step can be as large as $L - 1$, when one level fills the tile. The clip limit is what bounds the slope of each table, and so the gain applied to small differences such as noise.

**Claim 3 (the weights).** For a pixel column $x$, line L10 computes $u = (x + 1/2)/t_w - 1/2$, $a_0 = \operatorname{clamp}(\lfloor u \rfloor)$, $a_1 = \operatorname{clamp}(\lfloor u \rfloor + 1)$ and $s = u - \lfloor u \rfloor \in [0, 1)$, with clamp to $\{0, \ldots, n_x - 1\}$. Then for any values $V_0, \ldots, V_{n_x - 1}$,

$$(1 - s)V_{a_0} + s V_{a_1} = \sum_{a=0}^{n_x - 1} \Lambda(\bar u - a)\, V_a, \qquad \bar u = \min(\max(u, 0), n_x - 1),\ \Lambda(z) = \max(0, 1 - |z|).$$

*Proof.* Since $x \ge 0$ and $t_w \ge 1$, $u > -1$, so $\lfloor u \rfloor \ge -1$. Three cases. If $u < 0$, then $\lfloor u \rfloor = -1$, so $a_0 = a_1 = 0$ and the left side is $V_0$; also $\bar u = 0$ and the right side is $V_0$. If $u > n_x - 1$, then $\lfloor u \rfloor \ge n_x - 1$, so $a_0 = a_1 = n_x - 1$ and both sides are $V_{n_x - 1}$. Otherwise $0 \le u \le n_x - 1$ and $\bar u = u$. If $u < n_x - 1$, then $a_0 = \lfloor u \rfloor$ and $a_1 = a_0 + 1$ are in range, $\Lambda(u - a_0) = 1 - s$, $\Lambda(u - a_1) = s$, and $\Lambda(u - a) = 0$ for the other $a$. If $u = n_x - 1$, then $s = 0$ and both sides are $V_{n_x - 1}$. $\square$

The same holds for the rows with line L9. So line L12 is the bilinear interpolation of the four nearest tile tables at the tile centers, held constant beyond the outer centers.

**Claim 4 (the output).** For each pixel, $O(x, y) \in \{0, \ldots, L-1\}$. For a fixed position and fixed tables, $O$ is a nondecreasing function of the value $g$. If $n_x = n_y = 1$ and $\beta \ge n$, then $O$ equals the output of global histogram equalization.

*Proof.* The four weights of line L12 are $(1-s)(1-t)$, $s(1-t)$, $(1-s)t$ and $st$. They are nonnegative and sum to $((1-s) + s)((1-t) + t) = 1$. So the value before rounding is a convex combination of four table entries, each in $[0, L-1]$ by Claim 2, and it lies in $[0, L-1]$; rounding halves up keeps it in $\{0, \ldots, L-1\}$. Each table is nondecreasing in $g$, the weights do not depend on $g$, and rounding is nondecreasing, so $O$ is nondecreasing in $g$.

With one tile, $a_0 = a_1 = b_0 = b_1 = 0$ for every pixel, so $O(x, y) = \operatorname{round}(T_{00}[g]) = T_{00}[g]$. The tile is the whole image. If $\beta \ge n$, then no bin exceeds $\beta$, so $E = 0$ and $h' = h$ by Claim 1, and $T_{00}$ is the global equalization table. $\blacksquare$
