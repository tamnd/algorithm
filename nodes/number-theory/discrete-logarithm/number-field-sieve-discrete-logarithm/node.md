---
tag: YRSSHK
kind: algorithm
slug: number-field-sieve-discrete-logarithm
name: Number field sieve for discrete logarithms
aliases:
- NFS for discrete logarithms
- NFS-DL
- Number field sieve for the DLP
area: number-theory/discrete-logarithm
level: research
summary: Index-calculus variant over prime fields with heuristic complexity L(1/3, c).
solves: [finite-field-discrete-logarithm-problem, discrete-logarithm-problem]
model: word-ram
complexity:
  vars:
    p: the prime modulus
    r: the order of g, a divisor of p - 1
    t: the total size of the two factor bases
    B: the smoothness bound of the factor bases
  time:
    heuristic: exp(((64/9)^(1/3) + o(1)) (ln p)^(1/3) (ln ln p)^(2/3))
  space:
    extra: O(t^2)
  bit_operations:
    heuristic: exp(((64/9)^(1/3) + o(1)) (ln p)^(1/3) (ln ln p)^(2/3))
properties:
  deterministic: false
  recursive: false
prereqs: [index-calculus, finite-field-discrete-logarithm-problem, general-number-field-sieve]
see_also: [special-number-field-sieve, function-field-sieve, coppersmith-discrete-logarithm, relation-collection, structured-gaussian-elimination, smooth-number, factor-base, pohlig-hellman]
sources:
  - paper: doi:10.1137/0406010
    title: Daniel M. Gordon, Discrete logarithms in GF(p) using the number field sieve, SIAM Journal on Discrete Mathematics 6(1), 1993
    locator: pages 124 to 138 (the first number field sieve for discrete logarithms in prime fields, with a heuristic L_p(1/3) running time)
  - paper: doi:10.1098/rsta.1993.0139
    title: Oliver Schirokauer, Discrete logarithms and local units, Philosophical Transactions of the Royal Society of London, Series A 345, 1993
    locator: pages 409 to 423 (the maps that handle units and class groups, and the heuristic L_p(1/3, (64/9)^(1/3)) running time)
  - paper: doi:10.1007/bf01840433
    title: Don Coppersmith, Andrew M. Odlyzko and Richard Schroeppel, Discrete logarithms in GF(p), Algorithmica 1, 1986
    locator: pages 1 to 15 (the Gaussian integer method, with relations between a + b i in Z[i] and a + b s modulo p, and its heuristic L_p(1/2, 1) running time)
  - paper: doi:10.1007/3-540-61581-4_66
    title: Oliver Schirokauer, Damian Weber and Thomas Denny, Discrete logarithms, the effectiveness of the index calculus method, Algorithmic Number Theory, ANTS-II, 1996
    locator: pages 337 to 361 (a practical number field sieve for discrete logarithms in prime fields, with experiments)
  - paper: doi:10.1016/j.jalgor.2004.11.004
    title: Oliver Schirokauer, Virtual logarithms, Journal of Algorithms 57(2), 2005
    locator: pages 140 to 147 (logarithms of prime ideals that are not principal, defined through the Schirokauer maps)
  - paper: doi:10.1007/11818175_19
    title: Antoine Joux, Reynald Lercier, Nigel Smart and Frederik Vercauteren, The number field sieve in the medium prime case, Advances in Cryptology, CRYPTO 2006
    locator: pages 326 to 344 (the number field sieve for F_(p^n) with p of medium size, and L(1/3) for all finite fields)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 15, Sections 15.5.2, 15.5.6 and 15.5.7 (the L_p(1/2, 1) sieve of Coppersmith, Odlyzko and Schroeppel, the number field sieve for the DLP with heuristic L_p(1/3, (64/9)^(1/3)), the special number field sieve with L_p(1/3, (32/9)^(1/3)), and L(1/3) for all finite fields)
---

The number field sieve for discrete logarithms computes logarithms in the multiplicative group of a prime field $\mathbb{F}_p$ in heuristic time $L_p(1/3, (64/9)^{1/3})$. It is the fastest known method for large prime fields and the reason why prime field Diffie-Hellman needs moduli of thousands of bits. Like the [general number field sieve](/general-number-field-sieve/) for factoring, it takes two polynomials with a common root modulo $p$ and finds pairs $(a, b)$ for which $a - b\alpha$ is smooth on both sides. Each pair gives one linear equation among the logarithms of the factor base elements. Linear algebra modulo the group order gives these logarithms, and a descent expresses the target in terms of them. This page describes the general method and gives a full implementation of the simplest case, with an imaginary quadratic field of class number $1$. This case is the Gaussian integer method of Coppersmith, Odlyzko and Schroeppel.

## In plain words

[Index calculus](/index-calculus/) in $\mathbb{F}_p$ needs many numbers below $p$ that split into small primes. A random number below $p$ rarely does, and this limits basic index calculus to $L_p(1/2)$.

The number field sieve finds two ways to reach $\mathbb{F}_p$ from smaller objects. One way is from ordinary integers, the other is from the integers of a number field, for example the Gaussian integers $a + b i$, where $i$ goes to a square root of $-1$ modulo $p$. A pair $(a, b)$ gives a small integer on one side and a small algebraic integer on the other side, and the two have the same image in $\mathbb{F}_p$, up to a known factor. If both split into small primes, the logarithms of the pieces satisfy one linear equation.

Many equations and linear algebra give the logarithms of the small primes. A descent then writes the target in terms of them.

## The problem

**Input.** A prime $p$, an element $g$ of $(\mathbb{Z}/p\mathbb{Z})^*$ of known order $r$, and an element $h$ of $(\mathbb{Z}/p\mathbb{Z})^*$.

**Output.** The $x \in \{0, \dots, r - 1\}$ with $g^x \equiv h \pmod p$, or NONE if $h \notin \langle g \rangle$.

**Cost model.** The group is $(\mathbb{Z}/p\mathbb{Z})^*$, cyclic of order $p - 1$, and the target lives in the subgroup $\langle g \rangle$ of order $r$. One multiplication modulo $p$ costs $O((\log p)^2)$ bit operations with schoolbook arithmetic. The algorithm is not generic, since it factors integers and algebraic integers, so the [generic lower bound](/shoup-generic-lower-bound/) does not apply. With $L_p(\alpha, c) = \exp((c + o(1)) (\ln p)^\alpha (\ln \ln p)^{1 - \alpha})$, the running time $L_p(1/3, (64/9)^{1/3})$ of the general method is heuristic (Galbraith, Section 15.5.6). It assumes that the values on the two sides are smooth as often as random integers of the same size, and that the relation matrix reaches full rank soon after it has as many rows as unknowns. No proof of an $L(1/3)$ bound is known. The quadratic version implemented here has heuristic cost $L_p(1/2, 1)$, as for the Gaussian integer method.

## The algorithm

**The general method.** Choose irreducible polynomials $f_1, f_2 \in \mathbb{Z}[x]$ with a common root $s$ modulo $p$, and let $\alpha_i$ be a root of $f_i$ in the number field $K_i = \mathbb{Q}(\alpha_i)$. Often $f_2$ is linear, so $K_2 = \mathbb{Q}$. The ring maps $\mathbb{Z}[\alpha_i] \to \mathbb{F}_p$, $\alpha_i \mapsto s$, send $a - b\alpha_1$ and $a - b\alpha_2$ to the same element $a - bs$. The factor bases are the prime ideals of small norm in the two rings. For coprime $(a, b)$, the norms of $a - b\alpha_i$ are about $\max(|a|, |b|)^{\deg f_i}$ times the coefficient size of $f_i$, and with good polynomials of degree about $(3 \ln p / \ln \ln p)^{1/3}$ both are $L_p(2/3)$ in size. If both ideals $(a - b\alpha_i)$ factor over the factor bases, the pair gives a relation. Ideals are not elements, so their logarithms are not defined directly. Schirokauer's maps, $\ell$-adic linear maps on the units, add a few columns to each row so that the unknowns become well defined "virtual logarithms" of the prime ideals modulo $\ell$. After linear algebra, the descent writes the target through a chain of smaller and smaller smooth values, with special-$q$ lattices on both sides.

**The quadratic case implemented here.** Take $f_1 = x^2 + a_1 x + a_0$ such that $\mathbb{Z}[\omega] = \mathbb{Z}[x]/(f_1)$ is the full ring of integers of an imaginary quadratic field with class number $1$. The nine discriminants $-3, -4, -7, -8, -11, -19, -43, -67, -163$ give such fields. Every ideal is principal, so it has a generator, and the unit group is finite, of order $2$, $4$ or $6$. Take $p$ that splits in this field, and write $p = c^2 + a_1 c d + a_0 d^2$ with $d \ge 1$, so that $f_2 = d x - c$ and $f_1$ have the common root $s = c / d$ modulo $p$. The map $\omega \mapsto s$ sends $a + b\omega$ to $a + bs$, and $d (a + bs) \equiv a d + b c \pmod p$. So if $a + b\omega = \varepsilon^k \prod \pi^{e_\pi}$ over generators $\pi$ of the prime ideals of norm at most $B$, and the integer $N = a d + b c$ equals $\pm \prod q^{e_q}$ over the primes $q \le B$, then

$$L(\pm 1) + \sum_q e_q L(q) = L(d) + k L(\varepsilon) + \sum_\pi e_\pi L(\pi),$$

where $L$ is the logarithm to a generator $\gamma$ of $(\mathbb{Z}/p\mathbb{Z})^*$ and $L(\pi)$ means the logarithm of the image of $\pi$. The unknowns are $L(-1)$, the $L(q)$, $L(\varepsilon)$, the $L(\pi)$ and $L(d)$. Both sides have size about $W p^{1/2}$ and $W^2$ for $|a|, b \le W$, which is why this case costs $L_p(1/2)$ and not $L_p(1/3)$. As in [index calculus](/index-calculus/), the logarithms are computed modulo $\ell = \prod q^e$ over the prime powers $q^e \parallel p - 1$ with $q \mid r$.

```pseudo id=main
NFS-DL(g, h, r, p)                  ▷ p prime, g of order r; returns x with g^x ≡ h (mod p), or NONE
L1  if h^r ≢ 1 (mod p) then return NONE
L2  if h = 1 then return 0
L3  γ ← a generator of (Z/pZ)* ; ℓ ← ∏ q^e over the prime powers q^e ∥ p − 1 with q | r
L4  choose f_1 = x^2 + a_1 x + a_0 and f_2 = d x − c with c^2 + a_1 c d + a_0 d^2 = p ; s ← c/d mod p ; P ← {−1} ∪ primes ≤ B ; Π ← {ε} ∪ generators of prime ideals of norm ≤ B ∪ {d} ; R ← empty list
L5  for each pair (a, b) with gcd(a, b) = 1, 1 ≤ b ≤ W and |a| ≤ W do      ▷ relations
L6      N ← a d + b c                                                   ▷ N ≡ d (a + b s) (mod p)
L7      if p ∤ N, N = ± ∏ q^(e_q) over P and a + b ω = ε^k ∏ π^(e_π) over Π then append (sign, e_q ; −k, −e_π, −1 ; 0) to R
L8  repeat                                                              ▷ fix the scale
L9      m ← random in [0, p − 2] ; j ← random column of Π or none ; z ← γ^m, times the image of column j if j is not none, as a residue in (−p/2, p/2)
L10     if z = ± ∏ q^(e_q) over P then append (sign, e_q ; −1 in column j ; m) to R
L11 until SOLVE(R, q, q^e) succeeds for every q^e ∥ ℓ ; λ ← the CRT combination, so λ ≡ L (mod ℓ) on every column
L12 for y ∈ {g, h} do                                                   ▷ individual logarithms
L13     repeat m ← random ; z ← y·γ^m as a residue in (−p/2, p/2), split as ± ∏ q^(d_q) over P times ∏ Q_i^(u_i) with B < Q_i ≤ B^2
L14         for each Q_i: find coprime (a, b) with Q_i | a d + b c, Q_i^k ∥ N, gcd(k, ℓ) = 1, N / Q_i^k smooth over P and a + b ω smooth over Π; L(Q_i) ← (L(d) + L(a + b ω) − L(N / Q_i^k)) / k
L15     until z splits so and every Q_i got a logarithm
L16     L(y) ← Σ d_q λ_q + Σ u_i L(Q_i) − m mod ℓ
L17 c ← ℓ / r ; u ← L(g) / c                                            ▷ u is a unit modulo r
L18 return (L(h) / c) · u^(−1) mod r
SOLVE(R, q, M)                                                           ▷ solve all rows of R modulo M = q^e
L19 for each column j: find a row i ≥ j whose entry in column j is not divisible by q; if none, return FAIL
L20     swap rows i and j, scale row j by the inverse of its pivot modulo M, and clear column j in every other row
L21 return λ_j = the right side of row j, for every column j
```

Lines L1 and L2 decide membership and handle $h = 1$; the group is cyclic, so $\langle g \rangle = \{y : y^r = 1\}$. Line L3 finds a generator from the factorization of $p - 1$. Line L4 picks the first of the nine fields in which $p$ splits and finds $c$ and $d$ by a search over $d$. The two factor bases are the rational primes up to $B$ with the sign $-1$, and one generator for each prime ideal of norm at most $B$ with the unit generator $\varepsilon$ and the constant $d$. Lines L5 to L7 are the sieve; the test $p \nmid N$ keeps the common image nonzero. Lines L8 to L11 add rows from smooth values $\gamma^m$ or $\gamma^m w_j$, where $w_j$ is the image of an algebraic column. These rows tie the unknowns to $\gamma$, which the homogeneous rows of line L7 cannot do. Lines L12 to L16 are the descent. A shift $z = y\gamma^m$ must split into primes up to $B$ and medium primes $Q_i$ up to $B^2$. For each $Q_i$, line L14 searches a reduced basis of the lattice of pairs with $Q_i \mid a d + b c$, so that the rest of $N$ is small. Lines L17 and L18 convert the logarithms to base $\gamma$ into the logarithm to base $g$, as in [index calculus](/index-calculus/).

The implementation takes $B = \operatorname{round}(3 \exp(\tfrac12 (\ln p \ln \ln p)^{1/2}))$, clipped to $[1, (p - 1)/2]$, and lets the caller choose $B$. Since $B < p/2$, every prime $q \le B$ is its own balanced residue, and $p - 1$ is the residue $-1$. The sieve uses $W = \max(10, 2t)$ and stops after $2t$ relations, and SOLVE runs once $R$ has $t + 10$ rows. Line L14 tries the combinations $i v_1 + k v_2$ with $|i|, |k| \le 4$ of a Lagrange-reduced basis $v_1, v_2$. The implementation raises an error for the 18 primes below $10^5$ that split in none of the nine fields, the least being $3167$; the general method would use another polynomial $f_1$.

## Example

Take $p = 37$. Since $37 = 6^2 + 1^2$, the search gives $f_1 = x^2 + 1$ and $f_2 = x - 6$, so $\mathbb{Z}[\omega] = \mathbb{Z}[i]$, $d = 1$, $c = 6$ and $s = 6$, with $6^2 = 36 \equiv -1$. The element $\gamma = 2$ generates $(\mathbb{Z}/37\mathbb{Z})^*$. Let $g = 2^4 = 16$, of order $r = 9$, so $\ell = 9$. The unit $i$ maps to $6$, of order $4$, and $-1$ has order $2$, so their logarithms are $0$ modulo $9$; also $L(d) = L(1) = 0$.

With $B = 5$, the rational primes are $2, 3, 5$ and the Gaussian primes are $1 + i$, $2 - i$ and $2 + i$, with images $7$, $33$ and $8$. Write $X_2, X_3, X_5$ and $P_1, P_2, P_3$ for their logarithms modulo $9$. These six pairs with $b = 1$ give relations:

| $(a, b)$ | $N = a + 6b$ | $a + bi$ | row modulo $9$ |
|---|---|---|---|
| $(-3, 1)$ | $3$ | $i (1 + i)(2 + i)$ | $X_3 = P_1 + P_3$ |
| $(-2, 1)$ | $2^2$ | $-(2 - i)$ | $2 X_2 = P_2$ |
| $(-1, 1)$ | $5$ | $i (1 + i)$ | $X_5 = P_1$ |
| $(0, 1)$ | $2 \cdot 3$ | $i$ | $X_2 + X_3 = 0$ |
| $(2, 1)$ | $2^3$ | $2 + i$ | $3 X_2 = P_3$ |
| $(3, 1)$ | $3^2$ | $(1 + i)(2 - i)$ | $2 X_3 = P_1 + P_2$ |

All six rows are homogeneous. Suppose line L9 draws $m = 1$ with $j$ = none: $\gamma^1 = 2$ gives $X_2 = 1$. Then $X_3 = -1 \equiv 8$, $P_2 = 2$, $P_3 = 3$, $P_1 = 8 - 3 = 5$ and $X_5 = 5$, and the last row checks: $16 \equiv 7 = 5 + 2$. These agree with the true logarithms $L(3) = 26$, $L(5) = 23$, $L(7) = 32$, $L(33) = 20$ and $L(8) = 3$ reduced modulo $9$.

For the descent, $g = 2^4$ gives $L(g) = 4 X_2 = 4$ directly. Let $h = 26$. With $m = 0$, the balanced residue is $26 - 37 = -11$, and $11$ is a medium prime. The pairs with $11 \mid a + 6b$ form the lattice with basis $(11, 0), (5, 1)$, which Lagrange reduction turns into $(1, -2), (4, 3)$. The pair $-(1, -2) = (-1, 2)$ gives $N = -1 + 12 = 11$ and $-1 + 2i = i (2 + i)$. So $L(11) = L(d) + L(i) + P_3 = 3$, and $L(h) = L(-1) + L(11) - 0 = 3$. Here $c = \ell / r = 1$ and $u = 4$, so $x = 3 \cdot 4^{-1} \equiv 3 \cdot 7 = 21 \equiv 3 \pmod 9$. Indeed $16^3 = 4096 = 110 \cdot 37 + 26$. The test file checks this example with the implementation for five seeds, and also $h = 33 = g^5$, whose residue $-4 = -2^2$ gives $L(h) = 2$ and $x = 2 \cdot 7 \equiv 5$.

## Correctness

The two ring maps $\mathbb{Z} \to \mathbb{F}_p$ and $\mathbb{Z}[\omega] \to \mathbb{F}_p$, $\omega \mapsto s$, are well defined because $s$ is a root of $f_1$ modulo $p$, and $d (a + bs) \equiv a d + b c$ because $d s \equiv c$. Every factor base element has a nonzero image: a rational prime $q \le B < p$ is not divisible by $p$, and a generator $\pi$ of norm at most $B$ has $\pi \bar\pi = N(\pi) \not\equiv 0$, so its image is nonzero. Each row of $R$ is then a true congruence modulo $p - 1$ among the logarithms, and elimination with unit pivots keeps the true vector as the unique solution modulo each $q^e$. The descent identity of line L16 is the logarithm of $z = y\gamma^m$, and the conversion of lines L17 and L18 is the one of index calculus. The full argument is in [the correctness proof](proofs/correctness.md).

## Complexity

For the general method, choose $f_2 = x - m$ with $m \approx p^{1/(k+1)}$ and $f_1$ of degree $k$ with coefficients about $m$, by the base-$m$ method as in factoring. With $k \approx (3 \ln p / \ln \ln p)^{1/3}$, sieve bound $B = L_p(1/3, \beta)$ and sieve region $|a|, |b| \le B$, both norms are $L_p(2/3)$, and the usual smoothness estimate balances the sieve and the linear algebra at $L_p(1/3, (64/9)^{1/3})$, the same constant as for factoring. The linear algebra on $t = L_p(1/3)$ unknowns modulo $\ell$ costs $t^{2 + o(1)}$ with sparse methods. The descent has lower cost per target. For primes of a special form, such as $p = 2^n \pm 1$, the [special number field sieve](/special-number-field-sieve/) has a smaller constant, $(32/9)^{1/3}$ (Galbraith, Section 15.5.6). All of these bounds are heuristic.

For the quadratic version, the rational side is about $W p^{1/2}$ and the algebraic side about $W^2$. With $B = L_p(1/2, 1/2)$ and $W$ of the same size, the expected cost is $L_p(1/2, 1)$, which matches the Gaussian integer method of Coppersmith, Odlyzko and Schroeppel and the sieve of Galbraith, Section 15.5.2. The implementation also uses $O(p^{1/2})$ integer divisions to factor $p - 1$ by trial division and to find $c$ and $d$, and a linear search for $\gamma$; real implementations use known factorizations.

Space is the relation matrix, $O(t)$ rows of $t$ entries modulo $\ell$, so $O(t^2)$ words with dense rows. Large computations use [structured Gaussian elimination](/structured-gaussian-elimination/) and the [Wiedemann](/wiedemann-algorithm/) or [Lanczos](/block-lanczos-algorithm/) methods on sparse rows with $O(\log p)$ entries each.

## Properties

- **Randomized.** The scale rows and the descent use random exponents. The answer does not depend on the random choices, only the running time does.
- **Not generic.** The algorithm uses the integer representatives of the group elements and does not work in other groups of the same order.
- **Precomputation.** Lines L3 to L11 do not involve $h$, so the logarithms of the factor bases serve every target modulo the same $p$. This is what the Logjam attack exploited: one precomputation for a widely used 512-bit prime broke many connections.
- **Subgroup order.** Only the prime factors of $r$ matter. For a subgroup of prime order $r$, the linear algebra is modulo $r$ alone.
- **Two sides.** A relation compares two factorizations in different rings, and both factor bases enter the unknowns.

## Variants and improvements

- **Gaussian integer method.** Coppersmith, Odlyzko and Schroeppel used $\mathbb{Z}[i]$, or another imaginary quadratic ring, with $p = c^2 + d^2$; this is the case implemented here. They also gave a sieve with $H = \lceil p^{1/2} \rceil$ and the products $(H + c_1)(H + c_2)$ (Galbraith, Section 15.5.2).
- **Schirokauer maps and virtual logarithms.** For number fields of higher degree, units are infinite and ideals need not be principal. Schirokauer's maps and his virtual logarithms make the rows well defined modulo $\ell$.
- **Special number field sieve.** When $p$ has a sparse form, a polynomial with very small coefficients exists and the constant drops to $(32/9)^{1/3}$.
- **Other finite fields.** Joux, Lercier, Smart and Vercauteren extended the method to $\mathbb{F}_{p^n}$ with $p$ of medium size and gave $L(1/3)$ algorithms for all finite fields (Galbraith, Section 15.5.7). For small $p$ the [function field sieve](/function-field-sieve/) is used instead.
- **Small prime orders.** If $r$ has a small prime factor, [Pohlig-Hellman](/pohlig-hellman/) with [baby-step giant-step](/baby-step-giant-step/) handles it faster than the sieve.

## When to use it

Use the number field sieve for discrete logarithms in large prime fields, from about $100$ decimal digits upward; it holds the records for prime field discrete logarithms. For small $p$, up to about $10^{30}$, basic [index calculus](/index-calculus/) or the Gaussian integer method is simpler. For small subgroups of a large field, generic methods such as [Pollard rho](/pollard-rho-discrete-logarithm/) in the subgroup may be cheaper, since their cost depends only on $r$. The quadratic version here is a teaching tool for the two-sided relations, the descent and the conversion.

## Pitfalls

- **Forgetting the constant $d$.** The rational side is $d (a + bs)$ and not $a + bs$. Line L7 puts $-1$ in the column of $d$; dropping it makes every row wrong unless $d = 1$.
- **Forgetting units and signs.** The rational side can be negative, and the algebraic side has a unit factor. Line L7 records the sign and the unit exponent $k$ in their own columns.
- **Generators of the same ideal.** Associates $\varepsilon \pi$ give the same ideal; the factor base must contain one generator per ideal, or the factorization is not unique. The implementation keeps one canonical associate.
- **Inert primes.** A rational prime $q$ that stays prime in $\mathbb{Z}[\omega]$ has norm $q^2$; it belongs to the algebraic factor base when $q^2 \le B$.
- **A zero common image.** If $p \mid N$, the relation says nothing. Line L7 tests $p \nmid N$.
- **Rank deficiency for tiny $p$.** If $B \ge p/2$, a prime $q \le B$ may be represented by $q - p$, and two columns can merge; the system then never reaches full rank. The implementation keeps $B \le (p - 1)/2$.
- **Dividing by the multiplicity.** In line L14, $k$ must be a unit modulo $\ell$.

## Implementations

## History

Coppersmith, Odlyzko and Schroeppel described the Gaussian integer method and the related $L_p(1/2)$ sieves in 1986. After the number field sieve for factoring appeared in 1990, Gordon gave the first number field sieve for discrete logarithms in prime fields in 1993, with a heuristic $L_p(1/3)$ running time. Schirokauer introduced his maps in the same year and obtained the constant $(64/9)^{1/3}$. Schirokauer, Weber and Denny made the method practical in 1996, and Joux, Lercier, Smart and Vercauteren extended it to medium characteristic in 2006. Large record computations followed, and the Logjam attack of 2015 used the precomputation property against 512-bit export-grade Diffie-Hellman.

## References
