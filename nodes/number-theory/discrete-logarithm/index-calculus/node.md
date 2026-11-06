---
tag: C3H4Y5
kind: algorithm
slug: index-calculus
name: Index calculus
aliases:
- index calculus method
- index calculus algorithm
area: number-theory/discrete-logarithm
level: advanced
summary: Subexponential DLP method in (Z/pZ)^*. Collect relations among smooth powers of a generator, solve a linear system for the logarithms of small primes, then express the target over them.
solves: [discrete-logarithm-problem, finite-field-discrete-logarithm-problem]
model: word-ram
complexity:
  vars:
    p: the prime modulus
    n: the order of g
    t: the size of the factor base, the number of primes below B
  time:
    heuristic: exp((2 + o(1)) (ln p ln ln p)^(1/2))
  space:
    extra: O(t^2 + t log p)
  bit_operations:
    heuristic: exp((2 + o(1)) (ln p ln ln p)^(1/2))
properties:
  deterministic: false
  recursive: false
prereqs: [discrete-logarithm-problem, factor-base, smooth-number, chinese-remainder-theorem]
see_also: [relation-collection, number-field-sieve-discrete-logarithm, function-field-sieve, coppersmith-discrete-logarithm, quasi-polynomial-discrete-logarithm, semaev-summation-polynomial-index-calculus, structured-gaussian-elimination, dickman-function]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 3, Section 3.6.5 (Algorithm 3.68, Example 3.69, Notes 3.71 to 3.73), Section 3.6.6 (logarithms in subgroups via a generator of the whole group) and Section 3.12 (notes on the history and on the rigorous bounds)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 15, Section 15.5.1 (the rigorous algorithm, Example 15.5.4, Exercises 15.5.6 and 15.5.7 giving L_p(1/2, 2 + o(1))), Section 15.5.2 (the heuristic algorithms of Coppersmith, Odlyzko and Schroeppel and the number field sieve)
  - paper: doi:10.1007/bf01840433
    title: Don Coppersmith, Andrew M. Odlyzko and Richard Schroeppel, Discrete logarithms in GF(p), Algorithmica 1, 1986
    locator: pages 1 to 15 (the linear sieve, the residue list sieve and the Gaussian integer method, with heuristic time L_p(1/2, 1))
  - paper: "Carl Pomerance, Fast, rigorous factorization and discrete logarithm algorithms, in Discrete Algorithms and Complexity, Academic Press, 1987"
    locator: pages 119 to 143 (the rigorous expected time L_p(1/2, 2^(1/2)) for discrete logarithms in (Z/pZ)^*)
---

Index calculus computes discrete logarithms in $(\mathbb{Z}/p\mathbb{Z})^*$ in [subexponential time](/subexponential-time/), far faster than the $\sqrt n$ of generic methods. It fixes a [factor base](/factor-base/) of small primes, finds many exponents $k$ for which $\gamma^k \bmod p$ is [smooth](/smooth-number/), and reads each factorization as a linear equation among the unknown logarithms of the primes. Linear algebra modulo the group order then gives all those logarithms, and one more smooth value $h \gamma^k$ expresses $\log h$ in terms of them. The basic version with trial division runs in $L_p(1/2, 2)$ bit operations, and its descendants, the [number field sieve](/number-field-sieve-discrete-logarithm/) and the [function field sieve](/function-field-sieve/), are the methods that break finite field discrete logarithms in practice.

## In plain words

The logarithm turns multiplication into addition. So if a power of the base splits into small primes, the exponent equals a sum of the unknown logarithms of those primes. Each such split is one equation.

Try many random powers, keep those that split into small primes only, and stop when there are a few more equations than primes. Solving the equations gives the logarithm of every small prime. Then multiply the target by a random power until the product also splits into small primes; its logarithm is the sum of known ones, minus the power used.

The first part does not involve the target at all, so it can be done once and reused for every target in the same group.

## The problem

**Input.** A prime $p$, an element $g$ of $(\mathbb{Z}/p\mathbb{Z})^*$ of known order $n$, and an element $h$.

**Output.** The $x \in \{0, \dots, n - 1\}$ with $g^x = h$, or NONE if $h \notin \langle g \rangle$.

**Cost model.** The group is $(\mathbb{Z}/p\mathbb{Z})^*$, cyclic of order $p - 1$, with elements represented by integers in $[1, p - 1]$; the target lives in the subgroup $\langle g \rangle$ of order $n$. A multiplication modulo $p$ costs $O(\log^2 p)$ bit operations. The algorithm is not generic: it factors the integer representatives, so the [generic lower bound](/shoup-generic-lower-bound/) does not apply. Costs are in bit operations and in $L$-notation, $L_p(\alpha, c) = \exp((c + o(1)) (\ln p)^\alpha (\ln \ln p)^{1 - \alpha})$. With a factor base of size $L_p(1/2, 1/2)$, relation collection by trial division and dense linear algebra, the expected cost is $L_p(1/2, 2)$: the smoothness estimate is proved, because $\gamma^k$ is uniform in $(\mathbb{Z}/p\mathbb{Z})^*$, but the number of relations needed for full rank is heuristic. Galbraith's variant with a kernel vector is proved at $L_p(1/2, 2)$, and Pomerance proved $L_p(1/2, \sqrt 2)$; the sieving variants are heuristic.

## The algorithm

Let $\gamma$ be a generator of $(\mathbb{Z}/p\mathbb{Z})^*$, and write $L(y)$ for $\log_\gamma y \bmod (p - 1)$. If $g$ has order $n$, then $L(g) = c u$ with $c = (p - 1)/n$ and $u$ a unit modulo $n$, and $h = g^x$ gives $L(h) = x c u$, so $x = (L(h)/c) \, u^{-1} \bmod n$ (HAC, Section 3.6.6). Only the parts of $p - 1$ for primes dividing $n$ matter, so all logarithms are computed modulo $\ell = \prod q^f$ over the prime powers $q^f \parallel p - 1$ with $q \mid n$; when $n$ is a prime $r$ with $r^2 \nmid p - 1$, this is linear algebra over the field $\mathbb{F}_r$. Modulo a prime power $q^f$ every entry not divisible by $q$ is invertible, and elimination uses only such pivots.

```pseudo id=main
INDEX-CALCULUS(g, h, n, p)              ▷ g of order n modulo the prime p; returns x with g^x = h, or NONE
L1  if h^n ≠ 1 then return NONE
L2  if h = 1 then return 0
L3  γ ← a generator of (Z/pZ)^* ; ℓ ← ∏ q^f over the prime powers q^f ∥ p − 1 with q | n
L4  S ← the primes below min(B, p) ; R ← empty list        ▷ the factor base
L5  repeat                                                 ▷ relation collection
L6      k ← random in [0, p − 2]
L7      if γ^k mod p = ∏ s^(e_s) over s ∈ S then append (e, k) to R   ▷ k ≡ Σ e_s L(s) (mod p − 1)
L8      if |R| ≥ |S| + 10 then for each q^f ∥ ℓ, λ⁽q⁾ ← SOLVE(R, q, q^f)
L9  until every SOLVE succeeded ; λ ← the CRT combination of the λ⁽q⁾, so λ_s ≡ L(s) (mod ℓ)
L10 for y ∈ {g, h} do                                       ▷ individual logarithms
L11     repeat k ← random in [0, p − 2] until y · γ^k mod p = ∏ s^(d_s) over s ∈ S
L12     L(y) ← Σ d_s λ_s − k mod ℓ
L13 c ← ℓ / n ; u ← L(g) / c                               ▷ u is a unit modulo n
L14 return (L(h) / c) · u^(−1) mod n
SOLVE(R, q, m)                                              ▷ solve all rows of R modulo m = q^f
L15 for each column j: find a row i ≥ j whose entry in column j is not divisible by q; if none, return FAIL
L16     swap rows i and j, scale row j by the inverse of its pivot modulo m, and clear column j in every other row
L17 return λ_j = the right side of row j, for every column j
```

Line L1 decides membership, since $\langle g \rangle$ is the unique subgroup of order $n$ of the cyclic group $(\mathbb{Z}/p\mathbb{Z})^*$, and line L2 handles $h = 1$. Line L3 finds a generator from the factorization of $p - 1$ and fixes the modulus $\ell$. Lines L5 to L9 collect relations: an exponent $k$ whose power factors over $S$ gives $k \equiv \sum_s e_s L(s) \pmod{p - 1}$, because $L$ turns products into sums. Once there are at least $|S| + 10$ relations, line L8 tries Gauss-Jordan elimination modulo each prime power; it succeeds when every column has a pivot not divisible by $q$, and then the logarithms of the primes are determined modulo $q^f$. Line L9 combines them with the [Chinese remainder theorem](/chinese-remainder-theorem/). Lines L10 to L12 are the descent: a random shift $y \gamma^k$ that factors over $S$ gives $L(y) = \sum_s d_s L(s) - k$. Lines L13 and L14 convert the two logarithms to base $\gamma$ into the logarithm to base $g$. The implementation takes $B = \max(12, 2 L_p(1/2, 1/2))$ rounded, retries line L8 every $5$ new relations, and uses trial division at lines L7 and L11.

## Example

This is HAC's Example 3.69: $p = 229$, $\gamma = g = 6$ of order $n = 228 = 2^2 \cdot 3 \cdot 19$, and $h = 13$. Here $\ell = 228$. The factor base is $S = \{2, 3, 5, 7, 11\}$, and six smooth powers are found:

| $k$ | $6^k \bmod 229$ | factorization |
|---|---|---|
| 100 | 180 | $2^2 \cdot 3^2 \cdot 5$ |
| 18 | 176 | $2^4 \cdot 11$ |
| 12 | 165 | $3 \cdot 5 \cdot 11$ |
| 62 | 154 | $2 \cdot 7 \cdot 11$ |
| 143 | 198 | $2 \cdot 3^2 \cdot 11$ |
| 206 | 210 | $2 \cdot 3 \cdot 5 \cdot 7$ |

Each row is an equation; the first says $100 \equiv 2 L(2) + 2 L(3) + L(5) \pmod{228}$. Since $\mathbb{Z}/228\mathbb{Z}$ is not a field, line L8 solves the system modulo $4$, $3$ and $19$ separately. Each has a unit pivot in every column, and the solutions are $(1, 0, 2, 3, 2)$ modulo $4$, $(0, 1, 2, 2, 0)$ modulo $3$, and $(2, 18, 3, 12, 10)$ modulo $19$. The Chinese remainder theorem combines them into

$$L(2) = 21, \quad L(3) = 208, \quad L(5) = 98, \quad L(7) = 107, \quad L(11) = 162,$$

and indeed $6^{21} \equiv 2$, $6^{208} \equiv 3$, and so on. For the descent, $k = 77$ gives $13 \cdot 6^{77} \equiv 147 = 3 \cdot 7^2 \pmod{229}$, so

$$L(13) = L(3) + 2 L(7) - 77 = 208 + 214 - 77 \equiv 117 \pmod{228},$$

and $6^{117} \equiv 13 \pmod{229}$. Here $g = \gamma$, so $c = 1$, $u = 1$ and $x = 117$. In a subgroup, as in Galbraith's Example 15.5.4 with $p = 223$, $g = 15$ of order $37$ and $h = 68$, only $\ell = 37$ matters, the linear algebra is over $\mathbb{F}_{37}$, and the answer is $13$.

## Correctness

Every relation of line L7 is true modulo $p - 1$: if $\gamma^k = \prod s^{e_s}$, taking $L$ of both sides gives $k \equiv \sum e_s L(s)$. So the true vector $(L(s) \bmod q^f)_s$ satisfies every row modulo each $q^f \mid \ell$. Gauss-Jordan elimination with unit pivots replaces rows by invertible combinations of rows, so the solution set does not change, and when every column has a unit pivot the reduced system determines each unknown; hence $\lambda^{(q)}$ is the true vector modulo $q^f$, and after the Chinese remainder theorem $\lambda_s \equiv L(s) \pmod \ell$. Line L12 is the same argument for one row. For lines L13 and L14, $\gcd(L(g), p - 1) = (p - 1)/n$, so modulo $\ell$ the $q$-adic valuation of $L(g)$ is that of $c = \ell / n$ and $u$ is a unit modulo $n$; with $h = g^x$, $L(h) \equiv x c u \pmod \ell$ gives $x \equiv (L(h)/c) u^{-1} \pmod n$. Termination holds with probability $1$, since a power $\gamma^k$ equal to a prime $s \in S$ appears with positive probability and gives a unit pivot in column $s$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Smoothness.** Put $u = \ln p / \ln B$. By the theorem of Canfield, Erdős and Pomerance, a uniform integer below $p$ is $B$-smooth with probability $u^{-u(1 + o(1))}$, governed by the [Dickman function](/dickman-function/). Since $\gamma^k$ is uniform in $(\mathbb{Z}/p\mathbb{Z})^*$, this applies to line L7 without heuristics.
- **Balancing.** About $t = \pi(B)$ relations are needed, each after $u^{u(1 + o(1))}$ trials costing $O(t)$ trial divisions. Linear algebra on a $t \times t$ system costs $t^{3}$ with dense elimination or $t^{2 + o(1)}$ with Lanczos or Wiedemann methods, since each row has $O(\log p)$ nonzero entries. Taking $B = L_p(1/2, 1/2)$ makes both stages $L_p(1/2, 2)$ bit operations (Galbraith, Exercises 15.5.6 and 15.5.7).
- **Proved and heuristic.** The smoothness count is proved; whether $t + 10$ relations reach full rank modulo every $q$ is not, which makes the bound for this version heuristic (HAC, Section 3.12). Galbraith's version collects $t + 1$ relations and uses any kernel vector, which needs no rank condition and is proved at $L_p(1/2, 2)$; Pomerance's algorithm, with elliptic curve smoothness tests, is proved at $L_p(1/2, \sqrt 2)$.
- **Precomputation and descent.** Lines L3 to L9 depend only on $p$ and $g$'s group; each new target costs only the descent of line L11, about $u^{u}$ trials, much less than the precomputation.
- **Space.** $O(t \log p)$ for the sparse relations and $O(t^2)$ for dense elimination.
- **Subgroups.** The cost depends on $p$, not on $n$: for a subgroup of prime order $r \ll L_p(1/2, 2)$, [Pollard's rho](/pollard-rho-discrete-logarithm/) in $\sqrt r$ is faster, which is why DSA uses a large prime $p$ with a much smaller prime order subgroup.

## Properties

- **Las Vegas.** Each output is determined by true relations; the running time is random.
- **Not generic.** It needs a representation with a notion of smallness and unique factorization, here the integers; this is why it does not apply to general elliptic curves.
- **Two phases.** Relation collection and linear algebra are independent of the target, so one precomputation serves every logarithm in the same field. This is what made the Logjam attack on shared Diffie-Hellman primes practical.
- **Parallel collection.** Relations can be found on many machines independently and collected centrally (HAC, Note 3.73); the linear algebra is the harder step to distribute.
- **Linear algebra modulo the group order.** Unlike factoring, which needs dependencies modulo $2$, the system is solved modulo large primes $q \mid p - 1$.

## Variants and improvements

- **Sieving.** The linear sieve, the residue list sieve and the Gaussian integer method of Coppersmith, Odlyzko and Schroeppel produce relations among values of size about $\sqrt p$ that can be sieved, with heuristic time $L_p(1/2, 1)$.
- **Number field sieve.** Two factor bases, of rational primes and of prime ideals in a number field, give $L_p(1/3, (64/9)^{1/3})$ heuristic: the [number field sieve for discrete logarithms](/number-field-sieve-discrete-logarithm/).
- **Small characteristic.** In $\mathbb{F}_{2^n}$ the factor base is the irreducible polynomials of low degree. [Coppersmith's algorithm](/coppersmith-discrete-logarithm/) reached $L(1/3)$ first, the [function field sieve](/function-field-sieve/) generalizes it, and the [quasi-polynomial algorithms](/quasi-polynomial-discrete-logarithm/) of 2013 and later are faster still.
- **Elliptic curves and other groups.** Index calculus in Jacobians of high genus curves is subexponential; for elliptic curves, [summation polynomials](/semaev-summation-polynomial-index-calculus/) define a factor base, without a known subexponential bound over prime fields.
- **Better linear algebra.** [Structured Gaussian elimination](/structured-gaussian-elimination/) shrinks the sparse system, and the [block Lanczos](/block-lanczos-algorithm/) or [block Wiedemann](/block-wiedemann-algorithm/) methods solve it.
- **Better descent.** Writing $h \gamma^k \equiv w_1 / w_2$ with $w_1, w_2 \approx \sqrt p$ and requiring both to be smooth, or descending through medium primes with special-q sieving, makes individual logarithms cheap.

## When to use it

Use it for discrete logarithms in $(\mathbb{Z}/p\mathbb{Z})^*$, or in a large subgroup of it, once $p$ is beyond the reach of $\sqrt n$ methods; for $p$ of cryptographic size, use the number field sieve, which is the index calculus with a better relation search. It is also the method to use when many logarithms in one field are wanted, since the precomputation is shared. For small subgroups of large prime order, or for elliptic curves, use [Pohlig-Hellman](/pohlig-hellman/) and [rho](/pollard-rho-discrete-logarithm/) instead.

## Pitfalls

- **Linear algebra modulo a composite.** Gaussian elimination modulo $p - 1$ fails on non-invertible pivots. The right lines are L8 and L9: solve modulo each prime power with unit pivots and combine by the Chinese remainder theorem.
- **Powers of the subgroup generator only.** Taking relations from $g^k$ with $g$ of small order $n$ samples only $n$ elements, and few or none are smooth; the primes of $S$ are usually not in $\langle g \rangle$ at all. Line L6 uses a generator $\gamma$ of the whole group, or $g^k \delta$ with $\delta$ random in a complementary subgroup, as in Galbraith.
- **Too few relations.** With exactly $|S|$ relations the system is often singular modulo some $q$. Line L8 waits for $|S| + 10$ and line L9 checks for a unit pivot in every column, collecting more relations if one is missing.
- **Ignoring the conversion.** The logarithms of lines L10 to L12 are to base $\gamma$. Returning $L(h)$ instead of line L14's $(L(h)/c)u^{-1} \bmod n$ answers a different question.
- **No membership test.** Without line L1, a target outside $\langle g \rangle$ still gets a value $L(h)$, but $L(h)/c$ is not an integer. Line L1 must come first.
- **A factor base that is too large or too small.** Too small a $B$ makes smooth values rare, and too large a $B$ makes the system huge; $B$ near $L_p(1/2, 1/2)$ balances them for trial division.

## Implementations

## History

The ideas go back to Kraitchik around 1922 and to Cunningham, as reported by McCurley and by Western and Miller's 1968 tables of indices, and were rediscovered several times (HAC, Section 3.12). Adleman described the method for $(\mathbb{Z}/p\mathbb{Z})^*$ in 1979 and analysed its subexponential running time, and Hellman and Reyneri gave the first version for extension fields of small characteristic. Blake, Fuji-Hara, Mullin and Vanstone computed logarithms in $\mathbb{F}_{2^{127}}$, and Coppersmith's algorithm of 1984 reached $L(1/3)$ there. Coppersmith, Odlyzko and Schroeppel's 1986 paper gave three methods with heuristic time $L_p(1/2, 1)$, and Pomerance proved $L_p(1/2, \sqrt 2)$ in 1987. Gordon adapted the number field sieve in 1993, and Schirokauer improved the constant to $(64/9)^{1/3}$.

## References
