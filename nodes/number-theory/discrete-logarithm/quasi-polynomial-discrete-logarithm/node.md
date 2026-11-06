---
tag: 7RM8BX
kind: algorithm
slug: quasi-polynomial-discrete-logarithm
name: Quasi-polynomial discrete logarithm algorithm
aliases:
- Barbulescu-Gaudry-Joux-Thome algorithm
- BGJT algorithm
- Quasi-polynomial algorithm for discrete logarithms in small characteristic
area: number-theory/discrete-logarithm
level: research
summary: Quasi-polynomial time DLP for small-characteristic finite fields.
solves: [finite-field-discrete-logarithm-problem, discrete-logarithm-problem]
model: word-ram
complexity:
  vars:
    Q: the field size q^(2k)
    q: the size of the base field F_q, a prime power, with F_(q^2) a subfield of the field
    k: the degree of the field over F_(q^2), at most q + 2
    D: the degree of a polynomial in the descent
    r: the order of g, a divisor of Q - 1
  time:
    heuristic: exp(O((ln ln Q)^2))
  space:
    extra: O(q^4 log k)
  bit_operations:
    heuristic: exp(O((ln ln Q)^2))
properties:
  deterministic: false
  recursive: true
prereqs: [index-calculus, finite-field-discrete-logarithm-problem, irreducible-polynomial, function-field-sieve]
see_also: [coppersmith-discrete-logarithm, number-field-sieve-discrete-logarithm, pohlig-hellman, factor-base, smooth-number, relation-collection, structured-gaussian-elimination, generic-group-model]
sources:
  - paper: doi:10.1007/978-3-642-55220-5_1
    title: Razvan Barbulescu, Pierrick Gaudry, Antoine Joux and Emmanuel Thome, A heuristic quasi-polynomial algorithm for discrete logarithm in finite fields of small characteristic, Advances in Cryptology, EUROCRYPT 2014
    locator: pages 1 to 16 (the sparse medium subfield representation, the systematic equation with the cosets of PGL2(F_q) in PGL2(F_(q^2)), the descent that halves the degree, and the heuristic bound max(q, k)^(O(log k)))
  - url: https://arxiv.org/abs/1306.4244
    title: Razvan Barbulescu, Pierrick Gaudry, Antoine Joux and Emmanuel Thome, A quasi-polynomial algorithm for discrete logarithm in finite fields of small characteristic, arXiv 1306.4244, version 2
    locator: Definition 1, Proposition 2, Theorem 3, Corollaries 4 to 6 in Sections 2 and 3; equations (Em), Heuristics 7 and 8 and the count q^3 + q of cosets in Section 4; Proposition 10 on the polynomials that divide h1 X^q - h0
  - paper: doi:10.1007/978-3-662-43414-7_18
    title: Antoine Joux, A new index calculus algorithm with complexity L(1/4 + o(1)) in small characteristic, Selected Areas in Cryptography, SAC 2013
    locator: pages 355 to 379 (the representation with X^q = h0(X)/h1(X) and the systematic equation, which the quasi-polynomial algorithm keeps)
  - paper: doi:10.1090/jams/985
    title: Thorsten Kleinjung and Benjamin Wesolowski, Discrete logarithms in quasi-polynomial time in finite fields of fixed characteristic, Journal of the American Mathematical Society 35(2), 2022
    locator: pages 581 to 624 (a proved expected running time (pn)^(2 log_2 n + O(1)) for F_(p^n))
  - paper: doi:10.1007/s10623-015-0147-6
    title: Antoine Joux and Cecile Pierrot, Technical history of discrete logarithms in small characteristic finite fields, Designs, Codes and Cryptography 78(1), 2016
    locator: pages 73 to 85 (the road from L(1/3) to quasi-polynomial complexity)
  - paper: doi:10.1007/978-3-662-44381-1_8
    title: Robert Granger, Thorsten Kleinjung and Jens Zumbragel, Breaking '128-bit secure' supersingular binary curves, Advances in Cryptology, CRYPTO 2014
    locator: pages 126 to 145 (a record computation that combines the new descent methods)
  - paper: doi:10.1090/mcom/3669
    title: Robert Granger, Thorsten Kleinjung, Arjen K. Lenstra, Benjamin Wesolowski and Jens Zumbragel, Computation of a 30750-bit binary field discrete logarithm, Mathematics of Computation 90, 2021
    locator: the whole paper (a record in a binary field with these methods)
---

The quasi-polynomial algorithm of Barbulescu, Gaudry, Joux and Thomé computes discrete logarithms in a finite field $\mathbb{F}_{q^{2k}}$ with $k \le q + 2$ that is given in a special form, $X^q \equiv h_0(X)/h_1(X)$ with $h_0$ and $h_1$ of small degree. Its heuristic running time is $\max(q, k)^{O(\log k)}$. For a field $\mathbb{F}_Q$ of small characteristic this becomes $2^{O((\log \log Q)^2)}$, which is quasi-polynomial in the input size $\log Q$ and smaller than $L_Q(\varepsilon)$ for every $\varepsilon > 0$. It is an [index calculus](/index-calculus/) method. Its relations come from one identity, the systematic equation $X^q - X = \prod_{\alpha \in \mathbb{F}_q} (X - \alpha)$, and its descent writes the logarithm of a polynomial of degree $D$ in terms of polynomials of degree at most $\lceil D/2 \rceil$.

## In plain words

Index calculus needs many field elements that split into small pieces. Such elements are usually rare, and the search costs a lot.

This algorithm works in a field built on a smaller field with $q^2$ elements, and it picks the defining polynomial so that raising to the power $q$ is cheap. One identity from the smaller field then gives many relations for free. Take the product of all $X - \alpha$ over the smallest field and change the variable. One side of the result is a product of small pieces. The other side is a polynomial of degree at most $3$, and it often splits too.

The same trick works on any polynomial in place of $X$. A polynomial of degree $D$ is then rewritten as pieces of half its degree. After about $\log k$ levels a target reaches the small pieces, and that depth gives the quasi-polynomial cost.

## The problem

**Input.** An odd prime power $q$, the field $\mathbb{F}_{q^2}$, polynomials $h_0, h_1 \in \mathbb{F}_{q^2}[X]$ of degree at most $2$ with $\gcd(h_0, h_1) = 1$, and a monic irreducible factor $I$ of degree $k$ of $h_1 X^q - h_0$. These define $K = \mathbb{F}_{q^2}[X]/(I) \cong \mathbb{F}_{q^{2k}}$, in which $X^q = h_0(X)/h_1(X)$. Also an element $g \ne 0$ of known order $r$ and an element $h \ne 0$. Field elements are polynomials in $X$ of degree below $k$. The implementation takes $q$ prime, $2 \le k \le q + 2$, and $h_1$ a product of linear factors.

**Output.** The $x \in \{0, \dots, r - 1\}$ with $g^x = h$, or NONE if $h \notin \langle g \rangle$.

**Cost model.** The group is $K^*$, cyclic of order $Q - 1$ with $Q = q^{2k}$, and the target lives in the subgroup $\langle g \rangle$ of order $r$. One multiplication in $K$ with schoolbook arithmetic costs $O(k^2)$ operations in $\mathbb{F}_{q^2}$, and one operation in $\mathbb{F}_{q^2}$ costs $O((\log q)^2)$ bit operations; the implementation uses tables of logarithms in $\mathbb{F}_{q^2}^*$, so that it costs $O(1)$ word operations. The algorithm factors polynomial representatives, so it is not generic and the [generic lower bound](/shoup-generic-lower-bound/) does not apply. The bound $\max(q, k)^{O(\log k)}$ of Barbulescu, Gaudry, Joux and Thomé is heuristic: it assumes that the reduced sides of the equations below are smooth as often as random polynomials of the same degree, that certain matrices built from the action of $\mathrm{PGL}_2(\mathbb{F}_q)$ have full rank (their Heuristics 7 and 8), and that a representation with $\deg h_0, \deg h_1 \le 2$ exists. For fixed characteristic $p$, Kleinjung and Wesolowski proved an expected running time of $(pn)^{2 \log_2 n + O(1)}$ for $\mathbb{F}_{p^n}$, so a quasi-polynomial bound is now a theorem for that case.

## The algorithm

**The systematic equation.** For the $q + 1$ points $(\alpha : \beta)$ of the projective line over $\mathbb{F}_q$, $Y^q Z - Y Z^q = Z \prod_{\alpha \in \mathbb{F}_q} (Y - \alpha Z)$ holds in every commutative $\mathbb{F}_q$-algebra. For a matrix $m = \begin{pmatrix} a & b \\ c & d \end{pmatrix}$ with entries in $\mathbb{F}_{q^2}$ and $ad - bc \ne 0$, substitute $Y = aX + b$ and $Z = cX + d$. Write $\tilde a = a^q$. Since $(aX + b)^q = \tilde a X^q + \tilde b$ and $h_1 X^q \equiv h_0$ in $K$, multiplying by $h_1$ gives

$$h_1 \cdot Z \prod_{\alpha \in \mathbb{F}_q} (Y - \alpha Z) \equiv R_m = (\tilde a h_0 + \tilde b h_1)(cX + d) - (aX + b)(\tilde c h_0 + \tilde d h_1) \pmod I .$$

The left side is $h_1$ times a product of $q + 1$ polynomials of degree at most $1$. The right side has degree at most $3$. If $R_m$ splits into linear factors over $\mathbb{F}_{q^2}$, taking logarithms gives one linear relation among the logarithms of the $q^2$ monic linear polynomials $X + \beta$. Matrices in the same coset of $\mathrm{PGL}_2(\mathbb{F}_q)$ give the same relation, so only the $q^3 + q$ cosets of $\mathrm{PGL}_2(\mathbb{F}_{q^2}) / \mathrm{PGL}_2(\mathbb{F}_q)$ count.

**The descent.** For a polynomial $P$ of degree $D \ge 2$, Barbulescu, Gaudry, Joux and Thomé substitute $Y = aP + b$ and $Z = cP + d$ instead. Now the product side is a product of translates $P - u$ with $u \in \mathbb{F}_{q^2}$, and the reduced side has a numerator of degree at most $3D$. They keep the cosets whose numerator is $\lceil D/2 \rceil$-smooth. Each kept coset gives a row with a $1$ in the columns of the $q + 1$ translates that occur, out of $q^2 + 1$ columns. If this matrix has full rank, a linear combination of rows isolates the column of $P$ itself, and this writes $\log P$ in terms of $\log h_1$ and of at most $O(q^2 D)$ logarithms of polynomials of degree at most $\lceil D/2 \rceil$ (their Proposition 2). Applying the step again to each piece gives a tree of depth $O(\log k)$ and arity $O(q^2 k)$.

**The version below.** The pseudocode is what the implementation runs on fields with up to about $10^6$ elements. It collects the relations for $P = X$, and it keeps, from the same cosets, those with $R_m = c \cdot Q \cdot \ell_1$ where $Q$ is an irreducible quadratic and $\ell_1$ has degree at most $1$; each such coset gives $\log Q$. It does not run the recursive descent: it shifts the target by random powers of a generator $\gamma$ until it splits into linear factors and such quadratics. That last step has exponential cost in general, and it is there only to make the toy complete. As in [index calculus](/index-calculus/), logarithms are computed modulo $\ell = \prod \rho^e$ over the prime powers $\rho^e \parallel Q - 1$ with $\rho \mid r$, and the logarithm of a constant $c \in \mathbb{F}_{q^2}^*$ is known from $\omega = \gamma^{(Q-1)/(q^2-1)}$, which generates $\mathbb{F}_{q^2}^*$.

```pseudo id=main
QPA(g, h, r, q, h_0, h_1, I)       ▷ I irreducible of degree k, I | h_1·X^q − h_0, g of order r; returns x with g^x = h, or NONE
L1  if h^r ≠ 1 then return NONE
L2  if h = 1 then return 0
L3  γ ← a generator of K* ; ℓ ← ∏ ρ^e over the prime powers ρ^e ∥ Q − 1 with ρ | r
L4  columns ← the q^2 polynomials X + β, β ∈ F_(q^2) ; R ← empty list ; E ← empty map
L5  for each coset m = (a b; c d) of PGL_2(F_(q^2)) / PGL_2(F_q) do                 ▷ relations
L6      Y ← aX + b ; Z ← cX + d ; R_m ← (a^q h_0 + b^q h_1)·Z − Y·(c^q h_0 + d^q h_1)
L7      if R_m = c_0 ∏ (X + β)^(e_β) then append (factors of h_1 and of Z ∏ (Y − αZ), minus e ; L(c_0) minus the constants) to R
L8      else if R_m = c_0 · Q · ∏ (X + β)^(e_β) with Q irreducible of degree 2 then E[Q] ← that row
L9  repeat m ← random in [0, Q − 2] ; z ← γ^m                                       ▷ fix the scale
L10     if z = c ∏ (X + β)^(a_β) then append (a ; m − L(c)) to R
L11 until SOLVE(R, ρ, ρ^e) succeeds for every ρ^e ∥ ℓ ; λ ← the CRT combination, so λ_β ≡ L(X + β) (mod ℓ)
L12 for y ∈ {g, h} do                                                               ▷ individual logarithms
L13     repeat m ← random ; z ← y·γ^m mod I, split as c ∏ (X + β)^(d_β) ∏ Q_i^(u_i)
L14     until every Q_i is a key of E
L15     L(y) ← L(c) + Σ d_β λ_β + Σ u_i (e_i · λ − k_i) − m mod ℓ, where E[Q_i] = (e_i ; k_i)
L16 c ← ℓ / r ; u ← L(g) / c                                                        ▷ u is a unit modulo r
L17 return (L(h) / c) · u^(−1) mod r
SOLVE(R, ρ, M)                                                                      ▷ solve all rows of R modulo M = ρ^e
L18 for each column j: find a row i ≥ j whose entry in column j is not divisible by ρ; if none, return FAIL
L19     swap rows i and j, scale row j by the inverse of its pivot modulo M, and clear column j in every other row
L20 return λ_j = the right side of row j, for every column j
```

Lines L1 and L2 decide membership and handle $h = 1$; $K^*$ is cyclic, so $\langle g \rangle = \{y : y^r = 1\}$. Line L3 finds a generator from the factorization of $Q - 1$. Lines L5 to L8 run over one matrix in each coset. A row $(e ; v)$ means $\sum_\beta e_\beta L(X + \beta) \equiv v$. In line L7 each factor $uX + w$ of degree $1$ of the left side adds $1$ to the column of $X + w/u$ and $-L(u)$ to the right side, each constant factor $w$ adds $-L(w)$, and the factors of $h_1$ are counted the same way. Line L8 keeps the same row for a coset whose $R_m$ has one irreducible quadratic factor $Q$; then $L(Q) \equiv e \cdot \lambda - v$. Lines L9 to L11 add rows from powers of $\gamma$ that split into linear factors, until elimination modulo each prime power has a unit pivot in every column. These rows fix the scale of the solution, which the homogeneous rows of line L7 do not fix when the constants have logarithm $0$ modulo $\ell$. Lines L12 to L15 split shifts of $g$ and $h$, and lines L16 and L17 convert the logarithms to base $\gamma$ into the logarithm to base $g$.

The coset representatives come from a count of $\mathbb{F}_q$-structures. A coset is fixed by the $\mathbb{F}_q$-span $W$ of the rows $(a, b)$ and $(c, d)$, up to a scalar in $\mathbb{F}_{q^2}^*$. If the first coordinates of $W$ span a line over $\mathbb{F}_q$, then $W$ is spanned by $(1, b)$ and $(0, \delta)$, with $\delta$ taken modulo $\mathbb{F}_q^*$ and $b$ modulo $\mathbb{F}_q \delta$, which gives $q(q + 1)$ cosets. Otherwise $W = \{(x, s x + t x^q)\}$ with $s \in \mathbb{F}_{q^2}$ and $t \ne 0$ taken modulo the $q + 1$ elements of norm $1$, which gives $q^2(q - 1)$ cosets. The total is $q^3 + q$. The test file checks the count and that the $q^3 + q$ sets of $q + 1$ points are all different.

The implementation searches $h_0$ and $h_1$ at random with a fixed seed, or takes them from the caller. SOLVE runs once $R$ has $q^2 + 10$ rows, and after a failure it waits for $\max(10, q^2/4)$ more rows.

## Example

Take $q = 3$ and $\mathbb{F}_9 = \mathbb{F}_3(i)$ with $i^2 = -1$. Let $h_0 = X + 1$ and $h_1 = 1$. Then $X^3 - h_0 = X^3 - X - 1$ has no root in $\mathbb{F}_9$, so this cubic is irreducible, $I = X^3 - X - 1$, $k = 3$ and $K = \mathbb{F}_{729}$, with $X^3 = X + 1$. The generator found by line L3 is $\gamma = X + i$. Let $g = X + 1$, which has order $r = 13$, so $\ell = 13$. The constants of $\mathbb{F}_9^*$ have logarithms that are multiples of $728/8 = 91 = 7 \cdot 13$, so they drop out modulo $13$.

Of the $30$ cosets, $18$ give a split $R_m$ and $12$ give an irreducible quadratic. Two of the relations:

- $m$ the identity: $Y = X$, $Z = 1$. The left side is $X (X - 1)(X - 2) = X^3 - X$, and $R_m = h_0 - X h_1 = 1$. So $\lambda_X + \lambda_{X+1} + \lambda_{X+2} \equiv 0$.
- $Y = X + 1$, $Z = i$. The left side is $i (X + 1)(X + 1 + 2i)(X + 1 + i)$, and $R_m = (h_0 + 1) \cdot i - (X + 1) \cdot i^3 = i (X + 2) + i (X + 1) = 2iX$. So $\lambda_{X+1} + \lambda_{X+1+i} + \lambda_{X+1+2i} \equiv \lambda_X$.

The $18$ rows have rank $8$ modulo $13$. One row from line L10, $\gamma^1 = X + i$, gives $\lambda_{X+i} = 1$, and then SOLVE returns

| $\beta$ | $0$ | $1$ | $2$ | $i$ | $1 + i$ | $2 + i$ | $2i$ | $1 + 2i$ | $2 + 2i$ |
|---|---|---|---|---|---|---|---|---|---|
| $\lambda_{X+\beta} \bmod 13$ | $10$ | $4$ | $12$ | $1$ | $3$ | $9$ | $1$ | $3$ | $9$ |

The two relations above check: $10 + 4 + 12 = 26 \equiv 0$, and $4 + 3 + 3 = 10$.

Now take $h = 2X^2 + 2X + 1$. Suppose line L13 draws $m = 5$: then $z = h \gamma^5 = X^2 + X + i$, which has no root in $\mathbb{F}_9$, so $Q = X^2 + X + i$. The coset with $Y = X + 1 + i$ and $Z = iX + 2 + 2i$ has $R_m = 2iX^2 + 2iX + 1 = 2i \cdot Q$, since $2i \cdot i = 1$. Its left side has the monic factors $X + 2 + i$ (from $Z$), $X + 1 + i$, $X + 2i$ and $X$, so $L(Q) \equiv 9 + 3 + 1 + 10 = 23 \equiv 10$. Hence $L(h) \equiv 10 - 5 = 5$. Also $L(g) = \lambda_{X+1} = 4$. Here $c = \ell / r = 1$, so $x = 5 \cdot 4^{-1} = 5 \cdot 10 = 50 \equiv 11 \pmod{13}$. Indeed $(X + 1)^{11} = 2X^2 + 2X + 1$ in $K$. The test file checks this example with the implementation for five seeds.

## Correctness

The systematic identity $Y^q Z - Y Z^q = Z \prod_{\alpha \in \mathbb{F}_q} (Y - \alpha Z)$ holds as a polynomial identity over $\mathbb{F}_q$, and $h_1 (aX + b)^q \equiv \tilde a h_0 + \tilde b h_1$ modulo $I$. So each coset gives a true congruence $h_1 Z \prod (Y - \alpha Z) \equiv R_m$ in $K$. Both sides are nonzero: the factors on the left have degree at most $1 < k$ and are not zero because $ad - bc \ne 0$, and $I \nmid h_1$ because $\gcd(h_0, h_1) = 1$. Taking logarithms, each row of line L7 or line L8 holds modulo $Q - 1$, and so does each row of line L10. Elimination with unit pivots keeps the true vector as the unique solution modulo each $\rho^e$. The rest is the descent and conversion of [index calculus](/index-calculus/). The full argument is in [the correctness proof](proofs/correctness.md).

## Complexity

One step of the descent of Barbulescu, Gaudry, Joux and Thomé tests $q^3 + q$ cosets, each with a smoothness test on a polynomial of degree at most $3D$, and solves a sparse system with $q^2 + 1$ columns and $q + 1$ entries in each row, which costs $O(q^5)$ operations with sparse methods. So one node of the descent tree costs a polynomial in $q$ and $k$. The tree has depth $O(\log k)$, since the degree halves at each level, and arity $O(q^2 k)$. The number of nodes is at most $(q^2 k)^{O(\log k)}$, which gives $\max(q, k)^{O(\log k)}$ for the whole computation (their Theorem 3). The cost of the logarithms of the linear polynomials is polynomial in $q$.

In terms of the field size: if $q$ and $k$ are of the same size, then $Q \approx q^{2q}$ and $\log q = O(\log \log Q)$, so the cost is $q^{O(\log q)} = 2^{O((\log \log Q)^2)}$ (their Corollary 4). A field $\mathbb{F}_{p^n}$ with $p$ at most polynomial in $\log Q$ embeds into a field $\mathbb{F}_{q^{2k}}$ with $q = p^{\lceil \log_p k \rceil}$ and $k = n$ or $n/2$, which gives the same form (their Corollary 5); for example, $2^{O((\log n)^2)}$ for $\mathbb{F}_{2^n}$. If $q$ grows as $L_Q(\alpha)$, the cost is $L_Q(\alpha)^{O(\log \log Q)}$, which beats the [function field sieve](/function-field-sieve/) for $\alpha < 1/3$ (their Corollary 6). All these bounds are heuristic; the proved bound of Kleinjung and Wesolowski is given in the cost model.

Space: one node holds $O(q^3)$ rows with $q + 1$ entries each, and a depth-first traversal keeps one node for each level, which gives $O(q^4 \log k)$ entries.

The implementation is a toy. Lines L5 to L8 cost $O(q^3)$ cosets times $O(q^2)$ root tests. The dense elimination costs $O(q^6)$ operations modulo $\ell$. Lines L9 to L15 rely on random shifts, which split with probability about $1/(k-1)!$ when only linear factors are allowed, so their cost is exponential in $k$. The implementation also factors $Q - 1$ by trial division, which costs $O(Q^{1/2})$ divisions.

## Properties

- **Randomized.** The scale rows and the shifts use random exponents. The answer does not depend on them, only the running time does.
- **Not generic.** It uses the polynomial representation and the special form $X^q = h_0/h_1$; it does not apply to elliptic curves or other groups of the same order.
- **Precomputation.** Lines L3 to L11 do not involve $h$, so the logarithms of the linear polynomials serve every target in the same field.
- **One identity.** Every relation, at every level of the descent, comes from the systematic equation and a homography; no sieve over pairs of polynomials is needed.
- **Small degree of the reduced side.** For $P = X$ the reduced side has degree at most $1 + \max(\deg h_0, \deg h_1)$, which is why so many cosets give relations.

## Variants and improvements

- **Joux's $L(1/4)$ algorithm.** Joux introduced the representation $X^q = h_0/h_1$ and the systematic equation, and reached $L_Q(1/4 + o(1))$; its descent uses Gröbner bases for the middle degrees. The quasi-polynomial algorithm keeps the representation and replaces the descent.
- **A faster descent.** Barbulescu, Gaudry, Joux and Thomé note that, if the reduced sides are as smooth as random polynomials, one can choose among the cosets and descend to degree $O(D \log \log q / \log q)$, which gives $\max(q, k)^{O(\log k / \log \log q)}$.
- **Divisors of $h_1 X^q - h_0$.** An irreducible factor of $h_1 X^q - h_0$ other than $I$ divides every reduced side of the equations for it, so the descent step fails on it. Their Proposition 10 gives a separate relation for such a polynomial in terms of others of at most the same degree when $\deg h_0, \deg h_1 \le 2$.
- **Practical descents.** Record computations combine the new descent for high degrees with other elimination methods for low degrees; Granger, Kleinjung and Zumbrägel did so in 2014, and Granger, Kleinjung, Lenstra, Wesolowski and Zumbrägel computed a logarithm in a field of $2^{30750}$ elements.
- **Proved versions.** Kleinjung and Wesolowski proved a quasi-polynomial expected time for fixed characteristic, which removes the heuristics for that case.

## When to use it

Use these methods for fields of small characteristic, such as $\mathbb{F}_{2^n}$ and $\mathbb{F}_{3^n}$, and for fields $\mathbb{F}_{q^k}$ where $q$ is small compared with $k$. They show that such fields are not suitable for cryptography, including the fields in which pairings on supersingular curves of small characteristic take values. For prime fields and fields of large characteristic, use the [number field sieve](/number-field-sieve-discrete-logarithm/); for medium characteristic the [function field sieve](/function-field-sieve/) and the number field sieve remain the methods to compare. The toy version on this page only illustrates the relations and the conversion.

## Pitfalls

- **The factor $h_1$.** The congruence of line L6 has $h_1$ on the left side. Line L7 must add the factors of $h_1$ to the row; dropping them gives false rows unless $h_1$ is constant.
- **The Frobenius on coefficients.** In line L6 the coefficients $a, b, c, d$ are raised to the power $q$. Using $a$ in place of $a^q$ gives a polynomial that is not congruent to the left side.
- **Factors of degree $0$.** When $a = \alpha c$ for some $\alpha \in \mathbb{F}_q$, the factor $Y - \alpha Z$ is a constant. Line L7 must take its logarithm as a constant and not put it in a column.
- **Counting a coset twice.** Matrices in the same coset give the same row; enumerating all of $\mathrm{PGL}_2(\mathbb{F}_{q^2})$ costs $q(q^2 - 1)$ times more and gives no new information. Line L5 runs over one matrix in each coset.
- **Forgetting the scale.** If the logarithms of the constants are $0$ modulo $\ell$, every row of line L7 is homogeneous, and every multiple of the true vector satisfies them. Lines L9 and L10 add rows with right side $m$.
- **Too small $q$.** The heuristics need $\Theta(q^3)$ relations for $q^2 + 1$ unknowns, which can fail for small $q$; the toy relies on lines L9 and L10 to reach full rank.
- **Dropping the shift.** Line L15 must subtract $m$, since $z = y \gamma^m$ and not $y$ was split.

## Implementations

## History

Joux published an algorithm with complexity $L(1/4 + o(1))$ for small characteristic in 2013, with the representation $X^q = h_0/h_1$ and the systematic equation. In the same year Barbulescu, Gaudry, Joux and Thomé gave the descent that halves the degree and obtained a heuristic quasi-polynomial complexity; the paper appeared at EUROCRYPT 2014. Joux and Pierrot describe the steps from $L(1/3)$ to quasi-polynomial complexity. Kleinjung and Wesolowski proved a quasi-polynomial bound for fixed characteristic in 2022, and records in binary fields reached $30750$ bits in 2021.

## References
