---
title: Cardano's formula returns the three roots of the cubic with multiplicity
proves: [correctness]
status: full
---

We work in exact complex arithmetic. Let $a \ne 0$ and $f(x) = ax^3 + bx^2 + cx + d$.

**Lemma 1 (the shift).** With $s = b/(3a)$, $C = c/a$, $D = d/a$, $p = C - 3s^2$ and $q = D - sC + 2s^3$, we have $f(t - s) = a(t^3 + pt + q)$ for all $t$.

*Proof.* $f(x)/a = x^3 + 3s x^2 + Cx + D$, since $b/a = 3s$. Put $x = t - s$:
$(t - s)^3 + 3s(t - s)^2 + C(t - s) + D = t^3 - 3st^2 + 3s^2t - s^3 + 3st^2 - 6s^2t + 3s^3 + Ct - Cs + D$. The $t^2$ terms cancel, the $t$ terms give $(C - 3s^2)t = pt$, and the constants give $2s^3 - sC + D = q$. $\square$

So $x$ is a root of $f$ of multiplicity $m$ if and only if $t = x + s$ is a root of $g(t) = t^3 + pt + q$ of multiplicity $m$, and it suffices to show that $t_0, t_1, t_2$ are the roots of $g$ with multiplicity, that is, $g(t) = (t - t_0)(t - t_1)(t - t_2)$.

**Lemma 2 (the quadratic).** The numbers $-q/2 \pm r$ with $r^2 = q^2/4 + p^3/27$ are the two roots of $h(z) = z^2 + qz - p^3/27$. So their sum is $-q$ and their product is $-p^3/27$.

*Proof.* $(z + q/2)^2 - r^2 = z^2 + qz + q^2/4 - q^2/4 - p^3/27 = h(z)$, and $(z + q/2)^2 - r^2 = (z + q/2 - r)(z + q/2 + r)$. Vieta's formulas for a monic quadratic give the sum and product. $\square$

**Case $w = 0$.** Line L4 picks the root of $h$ of larger modulus. If it is $0$, both roots are $0$, so their sum $-q = 0$ and their product $-p^3/27 = 0$, so $p = q = 0$. Then $g(t) = t^3$ has the triple root $0$, and line L5 returns $x = -s$ three times, which is correct by Lemma 1.

**Case $w \ne 0$.** Let $u$ be a cube root of $w$ (line L6), so $u \ne 0$. For $k = 0, 1, 2$ put $u_k = \omega^k u$ and $v_k = -p/(3u_k)$, so that line L9 gives $t_k = u_k + v_k$. Write $v = v_0 = -p/(3u)$. Since $\omega^3 = 1$, $v_k = \omega^{-k}v = \omega^{2k} v$, and $u_k v_k = uv = -p/3$.

*Step 1: $u^3 + v^3 = -q$.* We have $u^3 = w$, one root of $h$, and $v^3 = -p^3/(27u^3) = (-p^3/27)/w$. By Lemma 2, the product of the two roots of $h$ is $-p^3/27$, so $v^3$ is the other root of $h$ (this also holds if the two roots are equal). Their sum is $-q$.

*Step 2: the elementary symmetric functions of $t_0, t_1, t_2$.* Use $1 + \omega + \omega^2 = 0$.

- $t_0 + t_1 + t_2 = u(1 + \omega + \omega^2) + v(1 + \omega^2 + \omega^4) = 0$, since $\omega^4 = \omega$.
- $t_0^2 + t_1^2 + t_2^2 = \sum_k (\omega^{2k}u^2 + 2uv + \omega^{4k}v^2) = u^2 \cdot 0 + 6uv + v^2 \cdot 0 = 6uv$. Hence $e_2 = \sum_{j<k} t_j t_k = \tfrac12\big((\sum t_k)^2 - \sum t_k^2\big) = -3uv = p$.
- $t_0 t_1 t_2 = (u + v)(\omega u + \omega^2 v)(\omega^2 u + \omega v)$. The product of the last two factors is $\omega^3 u^2 + \omega^2 uv + \omega^4 uv + \omega^3 v^2 = u^2 - uv + v^2$, using $\omega^2 + \omega^4 = \omega^2 + \omega = -1$. So $t_0t_1t_2 = (u + v)(u^2 - uv + v^2) = u^3 + v^3 = -q$.

*Step 3.* By Step 2, $(t - t_0)(t - t_1)(t - t_2) = t^3 - (\sum t_k) t^2 + e_2 t - t_0t_1t_2 = t^3 + pt + q = g(t)$. So $t_0, t_1, t_2$ are the roots of $g$ with multiplicity, and by Lemma 1, $x_k = t_k - s$ are the roots of $f$ with multiplicity. $\blacksquare$

**Remark (why line L9 and not a second cube root).** The proof uses $u_k v_k = -p/3$. Two independent cube roots $u'$ of $-q/2 + r$ and $v'$ of $-q/2 - r$ satisfy only $(u'v')^3 = -p^3/27$, so $u'v' = \omega^j(-p/3)$ for some $j \in \{0, 1, 2\}$. If $j \ne 0$ and $p \ne 0$, then $u' + v'$ is in general not a root.

**Remark (the irreducible case).** For real $p, q$ with $q^2/4 + p^3/27 < 0$, $r$ is imaginary and $w$ and $\bar w$ are the two roots of $h$, with $|w|^2 = -p^3/27$. Then $|u|^2 = -p/3$, so $v = -p/(3u) = \bar u$ and $t_k = 2\operatorname{Re}(\omega^k u)$ is real for each $k$. The three roots are real, and the formula reaches them through non-real $u$.
