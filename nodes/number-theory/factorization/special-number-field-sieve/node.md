---
tag: 89BD3K
kind: algorithm
slug: special-number-field-sieve
name: Special number field sieve
aliases:
- SNFS
area: number-theory/factorization
level: research
summary: The number field sieve for integers of a special form such as 2^k - 1 or 2^k + 1, where a polynomial with tiny coefficients exists. Heuristically L_N[1/3, (32/9)^(1/3)].
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the integer to factor, n: the number of binary digits of N, d: the degree of f, B: the smoothness bound, K: the number of columns of the matrix, A: the half width of the sieve line, Y: the number of sieve lines, D: the number of dependencies tried, L: the largest bit length of a coefficient of the algebraic square}
  time: {worst: O(Y A K n + K^3 + D d^2 L^2), heuristic: exp(((32/9)^(1/3) + o(1)) (ln N)^(1/3) (ln ln N)^(2/3))}
  space: {extra: O(K^2 + A + d L)}
properties: {deterministic: true, recursive: false}
prereqs: [general-number-field-sieve]
see_also: [general-number-field-sieve, quadratic-sieve, multiple-polynomial-quadratic-sieve, elliptic-curve-factorization, number-field-sieve-discrete-logarithm, relation-collection, integer-factorization]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 6.2.3, page 288 (coefficients of size n^(ε/d) give L(n)^(((2 + 2ε)/d)^(1/2) + o(1)) for fixed d and the constant (32(1 + ε)/9)^(1/3)); Section 6.2.7, Special number field sieve, pages 298 to 300 (the polynomial x^5 ± b^(5 - r) for b^k ± 1, F9 with x^5 + 8 and m = 2^103, and 10^193 - 1); Exercise 6.13
  - paper: doi:10.1007/BFb0091537
    title: A. K. Lenstra, H. W. Lenstra Jr., M. S. Manasse and J. M. Pollard, The number field sieve, in The development of the number field sieve, Lecture Notes in Mathematics 1554, Springer, 1993
    locator: pages 11 to 42
  - paper: doi:10.1090/S0025-5718-1993-1182953-4
    title: A. K. Lenstra, H. W. Lenstra Jr., M. S. Manasse and J. M. Pollard, The factorization of the ninth Fermat number, Mathematics of Computation 61(203) (1993)
    locator: pages 319 to 349
  - paper: doi:10.1007/BFb0091536
    title: J. M. Pollard, Factoring with cubic integers, in The development of the number field sieve, Lecture Notes in Mathematics 1554, Springer, 1993
    locator: pages 4 to 10
  - paper: doi:10.1090/S0002-9904-1903-01079-9
    title: F. N. Cole, On the factoring of large numbers, Bulletin of the American Mathematical Society 10(3) (1903)
    locator: pages 134 to 137 (2^67 - 1 = 193707721 · 761838257287)
  - paper: doi:10.1007/978-3-540-76900-2_1
    title: Kazumaro Aoki, Jens Franke, Thorsten Kleinjung, Arjen K. Lenstra and Dag Arne Osvik, A kilobit special number field sieve factorization, ASIACRYPT 2007, Lecture Notes in Computer Science 4833
    locator: pages 1 to 12 (2^1039 - 1)
---

The special number field sieve, SNFS, is the [number field sieve](/general-number-field-sieve/) applied to an integer $N$ that divides a number of a special form, such as $r^e \pm s$ with small $r$ and $s$. For such $N$ there is a polynomial $f$ with tiny coefficients and an integer $m$ with $f(m) \equiv 0 \pmod N$; for $2^{67} - 1$ it is $f(x) = x^3 - 4$ with $m = 2^{23}$. Small coefficients make the norms on the algebraic side much smaller than with a general polynomial, and the heuristic running time drops to $L_N[1/3, (32/9)^{1/3}]$. It was the first form of the number field sieve, and it has factored many Cunningham numbers $b^k \pm 1$.

## In plain words

Some numbers have a short description, such as two to some power, minus one. For those numbers there is a polynomial with tiny coefficients and an integer where the polynomial is a multiple of the number.

Feed that polynomial to the number field sieve. Each pair of small integers again gives two numbers, one ordinary and one from the ring of the polynomial. With tiny coefficients, the second number is much smaller than for a general polynomial, so both numbers break into small primes much more often.

Everything else is the same as in the general method: collect pairs where both sides break into small primes, combine them until both sides are squares, take the square root on each side, and finish with one gcd. The method also works for any factor of the special number, with the same polynomial.

## The problem

**Input.** An odd composite $N$ that is not a prime power, a monic $f \in \mathbb{Z}[x]$ of odd prime degree $d$ and an integer $m$ with $f(m) \equiv 0 \pmod N$, and the parameters $B$, $A$, $Y$, $k$ and $E$ of the general method.

**Output.** A proper factor $g$ of $N$, or $1$ for a failure with these parameters.

**The special polynomial.** Let $N$ divide $r^e + s$ with $r \ge 2$ and $s \ne 0$. For a degree $d$, let $l = \lceil e/d \rceil$ and $t = dl - e$, so $0 \le t < d$. Then
$$r^t(r^e + s) = (r^l)^d + s r^t,$$
so $f(x) = x^d + sr^t$ and $m = r^l$ satisfy $f(m) = r^t(r^e + s) \equiv 0 \pmod N$. The coefficient $sr^t$ is below $|s| r^{d-1}$, a constant, while $m \approx (r^e)^{1/d}$. This is the scheme of Crandall and Pomerance, Section 6.2.7, except that their $t$ is $d$ when $d \mid e$, and this page takes $t = 0$. Every factor of $r^e + s$ can use the same $f$, with $m$ reduced modulo that factor.

**Cost model.** As for the general method: word operations for the sieve, $O(n)$ per trial division of a value with $O(n)$ digits, a worst-case bound for fixed parameters, and a heuristic subexponential bound.

## The algorithm

The steps after line L1 are those of the general method; the page [general number field sieve](/general-number-field-sieve/) explains them in detail.

```pseudo id=main
SNFS(N, f, m, B, A, Y, k, E)       ▷ f monic of odd prime degree d, f(m) ≡ 0 (mod N); returns a proper factor or 1
L1  check f(m) ≡ 0 (mod N); for each integer root z of f, if 1 < gcd(m − z, N) < N, return it; if 1 < gcd(f′(m), N) < N, return it
L2  P ← primes p ≤ B; R ← pairs (p, r) with f(r) ≡ 0 (mod p); Q ← k pairs (q, s) with q > B prime, f(s) ≡ 0 and f′(s) ≢ 0 (mod q)
L3  for b = 1, 2, …, Y: sieve a ∈ [−A, A] on both sides; keep a with gcd(a, b) = 1 and both sums large
L4      if a − bm and F(a, b) = b^d f(a/b) both factor over P, append (a, b) to S; stop when |S| = 2 + |P| + |R| + k + E
L5  for (a, b) in S: vector mod 2 of the two signs, the exponents of p in a − bm, of (p, r) in F(a, b), and the k characters
L6  for each subset T of S whose vectors add to 0 mod 2 do
L7      x ← f′(m) ∏_{p ∈ P} p^(e_p/2) mod N, where ∏_T (a − bm) = ∏ p^(e_p)
L8      δ ← the square root of γ = f′(α)² ∏_T (a − bα) in Z[α], or go to the next T if there is none; y ← δ(m) mod N
L9      g ← gcd(x − y, N); if 1 < g < N then return g
L10 return 1
```

Line L1 is the only new part. A special polynomial can be reducible: for $2^{33} - 1$ and $d = 3$, $l = 11$ and $t = 0$, so $f = x^3 - 1 = (x - 1)(x^2 + x + 1)$. Then $m - 1 = 2^{11} - 1 = 2047$ divides $N$, an algebraic factor, and line L1 returns it. For $f = x^d + c$ with $d$ an odd prime, $f$ is reducible over $\mathbb{Q}$ exactly when $-c$ is a $d$-th power, that is, when $f$ has an integer root, so line L1 catches every reducible case. For $x^3 + c$ the inert prime of line L8 must satisfy $p \equiv 1 \pmod 3$, since every residue is a cube modulo a prime $p \equiv 2 \pmod 3$; together with $p \equiv 3 \pmod 4$ that means $p \equiv 7 \pmod{12}$.

The driver `factorize` looks for a form $N = r^e + s$ with $r \le 12$ and $|s| \le 12$, builds the polynomials of degrees $3$ and $5$, and for each composite cofactor tries them in the order of an estimate of the size of $(a - bm)F(a, b)$. It keeps only those that beat a base-$m$ polynomial of the cofactor, and that base-$m$ polynomial, the general method, comes last.

## Example

Take $N = 2^{41} - 1 = 2199023255551 = 13367 \cdot 164511353$ and $d = 3$. Then $l = 14$ and $t = 1$, so $f(x) = x^3 - 2$ and $m = 2^{14} = 16384$, with $f(m) = 2^{42} - 2 = 2N$. The norm is $F(a, b) = a^3 - 2b^3$.

With $B = 200$, $A = 600$ and $k = 10$, the rational base has $46$ primes and the algebraic base has $40$ pairs, starting $(2, 0), (3, 2), (5, 3), (11, 7), (17, 8), (23, 16)$. The characters start at $(223, 68)$ and $(223, 179)$. That is $98$ columns, so line L4 stops at $108$ relations, which the lines $b = 1$ to $59$ supply. The first three are:

| $(a, b)$ | $a - bm$ | $F(a, b)$ |
|---|---|---|
| $(-224, 1)$ | $-16608 = -2^5 \cdot 3 \cdot 173$ | $-11239426 = -2 \cdot 11 \cdot 43 \cdot 109^2$ |
| $(-208, 1)$ | $-16592 = -2^4 \cdot 17 \cdot 61$ | $-8998914 = -2 \cdot 3 \cdot 107^2 \cdot 131$ |
| $(-176, 1)$ | $-16560 = -2^4 \cdot 3^2 \cdot 5 \cdot 23$ | $-5451778 = -2 \cdot 101 \cdot 137 \cdot 197$ |

The rational side is about $bm$ and the algebraic side about $a^3$. The base-$m$ polynomial of $N$ is $x^3 + 18x^2 - 305x - 123$ with $m = 12998$. Its $m$ is a little smaller, but its coefficients are larger, and the estimate `value_size` of the largest product $(a - bm)F(a, b)$ over the box $|a|, b \le 600$ is $60$ binary digits for it against $53$ for $x^3 - 2$.

Elimination gives $21$ dependencies of $28$ to $52$ relations each, and every one of them gives an exact square root in $\mathbb{Z}[\alpha]$ with the inert prime $463$ (and $463 \equiv 7 \pmod{12}$). With $f'(m) = 3m^2 = 805306368$, the first one gives $\gcd(x - y, N) = 1$. The second has $52$ relations and gives $x = 1005209741009$ and $y = 1953782202407$, with $x^2 \equiv y^2 \pmod N$ and $\gcd(x - y, N) = 164511353$. Its $\gamma$ has coefficients of $283$ binary digits, and $\delta$ of $141$. Of the $21$ dependencies, $8$ give a proper factor, $8$ give $1$ and $5$ give $N$.

A larger case is Cole's number $2^{67} - 1 = 193707721 \cdot 761838257287$, with $f = x^3 - 4$ and $m = 2^{23}$, so $f(m) = 4N$. With $B = 764$ there are $135$ primes, $133$ pairs and $54$ characters, the implementation collects $334$ relations from $97$ lines and returns $193707721$. The run takes about $1.2$ seconds in Python. The same code with the base-$m$ polynomial $x^3 + 192x^2 - 1584838x + 405511$, $m = 5284428$, needs $B = 7465$ and about $14$ seconds. The test file checks these numbers.

## Correctness

The output is $1$ or a proper factor of $N$: every return of a value other than $1$ is a gcd with $N$, or a prime divisor of $N$ found by trial division, that is tested to lie strictly between $1$ and $N$. A subset $T$ that reaches line L9 gives $x^2 \equiv y^2 \pmod N$, by the same argument as in the general method. The only fact used about $f$ and $m$ is that $f(m) \equiv 0 \pmod N$, so that $\alpha \mapsto m$ defines a ring homomorphism $\mathbb{Z}[\alpha] \to \mathbb{Z}/N\mathbb{Z}$; $f(m) = N$ is not needed. The special polynomial satisfies $f(m) = r^t(r^e + s)$, which is $0$ modulo every divisor of $r^e + s$. Every loop is bounded, so the algorithm stops. The full proof is below.

Whether a dependency is a square in $\mathbb{Z}[\alpha]$, and whether it splits $N$, are the same heuristics as in the general method.

## Complexity

- **Proved bound for fixed parameters.** The same as for the general method: $O(YAKn)$ word operations for sieving and trial division, $O(K^3)$ bit operations for the elimination, and $O(d^2L^2)$ bit operations per square root with schoolbook arithmetic.
- **Heuristic bound.** Crandall and Pomerance (Section 6.2.3) show that if the coefficients of $f$ are at most $N^{\varepsilon/d}$, the time is $L(N)^{\sqrt{(2 + 2\varepsilon)/d} + o(1)}$ for fixed $d$, with $L(N) = \exp(\sqrt{\ln N \ln \ln N})$, and $\exp\big(((32(1 + \varepsilon)/9)^{1/3} + o(1))(\ln N)^{1/3}(\ln \ln N)^{2/3}\big)$ when $d$ grows suitably. Bounded coefficients give $\varepsilon = o(1)$ and the constant $(32/9)^{1/3} \approx 1.526$, against $(64/9)^{1/3} \approx 1.923$ for the general method. The difference is that the norms no longer contain the factor $N^{1/d}$ from the coefficients.
- **Fixed degree.** For $d = 3$ the fixed degree bound is $L(N)^{\sqrt{2/3} + o(1)}$, with $\sqrt{2/3} \approx 0.82$, below the exponent $1$ of the quadratic sieve. So even the toy version with $d = 3$ is heuristically faster than the quadratic sieve for special numbers, unlike the general method with $d = 3$.
- **Space.** $O(K^2)$ bits for the matrix, $O(A)$ for a sieve line, $O(dL)$ bits for the square root.

## Properties

- **Factors of special numbers.** The polynomial depends only on $r^e + s$, so it serves every factor of it, even after known factors are divided out. The size of the work depends on $r^e$, not on the size of the cofactor.
- **Small Galois groups.** For $f = x^d + c$ the Galois group has order dividing $d\varphi(d)$ rather than the generic $d!$, which makes free relations more useful (Crandall and Pomerance, Section 6.2.7).
- **Deterministic.** For fixed parameters the output is fixed.
- **Not general.** Only integers with a known special multiple benefit. For a random $N$ there is no polynomial with tiny coefficients, by a counting argument.

## Variants and improvements

- **Other forms.** Any small multiple of a number close to a power works. Lenstra, Lenstra, Manasse and Pollard factored $F_9 = 2^{512} + 1$ with $f = x^5 + 8$ and $m = 2^{103}$, so $f(m) = 8F_9$, and ignored the known factor $2424833$.
- **Two algebraic sides.** If $m$ is too large for a good linear polynomial, one can use two polynomials with a common root modulo $N$. For $10^{193} - 1$, Elkenbracht-Huizing and Montgomery combined $5x^3 - 10^8$ with a quadratic found by lattice reduction (Crandall and Pomerance, Section 6.2.7).
- **Degree choice.** The best degree grows like $(\ln N/\ln \ln N)^{1/3}$, as in the general method. The record factorizations used degree $5$ for $F_9$ and degree $6$ for $2^{1039} - 1$.
- **All the improvements of the general method.** Lattice sieving, large primes, filtering and block Lanczos or block Wiedemann apply unchanged.

## When to use it

Use SNFS when $N$ divides a number $r^e \pm s$ with small $r$ and $s$, or some other value of a polynomial with tiny coefficients, and has no factor that [ECM](/elliptic-curve-factorization/) can find quickly. This covers the Cunningham tables, Mersenne and Fermat numbers, and their cofactors. For numbers with no such form, use the [general number field sieve](/general-number-field-sieve/) or, below about 100 digits, the [multiple polynomial quadratic sieve](/multiple-polynomial-quadratic-sieve/). The polynomial trick is also used in the [number field sieve for discrete logarithms](/number-field-sieve-discrete-logarithm/) in fields of special characteristic.

## Pitfalls

- **A reducible polynomial.** If $d \mid e$ and $s = -1$, the scheme gives $x^d - 1$, which is reducible. No inert prime exists, so the square root step cannot work. Check for an integer root first; it gives the algebraic factor $\gcd(m - z, N)$, for example $2047 \mid 2^{33} - 1$.
- **The wrong congruence.** $f(m)$ is $r^t(r^e + s)$, not $N$. Code that tests $f(m) = N$, or that builds $f$ from the base-$m$ digits of $N$, loses the special form.
- **A special polynomial that is worse.** For a small cofactor $C$ of a large $r^e + s$, $m = r^l$ can be much larger than $C^{1/d}$. For the cofactor $C = 20857 \cdot 599479$ of $2^{66} - 1$, the special $x^3 - 1$ is reducible and gives no factor of $C$, and $x^5 - 16$ with $m = 2^{14}$ has a value estimate of $83$ binary digits against $63$ for a base-$m$ cubic of $C$. Before the driver compared these estimates, it spent $45$ seconds on $2^{66} - 1$; now it takes under a second.
- **Inert primes for $x^d + c$.** Modulo a prime $p \not\equiv 1 \pmod d$, $x^d + c$ always has a root, so it is never irreducible. A search for inert primes must look at $p \equiv 1 \pmod d$.
- **Unbalanced sides.** With $d = 3$, the rational side $bm$ is much larger than the algebraic side $a^3$. A larger $B$ helps more than a wider line.

## Implementations

## History

Frank Nelson Cole factored $2^{67} - 1$ by hand in 1903. In 1988 John Pollard proposed factoring numbers close to a cube with cubic integers, the idea of the number field sieve. Arjen Lenstra, Hendrik Lenstra, Mark Manasse and Pollard developed it for numbers of special form, presented it at STOC 1990, and with many helpers factored the ninth Fermat number $2^{512} + 1$ in 1990. The general method came after. The special sieve has since factored many Cunningham numbers, among them $2^{1039} - 1$ in 2007 by Kazumaro Aoki, Jens Franke, Thorsten Kleinjung, Arjen Lenstra and Dag Arne Osvik, the first SNFS factorization of a 1039 bit number.

## References
