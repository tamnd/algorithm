---
tag: FEGRDV
kind: technique
slug: size-reduction
name: Size reduction
aliases:
- size reduction step
- Hermite size reduction
- weak reduction
area: number-theory/lattice-reduction
level: advanced
summary: Subtracts integer multiples of basis vectors so Gram-Schmidt coefficients lie in [-1/2, 1/2].
prereqs: [lattice-basis, gram-schmidt-orthogonalization, unimodular-matrix]
see_also: [lll-algorithm, lll-reduction, lovasz-condition, lagrange-gauss-reduction, babai-nearest-plane, pslq-algorithm, seysen-reduction, lattice-basis-reduction]
sources:
  - paper: doi:10.1007/BF01457454
    title: A. K. Lenstra, H. W. Lenstra Jr. and L. Lovász, Factoring polynomials with rational coefficients, Mathematische Annalen 261, 1982
    locator: Section 1 (the condition that the Gram-Schmidt coefficients have absolute value at most 1/2 and the reduction step that enforces it)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Springer, Graduate Texts in Mathematics 138, 1993
    locator: Section 2.6 (the LLL algorithm and its subalgorithm for the size reduction of one coefficient)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 17, Lattice basis reduction (size reduction inside the LLL algorithm)
  - paper: "Phong Q. Nguyen and Damien Stehlé, An LLL algorithm with quadratic complexity, SIAM Journal on Computing 39(3), 2009"
    locator: pages 874 to 903 (the relaxed condition with a factor eta slightly above 1/2 for floating point)
---

Size reduction makes a [lattice basis](/lattice-basis/) as close to its [Gram-Schmidt](/gram-schmidt-orthogonalization/) basis as integer steps allow: from each vector $b_k$ it subtracts integer multiples of the earlier vectors until every coefficient $\mu_{kj}$ with $j < k$ has $|\mu_{kj}| \le 1/2$. It never changes the lattice or the Gram-Schmidt vectors $b_i^*$; it only removes the part of $b_k$ along the earlier directions that an integer combination can remove. It is the inner step of the [LLL algorithm](/lll-algorithm/), of [Babai's nearest plane](/babai-nearest-plane/) method and of most other reduction algorithms.

## In plain words

Each basis vector has a part that points in a new direction and a part that leans along the vectors before it. The new part is fixed by the earlier vectors and cannot change. The leaning part can be made smaller by subtracting whole copies of the earlier vectors.

So we subtract the right whole number of copies of each earlier vector, starting with the latest one and going back to the first. After that, the vector leans along each earlier direction by at most half of that direction's own length. The lattice stays the same, because subtracting whole copies of basis vectors is a step that can be undone.

This is the same idea as replacing a number by its remainder after division, but done one direction at a time.

## When it applies

- You have a basis $b_1, \ldots, b_n$ (rows) with its Gram-Schmidt data $b_i^*$ and $\mu_{ij}$, and you want short vectors without changing the order of the basis. Size reduction is the cheap part of a reduction; it does not change any $\|b_i^*\|$, so it cannot fix a bad order, which is the job of swaps such as the [Lovász condition](/lovasz-condition/).
- You need the bound $\|b_k\|^2 \le \|b_k^*\|^2 + \frac14 \sum_{j < k} \|b_j^*\|^2$, which turns bounds on the Gram-Schmidt lengths into bounds on the basis vectors.
- You need to keep numbers small: in LLL with exact arithmetic, size reduction is what keeps the entries of the basis from growing.
- You want to reduce a target vector $t$ modulo the lattice, to find a lattice point close to $t$: the same loop with $t$ in place of $b_k$ is [Babai's nearest plane](/babai-nearest-plane/) algorithm.

**Notation.** As on all pages of this area: basis rows $b_1, \ldots, b_n \in \mathbb{R}^m$, Gram-Schmidt vectors $b_i^*$, coefficients $\mu_{ij} = \langle b_i, b_j^* \rangle / \|b_j^*\|^2$ for $j < i$, so that $b_i = b_i^* + \sum_{j < i} \mu_{ij} b_j^*$. We set $\mu_{ii} = 1$. $\lfloor x \rceil$ is the nearest integer to $x$, with ties broken in a fixed way.

## The template

The template reduces one vector $b_k$ against $b_1, \ldots, b_{k-1}$. It has two holes: the rounding rule ROUND, and the vector being reduced, which is $b_k$ for basis reduction or a target $t$ for close vector search.

```pseudo id=main
SIZE-REDUCE(b_1..b_n, μ, k)            ▷ makes |μ_kj| ≤ 1/2 for all j < k
L1  for j = k − 1 down to 1 do
L2      q ← ROUND(μ_kj)                ▷ hole: nearest integer, or 0 when |μ_kj| ≤ η
L3      if q ≠ 0 then
L4          b_k ← b_k − q · b_j
L5          for i = 1 to j − 1 do μ_ki ← μ_ki − q · μ_ji
L6          μ_kj ← μ_kj − q
L7  return b_1..b_n, μ
```

A fully size-reduced basis comes from calling SIZE-REDUCE for $k = 2, \ldots, n$, in any order of $k$, because reducing $b_k$ changes only row $k$ of $\mu$.

**Walk-through and invariants.** Line L4 adds to $b_k$ a vector of $\operatorname{span}(b_1, \ldots, b_{k-1})$, so:

1. *The lattice does not change.* The step is the elementary row operation "row $k$ minus $q$ times row $j$", a [unimodular](/unimodular-matrix/) transform with inverse "row $k$ plus $q$ times row $j$".
2. *The Gram-Schmidt vectors do not change.* $b_i$ is unchanged for $i \ne k$, and $b_k^*$ is the projection of $b_k$ orthogonal to $\operatorname{span}(b_1, \ldots, b_{k-1})$, which the step leaves alone.
3. *Lines L5 and L6 keep $\mu$ correct.* Since $b_j = b_j^* + \sum_{i < j} \mu_{ji} b_i^*$, the new $b_k$ has coefficient $\mu_{ki} - q \mu_{ji}$ on $b_i^*$ for $i < j$, coefficient $\mu_{kj} - q$ on $b_j^*$, and unchanged coefficients for $i > j$.
4. *After the step for index $j$, $|\mu_{kj}| \le 1/2$, and it stays so.* $|\mu_{kj} - \lfloor \mu_{kj} \rceil| \le 1/2$, and the later steps, for $j' < j$, change only $\mu_{ki}$ with $i \le j' < j$.

This is why the loop runs from $j = k - 1$ down to 1. At the end, by orthogonality of the $b_i^*$,

$$\|b_k\|^2 = \|b_k^*\|^2 + \sum_{j < k} \mu_{kj}^2 \|b_j^*\|^2 \le \|b_k^*\|^2 + \frac14 \sum_{j < k} \|b_j^*\|^2.$$

Among all vectors $b_k + \sum_{j < k} x_j b_j$ with integer $x_j$, this is not always the shortest one, but it is the one that the nearest plane rule picks, and its distance from $b_k^*$ obeys the bound above.

**Cost.** One call does at most $k - 1$ rounds. Each round costs $m$ multiplications for line L4 and $j - 1$ for line L5, so one call takes $O(km + k^2)$ arithmetic operations, and a full size reduction takes $O(n^2 m + n^3)$. With exact arithmetic on an integer basis, the $\mu_{kj}$ are rationals with denominator $d_j = \prod_{i \le j} \|b_i^*\|^2$, which is an integer, so the work in bit operations depends on the sizes of these numbers; see the [LLL algorithm](/lll-algorithm/) page for the bounds inside LLL.

**Example.** Take $b_1 = (1, 1, 1)$, $b_2 = (-1, 0, 2)$, $b_3 = (3, 5, 6)$. The Gram-Schmidt data are $\|b_1^*\|^2 = 3$, $\|b_2^*\|^2 = 14/3$, $\|b_3^*\|^2 = 9/14$, $\mu_{21} = 1/3$, $\mu_{31} = 14/3$, $\mu_{32} = 13/14$. For $k = 2$ nothing happens, since $|\mu_{21}| \le 1/2$. For $k = 3$:

- $j = 2$: $q = \lfloor 13/14 \rceil = 1$, $b_3 \leftarrow (3, 5, 6) - (-1, 0, 2) = (4, 5, 4)$, $\mu_{31} \leftarrow 14/3 - 1 \cdot 1/3 = 13/3$, $\mu_{32} \leftarrow -1/14$.
- $j = 1$: $q = \lfloor 13/3 \rceil = 4$, $b_3 \leftarrow (4, 5, 4) - 4 (1, 1, 1) = (0, 1, 0)$, $\mu_{31} \leftarrow 1/3$.

The result $(1, 1, 1), (-1, 0, 2), (0, 1, 0)$ is size-reduced, with the same Gram-Schmidt lengths $3, 14/3, 9/14$. The third vector went from length $\sqrt{70}$ to 1. The basis is still not well ordered: the last vector is the shortest, and a swap is needed, which LLL does next.

## Classic examples

- **[Lagrange-Gauss reduction](/lagrange-gauss-reduction/).** In dimension 2, size reduction is the step $b_2 \leftarrow b_2 - \lfloor \mu_{21} \rceil b_1$; alternating it with swaps gives the Lagrange-Gauss algorithm, a vector form of the [Euclidean algorithm](/euclidean-algorithm/).
- **[LLL algorithm](/lll-algorithm/).** LLL alternates size reduction of $b_k$ with a swap of $b_{k-1}$ and $b_k$ when the [Lovász condition](/lovasz-condition/) fails. Size reduction is what makes an [LLL-reduced basis](/lll-reduction/) short and keeps the numbers polynomial in size.
- **[Babai's nearest plane](/babai-nearest-plane/).** Size reduction of a target $t$ against the whole basis, with $\mu_{t,j} = \langle t, b_j^* \rangle / \|b_j^*\|^2$, returns $t - w$ for a lattice vector $w$ with $\|t - w\|^2 \le \frac14 \sum_j \|b_j^*\|^2$.
- **[PSLQ](/pslq-algorithm/).** The "Hermite reduction" step of PSLQ is size reduction of the rows of a lower triangular matrix, which keeps the entries below the diagonal at most half the diagonal entry in absolute value.
- **[HKZ](/hkz-reduction/) and [BKZ](/bkz-algorithm/).** Both definitions require a size-reduced basis, and both algorithms run size reduction after each insertion of a short vector.
- **[Hermite normal form](/hermite-normal-form/).** The step that reduces the entries above each pivot modulo the pivot is the same idea in the triangular setting of integer matrices, with a different rounding rule.

## Variations

- **Relaxed size reduction.** Require only $|\mu_{kj}| \le \eta$ for a fixed $\eta$ with $1/2 < \eta < 1$, that is, round only when $|\mu_{kj}| > \eta$. With floating point $\mu$, the exact condition $\le 1/2$ cannot be checked reliably; the L² algorithm of Nguyen and Stehlé uses $\eta$ slightly above $1/2$.
- **Iterated size reduction.** With floating point, one pass may leave some $|\mu_{kj}|$ above $\eta$ because the computed $\mu$ were wrong. Floating point LLL variants recompute the $\mu_{kj}$ from the new $b_k$ and repeat the pass until no coefficient exceeds the bound.
- **Size reduction against the dual.** Seysen's measure treats the basis and its [dual](/dual-lattice/) together; the [Seysen reduction](/seysen-reduction/) step $b_j \leftarrow b_j + \lambda b_i$ is chosen to shrink both, not to bound $\mu$.
- **Matrix form.** Write $B = M B^*$ with $M$ lower triangular, unit diagonal and $M_{ij} = \mu_{ij}$. Full size reduction finds a lower triangular unimodular $U$ such that $U M$ has off-diagonal entries at most $1/2$ in absolute value; $U$ is unique when no rounding hits a tie.

## Pitfalls

- **The order of the loop matters.** Going from $j = 1$ up to $k - 1$ is wrong, because the step for $j$ changes $\mu_{ki}$ for every $i < j$. Example: $b_1 = (2, 0, 0)$, $b_2 = (1, 1, 0)$, $b_3 = (2, 2, 1)$ has $\mu_{21} = 1/2$, $\mu_{31} = 1$, $\mu_{32} = 2$. The upward order subtracts $b_1$, then $2 b_2$, and ends with $b_3 = (-2, 0, 1)$ and $\mu_{31} = -1$, not reduced. The downward order subtracts $2 b_2$ and ends with $b_3 = (0, 0, 1)$, with $\mu_{31} = \mu_{32} = 0$.
- **Forgetting to update $\mu$.** Line L5 is easy to omit. Without it, the next rounds use stale coefficients, and the result is not size-reduced.
- **Size reduction does not make vectors short.** It never changes $\|b_k^*\|$. If $b_1$ is long and $b_2$ short, size reduction of $b_2$ against $b_1$ does nothing useful; the basis needs a swap.
- **Floating point coefficients.** If the $\mu_{kj}$ are computed in floating point with too little precision, the rounding can pick the wrong $q$. The result is still a basis of the lattice, but the claimed bound may fail, and inside LLL a wrong reduction can cause a loop that never ends. Use exact rationals, or a precision proved to be enough, as in the L² algorithm.
- **Ties.** When $\mu_{kj}$ is exactly a half-integer, both roundings give $|\mu_{kj}| = 1/2$. Fix one rule so that results are reproducible.

## References
