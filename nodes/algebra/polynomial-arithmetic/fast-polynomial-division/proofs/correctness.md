---
title: FAST-DIVMOD returns the quotient and remainder of division with remainder in O(M(n)) operations
proves: [correctness]
status: full
---

Let $R$ be a commutative ring with $1$, $a, b \in R[x]$ with $b \ne 0$ and $\operatorname{lc}(b)$ a unit, $n = \deg a$ and $m = \deg b$ after line L1. For $f$ with $\deg f \le j$ write $\operatorname{rev}_j(f) = x^j f(1/x)$, a polynomial of degree at most $j$ whose coefficient of $x^i$ is the coefficient of $x^{j-i}$ in $f$.

**Lemma 1 (uniqueness).** There is at most one pair $(q, r)$ with $a = qb + r$ and $\deg r < m$.

*Proof.* If $qb + r = q'b + r'$ with $\deg r, \deg r' < m$, then $(q - q')b = r' - r$. If $q \ne q'$, the leading coefficient of $(q - q')b$ is $\operatorname{lc}(q - q') \operatorname{lc}(b)$, which is nonzero because $\operatorname{lc}(b)$ is a unit. So $\deg((q - q')b) \ge m > \deg(r' - r)$, a contradiction. So $q = q'$ and then $r = r'$. $\square$

Existence of the pair follows from long division, which needs only that $\operatorname{lc}(b)$ is a unit. It also follows from the theorem below, which constructs the pair.

**Lemma 2 (reversal).** Let $n \ge m$, and let $q, r$ satisfy $a = qb + r$ with $\deg q \le n - m$ and $\deg r \le m - 1$. Then

$$\operatorname{rev}_n(a) = \operatorname{rev}_{n-m}(q)\, \operatorname{rev}_m(b) + x^{n-m+1} \operatorname{rev}_{m-1}(r),$$

where $\operatorname{rev}_{m-1}(r) = 0$ if $m = 0$ (then $r = 0$).

*Proof.* Substitute $1/x$ for $x$ in $a = qb + r$ in the ring $R[x, 1/x]$ and multiply by $x^n = x^{n-m} \cdot x^m = x^{n-m+1} \cdot x^{m-1}$. This gives $x^n a(1/x) = x^{n-m} q(1/x) \cdot x^m b(1/x) + x^{n-m+1} \cdot x^{m-1} r(1/x)$. Each of the four factors of the form $x^j f(1/x)$ has $\deg f \le j$, so it is the polynomial $\operatorname{rev}_j(f)$. $\square$

**Lemma 3 (the reversed divisor is invertible).** The constant term of $\operatorname{rev}_m(b)$ is $\operatorname{lc}(b)$, a unit, so for each $k \ge 1$ there is a unique $h$ of degree less than $k$ with $\operatorname{rev}_m(b) \cdot h \equiv 1 \pmod{x^k}$, and line L4 computes it.

*Proof.* The constant term is the coefficient of $x^m$ in $b$, which is $\operatorname{lc}(b)$. Existence and uniqueness of $h$, and the fact that NEWTON-INVERSE returns it, are Lemma 1 and the correctness theorem of the proof for [Newton power series inversion](/newton-power-series-inversion/). $\square$

**Theorem (correctness).** FAST-DIVMOD$(a, b)$ returns the unique pair $(q, r)$ with $a = qb + r$ and $\deg r < \deg b$.

*Proof.* If $a = 0$ or $n < m$, line L2 returns $(0, a)$, which satisfies $a = 0 \cdot b + a$ with $\deg a < m$. By Lemma 1 it is the unique pair.

Let $n \ge m$ and $k = n - m + 1 \ge 1$ (line L3). Let $(q^*, r^*)$ be the pair of long division, so $a = q^* b + r^*$, $\deg r^* < m$, and $\deg q^* = n - m$ because $\deg(q^* b) = \deg(a - r^*) = n$ and $\operatorname{lc}(b)$ is a unit. By Lemma 2,

$$\operatorname{rev}_n(a) \equiv \operatorname{rev}_{n-m}(q^*)\, \operatorname{rev}_m(b) \pmod{x^k}.$$

Multiply both sides by the $h$ of line L4. By Lemma 3, $\operatorname{rev}_m(b) h \equiv 1 \pmod{x^k}$, so

$$\operatorname{rev}_n(a)\, h \equiv \operatorname{rev}_{n-m}(q^*) \pmod{x^k}.$$

Line L5 sets $s = \operatorname{rev}_n(a) \bmod x^k$, and $s h \equiv \operatorname{rev}_n(a) h \pmod{x^k}$. So the $t$ of line L6, which has degree less than $k$, is congruent to $\operatorname{rev}_{n-m}(q^*)$ modulo $x^k$. Both have degree less than $k$, so $t = \operatorname{rev}_{n-m}(q^*)$, and line L7 gives $q = \operatorname{rev}_{n-m}(t) = q^*$, since reversing twice with the same index is the identity on polynomials of degree at most $n - m$.

If $m = 0$, then $r^* = 0$ and the algorithm returns $(q^*, 0)$. Otherwise line L8 sets $u = q^* b \bmod x^m$ and line L9 sets $r = (a \bmod x^m) - u = (a - q^* b) \bmod x^m = r^* \bmod x^m = r^*$, because $\deg r^* < m$. So the algorithm returns $(q^*, r^*)$. $\square$

**Theorem (cost).** Assume that multiplying a polynomial with $j$ coefficients by one with at most $j$ coefficients costs at most $M(j)$ ring operations, and that $M(j)/j$ is nondecreasing. Let $k = n - m + 1$. Then FAST-DIVMOD uses at most

$$4M(k) + M(m) + 2 \lceil \log_2 k \rceil \frac{M(k)}{k} + O(n)$$

ring operations, plus one inversion of $\operatorname{lc}(b)$, and this is at most $4M(n + 1) + o(M(n)) + O(n)$. With a precomputed inverse it uses at most $M(k) + M(m) + O(n)$.

*Proof.* Lines L1, L3, L5, L7 and L9 touch each coefficient a bounded number of times: $O(n)$. Line L4 costs at most $3M(k) + 2\lceil \log_2 k \rceil M(k)/k + O(k)$ by the cost theorem for Newton inversion. Line L6 multiplies two polynomials with $k$ coefficients: at most $M(k)$. Line L8 needs only $q \bmod x^m$, which has at most $\min(k, m)$ coefficients, times $b \bmod x^m$, which has $m$ coefficients: at most $M(m)$. Adding these gives the first bound, and dropping line L4 gives the bound with a precomputed inverse.

For the second bound, $M(j)/j$ nondecreasing gives $M(k) \le \frac{k}{k+m} M(k + m)$ and $M(m) \le \frac{m}{k+m} M(k + m)$, so $4M(k) + M(m) \le 4(M(k) + M(m)) \le 4M(k + m) = 4M(n + 1)$. Also $2\lceil \log_2 k \rceil M(k)/k \le 2 \lceil \log_2 (n + 1) \rceil M(n + 1)/(n + 1)$, which is $o(M(n + 1))$ because $\log n / n \to 0$. $\blacksquare$
