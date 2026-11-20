---
tag: RHRTRM
kind: algorithm
slug: discrete-empirical-interpolation-method
name: Discrete empirical interpolation method
aliases:
- DEIM
area: scientific-computing/uncertainty-quantification
level: advanced
summary: Picks interpolation indices greedily from POD modes of snapshots of the nonlinear term, so a reduced model evaluates it at few points.
model: real-ram
complexity:
  vars: {n: the length of the vectors, m: the number of basis vectors and indices}
  time: {selection: "O(n m^2 + m^4)", online: "O(m^2)"}
  space: {extra: "O(n m)"}
properties: {deterministic: true, exact: false, iterative: false, interpolatory: true}
history:
  year: 2010
  people: [Saifon Chaturantabut, Danny C. Sorensen]
  note: A discrete version of the empirical interpolation method, made for the nonlinear term of POD-Galerkin models of ODE systems from discretized PDEs.
prereqs: [empirical-interpolation-method, pod-galerkin-reduced-model, singular-value-decomposition]
see_also: [reduced-basis-method, operator-inference, principal-component-analysis, qr-decomposition, lagrange-interpolation, lebesgue-constant, burgers-equation]
sources:
  - paper: doi:10.1137/090766498
    title: Saifon Chaturantabut and Danny C. Sorensen, Nonlinear model reduction via discrete empirical interpolation, SIAM Journal on Scientific Computing 32(5), 2010, 2737-2764
    locator: the DEIM index selection, the error bound with the factor of the inverse of P^T U, and the bound (1 + sqrt(2n))^(m-1) / |u_1|_inf of that factor (Lemma 3.2)
  - paper: arxiv:1407.5516
    title: Danny C. Sorensen and Mark Embree, A DEIM induced CUR factorization, 2014 (published in SIAM Journal on Scientific Computing, 2016)
    locator: Lemma 4.4 of the arXiv version, the sharper bound sqrt(n m / 3) 2^m of the DEIM factor
  - paper: doi:10.1016/j.crma.2004.08.006
    title: Maxime Barrault, Yvon Maday, Ngoc Cuong Nguyen and Anthony T. Patera, An empirical interpolation method, application to efficient reduced-basis discretization of partial differential equations, Comptes Rendus Mathematique 339(9), 2004, 667-672
    locator: the greedy choice of interpolation points that DEIM applies to vectors
---

The discrete empirical interpolation method (DEIM) chooses $m$ entries of a vector of length $n$, so that the vector can be rebuilt from those entries alone. It works with a basis $U = [u_1, \ldots, u_m]$ that is given, usually the leading [POD](/pod-galerkin-reduced-model/) modes of snapshots of a nonlinear term $F(y)$. The approximation is

$$f \approx \hat{f} = U (P^T U)^{-1} P^T f ,$$

where $P^T f$ picks the chosen entries. DEIM picks the indices one at a time. The first index is where $|u_1|$ is largest. Each later index is where the residual of $u_l$ is largest, after $u_l$ is interpolated by the earlier vectors at the earlier indices. In a POD-Galerkin model this means that the nonlinear term is computed at $m$ entries in place of $n$, so the online cost no longer depends on $n$ when each entry of $F$ depends on a few entries of $y$. DEIM is the discrete form of the [empirical interpolation method](/empirical-interpolation-method/). The difference is in the basis: EIM builds the basis from the functions in the same greedy loop that picks the points, and controls the max-norm error on a training set. DEIM takes a basis that is already computed, often by an SVD, and only picks the indices, and its error bound is in the 2-norm, relative to the POD projection error.

## In plain words

A reduced model has a few unknowns, but its nonlinear term is still a long vector, and computing it touches the whole mesh. If that vector always looks like a mix of a few known shapes, then a few of its entries are enough to know the mix. DEIM decides which entries to look at. It looks where the shapes are large and where each new shape differs most from what the earlier shapes can already explain at the earlier entries. Then the full vector is rebuilt from those few entries.

## The problem

The input is a matrix $U \in \mathbb{R}^{n \times m}$ with linearly independent columns $u_1, \ldots, u_m$. The output is a list of distinct indices $p_1, \ldots, p_m$ such that $P^T U$ is invertible, where $P = [e_{p_1}, \ldots, e_{p_m}]$. For a vector $f$, the DEIM approximation $\hat{f}$ is the vector in the range of $U$ that agrees with $f$ at the chosen indices.

In a model $\dot{y} = A y + F(y)$ with a Galerkin basis $V \in \mathbb{R}^{n \times r}$ and $y \approx V a$, the reduced nonlinear term $V^T F(V a)$ becomes $V^T U (P^T U)^{-1} \cdot P^T F(V a)$. The $r \times m$ matrix $V^T U (P^T U)^{-1}$ is computed once. If $F$ acts entry by entry, $P^T F(V a) = F(P^T V a)$ needs only the $m$ rows $P^T V$. For a stencil, it needs the rows of the neighbours too.

## The algorithm

```pseudo id=main
DEIM(u_1..u_m)                                ▷ columns of length n, linearly independent
L1  p_1 ← the index of the largest |u_1(i)|; U ← [u_1]; P ← [e_p1]
L2  for l ← 2 to m do
L3      solve (P^T U) c = P^T u_l
L4      r ← u_l - U c
L5      p_l ← the index of the largest |r(i)|; U ← [U u_l]; P ← [P e_pl]
L6  return p_1..p_m
```

Line L3 interpolates $u_l$ by the first $l - 1$ columns at the first $l - 1$ indices. Line L4 forms the residual, which is 0 at those indices. Line L5 picks the index where the residual is largest. The order of the columns matters: the POD modes come in the order of their singular values, so the first indices serve the most important modes. The online stage stores an LU factorization of $P^T U$ and solves with it for each new $f$, in $O(m^2)$, plus the cost of the $m$ entries of $f$.

## Example

**By hand.** Take $u_1 = (1, 3, 2)$ and $u_2 = (2, 1, 4)$. The largest entry of $|u_1|$ is the second, so $p_1 = 2$. Interpolation of $u_2$ at index 2 gives $c = u_2(2)/u_1(2) = 1/3$, and the residual is $u_2 - u_1/3 = (5/3, 0, 10/3)$. Its largest entry is the third, so $p_2 = 3$. Then $P^T U = \begin{pmatrix} 3 & 1 \\ 2 & 4 \end{pmatrix}$. For $f = (1, 1, 1)$, $P^T f = (1, 1)$ gives $c = (3/10, 1/10)$ and $\hat{f} = 0.3 u_1 + 0.1 u_2 = (0.5, 1, 1)$, which agrees with $f$ at the indices 2 and 3.

**A parametrized function.** Take $s(x; \mu) = (1 - x) \cos(3\pi\mu(x + 1))\, e^{-(1 + x)\mu}$ on $n = 100$ equispaced points of $[-1, 1]$, a test function of the kind that Chaturantabut and Sorensen use, with 51 snapshots at equispaced $\mu \in [1, \pi]$. The singular values of the snapshot matrix fall from 24.8 to 0.476 at the 11th and to $4.8 \times 10^{-5}$ at the 21st. The first six DEIM indices are at $x = -1, -0.758, -0.677, -0.576, -0.495, -0.232$, near the left end, where the functions are largest. The table is a measurement from the test file. It gives the largest 2-norm error over 20 test values of $\mu$ between the snapshots, where $\|f\|_2 \le 5.72$.

| $m$ | $\|(P^T U)^{-1}\|_2$ | DEIM error | POD projection error | ratio |
|---|---|---|---|---|
| 2 | 2.79 | 3.744 | 3.555 | 1.05 |
| 6 | 3.68 | 0.7186 | 0.6316 | 1.14 |
| 10 | 7.11 | 0.1645 | 0.1051 | 1.57 |
| 15 | 5.31 | $7.947 \times 10^{-3}$ | $5.003 \times 10^{-3}$ | 1.59 |
| 20 | 5.66 | $3.135 \times 10^{-5}$ | $1.389 \times 10^{-5}$ | 2.26 |

The DEIM error is within a factor 2.3 of the best error in the same space, and the factor $\|(P^T U)^{-1}\|_2$ stays below 8, while the proved bound $(1 + \sqrt{2n})^{m-1} / \|u_1\|_\infty$ of Chaturantabut and Sorensen is $4.7 \times 10^{22}$ for $m = 20$, and the bound $\sqrt{nm/3}\, 2^m$ of Sorensen and Embree is $2.7 \times 10^7$.

## Correctness

The proof file shows, in exact arithmetic:

1. The indices are distinct and $P^T U$ is invertible at each step. In fact $P^T U = L T$, where $L$ is lower triangular with the nonzero residual values $r_l(p_l)$ on its diagonal and $T$ is upper triangular with a unit diagonal, so line L3 can always be solved.
2. $\hat{f}$ is the unique vector in the range of $U$ with $P^T \hat{f} = P^T f$, and $\hat{f} = f$ when $f$ is in the range.
3. If $U$ has orthonormal columns, then

$$\|f - \hat{f}\|_2 \le \|(P^T U)^{-1}\|_2\, \|(I - U U^T) f\|_2 .$$

So the DEIM error is the POD projection error times a factor that depends only on $U$ and the indices. The proof writes $f - \hat{f}$ in terms of $w = (I - U U^T) f$ only, splits it into a part orthogonal to the range of $U$ and a part in it, and uses that the rows of $P^T [U, U_\perp]$ are orthonormal. The bounds of the factor, $(1 + \sqrt{2n})^{m-1} / \|u_1\|_\infty$ and $\sqrt{nm/3}\, 2^m$, are cited, not proved here. The tests check the error bound, both factor bounds and, by brute force over all index sets for $n \le 8$, that the best index set is not worse than DEIM.

## Complexity

In the [real RAM](/real-ram/) model, step $l$ of the selection solves a system of size $l - 1$ in $O(l^3)$ and forms the residual in $O(n l)$, so the selection costs $O(n m^2 + m^4)$. An LU factorization that grows by one row and one column per step gives $O(n m^2 + m^3)$. The POD basis costs more than the selection: $O(n k^2 + k^3)$ for $k$ snapshots by the method of snapshots, as in the implementation. The online stage needs $m$ entries of $f$ and $O(m^2)$ for the two triangular solves. Memory is $O(n m)$ for $U$.

## Properties

- **Interpolatory.** $\hat{f}$ equals $f$ at the chosen indices and is exact on the range of $U$.
- **Greedy and deterministic.** No search over index sets; the result depends on the order of the columns.
- **Error relative to POD.** The error is at most $\|(P^T U)^{-1}\|_2$ times the best 2-norm error in the range of $U$.
- **Independent of the basis scaling of each column.** Scaling a column does not change the indices, because the residual of line L4 scales with it.
- **Online cost independent of $n$.** For an entry-wise or local nonlinear term.

## Variants and improvements

- **Q-DEIM.** Choose the indices by a QR factorization with column pivoting of $U^T$. It gives a better worst-case bound of the factor and uses standard [QR](/qr-decomposition/) software.
- **Oversampling.** Take more than $m$ indices and use least squares, which lowers the factor and makes the approximation less sensitive to noise.
- **Localized and adaptive DEIM.** Use several local bases for different regions of the state space, or update the basis and the indices online.
- **DEIM for CUR.** The same indices, applied to the left and right singular vectors, choose the rows and columns of a CUR factorization of a matrix.
- **Unassembled DEIM.** For finite elements, apply DEIM to the element contributions, so each chosen entry needs one element.

## When to use it

Use DEIM in a POD-Galerkin model, such as a reduced model of [Burgers' equation](/burgers-equation/), when the nonlinear term is local, so that a few of its entries need a few entries of the state, and when snapshots of the nonlinear term have fast singular value decay. Use EIM when you work with functions and want the basis and the points from the same greedy loop. Use [operator inference](/operator-inference/) when the nonlinearity is polynomial and you cannot change the code; then the reduced operators are learned and no entries are sampled. Do not use DEIM for a dense nonlinear term, such as an integral operator, because each entry then needs the whole state.

## Pitfalls

- **Snapshots of the wrong quantity.** The basis must come from snapshots of $F(y)$, not of $y$. A basis of the state can represent the nonlinear term badly.
- **Too few modes for the nonlinear term.** If $m$ is smaller than the Galerkin size $r$, the DEIM error can dominate and the reduced model can become unstable. Choose $m$ from the singular values of the nonlinear snapshots.
- **Stencils.** For a finite difference term, $F_i$ depends on $y_{i-1}, y_i, y_{i+1}$. The rows of $V$ for all these entries must be kept, so the cost is a small multiple of $m$.
- **Forming the factor online.** Solve with a stored LU factorization of $P^T U$; do not form $(P^T U)^{-1}$ and do not recompute the selection.
- **Loss of accuracy in the POD.** The method of snapshots squares the singular values, so modes with $\sigma_j < \sqrt{\varepsilon_{mach}}\, \sigma_1$ are inaccurate. Use an SVD of the snapshot matrix for very small singular values.

## Implementations

## History

Chaturantabut and Sorensen introduced DEIM in 2010, as a discrete version of the empirical interpolation method of Barrault, Maday, Nguyen and Patera from 2004, made for POD-Galerkin models of systems of ODEs from discretized nonlinear PDEs. They proved the error bound with the factor $\|(P^T U)^{-1}\|_2$ and a first bound of this factor. Sorensen and Embree used the same index selection for CUR factorizations in 2014 and gave a sharper bound of the factor.

## References
