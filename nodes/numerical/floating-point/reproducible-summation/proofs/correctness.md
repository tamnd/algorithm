---
title: K-fold summation is exact in every fold, hence order independent, with a bounded error
proves: [correctness]
status: full
---

**Setting.** Binary floating point with precision $p \ge 4$ and round to nearest under any tie rule. $x_1, \ldots, x_n$ are finite floats, not all zero, with $2 \le 2n \le 2^{p-1}$. Let $m = \max_i |x_i|$, $c = \lceil \log_2 n \rceil + 1$ and $M_j = 2^{a_j}$ with $a_j = \lceil \log_2 m \rceil + c + (j - 1)(c - p)$. Assume no overflow ($M_1 \le 2^{e_{\max}}$) and $a_K \ge e_{\min} + 1$, so that every unit $M_j 2^{-p}$ is at least the smallest subnormal $2^{e_{\min} - p + 1}$ and $M_j/2$ is normal. (The implementation keeps this second condition by clamping, which is treated in Step 6.) We use two facts.

- **(F1) Sterbenz.** If $a, b$ are floats with $b/2 \le a \le 2b$, then $a - b$ is a float.
- **(F2)** If $a, b$ are floats and $s = \mathrm{fl}(a + b)$, then $a + b - s$ is a float. This holds with or without underflow.

**Theorem.** Let $v^{(1)}_i = x_i$, and for $j = 1, \ldots, K$ let $q^{(j)}_i = \mathrm{fl}(\mathrm{fl}(M_j + v^{(j)}_i) - M_j)$ and $v^{(j+1)}_i = \mathrm{fl}(v^{(j)}_i - q^{(j)}_i)$. Then:

1. $q^{(j)}_i = s - M_j$ and $v^{(j+1)}_i = v^{(j)}_i - q^{(j)}_i$ exactly, where $s = \mathrm{fl}(M_j + v^{(j)}_i)$.
2. For every order of $i$, line L9 computes $T_j = \sum_i q^{(j)}_i$ exactly. So $T_j$ depends only on the multiset $\{x_i\}$. The same holds when the index set is partitioned, each part is summed separately, and the part sums are added in any order.
3. $\bigl|\sum_i x_i - \sum_j T_j\bigr| \le n M_K 2^{-p} < 2nm\,(4n 2^{-p})^{K}$.

**Step 1 (input bound).** We show $|v^{(j)}_i| \le M_j / (2n)$ for all $j \le K$. For $j = 1$, $m \le 2^{\lceil \log_2 m \rceil}$ and $2n \le 2^{c}$, so $2nm \le M_1$. For $j \ge 1$, Step 3 below gives $|v^{(j+1)}_i| \le M_j 2^{-p} = M_{j+1} 2^{-c} \le M_{j+1}/(2n)$. The argument is an induction on $j$, in which Steps 2 and 3 use only the bound for the current $j$.

**Step 2 (exact extraction).** Fix $j$ and $i$, and write $M = M_j$, $v = v^{(j)}_i$. Since $|v| \le M/(2n) \le M/2$, we have $M/2 \le M + v \le 3M/2$. The numbers $M/2$ and $3M/2$ are floats, because $p \ge 2$ and $M/2$ is normal. Rounding is monotone, so $s = \mathrm{fl}(M + v) \in [M/2, 3M/2]$. By (F1), $s - M$ is a float, so $q = s - M$ exactly. Then $v - q = (M + v) - s$, which is a float by (F2), so $\mathrm{fl}(v - q) = v - q$. This proves part 1.

**Step 3 (sizes and grid).** Every float in $[M/2, 2M)$ is a multiple of $\mathrm{ulp}(M/2) = M 2^{-p}$, and so is $M$. Hence $q = s - M$ is an integer multiple of $U = M 2^{-p}$. The residual is the rounding error of $M + v$, so $|v - q| \le \tfrac12 \mathrm{ulp}(s) \le \tfrac12 \cdot 2M 2^{-p} = U$, because $s < 2M$ gives $\mathrm{ulp}(s) \le 2U$. So $|q| \le |v| + U \le M/(2n) + U$.

**Step 4 (exact accumulation).** Let $A$ be any subset of the indices. Then $\bigl|\sum_{i \in A} q^{(j)}_i\bigr| \le n\bigl(M/(2n) + U\bigr) = M/2 + nU \le M$, since $nU = n M 2^{-p} \le M/2$ by $2n \le 2^{p-1}$. The sum is an integer multiple of $U$ of magnitude at most $M = 2^{p} U$. Every such number is a float: it is $kU$ with $|k| \le 2^{p}$, and $U \ge 2^{e_{\min} - p + 1}$. Every partial sum formed in L9, in any order and over any partition, is such a subset sum. So every addition in L9 is exact, and the final $T_j$ equals $\sum_i q^{(j)}_i$. This proves part 2.

**Step 5 (error).** By part 1, $x_i = \sum_{j=1}^{K} q^{(j)}_i + v^{(K+1)}_i$ for each $i$. Summing over $i$, $\sum_i x_i = \sum_j T_j + E$ with $E = \sum_i v^{(K+1)}_i$, and by Step 3, $|E| \le n M_K 2^{-p}$. For the explicit form, $2^{\lceil \log_2 m \rceil} < 2m$ and $2^{c} < 4n$ give $M_1 < 8nm$, and $2^{c - p} < 4n 2^{-p}$. So $M_K < 8nm (4n 2^{-p})^{K-1}$, and $n M_K 2^{-p} < 2nm (4n 2^{-p})^{K}$. This proves part 3.

**Step 6 (the clamped bottom level).** The implementation never uses an exponent below $e_{\min} + 1$. If $a_j$ would fall below it, it uses $a_j = e_{\min} + 1$ instead. A larger boundary keeps Step 1 true, since $|v| \le M_{j-1}2^{-p} \le 2^{e_{\min}+1}/(2n)$ whenever $a_{j-1} + c - p \le e_{\min} + 1$. With $M = 2^{e_{\min} + 1}$ the unit is $U = 2^{e_{\min} - p + 1}$, the smallest subnormal. After that level every residual is $0$ or $\pm U$. The final level uses $M = 0$, so $q = v$ exactly and $v^{(K+1)} = 0$. Its partial sums are multiples of $U$ of magnitude at most $nU \le 2^{p} U$, so they are floats. Parts 1 and 2 hold for this level, and part 3 holds with $E = 0$.

**Corollary.** The returned value $\mathrm{fl}(T_1 + \mathrm{fl}(T_2 + \cdots))$ is computed from the $T_j$ in a fixed order. So it is the same for every order and partition of the input. By the standard model, $|R - \sum_j T_j| \le \gamma_{K-1}\sum_j |T_j|$, and with part 3,
$$
\Bigl|R - \sum_i x_i\Bigr| \le \gamma_{K-1}\sum_j |T_j| + n M_K 2^{-p}. \qquad \blacksquare
$$
