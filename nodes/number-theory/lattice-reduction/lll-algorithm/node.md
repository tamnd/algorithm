---
tag: 82SX9W
kind: algorithm
slug: lll-algorithm
name: LLL algorithm
aliases:
- Lenstra-Lenstra-Lovász algorithm
- LLL
- LLL lattice basis reduction
area: number-theory/lattice-reduction
level: advanced
summary: Polynomial-time basis reduction giving a 2^((n-1)/2)-approximate shortest vector.
solves: [lattice-basis-reduction, approximate-svp]
model: word-ram
complexity:
  vars: {n: the rank of the lattice, m: the length of the basis vectors with m at least n, X: the largest squared length of an input vector of an integer basis, M: the cost M(k) of multiplying two integers of k binary digits}
  time: {worst: O(n^3 m log X), best: O(n^2 m)}
  space: {extra: O(n^2 + n m)}
  bit_operations: {worst: O(n^5 m (log X)^3), refined: O(n^3 m log X M(n log X))}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1982
  people: [Arjen K. Lenstra, Hendrik W. Lenstra Jr., László Lovász]
  note: Published in Mathematische Annalen as the basis reduction step of the first polynomial-time algorithm to factor polynomials with rational coefficients.
prereqs: [lattice-basis, gram-schmidt-orthogonalization, size-reduction, lovasz-condition, lll-reduction]
see_also: [lll-approximation-guarantee, lagrange-gauss-reduction, deep-lll, bkz-algorithm, babai-nearest-plane, root-hermite-factor, polynomial-factorization-over-integers, coppersmith-method]
sources:
  - paper: doi:10.1007/BF01457454
    title: A. K. Lenstra, H. W. Lenstra Jr. and L. Lovász, Factoring polynomials with rational coefficients, Mathematische Annalen 261, 1982
    locator: Section 1 (the reduction algorithm, the proof of termination with the quantity D, and the bounds on the number of operations and on the sizes of the integers)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Springer, Graduate Texts in Mathematics 138, 1993
    locator: Section 2.6 (the LLL algorithm with the swap update of the Gram-Schmidt coefficients, its integral version and the version for generating sets)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 16, Short vectors in lattices (basis reduction, its cost analysis and the application to factoring)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Section 17.4, the LLL algorithm (the algorithm, its correctness and its complexity)
  - paper: "Phong Q. Nguyen and Damien Stehlé, An LLL algorithm with quadratic complexity, SIAM Journal on Computing 39(3), 2009"
    locator: pages 874 to 903 (the L2 algorithm with floating point Gram-Schmidt and its bit complexity)
  - paper: "C. P. Schnorr and M. Euchner, Lattice basis reduction: improved practical algorithms and solving subset sum problems, Mathematical Programming 66, 1994"
    locator: pages 181 to 199 (LLL with floating point arithmetic and with deep insertions)
---

The LLL algorithm turns any basis of a [lattice](/lattice/) into an [LLL-reduced basis](/lll-reduction/) of the same lattice in polynomial time. It alternates [size reduction](/size-reduction/) with swaps of neighbouring vectors where the [Lovász condition](/lovasz-condition/) fails, and each swap lowers an integer quantity by a constant factor, so it stops after polynomially many steps. The first output vector is at most $2^{(n-1)/2}$ times longer than a shortest nonzero vector for the classical parameter $\delta = 3/4$, and in practice it is much better. It was the first polynomial-time algorithm with an approximation guarantee for lattices, and it is the work horse behind polynomial factorization, knapsack attacks, [Coppersmith's method](/coppersmith-method/) and integer relation finding.

## In plain words

A lattice can be given by long, nearly parallel vectors that hide its short vectors. LLL makes the vectors short and nearly perpendicular, step by step, from the first to the last.

It walks along the list. At each position it first trims the current vector by subtracting whole copies of the earlier vectors. Then it checks whether the current vector, after removing its parts along the vectors before the previous one, is much shorter than the previous vector seen in the same way. If so, the two are in the wrong order: it swaps them and steps back one position. If not, it moves forward.

Each swap makes a certain whole number smaller by a fixed factor. A whole number cannot shrink forever, so the walk ends, and it ends quickly.

## The problem

**Input.** Linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$, the basis of a lattice $L$, and a parameter $\delta$ with $1/4 < \delta < 1$.

**Output.** A basis of $L$ that is **$\delta$-LLL-reduced**: with $B_i = \|b_i^*\|^2$,

1. $|\mu_{ij}| \le \frac12$ for all $1 \le j < i \le n$, and
2. $\delta B_{k-1} \le B_k + \mu_{k,k-1}^2 B_{k-1}$ for all $2 \le k \le n$.

With $\alpha = 1 / (\delta - \frac14)$, such a basis has $\|b_1\| \le \alpha^{(n-1)/2} \lambda_1(L)$ and $\|b_1\| \le \alpha^{(n-1)/4} \det(L)^{1/n}$; see the [LLL approximation guarantee](/lll-approximation-guarantee/). For $\delta = 3/4$, $\alpha = 2$.

**Notation and cost model.** As on all pages of this area: basis rows $b_1, \ldots, b_n$, [Gram-Schmidt](/gram-schmidt-orthogonalization/) vectors $b_i^*$, coefficients $\mu_{ij}$, first minimum $\lambda_1$, determinant $\det(L)$ and parameter $\delta$. The algorithm below uses exact rational arithmetic. Time bounds count arithmetic operations on rationals; bit bounds count operations on binary digits for an integer basis whose squared row lengths are at most $X$. $n$ is the rank, $m \ge n$ the length of the rows, and $\delta < 1$ is a fixed constant.

## The algorithm

```pseudo id=main
LLL(b_1..b_n, δ)                       ▷ independent rows, 1/4 < δ < 1
L1  compute b_i*, B_i = ‖b_i*‖², μ_ij for all j < i
L2  k ← 2
L3  while k ≤ n do
L4      REDUCE(k, k − 1)                ▷ make |μ_k,k−1| ≤ 1/2
L5      if δ · B_k−1 > B_k + μ_k,k−1² · B_k−1 then
L6          swap b_k−1 and b_k; update B_k−1, B_k and μ
L7          k ← max(2, k − 1)
L8      else
L9          for j = k − 2 down to 1 do REDUCE(k, j)
L10         k ← k + 1
L11 return b_1..b_n

REDUCE(k, j):  q ← ⌈μ_kj⌋;  b_k ← b_k − q b_j;  μ_ki ← μ_ki − q μ_ji for i < j;  μ_kj ← μ_kj − q
```

Line L1 runs [Gram-Schmidt](/gram-schmidt-orthogonalization/) once. REDUCE is one round of [size reduction](/size-reduction/); it changes $b_k$ and row $k$ of $\mu$ but no $b_i^*$. Line L4 reduces only $\mu_{k,k-1}$, because the Lovász test of line L5 depends on no other coefficient, and the rest of the size reduction (line L9) is done only when $b_k$ stays at position $k$.

The swap of line L6 changes only $b_{k-1}^*$ and $b_k^*$. With $\mu = \mu_{k,k-1}$ and $B = B_k + \mu^2 B_{k-1}$, the new values are

$$B_{k-1}' = B, \qquad \mu_{k,k-1}' = \frac{\mu B_{k-1}}{B}, \qquad B_k' = \frac{B_{k-1} B_k}{B},$$

the rows $\mu_{k-1,j}$ and $\mu_{k,j}$ for $j < k - 1$ are exchanged, and for every $i > k$, with $t = \mu_{i,k}$,

$$\mu_{i,k}' = \mu_{i,k-1} - \mu t, \qquad \mu_{i,k-1}' = t + \mu_{k,k-1}' \mu_{i,k}'.$$

These formulas are derived in the proof. They cost $O(n)$ operations, so the Gram-Schmidt data never need to be recomputed.

## Example

Reduce $b_1 = (1, 1, 1)$, $b_2 = (-1, 0, 2)$, $b_3 = (3, 5, 6)$ with $\delta = 3/4$. The lattice has $\det(L) = 3$, and at the start $B = (3, 14/3, 9/14)$. Halves are rounded up.

| step | $k$ | after line L4 | $B_{k-1}, B_k$ | $\mu_{k,k-1}$ | test of line L5 | action |
|---|---|---|---|---|---|---|
| 1 | 2 | nothing to do | $3, 14/3$ | $1/3$ | $9/4 \le 14/3 + 1/3$ | pass, $k = 3$ |
| 2 | 3 | $b_3 = (4, 5, 4)$ | $14/3, 9/14$ | $-1/14$ | $7/2 > 2/3$ | swap $b_2, b_3$, $k = 2$ |
| 3 | 2 | $b_2 = (4, 5, 4) - 4 b_1 = (0, 1, 0)$ | $3, 2/3$ | $1/3$ | $9/4 > 1$ | swap $b_1, b_2$, $k = 2$ |
| 4 | 2 | $b_2 = (1, 1, 1) - b_1 = (1, 0, 1)$ | $1, 2$ | $0$ | $3/4 \le 2$ | pass, $k = 3$ |
| 5 | 3 | $b_3 = (-1, 0, 2) - b_2 = (-2, 0, 1)$ | $2, 9/2$ | $-1/2$ | $3/2 \le 9/2 + 1/2$ | pass, $k = 4$ |

In step 5, line L9 finds $\mu_{31} = 0$ and does nothing. The output is $(0, 1, 0), (1, 0, 1), (-2, 0, 1)$, with $B = (1, 2, 9/2)$ and $\prod_i B_i = 9 = \det(L)^2$, as before. The first vector has length $1 = \lambda_1$. The potential $D = B_1 \cdot B_1 B_2$ of the proof goes $42, 6, 2$: the first swap divides it by 7, the second by 3, both more than the guaranteed factor $1/\delta = 4/3$.

## Correctness

The steps of lines L4, L6 and L9 are unimodular row operations, so the rows stay a basis of $L$. The update formulas of line L6 keep $B$ and $\mu$ equal to the Gram-Schmidt data of the current rows. The loop keeps the **invariant**: when line L3 is reached, the rows $b_1, \ldots, b_{k-1}$ form a $\delta$-LLL-reduced basis of the lattice they generate. It holds for $k = 2$. A pass (lines L9 and L10) makes $b_k$ fully size-reduced, and line L5 has checked the Lovász condition at $k$, so the invariant holds for $k + 1$; the rows before $k$ did not change. A swap changes only positions $k - 1$ and $k$, so $b_1, \ldots, b_{k-2}$ still satisfy it, which is the invariant for the new $k = \max(2, k - 1)$. When the loop exits, $k = n + 1$, and the whole basis is reduced. Termination follows from the potential argument below. The [full proof](proofs/correctness.md) has the derivation of the swap formulas and all details.

## Complexity

**Termination and the number of swaps (proved).** Let $d_i = \prod_{j \le i} B_j$, the Gram determinant of $b_1, \ldots, b_i$, and $D = \prod_{i=1}^{n-1} d_i$. Size reduction does not change any $B_j$. A swap at $k$ changes only $d_{k-1}$, and multiplies it by $B_{k-1}' / B_{k-1} < \delta$. For an integer basis every $d_i$ is a positive integer, so $D \ge 1$ always, while at the start $D \le X^{n(n-1)/2}$. So the number of swaps is at most

$$s \le \frac{n (n - 1)}{2} \cdot \frac{\log X}{\log (1 / \delta)} = O(n^2 \log X).$$

For rational input, multiply the basis by a common denominator: the algorithm makes the same choices on the scaled basis, since the test of line L5 is homogeneous. A pass increases $k$ by 1 and a swap decreases it by at most 1, so there are at most $n - 1 + s$ passes and $n - 1 + 2s$ loop iterations.

**Arithmetic operations (proved).** Line L1 costs $O(n^2 m)$. One iteration costs $O(m + n)$ for lines L4 to L7 and $O(n (m + n))$ for line L9, so $O(n m)$ as $m \ge n$. The total is $O(n^2 m + (n + s) n m) = O(n^3 m \log X)$ for fixed $\delta$. For an input that is already reduced there is no swap and the cost is $O(n^2 m)$.

**Bit operations (proved).** Lenstra, Lenstra and Lovász show that during the algorithm all the integers $d_i$, $d_j \mu_{ij}$ and the entries of $b_i$ have $O(n \log X)$ binary digits: the $d_i$ only decrease, $B_i \ge 1 / d_{i-1}$, and size reduction keeps $\|b_i\|$ bounded. With schoolbook arithmetic on numbers of that size this gives $O(n^3 m \log X \cdot n^2 \log^2 X) = O(n^5 m \log^3 X)$, or $O(n^3 m \log X \cdot M(n \log X))$ with fast multiplication, where we count the cost of the operations on $O(n \log X)$-digit numbers. With rationals kept in lowest terms, as in the implementation here, numerators and denominators have the same sizes, and each gcd costs $O(n^2 \log^2 X)$ bit operations with the [Euclidean algorithm](/euclidean-algorithm/), so the schoolbook bound does not change.

**Floating point (proved, different algorithm).** The L² algorithm of Nguyen and Stehlé keeps the Gram-Schmidt data in floating point with $O(n)$ digits of precision and proves the bit cost $O(n^2 m (n + \log X) \log X \cdot M(n))$ for the same output with a relaxed size reduction; see Variants.

**Observed in practice (heuristic).** On random inputs the number of swaps is usually far below the bound, and the output satisfies $\|b_1\| \approx 1.02^n \det(L)^{1/n}$ rather than the proved $1.075^n$; see [root Hermite factor](/root-hermite-factor/).

**Space.** The basis and the $n \times n$ table $\mu$, $O(n^2 + n m)$ numbers.

## Properties

- **Exact and deterministic.** The version above uses exact rationals, so the output is a $\delta$-LLL-reduced basis with no rounding error.
- **The same lattice.** Each step is a unimodular change of basis; the product of all of them is the transformation matrix, which can be tracked in the same loop.
- **Output depends on the input basis.** Two bases of the same lattice can give different reduced bases; an LLL-reduced basis is not unique.
- **Invariant under scaling and isometries.** Multiplying the basis by a constant or applying an orthogonal map does not change the steps, because everything depends on the Gram matrix.
- **Guarantees.** $\|b_1\| \le \alpha^{(n-1)/2} \lambda_1$, $\|b_i\| \le \alpha^{(n-1)/2} \lambda_i$ and $\prod_i \|b_i\| \le \alpha^{n(n-1)/4} \det(L)$, proved on the [LLL approximation guarantee](/lll-approximation-guarantee/) page.

## Variants and improvements

- **Integral LLL.** Keep the integers $d_i$ and $d_j \mu_{ij}$ instead of rationals; all divisions are exact. This avoids gcds and is the version usually given in computer algebra texts, for example in Cohen.
- **Floating point LLL.** Schnorr and Euchner computed the Gram-Schmidt data in floating point with exact basis vectors, which is much faster but was not proved correct in general. Nguyen and Stehlé's L² chooses a precision of $O(n)$ digits that provably suffices, with the relaxed conditions $|\mu_{ij}| \le \eta$ for $\eta > 1/2$.
- **Generating sets.** The MLLL variant accepts linearly dependent vectors and outputs a basis of the lattice they generate followed by zero vectors.
- **[Deep insertions](/deep-lll/).** Insert $b_k$ at the earliest position $i$ where it would shorten $b_i^*$, not only at $k - 1$. Better output in practice; no polynomial bound is known in general.
- **[BKZ](/bkz-algorithm/).** Replace the 2-dimensional step by an exact SVP in blocks of size $\beta$, which gives a better approximation factor at a cost exponential in $\beta$.
- **Faster LLL-type algorithms.** Recursive and block-oriented methods reduce the dependence on $\log X$, at the cost of slightly weaker output conditions.

## When to use it

Use LLL whenever a reasonably short vector or a reasonably good basis is enough: finding small roots in [Coppersmith's method](/coppersmith-method/), factoring [polynomials over the integers](/polynomial-factorization-over-integers/), attacking knapsack schemes such as [Merkle-Hellman](/merkle-hellman-knapsack/), [integer relation](/integer-relation-problem/) detection, simultaneous Diophantine approximation and [integer programming in fixed dimension](/integer-programming-fixed-dimension/). Use it as preprocessing before enumeration or BKZ. When the shortest vector itself is needed, follow LLL by [enumeration](/schnorr-euchner-enumeration/); in dimension 2, [Lagrange-Gauss reduction](/lagrange-gauss-reduction/) is exact and simpler. For large dimensions or large numbers, use a floating point implementation such as L², not exact rationals.

## Pitfalls

- **$\delta = 1$.** The potential then need not drop by a constant factor per swap, and no polynomial bound on the number of swaps is known. Use $\delta < 1$, for example $\delta = 0.99$.
- **Plain floating point.** Computing $\mu$ in double precision with no control of the error can make the algorithm loop forever or return a basis that is not reduced, already for moderate dimensions or entries. Use exact arithmetic or a proved precision.
- **Recomputing Gram-Schmidt after each step.** It is correct but costs $O(n^2 m)$ per iteration instead of $O(n m)$; use the update formulas of line L6.
- **Skipping line L9.** Without the full size reduction, the output satisfies the Lovász condition but not $|\mu_{ij}| \le 1/2$, and the bounds on $\|b_i\|$ fail.
- **Going back to $k = 1$.** After a swap at $k = 2$, $k$ must stay 2; there is no condition at $k = 1$.
- **Dependent input.** Some $B_i$ is 0 and the test divides by it. Check independence first, or use the MLLL variant.
- **Reading $\|b_1\|$ as $\lambda_1$.** The output is an approximation. In small dimension it is often a shortest vector, but this is not guaranteed.

## Implementations

## History

Arjen Lenstra, Hendrik Lenstra and László Lovász published the algorithm in 1982 as the core of a polynomial-time algorithm to factor polynomials with rational coefficients. The basis reduction step is usually credited to Lovász; its condition with the parameter $3/4$ relaxes Hermite's and Minkowski's classical reductions just enough to make the algorithm polynomial. Applications followed at once: H. W. Lenstra's integer programming in fixed dimension (1983), the attacks on knapsack cryptosystems by Lagarias and Odlyzko and others (1985), and later Coppersmith's small roots method (1996). Schnorr and Euchner made it practical with floating point arithmetic and deep insertions (1994), and Nguyen and Stehlé gave the first floating point version with a proved quadratic dependence on $\log X$ (2005, journal 2009).

## References
