---
tag: 4MBFM8
kind: algorithm
slug: cyclic-reduction
name: Cyclic reduction
aliases:
- odd-even reduction
- odd-even elimination
- CR
area: numerical/linear-systems
level: advanced
summary: Eliminate every other unknown recursively, suited to parallel tridiagonal solves.
solves: [tridiagonal-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the order of the tridiagonal matrix, at least 1"}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
  flops: {worst: "17 n - O(log n)"}
  span: {worst: Θ(log n)}
properties: {deterministic: true, in_place: false, recursive: true, parallel: true}
prereqs: [tridiagonal-system-solving, gaussian-elimination, schur-complement]
see_also: [thomas-algorithm, diagonally-dominant-matrix, positive-definite-matrix, partial-pivoting, parallel-prefix, poisson-equation, banded-matrix, growth-factor]
sources:
  - paper: doi:10.1145/321250.321259
    title: R. W. Hockney, A fast direct solution of Poisson's equation using Fourier analysis, Journal of the ACM 12(1), 1965
    locator: pp. 95 to 113 (odd-even reduction of the tridiagonal systems, credited there to G. H. Golub)
  - paper: doi:10.1137/0707049
    title: B. L. Buzbee, G. H. Golub and C. W. Nielson, On direct methods for solving Poisson's equations, SIAM Journal on Numerical Analysis 7(4), 1970
    locator: pp. 627 to 656 (block cyclic reduction, its instability for the Poisson problem, and the Buneman variant)
  - paper: doi:10.1137/0713042
    title: Don Heller, Some aspects of the cyclic reduction algorithm for block tridiagonal linear systems, SIAM Journal on Numerical Analysis 13(4), 1976
    locator: pp. 484 to 496 (quadratic decrease of the off-diagonal blocks under diagonal dominance, incomplete reduction)
  - paper: "P. Amodio and F. Mazzia, Backward error analysis of cyclic reduction for the solution of tridiagonal systems, Mathematics of Computation 62(206), 1994"
    title: Backward error analysis of cyclic reduction for the solution of tridiagonal systems
    locator: pp. 601 to 617
  - paper: doi:10.1145/321738.321741
    title: Harold S. Stone, An efficient parallel algorithm for the solution of a tridiagonal linear system of equations, Journal of the ACM 20(1), 1973
    locator: pp. 27 to 38 (recursive doubling, a log n depth alternative)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 4.5, Block Tridiagonal Systems (block cyclic reduction)
  - paper: "Walter Gander and Gene H. Golub, Cyclic reduction: history and applications, in Scientific Computing, Proceedings of the Workshop, Hong Kong, Springer, 1997"
    title: "Cyclic reduction: history and applications"
    locator: pp. 73 to 85 (survey)
---

Cyclic reduction solves a tridiagonal system $A x = d$ by eliminating the unknowns with even index from the equations with odd index, all at once. What remains is a tridiagonal system of half the size in the odd unknowns; repeating this $\lfloor \log_2 n \rfloor$ times leaves one equation, and the eliminated unknowns are recovered level by level in reverse. Every equation of a level is processed independently, so with $n$ processors the solve takes $O(\log n)$ parallel steps, against the $n$ sequential steps of the [Thomas algorithm](/thomas-algorithm/). The price is about $17 n$ flops instead of $8 n$. Algebraically the method is Gaussian elimination without pivoting on $P A P^T$ for an odd-even permutation $P$, so it is stable for the same matrices where elimination without pivoting is: strictly diagonally dominant and symmetric positive definite ones. For those the off-diagonal part shrinks quadratically from level to level.

## In plain words

In a tridiagonal system each unknown appears only next to its two neighbours. Use every even numbered equation to express its unknown through the two odd numbered neighbours, and substitute that into the odd numbered equations. Now the odd unknowns form a system just like the original, half as long. Do it again and again until one unknown is left, solve it, then fill in the others on the way back. All the substitutions at one stage are separate from each other, so many processors can do them at the same time.

## The problem

Given a tridiagonal $A \in \mathbb{R}^{n \times n}$ with subdiagonal $a_i$, diagonal $b_i$ and superdiagonal $c_i$, so that row $i$ reads $a_i x_{i-1} + b_i x_i + c_i x_{i+1} = d_i$ for $i = 0, \ldots, n-1$ (with $a_0 = c_{n-1} = 0$), find $x$. See [tridiagonal system solving](/tridiagonal-system-solving/).

**Notation.** Indices start at $0$. A level of the method maps a system of order $N$ to one of order $\lfloor N/2 \rfloor$ in the unknowns $x_1, x_3, x_5, \ldots$. $\hat x$ is the computed solution, $r = d - A \hat x$, $u = 2^{-53}$, and the normwise backward error is $\eta = \|r\|_\infty / (\|A\|_\infty \|\hat x\|_\infty + \|d\|_\infty)$. For strict row diagonal dominance, $\beta(A) = \max_i (|a_i| + |c_i|)/|b_i| < 1$.

## The algorithm

For an odd row $i$, multiply row $i - 1$ by $\alpha_i = -a_i / b_{i-1}$ and row $i + 1$ by $\gamma_i = -c_i / b_{i+1}$ and add them to row $i$. This removes $x_{i-1}$ and $x_{i+1}$ and brings in $x_{i-2}$ and $x_{i+2}$:

$$a_i' = \alpha_i a_{i-1}, \quad b_i' = b_i + \alpha_i c_{i-1} + \gamma_i a_{i+1}, \quad c_i' = \gamma_i c_{i+1}, \quad d_i' = d_i + \alpha_i d_{i-1} + \gamma_i d_{i+1}.$$

When $i + 1 = N$ the $\gamma$ terms are absent.

```pseudo id=main
CYCLIC-REDUCTION(a, b, c, d)
L1  copy the system; set a₀ ← 0 and c_{n−1} ← 0; push nothing yet
L2  while the current system has order N > 1 do  (push it, then reduce)
L3      for every odd i < N, in parallel do
L4          α ← −aᵢ / b_{i−1}   (fail if b_{i−1} = 0)
L5          γ ← −cᵢ / b_{i+1} if i + 1 < N, else γ ← 0
L6          new row ⌊i/2⌋: α·a_{i−1}, bᵢ + α·c_{i−1} + γ·a_{i+1}, γ·c_{i+1}, dᵢ + α·d_{i−1} + γ·d_{i+1}
L7  x₀ ← d₀ / b₀ for the final 1 by 1 system  (fail if b₀ = 0)
L8  while a pushed system remains do  (pop it)
L9      place the known values: x_{2k+1} ← (solution of the reduced system)ₖ
L10     for every even i < N, in parallel do
L11         xᵢ ← (dᵢ − aᵢ x_{i−1} − cᵢ x_{i+1}) / bᵢ
L12 return x
```

The code stores the levels and raises an error at the first zero pivot. A level of order $N$ needs about $2.5 N$ numbers of new storage, and the levels together fewer than $4 n$.

## Example

Take the second difference matrix $A = \operatorname{tridiag}(-1, 2, -1)$ of order $7$ and $d = (1, 0, 0, 0, 0, 0, 1)^T$, so that $x = (1, \ldots, 1)$. At the first level every $\alpha_i = \gamma_i = 1/2$:

| level | order | subdiagonal | diagonal | superdiagonal | right-hand side |
|---|---|---|---|---|---|
| 0 | 7 | $-1$ | $2$ | $-1$ | $(1, 0, 0, 0, 0, 0, 1)$ |
| 1 | 3 | $-1/2$ | $1$ | $-1/2$ | $(1/2, 0, 1/2)$ |
| 2 | 1 | | $1/2$ | | $(1/2)$ |

At level 1, row $3$ for instance becomes $b_3' = 2 - \frac12 - \frac12 = 1$, $a_3' = \frac12 \cdot (-1)$ and $d_3' = 0$. At level 2, $\alpha = \gamma = 1/2$ again and $b'' = 1 - \frac14 - \frac14 = \frac12$, $d'' = \frac14 + \frac14 = \frac12$, so $x_3 = 1$. Back substitution gives $x_1 = (\frac12 + \frac12 x_3)/1 = 1$ and $x_5 = 1$, then $x_0 = (1 + x_1)/2 = 1$, $x_2 = (x_1 + x_3)/2 = 1$, and so on. Every level is half the previous matrix, $2^{-j} \operatorname{tridiag}(-1, 2, -1)$: the constant coefficient structure survives, which is what made the method attractive for the [Poisson equation](/poisson-equation/). The count is $71 = 17 \cdot 7 - 16 \cdot 3$ flops.

## Correctness

The proofs are in `proofs/correctness.md`.

1. **Reduction (proved).** Each level replaces the odd equations by the [Schur complement](/schur-complement/) of the even unknowns: because no two even unknowns are coupled, that block is diagonal, and the complement is tridiagonal with the entries of line L6. So $x$ solves the system if and only if its odd part solves the reduced system and its even part satisfies line L11.
2. **Equivalence with elimination (proved).** Cyclic reduction performs Gaussian elimination without pivoting on $P A P^T$, where $P$ lists the even indices of level $0$, then those of level $1$, and so on. Therefore it succeeds exactly when all leading principal minors of $P A P^T$ are nonzero, and it reports failure for every singular $A$.
3. **No breakdown for dominant and SPD matrices (proved).** If $A$ is strictly diagonally dominant by rows, so is every reduced matrix, and in fact $\beta(A') \le \beta(A)^2$ (Heller 1976 proves the block version). If $A$ is symmetric positive definite, so is every reduced matrix. In both cases no pivot is zero.
4. **Termination.** Each level reduces the order from $N \ge 2$ to $\lfloor N/2 \rfloor \ge 1$, so there are $\lfloor \log_2 n \rfloor$ levels.

**Floating point.** By item 2 the computed solution is that of elimination without pivoting on $P A P^T$, with a different order of operations. For strictly diagonally dominant and SPD tridiagonal matrices Amodio and Mazzia (1994) prove a backward error bound of the form $\|\Delta A\| \le c(n)\, u \|A\|$ with $c(n)$ growing slowly in $n$ (proved, worst case); the quadratic decrease of $\beta$ means the reduced matrices become nearly diagonal, which limits growth. On $1000$ random systems of order up to $120$ the tests observe $\eta \le u \log_2(n + 1)$. Without dominance there is no such guarantee: for $A = \begin{pmatrix} \epsilon & 1 \\ 1 & 1 \end{pmatrix}$ with $\epsilon = 10^{-17}$ and $d = (1, 2)$, the method computes $\hat x = (0, 1)$ instead of about $(1, 1)$, a backward error of order $1$, just as Thomas without pivoting does.

## Complexity

For $n = 2^k - 1$ every level has odd order and the flop count is exactly $17 n - 16 k$: a reduced row with two neighbours costs $12$ flops (two divisions, six multiplications, four additions), and a recovered even unknown costs $5$, or $3$ at the two ends of a level. In general it is at most $17 n$ and at least $17 n - 22 \log_2 n - 16$. That is about $2.1$ times the $8 n - 7$ of the Thomas algorithm. The time is $\Theta(n)$ and the extra storage $\Theta(n)$. With one processor per row, every level of lines L3 to L6 and of lines L10 to L11 takes $O(1)$ steps, so the span is $\Theta(\log n)$. Proofs are in `proofs/complexity.md`.

## Properties

- **Parallel**: $\Theta(n)$ work and $\Theta(\log n)$ span. Thomas has $\Theta(n)$ span because each step needs the previous pivot.
- **No pivoting**, and therefore a restricted domain: the same matrices as Gaussian elimination without pivoting, up to the permutation.
- **Structure preserving**: on constant coefficient (Toeplitz) tridiagonal matrices of order $2^k - 1$, every level is again Toeplitz.
- **Generalizes to blocks**: with $b_i$, $a_i$, $c_i$ square blocks the same formulas give block cyclic reduction, the basis of fast Poisson solvers.
- **Deterministic**, and in exact arithmetic it gives the exact solution.

## Variants and improvements

- **Block cyclic reduction** (Hockney 1965, Buzbee, Golub and Nielson 1970). For the 2D Poisson problem the blocks are polynomials in the 1D matrix, so they never need to be formed. The plain version loses accuracy in the right-hand side recurrence; the Buneman variant (1969) reorganizes it into a stable form. Combined with FFTs this gives the FACR solvers in $O(n \log \log n)$ flops for $n$ grid points.
- **Parallel cyclic reduction** (Hockney and Jesshope). Reduce all equations at every level, not only the odd ones; after $\lceil \log_2 n \rceil$ levels every equation is decoupled. No back substitution, but $\Theta(n \log n)$ work. Hybrids switch between CR and PCR, as in GPU tridiagonal solvers.
- **Recursive doubling** (Stone 1973). Write Thomas' recurrences as products of $2 \times 2$ or $3 \times 3$ matrices and evaluate them with [parallel prefix](/parallel-prefix/); also $\Theta(\log n)$ span, with different stability properties.
- **Incomplete cyclic reduction** (Heller 1976). Since $\beta$ squares at every level, after a few levels the off-diagonal entries are below $u |b_i|$ and can be dropped, saving the last levels.
- **Partition methods** (Wang 1981, SPIKE). Split the matrix into $p$ blocks, solve them independently, then solve a small reduced system; better suited to $p \ll n$ processors.
- **Cyclic reduction for matrix equations.** For quasi-birth-death Markov chains and quadratic matrix equations, cyclic reduction converges quadratically (Bini, Latouche and Meini).

## When to use it

Use it on parallel hardware (GPUs, vector machines, SIMD lanes) for many tridiagonal systems of moderate size, or for one large system when the span matters, provided the matrix is diagonally dominant or SPD, as for implicit time stepping, splines and ADI methods. On one core, for a single system, the [Thomas algorithm](/thomas-algorithm/) does less than half the work and fewer memory passes. For a general tridiagonal matrix that may need row interchanges use LU with [partial pivoting](/partial-pivoting/) (LAPACK `gtsv`).

## Pitfalls

- **No pivoting.** A nonsingular matrix such as $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ breaks down at the first division, and small pivots produce large errors. Check dominance or definiteness first.
- **Memory traffic.** Each level reads and writes the whole remaining system with stride $2^j$, so on cache based machines the method is limited by memory bandwidth long before flops; store the levels contiguously.
- **Non power of two sizes.** When $N$ is even, the last odd row has no right neighbour; forgetting this reads out of bounds or uses a stale $c_{N-1}$.
- **The Poisson block version.** The plain block recurrence for the right-hand side is unstable; use the Buneman form.
- **Breakdown detection.** In floating point a singular matrix may give a tiny pivot instead of an exact zero; a test against zero is not a singularity test. Estimate the condition number if it matters.

## Implementations

## History

Gene Golub suggested odd-even reduction to Roger Hockney, who used it in 1965 in his fast Poisson solver for plasma simulation, together with Fourier analysis in the other direction. Buzbee, Golub and Nielson (1970) gave the block version and its analysis, including Buneman's stable variant. Heller (1976) proved the quadratic decrease of the off-diagonal blocks under diagonal dominance, and Amodio and Mazzia (1994) gave the backward error analysis. With vector and then GPU hardware the scalar method and its parallel variant became standard parallel tridiagonal solvers.

## References
