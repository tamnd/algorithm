---
title: Correctness of the general number field sieve
proves: [correctness, termination]
status: full
---

Let $N \ge 3$ be an odd integer, and let $f = x^d + c_{d-1}x^{d-1} + \dots + c_0 \in \mathbb{Z}[x]$ be the monic polynomial and $m$ the integer of line L1, with $f(m) = N$. Write $\mathbb{Z}[\alpha] = \mathbb{Z}[x]/(f)$, and represent each element by its coefficients on $1, \alpha, \dots, \alpha^{d-1}$. We prove three things. The output is always $1$ or a proper factor of $N$. Every subset that reaches line L9 gives a congruence of squares. The algorithm stops. We do not prove that a proper factor is found; that part is a heuristic. At the end we prove that the driver `factorize` returns the prime factorization.

**Lemma 1 (the homomorphism).** There is a ring homomorphism $\varphi\colon \mathbb{Z}[\alpha] \to \mathbb{Z}/N\mathbb{Z}$ with $\varphi(\alpha) = m \bmod N$, and $\varphi(u) = u(m) \bmod N$ for every $u$ of degree below $d$.

*Proof.* Evaluation at $m$ followed by reduction modulo $N$ is a ring homomorphism $\psi\colon \mathbb{Z}[x] \to \mathbb{Z}/N\mathbb{Z}$. It maps $f$ to $f(m) \bmod N = N \bmod N = 0$, so it maps the ideal $(f)$ to $0$, and it factors through $\mathbb{Z}[x]/(f)$. The value on the class of $u$ is $\psi(u) = u(m) \bmod N$. $\square$

The proof does not need $f$ to be irreducible: Lemma 1 holds for any monic $f$ with $f(m) = N$.

**Lemma 2 (exact products).** The functions `mulmod` with no modulus and `product_in_order` compute products in $\mathbb{Z}[\alpha]$ exactly.

*Proof.* `mulmod` forms the product $w$ of the two polynomials in $\mathbb{Z}[x]$, of degree at most $2d - 2$. For $k = 2d - 2$ down to $d$ it subtracts $w_k x^{k-d} f$, which does not change the class modulo $f$. Since $f$ is monic, this sets the coefficient of $x^k$ to $0$ and changes only lower coefficients. After the loop the degree is below $d$, so the result is the representative of $uv$. `product_in_order` multiplies pairs level by level; multiplication in a commutative ring is associative and commutative, so the result is the product of all the elements. $\square$

**Lemma 3 (the rational square).** Let $T$ be a set of relations whose vectors of line L5 add to $0$ modulo $2$, and let $e_p$ be the sum over $T$ of the exponents of $p$ in $a - bm$. Then $\prod_T (a - bm) = v^2$ with $v = \prod_{p \in P} p^{e_p/2}$, and the value $x$ of line L7 satisfies $x \equiv f'(m) v \pmod N$.

*Proof.* Each relation has $|a - bm| = \prod_{p \in P} p^{e_p(a, b)}$, which line L4 checks by trial division. The product over $T$ of the signs is $(-1)^s$, where $s$ is the number of negative $a - bm$; bit $0$ of the vectors is the sign, so $s$ is even and the product is positive. Bits for the rational primes are the exponents modulo $2$, so every $e_p$ is even. Hence $\prod_T (a - bm) = \prod_T |a - bm| = \prod_p p^{e_p} = v^2$. Line L7 computes $f'(m)$ times $\prod p^{e_p/2}$ modulo $N$. $\square$

**Lemma 4 (the algebraic square).** If line L8 returns $\delta$, then $\delta^2 = \gamma$ in $\mathbb{Z}[\alpha]$, where $\gamma = f'(\alpha)^2 \prod_T (a - b\alpha)$.

*Proof.* The implementation computes $\gamma$ exactly by Lemma 2, and `algebraic_sqrt` returns a candidate only after the test `mulmod(delta, delta, f) == gamma`, an exact product by Lemma 2. Otherwise it returns `None`, and line L8 goes on to the next subset. $\square$

**Lemma 5 (the congruence of squares).** If a subset $T$ reaches line L9, then $x^2 \equiv y^2 \pmod N$.

*Proof.* By Lemma 3, $x^2 \equiv f'(m)^2 \prod_T (a - bm) \pmod N$. By Lemma 1, $\varphi(a - b\alpha) = a - bm$ and $\varphi(f'(\alpha)) = f'(m)$, since $f'$ has degree $d - 1 < d$. By Lemma 4 and Lemma 1, $y^2 = \varphi(\delta)^2 = \varphi(\delta^2) = \varphi(\gamma) = f'(m)^2 \prod_T (a - bm)$ in $\mathbb{Z}/N\mathbb{Z}$. So $x^2 \equiv y^2$. $\square$

**Lemma 6 (the output).** `gnfs` returns $1$ or an integer $g$ with $1 < g < N$ and $g \mid N$.

*Proof.* There are four return points with a value other than $1$. The trial division returns a prime $p$ with $p \mid N$ only if $p < N$, and returns $1$ otherwise. Line L1 returns $\gcd(f'(m), N)$ only if it lies strictly between $1$ and $N$. Line L9 returns $\gcd(x - y, N)$ only if it lies strictly between $1$ and $N$. A gcd with $N$ divides $N$. Every other exit returns $1$. $\square$

When $g$ comes from line L9, Lemma 5 explains why it is a factor: $N \mid (x - y)(x + y)$, and $g$ is proper exactly when $x \not\equiv \pm y$ modulo some but not all prime power factors of $N$.

**Lemma 7 (inert primes and the square root modulo $p$).** Let $p$ be an odd prime with $p \equiv 3 \pmod 4$ such that `is_inert(f, p)` is true, where $d$ is an odd prime. Then $f$ is irreducible modulo $p$, $K = \mathbb{F}_p[x]/(f)$ is a field with $q = p^d$ elements, and $q \equiv 3 \pmod 4$. For $\gamma \in K^*$, $r_0 = \gamma^{(3q-5)/4}$ satisfies $r_0^2\gamma = 1$ if and only if $\gamma$ is a square in $K^*$.

*Proof.* The test says that $f$ has no root modulo $p$ and $x^{p^d} \equiv x \pmod{f, p}$. The second condition means that $f$ divides $x^{p^d} - x$ in $\mathbb{F}_p[x]$. That polynomial is the product of all monic irreducible polynomials over $\mathbb{F}_p$ of degree dividing $d$, each once. So every irreducible factor of $f$ has degree $1$ or $d$, since $d$ is prime. There is no root, so no factor of degree $1$, and $f$ is irreducible of degree $d$. Hence $K$ is a field with $q = p^d$ elements. Since $p \equiv 3 \pmod 4$ and $d$ is odd, $q \equiv 3^d \equiv 3 \pmod 4$, so $(3q - 5)/4$ is an integer.

$K^*$ is cyclic of order $q - 1$, so $\gamma$ is a square if and only if $\gamma^{(q-1)/2} = 1$. Now $r_0^2\gamma = \gamma^{(3q-5)/2 + 1} = \gamma^{3(q-1)/2} = (\gamma^{(q-1)/2})^3$. The value $\gamma^{(q-1)/2}$ is $1$ or $-1$, and its cube is the same value. So $r_0^2\gamma = 1$ exactly when $\gamma$ is a square. $\square$

Lemma 7 explains why line L8 finds the square root when it exists and the precision is high enough. Correctness does not depend on it, since Lemma 4 checks the result.

**Lemma 8 (Newton's step).** Let $M$ be an odd modulus, and let $r, \gamma$ in $(\mathbb{Z}/M^2)[x]/(f)$ satisfy $\gamma r^2 \equiv 1 \pmod M$. Then $r' = r(3 - \gamma r^2)/2$ satisfies $\gamma r'^2 \equiv 1 \pmod{M^2}$.

*Proof.* Write $\gamma r^2 = 1 - e$ with $e \equiv 0 \pmod M$. Then $r' = r(2 + e)/2$, where $2$ is invertible since $M$ is odd, and
$$\gamma r'^2 = \frac{(1 - e)(2 + e)^2}{4} = \frac{4 - 3e^2 - e^3}{4} = 1 - \frac{3e^2 + e^3}{4}.$$
Both $e^2$ and $e^3$ are $0$ modulo $M^2$. $\square$

**Lemma 9 (the vector of a relation is defined).** For a relation $(a, b)$ and a prime $p \in P$ that divides $F(a, b)$, $p \nmid b$, and the pair $(p, ab^{-1} \bmod p)$ is in the algebraic factor base.

*Proof.* Modulo $b$, $F(a, b) = \sum c_i a^i b^{d-i} \equiv a^d$, since $c_d = 1$. If $p \mid b$ and $p \mid F(a, b)$, then $p \mid a^d$, so $p \mid a$, against $\gcd(a, b) = 1$. So $p \nmid b$, and with $r = ab^{-1} \bmod p$, $0 \equiv F(a, b) = b^d f(a/b) \equiv b^d f(r) \pmod p$, so $f(r) \equiv 0 \pmod p$ and $(p, r)$ is one of the pairs of line L2. $\square$

So `relation_vector` never takes the inverse of $0$ modulo $p$ and never looks up a missing pair.

**Lemma 10 (termination).** `gnfs` stops on every input.

*Proof.* Polynomial selection tries at most $64$ values of $m$. The trial division and the search for an inert prime run over finite ranges (at most $2000$ candidates for the inert prime). If an inert prime $p$ is found, then $f$ is irreducible modulo $p$ by Lemma 7, so it is irreducible over $\mathbb{Q}$ (a factorization over $\mathbb{Q}$ gives one over $\mathbb{Z}$ with monic factors, by Gauss's lemma, and it reduces to a factorization modulo $p$). Then the loop of line L2 for the characters stops. Its discriminant $\Delta$ is not $0$, since an irreducible polynomial over $\mathbb{Q}$ has distinct roots. By Schur's theorem, infinitely many primes $q$ divide some value $f(s)$ with $s \in \mathbb{Z}$; for such $q \nmid \Delta$, $s \bmod q$ is a simple root, so $f'(s) \not\equiv 0 \pmod q$. So enough characters exist, and the search reaches them. The sieve runs over $Y$ lines of $2A + 1$ points. Trial division of a nonzero integer by finitely many primes stops. The elimination is a loop over the rows, and each inner loop clears the top bit of $v$ or stops, so it runs at most as many times as $v$ has bits. The dependency loop is finite. In `algebraic_sqrt`, the modulus is squared at each step and the loop stops when it passes a fixed bound. $\square$

**Theorem.** `gnfs` stops and returns either $1$ or a proper factor of $N$. When it returns a proper factor from line L9, it has found $x$ and $y$ with $x^2 \equiv y^2 \pmod N$.

*Proof.* Lemmas 10, 6 and 5. $\square$

**The driver.** `factorize(n)` returns the prime factors of $n \ge 1$ with multiplicity, in order, provided that `is_probable_prime` is correct on the numbers it sees. That holds for all numbers below $3317044064679887385961981$, where the strong test to the $13$ prime bases up to $41$ is a proof of primality.

*Proof.* The trial division divides out the primes below $1000$ in increasing order. If it stops because $p^2 > n$ for the remaining $n$, then $n$ has no prime factor below $p$, so $n$ is $1$ or a prime. Otherwise $n$ has no prime factor below $1000$. The invariant of the stack is this: the product of the output and of the stack equals the input, every output entry is prime, and every stack entry has no prime factor below $1000$. It holds at the start. A popped $m$ that is $1$ is dropped. A popped $m > 1$ with $m < 10^6$ is prime, because a composite with no prime factor below $1000$ is at least $1009^2 > 10^6$. A popped $m \ge 10^6$ that passes `is_probable_prime` is prime by the assumption. Otherwise $m$ is composite, and `_split(m)` returns a proper factor $g$: a perfect power $r^e$ with $e \ge 2$ gives $1 < r < m$; `gnfs` gives a proper factor by the Theorem; and the last resort finds the least odd $t \ge 1001$ with $t \mid m$, which exists and is below $m$ because $m$ is odd and composite with no prime factor below $1000$. Then $g$ and $m/g$ both divide $m$, so they have no prime factor below $1000$, and their product is $m$. The invariant holds after each step. Each split replaces $m$ by two numbers greater than $1$ whose product is $m$, so the total number of prime factors counted with multiplicity bounds the number of splits, and the loop stops. When the stack is empty, the output is a list of primes whose product is the input, and sorting puts it in order. $\blacksquare$
