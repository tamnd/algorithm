---
tag: MW7HYF
kind: algorithm
slug: apr-cl-primality-test
name: APR-CL primality test
aliases:
- Adleman-Pomerance-Rumely test
- cyclotomic primality test
area: number-theory/primality
level: research
summary: A deterministic primality test that checks powers of Jacobi sums in rings of roots of unity. It runs in time (log n)^(O(log log log n)) and proves primes of hundreds of digits.
solves: [primality-testing]
model: multitape-turing-machine
complexity:
  vars: {n: the number tested, c: an absolute constant, t: the even number chosen in line L2}
  time: {worst: O((log n)^(c log log log n)), best: O(1)}
  space: {extra: O(t log n)}
properties: {deterministic: true, recursive: false, certifying: false}
history:
  year: 1983
  people: [Leonard Adleman, Carl Pomerance, Robert Rumely, Henri Cohen, Hendrik Lenstra]
  note: Adleman Pomerance and Rumely gave the first deterministic test in time (log n)^(O(log log log n)) with Gauss sums. Cohen and Lenstra replaced the Gauss sums by Jacobi sums in 1984 and made the test practical.
prereqs: [jacobi-symbol, quadratic-reciprocity, primitive-root, chinese-remainder-theorem, multiplicative-order, roots-of-unity]
see_also: [aks-primality-test, ecpp, miller-rabin, baillie-psw, pocklington-primality-test, quasi-polynomial-time, euler-criterion, primality-proving]
sources:
  - paper: doi:10.2307/2006975
    title: Leonard M. Adleman, Carl Pomerance and Robert S. Rumely, On distinguishing prime numbers from composite numbers, Annals of Mathematics 117 (1983)
    locator: pages 173 to 206 (the Gauss sums test, the choice of t and the running time)
  - paper: doi:10.1090/S0025-5718-1984-0726006-X
    title: H. Cohen and H. W. Lenstra Jr., Primality testing and Jacobi sums, Mathematics of Computation 42 (1984)
    locator: pages 297 to 330 (the Jacobi sums, the conditions L_p and the final search)
  - paper: doi:10.1090/S0025-5718-1987-0866102-2
    title: H. Cohen and A. K. Lenstra, Implementation of a new primality test, Mathematics of Computation 48 (1987)
    locator: pages 103 to 121 (the practical form, the tables of t and timings)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 4.4 (the Gauss sums test, Algorithm 4.4.5 and Theorem 4.4.6, and the Jacobi sums test in Section 4.4.2), and Theorem 4.3.5 on the size of t
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Section 9.1 (the Jacobi sum test, with the proofs of the conditions L_p)
  - url: https://en.wikipedia.org/wiki/Adleman%E2%80%93Pomerance%E2%80%93Rumely_primality_test
    title: Adleman-Pomerance-Rumely primality test, Wikipedia
    locator: the outline of the test and its history
---

The APR-CL test decides whether an integer $n$ is prime, with no randomness and no unproved hypothesis. It checks that certain powers of Jacobi sums are [roots of unity](/roots-of-unity/) modulo $n$, in rings built from roots of unity. If all checks pass, every prime factor of $n$ is a power of $n$ modulo a known number $s > \sqrt n$, and a short search finds a factor or proves that there is none. Its running time $(\log n)^{O(\log \log \log n)}$ is not polynomial, but the exponent grows so slowly that the test is practical for numbers of hundreds of digits.

## In plain words

For a prime number, many identities hold that a composite number usually breaks. Each check of this test takes a small prime, builds a special number from it, raises it to a large power that depends on $n$, and looks at the result modulo $n$. For a prime $n$ the result is always a simple root of one. A composite $n$ is caught by a result that is not.

The strong point is what follows if every check passes. Then each prime factor of $n$ must be one of a short list of numbers, the powers of $n$ modulo a product of small primes. The test tries each number in the list as a factor. If none divides $n$, then $n$ is prime, and this is a proof, not a probability.

## The problem

The input is an integer $n$. The output is "prime" or "composite", and it must be right for every $n$. The code can also give no answer in one rare case, explained at line L16; this did not occur in the tests.

**Cost model.** The integers are of arbitrary precision, with $\lg n$ binary digits, and costs are in bit operations, as on a [multitape Turing machine](/multitape-turing-machine/). A product modulo $n$ costs $M(\log n)$, which is $O((\log n)^2)$ with [schoolbook multiplication](/schoolbook-multiplication/).

**The plan.** The test uses an even number $t$ with $t/2$ odd, and the smallest primes $q_1 < q_2 < \ldots < q_j$ with $q_i - 1 \mid t$, taken until $s = q_1 q_2 \cdots q_j$ has $s^2 > n$. As $t/2$ is odd, every odd $q_i$ has $q_i \equiv 3 \pmod 4$. The code takes the first $t$ of a fixed table that is large enough; the largest $t$ of the table, $29099070$, covers $n$ below about $10^{590}$.

**Characters and Jacobi sums.** Fix an odd $q$ of the plan and an odd prime $p \mid q - 1$, and let $m = p^k$ be the largest power of $p$ that divides $q - 1$. Let $\zeta$ be a primitive $m$-th root of unity, $g$ the least [primitive root](/primitive-root/) modulo $q$, and $\chi(g^x) = \zeta^x$; this is a character of order $m$ on the units modulo $q$. The Jacobi sum is
$$J = J(\chi, \chi) = \sum_{x = 2}^{q - 1} \chi(x) \chi(1 - x),$$
an element of $\mathbb{Z}[\zeta]$. For $c$ coprime to $p$, $\sigma_c$ is the map that replaces $\zeta$ by $\zeta^c$. Let $Y$ be the set of $y$ with $1 \le y < m$ and $p \nmid y$, and for $y \in Y$ let $y^{-1}$ be the inverse modulo $m$. The quantity of the test is
$$S = \prod_{y \in Y} \sigma_{y^{-1}}(J)^{\lfloor n y / m \rfloor} \bmod n.$$
The number $w = \sum_{y \in Y, \, y > m/2} y^{-1} \bmod m$ appears in the proof. Its value modulo $p$ does not depend on $k$, and it is not 0 for any $p$ of the table.

## The algorithm

```pseudo id=main
APR-CL(N)
L1  if N < 2 then return composite
L2  choose t and the primes q_1 < ... < q_j of the plan, s ← q_1 ⋯ q_j
L3  if N is one of the q_i or a prime factor of t then return prime
L4  if gcd(N, t·s) > 1 then return composite
L5  for each odd prime p | t: done[p] ← (N^(p-1) mod p² ≠ 1)
L6  done[2] ← (N mod 4 = 3)
L7  for each odd q in the plan:
L8      for each odd prime p | q - 1, with m = p^k exactly dividing q - 1:
L9          J ← the Jacobi sum J(χ, χ) in Z[ζ_m]
L10         S ← the product of σ_(1/y)(J)^⌊Ny/m⌋ over y in Y, modulo N
L11         if S ≠ ζ^h modulo N for every h then return composite
L12         if p ∤ h then done[p] ← true
L13     E ← (-q)^((N-1)/2) mod N
L14     if E ≠ 1 and E ≠ N - 1 then return composite
L15     if E = N - 1 then done[2] ← true
L16 for each p with done[p] false: run the extra check of p; stop if it shows N composite or gives up
L17 r ← 1; for i ← 1 to t - 1:
L18     r ← r·N mod s
L19     if 1 < r < N and r | N then return composite
L20 return prime
```

**Lines L1 to L4** handle small cases. After line L4, $N$ is coprime to every $q$ and to every prime factor of $t$, and is odd, as $2$ is always in the plan.

**Lines L9 and L10, the Jacobi sum check.** The code builds $J$ from a table of discrete logarithms modulo $q$: the term of $x = g^i$ is $\zeta^{i + \log(1 - g^i)}$. It computes $S$ as $(J^\theta)^{\lfloor N/m \rfloor}$ times the product for $N \bmod m$, where $J^\theta = \prod_{y} \sigma_{y^{-1}}(J)^y$, as $\lfloor N y/m \rfloor = \lfloor N/m \rfloor y + \lfloor (N \bmod m) y / m \rfloor$. The arithmetic is in $\mathbb{Z}[x]/(\Phi_m(x), N)$, with $\Phi_m(x) = \sum_{i < p} x^{i m / p}$, so an element is a list of $\varphi(m)$ numbers modulo $N$. A product costs $\varphi(m)^2$ products modulo $N$, and the large power uses [binary exponentiation](/binary-exponentiation/) with a window of 4 digits.

**Line L11.** If $N$ is prime, $S \equiv \chi(N)^{-wN}$, which is a root of unity. So a result that is no power of $\zeta$ proves $N$ composite.

**Lines L5, L6, L12 and L15, the conditions $L_p$.** The proof needs, for each prime $p \mid t$, the condition $L_p$ on every prime factor $r$ of $N$:

- for odd $p$, the power of $p$ in $r^{p-1} - 1$ is at least the power of $p$ in $N^{p-1} - 1$;
- for $p = 2$, the power of $2$ in $r - 1$ is at least the power of $2$ in $N - 1$.

$L_p$ holds at once if $N^{p-1} \not\equiv 1 \pmod{p^2}$ (line L5), and $L_2$ holds at once if $N \equiv 3 \pmod 4$ (line L6). A primitive root of unity at line L12, or $E = -1$ at line L15, also proves $L_p$.

**Lines L13 to L15, the case $p = 2$.** For $q \equiv 3 \pmod 4$ the character of order 2 is the [Legendre symbol](/legendre-symbol/), and the check is [Euler's criterion](/euler-criterion/) for $-q$: a prime $N$ gives $E = (-q/N) = \pm 1$.

**Line L16, the extra check.** For $p = 2$ the code rejects squares, finds the least $z$ with [Jacobi symbol](/jacobi-symbol/) $(z/N) = -1$, and requires $z^{(N-1)/2} \equiv -1$. For odd $p$ it runs lines L9 to L12 for further primes $q \equiv 1 \pmod p$ that are not in the plan, until one gives a primitive root of unity. For a prime $N$, each such $q$ succeeds unless $N$ is a $p$-th power modulo $q$, which happens for about one $q$ in $p$. The code stops after 60 tries and gives no answer; for a prime $N$ this has a chance of about $p^{-60}$.

**Lines L17 to L19, the final search.** If all checks pass, every prime factor $r$ of $N$ satisfies $r \equiv N^i \pmod s$ for some $0 \le i < t$. The least prime factor of a composite $N$ is at most $\sqrt N < s$, so it is equal to its residue $N^i \bmod s$, and the search finds a factor.

## Example

**A prime.** Take $N = 1999$. The plan is $t = 30$ with the primes $2, 3, 7, 11$, so $s = 462$, and $s^2 = 213444 > 1999$, while $42^2 = 1764$ is too small. $N$ is coprime to $30 \cdot 462$. As $1999^2 \equiv 1 \pmod 9$ and $1999^4 \equiv 1 \pmod{25}$, line L5 sets done[3] and done[5] to false; as $1999 \equiv 3 \pmod 4$, line L6 sets done[2] to true.

| $q$ | $p$, $m$ | $g$ | $J$ in the basis $1, \zeta, \ldots$ | $S$ | $E = (-q)^{999}$ |
|---|---|---|---|---|---|
| 3 | none | 2 | | | 1 |
| 7 | 3, 3 | 3 | $-1 - 3\zeta$ | $\zeta$ | 1 |
| 11 | 5, 5 | 2 | $2\zeta - 2\zeta^2 - \zeta^3$ | $\zeta^3$ | $-1$ |

For $q = 7$: $\sigma_2(J) = -1 - 3\zeta^2 = 2 + 3\zeta$, and $J \sigma_2(J) = 7$, as the norm of a Jacobi sum is $q$. Here $J^\theta = J \sigma_2(J)^2 = 14 + 21\zeta$, and $1999 \bmod 3 = 1$ gives no second factor, so $S = (14 + 21\zeta)^{666} \bmod 1999$, which the code finds equal to $\zeta$. So $h = 1$, and done[3] becomes true. This agrees with the formula for primes: $1999 \equiv 4 = 3^4 \pmod 7$, so $\chi(N) = \zeta^4 = \zeta$, and $\chi(N)^{-wN}$ with $w = 2$ is $\zeta^{-2 \cdot 1999} = \zeta$.

For $q = 11$: $J^\theta \equiv 1939 + 1949\zeta + 1874\zeta^2 + 783\zeta^3$, the second factor for $1999 \bmod 5 = 4$ is $396 + 330\zeta + 825\zeta^2 + 1229\zeta^3$, and $S \equiv (J^\theta)^{399}$ times that factor is $\zeta^3$. So done[5] becomes true; the formula gives $\chi(N) = \zeta^3$, as $1999 \equiv 8 = 2^3 \pmod{11}$, and $w = 1$, so $\zeta^{-3 \cdot 1999} = \zeta^3$.

All conditions are proved, so line L16 does nothing. The search computes $1999^i \bmod 462$ for $i = 1, \ldots, 29$: $151, 163, 127, 235, 373, \ldots, 205$. None of them is a factor of 1999, so 1999 is prime. The proof says more: any prime factor of 1999 would be $1$ or one of these 29 numbers modulo 462.

**A composite.** Take $N = 1891 = 31 \cdot 61$, with the same plan. For $q = 7$, $S \equiv 497 + 1116\zeta$, which is not $1$, $\zeta$ or $\zeta^2 = -1 - \zeta$, so line L11 returns composite. The search alone would not have found the factors: $1891 \bmod 462 = 43$ and $43^2 \equiv 1$, so the powers are only 43 and 1. It is the Jacobi sum check that rules out this $N$.

## Correctness

**Composite answers.** Each "composite" has a reason that no prime has: a proper factor from line L4, L16 or L19; a check that fails at line L11 or L14, where a prime $N$ gives a root of unity and $\pm 1$; or a square or a failed Euler criterion at line L16.

**Prime answers.** Suppose all checks pass, and let $r$ be a prime factor of $N$. Work in the ring $A = \mathbb{Z}[\zeta_m, \zeta_q]/(r)$. The Gauss sum $\tau = \sum_x \chi(x) \zeta_q^x$ has $\tau \bar\tau = q$, so it is a unit in $A$, and $J = \tau^2/\sigma_2(\tau)$. A computation in the group ring shows $S = u^N / \sigma_N(u)$ for a product $u$ of conjugates of $\tau$. The Frobenius map gives $u^r = \chi(r)^{-wr} \sigma_r(u)$ in $A$, and the check gives $u^N = \zeta^h \sigma_N(u)$. From these two, the condition $L_p$ and the [multiplicative order](/multiplicative-order/) of $N^{p-1}$ modulo powers of $p$, one gets $\chi(r) = \chi(N)^{l_p(r)}$ for one number $l_p(r)$ that does not depend on $q$. For $p = 2$ the same follows from Euler's criterion and [quadratic reciprocity](/quadratic-reciprocity/). By the [Chinese remainder theorem](/chinese-remainder-theorem/) on the exponents, $r \equiv N^l \pmod s$ with $0 \le l < t$, and line L19 finds the least prime factor of a composite $N$. So a passing composite cannot reach line L20.

**Termination.** All loops are finite; the search for $z$ ends below $N$ for a number that is not a square, and the extra check for odd $p$ has a cap. The full proof is in the proofs.

## Complexity

**One pair $(p, q)$.** The power at line L10 needs $O(\log N)$ products in $\mathbb{Z}[\zeta_m]$ modulo $N$, and $J^\theta$ needs $O(m \log m)$ more. With schoolbook products of $\varphi(m)^2$ multiplications modulo $N$, one pair costs $O(m^2 (\log N + m \log m) M(\log N))$ bit operations.

**The whole test.** There are at most $d(t)$ primes $q$, each with fewer than $\log_2 t$ primes $p$, and $m \le t$. The search costs $t$ products modulo $s$, and $s < \sqrt N \cdot (t + 1)$. So the cost is $t^{O(1)} (\log N)^{O(1)}$. Adleman, Pomerance and Rumely proved that there is a $t$ below $(\log N)^{c \log \log \log N}$, for a constant $c$, whose primes $q$ have a product above $\sqrt N$ (Crandall and Pomerance, Theorem 4.3.5); their $t$ is a product of distinct small primes, so $t/2$ is odd, as this page needs. This gives the bound $(\log n)^{O(\log \log \log n)}$, which is [quasi-polynomial time](/quasi-polynomial-time/) and is not polynomial. Odlyzko and Pomerance showed that for infinitely many $n$ no $t$ much smaller works, so the bound is the true cost of the method.

**In practice** the $t$ of the table are small: for $n$ of 300 digits, $t = 2645370 = 2 \cdot 3^2 \cdot 5 \cdot 7 \cdot 13 \cdot 17 \cdot 19$, so $m \le 19$, and the many pairs are cheap. On a loaded machine the Python code of this page takes about 1 second for a 100-digit prime, 10 seconds for 200 digits and a minute for 300 digits. All $n \le 10^5$ take 4.5 seconds together.

**Best case.** $n < 2$ stops at line L1, and an even $n$ stops at line L4 after the plan.

**Space.** The table of logarithms modulo $q$ has $q \le t + 1$ entries, and an element of the ring has $\varphi(m) < t$ numbers modulo $n$, so $O(t \log n)$ bits.

## Properties

- **Deterministic and proved.** No randomness and no hypothesis such as the generalized Riemann hypothesis is used; both answers are always right.
- **Not certifying.** A prime answer gives no short certificate that is faster to check than to repeat the test, unlike [ECPP](/ecpp/).
- **Not polynomial.** The exponent of $\log n$ grows like $\log \log \log n$, which is below 3 for every $n$ with fewer than 200 million digits, but is not bounded.
- **General.** It needs no special form of $n$ and no factorization of $n - 1$.

## Variants and improvements

- **Gauss sums.** The first form of Adleman, Pomerance and Rumely works with Gauss sums in $\mathbb{Z}[\zeta_p, \zeta_q]$, a ring of degree $(p - 1)(q - 1)$, which is much slower than the Jacobi sums in $\mathbb{Z}[\zeta_p]$.
- **Powers of 2.** Cohen and Lenstra allow $4 \mid t$, so $q \equiv 1 \pmod 4$ is possible; the characters of order $2^k$ with $k \ge 2$ then need the further Jacobi sums $J_2$ and $J_3$ and a separate proof. This page keeps $t/2$ odd so that the case $p = 2$ is only Euler's criterion.
- **Prime powers in $s$.** Cohen and Lenstra use $e(t) = 2 \prod_{q - 1 \mid t} q^{v_q(t) + 1}$ in place of $s$, which gives a larger modulus for the same $t$.
- **Combined with $n - 1$ and $n + 1$.** Known factors of $n - 1$ or $n + 1$, as in the [Pocklington](/pocklington-primality-test/) and [Lucas](/lucas-primality-test/) tests, give more information modulo $s$ and allow a smaller $t$ (Lenstra; Bosma and van der Hulst).
- **Cyclotomy with Gaussian periods.** Mihăilescu developed a cyclotomy test that uses sums over subgroups instead of characters, and used it for large numbers.

## When to use it

Use APR-CL to prove a number of up to some thousands of digits prime when a deterministic, unconditional answer is needed and no certificate is wanted. It is a good choice for a library function that must never be wrong. Run a fast [Miller-Rabin](/miller-rabin/) or [Baillie-PSW](/baillie-psw/) test first, as almost every composite fails it at once. If a certificate is needed, use [ECPP](/ecpp/). The [AKS test](/aks-primality-test/) has a polynomial bound but is far slower in practice.

## Pitfalls

- **The full power of $p$.** $m$ must be the full power $p^k$ of $p$ in $q - 1$, not a smaller power, or the character is not the one the proof uses.
- **The units $w$.** The proof needs $p \nmid w$. The value of $w$ modulo $p$ is $2(2^{p-1} - 1)/p$, which is 0 only for the Wieferich primes $p = 1093$ and $3511$. The code checks it for each $p$ of the plan; the extra pairs of line L16 use the same $p$, so the same value.
- **Forgetting $L_p$.** Without the conditions $L_p$, the final search proves nothing. If some $L_p$ cannot be proved, the test must not answer prime.
- **Negative bases.** In line L13, $-q$ must be reduced to $N - q$; a negative base in a modular power can give a wrong result in some languages.
- **The search bound.** The search needs $s > \sqrt N$ and all $t - 1$ powers; stopping early, or using $s < \sqrt N$, can miss the factor.
- **Square $N$.** The Jacobi symbol of a square is never $-1$, so the extra check for $p = 2$ must reject squares first, or the search for $z$ does not end.

## Implementations

## History

Before 1980 every deterministic test that was proved to work for all $n$ took time that grows like a power of $n$, except under the generalized Riemann hypothesis, as in Miller's test of 1976. Leonard Adleman, Carl Pomerance and Robert Rumely found a test with Gauss sums whose running time is $(\log n)^{O(\log \log \log n)}$; their paper appeared in the Annals of Mathematics in 1983. Henri Cohen and Hendrik Lenstra replaced the Gauss sums by Jacobi sums, which work in smaller rings, and gave the final search its simple form; their paper of 1984 made the test practical, and Cohen and Arjen Lenstra described an implementation in 1987. The name APR-CL comes from the five authors. In 2002 the [AKS test](/aks-primality-test/) became the first deterministic test with a proved polynomial bound.

## References
