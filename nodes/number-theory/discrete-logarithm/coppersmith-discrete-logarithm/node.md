---
tag: TEVZ61
kind: algorithm
slug: coppersmith-discrete-logarithm
name: Coppersmith's algorithm for discrete logarithms in GF(2^n)
aliases:
- Coppersmith index calculus
- Coppersmith's method
- Coppersmith's algorithm for GF(2^n)
area: number-theory/discrete-logarithm
level: research
summary: Index-calculus method for characteristic-2 fields with L(1/3) complexity.
solves: [finite-field-discrete-logarithm-problem, discrete-logarithm-problem]
model: word-ram
complexity:
  vars:
    n: the degree of the field F_(2^n) over F_2
    q: the field size 2^n
    r: the order of g, a divisor of 2^n - 1
    t: the size of the factor base, the number of irreducible polynomials of degree at most b
    b: the degree bound of the factor base, about n^(1/3) (ln n)^(2/3)
  time:
    heuristic: exp(((32/9)^(1/3) + o(1)) (ln q)^(1/3) (ln ln q)^(2/3))
  space:
    extra: O(t^2 + t n)
  bit_operations:
    heuristic: exp(((32/9)^(1/3) + o(1)) (ln q)^(1/3) (ln ln q)^(2/3))
properties:
  deterministic: false
  recursive: false
prereqs: [index-calculus, finite-field-discrete-logarithm-problem, gf2-polynomial-arithmetic, irreducible-polynomial]
see_also: [function-field-sieve, number-field-sieve-discrete-logarithm, quasi-polynomial-discrete-logarithm, relation-collection, structured-gaussian-elimination, polynomial-factorization-over-finite-fields, smooth-number, primitive-polynomial]
sources:
  - paper: doi:10.1109/TIT.1984.1056941
    title: Don Coppersmith, Fast evaluation of logarithms in fields of characteristic two, IEEE Transactions on Information Theory 30(4), 1984
    locator: pages 587 to 594 (the relations from C(x) = A(x) x^l + B(x) and C(x)^(2^k), and Section VII on the descent of the individual logarithms)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 15, Section 15.5.4 (Coppersmith's algorithm, equation (15.9), Exercise 15.5.18, Examples 15.5.19 and 15.5.20, Conjecture 15.5.21 and the heuristic derivation of the constant)
  - paper: doi:10.1137/0605029
    title: Ian F. Blake, Ryoh Fuji-Hara, Ronald C. Mullin and Scott A. Vanstone, Computing logarithms in finite fields of characteristic two, SIAM Journal on Algebraic and Discrete Methods 5(2), 1984
    locator: pages 276 to 285 (the systematic equations A(x)^(2^i) = A(x^(2^i)) for fields with a sparse defining polynomial)
  - paper: doi:10.1007/3-540-39757-4_20
    title: Andrew M. Odlyzko, Discrete logarithms in finite fields and their cryptographic significance, Advances in Cryptology, EUROCRYPT 84, 1985
    locator: pages 224 to 314 (the analysis of Coppersmith's algorithm and its running time)
  - paper: doi:10.1007/3-540-48071-4_22
    title: Daniel M. Gordon and Kevin S. McCurley, Massively parallel computation of discrete logarithms, Advances in Cryptology, CRYPTO 92, 1993
    locator: pages 312 to 323 (sieving for the pairs (A, B) in Coppersmith's algorithm)
  - paper: doi:10.1007/3-540-45682-1_7
    title: Emmanuel Thomé, Computation of discrete logarithms in F_(2^607), Advances in Cryptology, ASIACRYPT 2001
    locator: pages 107 to 124 (a record computation with Coppersmith's algorithm, with the parameters of Galbraith's Example 15.5.19)
---

Coppersmith's algorithm computes discrete logarithms in the multiplicative group of the binary field $\mathbb{F}_{2^n}$ in heuristic time $L_q(1/3, (32/9)^{1/3})$ with $q = 2^n$. It was the first algorithm with a subexponential running time of the form $L(1/3)$. It is an [index calculus](/index-calculus/) method whose factor base is the set of low degree [irreducible polynomials](/irreducible-polynomial/). The new idea is to choose the field polynomial $x^n + f_1(x)$ with $f_1$ of small degree, and to test pairs of polynomials $C$ and $D \equiv C^{2^k}$ that both have degree about $n^{2/3}$, instead of one polynomial of degree about $n$. Squaring is additive in characteristic $2$, so $D$ is easy to write down and stays small.

## In plain words

In a binary field every element is a polynomial with bits as coefficients. As in index calculus, a polynomial that splits into small irreducible pieces gives an equation among the logarithms of those pieces.

Small polynomials split far more often than large ones, and Coppersmith made both sides of each equation small. He takes a polynomial $C$ of degree about $n^{2/3}$ and squares it $k$ times. In characteristic two the square of a sum is the sum of the squares, so the result is $C$ with every exponent of $x$ times $2^k$, and one reduction by the special field polynomial makes it short again. If both $C$ and this power split into small pieces, their logarithms differ by the factor $2^k$.

Linear algebra then gives the logarithms of the small pieces. The target is broken into medium pieces, and each one is pushed down by choosing $C$ divisible by it.

## The problem

**Input.** An irreducible polynomial $f = x^n + f_1(x)$ over $\mathbb{F}_2$ with $f_1$ of small degree, which defines $\mathbb{F}_{2^n} = \mathbb{F}_2[x]/(f)$; an element $g \ne 0$ of known order $r$; and an element $h \ne 0$. Field elements are polynomials of degree below $n$.

**Output.** The $x \in \{0, \dots, r - 1\}$ with $g^x = h$, or NONE if $h \notin \langle g \rangle$.

**Cost model.** The group is $\mathbb{F}_{2^n}^*$, cyclic of order $2^n - 1$, and the target lives in the subgroup $\langle g \rangle$ of order $r$. One multiplication in $\mathbb{F}_{2^n}$ with schoolbook polynomial arithmetic costs $O(n^2)$ bit operations, or $O(n^2 / w)$ word operations with $w$-bit words. The algorithm is not generic, since it factors the polynomial representatives, so the [generic lower bound](/shoup-generic-lower-bound/) does not apply. The running time $L_q(1/3, (32/9)^{1/3})$, with $L_q(\alpha, c) = \exp((c + o(1)) (\ln q)^\alpha (\ln \ln q)^{1 - \alpha})$, is heuristic: it assumes that $C$ and $D$ are smooth as often as independent random polynomials of the same degrees, and that the relations reach full rank soon after there are as many as unknowns (Galbraith, Conjecture 15.5.21). No proof of an $L(1/3)$ bound is known for this algorithm. Smoothness of a polynomial can be tested in polynomial time, so sieving is a constant factor saving and not needed for the bound.

## The algorithm

Fix a degree bound $b$ and let $S$ be the irreducible polynomials of degree at most $b$. Fix $k$ with $2^k \approx (n/b)^{1/2}$ and $l = \lceil n / 2^k \rceil$. For polynomials $A$ and $B$ of degree below $b$ put $C = A x^l + B$. Over $\mathbb{F}_2$ the map $a \mapsto a^2$ is additive and $a(x)^2 = a(x^2)$, so

$$C^{2^k} = A(x^{2^k}) \, x^{2^k l} + B(x^{2^k}) \equiv A(x^{2^k}) \, x^{2^k l - n} f_1(x) + B(x^{2^k}) = D \pmod f,$$

using $x^n \equiv f_1$. Both $C$ and $D$ have degree about $\sqrt{n b}$. If both factor over $S$, then $2^k L(C) = L(D)$ for the logarithm $L$ to any generator, which is a linear equation among the $L(s)$, $s \in S$ (Galbraith, equation (15.9)). These equations have right side $0$, so a few equations of the plain index calculus type, from powers $\gamma^m$ that factor over $S$, fix the scale. As in [index calculus](/index-calculus/), logarithms are taken to a generator $\gamma$ and computed modulo $\ell = \prod q^e$ over the prime powers $q^e \parallel 2^n - 1$ with $q \mid r$. The descent writes $y \gamma^m$ as a product over $S$ and a few medium polynomials $G$ of degree at most $2b$, and pushes each $G$ down by choosing $C = A x^l + B$ divisible by $G$.

```pseudo id=main
COPPERSMITH(g, h, r, f)             ▷ f = x^n + f_1 irreducible, g of order r; returns x with g^x = h, or NONE
L1  if h^r ≠ 1 then return NONE
L2  if h = 1 then return 0
L3  γ ← a generator of F*_(2^n) ; ℓ ← ∏ q^e over the prime powers q^e ∥ 2^n − 1 with q | r
L4  S ← the irreducible polynomials of degree ≤ b ; choose 2^k ≈ (n/b)^(1/2) and l = ⌈n/2^k⌉ ; R ← empty list
L5  for each pair (A, B) with A ≠ 0, gcd(A, B) = 1 and deg A, deg B < b do        ▷ Coppersmith relations
L6      C ← A·x^l + B ; D ← A(x^(2^k)) · x^(2^k l − n) · f_1 + B(x^(2^k))      ▷ D ≡ C^(2^k) (mod f)
L7      if f ∤ C and C = ∏ s^(c_s), D = ∏ s^(d_s) over s ∈ S then append (2^k c − d, 0) to R
L8  repeat                                                                     ▷ fix the scale
L9      m ← random in [0, 2^n − 2] ; if γ^m mod f = ∏ s^(e_s) over S then append (e, m) to R
L10     for each q^e ∥ ℓ, λ⁽q⁾ ← SOLVE(R, q, q^e)
L11 until every SOLVE succeeded ; λ ← the CRT combination of the λ⁽q⁾, so λ_s ≡ L(s) (mod ℓ)
L12 for y ∈ {g, h} do                                                          ▷ individual logarithms
L13     repeat m ← random ; z ← y·γ^m mod f, split as ∏ s^(d_s) over S times ∏ G_i^(a_i) with b < deg G_i ≤ 2b
L14         for each G_i: find A, B with C = A·x^l + B = G_i^a · ∏ s^(c_s), gcd(a, ℓ) = 1, f ∤ C, D = ∏ s^(d'_s); L(G_i) ← (2^(−k) Σ d'_s λ_s − Σ c_s λ_s) / a
L15     until z splits so and every G_i got a logarithm
L16     L(y) ← Σ d_s λ_s + Σ a_i L(G_i) − m mod ℓ
L17 c ← ℓ / r ; u ← L(g) / c                                                   ▷ u is a unit modulo r
L18 return (L(h) / c) · u^(−1) mod r
SOLVE(R, q, M)                                                                  ▷ solve all rows of R modulo M = q^e
L19 for each column j: find a row i ≥ j whose entry in column j is not divisible by q; if none, return FAIL
L20     swap rows i and j, scale row j by the inverse of its pivot modulo M, and clear column j in every other row
L21 return λ_j = the right side of row j, for every column j
```

Lines L1 and L2 decide membership and handle $h = 1$; $\mathbb{F}_{2^n}^*$ is cyclic, so $\langle g \rangle = \{y : y^r = 1\}$. Line L3 finds a generator from the factorization of $2^n - 1$. Lines L5 to L7 are the sieve: each pair whose $C$ and $D$ both factor over $S$ gives a row $\sum_s (2^k c_s - d_s) L(s) \equiv 0$. The condition $f \nmid C$ keeps $C$ nonzero in the field. Lines L8 to L11 add rows $\sum_s e_s L(s) \equiv m$ from smooth powers of $\gamma$ until Gauss-Jordan elimination modulo each prime power has a unit pivot in every column, and then combine the solutions with the [Chinese remainder theorem](/chinese-remainder-theorem/). Lines L12 to L16 are the descent. A random shift $z = y \gamma^m$ must split into factor base elements and medium polynomials $G_i$. For each $G_i$, line L14 takes $B \equiv A x^l \pmod{G_i}$ plus a small multiple of $G_i$, so that $G_i$ divides $C$, and waits until the rest of $C$ and the whole of $D$ factor over $S$. Then $2^k (a L(G_i) + \sum_s c_s L(s)) = L(D)$ gives $L(G_i)$, since $2$ is a unit modulo the odd number $\ell$. If some $G_i$ resists, line L15 draws a new $m$. Lines L17 and L18 convert the logarithms to base $\gamma$ into the logarithm to base $g$, as in [index calculus](/index-calculus/).

The implementation takes $b = \operatorname{round}(0.974 \, n^{1/3} (\ln n)^{2/3})$, clipped to $[1, n - 1]$, from the optimal constant $c = (2/(3 \ln 2))^{2/3}$ of Galbraith's analysis; it lets the caller choose $b$. It stops the sieve after $2|S|$ relations, calls SOLVE only once $R$ has $|S| + 10$ rows, and in line L14 tries every $A \ne 0$ of degree below $b$ with $B = (A x^l \bmod G_i) + T G_i$ for the four $T$ of degree at most $1$. All factoring is trial division by the members of $S$ and by the irreducible polynomials of degree up to $2b$.

## Example

This is Galbraith's Example 15.5.20. Take $f = x^{15} + x + 1$, so $n = 15$ and $f_1 = x + 1$, with $2^{15} - 1 = 7 \cdot 31 \cdot 151$. Let $g = x^{11} + x^7 + x^5 + x^2 + 1$, of prime order $r = 151$, and $h = x^{14} + x^{11} + x^{10} + x^9 + 1$. The polynomial $x$ is a generator, so $\gamma = x$, and $\ell = 151$.

With $b = 3$ the factor base is $S = (x, \; x + 1, \; x^2 + x + 1, \; x^3 + x + 1, \; x^3 + x^2 + 1)$, in this order. Next $2^k = 2$, since $(15/3)^{1/2} \approx 2.2$, and $l = 8$; $A$ and $B$ have degree at most $2$, and $D = A(x^2) \, x (x + 1) + B(x^2)$. Of the pairs with $\gcd(A, B) = 1$, four have $C$ and $D$ both smooth.

| $A$ | $B$ | $C = A x^8 + B$ | $D$ | row $2c - d$ |
|---|---|---|---|---|
| $1$ | $0$ | $x^8$ | $x (x + 1)$ | $(15, -1, 0, 0, 0)$ |
| $1$ | $1$ | $(x + 1)^8$ | $x^2 + x + 1$ | $(0, 16, -1, 0, 0)$ |
| $1$ | $x$ | $x (x + 1)(x^3 + x + 1)(x^3 + x^2 + 1)$ | $x$ | $(1, 2, 0, 2, 2)$ |
| $1$ | $x^2$ | $x^2 (x + 1)^2 (x^2 + x + 1)^2$ | $x (x^3 + x + 1)$ | $(3, 4, 4, -1, 0)$ |

These four homogeneous rows cannot fix the scale. Suppose line L9 draws $m = 1$: $\gamma^1 = x$ gives the row $(1, 0, 0, 0, 0)$ with right side $1$. Elimination modulo $151$ now gives $L(x) = 1$, $L(x + 1) = 15$, $L(x^2 + x + 1) = 16 \cdot 15 = 240 \equiv 89$, $L(x^3 + x + 1) = 3 + 4 \cdot 15 + 4 \cdot 89 = 419 \equiv 117$, and from $1 + 2 \cdot 15 + 2 \cdot 117 + 2 L(x^3 + x^2 + 1) \equiv 0$, $L(x^3 + x^2 + 1) \equiv 94$. These agree with Galbraith's full logarithms $15$, $240$, $1023$ and $15345$ reduced modulo $151$.

For the descent of $g$, take $m = 36$: $g x^{36} \bmod f = (x^2 + x + 1) \, G_1 G_2$ with $G_1 = x^4 + x^3 + x^2 + x + 1$ and $G_2 = x^5 + x^4 + x^3 + x + 1$, both of degree in $(3, 6]$. For $G_1$, $A = 1$ and $B = x^8 \bmod G_1 = x^3$ give $C = x^8 + x^3 = G_1 \cdot x^3 (x + 1)$ and $D = C^2 \bmod f = x^6 + x^2 + x = x (x^2 + x + 1)(x^3 + x^2 + 1)$. So $2 (L(G_1) + 3 + 15) \equiv 1 + 89 + 94$, and $L(G_1) \equiv 2^{-1} \cdot 33 - 18 \equiv 74$. For $G_2$, $A = 1$ and $B = x^3 + x^2 + x + 1$ give $C = G_2 (x^3 + x^2 + 1)$ and $D = (x + 1)(x^2 + x + 1)(x^3 + x + 1)$, so $L(G_2) \equiv 2^{-1} \cdot 70 - 94 \equiv 92$. Then $L(g) \equiv 89 + 74 + 92 - 36 \equiv 68$.

For $h$, take $m = 164$: $h x^{164} \bmod f = (x^2 + x + 1)^2 (x^3 + x + 1) \, G_1$, so $L(h) \equiv 2 \cdot 89 + 117 + 74 - 164 \equiv 54$. Here $c = 1$, and $x = 54 \cdot 68^{-1} \equiv 23 \pmod{151}$. Indeed $68 \cdot 23 = 1564 = 10 \cdot 151 + 54$, and $g^{23} = h$, as in Galbraith.

## Correctness

The equation $C^{2^k} \equiv D$ holds for every pair because squaring is a ring map in characteristic $2$ that fixes the coefficients $0$ and $1$, and $x^n \equiv f_1 \pmod f$. Every member of $S$ and every medium $G_i$ has degree below $n$, so it is a nonzero field element and has a logarithm. The test $f \nmid C$ makes $C$, and so $D \equiv C^{2^k}$, nonzero. Each row of $R$ is then a true congruence among the $L(s)$ modulo $2^n - 1$, and elimination with unit pivots keeps the true vector $(L(s) \bmod q^e)_s$ as the unique solution. The descent identity $L(y) = \sum d_s L(s) + \sum a_i L(G_i) - m$ is the logarithm of $z = y \gamma^m$, and the conversion of lines L17 and L18 is the one of index calculus. The full argument is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $q = 2^n$ and $b = c \, n^{1/3} (\ln n)^{2/3}$. Then $2^k \approx (n/b)^{1/2}$ and $l \approx (n b)^{1/2}$, so $C$ has degree about $l$ and $D$ about $2^k b$, both about $n^{2/3} (\ln n)^{1/3}$. If a polynomial of degree $d$ is $b$-smooth with probability $u^{-u(1 + o(1))}$, $u = d / b$, as for random polynomials, a pair is a relation after about $\exp(\tfrac{2}{3 \sqrt c} n^{1/3} (\ln n)^{2/3})$ trials. About $2^b / b$ relations are needed, so the sieve costs $\exp((c \ln 2 + \tfrac{2}{3\sqrt c}) n^{1/3} (\ln n)^{2/3})$, which is least at $c = (2 / (3 \ln 2))^{2/3}$ and gives $L_q(1/3, (32/9)^{1/3})$ in terms of $q$. Dense or sparse linear algebra on $t \approx 2^b / b$ unknowns costs $t^{2 + o(1)}$ operations modulo $\ell$, the same order. The descent handles polynomially many medium polynomials, each with far fewer trials, and has lower cost (Galbraith, Section 15.5.4). Every step works with polynomials of degree below $2n$, so each smoothness test is polynomial in $n$, and the bit cost has the same $L_q(1/3, (32/9)^{1/3})$ form.

All these figures are heuristic. The smoothness of $C$ and of $D$ is not independent, and $D$ has a special shape; the rank of the system is assumed and not proved. For comparison, the basic index calculus in $\mathbb{F}_{2^n}$, with random powers of $\gamma$ only, costs $L_q(1/2, c)$ for a constant $c$ (Galbraith, Section 15.5.3).

Space is the relation matrix: $O(t)$ rows of $t$ entries modulo $\ell$, plus the factor base of $t$ polynomials of degree at most $b$, which gives $O(t^2 + t n)$ words. The implementation stores dense rows; record computations use [structured Gaussian elimination](/structured-gaussian-elimination/) and the [Wiedemann](/wiedemann-algorithm/) or [Lanczos](/block-lanczos-algorithm/) methods on sparse rows.

## Properties

- **Randomized.** The scale rows and the descent use random exponents. The answer does not depend on the random choices, only the running time does.
- **Not generic.** The algorithm uses the polynomial representation of field elements and does not work in other groups of the same order.
- **Precomputation.** Lines L3 to L11 do not involve $h$, so the logarithms of $S$ serve every target in the same field.
- **Special field polynomial.** The bound needs $f = x^n + f_1$ with $\deg f_1$ small. Every binary field has such a polynomial in practice, and a change of basis to another representation is a polynomial time isomorphism, so this is no real restriction.
- **Characteristic $2$.** The trick needs the Frobenius map $a \mapsto a^p$ to be cheap and to keep degrees small, which is why it is stated for $p = 2$; the same idea works for other small fixed characteristics.

## Variants and improvements

- **Systematic equations.** Blake, Fuji-Hara, Mullin and Vanstone used $A^{2^i} = A(x^{2^i}) \equiv \tilde A \pmod f$ for factor base elements $A$; for $f = x^{127} + x + 1$, $A(x)^{128} \equiv A(x^2 + x)$, which is irreducible or a product of two polynomials of the same degree (Galbraith, Exercise 15.5.18). Coppersmith's algorithm extends these free relations to a whole family.
- **Sieving.** Gordon and McCurley sieved over the pairs $(A, B)$ instead of factoring each $C$ and $D$ separately, and ran the sieve on massively parallel machines.
- **Deeper descent.** Coppersmith's Section VII descends in several levels: a target is first split into pieces of degree about $n^{2/3}$, then each piece is pushed down through intermediate degrees until only factor base elements remain. The implementation stops at one level and redraws $m$ instead.
- **Function field sieve.** Coppersmith's method is a special case of the [function field sieve](/function-field-sieve/), which uses two factor bases and applies to $\mathbb{F}_{p^n}$ for small $p$ (Galbraith, Section 15.5.4).
- **Quasi-polynomial algorithms.** Since 2013, algorithms in the style of [Barbulescu, Gaudry, Joux and Thomé](/quasi-polynomial-discrete-logarithm/) solve the problem in small characteristic in heuristic quasi-polynomial time, $n^{O(\log n)}$, which beats every $L(1/3)$ method.

## When to use it

Coppersmith's method was the method of choice for binary fields from 1984 until the function field sieve and then the quasi-polynomial methods replaced it. It still shows clearly how a special field polynomial and the Frobenius map give an $L(1/3)$ algorithm, and it is a good first case of the descent step. For prime fields use the [number field sieve](/number-field-sieve-discrete-logarithm/). The result also explains why binary fields of small degree, once used for Diffie-Hellman, are no longer considered secure.

## Pitfalls

- **Forgetting the scale.** The rows of line L7 all have right side $0$, so they are satisfied by every multiple of the true logarithm vector. Without the rows of line L9, SOLVE can only return a vector up to a scalar, or fails. Line L9 adds rows with nonzero right sides.
- **A zero $C$ in the field.** If $f \mid C$, then $D \equiv 0$ and the relation is meaningless. Line L7 tests $f \nmid C$; line L14 does the same.
- **Factor base elements that are $0$ in the field.** For tiny $n$, a factor base with $b \ge n$ contains $f$ itself, whose logarithm does not exist. The implementation clips $b$ to $n - 1$.
- **Dividing by the multiplicity.** If $G_i^a$ exactly divides $C$, line L14 must divide by $a$ modulo $\ell$; when a prime $q \mid \ell$ divides $a$, the relation does not determine $L(G_i)$ modulo $q$. Line L14 skips such $C$.
- **Using $l$ with $2^k l < n$.** The reduction $x^{2^k l} = x^{2^k l - n} f_1$ needs $2^k l \ge n$. Line L4 takes $l = \lceil n / 2^k \rceil$.
- **Dropping the shift.** Line L16 must subtract $m$, since $z = y \gamma^m$ and not $y$ was split.

## Implementations

## History

Blake, Fuji-Hara, Mullin and Vanstone studied index calculus in $\mathbb{F}_{2^n}$ and found the systematic equations for $\mathbb{F}_{2^{127}}$, published in 1984. Coppersmith's paper of 1984 extended their idea to the pairs $C$ and $C^{2^k}$ and gave the first algorithm with a heuristic $L(1/3)$ running time. Its estimates showed that fields such as $\mathbb{F}_{2^{127}}$ gave little security. Odlyzko's survey of 1985 analyzed the method in detail. Gordon and McCurley added sieving and parallel machines in 1992, and Thomé computed discrete logarithms in $\mathbb{F}_{2^{607}}$ with it in 2001. Coppersmith's method was later seen as a special case of Adleman's function field sieve, and in 2013 and 2014 the work of Joux and of Barbulescu, Gaudry, Joux and Thomé made all $L(1/3)$ methods obsolete for small characteristic.

## References
