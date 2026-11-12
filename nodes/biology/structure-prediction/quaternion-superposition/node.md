---
tag: AMR9P8
kind: algorithm
slug: quaternion-superposition
name: Quaternion-based superposition
aliases:
- Horn's method
- Quaternion RMSD
- QCP method
area: biology/structure-prediction
level: advanced
summary: Finds the least-RMSD rotation between matched 3D point sets as the top eigenvector of a symmetric 4 by 4 matrix, a unit quaternion, so a reflection can never occur.
solves: [optimal-superposition]
model: real-ram
complexity:
  vars: {N: the number of matched point pairs}
  time: {worst: Θ(N), average: Θ(N), best: Θ(N)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1987
  people: [Berthold K. P. Horn, Simon K. Kearsley, Douglas L. Theobald]
  note: Horn gave the closed form with unit quaternions in 1987, Kearsley gave it for molecules in 1989, and Theobald made it fast with the QCP method in 2005.
prereqs: [optimal-superposition, symmetric-eigenproblem, eigenvector]
see_also: [kabsch-algorithm, rayleigh-quotient, jacobi-eigenvalue-algorithm, power-iteration, newton-raphson-method, rmsd]
sources:
  - paper: doi:10.1364/JOSAA.4.000629
    title: Berthold K. P. Horn, Closed-form solution of absolute orientation using unit quaternions, Journal of the Optical Society of America A 4(4), 1987, 629-642
    locator: the reduction of the best rotation to the eigenvector of the largest eigenvalue of a symmetric 4 by 4 matrix built from the cross-covariance matrix
  - paper: doi:10.1107/S0108767388010128
    title: Simon K. Kearsley, On the orthogonal transformation used for structural comparisons, Acta Crystallographica A45(2), 1989, 208-210
    locator: the quaternion form of the least-squares superposition of molecules
  - paper: doi:10.1107/S0108767305015266
    title: Douglas L. Theobald, Rapid calculation of RMSDs using a quaternion-based characteristic polynomial, Acta Crystallographica A61(4), 2005, 478-480
    locator: the coefficients of the characteristic polynomial and the Newton iteration started at (G_A + G_B)/2
  - paper: doi:10.1002/jcc.20110
    title: Evangelos A. Coutsias, Chaok Seok and Ken A. Dill, Using quaternions to calculate RMSD, Journal of Computational Chemistry 25(15), 2004, 1849-1857
    locator: the derivation of the quaternion method, its equivalence to the SVD method, and the eigenvalues of the 4 by 4 matrix
---

The quaternion method computes the rotation of least [RMSD](/rmsd/) between two sets of $N$ matched points as the top [eigenvector](/eigenvector/) of a symmetric $4 \times 4$ matrix. It solves the same [optimal superposition](/optimal-superposition/) problem as the [Kabsch algorithm](/kabsch-algorithm/), and it gives the same answer. The eigenvector is a unit quaternion, and each unit quaternion is a proper rotation, so a reflection cannot occur and no sign fix is needed. The least RMSD is $\sqrt{(G_A + G_B - 2\lambda_{\max})/N}$, where $\lambda_{\max}$ is the top eigenvalue. The QCP variant finds $\lambda_{\max}$ by Newton's method on the characteristic polynomial and gets the RMSD without the rotation. The cost is $\Theta(N)$ time.

## In plain words

You have two copies of a molecule with matched atoms, and you want the turn that brings the partners closest together. A turn in space can be written with four numbers, called a quaternion. Any set of four numbers, scaled to length one, is a real turn and never a mirror image.

The method adds up how the two copies line up, direction by direction, and puts the result into a small square table of sixteen numbers. The quality of each possible turn is then a simple expression of its four numbers and this table. The best turn is the direction in which the table stretches vectors the most, a standard question with a standard answer. The size of that stretch also gives the best possible fit at once, before you even build the turn.

## The problem

**Input.** Points $x_1, \ldots, x_N$ and $y_1, \ldots, y_N$ in $\mathbb{R}^3$, with $N \ge 1$ and $x_i$ matched to $y_i$, for example the $C_\alpha$ atoms of aligned residues, in Å.

**Output.** A rotation $R \in SO(3)$ and a vector $t$ that minimize $E(R, t) = \sum_i |R x_i + t - y_i|^2$, and the least RMSD $\sqrt{E/N}$ in Å. The [optimal superposition](/optimal-superposition/) page states the problem in full.

## The algorithm

Center both sets: $a_i = x_i - \bar x$ and $b_i = y_i - \bar y$. The best translation matches the centroids, and then $E = G_A + G_B - 2\operatorname{tr}(RS)$ with $G_A = \sum |a_i|^2$, $G_B = \sum |b_i|^2$ and $S = \sum a_i b_i^{\mathsf T}$. A unit quaternion $q = (w, x, y, z)$ gives the rotation

$$R(q) = \begin{pmatrix} w^2 + x^2 - y^2 - z^2 & 2(xy - wz) & 2(xz + wy) \\ 2(xy + wz) & w^2 - x^2 + y^2 - z^2 & 2(yz - wx) \\ 2(xz - wy) & 2(yz + wx) & w^2 - x^2 - y^2 + z^2 \end{pmatrix}.$$

The entries of $R(q)$ are quadratic in $q$, so $\operatorname{tr}(R(q) S)$ is a quadratic form $q^{\mathsf T} N q$. Horn's matrix is

$$N = \begin{pmatrix} S_{xx} + S_{yy} + S_{zz} & S_{yz} - S_{zy} & S_{zx} - S_{xz} & S_{xy} - S_{yx} \\ S_{yz} - S_{zy} & S_{xx} - S_{yy} - S_{zz} & S_{xy} + S_{yx} & S_{zx} + S_{xz} \\ S_{zx} - S_{xz} & S_{xy} + S_{yx} & -S_{xx} + S_{yy} - S_{zz} & S_{yz} + S_{zy} \\ S_{xy} - S_{yx} & S_{zx} + S_{xz} & S_{yz} + S_{zy} & -S_{xx} - S_{yy} + S_{zz} \end{pmatrix}.$$

The best rotation maximizes $q^{\mathsf T} N q$ over $|q| = 1$, which is the [Rayleigh quotient](/rayleigh-quotient/) of $N$. Its maximum is $\lambda_{\max}(N)$, at the top eigenvector.

```pseudo id=main
QUATERNION-SUPERPOSITION(X, Y)              ▷ x_i is matched to y_i, i = 1 .. N
L1  center: a_i ← x_i − x̄, b_i ← y_i − ȳ;  G_A ← Σ|a_i|², G_B ← Σ|b_i|²
L2  S ← Σ a_i b_iᵀ                            ▷ 3 × 3 covariance
L3  N ← Horn's 4 × 4 symmetric matrix of S
L4  (λ_max, q) ← the largest eigenvalue of N and a unit eigenvector
L5  R ← R(q)
L6  t ← ȳ − R x̄
L7  return R, t, √(max(G_A + G_B − 2 λ_max, 0) / N)
```

The implementation solves line L4 with the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/), which returns all four eigenpairs of a symmetric matrix.

**QCP.** If only the RMSD is needed, lines L4 to L6 can be replaced by a root search. The characteristic polynomial is $P(\lambda) = \lambda^4 + c_2\lambda^2 + c_1\lambda + c_0$ with $c_2 = -2\sum_{r,c} S_{rc}^2$, $c_1 = -8\det S$ and $c_0 = \det N$ (the $\lambda^3$ term is 0 because $\operatorname{tr} N = 0$). Theobald's QCP method runs [Newton's method](/newton-raphson-method/) on $P$ from $\lambda_0 = (G_A + G_B)/2$. This start is never below $\lambda_{\max}$, because $E \ge 0$, and all roots of $P$ are real, so the iteration decreases to $\lambda_{\max}$ without overshoot.

## Example

Take $x = (0,0,0), (2,0,0), (0,3,0), (0,0,4)$, and let $y_i$ be $x_i$ turned by $90°$ about the $z$ axis and moved by $(1,2,3)$. Then $G_A = G_B = 21.75$ and

$$N = \begin{pmatrix} 12 & -1 & 5 & 9.75 \\ -1 & -9 & -3.75 & 1 \\ 5 & -3.75 & -15 & -5 \\ 9.75 & 1 & -5 & 12 \end{pmatrix}.$$

| step | rotation case | mirror case ($z \to -z$) |
|---|---|---|
| L4: eigenvalues of $N$ | $21.75, 5.2638, -8.4766, -18.5372$ | $18.5372, 8.4766, -5.2638, -21.75$ |
| L4: $q$ | $(0.7071, 0, 0, 0.7071)$ | $(0.2866, 0.4185, -0.8618, 0)$ |
| L5: $R(q)$ | the $90°$ turn about $z$ | a proper rotation, $\det R = +1$ |
| L7: $E = 43.5 - 2\lambda_{\max}$ | $0$ | $6.4256$ |
| L7: RMSD | $0$ Å | $1.2674$ Å |

The quaternion $(\cos 45°, 0, 0, \sin 45°)$ is the turn by $90°$ about $z$, and the rotation is exact. In the mirror case, where $y_4 = (0, 0, -4)$ and the other points stay, the mirror itself would fit with RMSD 0, but no quaternion gives a mirror. The result is the same as the [Kabsch algorithm](/kabsch-algorithm/) gives.

For the mirror case QCP has $c_2 = -458.125$, $c_1 = 1152$ and $c_0 = 17989.6289$. Newton's method from $\lambda_0 = 21.75$ gives the iterates $21.75$, $19.5109$, $18.6650$, $18.5398$, $18.53720$, $18.537194$, which decrease to $\lambda_{\max}$ as the theory says. In the rotation case $\lambda_0 = 21.75$ is already the root.

## Correctness

The proof has four parts. First, each unit quaternion gives a rotation, and each rotation comes from a unit quaternion (Euler-Rodrigues and Euler's rotation theorem). Second, for a fixed $R$ the best translation matches the centroids and leaves $E = G_A + G_B - 2\operatorname{tr}(RS)$. Third, Horn's identity $q^{\mathsf T} N q = \operatorname{tr}(R(q)S)$ holds for all $q$, which a check of the coefficient of each of the nine entries of $S$ proves. Fourth, the maximum of a quadratic form of a symmetric matrix over unit vectors is its top eigenvalue. For QCP, the roots of $P$, $P'$ and $P''$ are all real and at most $\lambda_{\max}$, so $P$ is increasing and convex to the right of $\lambda_{\max}$ and Newton's method cannot pass it. The full proof is below.

## Complexity

Lines L1 and L2 cost $\Theta(N)$. Lines L3 to L7 work on a $4 \times 4$ matrix. In the [real RAM](/real-ram/), the eigenvalues of a $4 \times 4$ matrix have a closed form by the quartic formula, so these lines take $O(1)$ time; in floating point, Jacobi or QCP converge in a few steps. The total is $\Theta(N)$ in the worst case, the same as Kabsch. The extra space is $\Theta(1)$ when $S$ is accumulated from the raw sums.

## Properties

- **Exact and global.** The answer is the global minimum. There is no local search.
- **Always proper.** Each unit quaternion is a rotation, so the reflection case of Kabsch does not arise. In the mirror case the top eigenvalue is simply smaller.
- **Two quaternions for one rotation.** $q$ and $-q$ give the same $R$. The implementation keeps $w \ge 0$.
- **The value without the rotation.** The least RMSD depends only on $\lambda_{\max}$, so QCP can skip the eigenvector.
- **Unique when $\lambda_{\max}$ is simple.** If the top eigenvalue has multiplicity 1, the optimal rotation is unique. If the points lie on a line, the top eigenvalue is double, and each turn about the line is optimal.

## Variants and improvements

- **Kearsley's form.** Kearsley (1989) minimizes the residual directly as a quadratic form in $q$, with the smallest eigenvalue of a related $4 \times 4$ matrix.
- **QCP.** Theobald (2005) computes $\lambda_{\max}$ by Newton's method on the characteristic polynomial. Later work in the same line recovers the rotation from the adjugate of $N - \lambda_{\max} I$.
- **Weights.** Use weighted centroids and $S = \sum w_i a_i b_i^{\mathsf T}$.
- **SVD.** The [Kabsch algorithm](/kabsch-algorithm/) finds the same rotation from the singular value decomposition of $S$ and needs a sign fix for reflections.

## When to use it

Use the quaternion method when you want a rotation that is proper by construction, or a quaternion as output, for example to interpolate between orientations. Use QCP when you need only the RMSD for very many pairs, as in the clustering of simulation frames, because it skips both the SVD and the eigenvector. When a library SVD is at hand and you need the matrix, the Kabsch form is just as good.

## Pitfalls

- **The largest eigenvalue in absolute value.** Line L4 needs the largest eigenvalue, not the one of largest absolute value. Plain [power iteration](/power-iteration/) converges to the one of largest absolute value. In the mirror example the eigenvalues are $18.5372, 8.4766, -5.2638, -21.75$, so power iteration returns $-21.75$, which is the worst rotation. Shift $N$ by a constant at least $G_A + G_B$ first, or use a full symmetric solver.
- **The wrong layout of $N$.** If line L3 builds $N$ from $S^{\mathsf T}$, the result is $R^{\mathsf T}$, the rotation from $y$ to $x$. Check the identity $q^{\mathsf T} N q = \operatorname{tr}(R(q) S)$ for random $q$, as the tests do.
- **No normalization.** If line L5 uses an eigenvector whose length is not 1, $R(q)$ is a rotation times $|q|^2$, not a rotation.
- **Newton from the wrong side.** In QCP, a start below $\lambda_{\max}$ can converge to another root of $P$. The start $(G_A + G_B)/2$ is always safe.
- **A negative $E$.** For a perfect fit, line L7 can see a tiny negative number from rounding. Clamp it at 0.

## Implementations

## History

Horn published the closed-form solution with unit quaternions in 1987 for the absolute orientation problem of photogrammetry. Kearsley gave a quaternion form for the comparison of molecular structures in 1989. Coutsias, Seok and Dill compared the quaternion and SVD methods in detail in 2004. Theobald's QCP method of 2005 replaced the eigenproblem with a few Newton steps on the characteristic polynomial, and it is the core of many fast RMSD codes.

## References
