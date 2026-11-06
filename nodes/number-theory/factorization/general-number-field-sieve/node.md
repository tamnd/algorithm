---
tag: H28VR1
kind: algorithm
slug: general-number-field-sieve
name: General number field sieve
aliases:
- GNFS
- NFS
area: number-theory/factorization
level: research
summary: The fastest known classical method to factor a large integer with no special form. It gets a congruence of squares from relations smooth on two sides. Heuristically L_N[1/3, (64/9)^(1/3)].
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the integer to factor, n: the number of binary digits of N, d: the degree of f, B: the smoothness bound, K: the number of columns of the matrix, A: the half width of the sieve line, Y: the number of sieve lines, D: the number of dependencies tried, L: the largest bit length of a coefficient of the algebraic square}
  time: {worst: O(Y A K n + K^3 + D d^2 L^2), heuristic: exp(((64/9)^(1/3) + o(1)) (ln N)^(1/3) (ln ln N)^(2/3))}
  space: {extra: O(K^2 + A + d L)}
properties: {deterministic: true, recursive: false}
prereqs: [quadratic-sieve, relation-collection, factor-base, smooth-number, irreducible-polynomial, hensel-lifting]
see_also: [special-number-field-sieve, quadratic-sieve, multiple-polynomial-quadratic-sieve, number-field-sieve-discrete-logarithm, function-field-sieve, block-lanczos-algorithm, congruence-of-squares, integer-factorization]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 6.2, Number field sieve, pages 278 to 301; Lemma 6.2.1 (squares and the exponents of first degree primes), Section 6.2.3, pages 285 to 288 (the heuristic complexity and the degree (3 ln n/ln ln n)^(1/3)); Section 6.2.4, pages 288 to 291 (the four obstructions, Lemma 6.2.3 on f'(α), Lemma 6.2.4 on quadratic characters); Section 6.2.5 (square roots); Algorithm 6.2.5, page 293
  - paper: doi:10.1007/BFb0091539
    title: J. P. Buhler, H. W. Lenstra Jr. and Carl Pomerance, Factoring integers with the number field sieve, in The development of the number field sieve, Lecture Notes in Mathematics 1554, Springer, 1993
    locator: pages 50 to 94 (the general method, its heuristic analysis, and the bound on the obstructions, Theorem 6.7)
  - paper: doi:10.1007/BFb0091537
    title: A. K. Lenstra, H. W. Lenstra Jr., M. S. Manasse and J. M. Pollard, The number field sieve, in The development of the number field sieve, Lecture Notes in Mathematics 1554, Springer, 1993
    locator: pages 11 to 42
  - paper: doi:10.1007/BFb0091536
    title: J. M. Pollard, Factoring with cubic integers, in The development of the number field sieve, Lecture Notes in Mathematics 1554, Springer, 1993
    locator: pages 4 to 10 (the original idea, for numbers close to a cube)
  - paper: doi:10.1007/BFb0091540
    title: Jean-Marc Couveignes, Computing a square root for the number field sieve, in The development of the number field sieve, Lecture Notes in Mathematics 1554, Springer, 1993
    locator: pages 95 to 102
  - paper: "Matthew E. Briggs, An introduction to the general number field sieve, Master's thesis, Virginia Polytechnic Institute and State University, 1998"
    locator: the worked example with n = 45113 and m = 31
  - paper: doi:10.1007/978-3-030-56880-1_3
    title: Fabrice Boudot, Pierrick Gaudry, Aurore Guillevic, Nadia Heninger, Emmanuel Thomé and Paul Zimmermann, Comparing the difficulty of factorization and discrete logarithm, a 240-digit experiment, CRYPTO 2020, Lecture Notes in Computer Science 12171
    locator: pages 62 to 91 (the factorization of RSA-240 with CADO-NFS)
---

The general number field sieve, GNFS or NFS, is the fastest known classical algorithm to factor a large integer $N$ that has no special form. Like the [quadratic sieve](/quadratic-sieve/), it collects many [smooth](/smooth-number/) relations and combines them by linear algebra modulo $2$ into a [congruence of squares](/congruence-of-squares/) $x^2 \equiv y^2 \pmod N$. The new idea is to take one side of each relation from the ring $\mathbb{Z}[\alpha]$, where $\alpha$ is a root of a polynomial $f$ with $f(m) \equiv 0 \pmod N$, so that both sides are numbers of size about $N^{1/d}$ instead of $\sqrt N$. Its heuristic running time is $L_N[1/3, (64/9)^{1/3}]$, and it holds the record for the factorization of RSA moduli.

## In plain words

The quadratic sieve looks for numbers that break into small primes, but its numbers are large, so such numbers are rare.

The number field sieve makes the numbers much smaller. It picks a polynomial with small coefficients whose value at one integer is the number to factor. Each pair of small integers then gives two numbers: one is an ordinary integer, and the other is the size of an element of a larger ring that the polynomial defines. Both numbers are small, so both often break into small primes.

When both break, the pair is kept. A table of such pairs is combined, as in the quadratic sieve, until a product is a square on both sides. The square root on the ring side is the hard step. Mapping that root back to the integers gives two numbers with equal squares, and one gcd then splits the number.

## The problem

**Input.** An odd composite $N$ that is not a prime power, a degree $d$ (an odd prime, $3$ or $5$ in the implementation), a smoothness bound $B$, a half width $A$ and a count $Y$ of sieve lines, a count $k$ of quadratic characters, and a count $E \ge 1$ of extra relations.

**Output.** A proper factor $g$ of $N$ (with $1 < g < N$), or $1$ for a failure with these parameters.

**The two sides.** Let $f(x) = x^d + c_{d-1}x^{d-1} + \dots + c_0 \in \mathbb{Z}[x]$ be monic with $f(m) = N$ for an integer $m$, and let $\mathbb{Z}[\alpha] = \mathbb{Z}[x]/(f)$. Since $f(m) \equiv 0 \pmod N$, the map $\varphi\colon \mathbb{Z}[\alpha] \to \mathbb{Z}/N\mathbb{Z}$ with $\varphi(\alpha) = m$ is a ring homomorphism. For a pair $(a, b)$ with $\gcd(a, b) = 1$ and $b \ge 1$, the integer $a - bm$ is the rational side and $a - b\alpha$ is the algebraic side, and $\varphi(a - b\alpha) = a - bm$. The size of $a - b\alpha$ is its norm
$$F(a, b) = b^d f(a/b) = \sum_{i=0}^{d} c_i a^i b^{d-i},$$
an integer. If a set $T$ of pairs makes $\prod_T (a - bm) = v^2$ in $\mathbb{Z}$ and $f'(\alpha)^2 \prod_T (a - b\alpha) = \delta^2$ in $\mathbb{Z}[\alpha]$, then $x = f'(m)v$ and $y = \varphi(\delta)$ satisfy $x^2 \equiv y^2 \pmod N$.

**Cost model.** On the [word RAM](/word-ram/), sieve steps and arithmetic modulo the primes below $B$ cost $O(1)$. For $N$ with $n$ binary digits, a value $a - bm$ or $F(a, b)$ has $O(n)$ digits for $|a|, b$ below $N^{1/d}$, and a trial division of it by a word prime costs $O(n)$. The worst case bound below is proved for fixed parameters; the subexponential bound is a heuristic, and no proved bound of this form is known.

## The algorithm

$S$ is the list of relations. $P$ is the rational factor base, $R$ the algebraic one, and $Q$ the set of quadratic characters.

```pseudo id=main
GNFS(N, d, B, A, Y, k, E)        ▷ N odd composite, not a prime power; returns a proper factor of N or 1
L1  choose m and a monic f of degree d with f(m) = N and small coefficients; if 1 < gcd(f′(m), N) < N, return it
L2  P ← primes p ≤ B; R ← pairs (p, r) with f(r) ≡ 0 (mod p); Q ← k pairs (q, s) with q > B prime, f(s) ≡ 0 and f′(s) ≢ 0 (mod q)
L3  for b = 1, 2, …, Y: sieve a ∈ [−A, A], adding log p where a ≡ bm (mod p) and where a ≡ br (mod p); keep a with gcd(a, b) = 1 and both sums large
L4      if a − bm and F(a, b) both factor over P, append (a, b) to S; stop when |S| = 2 + |P| + |R| + k + E
L5  for (a, b) in S: vector mod 2 of the signs of a − bm and F(a, b), the exponents of p in a − bm, the exponents of (p, r) in F(a, b), and [((a − bs)/q) = −1] for (q, s) in Q
L6  for each subset T of S whose vectors add to 0 mod 2 do
L7      x ← f′(m) ∏_{p ∈ P} p^(e_p/2) mod N, where ∏_T (a − bm) = ∏ p^(e_p)
L8      δ ← the square root of γ = f′(α)² ∏_T (a − bα) in Z[α], or go to the next T if there is none; y ← δ(m) mod N
L9      g ← gcd(x − y, N); if 1 < g < N then return g
L10 return 1
```

Line L1 is polynomial selection. The implementation tries $m = \lfloor N^{1/d} \rfloor, m - 1, \dots$, writes $N$ in base $m$ with digits in $(-m/2, m/2]$, and keeps the monic expansion with the smallest largest coefficient. Before line L2 it removes small prime factors by trial division and finds an inert prime: the least prime $p > B$ with $p \equiv 3 \pmod 4$ such that $f$ is [irreducible](/irreducible-polynomial/) modulo $p$. If none is found, $f$ is reducible over $\mathbb{Q}$ and the call returns $1$.

Line L2 builds the [factor bases](/factor-base/). A pair $(p, r)$ stands for a prime ideal of degree one: for $p \nmid b$, $p$ divides $F(a, b)$ exactly when $a \equiv br \pmod p$ for a root $r$ of $f$ modulo $p$. Lines L3 and L4 are a line sieve: for each $b$, one array of logarithms per side over $a \in [-A, A]$, with candidates confirmed by trial division, as in the [relation collection](/relation-collection/) of the quadratic sieve. Each relation gives one row of the matrix in line L5. Its algebraic part puts the exponent of $p$ in $F(a, b)$ in the column of the one pair $(p, r)$ with $a \equiv br$. The character bits are [Legendre symbols](/legendre-symbol/), computed by [Euler's criterion](/euler-criterion/).

Line L6 runs over the dependencies found by [Gaussian elimination](/gaussian-elimination/) on bit masks. Line L7 takes the integer square root from the summed exponents. Line L8 is the algebraic square root. With the inert prime $p$ and $q = p^d$, $\mathbb{F}_p[x]/(f)$ is the field with $q$ elements and $q \equiv 3 \pmod 4$. If $\gamma$ is a square there, $r_0 = \gamma^{(3q-5)/4}$ satisfies $r_0^2\gamma = 1$. Newton's iteration $r \leftarrow r(3 - \gamma r^2)/2$ lifts $r_0$ to $\gamma^{-1/2}$ modulo $p^2, p^4, p^8, \dots$, which is [Hensel lifting](/hensel-lifting/) in the ring $(\mathbb{Z}/p^j)[x]/(f)$. Then $\gamma r$ is a square root of $\gamma$ modulo $p^j$. Once its coefficients, taken between $-p^j/2$ and $p^j/2$, square exactly to $\gamma$, that is $\delta$. Line L9 is the gcd of the congruence of squares.

## Example

Take Briggs's example $N = 45113 = 197 \cdot 229$, $d = 3$ and $m = 31$. The base $31$ digits of $N$ give $f(x) = x^3 + 15x^2 + 29x + 8$, and $f(31) = 45113$. With $B = 100$, $A = 300$ and $k = 10$, the rational base has the $25$ primes up to $100$ and the algebraic base has $21$ pairs, starting $(2, 0), (7, 6), (17, 13), (23, 11)$. The characters start at $(101, 87)$. That gives $2 + 25 + 21 + 10 = 58$ columns, so line L4 stops at $68$ relations, which the lines $b = 1$ to $9$ supply. The inert prime is $307$.

Elimination gives $22$ dependencies. The first one has these nine relations:

| $(a, b)$ | $a - bm$ | $F(a, b)$ |
|---|---|---|
| $(-116, 1)$ | $-147 = -3 \cdot 7^2$ | $-1362412 = -2^2 \cdot 43 \cdot 89^2$ |
| $(-104, 1)$ | $-135 = -3^3 \cdot 5$ | $-965632 = -2^{10} \cdot 23 \cdot 41$ |
| $(-32, 1)$ | $-63 = -3^2 \cdot 7$ | $-18328 = -2^3 \cdot 29 \cdot 79$ |
| $(-13, 1)$ | $-44 = -2^2 \cdot 11$ | $-31$ |
| $(-4, 1)$ | $-35 = -5 \cdot 7$ | $68 = 2^2 \cdot 17$ |
| $(1, 1)$ | $-30 = -2 \cdot 3 \cdot 5$ | $53$ |
| $(142, 1)$ | $111 = 3 \cdot 37$ | $3169874 = 2 \cdot 29 \cdot 31 \cdot 41 \cdot 43$ |
| $(-17, 3)$ | $-110 = -2 \cdot 5 \cdot 11$ | $3871 = 7^2 \cdot 79$ |
| $(56, 3)$ | $-37$ | $331568 = 2^4 \cdot 17 \cdot 23 \cdot 53$ |

The product of the rational sides is $2^4 3^8 5^4 7^4 11^2 37^2 = 161538300^2$. The product of the norms is $3310622949437167616^2$. Here a square norm is necessary but not enough; the matrix columns for the pairs and the characters make $\gamma$ a square in fact.

- **The rational root.** $f'(x) = 3x^2 + 30x + 29$ and $f'(31) = 3842$, so $x = 3842 \cdot 161538300 \bmod 45113 = 6045$.
- **The algebraic root.** $\gamma = f'(\alpha)^2 \prod_T (a - b\alpha) = 1383514992730880 + 788159310461352\alpha + 222288412881565\alpha^2$. In $\mathbb{F}_{307^3}$, $r_0 = 191 + 17\alpha + 304\alpha^2$ has $r_0^2\gamma = 1$. One Newton step modulo $307^2$ gives a $\delta$ that is not yet exact. The second, modulo $307^4 = 8882874001$, gives $\delta = -36380984 - 8069491\alpha - 1426166\alpha^2$, and $\delta^2 = \gamma$ in $\mathbb{Z}[\alpha]$.
- **The factor.** $y = \delta(31) = -1657080731 \equiv 9985 \pmod{45113}$. Then $6045^2 \equiv 9985^2 \pmod{45113}$ and $\gcd(6045 - 9985, 45113) = \gcd(3940, 45113) = 197$.

Of the $22$ dependencies, $11$ give a proper factor, $3$ give $\gcd = 1$ and $8$ give $\gcd = N$, close to the half that the heuristic predicts. The test file checks all these numbers.

## Correctness

Whatever the parameters, the output is $1$ or a proper factor of $N$: line L1 returns a gcd only when it is proper, the trial division returns a prime $p < N$ with $p \mid N$, and line L9 tests $1 < g < N$ for a divisor $g$ of $N$. For a subset $T$ that reaches line L9, $x^2 \equiv y^2 \pmod N$. The sign bit and the exponents of $P$ add to $0$ modulo $2$, so $\prod_T (a - bm)$ is a positive square $v^2$ with $v = \prod p^{e_p/2}$, and $x^2 \equiv f'(m)^2 v^2$. Line L8 accepts $\delta$ only if $\delta^2 = \gamma$ exactly, and $\varphi$ is a ring homomorphism, so $y^2 \equiv \varphi(\gamma) = f'(m)^2 \prod_T (a - bm) \pmod N$. Every loop is bounded, so the algorithm stops. The full proof is below.

Why some $T$ succeeds is a heuristic, in two parts. First, a product with even exponents at every $(p, r)$ and with all characters equal to $1$ is "probably" a square in $\mathbb{Z}[\alpha]$ after the factor $f'(\alpha)^2$. The pair columns make the ideal of the product a square, and the characters detect the remaining obstructions, which lie in small groups: the [unit group](/unit-group/), the [class group](/ideal-class-group/) and the quotient of the ring of integers by $\mathbb{Z}[\alpha]$ (Crandall and Pomerance, Section 6.2.4). Lemma 6.2.3 there shows that $f'(\alpha)$ times an algebraic integer lies in $\mathbb{Z}[\alpha]$. Second, if $N$ has at least two distinct prime factors, each congruence of squares splits $N$ with probability about $1/2$ or more.

## Complexity

- **Proved bound for fixed parameters.** The sieve does $O(A \ln \ln B + K)$ additions per line, and at most $2A + 1$ candidates per line each cost $O(Kn)$ for trial division. So the $Y$ lines cost $O(YAKn)$ word operations. The elimination of a $K' \times K$ matrix over $\mathbb{F}_2$ with $K' = K + E$ costs $O(K^3)$ bit operations. Each dependency costs a product tree and $O(\log L)$ Newton steps in $\mathbb{Z}[\alpha]$, $O(d^2L^2)$ bit operations with schoolbook arithmetic, where $L$ is the largest bit length of a coefficient of $\gamma$. $L$ grows about linearly with the number of relations in $T$.
- **Heuristic bound.** Crandall and Pomerance (Section 6.2.3) model the values $F(a, b)(a - bm)$ as random integers below $X = 2(d + 1)N^{2/d}M^{d+1}$ for $|a|, |b| \le M$. By Pomerance's theorem on random squares, $L(X)^{\sqrt 2 + o(1)}$ pairs suffice, with $L(X) = \exp(\sqrt{\ln X \ln \ln X})$. With $d \sim (3 \ln N/\ln \ln N)^{1/3}$ and $B = M = L_N[1/3, (8/9)^{1/3}]$ this gives the total time $\exp\big(((64/9)^{1/3} + o(1))(\ln N)^{1/3}(\ln \ln N)^{2/3}\big)$, with $(64/9)^{1/3} \approx 1.923$. This is a heuristic: the values are not random, and the analysis assumes that the obstructions are as small as stated.
- **Fixed degree.** For fixed $d$ the same model gives $L(N)^{\sqrt{4/d} + o(1)}$, which is worse than the $L(N)^{1 + o(1)}$ of the quadratic sieve for $d = 3$ and better only for $d \ge 5$. So the toy implementation, with $d = 3$, is not asymptotically faster than the quadratic sieve. In Python it factors products of two random $26$ bit primes in about $2$ seconds on average.
- **Space.** $O(K^2)$ bits for the matrix, $O(A)$ for one sieve line, and $O(dL)$ bits for the square root.

## Properties

- **Two smooth sides.** Each relation needs two numbers of size about $N^{1/d}$ times a power of the sieve region to be smooth, instead of one number of size about $\sqrt N$. For large $N$ that is a much better bet.
- **Exact arithmetic.** The square root step works with large exact elements of $\mathbb{Z}[\alpha]$. No floating point is used.
- **Deterministic.** For fixed parameters the output is fixed.
- **Independent of the size of the factors.** Like the quadratic sieve, the method does not find small factors faster. Remove them first.
- **Parallel sieving.** Different lines $b$, or different special primes in a lattice sieve, are independent.

## Variants and improvements

- **The special number field sieve.** If $N = r^e \pm s$ for small $r$ and $s$, a polynomial with tiny coefficients exists and the constant drops to $(32/9)^{1/3}$; see the [special number field sieve](/special-number-field-sieve/).
- **Better polynomials.** Nonmonic polynomials and two nonlinear polynomials allow smaller coefficients. Practical polynomial selection searches for polynomials with small values and many roots modulo small primes. This needs a small change on the algebraic side, the leading coefficient times $F(a, b)$.
- **Lattice sieving.** Pollard's lattice sieve fixes a "special" prime ideal $\mathfrak q$ of medium size and sieves only the pairs $(a, b)$ whose algebraic side it divides. Large implementations use it in place of the line sieve.
- **Large primes.** Keep relations with one to three primes slightly above $B$ on each side and combine them later, as in the [relation collection](/relation-collection/) of the quadratic sieve.
- **Sparse linear algebra.** The matrix is huge and sparse; filtering removes singletons and merges, then [block Lanczos](/block-lanczos-algorithm/) or [block Wiedemann](/block-wiedemann-algorithm/) finds the dependencies.
- **Square roots without large numbers.** Couveignes's method for odd degree uses several inert primes and the Chinese remainder theorem. Peter Montgomery's method, refined by Phong Nguyen in 1998, divides the ideal of the product step by step by ideals of small norm found by lattice reduction. Both avoid the huge $\gamma$.
- **Discrete logarithms.** The same machinery solves discrete logarithms in prime fields; see the [number field sieve for discrete logarithms](/number-field-sieve-discrete-logarithm/).

## When to use it

GNFS is the method of choice for integers above roughly 100 to 120 decimal digits with no small factor and no special form, such as RSA moduli. Below that, the [multiple polynomial quadratic sieve](/multiple-polynomial-quadratic-sieve/) is simpler and faster. If $N$ might have a factor of up to about 40 to 60 digits, run [ECM](/elliptic-curve-factorization/) first. For numbers of a special form, use the special number field sieve. The page implementation is for study only.

## Pitfalls

- **Forgetting the characters.** For $N = 1000036000099$ with $B = 933$ and $30$ characters, all $15$ tested dependencies give squares. With no characters and no sign of the norm in the vectors, only $3$ of $15$ do. The other products have square ideals but are not squares, so line L8 fails on them.
- **Forgetting $f'(\alpha)^2$.** A square root of $\prod (a - b\alpha)$ may lie in the ring of integers but not in $\mathbb{Z}[\alpha]$. Multiplying by $f'(\alpha)^2$ puts it in $\mathbb{Z}[\alpha]$, and then $x$ must include $f'(m)$ too.
- **Mixing up the roots.** For $p \nmid b$, the exponent of $p$ in $F(a, b)$ belongs to the pair $(p, r)$ with $r \equiv ab^{-1} \pmod p$, not to $p$ as a whole. If $p \mid b$ and $p \mid F(a, b)$, then $p \mid a^d$, which $\gcd(a, b) = 1$ excludes.
- **A reducible $f$.** If $f$ is reducible over $\mathbb{Q}$, no inert prime exists and the square root method of line L8 cannot work. A factor $g$ of $f$ with $g(m)$ a proper divisor of $N$ would split $N$ at once.
- **A precision limit that is too low.** The coefficients of $\delta$ can be larger than those of $\gamma$. The implementation checks $\delta^2 = \gamma$ after each lift and gives up at a size bound, so a too small bound only loses a dependency, never gives a wrong factor.
- **A bad default.** In the toy version a bound $B$ that is too small makes relations rare, and a sieve width $A$ much larger than $B$ only adds large values. Measure before tuning.

## Implementations

## History

John Pollard proposed the method in 1988, in a letter about factoring numbers close to a cube with cubic integers (the paper appeared in the 1993 volume). Arjen Lenstra, Hendrik Lenstra, Mark Manasse and Pollard developed it into the number field sieve for numbers of special form, presented at STOC 1990, and used it to factor the ninth Fermat number $2^{512} + 1$ in 1990. Joe Buhler, Hendrik Lenstra and Carl Pomerance then extended it to general integers, and Leonard Adleman proposed the quadratic characters for the obstructions. The 1993 volume *The development of the number field sieve*, edited by Arjen and Hendrik Lenstra, collects these papers. GNFS overtook the quadratic sieve in the mid 1990s, with RSA-130 in 1996. Since then it has set every record for general integers, including RSA-768 in 2009, RSA-240 in 2019 and RSA-250 in 2020, the last two with the CADO-NFS software.

## References
