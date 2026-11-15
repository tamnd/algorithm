---
title: The Jury table decides whether a real polynomial is Schur, and in the regular case the number of negative first-column entries is the number of roots outside the unit circle
proves: [correctness, termination]
status: full
---

Let $p(z) = a_0 z^n + a_1 z^{n-1} + \dots + a_n$ be real with $a_0 > 0$ (line L1 makes $a_0$ positive; multiplying $p$ by $-1$ changes no root). The arithmetic is exact. For a real polynomial $q$ of exact degree $k$, let $q^*(z) = z^k q(1/z)$ be the reversed polynomial (the same coefficients in the opposite order). Write $\mathbb{D} = \{|z| < 1\}$ and $\mathbb{T} = \{|z| = 1\}$. For $q$ with no root on $\mathbb{T}$, $\operatorname{in}(q)$ and $\operatorname{out}(q)$ are the numbers of roots of $q$ in $\mathbb{D}$ and outside $\overline{\mathbb{D}}$, counted with multiplicity, so $\operatorname{in}(q) + \operatorname{out}(q) = \deg q$.

The algorithm computes $p_n = p$ and, while the leading coefficient $c_0$ of $p_k$ is not zero, $\alpha_k = c_k / c_0$ and

$$z\, p_{k-1}(z) = p_k(z) - \alpha_k\, p_k^*(z), \qquad (1)$$

whose coefficients are $c_i - \alpha_k c_{k-i}$, $i = 0, \dots, k-1$ (line L5). The first column is $F = (f_n, f_{n-1}, \dots)$ with $f_k$ the leading coefficient of $p_k$.

## Lemma 1: one step

Let $p_k$ have exact degree $k \ge 1$, leading coefficient $f_k \ne 0$ and constant term $c_k$.

(a) The right side of (1) has constant term $0$, so $p_{k-1}$ is a polynomial of degree at most $k - 1$, and its coefficient of $z^{k-1}$ is $f_{k-1} = f_k (1 - \alpha_k^2)$.

(b) $f_{k-1}$ has the sign of $f_k$ if $|\alpha_k| < 1$, the opposite sign if $|\alpha_k| > 1$, and $f_{k-1} = 0$ if $|\alpha_k| = 1$.

(c) If $p_k$ has no root on $\mathbb{T}$ and $|\alpha_k| \ne 1$, then $p_{k-1}$ has exact degree $k - 1$, no root on $\mathbb{T}$, and

$$\operatorname{out}(p_{k-1}) = \operatorname{out}(p_k) \text{ if } |\alpha_k| < 1, \qquad \operatorname{out}(p_{k-1}) = k - \operatorname{out}(p_k) \text{ if } |\alpha_k| > 1 .$$

*Proof.* (a) The constant term of $p_k^*$ is $f_k$, so the constant term of the right side is $c_k - \alpha_k f_k = 0$. The leading coefficient of $p_k^*$ is $c_k$, so the coefficient of $z^k$ on the right side is $f_k - \alpha_k c_k = f_k - c_k^2 / f_k = f_k(1 - \alpha_k^2)$. (b) follows from (a).

(c) By (b), $f_{k-1} \ne 0$, so $\deg p_{k-1} = k - 1$. For $z \in \mathbb{T}$, $1/z = \bar z$, and since the coefficients are real, $p_k(\bar z) = \overline{p_k(z)}$. So $|p_k^*(z)| = |z^k|\,|p_k(\bar z)| = |p_k(z)|$ on $\mathbb{T}$, and this is positive because $p_k$ has no root on $\mathbb{T}$.

If $|\alpha_k| < 1$, then $|\alpha_k p_k^*(z)| < |p_k(z)|$ on $\mathbb{T}$. So $|z p_{k-1}(z)| \ge (1 - |\alpha_k|)|p_k(z)| > 0$ on $\mathbb{T}$, and by Rouché's theorem $z p_{k-1}$ and $p_k$ have the same number of roots in $\mathbb{D}$. The factor $z$ adds the root $0$, so $\operatorname{in}(p_{k-1}) = \operatorname{in}(p_k) - 1$, and $\operatorname{out}(p_{k-1}) = (k - 1) - \operatorname{in}(p_{k-1}) = k - \operatorname{in}(p_k) = \operatorname{out}(p_k)$.

If $|\alpha_k| > 1$, then $|p_k(z)| < |\alpha_k p_k^*(z)|$ on $\mathbb{T}$, $z p_{k-1}$ has no root on $\mathbb{T}$, and by Rouché's theorem $z p_{k-1}$ has as many roots in $\mathbb{D}$ as $p_k^*$. The roots of $p_k^*$ are the reciprocals $1/\zeta$ of the roots $\zeta$ of $p_k$ (none of which is $0$, because $p_k^*$ has degree $k$ only if $c_k \ne 0$, and $|\alpha_k| > 1$ gives $c_k \ne 0$), with the same multiplicities. So $\operatorname{in}(p_k^*) = \operatorname{out}(p_k)$. Then $\operatorname{in}(p_{k-1}) = \operatorname{out}(p_k) - 1$ and $\operatorname{out}(p_{k-1}) = k - 1 - \operatorname{out}(p_k) + 1 = k - \operatorname{out}(p_k)$. $\square$

## Lemma 2: a root on the circle makes the table singular

If $p$ has a root $\zeta \in \mathbb{T}$, then some entry of $F$ is zero.

*Proof.* Suppose that $p_k(\zeta) = 0$ and $p_k$ has exact degree $k$. Then $p_k^*(\zeta) = \zeta^k p_k(\bar\zeta) = \zeta^k\, \overline{p_k(\zeta)} = 0$, and by (1), $p_{k-1}(\zeta) = 0$ because $\zeta \ne 0$. If no entry of $F$ were zero, every $p_k$ would have exact degree $k$, and by induction $p_0(\zeta) = 0$. But $p_0$ is the nonzero constant $f_0$. This is a contradiction. $\square$

The same argument shows that a pair of roots $\zeta$ and $1/\zeta$ of $p$ (a common root of $p$ and $p^*$) also makes the table singular.

## Theorem

The loop runs at most $n$ times. Let the algorithm return.

(i) If no entry of $F$ is zero (the regular case), then $p$ has no root on $\mathbb{T}$, and the number $N$ of negative entries of $F$ equals $\operatorname{out}(p)$. In particular $p$ is Schur if and only if $N = 0$.

(ii) If some entry of $F$ is zero (the singular case), then $p$ is not Schur.

*Proof.* Termination: each pass lowers the length of the coefficient list by exactly one, so there are at most $n$ passes.

(i) By Lemma 2, $p$ has no root on $\mathbb{T}$. Since every $f_k \ne 0$, Lemma 1(b) gives $|\alpha_k| \ne 1$ for every $k$, and Lemma 1(c) applies at every step. Let $s_k$ be the sign of $f_k$ and let $c_k$ be the number of indices $j < k$ with $s_j \ne s_k$. We show $\operatorname{out}(p_k) = c_k$ by induction on $k$. For $k = 0$, $p_0$ is a nonzero constant, and $\operatorname{out}(p_0) = 0 = c_0$. Let $k \ge 1$.

- If $|\alpha_k| < 1$, then $s_{k-1} = s_k$ by Lemma 1(b), so $c_k = c_{k-1}$, and $\operatorname{out}(p_k) = \operatorname{out}(p_{k-1}) = c_{k-1} = c_k$ by Lemma 1(c).
- If $|\alpha_k| > 1$, then $s_{k-1} = -s_k$. Index $k - 1$ counts in $c_k$, and an index $j < k - 1$ counts in $c_k$ exactly when $s_j = s_{k-1}$. So $c_k = 1 + (k - 1 - c_{k-1}) = k - c_{k-1}$. By Lemma 1(c), $\operatorname{out}(p_k) = k - \operatorname{out}(p_{k-1}) = k - c_{k-1} = c_k$.

For $k = n$, $s_n = +1$ because $a_0 > 0$, so $c_n$ is the number of negative entries of $F$, which is $N$.

(ii) Let $f_{k-1} = 0$ be the first zero entry, so $|\alpha_k| = 1$ and $|c_k| = |f_k|$, where $c_k$ is the constant term of $p_k$. Suppose that $p$ is Schur. Then, by induction with Lemma 1, every $p_j$ with $j \ge k$ is Schur: $p_n = p$ is Schur, and if $p_j$ is Schur then $|\alpha_j| = |c_j / f_j|$ is the product of the moduli of the $j$ roots of $p_j$, which is less than $1$, so Lemma 1(c) gives $\operatorname{out}(p_{j-1}) = \operatorname{out}(p_j) = 0$. But then $|\alpha_k| < 1$, which contradicts $|\alpha_k| = 1$. So $p$ is not Schur. $\square$

## Corollary: the n + 1 conditions of the classic table

For $a_0 > 0$ and $n \ge 2$, $p$ is Schur if and only if $p(1) > 0$, $(-1)^n p(-1) > 0$, and $|\alpha_k| < 1$ for $k = n, n - 1, \dots, 2$.

*Proof.* By the theorem and Lemma 1(b), $p$ is Schur if and only if $|\alpha_k| < 1$ for $k = n, \dots, 1$ (then all $f_k$ are positive). At $z = 1$, (1) gives $p_{k-1}(1) = p_k(1)(1 - \alpha_k)$, because $p_k^*(1) = p_k(1)$. At $z = -1$, $p_k^*(-1) = (-1)^k p_k(-1)$, so $p_{k-1}(-1) = -p_k(-1)(1 - (-1)^k \alpha_k)$. If $|\alpha_k| < 1$ for $k = n, \dots, 2$, the factors $1 \mp \alpha_k$ are positive. Then $p_1(1)$ has the sign of $p(1)$, and $-p_1(-1)$ has the sign of $(-1)^n p(-1)$. The polynomial $p_1(z) = f_1 z + c_1$ has $f_1 > 0$, and $|\alpha_1| = |c_1| / f_1 < 1$ holds if and only if $p_1(1) = f_1 + c_1 > 0$ and $-p_1(-1) = f_1 - c_1 > 0$. So, under $|\alpha_k| < 1$ for $k \ge 2$, the condition $|\alpha_1| < 1$ is equivalent to $p(1) > 0$ and $(-1)^n p(-1) > 0$. If some $|\alpha_k| \ge 1$ with $k \ge 2$, both sides of the claim are false. $\square$

The classic table forms the rows without the division by $c_0$, so each row is a positive or negative multiple of the row above, and the test $|\alpha_k| < 1$ becomes $|\text{first entry}| > |\text{last entry}|$, which does not depend on that factor.
