---
title: EQUAL-DEGREE returns the irreducible factors and stops with probability one
proves: [correctness]
status: full
---

Let $p$ be a prime, $\mathbb{F}_p = \mathbb{Z}/p\mathbb{Z}$, $d \ge 1$, and $f = q_1 \cdots q_r \in \mathbb{F}_p[x]$ with distinct monic irreducible $q_j$ of degree $d$. Let $K = \mathbb{F}_{p^d}$ be a field with $p^d$ elements. For odd $p$, $e = (p^d - 1)/2$. For $p = 2$, $T(y) = y + y^2 + \cdots + y^{2^{d-1}}$.

**Lemma 1 (pieces).** Every polynomial on the stack and in the output is monic and is the product of a nonempty set of the $q_j$, and the sets of all polynomials on the stack and in the output form a partition of $\{q_1, \ldots, q_r\}$.

*Proof.* This holds after line L1. Line L3 removes $h$ and either line L4 moves it to the output, or line L6 or line L9 pushes $g$ and $h/g$, or line L9 pushes $h$ back. In line L6 and line L9, $g$ is a monic divisor of $h$ with $g \ne 1$ and $g \ne h$ (in line L6, $g \ne h$ since $\deg a < \deg h$ and $a \ne 0$). As $h$ is square-free, $g$ is the product of a nonempty proper subset of the factors of $h$, and $h/g$ is the product of the rest. $\square$

**Output.** By Lemma 1, each output $h$ with $\deg h = d$ is a product of $q_j$ of degree $d$, so it is exactly one $q_j$. When the stack is empty, Lemma 1 says that the output is a partition of $\{q_1, \ldots, q_r\}$ into single factors, so it lists each $q_j$ exactly once.

**Lemma 2 (Chinese remainder theorem).** Let $h = q_{j_1} \cdots q_{j_s}$ as in Lemma 1. The map $a \mapsto (a \bmod q_{j_1}, \ldots, a \bmod q_{j_s})$ is a ring isomorphism from $\mathbb{F}_p[x]/(h)$ onto $\prod_{i=1}^s \mathbb{F}_p[x]/(q_{j_i})$, and each factor is a field with $p^d$ elements. So if $a$ is uniform among the polynomials of degree less than $\deg h$, the residues $a_i = a \bmod q_{j_i}$ are independent and uniform in fields with $p^d$ elements.

*Proof.* The $q_{j_i}$ are pairwise coprime, so this is the [Chinese remainder theorem](/chinese-remainder-theorem/) for $\mathbb{F}_p[x]$. Both sides have $p^{\deg h}$ elements, so the bijection maps the uniform distribution to the uniform distribution on the product. Each $q_{j_i}$ is irreducible of degree $d$, so $\mathbb{F}_p[x]/(q_{j_i})$ is a field with $p^d$ elements. $\square$

**Lemma 3 (the values of $b$).** Let $L$ be a field with $p^d$ elements and $y \in L$.

1. If $p$ is odd, then $y^e \in \{0, 1, -1\}$; $y^e = 0$ only for $y = 0$, and $y^e = 1$ for exactly $(p^d - 1)/2$ values of $y$.
2. If $p = 2$, then $T(y) \in \{0, 1\}$, and $T(y) = 1$ for exactly $2^{d-1}$ values of $y$.

*Proof.* (1) The group $L^\times$ is cyclic of even order $p^d - 1$. For $y \ne 0$, $(y^e)^2 = y^{p^d - 1} = 1$, so $y^e = \pm 1$, and $1 \ne -1$ since $p$ is odd. The map $y \mapsto y^e$ is a group homomorphism from $L^\times$ to $\{\pm 1\}$. With a generator $\gamma$, $\gamma^e \ne 1$ because the order of $\gamma$ is $2e > e$, so the map is onto and its kernel has $(p^d - 1)/2$ elements.

(2) In characteristic $2$, $y \mapsto y^2$ is additive, so $T$ is additive, and $T(y)^2 = y^2 + \cdots + y^{2^d} = T(y) - y + y^{2^d} = T(y)$, since $y^{2^d} = y$ in $L$. So $T(y)$ is a root of $z^2 - z$, which means $T(y) \in \{0, 1\}$. $T$ is a polynomial in $y$ of degree $2^{d-1}$, so it has at most $2^{d-1} < 2^d$ roots, and $T$ is not zero. So $T$ is an onto additive map from $L$ to $\{0, 1\}$, and each of its two values is taken $2^{d-1}$ times. $\square$

**Lemma 4 (one attempt).** Let $h$ be a piece with $s \ge 2$ factors, and $a$ uniform among the polynomials of degree less than $\deg h$, drawn again while $a$ is constant. Then the attempt at lines L5 to L9 pushes a proper factorization of $h$ with probability at least $1/2$.

*Proof.* Let $m = \deg h$ and let $u$ be uniform over all polynomials of degree less than $m$, constants included, with residues $u_i = u \bmod q_{j_i}$. Let $E$ be the event that the values $u_i^e$ (or $T(u_i)$ for $p = 2$) are all equal, and for odd $p$ also all $u_i \ne 0$.

*A nonconstant $a$ that fails lies in $E$.* By Lemma 2, $b = a^e \bmod h$ (or $T(a) \bmod h$) has residues $b_i = a_i^e$ (or $T(a_i)$) modulo $q_{j_i}$, so $\gcd(b - 1, h)$ is the product of the $q_{j_i}$ with $b_i = 1$, and line L9 splits $h$ unless all $b_i$ are equal. If $\gcd(a, h) \ne 1$, line L6 splits $h$, since $a \ne 0$ and $\deg a < m$ give $g \ne h$. So for odd $p$ a failure needs $\gcd(a, h) = 1$, that is, all $a_i \ne 0$, and all $b_i$ equal.

*The probability of $E$.* For odd $p$, by Lemma 3 each $u_i$ is nonzero with $u_i^e = 1$ with probability $(p^d - 1)/(2 p^d) < 1/2$, and the same holds for $-1$. By the independence of Lemma 2, $\Pr[E] < 2 \cdot 2^{-s} \le 1/2$. For $p = 2$, each $T(u_i)$ is $0$ or $1$ with probability exactly $1/2$, so $\Pr[E] = 2 \cdot 2^{-s} \le 1/2$.

*Drawing again while $a$ is constant.* Then $a$ is distributed as $u$ given that $u$ is not constant. Let $c$ be the probability that $u$ is constant and $c'$ the probability that $u$ is a constant in $E$. A constant has equal residues, so every nonzero constant is in $E$, and for $p = 2$ also $0$; hence $c' \ge c (p - 1)/p \ge c/2$. The failure probability is at most $\Pr[E \text{ and } u \text{ not constant}]/(1 - c) = (\Pr[E] - c')/(1 - c) \le (1/2 - c/2)/(1 - c) = 1/2$. $\square$

**Termination.** Each attempt on a piece with $s \ge 2$ factors succeeds with probability at least $1/2$, independently of earlier attempts. So the number of attempts on that piece until it splits is at most a geometric random variable with mean $2$, and it is finite with probability $1$. Each split increases the number of pieces by one, and there are at most $r$ pieces, so there are $r - 1$ splits and $r$ outputs in all. Pieces with one factor have degree $d$ and are output at line L4 without an attempt. So the algorithm stops with probability $1$, after an expected number of at most $2(r - 1)$ attempts, and by the part on the output it then returns $q_1, \ldots, q_r$. $\blacksquare$
