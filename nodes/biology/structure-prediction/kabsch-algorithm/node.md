---
tag: P934Z2
kind: algorithm
slug: kabsch-algorithm
name: Kabsch algorithm
aliases:
- Kabsch superposition
- Kabsch-Umeyama algorithm
area: biology/structure-prediction
level: core
summary: Finds the rotation and translation of least RMSD between two matched 3D point sets from the SVD of their 3 by 3 covariance matrix, with a sign fix that excludes reflections.
solves: [optimal-superposition]
model: real-ram
complexity:
  vars: {N: the number of matched point pairs}
  time: {worst: Θ(N), average: Θ(N), best: Θ(N)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1976
  people: [Wolfgang Kabsch]
  note: Kabsch published the solution in Acta Crystallographica A in 1976 and a discussion of the case of a negative determinant, which gives a reflection, in 1978.
prereqs: [optimal-superposition, singular-value-decomposition, rmsd]
see_also: [quaternion-superposition, jacobi-eigenvalue-algorithm, symmetric-eigenproblem, structure-alignment, tm-score, gdt-ts]
sources:
  - paper: doi:10.1107/S0567739476001873
    title: Wolfgang Kabsch, A solution for the best rotation to relate two sets of vectors, Acta Crystallographica A32(5), 1976, 922-923
    locator: the whole note (the weighted least squares problem with the orthogonality constraint, the eigenvectors of the product of the correlation matrix with its transpose, and the construction of the rotation)
  - paper: doi:10.1107/S0567739478001680
    title: Wolfgang Kabsch, A discussion of the solution for the best rotation to relate two sets of vectors, Acta Crystallographica A34(5), 1978, 827-828
    locator: the whole note (the case of a negative determinant, where the plain solution is a reflection, and its correction)
  - paper: doi:10.1109/34.88573
    title: Shinji Umeyama, Least-squares estimation of transformation parameters between two point patterns, IEEE Transactions on Pattern Analysis and Machine Intelligence 13(4), 1991, 376-380
    locator: the main theorem (the optimal rotation V diag(1, ..., 1, d) U^T in any dimension, with the sign of the determinant, and the optimal scale)
  - paper: doi:10.1007/BF02289451
    title: Peter H. Schönemann, A generalized solution of the orthogonal Procrustes problem, Psychometrika 31(1), 1966, 1-10
    locator: the solution by the singular value decomposition, when reflections are allowed
  - paper: doi:10.1002/jcc.20110
    title: Evangelos A. Coutsias, Chaok Seok and Ken A. Dill, Using quaternions to calculate RMSD, Journal of Computational Chemistry 25(15), 2004, 1849-1857
    locator: the comparison of the SVD solution with the quaternion solution, and the treatment of the reflection case
---

The Kabsch algorithm computes the rotation $R$ and the translation $t$ that move one set of $N$ matched points onto a second set with the least [RMSD](/rmsd/). It solves the [optimal superposition](/optimal-superposition/) problem in three dimensions: it centers both sets, forms the $3 \times 3$ covariance matrix $H$, takes its [singular value decomposition](/singular-value-decomposition/) $H = U S V^{\mathsf T}$, and returns $R = V \operatorname{diag}(1, 1, d)\, U^{\mathsf T}$ with $d = \operatorname{sign}(\det(V U^{\mathsf T}))$. The sign $d$ is the fix of Kabsch's 1978 note: without it the answer can be a reflection, which no rigid motion of a protein can produce. The cost is $\Theta(N)$ time.

## In plain words

You have two copies of the same molecule, for example a model and the real structure. Each atom of one copy has a partner in the other copy. You want to turn and slide the first copy so that the partners come as close together as possible.

The slide is easy: put the center of each copy at the same place. The turn is the hard part. The method adds up, over all partners, how each direction of one copy lines up with each direction of the other. This gives a small table of nine numbers. A standard matrix tool splits the table into main directions, and the best turn maps those of one copy onto those of the other.

There is one trap. Sometimes the best match is a mirror image, which is not a turn. The method then flips the weakest direction and accepts a worse fit.

## The problem

**Input.** Points $x_1, \ldots, x_N$ and $y_1, \ldots, y_N$ in $\mathbb{R}^3$, with $N \ge 1$. The point $x_i$ is matched to $y_i$: for proteins these are usually the $C_\alpha$ atoms of residues that an alignment pairs.

**Output.** A rotation $R \in SO(3)$ (so $R^{\mathsf T} R = I$ and $\det R = +1$) and a vector $t \in \mathbb{R}^3$ that minimize

$$E(R, t) = \sum_{i=1}^{N} |R x_i + t - y_i|^2,$$

and the least RMSD $\sqrt{E/N}$. The [optimal superposition](/optimal-superposition/) page states the problem in full and proves that the best $t$ matches the two centroids.

## The algorithm

Let $\bar x$ and $\bar y$ be the centroids and $a_i = x_i - \bar x$, $b_i = y_i - \bar y$. Then $E = G_A + G_B - 2\operatorname{tr}(RH)$ with $G_A = \sum |a_i|^2$, $G_B = \sum |b_i|^2$ and $H = \sum a_i b_i^{\mathsf T}$, so the task is to maximize $\operatorname{tr}(RH)$ over rotations. With the SVD $H = U S V^{\mathsf T}$, the answer is $R = V \operatorname{diag}(1, 1, d)\, U^{\mathsf T}$. Kabsch (1976) did not call a general SVD routine. He took the eigenvectors of the symmetric matrix $H^{\mathsf T} H$, which are the right singular vectors, and built the left ones from them. The pseudocode follows that route, and makes both $U$ and $V$ proper, which builds the sign $d$ into the construction.

```pseudo id=main
KABSCH(X, Y)                                ▷ x_i is matched to y_i, i = 1 .. N
L1  x̄ ← (1/N) Σ x_i ;  ȳ ← (1/N) Σ y_i
L2  a_i ← x_i − x̄ ;  b_i ← y_i − ȳ          for i = 1 .. N
L3  H ← Σ a_i b_iᵀ                            ▷ 3 × 3 covariance
L4  (s_k², v_k), k = 1, 2, 3 ← eigenpairs of HᵀH, with s_1 ≥ s_2 ≥ s_3 ≥ 0
L5  if det[v_1 v_2 v_3] < 0 then v_3 ← −v_3   ▷ make V proper
L6  u_1 ← H v_1 / s_1 ;  u_2 ← H v_2 / s_2     ▷ if s_2 = 0: any unit u_2 ⊥ u_1
L7  u_3 ← u_1 × u_2                           ▷ makes U proper: this is the sign fix
L8  R ← v_1 u_1ᵀ + v_2 u_2ᵀ + v_3 u_3ᵀ          ▷ R = V Uᵀ
L9  t ← ȳ − R x̄
L10 E ← Σ|a_i|² + Σ|b_i|² − 2 tr(R H)
L11 return R, t, √(max(E, 0) / N)
```

Lines L1 to L3 are the only work that depends on $N$. Line L4 solves a $3 \times 3$ [symmetric eigenproblem](/symmetric-eigenproblem/); the implementation uses the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/). Since $H^{\mathsf T} H = V S^2 U^{\mathsf T} U S V^{\mathsf T} = V S^2 V^{\mathsf T}$, its eigenvectors are the right singular vectors of $H$, and $H v_k = s_k u_k$ gives the left ones in line L6. Line L7 does not compute $u_3 = H v_3 / s_3$. It takes the cross product instead, so $\det U = +1$. Then $H v_3 = \sigma u_3$ with $\sigma = \pm s_3$, and the sign of $\sigma$ is the sign of $\det H$. When $\sigma < 0$, the plain SVD would have $\det(V U^{\mathsf T}) = -1$ and $d = -1$, and $V U^{\mathsf T}$ with the proper $U$ of line L7 is exactly $V \operatorname{diag}(1, 1, -1)\, U_{\text{svd}}^{\mathsf T}$. So line L8 always returns a rotation, and it is the best one. Line L10 uses $\operatorname{tr}(RH) = s_1 + s_2 + \sigma$.

## Example

Take the four points $x_1 = (0,0,0)$, $x_2 = (2,0,0)$, $x_3 = (0,3,0)$, $x_4 = (0,0,4)$, and let $y_i$ be $x_i$ turned by $90°$ about the $z$ axis and moved by $(1, 2, 3)$: $y = (1,2,3), (1,4,3), (-2,2,3), (1,2,7)$.

| step | value |
|---|---|
| L1 | $\bar x = (0.5, 0.75, 1)$, $\bar y = (0.25, 2.5, 4)$ |
| L3 | $H = \begin{pmatrix} 1.5 & 3 & -2 \\ -6.75 & -1.5 & -3 \\ 3 & -2 & 12 \end{pmatrix}$, $\det H = 144$ |
| L4 | eigenvalues of $H^{\mathsf T}H$: $182.4361, 44.0459, 2.5805$, so $s = (13.5069, 6.6367, 1.6064)$ |
| L7 | $\det H > 0$, so $\sigma = +s_3$ and no flip is needed |
| L8 | $R = \begin{pmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix}$, the $90°$ turn |
| L9 | $t = (1, 2, 3)$ |
| L10 | $G_A = G_B = 21.75 = s_1 + s_2 + s_3$, so $E = 0$ and the RMSD is 0 |

Now let $y_i$ be the mirror image of $x_i$ in the plane $z = 0$: $y_4 = (0, 0, -4)$ and the other points stay. The covariance has the same singular values, but $\det H = -144$. The plain SVD gives $V U^{\mathsf T} = \operatorname{diag}(1, 1, -1)$: the mirror itself, with RMSD 0, but it is not a rotation. With the fix, $\sigma = -1.6064$, $\operatorname{tr}(RH) = 13.5069 + 6.6367 - 1.6064 = 18.5372$, and

$$E = 43.5 - 2 \cdot 18.5372 = 6.4256, \qquad \text{RMSD} = \sqrt{6.4256 / 4} = 1.2674.$$

This is the true minimum over rotations. The [quaternion method](/quaternion-superposition/) gives the same value on this input.

## Correctness

The proof has three steps. First, for a fixed $R$, the best $t$ is $\bar y - R\bar x$, and then $E = G_A + G_B - 2\operatorname{tr}(RH)$. Second, with $H = U S V^{\mathsf T}$ and $d = \det U \det V$, the substitution $W = V^{\mathsf T} R U$ gives $\operatorname{tr}(RH) = \sum_k W_{kk} s_k$ over the orthogonal $W$ with $\det W = d$. This is at most $s_1 + s_2 + d\, s_3$, with equality at $W = \operatorname{diag}(1, 1, d)$. The case $d = -1$ needs the fact that a rotation by $\theta$ about the axis $n$ has diagonal entries $\cos\theta + (1 - \cos\theta) n_k^2$. Third, lines L4 to L8 build exactly this $R$, including the cases where the points lie on a line or coincide. The full proof is below.

## Complexity

Lines L1 to L3 take a constant number of operations for each point, so they cost $\Theta(N)$. Lines L4 to L11 work on $3 \times 3$ matrices only. In the [real RAM](/real-ram/) with square roots, the eigenvalues of a $3 \times 3$ symmetric matrix have a closed form by the cubic formula, so these lines take $O(1)$ time. In floating point, a Jacobi solver converges quadratically, and a fixed cap of sweeps is enough. The total time is $\Theta(N)$ in each case, which is optimal, because each point must be read.

The extra space is $\Theta(1)$ if the code accumulates $H$ with $H = \sum x_i y_i^{\mathsf T} - N \bar x \bar y^{\mathsf T}$ instead of storing the centered copies; the reference code stores them, for clarity, and uses $\Theta(N)$.

## Properties

- **Exact.** In exact arithmetic the answer is the global minimum. No search and no starting guess are needed.
- **Proper.** The result has $\det R = +1$ by construction.
- **Unique in most cases.** The optimal $R$ is unique when $s_2 > 0$ and, in the case $d = -1$, $s_2 > s_3$. If the points lie on one line ($s_2 = 0$), each turn about that line is also optimal. If $d = -1$ and $s_2 = s_3$, each turn about the first singular axis is also optimal.
- **Symmetric in a weak sense.** Swapping the roles of $X$ and $Y$ gives $R^{\mathsf T}$ and the same RMSD.

## Variants and improvements

- **Weights.** Kabsch's 1976 note minimizes $\sum w_i |R x_i - y_i|^2$. Use weighted centroids and $H = \sum w_i a_i b_i^{\mathsf T}$.
- **Scale.** Umeyama (1991) adds a scale factor $c$ to $c R x + t$ and gives the same sign fix in any dimension.
- **Reflections allowed.** If reflections are allowed, the answer is $V U^{\mathsf T}$ from the plain SVD. This is the orthogonal Procrustes problem of Schönemann (1966).
- **Quaternions.** The [quaternion method](/quaternion-superposition/) of Horn (1987) finds the same rotation as the top eigenvector of a $4 \times 4$ symmetric matrix and never meets the reflection case. The QCP method of Theobald (2005) gets the least RMSD from the characteristic polynomial without forming $R$.

## When to use it

Use the Kabsch algorithm whenever two point sets are already matched one to one: to compare a model with a native structure, to compare frames of a simulation, or as the inner step of an [alignment](/structure-alignment/) method that alternates between a match and a fit. If a library SVD is at hand, the SVD form is the shortest correct code. If you need only the RMSD of many pairs, the QCP route of the quaternion method is faster. If the matching is not known, Kabsch alone does not help, because the RMSD depends on the match.

## Pitfalls

- **No sign fix.** The line $R \leftarrow V U^{\mathsf T}$ from a library SVD returns a reflection with $\det R = -1$ when $\det H < 0$. Use $R = V \operatorname{diag}(1, 1, d)\, U^{\mathsf T}$ with $d = \operatorname{sign}(\det(V U^{\mathsf T}))$, or the cross product of line L7.
- **The wrong transpose.** With $H = \sum a_i b_i^{\mathsf T}$ the rotation that moves $x$ onto $y$ is $V U^{\mathsf T}$. With $H = \sum b_i a_i^{\mathsf T}$ it is $U V^{\mathsf T}$. Mixing the two conventions gives $R^{\mathsf T}$, which turns the structure the wrong way.
- **No centering.** If lines L1 and L2 are skipped, $H$ mixes the translation into the rotation and the answer is wrong for any input whose centroids differ.
- **Loss of precision.** Line L4 squares $H$. A singular value near $10^{-8} s_1$ then has the size of the rounding error of $s_1^2$, so the computed $u_2$ can be poor for points close to a line. A library SVD of $H$ itself, or the quaternion method, avoids the squaring.
- **A negative $E$.** When the fit is perfect, line L10 can return a tiny negative number from rounding. Take $\max(E, 0)$ before the square root, as in line L11. The RMSD of a perfect fit is then about the square root of the rounding error, near $10^{-7}$ for coordinates of size 10.

## Implementations

## History

Kabsch published the method in 1976, in a one-page note in Acta Crystallographica, for the comparison of crystal structures. In 1978 he discussed the case of a negative determinant, where the plain construction gives a reflection, and how to correct it. The same matrix problem, with reflections allowed, had been solved in psychometrics as the orthogonal Procrustes problem by Schönemann in 1966. Horn gave the quaternion form in 1987, and Umeyama extended the sign fix to any dimension, with a scale, in 1991. In computer vision the method is often called the Kabsch-Umeyama algorithm.

## References
