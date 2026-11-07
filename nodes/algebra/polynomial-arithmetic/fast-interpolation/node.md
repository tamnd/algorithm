---
tag: 2CT8SN
kind: algorithm
slug: fast-interpolation
name: Fast polynomial interpolation
aliases:
- subproduct-tree interpolation
- fast Lagrange interpolation
area: algebra/polynomial-arithmetic
level: advanced
summary: Interpolates at n points in O(M(n) log n) using the subproduct tree and the transposed multipoint evaluation.
solves: [polynomial-interpolation]
model: blum-shub-smale-machine
complexity:
  vars: {n: the number of points, M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {worst: O(M(n) log n), best: O(M(n) log n)}
  space: {extra: O(n log n)}
  ring_operations: {worst: 19M(n)(log2 n + 1) + O(n log n)}
properties: {deterministic: true, in_place: false, recursive: false, online: false}
history:
  year: 1972
  people: [Robert T. Moenck, Allan Borodin]
  note: Fast interpolation in O(M(n) log n) followed from fast multipoint evaluation and fast division in the work of Moenck and Borodin, Kung, and Strassen in the early 1970s.
prereqs: [fast-multipoint-evaluation, multipoint-evaluation, point-value-representation]
see_also: [subproduct-tree, polynomial-interpolation, lagrange-interpolation, chinese-remainder-theorem, evaluation-interpolation-paradigm, fast-polynomial-division, vandermonde-matrix, reed-solomon-decoding]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 10.2, Fast interpolation; Section 10.3, Fast Chinese remaindering; Section 5.2, Evaluation and interpolation (Lagrange interpolation)
  - paper: doi:10.1145/860854.860870
    title: Alin Bostan, Gregoire Lecerf and Eric Schost, Tellegen's principle into practice, Proceedings of ISSAC 2003, 37-44
    locator: interpolation by the transposed algorithms and its constant
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.4, Evaluation of polynomials (interpolation and Newton's divided differences)
---

Fast interpolation finds the polynomial $f$ of degree less than $n$ that takes given values $v_0, \ldots, v_{n-1}$ at given points $u_0, \ldots, u_{n-1}$, with $O(M(n) \log n)$ ring operations instead of the $\Theta(n^2)$ of Lagrange's or Newton's formula. It writes Lagrange's formula with the derivative of $m = \prod_i (x - u_i)$, computes the needed values $m'(u_i)$ by one [fast multipoint evaluation](/fast-multipoint-evaluation/), and then sums the weighted products $m/(x - u_i)$ by walking up the subproduct tree. The upward walk is the transpose of the remainder descent of multipoint evaluation.

Notation: $R$ is a commutative ring with $1$, a polynomial is the list of its coefficients with the constant term first, and $M(n)$ is the cost of multiplying two polynomials of degree less than $n$ over $R$. We assume that $M(k)/k$ is nondecreasing and that $M(2k) \le 4M(k)$. Costs count ring operations in the algebraic complexity model. All differences $u_i - u_j$ with $i \ne j$ must be units of $R$; in practice $R$ is a field.

## In plain words

You know the values of an unknown polynomial at some numbers, and you want its coefficients. A classical formula builds the answer as a sum of simple pieces, one for each number. Each piece is zero at all numbers but one, and has the right value at that one. Working out each piece on its own takes time that grows with the square of the number of points. The fast method shares the work. It first finds, for each number, the value that scales its piece; these values all come from one fast evaluation at all the numbers. Then it adds the pieces in pairs, the pairs in pairs, and so on, along the same tree of products that fast evaluation uses.

## The problem

**Input:** points $u_0, \ldots, u_{n-1} \in R$, with $u_i - u_j$ a unit for $i \ne j$, and values $v_0, \ldots, v_{n-1} \in R$.

**Output:** the unique $f \in R[x]$ with $\deg f < n$ and $f(u_i) = v_i$ for all $i$.

This is [polynomial interpolation](/polynomial-interpolation/). The solution exists and is unique: with $m = \prod_i (x - u_i)$, Lagrange's formula is

$$f = \sum_{i=0}^{n-1} \frac{v_i}{m'(u_i)} \cdot \frac{m}{x - u_i}, \qquad m'(u_i) = \prod_{j \ne i} (u_i - u_j),$$

and $m'(u_i)$ is a unit because each factor is. If $g$ is another solution, then $f - g$ has degree less than $n$ and vanishes at the $n$ points, so it is divisible by $m$, of degree $n$, and is $0$.

## The algorithm

The subproduct tree is the one of [fast multipoint evaluation](/fast-multipoint-evaluation/): the leaves at level $0$ are $x - u_i$, node $k$ of level $j + 1$ is the product of nodes $2k$ and $2k + 1$ of level $j$, a last node without a sibling is copied up, and the top level $h = \lceil \log_2 n \rceil$ holds $m$.

```pseudo id=main
FAST-INTERPOLATE(u_0, ..., u_{n−1}; v_0, ..., v_{n−1})
L1  if n = 0 then return 0
L2  build the subproduct tree; m ← its root
L3  (s_0, ..., s_{n−1}) ← FAST-MULTIPOINT-EVAL(m', u_0, ..., u_{n−1}) on the same tree
L4  c_i ← v_i · s_i^{−1} for each i                ▷ the Lagrange weights
L5  return LINEAR-COMBINATION(c, tree)              ▷ Σ c_i · m / (x − u_i)

LINEAR-COMBINATION(c, tree)
C1  r_{0,i} ← c_i for each leaf i
C2  for j ← 1 to h do
C3      for each node k of level j do
C4          if node k has two children then
C5              r_{j,k} ← r_{j−1,2k} · m_{j−1,2k+1} + r_{j−1,2k+1} · m_{j−1,2k}
C6          else r_{j,k} ← r_{j−1,2k}
C7  return r_{h,0}
```

Line C5 is the step that adds two halves of the Lagrange sum: if $r_{\text{left}} = \sum_{i \in L} c_i\, m_L/(x - u_i)$ and $r_{\text{right}}$ is the same for the right half, then multiplying each by the other half's product gives the sum over both halves with the common factor $m_L m_R$.

## Example

Interpolate the values $1, 0, 5, 22$ at the points $0, 1, 2, 3$ over $\mathbb{Q}$. These are the values of $x^3 - 2x + 1$, from the example of fast multipoint evaluation.

**Lines L2 and L3.** The tree has $x^2 - x$ and $x^2 - 5x + 6$ at level 1 and $m = x^4 - 6x^3 + 11x^2 - 6x$ at the top, so $m' = 4x^3 - 18x^2 + 22x - 6$. Its values at the points are $s = (-6, 2, -2, 6)$.

**Line L4.** $c = (1/(-6), 0/2, 5/(-2), 22/6) = (-1/6, 0, -5/2, 11/3)$.

**Lines C1 to C7.**

| level | nodes | partial sums |
|---|---|---|
| 0 | $x$, $x - 1$, $x - 2$, $x - 3$ | $-1/6$, $0$, $-5/2$, $11/3$ |
| 1 | $x^2 - x$, $x^2 - 5x + 6$ | $-\tfrac16 (x - 1) + 0 \cdot x = -\tfrac16 x + \tfrac16$, and $-\tfrac52 (x - 3) + \tfrac{11}{3} (x - 2) = \tfrac76 x + \tfrac16$ |
| 2 | $m$ | $(-\tfrac16 x + \tfrac16)(x^2 - 5x + 6) + (\tfrac76 x + \tfrac16)(x^2 - x) = x^3 - 2x + 1$ |

A script checked every entry with the implementation.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The values $s_i$ of line L3 are $m'(u_i)$ by the correctness of fast multipoint evaluation, and they are units, so line L4 computes the Lagrange weights. The upward pass keeps the invariant that $r_{j,k} = \sum_{i \in S} c_i\, m_{j,k}/(x - u_i)$, where $S$ is the set of leaves below node $(j, k)$: it holds at the leaves, where $m_{0,i}/(x - u_i) = 1$, and line C5 preserves it because $m_{j,k} = m_L m_R$. At the root it gives Lagrange's formula.

## Complexity

All bounds count ring operations in the algebraic complexity model and are proved under the assumptions on $M$ stated above, plus $n$ inversions in $R$.

- **The tree.** At most $4M(n)$ per level, as for fast multipoint evaluation.
- **The derivative and its values.** $m'$ costs $O(n)$. The remainder descent costs at most $7M(n) + O(n)$ per level.
- **The weights.** $n$ inversions and $n$ multiplications.
- **The upward pass.** At a node of degree $D = d_1 + d_2$, line C5 does two products of at most $D + 1$ coefficients each, at most $2M(D + 1)$, and an addition. Over a level, $\sum (D + 1) \le 2n$, so the level costs at most $2M(2n) \le 8M(n)$.
- **Total.** At most $19 M(n) \lceil \log_2 n \rceil + O(n \log n)$, that is $O(M(n) \log n)$; with FFT multiplication $O(n \log^2 n)$.

The constant 19 is a safe bound from this proof. Von zur Gathen and Gerhard, Section 10.2, give a smaller one, and the transposed algorithms of Bostan, Lecerf and Schost lower it further.

**Space.** $O(n \log n)$ ring elements for the tree, and $O(n)$ for each level of the passes.

| multiplication | $M(n)$ | fast interpolation |
|---|---|---|
| schoolbook | $\Theta(n^2)$ | $\Theta(n^2)$, slower than Newton's divided differences |
| Karatsuba | $O(n^{\log_2 3})$ | $O(n^{\log_2 3})$ |
| FFT over a ring with suitable roots of unity | $O(n \log n)$ | $O(n \log^2 n)$ |

**In practice (observed).** Newton's divided differences use about $n^2/2$ divisions and as many subtractions, with very little overhead, so they win for small $n$. The crossover depends on the field, the multiplication and the machine and is found by measurement. When the same points are used for many interpolations, the tree and the inverses $1/m'(u_i)$ are computed once, and each further interpolation costs only the upward pass.

## Properties

- **Exact.** Over $\mathbb{Q}$ or $\mathbb{Z}/p\mathbb{Z}$ the result is exact.
- **Needs units.** The only divisions are by $m'(u_i)$. Over $\mathbb{Z}$ this almost never works: already for the points $0, 1, 2$ the value $m'(0) = 2$ is not a unit. Over $\mathbb{Z}$, interpolate modulo primes and combine by Chinese remaindering, or work over $\mathbb{Q}$.
- **Shared tree.** The same subproduct tree serves evaluation and interpolation at the same points.
- **Linear in the values.** For fixed points the map from values to coefficients is linear, the inverse of the [Vandermonde matrix](/vandermonde-matrix/).
- **Not numerically stable.** Over floating point numbers, the method loses accuracy for most point sets, as fast multipoint evaluation does.

## Variants and improvements

- **Fast Chinese remaindering.** Replace the leaves $x - u_i$ by pairwise coprime moduli $m_i$, the values by residues $v_i \bmod m_i$, and $1/m'(u_i)$ by the inverse of $m/m_i$ modulo $m_i$. The same upward pass gives the unique $f$ of degree less than $\sum \deg m_i$ with $f \equiv v_i \pmod{m_i}$, in $O(M(n) \log n)$ plus the cost of the inverses. This is the polynomial form of the [Chinese remainder theorem](/chinese-remainder-theorem/), in von zur Gathen and Gerhard, Section 10.3.
- **Precomputed points.** For a fixed set of points, store the tree and the weights $1/m'(u_i)$.
- **Roots of unity.** At the $n$-th roots of unity, $m = x^n - 1$, $m'(\omega^i) = n \omega^{-i}$, and the interpolation is the inverse DFT, with $O(n \log n)$ operations by the [FFT](/fast-fourier-transform/).
- **Transposed algorithms.** Bostan, Lecerf and Schost compute the weights and the linear combination with transposed products, with a smaller constant.
- **Hermite interpolation.** With repeated points and given derivatives, the leaves become powers $(x - u_i)^{e_i}$, and the problem is a case of fast Chinese remaindering.

## When to use it

Use fast interpolation for large $n$ when fast multiplication is available: in the [evaluation-interpolation paradigm](/evaluation-interpolation-paradigm/) for determinants, resultants and products, in decoding of [Reed-Solomon codes](/reed-solomon-decoding/), and in modular algorithms that rebuild a polynomial from its values. For small $n$, use [Lagrange interpolation](/lagrange-interpolation/) or Newton's divided differences. At roots of unity, use the inverse FFT.

## Pitfalls

- **Repeated or too close points.** If $u_i = u_j$ for some $i \ne j$, then $m'(u_i) = 0$ and the weights do not exist. Over $\mathbb{Z}/m\mathbb{Z}$ with composite $m$, a difference that is a zero divisor has the same effect. The implementation raises an error.
- **Integer inputs.** Values and points in $\mathbb{Z}$ give an interpolant in $\mathbb{Q}[x]$ in general. Do not expect integer coefficients, and do not divide with integer division.
- **The order of the children.** In line C5 the left partial sum is multiplied by the right product and the right partial sum by the left product. Swapping them gives a wrong result that still has the right degree.
- **An odd number of nodes.** A node without a sibling passes its partial sum up unchanged.
- **Floating point.** Over $\mathbb{R}$ with equally spaced points, the weights $1/m'(u_i)$ differ by factors of about $2^n$, and the computed coefficients have no correct digits for moderate $n$.

## Implementations

## History

Lagrange's interpolation formula appeared in 1795, and Newton's divided differences are older; both cost $\Theta(n^2)$ operations. Fast interpolation in $O(M(n) \log n)$ came in the early 1970s with fast multipoint evaluation, in work of Moenck and Borodin, Kung, and Strassen, using the identity $m'(u_i) = \prod_{j \ne i} (u_i - u_j)$ to reduce the weights to one evaluation. The textbook form with the subproduct tree and fast Chinese remaindering is in von zur Gathen and Gerhard, Chapter 10. Bostan, Lecerf and Schost lowered the constant in 2003 with the transposition principle.

## References
