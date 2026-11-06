---
tag: 24ANYQ
kind: algorithm
slug: babai-rounding
name: Babai rounding
aliases:
- Babai's round-off algorithm
- Babai's rounding technique
- round-off decoding
area: number-theory/lattice-reduction
level: advanced
summary: Rounds the target in the coordinates of a reduced basis to get an approximate closest vector.
solves: [closest-vector-problem]
model: word-ram
complexity:
  vars: {n: the rank of the lattice, m: the length of the vectors, β: the largest binary length of an integer entry of the basis or the target}
  time: {worst: O(n^2 m + n^3), best: O(n^2 m + n^3), per_target: O(n m)}
  space: {extra: O(n^2 + n m)}
  bit_operations: {worst: O(n^2 m (β + log m)^2 + n^5 (β + log(n m))^2)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1986
  people: [László Babai]
  note: Babai analysed rounding and the nearest plane method on LLL-reduced bases in his 1986 Combinatorica paper; rounding with a private good basis is the decryption step of the GGH cryptosystem of 1997.
prereqs: [lattice, closest-vector-problem, dual-lattice]
see_also: [babai-nearest-plane, bounded-distance-decoding, lll-algorithm, gram-schmidt-orthogonalization, lattice-based-cryptography, learning-with-errors, fincke-pohst-enumeration, covering-radius]
sources:
  - paper: "L. Babai, On Lovász' lattice reduction and the nearest lattice point problem, Combinatorica 6(1) (1986)"
    locator: pages 1 to 13 (the rounding-off and nearest plane procedures and their approximation factors on LLL-reduced bases)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 18, Close and short vectors (Babai's rounding technique, with examples and its comparison with the nearest plane method)
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 2, Approximation algorithms (Babai's algorithms for the closest vector problem)
  - paper: "O. Goldreich, S. Goldwasser and S. Halevi, Public-key cryptosystems from lattice reduction problems, CRYPTO 1997, LNCS 1294"
    locator: decryption by rounding in the coordinates of the private basis
---

Babai rounding is the simplest approximation algorithm for the [closest vector problem](/closest-vector-problem/). It writes the target $t$ in the coordinates of a basis $b_1, \ldots, b_n$ of the [lattice](/lattice/), rounds each coordinate to the nearest integer, and returns the lattice vector with those integer coordinates. On a nearly orthogonal basis the answer is close to optimal and is exactly right when $t$ is near the lattice; on a skewed basis it can be far off, which is why it is run after [LLL](/lll-algorithm/) or a stronger reduction.

## In plain words

A grid of points is built from a few arrows. You are given a point and want the grid point nearest to it.

Ask how many copies of each arrow it takes to reach the point. The answers are usually not whole numbers, such as 2.7 copies of the first arrow and minus 1.2 of the second. Round each answer to the nearest whole number, 3 and minus 1, and walk that many copies of each arrow. You land on a grid point near the given one.

How near depends on the arrows. When they are short and close to square with one another, rounding loses little and the point is often the nearest one. When they are long and almost parallel, a small rounding step can move you very far, so the arrows are tidied first.

## The problem

**Input.** Linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$ of a matrix $B$, and a target $t \in \mathbb{Q}^m$.

**Output.** A vector $v \in L(B)$ close to $t$, together with its integer coefficients $x$, $v = x B$.

**Notation and cost model.** As on the other pages of this area, basis vectors are rows $b_1, \ldots, b_n$, $b_i^*$ and $\mu_{ij}$ are the [Gram-Schmidt](/gram-schmidt-orthogonalization/) data, $\lambda_1$ is the first minimum, $\det(L)$ is the determinant and $\delta$ is the LLL parameter. The rows $d_1, \ldots, d_n$ of $D = (B B^T)^{-1} B$ form the [dual basis](/dual-lattice/), with $\langle b_i, d_j \rangle = [i = j]$. All arithmetic is exact, on integers or rationals. The time bound counts arithmetic operations; the bit bound counts operations on binary digits for integer input with entries of binary length at most $\beta$. Every bound below is proved; the quality on random or reduced bases in practice is noted separately as observed.

## The algorithm

```pseudo id=main
BABAI-ROUNDING(B, t)                ▷ independent rows b_1..b_n; returns (x, v) with v = x B
L1  G ← B Bᵀ                          ▷ Gram matrix, G[i][j] = ⟨b_i, b_j⟩
L2  y ← the solution of G y = B t     ▷ y_i = ⟨t, d_i⟩
L3  x_i ← ⌈y_i⌋ for i = 1..n          ▷ nearest integer, halves rounded up
L4  v ← x_1 b_1 + ... + x_n b_n
L5  return (x, v)
```

When $t$ lies in the span and $n = m$, line L2 is simply $y = t B^{-1}$. The Gram form also handles $n < m$, where it uses the projection of $t$ onto the span.

## Example

The [lattice](/lattice/) with rows $(2, 0), (1, 2)$ and the target $t = (0.7, 2.3)$, the example of the [bounded distance decoding](/bounded-distance-decoding/) page. The closest lattice vector is $(1, 2)$, at squared distance $0.18$.

| Step | Good basis $(2, 0), (1, 2)$ | Bad basis $(4, 4), (9, 10)$ |
|------|------|------|
| L1 | $G = \begin{pmatrix} 4 & 2 \\ 2 & 5 \end{pmatrix}$ | $G = \begin{pmatrix} 32 & 76 \\ 76 & 181 \end{pmatrix}$ |
| L2 | $B t = (1.4, 5.3)$, $y = (-0.225, 1.15)$ | $B t = (12, 29.3)$, $y = (-3.425, 1.6)$ |
| L3 | $x = (0, 1)$ | $x = (-3, 2)$ |
| L4 | $v = (1, 2)$ | $v = (6, 8)$ |
| L5 | squared distance $0.18$, optimal | squared distance $60.58$ |

The two bases generate the same lattice: $(1, 2) = -2 \cdot (4, 4) + 1 \cdot (9, 10)$, so in the bad basis the right answer has coefficients $(-2, 1)$. The error $e = t - (1, 2) = (-0.3, 0.3)$ shifts the coordinates by $\langle e, d_i \rangle$. For the good basis the dual rows are $(0.5, -0.25)$ and $(0, 0.5)$, the shifts are $-0.225$ and $0.15$, both below $1/2$, and rounding removes them. For the bad basis the dual rows are $(2.5, -2.25)$ and $(-1, 1)$, the shifts are $-1.425$ and $0.6$, and rounding lands on the wrong point, more than 7 units away.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Line L2 computes $y_i = \langle t, d_i \rangle$, and $\sum y_i b_i$ is the projection of $t$ onto the span. Line L3 makes the coefficients integers, so $v$ is in the lattice.

If $t = u + e$ with $u = z B \in L$, then $y_i = z_i + \langle e, d_i \rangle$. So rounding returns $u$ exactly whenever $|\langle e, d_i \rangle| < 1/2$ for every $i$, in particular whenever $\|e\| < 1/(2 \max_i \|d_i\|)$. For a closest vector $u$, the same identity and $|\lceil \varepsilon \rfloor| \le 2 |\varepsilon|$ give

$$\|t - v\| \le \Big(1 + 2 \sum_i \|b_i\| \|d_i\|\Big) \operatorname{dist}(t, L).$$

## Complexity

- **Arithmetic operations.** $O(n^2 m)$ for the Gram matrix, $O(n m + n^3)$ for the solve, and $O(n m)$ for the rounding and the combination, so $O(n^2 m + n^3)$ in total, in the best and the worst case alike. With $D$ precomputed, each further target costs $O(n m)$, the `per_target` bound above: $y = D t$, round, multiply.
- **Bit operations.** For integer $B$ and $t$ with entries of $\beta$ binary digits, the Gram entries have $O(\beta + \log m)$ digits. Fraction-free elimination keeps every intermediate value a minor of the augmented Gram matrix, of $O(n (\beta + \log(n m)))$ digits by Hadamard's inequality, which gives the bound $O(n^2 m (\beta + \log m)^2 + n^5 (\beta + \log(n m))^2)$ with schoolbook multiplication. The reference implementation uses Python fractions instead, which also stays polynomial.
- **Space.** $O(n^2 + n m)$ numbers for $G$ and the elimination, or for the stored dual basis.
- **Floating point.** In practice $D$ is computed once in floating point, and the rounding is correct as long as each $y_i$ is computed to within the distance from $y_i$ to the nearest half-integer. This is an observed practice with problem-specific error analysis, not a general proved bound.

## Properties

- **Deterministic and exact.** With exact arithmetic the output is a function of $B$ and $t$; ties $y_i \in \mathbb{Z} + 1/2$ are rounded up here.
- **Basis dependent.** Different bases of the same lattice give different answers, as in the example. The decoding region, the set of errors that are corrected, is the parallelepiped $\{e : |\langle e, d_i \rangle| < 1/2\}$, a fundamental domain spanned by the basis vectors and centred at 0.
- **Coordinatewise.** The $n$ roundings are independent, so the method parallelizes perfectly and is easy to vectorize.
- **Translation invariant.** Adding a lattice vector $w$ to $t$ adds $w$ to the output, since $\lceil k + z \rfloor = k + \lceil z \rfloor$.
- **Exact for orthogonal bases.** If the $b_i$ are pairwise orthogonal, the distance splits into independent coordinates and rounding returns a closest vector.

## Variants and improvements

- **Nearest plane.** [Babai's nearest plane method](/babai-nearest-plane/) rounds one coordinate at a time along the Gram-Schmidt vectors and updates the target. Its decoding region is the rectangular box spanned by the $b_i^*$, of the same volume $\det(L)$ as the parallelepiped of rounding, and it has the better proved factor $2^{n/2}$ on LLL-reduced bases.
- **Precomputed dual.** For many targets on one lattice, store $D$ or $B^{-1}$, so each target costs one matrix-vector product and $n$ roundings.
- **Randomized rounding.** Peikert's discrete Gaussian sampler (2010) rounds each coordinate randomly around $y_i$, and Klein's sampler does the same inside nearest plane. When the width is large enough the output distribution does not depend on the basis, which is what hash-and-sign signatures need.
- **Rounding in structured lattices.** In Ring-LWE decryption the lattice is an ideal of a ring of integers, and rounding is done coefficientwise in a suitable basis of the ring, with the changes of basis done by fast transforms.
- **Rounding after reduction.** LLL, [BKZ](/bkz-algorithm/) or an HKZ basis make $\sum_i \|b_i\| \|d_i\|$ smaller and enlarge the decoding region; Babai proved the factor $1 + 2n (9/2)^{n/2}$ on LLL-reduced bases with $\delta = 3/4$.

## When to use it

- When the basis is known to be good, such as a trapdoor basis in decryption, or a nearly orthogonal basis after reduction, and speed per target matters.
- When many targets share one lattice, so the dual basis can be precomputed.
- As a first guess for exact methods: the distance from rounding is a valid radius for [Fincke-Pohst enumeration](/fincke-pohst-enumeration/).
- Not as the only step on a raw or skewed basis: reduce first, and prefer nearest plane when its sequential cost is acceptable.

## Pitfalls

- **Skipping reduction.** On the bad basis of the example the answer is about 18 times farther than optimal. The quality depends entirely on the basis.
- **Solving with the wrong matrix.** For $n < m$ the system $y B = t$ has no solution when $t$ is outside the span; solve the Gram system $G y = B t$, which projects first.
- **Floating point.** Computing $B^{-1}$ in low precision for a badly conditioned basis rounds coordinates to the wrong integer even when the exact answer would be right.
- **Ties.** A coordinate exactly halfway between integers can go either way; the guarantees hold for either choice, but tests must fix one.
- **Dependent rows.** A generating set that is not a basis has a singular Gram matrix; reduce it to a basis first.

## Implementations

## History

László Babai introduced the rounding-off procedure and the nearest plane procedure in a 1986 paper in Combinatorica, as polynomial-time approximations to the nearest lattice point problem on top of the LLL algorithm of 1982. He proved approximation factors of $1 + 2n (9/2)^{n/2}$ for rounding and $2^{n/2}$ for nearest plane on LLL-reduced bases. In 1997 Goldreich, Goldwasser and Halevi built a public-key cryptosystem whose decryption is rounding with a secret good basis and whose public key is a bad basis; Nguyen broke the proposed parameters in 1999. Rounding remains the decryption step of many lattice schemes and the reference against which nearest plane and enumeration are compared.

## References
