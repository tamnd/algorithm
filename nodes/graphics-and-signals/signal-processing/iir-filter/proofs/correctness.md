---
title: The transposed direct form solves the difference equation, and the step-down test decides stability
proves: [correctness]
status: full
---

We assume $a[0] = 1$ and that $b$ and $a$ are padded to length $P + 1$. We write $x[i] = y[i] = 0$ for $i < 0$. The output $y$ is defined by the difference equation $y[n] = \sum_{k=0}^{P} b[k]\, x[n-k] - \sum_{k=1}^{P} a[k]\, y[n-k]$ for $n \ge 0$, which has exactly one solution because each $y[n]$ is given by earlier values.

For $i = 0, \ldots, P - 1$ and $n \ge 0$ let

$$S_i(n) = \sum_{k=i+1}^{P} \big(b[k]\, x[n+i-k] - a[k]\, y[n+i-k]\big).$$

**Lemma 1 (the state).** At the start of the step for $x[n]$, that is just before line L3, $z[i] = S_i(n)$ for each $i$.

*Proof.* By induction on $n$. For $n = 0$, every index $n + i - k$ with $k \ge i + 1$ is negative, so $S_i(0) = 0$, and line L1 sets $z[i] = 0$.

Assume the statement for $n$. Line L3 computes $out = b[0]\, x[n] + S_0(n) = \sum_{k=0}^{P} b[k]\, x[n-k] - \sum_{k=1}^{P} a[k]\, y[n-k] = y[n]$. Line L5, for $i$ from 0 to $P - 2$, reads $z[i+1]$ before it is written, because the loop writes only $z[0], \ldots, z[i]$ up to that point. So it sets

$$z[i] = b[i+1]\, x[n] - a[i+1]\, y[n] + S_{i+1}(n).$$

Now $S_{i+1}(n) = \sum_{k=i+2}^{P} \big(b[k]\, x[n+1+i-k] - a[k]\, y[n+1+i-k]\big)$, and the term $k = i + 1$ of $S_i(n+1)$ is $b[i+1]\, x[n] - a[i+1]\, y[n]$. So the new $z[i]$ is $S_i(n+1)$. Line L6 sets $z[P-1] = b[P]\, x[n] - a[P]\, y[n]$, which is $S_{P-1}(n+1)$, a sum with the single term $k = P$. $\square$

**Theorem 1.** Line L7 of the step for $x[n]$ outputs $y[n]$.

*Proof.* This is the computation of line L3 in the proof of Lemma 1. $\blacksquare$

**Stability.** Let $A(z) = \sum_{k=0}^{p} c[k] z^{-k}$ with $c[0] = 1$, and let $Q(z) = z^p A(z) = \sum_k c[k] z^{p-k}$. Its reversed polynomial is $\tilde Q(z) = z^p Q(1/z) = \sum_k c[k] z^k$. For real coefficients, $|\tilde Q(z)| = |Q(z)|$ on $|z| = 1$.

**Lemma 2 (one step down).** Let $k_p = c[p]$ with $|k_p| < 1$, and let $R(z) = (Q(z) - k_p \tilde Q(z))/(1 - k_p^2)$. Then $R$ has degree at most $p$, its coefficient of $z^0$ is zero, so $R(z) = z\, Q'(z)$ for a polynomial $Q'$ of degree $p - 1$ with leading coefficient 1, and the coefficients of $Q'$ are $c'[i] = (c[i] - k_p c[p-i])/(1 - k_p^2)$. The polynomial $Q$ has all its roots in $|z| < 1$ if and only if $Q'$ has.

*Proof.* The coefficient of $z^{p-i}$ in $Q - k_p \tilde Q$ is $c[i] - k_p c[p-i]$. For $i = p$ it is $c[p] - k_p c[0] = 0$, and for $i = 0$ it is $1 - k_p^2$, so after the division the leading coefficient is 1. This gives the formula for $c'$.

On the circle $|z| = 1$ we have $|k_p \tilde Q(z)| = |k_p|\, |Q(z)| < |Q(z)|$ wherever $Q(z) \ne 0$. If $Q$ has a root on the circle, so does $\tilde Q$, hence $R$ and $Q'$ do, and both sides of the claim are false. Otherwise, by Rouché's theorem, $Q$ and $Q - k_p \tilde Q$ have the same number of roots in $|z| < 1$. The polynomial $Q - k_p \tilde Q = (1 - k_p^2)\, z\, Q'(z)$ has the root $z = 0$ and the roots of $Q'$. So $Q$ has all its $p$ roots inside if and only if $Q'$ has all its $p - 1$ roots inside. $\square$

**Lemma 3 (the first coefficient).** If all roots $r_1, \ldots, r_p$ of $Q$ are in $|z| < 1$, then $|c[p]| < 1$.

*Proof.* $c[p] = (-1)^p r_1 \cdots r_p$, a product of numbers of modulus below 1. $\square$

**Theorem 2.** The step-down recursion reports "stable" (all $|k_j| < 1$) if and only if all roots of $z^P A(z)$ are in $|z| < 1$.

*Proof.* By induction on the degree $p$. For $p = 0$ the claim is empty. If the recursion stops with $|k_p| \ge 1$, Lemma 3 shows that some root is not inside. Else Lemma 2 reduces the claim for $Q$ to the claim for $Q'$ of degree $p - 1$, which holds by the induction hypothesis. $\blacksquare$

**Theorem 3 (BIBO).** If $B$ and $A$ have no common root, the filter is BIBO stable if and only if all poles, the roots of $z^P A(z)$, are in $|z| < 1$.

*Proof.* By partial fractions, $h[n]$ is, for $n$ larger than $P$, a sum of terms $q_j(n)\, r_j^n$ over the distinct poles $r_j$, with nonzero polynomials $q_j$ of degree below the multiplicity of $r_j$. If all $|r_j| < 1$, each term is summable, so $\sum_n |h[n]| < \infty$, and an LTI system with an absolutely summable impulse response is BIBO stable. If some $|r_j| \ge 1$, let $\rho \ge 1$ be the largest pole modulus and $d$ the largest degree of $q_j$ among the poles of modulus $\rho$. Then $h[n] / (n^d \rho^n) = \sum_j c_j e^{i\theta_j n} + o(1)$, where the sum runs over those poles $r_j = \rho e^{i\theta_j}$ with $\deg q_j = d$, and the $c_j$ are nonzero. A sum of this form with distinct $\theta_j$ has the mean square $\sum_j |c_j|^2 > 0$ over long blocks of $n$, so it does not tend to 0. So $h[n]$ does not tend to 0, so $\sum_n |h[n]|$ is infinite, and the bounded input $x[m] = \operatorname{sign}(h[n - m])$ for $0 \le m \le n$ gives $y[n] = \sum_{m=0}^{n} |h[m]|$, which is unbounded in $n$. $\blacksquare$
