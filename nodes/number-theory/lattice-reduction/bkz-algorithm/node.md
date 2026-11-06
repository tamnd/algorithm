---
tag: TQ85KA
kind: algorithm
slug: bkz-algorithm
name: BKZ algorithm
aliases:
- block Korkine-Zolotarev reduction
- Schnorr-Euchner BKZ
- BKZ reduction
- block Korkine-Zolotarev algorithm
area: number-theory/lattice-reduction
level: advanced
summary: Block-wise reduction that calls an SVP oracle on blocks of bounded size.
solves: [lattice-basis-reduction, approximate-svp]
model: word-ram
complexity:
  vars: {n: the rank of the lattice, m: the length of the vectors, β: the block size, P: "the number of steps (calls of the block oracle), finite but with no known polynomial bound", S: "the cost of one block enumeration, at most 2^(O(β^2)) arithmetic operations on an LLL-reduced block", T: "the cost of one LLL call, polynomial in n, m and the input size"}
  time: {worst: O(P (n^2 m + S + T)), best: O(T + n (n^2 m + S)), per_step: O(n^2 m + S + T)}
  space: {extra: O(n^2 + n m)}
properties: {deterministic: true, recursive: false, exact: true, polynomial_time: false}
history:
  year: 1987
  people: [Claus-Peter Schnorr, Martin Euchner]
  note: Schnorr defined block Korkine-Zolotarev reduction and its hierarchy of algorithms in 1987; Schnorr and Euchner gave the practical BKZ algorithm with floating-point arithmetic and zigzag enumeration in 1994.
prereqs: [lll-algorithm, hkz-reduction, lattice-enumeration, gram-schmidt-orthogonalization]
see_also: [deep-lll, root-hermite-factor, gaussian-heuristic, schnorr-euchner-enumeration, lattice-sieving, approximate-svp, hermite-constant, lattice-based-cryptography]
sources:
  - paper: "C. P. Schnorr, A hierarchy of polynomial time lattice basis reduction algorithms, Theoretical Computer Science 53(2-3) (1987)"
    locator: pages 201 to 224 (block reduction, the Korkine-Zolotarev constant and the approximation factor of block-reduced bases)
  - paper: "C. P. Schnorr and M. Euchner, Lattice basis reduction: improved practical algorithms and solving subset sum problems, Mathematical Programming 66 (1994)"
    locator: pages 181 to 199 (the BKZ algorithm with tours over all blocks, floating-point Gram-Schmidt data and zigzag enumeration)
  - paper: "N. Gama and P. Q. Nguyen, Predicting lattice reduction, EUROCRYPT 2008, LNCS 4965"
    locator: the experimental root Hermite factors and running times of BKZ on random lattices
  - paper: "Y. Chen and P. Q. Nguyen, BKZ 2.0, Better lattice security estimates, ASIACRYPT 2011, LNCS 7073"
    locator: BKZ with extreme pruning, early abort and the simulator of the Gram-Schmidt profile
  - paper: "G. Hanrot, X. Pujol and D. Stehlé, Analyzing blockwise lattice algorithms using dynamical systems, CRYPTO 2011, LNCS 6841"
    locator: the bound on the output of BKZ after a polynomial number of tours
---

The BKZ algorithm reduces a [lattice](/lattice/) basis by solving the [shortest vector problem](/shortest-vector-problem/) exactly in small windows. For each position $k$ it looks at the block of $\beta$ consecutive vectors starting at $k$, projected away from the earlier ones, finds a shortest vector of that projected block by [enumeration](/lattice-enumeration/) or sieving, and inserts it at position $k$ if it is shorter than $\sqrt\delta \, \|b_k^*\|$. Block size 2 gives about [LLL](/lll-algorithm/), block size $n$ gives [HKZ reduction](/hkz-reduction/), and the block sizes in between trade running time against the quality of the basis; this trade-off is the base of almost all security estimates for [lattice-based cryptography](/lattice-based-cryptography/).

## In plain words

LLL tidies a set of arrows that build a grid by looking at two neighbouring arrows at a time. BKZ looks at a window of several neighbours, say twenty, at a time.

Inside the window it searches hard, by brute force, for the shortest arrow that the window can build, after ignoring everything the earlier arrows already cover. If that arrow is clearly shorter than the first arrow of the window, it goes to the front of the window, and a quick LLL clean-up follows. Then the window slides one place on. The windows wrap around and the passes repeat until a full round makes no change.

A larger window gives a much better set of arrows, but the brute-force search inside the window costs time that grows very fast with its size. So the window size is the dial between speed and quality.

## The problem

**Input.** Linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$, a block size $\beta \ge 2$ and a parameter $\delta$ with $1/4 < \delta \le 1$.

**Output.** A basis of the same lattice that is **BKZ-reduced**: it is [LLL-reduced](/lll-reduction/) with parameter $\delta$, and for every $k$,

$$\delta \, \|b_k^*\|^2 \le \lambda_1\big(L_{[k]}\big)^2, \qquad L_{[k]} = \pi_k\big(L(b_k, \ldots, b_{h})\big), \quad h = \min(k + \beta - 1, n),$$

where $\pi_k$ projects orthogonally to $b_1, \ldots, b_{k-1}$. So $b_k^*$ is, up to the factor $\sqrt\delta$, a shortest vector of its projected block. With $\delta = 1$ and $\beta = n$ this is HKZ reduction.

**Notation and cost model.** As on the other pages of this area, basis vectors are rows $b_1, \ldots, b_n$, $b_i^*$ and $\mu_{ij}$ are the [Gram-Schmidt](/gram-schmidt-orthogonalization/) data, $N_i = \|b_i^*\|^2$, $\lambda_1$ is the first minimum, $\det(L)$ is the determinant and $\delta$ is the reduction parameter. The reference implementation uses exact rational arithmetic and an exact enumeration oracle. Time counts arithmetic operations on rationals. The cost of one step is proved; the number of steps is proved finite only; the quality of the output in practice and the cost of the floating-point versions with pruning are observed or heuristic. Cryptographic practice uses floating point with heuristic precision.

## The algorithm

```pseudo id=main
BKZ(B, β, δ)                        ▷ independent rows b_1..b_n, β ≥ 2, 1/4 < δ ≤ 1
L1  LLL-reduce B with δ; z ← 0; k ← 0
L2  while z < n − 1
L3      k ← (k mod (n − 1)) + 1; h ← min(k + β − 1, n)
L4      x ← shortest nonzero vector of π_k(L(b_k, ..., b_h)), by enumeration
L5      if ‖π_k(Σ x_i b_i)‖² < δ N_k
L6          replace b_k, ..., b_h by a basis of the same block with first vector Σ x_i b_i
L7          LLL-reduce B with δ; z ← 0
L8      else z ← z + 1
L9  return B
```

The counter $z$ counts consecutive steps without change. One sweep of $k$ over $1, \ldots, n-1$ is a **tour**; the loop stops after $n - 1$ consecutive steps without an insertion, which may span two tours.

Line L4 is [Fincke-Pohst enumeration](/fincke-pohst-enumeration/) on the projected block, whose Gram-Schmidt data are $\mu_{ij}$ and $N_i$ for $k \le j < i \le h$; the radius starts at $N_k$ and shrinks each time a shorter vector is found. Line L6 works on the integer coefficients only: a shortest vector has $\gcd(x) = 1$, and a sweep of $2 \times 2$ steps from the [extended Euclidean algorithm](/extended-euclidean-algorithm/), from the end of the block to the front, turns $x$ into $(1, 0, \ldots, 0)$ while applying the same unimodular matrices to the rows. Schnorr and Euchner instead insert the new vector in front of the block and let LLL remove the linear dependence; both give a basis of the same lattice.

## Example

The basis $b_1 = (4, 0, 0)$, $b_2 = (-2, 3, 0)$, $b_3 = (1, 1, 3)$ with $\delta = 3/4$, the example of the [deep LLL](/deep-lll/) page. It is LLL-reduced, with $N = (16, 9, 9)$, $\mu_{21} = -\tfrac12$, $\mu_{31} = \tfrac14$, $\mu_{32} = \tfrac13$.

**Block size 2.** Here $n - 1 = 2$, so the loop stops after two steps without change.

| Step | $k$ | Block | Shortest $x$, squared length | Test at L5 | Action |
|------|-----|------|------|------|------|
| 1 | 1 | $b_1, b_2$ | $(-1, -1)$, $13$ | $13 \ge \tfrac34 \cdot 16 = 12$ | $z = 1$ |
| 2 | 2 | $\pi_2(b_2), \pi_2(b_3)$ | $(1, 0)$, $9$ | $9 \ge \tfrac34 \cdot 9$ | $z = 2$, stop |

BKZ with $\beta = 2$ returns the input unchanged, like LLL, although $\|b_3\|^2 = 11 < 16$.

**Block size 3.** The first block is the whole lattice.

| Step | $k$ | $N$ | Shortest $x$, squared length | Test at L5 | Action |
|------|-----|------|------|------|------|
| 1 | 1 | $(16, 9, 9)$ | $(0, 0, -1)$, $11$ | $11 < 12$ | insert $-b_3$: rows $(-1, -1, -3), (-4, 0, 0), (-2, 3, 0)$; LLL gives $(-1, -1, -3), (2, 3, 0), (-2, 3, 0)$; $z = 0$ |
| 2 | 2 | $(11, \tfrac{118}{11}, \tfrac{648}{59})$ | $(1, 0)$, $\tfrac{118}{11}$ | $\tfrac{118}{11} \ge \tfrac{177}{22}$ | $z = 1$ |
| 3 | 1 | $(11, \tfrac{118}{11}, \tfrac{648}{59})$ | $(1, 0, 0)$, $11$ | $11 \ge \tfrac{33}{4}$ | $z = 2$, stop |

The output $(-1, -1, -3), (2, 3, 0), (-2, 3, 0)$ starts with a shortest vector, $\lambda_1^2 = 11$, and since the block is the whole lattice it is HKZ-reduced. The determinant is unchanged: $N_1 N_2 N_3 = 11 \cdot \tfrac{118}{11} \cdot \tfrac{648}{59} = 1296 = 36^2$, the square of $|\det B| = 36$. The test file checks both traces.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The enumeration of line L4 is exact: the scan skips only coefficients that cannot beat the current best, and the best only decreases, so nothing skipped could become useful later. A shortest vector of the projected block has coprime coefficients, since dividing by a common factor would shorten it, so the Euclidean sweep of line L6 is unimodular and keeps the lattice. LLL is unimodular too.

After every step the basis is LLL-reduced, and a step without insertion changes nothing. So when $z$ reaches $n - 1$, the last $n - 1$ steps checked every $k \le n - 1$ on the same basis, and every block condition holds; the block at $k = n$ is one vector and always satisfies it.

For termination, let $D_j = N_1 \cdots N_j$ and scale by a common denominator $s$ of the input, so that $s^{2j} D_j$ are positive integers. An insertion at $k$ keeps $D_1, \ldots, D_{k-1}$ and makes $D_k$ smaller, and each LLL swap makes one $D_j$ smaller and keeps the others. So the tuple $(s^2 D_1, \ldots, s^{2n} D_n)$ decreases lexicographically at every insertion and swap, which can happen only finitely often. Between insertions there are at most $n - 1$ steps. The argument works for $\delta = 1$ too, but it gives no polynomial bound.

## Complexity

- **One step, proved.** Line L4 needs the Gram-Schmidt data, $O(n^2 m)$ operations if recomputed, and one enumeration. On an LLL-reduced basis $N_k / N_{k+j} \le \alpha^j$ with $\alpha = 1/(\delta - 1/4)$, so the enumeration tree has at most $\beta \prod_{j=0}^{\beta-1} (2 \alpha^{j/2} + 1) = 2^{O(\beta^2)}$ nodes of $O(\beta)$ operations each. Line L6 is $O(\beta m)$ operations on integers of the size of $x$, and line L7 is one LLL call, polynomial in $n$, $m$ and the input size.
- **Number of steps, open.** The proof shows that the number $P$ of steps is finite. No polynomial bound on the number of tours is known for BKZ as stated. Hanrot, Pujol and Stehlé proved that after a number of tours polynomial in $n$, of order $n^3 / \beta^2$ times a logarithmic factor, the first vector already satisfies a bound close to the one for fully reduced bases; practical implementations stop after a fixed number of tours for this reason.
- **Stronger oracles.** With HKZ preprocessing of each block, enumeration costs $\beta^{\beta/(2e) + o(\beta)}$ (Kannan, with the analysis of Hanrot and Stehlé). Sieving costs $2^{0.292 \beta + o(\beta)}$ time and $2^{0.208 \beta + o(\beta)}$ memory, heuristically. Extreme pruning in BKZ 2.0 makes enumeration much faster in practice, also heuristically.
- **Proved quality.** Schnorr proved that a BKZ-reduced basis with $\delta = 1$ has $\|b_1\|^2 \le \alpha_\beta^{(n-1)/(\beta-1)} \lambda_1^2$, where $\alpha_\beta \le \beta^{1 + \ln \beta}$ is the Korkine-Zolotarev constant. So the approximation factor is $\beta^{O(n \log \beta / \beta)}$: exponential in $n$ for fixed $\beta$, polynomial in $n$ only for $\beta$ linear in $n$.
- **Observed quality.** On random lattices the first vector has $\|b_1\| \approx \delta_\beta^n \det(L)^{1/n}$ for a [root Hermite factor](/root-hermite-factor/) $\delta_\beta$ that depends on $\beta$ only. Gama and Nguyen measured about $1.0128$ for $\beta = 20$, against $1.0219$ for LLL. For large $\beta$ the [Gaussian heuristic](/gaussian-heuristic/) predicts $\delta_\beta \approx \big(\tfrac{\beta}{2\pi e} (\pi \beta)^{1/\beta}\big)^{1/(2(\beta-1))}$.

## Properties

- **The hierarchy.** $\beta = 2$ gives an LLL-reduced basis with the extra condition that each projected pair is reduced in the sense of [Lagrange-Gauss](/lagrange-gauss-reduction/) up to $\delta$; $\beta = n$ with $\delta = 1$ gives HKZ. A larger $\beta$ makes the Gram-Schmidt norms decrease more slowly.
- **Exact and deterministic.** With the exact oracle the output is a function of the input, $\beta$ and $\delta$. The shortest vector of a block is not unique, so implementations with different enumeration orders return different, equally valid bases.
- **The output is LLL-reduced.** So all LLL bounds hold for it as well, and the BKZ bounds are better for $\beta \ge 3$.
- **Not monotone in practice.** One tour can make $\|b_1\|$ shorter while making later Gram-Schmidt norms worse; the quality improves mostly in the first few tours.

## Variants and improvements

- **BKZ 2.0.** Chen and Nguyen (2011) added extreme pruning in the enumeration, early abort after a few tours, recursive preprocessing of blocks with a smaller block size, and a simulator that predicts the Gram-Schmidt profile from the Gaussian heuristic.
- **Sieving inside BKZ.** Replacing enumeration by [sieving](/lattice-sieving/), as in the G6K framework of Albrecht and coauthors (2019), was faster than enumeration from block sizes of about 70 to 80 in their experiments, and it set the records in the Darmstadt SVP challenge.
- **Slide reduction.** Gama and Nguyen (2008) reduce primal and dual blocks alternately; it reaches Mordell's inequality $\|b_1\| \le ((1 + \varepsilon) \gamma_\beta)^{(n-\beta)/(\beta-1)} \lambda_1$ for the [Hermite constant](/hermite-constant/) $\gamma_\beta$ in a polynomial number of oracle calls.
- **Self-dual and dual BKZ.** Micciancio and Walter (2016) apply the block step to the dual basis as well, which gives a more predictable output profile.
- **Deep-BKZ and terminating BKZ.** Using [deep LLL](/deep-lll/) inside the tours improves small block sizes; stopping after a fixed number of tours keeps the cost bounded.

## When to use it

- When LLL is not strong enough: for short vectors in dimension above about 50, as preprocessing before exact [enumeration](/lattice-enumeration/), and in cryptanalysis.
- For security estimates of [LWE](/learning-with-errors/), NTRU and other lattice schemes, which ask which block size $\beta$ reaches the required [root Hermite factor](/root-hermite-factor/) or solves the [unique SVP](/unique-svp/) instance, and price it by the cost of the oracle.
- Use LLL when polynomial-time guarantees matter more than quality, and slide reduction or self-dual BKZ when a proved bound on the number of oracle calls is needed.

## Pitfalls

- **Unbounded tours.** Waiting for full convergence can take very long for large $\beta$; practical code stops after a fixed number of tours or when the profile stops improving.
- **Inserting a non-primitive vector.** A vector with $\gcd(x) > 1$ generates a sublattice; with an exact oracle this cannot happen, but an approximate or pruned oracle can return such a vector, so the insertion must check for it or let LLL handle the dependence.
- **Stale Gram-Schmidt data.** After an insertion and LLL, the data of all positions from $k$ on change; reusing old values gives wrong blocks.
- **$\delta = 1$ in floating point.** The test at line L5 with $\delta = 1$ can loop on rounding errors; practical code uses $\delta = 0.99$.
- **Reading block size as cost.** The cost of BKZ depends on $\beta$ much more than on $n$; dimension 200 with $\beta = 20$ is easy, while $\beta = 100$ is a large computation.
- **Precision.** Floating-point BKZ needs enough precision for the Gram-Schmidt data of the whole basis; too little precision makes enumeration miss vectors or report wrong lengths.

## Implementations

## History

Korkine and Zolotarev defined the reduced quadratic forms behind HKZ reduction in 1873, and Kannan used them in 1983 for his shortest vector algorithm. Claus-Peter Schnorr introduced block Korkine-Zolotarev reduction in 1987 as a hierarchy of polynomial-time algorithms between LLL and HKZ, and proved its approximation factor. In 1994 Schnorr and Euchner gave the form used today, with tours over all blocks, floating-point arithmetic and zigzag enumeration, and used it on subset sum problems. Gama and Nguyen's experiments of 2008 turned it into the standard benchmark for lattice reduction; Chen and Nguyen's BKZ 2.0 of 2011 and the later sieving-based implementations made it the main tool of lattice cryptanalysis, and Hanrot, Pujol and Stehlé gave the first analysis of its output after a polynomial number of tours in 2011.

## References
