---
tag: CCN5EK
kind: algorithm
slug: cg-sense
name: CG-SENSE
aliases:
- iterative SENSE
area: imaging-and-inverse-problems/mri-reconstruction
level: advanced
summary: "Solves the SENSE least squares problem for any k-space trajectory with the conjugate gradient method on the normal equations, with the coil encoding operator and its adjoint by FFT or nonuniform FFT."
solves: [mri-reconstruction-problem]
model: real-ram
complexity:
  vars: {n: "the side of the n x n image", c: "the number of coils", S: "the number of samples per coil", K: "the number of iterations, at most n^2 in exact arithmetic"}
  time: {worst: "O(K c (n^2 log n + S))"}
  space: {extra: "O(c (n^2 + S))"}
properties: {deterministic: true, online: false, in_place: false, exact: true}
history:
  year: 2001
  people: [Klaas P. Pruessmann, Markus Weiger, Peter Boernert, Peter Boesiger]
  note: Pruessmann, Weiger, Boernert and Boesiger extended SENSE to arbitrary trajectories by solving the normal equations with the conjugate gradient method and fast gridding.
prereqs: [sense, conjugate-gradient-method]
see_also: [nonuniform-fft, density-compensation, cgls, k-space-trajectory, spirit, preconditioning, krylov-subspace, compressed-sensing-mri]
sources:
  - paper: doi:10.1002/mrm.1241
    title: Klaas P. Pruessmann, Markus Weiger, Peter Boernert and Peter Boesiger, Advances in sensitivity encoding with arbitrary k-space trajectories, Magnetic Resonance in Medicine 46(4), 2001, 638 to 651
    locator: the encoding operator for any trajectory, the conjugate gradient iteration on the normal equations, and the density compensation as a preconditioner (general locator; section numbers not confirmed)
  - paper: doi:10.6028/jres.049.044
    title: Magnus R. Hestenes and Eduard Stiefel, Methods of conjugate gradients for solving linear systems, Journal of Research of the National Bureau of Standards 49(6), 1952, 409 to 436
    locator: the conjugate gradient method, its finite termination and the minimization of the error norm over the Krylov subspace (general locator)
  - paper: doi:10.1002/(SICI)1522-2594(199911)42:5<952::AID-MRM16>3.0.CO;2-S
    title: Klaas P. Pruessmann, Markus Weiger, Markus B. Scheidegger and Peter Boesiger, SENSE, sensitivity encoding for fast MRI, Magnetic Resonance in Medicine 42(5), 1999, 952 to 962
    locator: the least squares model of sensitivity encoding that CG-SENSE solves (general locator)
---

CG-SENSE reconstructs an MR image from multi-coil data on any [k-space trajectory](/k-space-trajectory/): radial, spiral, or a Cartesian pattern with irregular gaps. It solves the same [least squares problem](/least-squares-problem/) as [SENSE](/sense/), but the problem no longer splits into small pixel groups, so it uses the [conjugate gradient method](/conjugate-gradient-method/) on the [normal equations](/normal-equations/). Each iteration applies the encoding operator and its adjoint once, by an FFT on a Cartesian grid or by a [nonuniform FFT](/nonuniform-fft/) on a trajectory. Pruessmann, Weiger, Boernert and Boesiger published it in 2001. In exact arithmetic it reaches the least squares solution in at most $n^2$ steps, and the energy norm of the error does not increase (theorems).

## In plain words

SENSE solves many tiny puzzles, one per folded pixel. With spokes or spirals instead of skipped lines, the folding is spread over the whole image, and there is one huge puzzle instead. CG-SENSE does not write that puzzle down. It only needs two moves: predict the coil data from a guess of the image, and spread a set of data back onto the image. With these two moves the conjugate gradient method walks to the best fitting image in a few dozen steps, each step better than the last in a fixed sense.

## The problem

The input is the data $y = (y_1, \ldots, y_c)$, $S$ samples per coil at the k-space points of the trajectory, the [coil sensitivity maps](/coil-sensitivity-map/) $s_k$, and optionally positive sample weights $D$. The encoding operator is $E x = (M F (s_k x))_k$, where $F$ is the unitary DFT followed by the sampling $M$ on a Cartesian grid, or the [nonuniform DFT](/nonuniform-discrete-fourier-transform/) on a trajectory. The output is the minimizer of $\lVert D^{1/2}(E x - y) \rVert^2$ over $n \times n$ images, the solution of

$$E^H D E\, x = E^H D y.$$

This is the [MRI reconstruction problem](/mri-reconstruction-problem/) with coil maps and a quadratic data term.

## The algorithm

$\langle u, w \rangle = u^H w$. $E$ and $E^H$ are given as functions.

```pseudo id=main
CG-SENSE(y, E, E^H, D, iters, tol)
L1  b <- E^H (D y)
L2  x <- 0; r <- b; p <- r
L3  for t = 0, 1, ..., iters - 1 do
L4      if ||r|| <= tol ||b|| then stop
L5      q <- E^H (D (E p))           ▷ one E and one E^H
L6      alpha <- ||r||^2 / <p, q>
L7      x <- x + alpha p
L8      r_new <- r - alpha q
L9      p <- r_new + (||r_new||^2 / ||r||^2) p; r <- r_new
L10 return x
```

Line L1 is the back projection of the weighted data. Line L5 is the only expensive step: it multiplies by the maps, transforms, samples, weights, and goes back. The vector $r$ of line L8 is the residual $b - E^H D E x$ of the normal equations. Line L9 makes the new direction conjugate to the old ones. With $D$ equal to a [density compensation](/density-compensation/) for a radial or spiral trajectory, the iteration converges in fewer steps on noiseless data; Pruessmann et al. (2001) apply it as a preconditioner.

## Example

Take an $8 \times 8$ modified Shepp-Logan phantom, the four ring coil maps of the [coil sensitivity map](/coil-sensitivity-map/) page, and a radial trajectory of 8 spokes with 8 samples each, without noise. The data have $4 \cdot 64 = 256$ values for 64 unknowns. The table gives the relative error $\lVert x_t - x \rVert / \lVert x \rVert$ (measurement with the code of this page, direct nonuniform DFT).

| weights $D$ | error after 5 steps | after 10 steps | steps to $10^{-3}$ | steps to $10^{-6}$ |
|---|---|---|---|---|
| $D = I$ | 0.256 | 0.078 | 44 | 49 |
| $D = \lvert k \rvert$ (radial density) | 0.116 | 0.055 | 31 | 34 |

Both runs reach the object, as part 4 of the theorem says for noiseless data, and both stop below $n^2 = 64$ steps. The density weights change the path, not the end point. On a $32 \times 32$ image with 24 of 32 phase encoding lines kept (a full center of 7 lines and random outer lines), the error was $2.5 \times 10^{-2}$ after 5 steps, $1.5 \times 10^{-3}$ after 10, and $2.2 \times 10^{-6}$ after 20 (measurement).

## Correctness

If $E$ has full column rank, $E^H D E$ is Hermitian positive definite and the least squares solution $x^\star$ is unique. The conjugate gradient iterates satisfy the Galerkin condition: the residual $r_t$ is orthogonal to the Krylov subspace $\mathcal{K}_t = \operatorname{span}\{b, Ab, \ldots, A^{t-1}b\}$, with $A = E^H D E$. So $x_t$ minimizes the energy norm $\lVert x - x^\star \rVert_A$ over $\mathcal{K}_t$, the norm does not increase, and the residuals, which are mutually orthogonal, vanish after at most $n^2$ steps. For uniform Cartesian undersampling and $D = I$, the least squares problem splits into the SENSE problems of the folded pixels, so $x^\star$ is the SENSE output. The [proof](proofs/correctness.md) gives all steps. These are theorems in exact arithmetic; in floating point the residuals lose orthogonality and the finite termination is lost.

## Complexity

In the [real RAM](/real-ram/), one iteration costs one application of $E$ and one of $E^H$, plus $O(n^2)$ for the vector updates. On a Cartesian grid with an FFT, one application costs $O(c n^2 \log n)$. On a trajectory with a [nonuniform FFT](/nonuniform-fft/) of fixed kernel width and oversampling, it costs $O(c(n^2 \log n + S))$; the direct nonuniform DFT of the code costs $O(c S n^2)$. The nonuniform FFT is not a reconstruction by itself: it only applies $E$ and $E^H$ fast, and CG-SENSE calls it twice per iteration. With $K$ iterations the total is $O(K c (n^2 \log n + S))$. The bound $K \le n^2$ holds in exact arithmetic. In practice the iteration stops when $\lVert r \rVert \le \mathrm{tol} \lVert b \rVert$, and the number of steps depends on the condition number of $E^H D E$, which grows with the g-factor. The memory holds a few images and one data vector, $O(c(n^2 + S))$.

## Properties

- **Least squares solution.** With full column rank, the iteration reaches $x^\star$ in at most $n^2$ steps in exact arithmetic (theorem).
- **Monotone error in the energy norm.** $\lVert x_t - x^\star \rVert_A$ does not increase (theorem). The test of this page checks it at each step on a radial problem. The Euclidean error and the data residual $\lVert E x_t - y \rVert$ are not proved monotone for this iteration, and the tests do not check them.
- **Same as SENSE for uniform Cartesian sampling.** For $D = I$, the limit is the SENSE output (theorem). The test of this page checks it on a $32 \times 32$ image with $R = 2$ and noise to $10^{-8}$.
- **Matrix free.** Only $E$ and $E^H$ are needed, so any trajectory, field map or other linear term can be added to $E$.
- **Same noise as SENSE at convergence.** At the solution the noise covariance is the one of the least squares estimate; the [g-factor](/g-factor/) describes it for uniform Cartesian sampling.

## Variants and improvements

- **CGLS and LSQR.** [CGLS](/cgls/) runs the same iteration on $D^{1/2} E$ without forming the normal equations, with better behavior in floating point. Its iterates are the same in exact arithmetic.
- **Regularized CG-SENSE.** Adding $\lambda \lVert x \rVert^2$ or $\lambda \lVert L x \rVert^2$ to the objective gives a better conditioned system, the [Tikhonov](/tikhonov-regularization/) form. Early stopping regularizes as well.
- **Preconditioning.** Density compensation in $D$, or a diagonal [preconditioner](/preconditioning/) in the image, reduces the number of steps.
- **Nonlinear priors.** [Compressed sensing MRI](/compressed-sensing-mri/) adds a sparsity term and replaces CG by a proximal method, with the same $E$.
- **k-space alternatives.** [SPIRiT](/spirit/) poses a consistency problem in k-space with a calibrated kernel instead of explicit maps, and also solves it with conjugate gradients.

## When to use it

Use CG-SENSE for non-Cartesian trajectories and for Cartesian patterns that SENSE cannot unfold pixel by pixel, such as variable density or random line patterns, when good coil maps are known. On uniform Cartesian data, direct [SENSE](/sense/) gives the same result faster. With noisy data and a high g-factor, stop early or add regularization. When the maps are not available, use [ESPIRiT](/espirit/) to estimate them, or a k-space method such as [SPIRiT](/spirit/).

## Pitfalls

- **Adjoint that is not the adjoint.** Line L5 needs the exact adjoint of $E$. A gridding operator with a different kernel for the two directions breaks the theorem, and the iteration can stall or diverge. An adjoint test, $|\langle E x, y \rangle - \langle x, E^H y \rangle|$ small, finds the error.
- **Weights in the wrong place.** $D$ must appear in line L1 and inside line L5. Weighting only line L1 solves a different, non-Hermitian system.
- **Running to convergence on noisy data.** With a high g-factor, the late iterations fit the noise. The semi-convergence of the error is the reason; choose the stopping index or a regularization weight.
- **Rank deficiency.** Where all maps are zero, or where the trajectory leaves a gap that the coils cannot fill, $E$ does not have full column rank. CG then converges to the solution of least norm in the range, and the missing part stays zero.
- **Floating point.** The residual of line L8 is updated, not recomputed, and drifts from $b - Ax$ after many steps.

## Implementations

## History

Hestenes and Stiefel published the conjugate gradient method in 1952. Pruessmann, Weiger, Scheidegger and Boesiger published [SENSE](/sense/) for Cartesian scans in 1999. In 2001 Pruessmann, Weiger, Boernert and Boesiger wrote the reconstruction for any trajectory as a large linear system, solved it with conjugate gradients, applied the encoding operator with gridding and FFTs, and used density compensation as a preconditioner. The method became the base of most later iterative MR reconstructions with coil arrays, including [compressed sensing MRI](/compressed-sensing-mri/).

## References
