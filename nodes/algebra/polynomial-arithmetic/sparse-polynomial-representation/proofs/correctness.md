---
title: The sparse operations return the normalized term list of the exact result
proves: [correctness]
status: full
---

Let $R$ be a commutative ring. A list $a = [(e_0, c_0), \ldots, (e_{t-1}, c_{t-1})]$ meets (S) when $e_0 < \cdots < e_{t-1}$ and every $c_i \ne 0$, and $\operatorname{val}(a) = \sum_i c_i x^{e_i}$.

**Lemma 1 (uniqueness).** Two lists that meet (S) and have the same value are equal.

*Proof.* The coefficient of $x^k$ in $\operatorname{val}(a)$ is $c_i$ if $k = e_i$ and $0$ if $k$ is not an exponent of $a$, because the exponents are distinct. So the set of exponents of $a$ is the set of $k$ with a nonzero coefficient in $\operatorname{val}(a)$, and the coefficients are the coefficients of $\operatorname{val}(a)$. Both are determined by the value, and the order is fixed by (S). $\square$

So it suffices to show that each operation returns a list that meets (S) and has the right value.

**ADD.** Let $a$ and $b$ meet (S), with $s$ and $t$ terms. Consider the statement $I(i, j)$:

1. $c$ meets (S);
2. $\operatorname{val}(c) = \sum_{k < i} c^a_k x^{e^a_k} + \sum_{k < j} c^b_k x^{e^b_k}$, the sum of the terms already read;
3. every exponent in $c$ is less than $e^a_i$ if $i < s$, and less than $e^b_j$ if $j < t$;
4. the exponents of $a[0 .. i-1]$ and $b[0 .. j-1]$ are all less than $e^a_i$ if $i < s$ and less than $e^b_j$ if $j < t$.

*Initialization.* At line L1, $i = j = 0$ and $c$ is empty, so all four parts hold.

*Maintenance.* Assume $I(i, j)$ at line L2 with $i < s$ and $j < t$.

- Case line L3, $e^a_i < e^b_j$. The term $a[i]$ is appended. By part 3 its exponent is larger than all exponents in $c$, and $c^a_i \ne 0$, so $c$ still meets (S). Part 2 holds for $(i + 1, j)$. For part 3, the new last exponent $e^a_i$ is less than $e^a_{i+1}$ by (S) for $a$, and less than $e^b_j$ by the case. For part 4, $e^a_i < e^a_{i+1}$ and $e^a_i < e^b_j$, and the old terms were already below both bounds, since $e^a_{i+1} > e^a_i$.
- Case line L4 is symmetric.
- Case lines L5 to L8, $e^a_i = e^b_j = e$. The two terms add to $(c^a_i + c^b_j) x^e = u x^e$. If $u \ne 0$, the term $(e, u)$ is appended; its exponent is larger than all of $c$ by part 3, so (S) holds. If $u = 0$, nothing is appended and the value changes by $0$. In both cases part 2 holds for $(i + 1, j + 1)$. Parts 3 and 4 hold because $e < e^a_{i+1}$ and $e < e^b_{j+1}$ by (S) for $a$ and $b$.

*Termination.* Each pass increases $i + j$ by at least $1$, and $i + j \le s + t$, so the loop stops after at most $s + t - 1$ passes, with $i = s$ or $j = t$.

*End.* Say $i = s$ (the case $j = t$ is symmetric). Then line L9 appends $b[j .. t-1]$, and the tail of $a$ is empty. By part 3, every exponent of $c$ is less than $e^b_j$, and the tail is increasing with nonzero coefficients, so the result meets (S). By part 2, its value is $\operatorname{val}(a) + \operatorname{val}(b)$. $\blacksquare$ for ADD.

**MUL.** For each $k$, the final value of $D[k]$ is $\sum u v$ over the pairs of terms $(e, u)$ of $a$ and $(d, v)$ of $b$ with $e + d = k$, since line M4 adds each such product once and no other. This sum is the coefficient of $x^k$ in $\operatorname{val}(a) \operatorname{val}(b) = \sum_{e, d} u v\, x^{e + d}$. Every exponent $k$ with a nonzero coefficient in the product is a key of $D$, because a nonzero sum has a nonzero term. Line M5 returns the keys with $D[k] \ne 0$, each once, in increasing order. So the result meets (S) and has the value of the product.

**EVALUATE.** Let the terms be $(e_0, u_0), \ldots, (e_{t-1}, u_{t-1})$. Claim: before the pass for term $i$ of line E2, $p = z^{\text{prev}}$, $\text{prev} = e_{i-1}$ (or $0$ when $i = 0$) and $y = \sum_{k < i} u_k z^{e_k}$. At line E1 this holds with $p = 1 = z^0$ and $y = 0$. In the pass, $e_i \ge \text{prev}$ by (S) (and $e_0 \ge 0$), so line E3 sets $p = z^{\text{prev}} z^{e_i - \text{prev}} = z^{e_i}$, line E4 sets $\text{prev} = e_i$, and line E5 adds $u_i z^{e_i}$ to $y$. After the last pass, $y = \sum_k u_k z^{e_k} = \operatorname{val}(a)(z)$. Binary powering computes $z^g$ correctly by the identity $z^g = (z^2)^{\lfloor g/2 \rfloor} z^{g \bmod 2}$.

**Derivative and scalar multiple.** Both map the term with exponent $e$ to a term with exponent $e - 1$ or $e$, a strictly increasing map on the exponents, so the order of (S) is kept. Terms whose new coefficient is $0$ are dropped, so the coefficients are nonzero. The value is $\sum_{e \ge 1} e c\, x^{e-1} = \operatorname{val}(a)'$ and $\sum u c\, x^e = u \operatorname{val}(a)$, by linearity. $\blacksquare$
