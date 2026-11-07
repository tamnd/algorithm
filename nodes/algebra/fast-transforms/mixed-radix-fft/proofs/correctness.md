---
title: MIXED-RADIX-FFT computes the DFT of length r_1 ⋯ r_t with n Σ (r_i − 1) additions and at most as many multiplications
proves: [correctness, complexity]
status: full
---

**Statement.** Let $R$ be a commutative ring, $t \ge 0$, $r_1, \ldots, r_t \ge 2$ integers, $n = r_1 \cdots r_t$, and $\omega \in R$ with $\omega^n = 1$. For every $x \in R^n$, MIXED-RADIX-FFT$(x, \omega, (r_1, \ldots, r_t))$ returns $X$ with $X_k = \sum_{j=0}^{n-1} x_j \omega^{jk}$ for $0 \le k < n$. It does exactly $A(n) = n \sum_{i=1}^{t} (r_i - 1)$ additions and at most $M(n) = n \sum_{i=1}^{t} (r_i - 1)$ multiplications in $R$, with equality for $M$ when every $r_i$ is prime, besides building the table of powers of $\omega$. If moreover $\omega$ is a principal $n$-th root of unity and $n$ is a unit, running it with $\omega^{-1}$ and dividing by $n$ inverts it.

**Lemma 1 (the splitting).** Let $n = r m$, $\omega^n = 1$, and for $0 \le l < r$ let $Y^{(l)}_k = \sum_{q=0}^{m-1} x_{rq+l}\, (\omega^r)^{qk}$ for $0 \le k < m$. Then for $0 \le k < m$ and $0 \le s < r$,

$$X_{k+ms} = \sum_{l=0}^{r-1} \left(\omega^{lk} Y^{(l)}_k\right) (\omega^m)^{ls}.$$

*Proof.* Every $j \in [0, n)$ is uniquely $j = rq + l$ with $0 \le q < m$ and $0 \le l < r$ (division by $r$). So

$$X_{k+ms} = \sum_{l=0}^{r-1} \sum_{q=0}^{m-1} x_{rq+l}\, \omega^{(rq+l)(k+ms)}.$$

Expand the exponent: $(rq + l)(k + ms) = rqk + rqms + lk + lms$. Here $\omega^{rqms} = (\omega^n)^{qs} = 1$, $\omega^{rqk} = (\omega^r)^{qk}$ and $\omega^{lms} = (\omega^m)^{ls}$. Factoring out the terms that do not depend on $q$ gives $\sum_l \omega^{lk} (\omega^m)^{ls} \sum_q x_{rq+l} (\omega^r)^{qk}$, which is the claim. $\square$

**Correctness.** By induction on $t$. If $t = 0$ then $n = 1$, line L2 returns $x$, and $X_0 = x_0 \omega^0 = x_0$. Let $t \ge 1$, $r = r_1$, $m = n/r = r_2 \cdots r_t$. Since $(\omega^r)^m = \omega^n = 1$, the induction hypothesis for the $t - 1$ radices $(r_2, \ldots, r_t)$ shows that line L5 sets $Y^{(l)}$ to the DFT of length $m$ with root $\omega^r$ of the subsequence $(x_{rq+l})_q$, which is the $Y^{(l)}$ of Lemma 1. For fixed $k$, line L7 sets $t_l = \omega^{lk} Y^{(l)}_k$, and line L9 sets $X_{k+ms} = t_0 + \sum_{l \ge 1} \omega^{mls} t_l = \sum_{l} (\omega^m)^{ls} t_l$, because $(\omega^m)^{0 \cdot s} = 1$. By Lemma 1 this is the correct value. The map $(k, s) \mapsto k + ms$ from $[0, m) \times [0, r)$ to $[0, n)$ is a bijection (division by $m$), so every output is written exactly once, by the loops at lines L6 and L8. So the returned vector is $X$.

**Inverse.** If $\omega$ is a principal $n$-th root of unity, so is $\omega^{-1}$, and $\omega^{-n} = 1$, so the program with $\omega^{-1}$ returns $Z_j = \sum_k X_k \omega^{-jk} = \sum_i x_i \sum_k \omega^{(i-j)k} = n x_j$, since the inner sum is $n$ for $i = j$ and $0$ otherwise by principality. Dividing by the unit $n$ gives $x$.

**Operation count.** Let $A_t$ and $M_t$ be the counts for $t$ radices, as functions of the radices. For $t = 0$ both are $0$. For $t \ge 1$, line L5 makes $r$ calls of length $m$, costing $r A_{t-1}(r_2, \ldots, r_t)$ additions. Lines L6 to L9 run for $m$ values of $k$; for each, line L7 does $r - 1$ multiplications ($t_0$ needs none), and line L9 does, for each of the $r$ values of $s$, exactly $r - 1$ additions and one multiplication for each $l \ge 1$ with $ls \not\equiv 0 \pmod r$, as in the implementation, which uses the table entry $\omega^{m (ls \bmod r)}$ and skips the factor $1$. That is $r(r-1)$ additions and at most $(r-1)^2$ multiplications per $k$ (the pairs $l, s \ge 1$), with equality when $r$ is prime, since then $ls \not\equiv 0$ for $1 \le l, s < r$. So the stage costs exactly $m \cdot r (r - 1) = n (r - 1)$ additions and at most $m((r - 1) + (r-1)^2) = m r (r - 1) = n(r - 1)$ multiplications. Hence

$$A_t = n (r_1 - 1) + r_1 A_{t-1}(r_2, \ldots, r_t) \quad\text{with}\quad A_{t-1}(r_2, \ldots, r_t) = m \sum_{i \ge 2} (r_i - 1)$$

by induction, so $A_t = n(r_1 - 1) + r_1 m \sum_{i \ge 2}(r_i - 1) = n \sum_{i=1}^{t} (r_i - 1)$. The same computation with inequalities gives $M_t \le n \sum_i (r_i - 1)$, with equality when every $r_i$ is prime.

**Time and space.** The index arithmetic per counted operation is $O(1)$, and each call does $O(r)$ work besides its stage, so the time is $\Theta(A_t + M_t + \text{number of calls})$. The calls at level $i$ number $n / n_i \le n$, with $n_i = r_i \cdots r_t$, and $t \le \lg n$, so the time is $\Theta(n \sum_i r_i)$, since $n (r_i - 1) \ge n r_i / 2$. The recursion holds at most one partial result per level along the current path, of total size $\sum_i n_i \le 2n$, plus the table of $n$ powers, so the extra space is $\Theta(n)$. $\blacksquare$
