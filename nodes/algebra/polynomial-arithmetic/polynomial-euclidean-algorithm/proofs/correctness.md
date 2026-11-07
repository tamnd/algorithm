---
title: The Euclidean algorithm returns the monic gcd
proves: [correctness]
status: full
---

Let $F$ be a field and $f, g \in F[x]$. For $a, b \in F[x]$ let $D(a, b)$ be the set of common divisors of $a$ and $b$ in $F[x]$.

**Lemma.** If $b \ne 0$ and $a = q b + c$, then $D(a, b) = D(b, c)$.

*Proof.* If $d \mid a$ and $d \mid b$, then $d \mid a - q b = c$. If $d \mid b$ and $d \mid c$, then $d \mid q b + c = a$. $\square$

**Invariant.** Before each test of line L2, $D(r_0, r_1) = D(f, g)$.

*Initialization.* Line L1 only strips zero coefficients, which does not change the polynomials, so $r_0 = f$ and $r_1 = g$.

*Maintenance.* Line L3 runs only when $r_1 \ne 0$. Over a field, $\operatorname{lc}(r_1)$ is a unit, so long division gives $r_0 = q r_1 + c$ with $c = r_0 \operatorname{rem} r_1$ and $\deg c < \deg r_1$ (see the proof for [long division](/polynomial-long-division/)). By the lemma, $D(r_1, c) = D(r_0, r_1) = D(f, g)$, and the new pair is $(r_1, c)$.

**Termination.** Let $d_t$ be $\deg r_1$ before the $t$-th test of line L2, with $\deg 0 = -\infty$. While the loop runs, $r_1 \ne 0$, so $d_t \ge 0$, and line L3 gives $d_{t+1} = \deg(r_0 \operatorname{rem} r_1) < d_t$. A strictly decreasing sequence of integers that are at least $0$ has at most $d_1 + 1$ terms, so after at most $\deg g + 1$ passes the new remainder is $0$ and the loop stops. If $g = 0$, it stops at once.

**Result.** When the loop stops, $r_1 = 0$ and $D(f, g) = D(r_0, 0)$, the set of divisors of $r_0$.

- If $r_0 = 0$, every polynomial is in $D(f, g)$, so $f = g = 0$, and line L4 returns $0 = \gcd(0, 0)$.
- If $r_0 \ne 0$, then $r_0$ divides itself, so $r_0 \in D(f, g)$, and every $d \in D(f, g)$ divides $r_0$. So $r_0$ is a gcd of $f$ and $g$. Lines L5 and L6 multiply it by the unit $u = \operatorname{lc}(r_0)^{-1}$, which does not change the set of its divisors or of its multiples, and give a gcd with leading coefficient $u \operatorname{lc}(r_0) = 1$. The monic gcd is unique, since two gcds divide each other and so differ by a unit factor, and only one unit multiple is monic.

So EUCLID$(f, g)$ returns the monic $\gcd(f, g)$.

**Cost.** Let $m = \deg f \ge n = \deg g \ge 0$ and let $n_1 = n > n_2 > \cdots > n_\ell \ge 0$ be the degrees of the nonzero remainders $r_1 = g, r_2, \ldots, r_\ell$, with $n_0 = m$. The pass that divides $r_{i-1}$ by $r_i$ costs at most $(2 n_i + 1)(n_{i-1} - n_i + 1)$ field operations and one inversion, by the count for long division. Since $2 n_i + 1 \le 2n + 1$ and $\sum_{i=1}^{\ell} (n_{i-1} - n_i + 1) = n_0 - n_\ell + \ell$, the passes cost at most $(2n + 1)(m - n_\ell + \ell)$. The degrees $n_1, \ldots, n_\ell$ are distinct integers in $[0, n]$, so $\ell \le n + 1$, and $n_\ell \ge 0$. This gives at most $(2n + 1)(m + n + 1)$ operations and $n + 1$ inversions for the loop. Lines L5 and L6 add one inversion and $n_\ell + 1 \le n + 1$ multiplications. $\blacksquare$
