---
tag: 70W13Q
kind: algorithm
slug: babai-nearest-plane
name: Babai nearest plane algorithm
aliases:
- nearest plane algorithm
- Babai's nearest plane method
- size reduction of the target
area: number-theory/lattice-reduction
level: advanced
summary: Successively projects onto Gram-Schmidt hyperplanes to find a nearby lattice vector.
solves: [closest-vector-problem, bounded-distance-decoding]
model: word-ram
complexity:
  vars: {n: the rank of the lattice, m: the length of the vectors (m >= n), β: the largest binary length of an integer entry of the basis or the target}
  time: {worst: O(n^2 m), best: O(n^2 m), per_target: O(n m)}
  space: {extra: O(n m)}
  bit_operations: {worst: O(n^4 m (β + log m)^2)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1986
  people: [László Babai]
  note: Babai introduced the nearest plane procedure in his 1986 Combinatorica paper and proved the factor 2^(n/2) on LLL-reduced bases.
prereqs: [closest-vector-problem, gram-schmidt-orthogonalization, lattice]
see_also: [babai-rounding, bounded-distance-decoding, lll-algorithm, size-reduction, fincke-pohst-enumeration, gpv-signature, covering-radius, lattice-based-cryptography]
sources:
  - paper: "L. Babai, On Lovász' lattice reduction and the nearest lattice point problem, Combinatorica 6(1) (1986)"
    locator: pages 1 to 13 (the nearest plane procedure and the factor 2^(n/2) on LLL-reduced bases)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 18, Close and short vectors (Babai's nearest plane method, its analysis and examples)
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 2, Approximation algorithms (the nearest plane algorithm and its approximation factor)
  - paper: "C. Gentry, C. Peikert and V. Vaikuntanathan, Trapdoors for hard lattices and new cryptographic constructions, STOC 2008"
    locator: the randomized nearest plane algorithm, after Klein, as a discrete Gaussian sampler
---

Babai's nearest plane algorithm finds a [lattice](/lattice/) vector close to a target $t$. It works through the [Gram-Schmidt](/gram-schmidt-orthogonalization/) vectors of the basis from last to first: at each step it picks the translate of a hyperplane spanned by the earlier basis vectors that lies nearest to the current target, moves the target into it and continues inside. It returns the exact [closest vector](/closest-vector-problem/) whenever $t$ is within half the shortest Gram-Schmidt vector of the lattice, and on an [LLL](/lll-algorithm/)-reduced basis it is always within a factor $2^{n/2}$ of the optimum.

## In plain words

A grid of points is built from a few arrows. You are given a point and want a grid point near it.

The grid is made of parallel layers: every grid point sits on one of them. First choose the layer nearest to the given point and slide the point into that layer. Inside the layer the grid is one dimension smaller, again made of parallel layers, so choose the nearest of those and slide again. After one choice per arrow, the point has landed on a grid point.

Each choice is made as well as it can be at the time, but an early choice is never revisited, so the result is not always the nearest grid point. When the arrows have been tidied first, the result is provably not far off.

## The problem

**Input.** Linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$ of a matrix $B$, and a target $t \in \mathbb{Q}^m$.

**Output.** A vector $v \in L(B)$ close to $t$, together with its integer coefficients $x$, $v = x B$, such that the error has small Gram-Schmidt coordinates:

$$t - v = o + \sum_{i=1}^n c_i b_i^*, \qquad o \perp \operatorname{span}(L), \qquad -\tfrac12 \le c_i < \tfrac12.$$

**Notation and cost model.** As on the other pages of this area, basis vectors are rows $b_1, \ldots, b_n$, $b_i^*$ and $\mu_{ij}$ are the Gram-Schmidt data, $\lambda_1$ is the first minimum, $\det(L)$ is the determinant and $\delta$ is the LLL parameter. All arithmetic is exact, on integers or rationals. The time bound counts arithmetic operations; the bit bound counts operations on binary digits for integer input with entries of binary length at most $\beta$, with schoolbook multiplication. Every bound on this page is proved; the remarks on practice are marked as observed.

## The algorithm

```pseudo id=main
NEAREST-PLANE(B, t)                  ▷ independent rows b_1..b_n; returns (x, v) with v = x B
L1  compute b_1*, ..., b_n* and N_i = ‖b_i*‖²
L2  w ← t
L3  for i ← n down to 1
L4      x_i ← ⌈⟨w, b_i*⟩ / N_i⌋        ▷ nearest integer, halves rounded up
L5      w ← w − x_i b_i
L6  return (x, t − w)
```

The hyperplanes of the name are $\operatorname{span}(b_1, \ldots, b_{i-1}) + k b_i$ for integers $k$; they lie at distance $\|b_i^*\|$ from one another, and line L4 picks the $k$ nearest to $w$. The loop is exactly [size reduction](/size-reduction/) of $t$ against the basis.

## Example

The lattice with rows $(2, 0), (1, 2)$ and the target $t = (0.7, 2.3)$, the example of the [bounded distance decoding](/bounded-distance-decoding/) page. The closest lattice vector is $(1, 2)$, at squared distance $0.18$, and the promise radius there is $\tfrac12$.

Good basis $b_1 = (2, 0)$, $b_2 = (1, 2)$, with $b_1^* = (2, 0)$, $b_2^* = (0, 2)$, $N = (4, 4)$:

| Step | $i$ | $\langle w, b_i^* \rangle / N_i$ | $x_i$ | $w$ after L5 |
|------|-----|------|------|------|
| L2 | | | | $(0.7, 2.3)$ |
| L4, L5 | 2 | $4.6 / 4 = 1.15$ | 1 | $(-0.3, 0.3)$ |
| L4, L5 | 1 | $-0.6 / 4 = -0.15$ | 0 | $(-0.3, 0.3)$ |
| L6 | | | | $v = (1, 2)$, squared distance $0.18$ |

Bad basis $b_1 = (4, 4)$, $b_2 = (9, 10)$ of the same lattice, with $b_1^* = (4, 4)$, $b_2^* = (-\tfrac12, \tfrac12)$, $N = (32, \tfrac12)$:

| Step | $i$ | $\langle w, b_i^* \rangle / N_i$ | $x_i$ | $w$ after L5 |
|------|-----|------|------|------|
| L2 | | | | $(0.7, 2.3)$ |
| L4, L5 | 2 | $0.8 / 0.5 = 1.6$ | 2 | $(-17.3, -17.7)$ |
| L4, L5 | 1 | $-140 / 32 = -4.375$ | $-4$ | $(-1.3, -1.7)$ |
| L6 | | | | $v = (2, 4)$, squared distance $4.58$ |

The answer for the bad basis is about 5 times farther than optimal, but it is much better than [Babai rounding](/babai-rounding/) on the same basis, which returns $(6, 8)$ at squared distance $60.58$. The decoding radius $\tfrac12 \min_i \|b_i^*\|$ is $1$ for the good basis, so $t$ is decoded, and $\sqrt{0.5}/2 \approx 0.354$ for the bad one, below the actual distance $0.424$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Three facts carry it.

- **The output is in the lattice.** Every step subtracts an integer multiple of a basis vector from $t$.
- **The error is small along each $b_i^*$.** Line L4 makes the coordinate of $w$ along $b_i^*$ lie in $[-\tfrac12, \tfrac12)$, and the later steps subtract $b_j$ with $j < i$, which are orthogonal to $b_i^*$, so that coordinate never changes again.
- **A wrong step needs a large error.** If $u = z B$ is a closest vector and $k$ is the last index where the algorithm chose $x_k \ne z_k$, then up to step $k$ it followed $u$, and the coordinate it rounded was $z_k + \langle e, b_k^* \rangle / N_k$ with $e = t - u$; rounding away from $z_k$ needs $\|e\| \ge \tfrac12 \|b_k^*\|$.

From the last fact: if $\operatorname{dist}(t, L) < \tfrac12 \min_i \|b_i^*\|$, the output is the closest vector. In general $\|t - v\|^2 \le (1 + \max_k \sum_{i \le k} N_i / N_k) \operatorname{dist}(t, L)^2$. For a basis that is LLL-reduced with parameter $\delta$, $N_i \le \alpha^{k - i} N_k$ with $\alpha = 1/(\delta - 1/4)$, which gives

$$\|t - v\|^2 \le \Big(1 + \frac{\alpha^n - 1}{\alpha - 1}\Big) \operatorname{dist}(t, L)^2, \qquad \text{and } \|t - v\| \le 2^{n/2} \operatorname{dist}(t, L) \text{ for } \delta = 3/4.$$

## Complexity

- **Arithmetic operations.** Gram-Schmidt at line L1 costs $O(n^2 m)$. The loop costs $O(m)$ per index, $O(n m)$ in total. So the algorithm uses $O(n^2 m)$ operations in the best and the worst case, and $O(n m)$ per further target once the Gram-Schmidt data are stored, as when it runs after LLL, which computes them anyway.
- **Bit operations.** For integer input, the Gram-Schmidt data are quotients of integers with $O(n (\beta + \log m))$ digits, and so are the coefficients $x_i$, because $v$ is within $\|t\| + \tfrac12 \sum_i \|b_i\|$ of the origin and its coefficients are inner products with the dual basis. Each of the $O(n^2 m)$ operations is then on numbers of $O(n (\beta + \log m))$ digits, which gives $O(n^4 m (\beta + \log m)^2)$ bit operations.
- **Space.** $O(n m)$ numbers for the Gram-Schmidt vectors.
- **Floating point.** In practice the Gram-Schmidt coefficients are kept in floating point, as in floating-point LLL, and the target is reduced through the coefficients $\mu_{ij}$ rather than the vectors $b_i^*$. The analysis of floating-point size reduction in the $L^2$ algorithm of Nguyen and Stehlé bounds the precision this loop needs on LLL-reduced bases; in practice double precision usually suffices in moderate dimension, which is observed rather than proved.

## Properties

- **Deterministic and exact.** With exact arithmetic the output is a function of the basis and $t$.
- **Basis dependent.** The decoding region, the set of errors $t - v$ that are produced, is the box $\{\sum_i c_i b_i^* : -\tfrac12 \le c_i < \tfrac12\}$, a fundamental domain of the lattice of volume $\det(L)$. A basis with Gram-Schmidt lengths close to each other gives a nearly cubic box and good decoding.
- **Order dependent.** Reordering the basis changes the $b_i^*$ and the answer.
- **Translation invariant.** Adding a lattice vector $z B$ to $t$ adds $z$ to $x$.
- **Sequential.** Each step depends on the previous one, unlike rounding.

## Variants and improvements

- **[Babai rounding](/babai-rounding/).** Rounds all coordinates at once in the original basis; simpler and parallel, with the weaker proved factor $1 + 2n (9/2)^{n/2}$ on LLL-reduced bases.
- **Randomized nearest plane.** Klein (2000), and Gentry, Peikert and Vaikuntanathan (2008), replace the rounding at line L4 by sampling from a discrete Gaussian around the coordinate. The output is a discrete Gaussian sample on the coset of the lattice whose distribution does not depend on the basis, which is the signing step of [GPV signatures](/gpv-signature/) and Falcon.
- **Nearest planes (Lindner and Peikert, 2011).** Keeps several nearest hyperplanes at the top levels, trading time for a larger decoding region; used in attacks on LWE.
- **Enumeration.** Keeping all hyperplanes within a radius instead of the nearest one turns the algorithm into [Fincke-Pohst enumeration](/fincke-pohst-enumeration/) for exact CVP; Babai's answer gives a starting radius.
- **Embedding.** Kannan's embedding reduces CVP to SVP in one more dimension instead; it often beats nearest plane in cryptanalysis when the target is very close.

## When to use it

- After LLL or [BKZ](/bkz-algorithm/), whenever an approximate closest vector is needed in polynomial time, for example in [bounded distance decoding](/bounded-distance-decoding/) with a trapdoor basis.
- As the first step of exact CVP: its distance is a valid enumeration radius.
- In integer programming and integer least squares as a fast rounding heuristic (the Babai point of GPS and communications).
- Prefer rounding when the targets arrive in large batches on a very good basis and parallel speed matters more than the decoding radius.

## Pitfalls

- **Unreduced input.** On a skewed basis the last Gram-Schmidt vectors are tiny and the guarantee is useless; reduce first.
- **Rounding with $b_i$ instead of $b_i^*$.** Line L4 must project on the Gram-Schmidt vector $b_i^*$, while line L5 subtracts the basis vector $b_i$. Swapping the two gives a point that is not in the lattice or not near $t$.
- **Wrong order.** The loop must run from $n$ down to 1, so that later steps do not disturb the coordinates already fixed.
- **Target outside the span.** The component orthogonal to the span cannot be removed; the guarantee is about the projection, and $\|o\|^2$ adds to every distance.
- **Floating point.** Low precision Gram-Schmidt on a large basis can round a coordinate the wrong way; use exact or carefully analysed arithmetic when the answer must be correct.

## Implementations

## History

László Babai introduced the nearest plane procedure, together with rounding, in a 1986 paper in Combinatorica, as a way to use the new LLL algorithm for the nearest lattice point problem; he proved the factor $2^{n/2}$ on LLL-reduced bases. The same loop is the size reduction step inside LLL. Klein made it randomized in 2000 for bounded distance decoding, and Gentry, Peikert and Vaikuntanathan turned the randomized version into a trapdoor sampler in 2008, the basis of hash-and-sign lattice signatures such as Falcon.

## References
