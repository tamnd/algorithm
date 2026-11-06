---
tag: AJXW0K
kind: algorithm
slug: function-field-sieve
name: Function field sieve
aliases:
- FFS
- Joux-Lercier function field sieve
- Function field sieve for discrete logarithms
area: number-theory/discrete-logarithm
level: research
summary: Sieving method for DLP in fields GF(p^n) with large n and small p.
solves: [finite-field-discrete-logarithm-problem, discrete-logarithm-problem]
model: word-ram
complexity:
  vars:
    p: the characteristic, a prime that is small compared with q
    n: the degree of the field F_(p^n) over F_p
    q: the field size p^n
    r: the order of g, a divisor of p^n - 1
    t: the total size of the two factor bases
    D: the degree bound of the factor bases
  time:
    heuristic: exp(((32/9)^(1/3) + o(1)) (ln q)^(1/3) (ln ln q)^(2/3))
  space:
    extra: O(t^2 + t n)
  bit_operations:
    heuristic: exp(((32/9)^(1/3) + o(1)) (ln q)^(1/3) (ln ln q)^(2/3))
properties:
  deterministic: false
  recursive: false
prereqs: [index-calculus, finite-field-discrete-logarithm-problem, irreducible-polynomial, polynomial-factorization-over-finite-fields]
see_also: [coppersmith-discrete-logarithm, number-field-sieve-discrete-logarithm, quasi-polynomial-discrete-logarithm, general-number-field-sieve, relation-collection, structured-gaussian-elimination, smooth-number, factor-base]
sources:
  - paper: doi:10.1007/11761679_16
    title: Antoine Joux and Reynald Lercier, The function field sieve in the medium prime case, Advances in Cryptology, EUROCRYPT 2006
    locator: pages 254 to 270 (the construction with two polynomials f1 and f2 such that x - f2(f1(x)) has an irreducible factor of degree n, and the analysis for p up to L(1/3))
  - paper: doi:10.1007/3-540-45455-1_34
    title: Antoine Joux and Reynald Lercier, The function field sieve is quite special, Algorithmic Number Theory, ANTS-V, 2002
    locator: pages 431 to 445 (a simplified function field sieve and its practical use in small characteristic)
  - paper: doi:10.1007/3-540-58691-1_48
    title: Leonard M. Adleman, The function field sieve, Algorithmic Number Theory, ANTS-I, 1994
    locator: pages 108 to 121 (the first function field sieve, with a curve over F_p and its function field)
  - paper: doi:10.1006/inco.1998.2761
    title: Leonard M. Adleman and Ming-Deh A. Huang, Function field sieve method for discrete logarithms over finite fields, Information and Computation 151(1-2), 1999
    locator: pages 5 to 16 (the improved heuristic L(1/3) analysis for small characteristic)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 15, Sections 15.5.4 and 15.5.5 (Coppersmith's method as a special case of the function field sieve; the Joux-Lercier algorithm with deg F1 = deg F2 = ceil(n^(1/2)), the maps psi1, psi2, phi1, phi2 of Exercise 15.5.23, the special-q descent, and the heuristic complexity between L(1/3, 3^(1/3)) and L(1/3, (32/9)^(1/3)))
---

The function field sieve computes discrete logarithms in the multiplicative group of a finite field $\mathbb{F}_{p^n}$ whose characteristic $p$ is small compared with the field size $q = p^n$. Its heuristic running time is $L_q(1/3, c)$ with $c$ at most $(32/9)^{1/3}$. It is an [index calculus](/index-calculus/) method with two factor bases of low degree [irreducible polynomials](/irreducible-polynomial/), one on each side of a commutative diagram of polynomial rings. Each candidate relation is a pair of polynomials of degree about $n^{2/3}$ that map to the same field element, so both are small and both are often smooth. This page uses the simple form of Joux and Lercier, in which both sides are polynomial rings and the field polynomial divides $F_2(F_1(t)) - t$.

## In plain words

In index calculus a relation is a field element whose polynomial splits into small irreducible pieces. A random element has degree about $n$ and rarely splits.

The function field sieve takes two ways to reach the same field. On one side the variable is $x$, on the other side it is $y$, and the field is reached by $x \mapsto t$ and $y \mapsto F_1(t)$. The two maps agree because the field polynomial divides $F_2(F_1(t)) - t$. A small expression $A(x) + B(x) y$ becomes a polynomial in $x$ on one side and a polynomial in $y$ on the other side, both of moderate degree. If both split, their logarithms are equal, and this gives one linear equation among the logarithms of the small pieces.

Linear algebra gives those logarithms. The target is then broken into medium pieces, and each piece is pushed down with expressions that it divides.

## The problem

**Input.** A prime $p$; monic polynomials $F_1$ and $F_2$ over $\mathbb{F}_p$; a monic irreducible polynomial $f$ of degree $n$ that divides $F_2(F_1(t)) - t$, which defines $\mathbb{F}_{p^n} = \mathbb{F}_p[t]/(f)$; an element $g \ne 0$ of known order $r$; and an element $h \ne 0$. Field elements are polynomials in $t$ of degree below $n$.

**Output.** The $x \in \{0, \dots, r - 1\}$ with $g^x = h$, or NONE if $h \notin \langle g \rangle$.

**Cost model.** The group is $\mathbb{F}_{p^n}^*$, cyclic of order $p^n - 1$, and the target lives in the subgroup $\langle g \rangle$ of order $r$. One multiplication in $\mathbb{F}_{p^n}$ with schoolbook arithmetic costs $O(n^2)$ operations in $\mathbb{F}_p$, that is $O(n^2 (\log p)^2)$ bit operations. The algorithm is not generic, since it factors polynomial representatives, so the [generic lower bound](/shoup-generic-lower-bound/) does not apply. With $L_q(\alpha, c) = \exp((c + o(1)) (\ln q)^\alpha (\ln \ln q)^{1 - \alpha})$, the running time $L_q(1/3, c)$, with $c$ between $3^{1/3}$ and $(32/9)^{1/3}$ when $p \le L_q(1/3, (4/9)^{1/3})$, is heuristic (Galbraith, Section 15.5.5). It assumes that the two sides of a candidate are smooth as often as independent random polynomials of the same degrees, and that the relation matrix reaches full rank soon after it has as many rows as unknowns. No proof of an $L(1/3)$ bound is known for this algorithm.

## The algorithm

Let $x$ and $y$ be two variables and $K = \mathbb{F}_p[t]/(f)$. The two maps $\varphi_1 : \mathbb{F}_p[x] \to K$, $x \mapsto t$, and $\varphi_2 : \mathbb{F}_p[y] \to K$, $y \mapsto F_1(t)$, are ring maps. For $G = A(x) + B(x) \, y$ put

$$\psi_1(G) = A(x) + B(x) F_1(x), \qquad \psi_2(G) = A(F_2(y)) + B(F_2(y)) \, y .$$

Since $f$ divides $F_2(F_1(t)) - t$, we have $F_2(F_1(t)) \equiv t$ in $K$, and so $\varphi_1(\psi_1(G)) = \varphi_2(\psi_2(G))$. Fix a degree bound $D$, let $S_1$ be the monic irreducibles in $x$ of degree at most $D$, and let $S_2$ be the monic irreducibles in $y$ of degree at most $D$ whose image $s(F_1(t))$ is nonzero. Write $L$ for the logarithm to a generator $\gamma$ of $K^*$. If $\psi_1(G) = c_1 \prod s^{a_s}$ over $S_1$ and $\psi_2(G) = c_2 \prod s^{b_s}$ over $S_2$, with constants $c_1, c_2 \in \mathbb{F}_p^*$, then

$$L(c_1) + \sum_{s \in S_1} a_s L(\varphi_1 s) = L(c_2) + \sum_{s \in S_2} b_s L(\varphi_2 s),$$

a linear equation among the $t = |S_1| + |S_2|$ unknowns. The logarithms of constants are known, since $\omega = \gamma^{(p^n - 1)/(p - 1)}$ generates $\mathbb{F}_p^*$ and $L(\omega^i) = i (p^n - 1)/(p - 1)$. As in [index calculus](/index-calculus/), the logarithms are computed modulo $\ell = \prod q^e$ over the prime powers $q^e \parallel p^n - 1$ with $q \mid r$.

```pseudo id=main
FFS(g, h, r, p, F_1, F_2, f)        ▷ f irreducible of degree n, f | F_2(F_1(t)) − t, g of order r; returns x with g^x = h, or NONE
L1  if h^r ≠ 1 then return NONE
L2  if h = 1 then return 0
L3  γ ← a generator of F*_(p^n) ; ℓ ← ∏ q^e over the prime powers q^e ∥ p^n − 1 with q | r
L4  S_1 ← monic irreducibles in x of degree ≤ D ; S_2 ← monic irreducibles in y of degree ≤ D with f ∤ s(F_1) ; R ← empty list
L5  for each pair (A, B) with B monic, deg A ≤ e, deg B ≤ e and gcd(A, B) = 1 do         ▷ relations
L6      ψ_1 ← A(x) + B(x)·F_1(x) ; ψ_2 ← A(F_2(y)) + B(F_2(y))·y
L7      if f ∤ ψ_1, ψ_1 = c_1 ∏ s^(a_s) over S_1 and ψ_2 = c_2 ∏ s^(b_s) over S_2 then append (a, −b ; L(c_2) − L(c_1)) to R
L8  repeat                                                                              ▷ fix the scale
L9      m ← random in [0, p^n − 2] ; j ← random in S_2 or none ; z ← γ^m, times s_j(F_1(t)) if j is not none
L10     if z = c ∏ s^(a_s) over S_1 then append (a, −1 in column j ; m − L(c)) to R
L11 until SOLVE(R, q, q^e) succeeds for every q^e ∥ ℓ ; λ ← the CRT combination, so λ_s ≡ L(s) (mod ℓ)
L12 for y ∈ {g, h} do                                                                   ▷ individual logarithms
L13     repeat m ← random ; z ← y·γ^m mod f, split as c ∏ s^(d_s) over S_1 times ∏ G_i^(u_i) with D < deg G_i ≤ 2D
L14         for each G_i: find G = A + B·y with G_i^a ∥ ψ_1(G), gcd(a, ℓ) = 1, f ∤ ψ_1(G), and ψ_1(G) / G_i^a, ψ_2(G) smooth; L(G_i) ← (L(ψ_2) − L(ψ_1 / G_i^a)) / a
L15     until z splits so and every G_i got a logarithm
L16     L(y) ← L(c) + Σ d_s λ_s + Σ u_i L(G_i) − m mod ℓ
L17 c ← ℓ / r ; u ← L(g) / c                                                            ▷ u is a unit modulo r
L18 return (L(h) / c) · u^(−1) mod r
SOLVE(R, q, M)                                                                           ▷ solve all rows of R modulo M = q^e
L19 for each column j: find a row i ≥ j whose entry in column j is not divisible by q; if none, return FAIL
L20     swap rows i and j, scale row j by the inverse of its pivot modulo M, and clear column j in every other row
L21 return λ_j = the right side of row j, for every column j
```

Lines L1 and L2 decide membership and handle $h = 1$; $K^*$ is cyclic, so $\langle g \rangle = \{y : y^r = 1\}$. Line L3 finds a generator from the factorization of $p^n - 1$. Line L4 builds the two factor bases. A polynomial in $y$ whose image is $0$ has no logarithm, so it is left out of $S_2$. Lines L5 to L7 are the sieve. The test $\gcd(A, B) = 1$ removes multiples of earlier pairs, and the test $f \nmid \psi_1$ keeps the common image nonzero. Lines L8 to L11 add rows from smooth elements $\gamma^m$ or $\gamma^m s_j(F_1(t))$. These rows tie the unknowns to $\gamma$ and remove the parasitic solutions that the homogeneous rows of line L7 allow (Galbraith, Section 15.5.5), and they are added until elimination modulo each prime power has a unit pivot in every column. Lines L12 to L16 are the descent. A shift $z = y \gamma^m$ must split into members of $S_1$ and medium polynomials $G_i$. For a medium $G_i$, line L14 takes $A \equiv -B F_1 \pmod{G_i}$ plus a small multiple of $G_i$, so that $G_i$ divides $\psi_1(G)$, and waits until the rest of both sides factors over the bases. Lines L17 and L18 convert the logarithms to base $\gamma$ into the logarithm to base $g$, as in [index calculus](/index-calculus/).

The implementation takes $D = 4, 3, 2$ for $p = 2, 3, 5$ and $D = 1$ for larger $p$, clipped to $[1, n - 1]$, and lets the caller choose $D$. The sieve degree $e$ is the least value with $p^{2e + 1} \ge 8t$, and the sieve stops after $2t$ relations. SOLVE runs only once $R$ has $t + 10$ rows. In line L14 it tries every monic $B$ of degree at most $e$ with $A = -(B F_1 \bmod G_i) + T G_i$ for the $p^2$ polynomials $T$ of degree at most $1$. All factoring is trial division by the factor base and by the irreducibles of degree up to $2D$. A helper `ffs_field(p, n)` finds $F_1$ of degree $\lceil n^{1/2} \rceil$ and $F_2$ of degree about $n / \deg F_1$ such that $F_2(F_1(t)) - t$ has exactly one irreducible factor of degree $n$.

## Example

Take $p = 3$, $F_1 = t^2$ and $F_2 = t^2 + 2$. Then $F_2(F_1(t)) - t = t^4 - t + 2 = t^4 + 2t + 2$, which is irreducible over $\mathbb{F}_3$, so $f = t^4 + 2t + 2$ and $K = \mathbb{F}_{81}$. The element $t$ generates $K^*$, so $\gamma = t$. Let $g = t^{16} = t^3 + 2t + 2$, of prime order $r = 5$, and $h = 2t^2 + t + 2$. Then $\ell = 5$. The constant $2 = t^{40}$ has $L(2) = 40 \equiv 0 \pmod 5$, so the constants drop out.

With $D = 1$, the factor bases are $S_1 = (x, x + 1, x + 2)$ and $S_2 = (y, y + 1, y + 2)$, whose images in $K$ are $t, t + 1, t + 2$ and $t^2, t^2 + 1, t^2 + 2$. Write $X_0, X_1, X_2$ and $Y_0, Y_1, Y_2$ for their logarithms modulo $5$. With $\deg A \le 1$ and $\deg B \le 1$, four pairs give relations; all have $B = 1$.

| $G$ | $\psi_1(G)$ | $\psi_2(G)$ | row |
|---|---|---|---|
| $y$ | $x^2$ | $y$ | $2 X_0 - Y_0 = 0$ |
| $y + 2$ | $(x + 1)(x + 2)$ | $y + 2$ | $X_1 + X_2 - Y_2 = 0$ |
| $y + x + 1$ | $(x + 2)^2$ | $y (y + 1)$ | $2 X_2 - Y_0 - Y_1 = 0$ |
| $y + 2x + 1$ | $(x + 1)^2$ | $2 (y + 1)^2$ | $2 X_1 - 2 Y_1 = L(2) \equiv 0$ |

For example, $\psi_2(y + x + 1) = 1 + F_2(y) + y = y^2 + y$. These rows are homogeneous. Suppose line L9 draws $\gamma^1 = t$, $\gamma^4 = t + 1$ and $\gamma^{53} = t + 2$, each with $j$ = none. They give $X_0 = 1$, $X_1 = 4$ and $X_2 = 53 \equiv 3$. The relations then give $Y_0 = 2$, $Y_2 = 7 \equiv 2$ and $Y_1 = 6 - 2 = 4$, and the fourth row checks: $8 - 8 = 0$. These agree with the true logarithms $L(t^2) = 2$, $L(t^2 + 1) = 24$ and $L(t^2 + 2) = 57$ reduced modulo $5$.

For the descent of $g$, take $m = 1$: $g t = 2t^2 + 1 = 2 (t + 1)(t + 2)$, so $L(g) \equiv 0 + 4 + 3 - 1 = 6 \equiv 1$. For $h$, take $m = 0$: $h = 2 (t + 1)^2$, so $L(h) \equiv 2 \cdot 4 = 8 \equiv 3$. Here $c = \ell / r = 1$ and $u = 1$, so $x = 3$. Indeed $g^3 = t^{48} = h$. The test file checks this example with the implementation for five seeds.

## Correctness

The key identity is $\varphi_1(\psi_1(G)) = \varphi_2(\psi_2(G))$ for every $G = A(x) + B(x) y$: substituting $y = F_1(t)$ in $\psi_2(G)$ gives $A(F_2(F_1(t))) + B(F_2(F_1(t))) F_1(t)$, and $F_2(F_1(t)) \equiv t \pmod f$. Every member of $S_1$ and every medium $G_i$ has degree below $n$, so it is a nonzero field element. The members of $S_2$ have nonzero images by the choice in line L4. The test $f \nmid \psi_1$ makes the common image nonzero, so each row of $R$ is a true congruence modulo $p^n - 1$ among the logarithms. Elimination with unit pivots keeps the true vector as the unique solution modulo each $q^e$. The descent identity of line L16 is the logarithm of $z = y \gamma^m$, and the conversion of lines L17 and L18 is the one of index calculus. The full argument is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $d_1 = \deg F_1$ and $d_2 = \deg F_2$ with $d_1 d_2 \approx n$. For $\deg A, \deg B \le e$, the side $\psi_1$ has degree at most $e + d_1$ and the side $\psi_2$ has degree at most $(e + 1) d_2$. Joux and Lercier choose $d_1$ and $d_2$ so that the two degrees are balanced, and take $D$ and $e$ of size about $n^{1/3} (\ln n)^{2/3}$. Then both sides have degree about $n^{2/3} (\ln n)^{1/3}$, as in [Coppersmith's algorithm](/coppersmith-discrete-logarithm/), and the same smoothness estimate gives a heuristic cost of $L_q(1/3, (32/9)^{1/3})$ for the sieve when $p$ is fixed. The linear algebra on $t \approx 2 p^D / D$ unknowns costs $t^{2 + o(1)}$ operations modulo $\ell$, the same order. The descent, done in several levels, has lower cost. When $p$ grows up to $L_q(1/3, (4/9)^{1/3})$ the constant moves into the range from $3^{1/3}$ to $(32/9)^{1/3}$ (Galbraith, Section 15.5.5). Each smoothness test is polynomial in $n$ and $\log p$, so the bit cost has the same form.

All these figures are heuristic: the two sides of a candidate are not independent random polynomials, and the rank of the system is assumed and not proved. For comparison, the basic index calculus in $\mathbb{F}_{p^n}$ with random powers of $\gamma$ only costs $L_q(1/2, c)$ for a constant $c$.

Space is the relation matrix, $O(t)$ rows of $t$ entries modulo $\ell$, plus the two factor bases of $t$ polynomials of degree at most $D$, which gives $O(t^2 + t n)$ words. The implementation stores dense rows; large computations use [structured Gaussian elimination](/structured-gaussian-elimination/) and the [Wiedemann](/wiedemann-algorithm/) or [Lanczos](/block-lanczos-algorithm/) methods on sparse rows. The implementation also does $O(q^{1/2})$ integer divisions to factor $p^n - 1$ by trial division, and a linear search for $\gamma$; real implementations use known factorizations.

## Properties

- **Randomized.** The scale rows and the descent use random exponents. The answer does not depend on the random choices, only the running time does.
- **Not generic.** The algorithm uses the polynomial representation of field elements and does not work in other groups of the same order.
- **Precomputation.** Lines L3 to L11 do not involve $h$, so the logarithms of the factor bases serve every target in the same field.
- **Free choice of representation.** Any monic $F_1$ and $F_2$ work as long as $F_2(F_1(t)) - t$ has an irreducible factor of degree $n$. Every representation of $\mathbb{F}_{p^n}$ is isomorphic to every other one in polynomial time, so the algorithm can change to this representation first.
- **Two sides.** The relation is between two different polynomial rings, so each factor base appears in only one side, and the unknowns are the logarithms of both bases.

## Variants and improvements

- **Adleman's function field sieve.** The first function field sieve, by Adleman in 1994, used a plane curve $H(x, y) = 0$ over $\mathbb{F}_p$, and its second factor base consisted of places of the function field of the curve. Adleman and Huang improved the choice of the curve. The Joux-Lercier form replaces the curve by $y = F_1(x)$ and $x = F_2(y)$, so both sides are polynomial rings and no function field arithmetic is needed.
- **Coppersmith's algorithm.** For $p = 2$, [Coppersmith's algorithm](/coppersmith-discrete-logarithm/) compares $C$ with $C^{2^k}$, which plays the role of the second side; Galbraith describes it as a special case of the function field sieve.
- **Medium prime case.** Joux and Lercier also analyzed fields with $p$ up to $L_q(1/3)$, where both $d_1$ and $d_2$ are small and the sieve is over linear $A$ and $B$.
- **Number field sieve.** For large $p$, the [number field sieve](/number-field-sieve-discrete-logarithm/) replaces the polynomial rings over $\mathbb{F}_p$ by rings of integers of number fields.
- **Quasi-polynomial algorithms.** Since 2013, [quasi-polynomial algorithms](/quasi-polynomial-discrete-logarithm/) solve the problem in small characteristic in heuristic time $n^{O(\log n)}$ for fixed $p$, which beats every $L(1/3)$ method; their descent steps still use relations of this kind.

## When to use it

The function field sieve was the method of choice for fields of small characteristic from the late 1990s until 2013. For fixed $p$ and large $n$, the quasi-polynomial methods now replace it. It remains the standard method in the medium range between small characteristic and the range of the number field sieve, and it is the natural setting to learn the two-sided relations, the special-q descent and the conversion of logarithms. For prime fields use the [number field sieve](/number-field-sieve-discrete-logarithm/).

## Pitfalls

- **Forgetting the constants.** The two sides of a relation have leading coefficients $c_1$ and $c_2$ in $\mathbb{F}_p^*$, and $L(c)$ is not $0$ when $p > 2$. Line L7 puts $L(c_2) - L(c_1)$ on the right side, and line L16 adds $L(c)$.
- **A zero common image.** If $f \mid \psi_1(G)$, the two sides map to $0$ and the relation is meaningless. Line L7 tests $f \nmid \psi_1$; line L14 does the same.
- **Factor base elements with image $0$.** A polynomial $s(y)$ with $f \mid s(F_1(t))$ has no logarithm. Line L4 leaves it out of $S_2$; including it makes the system inconsistent.
- **Mixing the two bases.** The polynomial $x + 1$ in $S_1$ and the polynomial $y + 1$ in $S_2$ are different unknowns, since their images are $t + 1$ and $F_1(t) + 1$. Line L7 puts them in different columns.
- **Forgetting the scale.** The rows of line L7 are all satisfied by every multiple of the true vector when the constants are trivial, as for $p = 2$. Lines L8 to L10 add rows with right sides from $\gamma^m$.
- **Dividing by the multiplicity.** If $G_i^a$ exactly divides $\psi_1(G)$, line L14 divides by $a$ modulo $\ell$, which needs $\gcd(a, \ell) = 1$.
- **Dropping the shift.** Line L16 must subtract $m$, since $z = y \gamma^m$ and not $y$ was split.

## Implementations

## History

Adleman introduced the function field sieve in 1994, as the analogue for small characteristic of the [number field sieve](/general-number-field-sieve/), with a heuristic $L(1/3)$ running time. Adleman and Huang refined it in 1999. Joux and Lercier simplified it in 2002 and, in 2006, gave the form with two polynomials $F_1$ and $F_2$ used here and extended the analysis to the medium prime case. Many record computations in fields of characteristic $2$ and $3$ used the function field sieve, until the work of Joux and of Barbulescu, Gaudry, Joux and Thomé in 2013 and 2014 gave quasi-polynomial algorithms for small characteristic.

## References
