---
tag: 9A002M
kind: definition
slug: hkz-reduction
name: Hermite-Korkine-Zolotarev reduction
aliases:
- HKZ reduction
- Korkine-Zolotarev reduction
- KZ reduction
- HKZ-reduced basis
area: number-theory/lattice-reduction
level: advanced
summary: 'Strongest classical basis notion: each vector is a shortest projected vector of its sublattice.'
prereqs: [lattice-basis, gram-schmidt-orthogonalization, size-reduction, shortest-vector-problem]
see_also: [kannan-enumeration, bkz-algorithm, minkowski-reduced-basis, lll-reduction, hermite-constant, successive-minima, lagrange-gauss-reduction, lattice-basis-reduction]
sources:
  - paper: "J. C. Lagarias, H. W. Lenstra Jr. and C. P. Schnorr, Korkin-Zolotarev bases and successive minima of a lattice and its reciprocal lattice, Combinatorica 10(4) (1990)"
    locator: pages 333 to 348 (the bounds (i+3)/4 between the basis lengths and the successive minima)
  - book: isbn:9783642261640
    title: Phong Q. Nguyen and Brigitte Vallée (editors), The LLL Algorithm, Survey and Applications, Springer, 2010
    locator: Chapter 2, Phong Q. Nguyen, Hermite's constant and lattice algorithms (HKZ reduction and its relation to Hermite's constant)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Section 18.5, Korkine-Zolotarev bases
  - paper: "R. Kannan, Minkowski's convex body theorem and integer programming, Mathematics of Operations Research 12(3) (1987)"
    locator: the algorithm that computes an HKZ-reduced basis with n^(O(n)) arithmetic operations
---

A basis is Hermite-Korkine-Zolotarev reduced (HKZ-reduced) when it is size-reduced and each Gram-Schmidt vector $b_i^*$ is a shortest nonzero vector of the projected lattice it belongs to. So $b_1$ is a shortest vector of the [lattice](/lattice/), $b_2$ is a shortest vector after projecting away $b_1$, and so on. It is the strongest of the classical reduction notions in the Gram-Schmidt sense, it is the goal that [LLL](/lll-reduction/) relaxes and [BKZ](/bkz-algorithm/) approximates block by block, and computing it costs about as much as solving the [shortest vector problem](/shortest-vector-problem/).

## Definition

Notation is that of the other pages in this area: basis rows $b_1, \ldots, b_n$, [Gram-Schmidt](/gram-schmidt-orthogonalization/) vectors $b_i^*$ and coefficients $\mu_{ij} = \langle b_i, b_j^* \rangle / \langle b_j^*, b_j^* \rangle$, and $\pi_i$ the orthogonal projection onto $\operatorname{span}(b_1, \ldots, b_{i-1})^\perp$, so that $\pi_i(b_i) = b_i^*$ and $\pi_1$ is the identity.

**Definition.** A basis $b_1, \ldots, b_n$ of $L$ is **HKZ-reduced** if

1. it is **size-reduced**: $|\mu_{ij}| \le \tfrac12$ for all $1 \le j < i \le n$;
2. for every $i$, $\|b_i^*\| = \lambda_1(\pi_i(L))$, where $\pi_i(L)$ is the projected lattice of rank $n - i + 1$ spanned by $\pi_i(b_i), \ldots, \pi_i(b_n)$.

**Recursive form.** Condition 2 holds if and only if $b_1$ is a shortest nonzero vector of $L$ and the projected basis $\pi_2(b_2), \ldots, \pi_2(b_n)$ satisfies condition 2 for $\pi_2(L)$. This is how an HKZ basis is computed: find a shortest vector, make it the first vector of a basis, project, and recurse; then size-reduce, which does not change any $b_i^*$.

**Existence.** Every lattice has an HKZ-reduced basis. A shortest vector of $\pi_i(L)$ is primitive in $\pi_i(L)$, and any lift of it to $L$ extends $b_1, \ldots, b_{i-1}$ to a set that can be completed to a basis; size reduction then makes condition 1 hold. The basis is not unique in general, even up to signs.

**Properties.** For an HKZ-reduced basis:

- $\|b_1\| = \lambda_1(L)$, and $\|b_1\| \le \sqrt{\gamma_n} \det(L)^{1/n}$ with $\gamma_n$ the [Hermite constant](/hermite-constant/). More generally $\|b_i^*\| \le \sqrt{\gamma_{n-i+1}}\, \big(\prod_{j \ge i} \|b_j^*\|\big)^{1/(n-i+1)}$ for each $i$.
- **Lagarias, Lenstra and Schnorr.** For each $i$, $\tfrac{4}{i+3} \le \|b_i\|^2 / \lambda_i(L)^2 \le \tfrac{i+3}{4}$, where $\lambda_i$ are the [successive minima](/successive-minima/). So every basis vector is within a factor $\sqrt{(n+3)/4}$ of the corresponding minimum.
- Every block is reduced too: for $i \le k$, the projected basis $\pi_i(b_i), \ldots, \pi_i(b_k)$ is HKZ-reduced. In particular every pair $(\pi_i(b_i), \pi_i(b_{i+1}))$ is [Lagrange-reduced](/lagrange-gauss-reduction/), so an HKZ basis is [LLL-reduced](/lll-reduction/) for every $\delta \le 1$.

**Computation.** Kannan's algorithm computes an HKZ-reduced basis with $n^{O(n)}$ arithmetic operations on numbers of polynomial size; Hanrot and Stehlé sharpened the analysis of [Kannan enumeration](/kannan-enumeration/) to $n^{n/(2e) + o(n)}$. Computing an HKZ basis takes $n$ SVP computations in decreasing dimension, and an HKZ basis gives $\lambda_1$ at once, so the two problems are equivalent up to a polynomial factor. Since SVP is NP-hard under randomized reductions, no polynomial-time algorithm is expected.

## Examples and non-examples

**Examples.**

- **Dimension 2.** A basis $(b_1, b_2)$ of rank 2 is HKZ-reduced exactly when it is Lagrange-reduced: $\|b_1\| \le \|b_2\|$ and $|\mu_{21}| \le \tfrac12$. For $b_1 = (3, -1)$, $b_2 = (0, 4)$, $\mu_{21} = -\tfrac25$ and $\|b_1\|^2 = 10 \le 16$, so it is HKZ-reduced.
- **An orthogonal basis** ordered by increasing length, such as $(1, 0, 0), (0, 2, 0), (0, 0, 3)$, is HKZ-reduced: all $\mu_{ij} = 0$ and each $b_i$ is a shortest vector of the projected lattice $b_i \mathbb{Z} \oplus \cdots \oplus b_n \mathbb{Z}$.
- **The checkerboard lattice $D_3$.** The basis $(-1, 0, 1), (0, -1, -1), (0, 1, -1)$ is HKZ-reduced. Its squared Gram-Schmidt lengths are $2, \tfrac32, \tfrac43$, whose product is $4 = \det(D_3)^2$. The first is $\lambda_1^2 = 2$, and $\tfrac32$ and $\tfrac43$ are the minima of the projected lattices.
- **A three-dimensional example.** The basis $b_1 = (10, 0, 0)$, $b_2 = (5, 10, 0)$, $b_3 = (5, 4, 10)$ has $\|b_i^*\| = 10$ for all $i$, $\mu_{21} = \tfrac12$, $\mu_{31} = \tfrac12$ and $\mu_{32} = \tfrac25$. The squared lengths of the shortest vectors are $100, 125, 136$, so $b_1$ is a shortest vector; $\pi_2(L)$ is generated by $(0, 10, 0)$ and $(0, 4, 10)$ and has minimum 10; and $b_3^*$ is fixed up to sign. So the basis is HKZ-reduced.

**Non-examples.**

- **HKZ is not Minkowski.** In the last example, $\|b_3\|^2 = 141$, but $b_3 - b_2 = (0, -6, 10)$ has squared length $136$ and $b_1, b_2, b_3 - b_2$ is also a basis. So the basis is not [Minkowski-reduced](/minkowski-reduced-basis/), and no HKZ basis of this lattice is, because size reduction forces $\mu_{32} = \tfrac25$ and $\|b_3\|^2 = 141$. HKZ minimizes the projected lengths $\|b_i^*\|$ one after the other, and Minkowski minimizes the lengths $\|b_i\|$; the two agree in dimension 2 and differ from dimension 3 on.
- **Shortest vector first is not enough.** $b_1 = (1, 0, 0)$, $b_2 = (0, 3, 0)$, $b_3 = (0, 1, 1)$ has $b_1$ shortest and is size-reduced, but $\pi_2(b_3) = (0, 1, 1)$ is shorter than $b_2^* = (0, 3, 0)$, so condition 2 fails at $i = 2$.
- **Not size-reduced.** $(1, 0), (5, 1)$ has the right Gram-Schmidt vectors $(1, 0), (0, 1)$ but $\mu_{21} = 5$, so it fails condition 1; subtracting $5 b_1$ gives the HKZ basis $(1, 0), (0, 1)$.
- **LLL-reduced bases.** An LLL-reduced basis satisfies only $\|b_{i+1}^*\|^2 \ge (\delta - \mu_{i+1,i}^2) \|b_i^*\|^2$, a local condition on pairs; its first vector can be longer than $\lambda_1$ by a factor exponential in $n$.

## Related definitions

- **[Size reduction](/size-reduction/).** Condition 1, shared with LLL and BKZ.
- **[LLL reduction](/lll-reduction/).** The relaxation that asks only that consecutive projected pairs be nearly Lagrange-reduced; computable in polynomial time.
- **[BKZ](/bkz-algorithm/) reduction with block size $\beta$.** Each projected block $\pi_i(b_i), \ldots, \pi_i(b_{\min(i+\beta-1, n)})$ has its first vector shortest. For $\beta = 2$ it is close to LLL, and for $\beta = n$ it is HKZ.
- **[Minkowski reduction](/minkowski-reduced-basis/).** Each $b_i$ is a shortest vector that extends $b_1, \ldots, b_{i-1}$ to part of a basis; it compares full lengths rather than projected lengths.
- **Dual HKZ.** A basis whose reversed [dual basis](/dual-lattice/) is HKZ-reduced; it makes $\|b_n^*\|$ as large as possible, and it is used in slide reduction and in dual BKZ.
- **Hermite reduction.** Hermite's earlier notion, from which Korkine and Zolotarev developed theirs for quadratic forms in 1873 and 1877.

## References
