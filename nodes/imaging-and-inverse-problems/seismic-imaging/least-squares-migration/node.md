---
tag: H0YJBB
kind: algorithm
slug: least-squares-migration
name: Least-squares migration
aliases:
- LSM
- least-squares RTM
area: imaging-and-inverse-problems/seismic-imaging
level: research
summary: "Find the reflectivity whose Born modeled data best fits the recorded data, solved by conjugate gradients with migration as the adjoint."
solves: [seismic-migration]
model: real-ram
complexity:
  vars: {k: "the number of iterations", a: "the cost of one product with the modeling operator or its transpose", n: "the number of image points", d: "the number of data samples"}
  time: {per_iteration: "O(a + n + d)", total: "O(k (a + n + d))"}
  space: {extra: "O(n + d)"}
properties: {deterministic: true, linear: true, iterative: true, needs_exact_adjoint: true, regularized_by_early_stopping: true}
history:
  year: 1999
  people: [Tamas Nemeth, Chengjun Wu, Gerard T. Schuster]
  note: Lailly (1983) and Tarantola (1984) cast migration as the first step of a least-squares inversion, and Nemeth, Wu and Schuster (1999) showed with Kirchhoff operators that least-squares migration reduces the artifacts of incomplete data.
prereqs: [reverse-time-migration, cgls]
see_also: [cgls, conjugate-gradient-method, reverse-time-migration, kirchhoff-migration, full-waveform-inversion, tikhonov-regularization, semi-convergence, normal-equations]
sources:
  - paper: doi:10.1190/1.1444517
    title: Tamas Nemeth, Chengjun Wu and Gerard T. Schuster, Least-squares migration of incomplete reflection data, Geophysics 64(1), 1999, 208 to 221
    locator: migration as the adjoint of a Kirchhoff modeling operator and its least-squares inversion by conjugate gradients
  - paper: doi:10.1190/1.1441754
    title: Albert Tarantola, Inversion of seismic reflection data in the acoustic approximation, Geophysics 49(8), 1984, 1259 to 1266
    locator: the gradient of the least-squares misfit as a migration of the residuals
  - paper: doi:10.6028/jres.049.044
    title: Magnus R. Hestenes and Eduard Stiefel, Methods of conjugate gradients for solving linear systems, Journal of Research of the National Bureau of Standards 49(6), 1952, 409 to 436
    locator: the conjugate gradient method and its form for least-squares problems through the normal equations
---

Least-squares migration (LSM) finds the reflectivity $m$ whose modeled data $Lm$ fit the recorded data $d$ best, $\min_m \|Lm - d\|^2$, where $L$ is a linear (Born) modeling operator. Ordinary migration computes only $L^{\mathsf T}d$, the adjoint, which is not the inverse: it blurs the image with the wavelet, the illumination and the aperture (a theorem about adjoints: $L^{\mathsf T}L \ne I$ in general). LSM removes part of that blur by running [CGLS](/cgls/), the [conjugate gradient method](/conjugate-gradient-method/) on the [normal equations](/normal-equations/) $L^{\mathsf T}Lm = L^{\mathsf T}d$, with one modeling and one migration per iteration. Any migration can serve as $L^{\mathsf T}$ if it is the exact transpose of the modeling: Kirchhoff migration gives least-squares Kirchhoff migration, and [reverse-time migration](/reverse-time-migration/) gives least-squares RTM, one variant of the method. LSM is linear in $m$ for a fixed background velocity; [full-waveform inversion](/full-waveform-inversion/) instead updates the velocity itself, which is nonlinear.

## In plain words

Migration makes a picture of the ground from the echoes, but the picture is not sharp: deep parts are weak, edges are smeared, and gaps in the recording leave stripes. Least-squares migration asks a better question. Which picture of the ground would produce echoes that look like the recorded ones? It starts with an empty picture, simulates the echoes it would make, compares them with the real ones, and migrates the difference to improve the picture. It repeats this, and each round uses the conjugate gradient rule so that it never undoes the gains of earlier rounds. After some rounds the picture is sharper and more balanced. Each round costs one simulation and one migration.

## The problem

Given the data $d \in \mathbb{R}^{n_d}$ and a linear modeling operator $L : \mathbb{R}^{n} \to \mathbb{R}^{n_d}$ (Born modeling in a fixed background velocity) with its exact transpose $L^{\mathsf T}$ (migration), find
$$m^* = \arg\min_m \|Lm - d\|_2^2,$$
or, with damping, $\min_m \|Lm - d\|^2 + \varepsilon\|m\|^2$, the [Tikhonov](/tikhonov-regularization/) form. This is [seismic migration](/seismic-migration/) posed as a linear inverse problem.

## The algorithm

```pseudo id=main
LEAST-SQUARES-MIGRATION(L, Lᵀ, d, k_max)     ▷ L: Born modeling, Lᵀ: migration
L1  m ← 0;  r ← d      ▷ the data residual
L2  s ← Lᵀ r;  p ← s;  γ ← ‖s‖²      ▷ s: the migrated residual
L3  for k ← 1 to k_max do
L4      if γ = 0 then break
L5      q ← L p      ▷ one Born modeling
L6      α ← γ / ‖q‖²
L7      m ← m + α p
L8      r ← r - α q
L9      s ← Lᵀ r;  γ_new ← ‖s‖²      ▷ one migration
L10     p ← s + (γ_new / γ) p;  γ ← γ_new
L11 return m
```

Line L2 is ordinary migration: the first search direction is the migrated image $L^{\mathsf T}d$. Line L5 models data for the search direction, and line L6 chooses the step that minimizes the residual along it. Lines L7 and L8 update the image and the residual together, so line L9 never needs another modeling. Line L10 makes the next direction conjugate to the earlier ones with respect to $L^{\mathsf T}L$. For the damped problem, run the same loop with the stacked operator $\begin{bmatrix} L \\ \sqrt{\varepsilon} I\end{bmatrix}$ and the data $\begin{bmatrix} d \\ 0\end{bmatrix}$.

## Example

**Migration is not the inverse, by hand.** Let $L = \operatorname{diag}(2, 1/2)$, a toy operator that sees one reflector four times better than the other, and the true model $m = (1, 1)$, so $d = (2, 0.5)$. Migration gives $L^{\mathsf T}d = (4, 0.25)$: the two equal reflectors differ by a factor of 16 in the image. CGLS fixes this. The first iteration gives $m_1 = (1.0037, 0.0627)$ with the residual norm $0.469$. The second gives $m_2 = (1, 1)$ to rounding, with the residual norm $4 \times 10^{-16}$, because $L$ has only two distinct singular values (a theorem: CGLS ends in at most that many steps in exact arithmetic).

**A Born-Kirchhoff test.** The test operator is a zero-offset Born-Kirchhoff operator in constant velocity 2000 m/s with a 30 Hz Ricker wavelet, an image of $8 \times 10$ points (80 unknowns) and 40 samples on 10 traces (400 data). It has 28540 nonzero entries. The true model has two point scatterers and a flat layer. The best scaled migration image has a relative model error of 0.727. CGLS reaches the following (measurements on this case):

| iterations | relative model error | residual norm / data norm |
|---|---|---|
| 5 | 0.575 | 0.0766 |
| 10 | 0.515 | 0.0273 |
| 25 | 0.463 | 0.0087 |
| 50 | 0.410 | 0.0035 |
| 100 | 0.290 | 0.0015 |

The residual drops fast and the model error slowly, because the small singular values of $L$ belong to image details that the 10 traces barely see.

## Correctness

The full proof is in proofs/correctness.md.

- **Minimizers (theorem).** The minimizers of $\|Lm - d\|$ are the solutions of $L^{\mathsf T}Lm = L^{\mathsf T}d$; among them, the one in the range of $L^{\mathsf T}$ is the minimum-norm solution $L^+d$.
- **Invariants (theorem).** At line L3 the loop keeps $r = d - Lm$ and $s = L^{\mathsf T}r$.
- **CGLS is CG on the normal equations (theorem).** The iterates are those of the conjugate gradient method on $L^{\mathsf T}Lm = L^{\mathsf T}d$ from $m = 0$. So $m_k$ minimizes $\|Lm - d\|$ over the Krylov space $\operatorname{span}\{L^{\mathsf T}d, \dots, (L^{\mathsf T}L)^{k-1}L^{\mathsf T}d\}$, the residual norms never increase, line L6 never divides by zero, and in exact arithmetic the loop ends within $\operatorname{rank}(L)$ iterations at $L^+d$.
- **Damping (theorem).** The stacked operator gives the minimizer of $\|Lm - d\|^2 + \varepsilon\|m\|^2$; the test matches a direct solve to $10^{-6}$.
- **Exact transpose (theorem).** The sparse modeling and migration of the test operator are exact transposes; the dot-product test holds to $10^{-12}$.

That the image after a few iterations is a better picture of the earth than the migrated image is not a theorem; it holds when the operator and the background velocity are right (a heuristic, supported by the test above).

## Complexity

- **Real-ram.** Each iteration costs one product with $L$ (line L5), one with $L^{\mathsf T}$ (line L9) and $O(n + n_d)$ for the vectors. With $a$ the cost of one product, $k$ iterations cost $O(k(a + n + n_d))$.
- **In practice.** For RTM operators one product costs as much as one migration, so $k$ iterations cost about $2k$ migrations. This cost is the main barrier to its use.
- **Space.** The vectors $m, p, s$ of size $n$ and $r, q$ of size $n_d$, plus what the operators need.

## Properties

- **A linear problem, a nonlinear iteration.** The problem is linear, because the background velocity is fixed. The result after a fixed number of iterations is not linear in $d$, because the step sizes depend on $d$.
- **Needs an exact adjoint.** CGLS assumes that line L9 is the transpose of line L5. An approximate adjoint breaks the conjugacy and can stop convergence; check it with the dot-product test.
- **Early stopping regularizes.** The iteration count acts as a regularization parameter: the first iterations fit the large singular values, and later ones fit noise. This is [semi-convergence](/semi-convergence/).
- **Sensitive to the velocity.** If the background velocity is wrong, events from different shots do not agree, and LSM fits them with artifacts instead of focusing them.

## Variants and improvements

- **Least-squares Kirchhoff migration.** $L$ is a ray-based Born operator and $L^{\mathsf T}$ is [Kirchhoff migration](/kirchhoff-migration/), as in the test.
- **Least-squares RTM.** $L$ is wave-equation Born modeling and $L^{\mathsf T}$ is [reverse-time migration](/reverse-time-migration/), which handles complex velocity at a high cost per iteration.
- **Preconditioning.** Scale the image by an illumination estimate or use the Hessian diagonal, which speeds up convergence.
- **Single-iteration approximations.** Estimate the inverse Hessian with point spread functions or a matching filter between $m$ and $L^{\mathsf T}Lm$, and apply it to the migrated image without iteration.
- **Sparsity and other priors.** Replace the damping by an $\ell_1$ norm in a curvelet or seislet domain and use an iterative shrinkage method.
- **Other Krylov solvers.** [LSQR](/lsqr/) gives the same iterates as CGLS in exact arithmetic, with a different recursion based on bidiagonalization.

## When to use it

Use LSM when migration artifacts limit the interpretation: uneven illumination below complex overburden, gaps in the acquisition, or a need for amplitudes close to reflection coefficients. Use it only when the background velocity is already good and an exact adjoint pair is available. When the velocity itself is wrong, first improve it with tomography or [full-waveform inversion](/full-waveform-inversion/).

## Pitfalls

- **An inexact adjoint.** Using a migration that is not the exact transpose of the modeling in line L9 makes the method stall or diverge after a few iterations. Build $L$ and $L^{\mathsf T}$ as a pair and run the dot-product test.
- **Too many iterations.** With noisy data, the model error goes down and then up while the residual keeps falling. Stop early or add damping.
- **Recomputing the residual.** Computing $r = d - Lm$ from scratch in line L8 costs an extra modeling per iteration; the update $r \leftarrow r - \alpha q$ reuses $q$ from line L5.
- **Forming the normal matrix.** Computing $L^{\mathsf T}L$ as a matrix costs $O(n^2)$ memory, which is far too much for seismic images, and squares the condition number of the stored problem. CGLS uses only products with $L$ and $L^{\mathsf T}$ (lines L5 and L9).

## Implementations

## History

Lailly (1983) and Tarantola (1984) showed that migration of the data residuals is the gradient of a least-squares misfit, so migration is the first step of an inversion. Least-squares Kirchhoff migration was studied in the 1990s; Nemeth, Wu and Schuster (1999) showed that it reduces the migration artifacts that incomplete data cause. With more computing power, least-squares RTM in the 2010s brought the method to complex velocity models.

## References
