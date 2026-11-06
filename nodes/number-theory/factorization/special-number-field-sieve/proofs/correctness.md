---
title: Correctness of the special number field sieve
proves: [correctness, termination]
status: full
---

Let $N \ge 3$ be an odd integer, let $f = x^d + c_{d-1}x^{d-1} + \dots + c_0 \in \mathbb{Z}[x]$ be monic of odd prime degree $d$, and let $m$ be an integer with $f(m) \equiv 0 \pmod N$. Write $\mathbb{Z}[\alpha] = \mathbb{Z}[x]/(f)$, and represent each element by its coefficients on $1, \alpha, \dots, \alpha^{d-1}$. After line L1 the implementation replaces $m$ by $m \bmod N$, which keeps $f(m) \equiv 0 \pmod N$; we use the reduced $m$ from then on. We prove that the output is always $1$ or a proper factor of $N$, that every subset that reaches line L9 gives a congruence of squares, and that the algorithm stops. We do not prove that a proper factor is found; that part is a heuristic. We also prove the two facts about special polynomials that the page uses, and at the end that the driver `factorize` returns the prime factorization.

**Lemma 1 (the special polynomial).** Let $r \ge 2$, $e \ge 1$, $s \ne 0$ and $d \ge 2$ be integers, $l = \lceil e/d \rceil$, $t = dl - e$, $f = x^d + sr^t$ and $m = r^l$. Then $0 \le t < d$ and $f(m) = r^t(r^e + s)$. So $f(m) \equiv 0 \pmod C$ for every divisor $C$ of $r^e + s$.

*Proof.* By the definition of the ceiling, $e/d \le l < e/d + 1$, so $e \le dl < e + d$ and $0 \le t < d$. Then $f(m) = r^{dl} + sr^t = r^{e + t} + sr^t = r^t(r^e + s)$. If $C \mid r^e + s$, then $C \mid f(m)$. $\square$

**Lemma 2 (the homomorphism).** There is a ring homomorphism $\varphi\colon \mathbb{Z}[\alpha] \to \mathbb{Z}/N\mathbb{Z}$ with $\varphi(\alpha) = m \bmod N$, and $\varphi(u) = u(m) \bmod N$ for every $u$ of degree below $d$.

*Proof.* Evaluation at $m$ followed by reduction modulo $N$ is a ring homomorphism $\psi\colon \mathbb{Z}[x] \to \mathbb{Z}/N\mathbb{Z}$. It maps $f$ to $f(m) \bmod N = 0$, so it maps the ideal $(f)$ to $0$, and it factors through $\mathbb{Z}[x]/(f)$. The value on the class of $u$ is $\psi(u) = u(m) \bmod N$. $\square$

Only $f(m) \equiv 0 \pmod N$ is used; $f(m) = N$ is not needed, and neither is the irreducibility of $f$. This is the one place where the special sieve differs from the general one, whose polynomial satisfies $f(m) = N$.

**Lemma 3 (integer roots and algebraic factors).** `integer_roots(f)` returns exactly the integer roots of $f$ when $c_0 \ne 0$. For each integer root $z$, $m - z$ divides $f(m)$, so a value $1 < \gcd(m - z, N) < N$ returned by line L1 is a proper factor of $N$. If $f = x^d + c$ with $d$ an odd prime and $c \ne 0$, then $f$ is reducible over $\mathbb{Q}$ if and only if it has an integer root.

*Proof.* If $z \in \mathbb{Z}$ and $f(z) = 0$, then $c_0 = -z(z^{d-1} + c_{d-1}z^{d-2} + \dots + c_1)$, so $z \mid c_0$, and $z \ne 0$ since $c_0 \ne 0$. Every divisor $u > 0$ of $|c_0|$ is $t$ or $|c_0|/t$ for some $t \le \sqrt{|c_0|}$ with $t \mid |c_0|$, and the function tests $u$ and $-u$ for each of them by exact evaluation. So it returns every integer root and nothing else. For an integer root $z$, $f = (x - z)h$ with $h \in \mathbb{Z}[x]$ monic, by division by the monic $x - z$; so $f(m) = (m - z)h(m)$ and $m - z \mid f(m)$. Any gcd with $N$ divides $N$, and line L1 returns it only if it is strictly between $1$ and $N$.

For the last claim, an integer root gives the factor $x - z$, and $d \ge 3$, so $f$ is reducible. Conversely, let $f = x^d - a$ with $a = -c$ be reducible over $\mathbb{Q}$, and let $\theta$ be a complex root, so $\theta^d = a$. Let $g$ be the minimal polynomial of $\theta$ over $\mathbb{Q}$, of degree $k$ with $1 \le k < d$. The roots of $f$ are $\theta\zeta^j$ with $\zeta = e^{2\pi i/d}$, and $g$ divides $f$, so the roots of $g$ are $k$ of them. Their product is $b = \theta^k\zeta^j$ for some $j$, and it is $(-1)^k$ times the constant term of $g$, so $b$ is rational, and $b \ne 0$ since $a \ne 0$. As $\zeta^d = 1$, $b^d = \theta^{kd} = a^k$. Since $d$ is prime and $1 \le k < d$, there are integers $u, v$ with $uk + vd = 1$. Then $w = b^u a^v$ is rational and $w^d = (b^d)^u a^{vd} = a^{uk + vd} = a$. So $a$ is the $d$-th power of a rational number, and since $a$ is an integer, of an integer $z$ (a rational root of a monic integer polynomial is an integer, by the argument of the first paragraph). Then $f(z) = z^d - a = 0$. $\square$

So for the special polynomials of the driver, the check of line L1 removes every reducible case; the example $2^{33} - 1$ with $f = x^3 - 1$, $z = 1$ and $m = 2^{11}$ gives $\gcd(2047, N) = 2047$.

**Lemma 4 (exact products).** The functions `mulmod` with no modulus and `product_in_order` compute products in $\mathbb{Z}[\alpha]$ exactly.

*Proof.* `mulmod` forms the product $w$ of the two polynomials in $\mathbb{Z}[x]$, of degree at most $2d - 2$. For $k = 2d - 2$ down to $d$ it subtracts $w_k x^{k-d} f$, which does not change the class modulo $f$. Since $f$ is monic, this sets the coefficient of $x^k$ to $0$ and changes only lower coefficients. After the loop the degree is below $d$, so the result is the representative of $uv$. `product_in_order` multiplies pairs level by level; multiplication in a commutative ring is associative and commutative, so the result is the product of all the elements. $\square$

**Lemma 5 (the rational square).** Let $T$ be a set of relations whose vectors of line L5 add to $0$ modulo $2$, and let $e_p$ be the sum over $T$ of the exponents of $p$ in $a - bm$. Then $\prod_T (a - bm) = v^2$ with $v = \prod_{p \in P} p^{e_p/2}$, and the value $x$ of line L7 satisfies $x \equiv f'(m) v \pmod N$.

*Proof.* Each relation has $|a - bm| = \prod_{p \in P} p^{e_p(a, b)}$, which line L4 checks by trial division. The rational prefilter of the implementation only skips points; it never adds a point that fails this check. The product over $T$ of the signs is $(-1)^s$, where $s$ is the number of negative $a - bm$; bit $0$ of the vectors is that sign, so $s$ is even and the product is positive. The bits for the rational primes are the exponents modulo $2$, so every $e_p$ is even. Hence $\prod_T (a - bm) = \prod_p p^{e_p} = v^2$. Line L7 computes $f'(m)$ times $\prod p^{e_p/2}$ modulo $N$. $\square$

**Lemma 6 (the algebraic square).** If line L8 returns $\delta$, then $\delta^2 = \gamma$ in $\mathbb{Z}[\alpha]$, where $\gamma = f'(\alpha)^2 \prod_T (a - b\alpha)$.

*Proof.* The implementation computes $\gamma$ exactly by Lemma 4, and `algebraic_sqrt` returns a candidate only after the test `mulmod(delta, delta, f) == gamma`, an exact product by Lemma 4. Otherwise it returns `None`, and line L8 goes on to the next subset. $\square$

**Lemma 7 (the congruence of squares).** If a subset $T$ reaches line L9, then $x^2 \equiv y^2 \pmod N$.

*Proof.* By Lemma 5, $x^2 \equiv f'(m)^2 \prod_T (a - bm) \pmod N$. By Lemma 2, $\varphi(a - b\alpha) = a - bm$ and $\varphi(f'(\alpha)) = f'(m)$, since $f'$ has degree $d - 1 < d$. Line L8 sets $y = \delta(m) \bmod N = \varphi(\delta)$. By Lemma 6 and Lemma 2, $y^2 = \varphi(\delta^2) = \varphi(\gamma) = f'(m)^2 \prod_T (a - bm)$ in $\mathbb{Z}/N\mathbb{Z}$. So $x^2 \equiv y^2$. $\square$

**Lemma 8 (the output).** `snfs` returns $1$ or an integer $g$ with $1 < g < N$ and $g \mid N$, or raises `ValueError` when $f(m) \not\equiv 0 \pmod N$.

*Proof.* Line L1 raises the error exactly when $f(m) \bmod N \ne 0$. The returns with a value other than $1$ are these. Line L1 returns $\gcd(m - z, N)$ only if it lies strictly between $1$ and $N$. The trial division returns a prime $p$ with $p \mid N$ only if $p < N$, and $1$ otherwise. The test of $\gcd(f'(m), N)$ and line L9 return a gcd only if it lies strictly between $1$ and $N$. A gcd with $N$ divides $N$. Every other exit returns $1$. $\square$

When $g$ comes from line L9, Lemma 7 explains why it is a factor: $N \mid (x - y)(x + y)$, and $g$ is proper exactly when $x \not\equiv \pm y$ modulo some but not all prime power factors of $N$.

**Lemma 9 (inert primes and the square root modulo $p$).** Let $p$ be an odd prime with $p \equiv 3 \pmod 4$ such that `is_inert(f, p)` is true. Then $f$ is irreducible modulo $p$, $K = \mathbb{F}_p[x]/(f)$ is a field with $q = p^d$ elements, and $q \equiv 3 \pmod 4$. For $\gamma \in K^*$, $r_0 = \gamma^{(3q-5)/4}$ satisfies $r_0^2\gamma = 1$ if and only if $\gamma$ is a square in $K^*$. Moreover, if $f = x^d + c$ and $p \not\equiv 1 \pmod d$, then $f$ has a root modulo $p$, so $p$ is not inert.

*Proof.* The test says that $f$ has no root modulo $p$ and $x^{p^d} \equiv x \pmod{f, p}$. The second condition means that $f$ divides $x^{p^d} - x$ in $\mathbb{F}_p[x]$. That polynomial is the product of all monic irreducible polynomials over $\mathbb{F}_p$ of degree dividing $d$, each once. So every irreducible factor of $f$ has degree $1$ or $d$, since $d$ is prime. There is no root, so no factor of degree $1$, and $f$ is irreducible of degree $d$. Hence $K$ is a field with $q = p^d$ elements. Since $p \equiv 3 \pmod 4$ and $d$ is odd, $q \equiv 3^d \equiv 3 \pmod 4$, so $(3q - 5)/4$ is an integer.

$K^*$ is cyclic of order $q - 1$, so $\gamma$ is a square if and only if $\gamma^{(q-1)/2} = 1$. Now $r_0^2\gamma = \gamma^{(3q-5)/2 + 1} = \gamma^{3(q-1)/2} = (\gamma^{(q-1)/2})^3$. The value $\gamma^{(q-1)/2}$ is $1$ or $-1$, and its cube is the same value. So $r_0^2\gamma = 1$ exactly when $\gamma$ is a square.

For the last claim, if $p = d$ then $x^d + c \equiv (x + c)^d \pmod d$ has the root $-c$. Otherwise $d \nmid p - 1$, and since $d$ is prime, $\gcd(d, p - 1) = 1$. Then $u \mapsto u^d$ is injective on the cyclic group $\mathbb{F}_p^*$ of order $p - 1$, hence onto, and on $0$ it is $0$. So $-c$ is a $d$-th power $u^d$ modulo $p$, and $u$ is a root. $\square$

Lemma 9 explains why line L8 finds the square root when it exists, and why `inert_prime` only succeeds at primes $p \equiv 1 \pmod d$ for the special polynomials. Correctness does not depend on it, since Lemma 6 checks the result.

**Lemma 10 (Newton's step).** Let $M$ be an odd modulus, and let $r, \gamma$ in $(\mathbb{Z}/M^2)[x]/(f)$ satisfy $\gamma r^2 \equiv 1 \pmod M$. Then $r' = r(3 - \gamma r^2)/2$ satisfies $\gamma r'^2 \equiv 1 \pmod{M^2}$.

*Proof.* Write $\gamma r^2 = 1 - e$ with $e \equiv 0 \pmod M$. Then $r' = r(2 + e)/2$, where $2$ is invertible since $M$ is odd, and
$$\gamma r'^2 = \frac{(1 - e)(2 + e)^2}{4} = \frac{4 - 3e^2 - e^3}{4} = 1 - \frac{3e^2 + e^3}{4}.$$
Both $e^2$ and $e^3$ are $0$ modulo $M^2$. $\square$

**Lemma 11 (the vector of a relation is defined).** For a relation $(a, b)$ and a prime $p \in P$ that divides $F(a, b)$, $p \nmid b$, and the pair $(p, ab^{-1} \bmod p)$ is in the algebraic factor base.

*Proof.* Modulo $b$, $F(a, b) = \sum c_i a^i b^{d-i} \equiv a^d$, since $c_d = 1$. If $p \mid b$ and $p \mid F(a, b)$, then $p \mid a^d$, so $p \mid a$, against $\gcd(a, b) = 1$. So $p \nmid b$, and with $r = ab^{-1} \bmod p$, $0 \equiv F(a, b) = b^d f(a/b) \equiv b^d f(r) \pmod p$, so $f(r) \equiv 0 \pmod p$ and $(p, r)$ is one of the pairs of line L2. $\square$

**Lemma 12 (termination).** `snfs` stops on every input.

*Proof.* `integer_roots` loops up to $\sqrt{|c_0|}$. The trial division and the search for an inert prime run over finite ranges (at most $2000$ candidates for the inert prime), and if none is found the function returns $1$. If an inert prime $p$ is found, then $f$ is irreducible modulo $p$ by Lemma 9, so it is irreducible over $\mathbb{Q}$ (a factorization over $\mathbb{Q}$ gives one over $\mathbb{Z}$ with monic factors, by Gauss's lemma, and it reduces to a factorization modulo $p$). Then the loop of line L2 for the characters stops: the discriminant $\Delta$ of $f$ is not $0$, since an irreducible polynomial over $\mathbb{Q}$ has distinct roots, and by Schur's theorem infinitely many primes $q$ divide some value $f(s)$ with $s \in \mathbb{Z}$; for such $q \nmid \Delta$, $s \bmod q$ is a simple root, so $f'(s) \not\equiv 0 \pmod q$. So enough characters exist, and the search reaches them. The sieve runs over at most $Y$ lines of $2A + 1$ points. Trial division of a nonzero integer by finitely many primes stops. The elimination is a loop over the rows, and each inner loop clears the top bit of $v$ or stops, so it runs at most as many times as $v$ has binary digits. The dependency loop is finite. In `algebraic_sqrt`, the modulus is squared at each step and the loop stops when it passes a fixed bound. $\square$

**Theorem.** `snfs` stops and returns either $1$ or a proper factor of $N$. When it returns a proper factor from line L9, it has found $x$ and $y$ with $x^2 \equiv y^2 \pmod N$.

*Proof.* Lemmas 12, 8 and 7. $\square$

**The driver.** `factorize(n)` returns the prime factors of $n \ge 1$ with multiplicity, in order, provided that `is_probable_prime` is correct on the numbers it sees. That holds for all numbers below $3317044064679887385961981$, where the strong test to the $13$ prime bases up to $41$ is a proof of primality.

*Proof.* `special_form` returns $(r, e, s)$ with $n = r^e + s$ or nothing, and the polynomials of degrees $3$ and $5$ come from Lemma 1, so for each of them $f(\text{root}) \equiv 0$ modulo every divisor of $n$.

The trial division divides out the primes below $1000$ in increasing order. If it stops because $p^2 > n$ for the remaining $n$, then $n$ has no prime factor below $p$, so $n$ is $1$ or a prime. Otherwise $n$ has no prime factor below $1000$. The invariant of the stack is this: the product of the output and of the stack equals the input, every output entry is prime, and every stack entry divides the original $n$ and has no prime factor below $1000$. It holds at the start. A popped $m$ that is $1$ is dropped. A popped $m > 1$ with $m < 10^6$ is prime, because a composite with no prime factor below $1000$ is at least $1009^2 > 10^6$. A popped $m \ge 10^6$ that passes `is_probable_prime` is prime by the assumption. Otherwise $m$ is composite and odd, and `_split(m)` returns a proper factor $g$:

- A perfect power $m = r^e$ with $e \ge 2$ gives $1 < r < m$ and $r \mid m$.
- `_split` keeps a special polynomial only if $f(\text{root}) \equiv 0 \pmod m$, which it tests, so `snfs` never raises. A returned $\gcd(\text{root} - z, m)$ strictly between $1$ and $m$ is a proper factor.
- The base-$m$ polynomial of `select_polynomial` satisfies $f(\text{root}) = m$, so $f(\text{root}) \equiv 0 \pmod m$ as well. The choice and order of the polynomials, by `value_size`, only affect the speed. Every value returned from `snfs` is accepted only if it lies strictly between $1$ and $m$, and it divides $m$ by the Theorem.
- The last resort finds the least odd $t \ge 1001$ with $t \mid m$, which exists and is below $m$ because $m$ is odd and composite with no prime factor below $1000$.

Each of these loops is finite: at most $2 + 1$ polynomials, $3$ bounds each, and `snfs` stops by Lemma 12. Then $g$ and $m/g$ both divide $m$, so they divide $n$ and have no prime factor below $1000$, and their product is $m$. The invariant holds after each step. Each split replaces $m$ by two numbers greater than $1$ whose product is $m$, so the total number of prime factors counted with multiplicity bounds the number of splits, and the loop stops. When the stack is empty, the output is a list of primes whose product is the input, and sorting puts it in order. $\blacksquare$
