---
title: Rabin's test accepts exactly the irreducible polynomials over a finite field
proves: [correctness]
status: full
---

Let $\mathbb{F}_q$ be a finite field with $q$ elements and let $f \in \mathbb{F}_q[x]$ be monic of degree $n \ge 1$ (line L1 makes the input monic; this does not change irreducibility). Let $P$ be the set of prime divisors of $n$.

**Lemma.** For every $m \ge 1$, $x^{q^m} - x$ is the product of all monic irreducible polynomials in $\mathbb{F}_q[x]$ whose degree divides $m$, each taken once.

*Proof.* Let $u = x^{q^m} - x$.

(a) *$u$ is square-free.* Its derivative is $q^m x^{q^m - 1} - 1 = -1$, because $q = 0$ in $\mathbb{F}_q$. So $\gcd(u, u') = 1$, and a repeated factor $g^2 \mid u$ would give $g \mid u'$, which is impossible.

(b) *Each monic irreducible $g$ of degree $d \mid m$ divides $u$.* The ring $K = \mathbb{F}_q[x]/(g)$ is a field with $q^d$ elements. Its nonzero elements form a group of order $q^d - 1$, so $\beta^{q^d} = \beta$ for every $\beta \in K$. Applying this $m/d$ times gives $\beta^{q^m} = \beta$. For $\beta = x \bmod g$ this says $g \mid x^{q^m} - x$.

(c) *Each monic irreducible $g \mid u$ has degree dividing $m$.* Let $d = \deg g$ and $K = \mathbb{F}_q[x]/(g)$, with $\alpha = x \bmod g$, so $\alpha^{q^m} = \alpha$. The map $\varphi(\beta) = \beta^q$ is a ring homomorphism of $K$ (the binomial coefficients $\binom{q}{i}$ for $0 < i < q$ are divisible by the characteristic) that fixes $\mathbb{F}_q$, because $c^q = c$ for $c \in \mathbb{F}_q$ by the group order argument of (b). The set $\{\beta : \varphi^m(\beta) = \beta\}$ is therefore closed under addition and multiplication and contains $\mathbb{F}_q$ and $\alpha$; every element of $K$ is a polynomial in $\alpha$ with coefficients in $\mathbb{F}_q$, so $\varphi^m$ is the identity on $K$. Let $t$ be the least $j \ge 1$ with $\varphi^j = \mathrm{id}$. Then $t \le d$ by (b), and $t \ge d$, because every element of $K$ is a root of $x^{q^t} - x$, a polynomial with at most $q^t$ roots in the field $K$, and $K$ has $q^d$ elements. So $t = d$, and $\varphi^m = \mathrm{id}$ gives $d \mid m$: write $m = s d + r$ with $0 \le r < d$; then $\varphi^r = \varphi^m (\varphi^{d})^{-s} = \mathrm{id}$, so $r = 0$.

By unique factorization in $\mathbb{F}_q[x]$ and (a), (b), (c), $u$ is the stated product. $\square$

**The loop.** Line L3 sets $h = x \bmod f$. By induction, after line L5 in pass $j$, $h = x^{q^j} \bmod f$: raising to the power $q$ commutes with reduction modulo $f$, since $(a \bmod f)^q \equiv a^q \pmod f$. Line L6 is true exactly when $j = n / r$ for a prime $r \in P$, and then line L7 tests $\gcd(x^{q^{n/r}} - x, f) = 1$, because $\gcd(h - x, f) = \gcd(x^{q^{n/r}} - x, f)$ when $h \equiv x^{q^{n/r}} \pmod f$. Line L8 tests $x^{q^n} \equiv x \pmod f$. So the algorithm returns true exactly when

1. $f \mid x^{q^n} - x$, and
2. $\gcd(x^{q^{n/r}} - x, f) = 1$ for every prime $r \mid n$.

**If $f$ is irreducible, both conditions hold.** Condition 1 is part (b) of the lemma with $m = n$. For condition 2, $\gcd(x^{q^{n/r}} - x, f)$ is a monic divisor of the irreducible $f$, so it is $1$ or $f$. If it were $f$, then $f \mid x^{q^{n/r}} - x$, and by part (c), $n \mid n/r$, which is false for $r \ge 2$. So the gcd is $1$.

**If both conditions hold, $f$ is irreducible.** By condition 1 and the lemma, $f$ is a product of distinct monic irreducible polynomials whose degrees divide $n$. Suppose $f$ is reducible; then one of these factors, $g$, has degree $d < n$ with $d \mid n$. Then $n / d > 1$ has a prime divisor $r$, and $d \mid n / r$. By part (b) of the lemma with $m = n / r$, $g \mid x^{q^{n/r}} - x$, so $g$ divides $\gcd(x^{q^{n/r}} - x, f)$, which contradicts condition 2.

The implementation works over the prime field, $q = p$. $\blacksquare$
