---
title: Zeilberger's algorithm returns a telescoper of least order
proves: [correctness]
status: full
---

**Setting.** $K$ is a field of characteristic $0$ (in the code, $K = \mathbb{Q}$), and $\mathbb{F} = K(n)$. The summand is
$$F(n, k) = \mathrm{poly}(n, k)\, x^k \prod_i (a_i n + b_i k + c_i)!^{e_i}$$
with $\mathrm{poly} \in K[n, k]$, $x \in K^*$, integers $a_i, b_i, c_i$ and $e_i = \pm 1$. A *telescoper of order $J$ with rational certificate* is a vector $(\alpha_0, \ldots, \alpha_J) \in \mathbb{F}^{J+1}$, not all zero, together with $R \in K(n, k)$, such that
$$\sum_{j=0}^{J} \alpha_j F(n + j, k) = G(n, k + 1) - G(n, k), \qquad G = R F. \tag{1}$$
Identity (1) is an identity of hypergeometric terms: after division by $F(n, k)$ it is an identity of rational functions in $n$ and $k$.

**Theorem.** (a) If the algorithm returns $(J, a_0, \ldots, a_J, R)$, then the $a_j$ are polynomials in $n$, not all zero, and (1) holds. (b) $J$ is the least order for which a telescoper with rational certificate exists. (c) If the summand is $0$, the output is $J = 0$, $a_0 = 1$ and $G = 0$.

Part (c) is the first line of the code. From now on $\mathrm{poly} \ne 0$.

## Lemma 1 (step L2)

For $0 \le j \le J$, $F(n + j, k) = H(k)\, \varphi_j(k)$ with $\varphi_j \in K[n][k]$, where $H(k) = x^k \prod_i (a_i n + b_i k + c_i')!^{e_i}$ with $c_i' = c_i + \min(0, a_i J)$ if $e_i = 1$ and $c_i' = c_i + \max(0, a_i J)$ if $e_i = -1$. Also $H(k + 1) / H(k) = \mathrm{num}(k) / \mathrm{den}(k)$, where num and den are a constant times a product of monic linear factors $k + u(n)$, with $u$ of degree at most $1$ in $n$.

*Proof.* Write $L = a_i n + b_i k$. If $e_i = 1$, then $c_i + a_i j \ge c_i'$, and $(L + c_i + a_i j)! = (L + c_i')! \prod_{l = c_i' + 1}^{c_i + a_i j} (L + l)$. If $e_i = -1$, then $c_i + a_i j \le c_i'$, and $1 / (L + c_i + a_i j)! = \bigl(1 / (L + c_i')!\bigr) \prod_{l = c_i + a_i j + 1}^{c_i'} (L + l)$. In both cases the extra factor is a polynomial, and $\varphi_j$ is $\mathrm{poly}(n + j, k)$ times these products. For the ratio, $(L + b_i + c)! / (L + c)!$ is $\prod_{l=1}^{b_i} (L + c + l)$ if $b_i > 0$, the inverse of $\prod_{l=0}^{-b_i - 1} (L + c - l)$ if $b_i < 0$, and $1$ if $b_i = 0$. Each factor $a_i n + b_i k + c$ with $b_i \ne 0$ is $b_i (k + u)$ with $u = (a_i n + c) / b_i$. For $e_i = -1$ the factor moves to the other side. $\square$

## Lemma 2 (step L3)

The output $q, r, c$ of the Gosper-Petkovšek step satisfies
$$\frac{H(k + 1)}{H(k)} = \frac{q(k)}{r(k + 1)} \cdot \frac{c(k + 1)}{c(k)}, \tag{2}$$
with $q, r, c \in K[n][k]$, and $\gcd(q(k), r(k + h)) = 1$ in $\mathbb{F}[k]$ for every integer $h \ge 1$.

*Proof.* Start with $q = \mathrm{num}$, $r(k) = \mathrm{den}(k - 1)$ and $c = 1$. Then (2) holds. A step removes a factor $k + u$ from $q$ and a factor $k + w$ from $r$ with $u - w = h$, an integer $h \ge 1$, and multiplies $c$ by $C(k) = \prod_{i=1}^{h-1} (k + u - i)$. The removed part of $q(k)/r(k+1)$ is $(k + u)/(k + 1 + u - h)$. A direct computation gives
$$\frac{C(k + 1)}{C(k)} = \frac{\prod_{i=1}^{h-1} (k + u + 1 - i)}{\prod_{i=1}^{h-1} (k + u - i)} = \frac{k + u}{k + u + 1 - h},$$
so (2) still holds. Each step removes two factors, so the loop stops. When it stops, no pair $u, w$ has $u - w \in \{1, 2, \ldots\}$. Over $\mathbb{F}$, $q(k)$ and $r(k + h)$ are products of monic linear factors $k + u$ and $k + w + h$. They have a common factor exactly when some $u = w + h$, that is, $u - w = h$. So the gcd condition holds. $\square$

## Lemma 3 (steps L4 to L6, the parametrized Gosper equation)

Fix $\alpha \in \mathbb{F}^{J+1}$, let $t(k) = \sum_j \alpha_j F(n + j, k)$ and $P(k) = c(k) \sum_j \alpha_j \varphi_j(k)$. If $f \in \mathbb{F}[k]$ satisfies
$$q(k) f(k + 1) - r(k) f(k) = P(k), \tag{3}$$
then $G = R F$ with $R = r(k) f(k) / (c(k) \varphi_0(k))$ satisfies (1). Conversely, if (1) holds for $\alpha$ with some rational $R$, then (3) has a polynomial solution of degree at most the bound $D$ of L5.

*Proof.* By Lemma 1, $t = H \cdot P / c$. If $P = 0$, then $t = 0$ and $f = 0$ solves (3), and $R = 0$ satisfies (1). Let $P \ne 0$. By (2), $t(k + 1) / t(k) = \bigl(P(k + 1) / P(k)\bigr) \cdot q(k) / r(k + 1)$. Put $z(k) = r(k) f(k) t(k) / P(k)$. Then
$$z(k + 1) - z(k) = \frac{t(k)}{P(k)} \Bigl( r(k + 1) f(k + 1) \frac{P(k)\, t(k + 1)}{P(k + 1)\, t(k)} - r(k) f(k) \Bigr) = \frac{t(k)}{P(k)} \bigl( q(k) f(k + 1) - r(k) f(k) \bigr) = t(k).$$
Also $z = r f H / c = R F$, since $F = H \varphi_0$. This proves the first claim.

For the converse, (1) says that $t$ has the antidifference $G = R F$, a rational multiple of $t$ when $t \ne 0$. With the representation of $t$'s ratio above and the gcd condition of Lemma 2, Gosper's theorem says that then (3) has a polynomial solution $f$, of degree $\deg P - \max(\deg q, \deg r)$ if $\deg q \ne \deg r$ or $\mathrm{LC}(q) \ne \mathrm{LC}(r)$, and otherwise of degree $\deg P - \deg q + 1$ or $s = (r_{d-1} - q_{d-1}) / \mathrm{LC}(q)$, where $r_{d-1}$ and $q_{d-1}$ are the coefficients of $k^{d-1}$. The second option is possible only if $s$ is a nonnegative integer. The proof is the comparison of the two top coefficients of (3) (Petkovšek, Wilf and Zeilberger, A = B, Chapter 5, and the page on Gosper's algorithm). Here the leading coefficients of $q$ and $r$ lie in $K$, and $s \in \mathbb{F}$ is an integer only if it is a constant. L5 uses $\deg P \le \max_j \deg(c \varphi_j)$, and the bound is increasing in $\deg P$, so the true degree is at most $D$. If $D < 0$, only $f = 0$ is possible, and the code then allows no $f$ unknowns. $\square$

## Lemma 4 (step L7)

The vectors returned by the fraction-free elimination form a basis of the kernel over $\mathbb{F}$ of the coefficient matrix of (3), with unknowns $(\alpha_0, \ldots, \alpha_J, f_0, \ldots, f_D)$.

*Proof.* Row $i$ is replaced by $p \cdot \mathrm{row}_i - m \cdot \mathrm{row}_r$ with the pivot $p \ne 0$, and then divided by a nonzero polynomial. Both operations are invertible over $\mathbb{F}$, and they keep the row space and so the kernel. Swaps also keep it. At the end, every pivot column has a single nonzero entry $M_{i, c_i}$ in its row $i$, and the rows below are zero. For a free column, the vector with $1$ there, $0$ in the other free columns and $-M_{i, \mathrm{free}} / M_{i, c_i}$ in pivot column $c_i$ satisfies every row. These vectors are independent, one for each free column, and the kernel has dimension equal to the number of free columns. $\square$

## Proof of the theorem

(a) The equations of L6 are the coefficients in $k$ of (3), and they are linear in the unknowns. A kernel vector with some $\alpha_j \ne 0$ gives, by Lemma 3, a solution of (1) with $R = r f / (c \varphi_0)$. The code multiplies the vector by a common denominator $L(n)$ and then divides the $\alpha$ part by its content $g(n)$. This multiplies the whole vector by $L / g \in \mathbb{F}^*$, and (3) and (1) are linear, so they still hold with $f$ replaced by $f / g$. That is why $g$ appears in the denominator of $R$. A final scaling by a nonzero rational number does not change this. So the $a_j$ are polynomials, not all zero, and (1) holds.

(b) Suppose some order $J' < J$ has a telescoper with rational certificate. By the converse in Lemma 3 at order $J'$, (3) has a solution with $\deg f \le D$, so the system of L6 at order $J'$ has a kernel vector with $\alpha \ne 0$, and by Lemma 4 the basis of L7 contains a vector with a nonzero $\alpha$ part (the kernel vectors with $\alpha = 0$ form a subspace, and a basis of the whole kernel cannot lie in it). So the algorithm would have stopped at order $J'$, a contradiction. $\blacksquare$

**Termination.** For a proper hypergeometric term, a telescoper with rational certificate exists. This is the fundamental theorem of Wilf and Zeilberger (Inventiones 1992; A = B, Chapter 4 and Chapter 6), which gives a $k$-free recurrence for $F$, and a $k$-free recurrence yields a telescoper. By (b) the algorithm then stops at an order at most that bound. The parameter `max_order` only cuts the search short. The code returns `None` when it is reached, and that says nothing about larger orders.
