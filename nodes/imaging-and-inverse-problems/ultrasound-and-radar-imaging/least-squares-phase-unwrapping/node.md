---
tag: FX5THR
kind: algorithm
slug: least-squares-phase-unwrapping
name: Least-squares phase unwrapping
aliases:
- Ghiglia-Romero phase unwrapping
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: "Find the phase whose gradient best fits the wrapped phase differences in least squares, by solving a Poisson equation with fast cosine transforms."
solves: [phase-unwrapping]
model: real-ram
complexity:
  vars: {m: the number of rows of the image, n: the number of columns of the image}
  time: {worst: O(m n log(m n))}
  space: {extra: O(m n)}
properties: {deterministic: true, recursive: false, exact: false, linear_in_data: false}
history:
  year: 1994
  people: [Dennis C. Ghiglia, Louis A. Romero]
  note: "Hunt (1979) wrote the reconstruction of phase from phase differences as a least squares matrix problem. Ghiglia and Romero (1994) solved the unweighted problem for wrapped data with fast cosine transforms and the weighted problem by preconditioned conjugate gradients."
prereqs: [phase-unwrapping, poisson-equation, fast-dct]
see_also: [goldstein-branch-cut, sar-interferometry, quantitative-susceptibility-mapping, conjugate-gradient-method, preconditioning, multigrid-method, min-cost-flow-problem, weighted-least-squares]
sources:
  - paper: doi:10.1364/JOSAA.11.000107
    title: "Dennis C. Ghiglia and Louis A. Romero, Robust two-dimensional weighted and unweighted phase unwrapping that uses fast transforms and iterative methods, Journal of the Optical Society of America A 11(1), 1994, 107"
    locator: "the unweighted least squares problem as a Poisson equation with Neumann boundary conditions solved by the DCT, and the weighted problem by preconditioned conjugate gradients (general locator)"
  - paper: doi:10.1364/JOSA.69.000393
    title: "B. R. Hunt, Matrix formulation of the reconstruction of phase values from phase differences, Journal of the Optical Society of America 69(3), 1979, 393"
    locator: "the least squares estimate of a phase from its differences in matrix form (general locator)"
  - paper: doi:10.1364/AO.21.002470
    title: "Kazuyoshi Itoh, Analysis of the phase unwrapping algorithm, Applied Optics 21(14), 1982, 2470"
    locator: "the condition that the true phase differences lie in (-pi, pi) (general locator)"
  - paper: doi:10.1109/36.673674
    title: "Mario Costantini, A novel phase unwrapping method based on network programming, IEEE Transactions on Geoscience and Remote Sensing 36(3), 1998, 813 to 821"
    locator: "the minimum L1 unwrapping as a minimum cost flow problem (general locator)"
  - paper: doi:10.1364/JOSAA.17.000401
    title: "Curtis W. Chen and Howard A. Zebker, Network approaches to two-dimensional phase unwrapping: intractability and two new algorithms, Journal of the Optical Society of America A 17(3), 2000, 401"
    locator: "the NP-hardness of minimum L0 phase unwrapping (general locator)"
  - book: isbn:9780471249351
    title: "Dennis C. Ghiglia and Mark D. Pritt, Two-Dimensional Phase Unwrapping: Theory, Algorithms, and Software, Wiley, 1998"
    locator: "the chapter on minimum-norm methods (unweighted and weighted least squares, transform and iterative solvers)"
---

Least squares phase unwrapping turns a wrapped phase image into a continuous one by asking for the image whose gradient is as close as possible, in the sum of squares, to the wrapped differences of neighbouring pixels. Ghiglia and Romero (1994) showed that the normal equations of this problem are the discrete [Poisson equation](/poisson-equation/) with Neumann boundary conditions, and that the two-dimensional [discrete cosine transform](/discrete-cosine-transform/) diagonalizes it. So the whole method is one DCT, one division per coefficient and one inverse DCT, $O(m n \log(m n))$ with a [fast DCT](/fast-dct/). It never fails and never needs a choice of path, unlike path-following methods such as the [Goldstein branch cut algorithm](/goldstein-branch-cut/). The price is accuracy: where the data have residues, the method spreads the error over a wide area, it underestimates steep slopes, and the result is in general not congruent to the data, that is it does not differ from the wrapped phase by multiples of $2\pi$. It solves one formulation of the [phase unwrapping problem](/phase-unwrapping/).

## In plain words

A wrapped phase image only knows each value up to a whole number of turns. The differences between neighbouring pixels are reliable as long as the true phase changes by less than half a turn per pixel, so the method takes those differences, wrapped back into half a turn, as a field of slopes.

Then it looks for the smooth image whose slopes match that field best, measured by the sum of the squared errors. Finding it is the same as solving a Poisson equation, the equation of a stretched membrane, and a cosine transform solves that equation in one step. Where the slope field is not consistent, the error is spread out evenly and is not hidden behind cuts.

## The problem

**Input.** A wrapped phase image $\psi(i, j) \in (-\pi, \pi]$ on an $m \times n$ grid. The wrapping operator is $W(x) = x - 2\pi k$ with the integer $k$ that puts the value in $(-\pi, \pi]$.

**Data.** The wrapped differences along rows and columns,

$$g^x_{i,j} = W(\psi_{i,j+1} - \psi_{i,j}), \qquad g^y_{i,j} = W(\psi_{i+1,j} - \psi_{i,j}).$$

**Output.** The image $\varphi$ that minimizes

$$J(\varphi) = \sum_{i,j} (\varphi_{i,j+1} - \varphi_{i,j} - g^x_{i,j})^2 + \sum_{i,j} (\varphi_{i+1,j} - \varphi_{i,j} - g^y_{i,j})^2,$$

a [least squares problem](/least-squares-problem/) with $mn$ unknowns, defined up to an additive constant. The code returns the solution with zero mean.

**Residues.** The sum of $g$ around a $2 \times 2$ square of pixels is $2\pi q$ with the charge $q \in \{-1, 0, 1\}$. A nonzero charge is a residue, and it means that the slope field is not the gradient of any image. Without residues the problem has an exact solution; with them it does not.

## The algorithm

```pseudo id=main
LS-UNWRAP(ψ)                                  ▷ m × n wrapped phase
L1  g^x, g^y ← wrapped differences of ψ along rows and columns
L2  ρ(i,j) ← g^x(i,j) - g^x(i,j-1) + g^y(i,j) - g^y(i-1,j)   ▷ missing terms are 0
L3  ρ̂ ← DCT-II(ρ)                             ▷ two-dimensional
L4  φ̂(k,l) ← ρ̂(k,l) / (2 cos(π k/m) + 2 cos(π l/n) - 4)   for (k,l) ≠ (0,0)
L5  φ̂(0,0) ← 0                                ▷ the free constant
L6  φ ← inverse DCT-II(φ̂)
L7  return φ
```

Line L2 is the divergence of the slope field; a term that would use a difference outside the grid is dropped, which is the Neumann boundary condition. The normal equations of $J$ are $\Delta \varphi = \rho$ with the five point Laplacian $\Delta$ in which a border pixel has only its neighbours inside the grid. The cosine functions $\cos(\pi k (2i + 1)/(2m)) \cos(\pi l (2j + 1)/(2n))$ are the eigenvectors of that Laplacian, with the eigenvalues in the denominator of line L4, so lines L3 to L6 solve the equation exactly. The eigenvalue is zero only for $k = l = 0$, the constant image, and line L5 fixes that free constant.

## Example

Take the $2 \times 2$ image $\psi = \begin{pmatrix} 0 & 2 \\ -2 & 2.5 \end{pmatrix}$. Line L1 gives the row differences $g^x_{0,0} = 2$ and $g^x_{1,0} = W(4.5) = 4.5 - 2\pi = -1.7832$, and the column differences $g^y_{0,0} = -2$ and $g^y_{0,1} = 0.5$. Around the square, $2 + 0.5 - (-1.7832) - (-2) = 2\pi$: one residue of charge $+1$, so no image fits all four differences.

Line L2 gives $\rho = \begin{pmatrix} 0 & -1.5 \\ 0.2168 & 1.2832 \end{pmatrix}$, which sums to 0. The DCT of line L3 gives $\hat\rho(0,1) = 0.3066$, $\hat\rho(1,0) = -2.1213$ and $\hat\rho(1,1) = 1.2832$, with $\hat\rho(0,0) = 0$. The denominators of line L4 are $-2$, $-2$ and $-4$. The inverse DCT gives, after subtracting the value at $(0,0)$,

$$\varphi = \begin{pmatrix} 0 & 0.4292 \\ -0.4292 & -0.6416 \end{pmatrix}.$$

Each of the four differences of $\varphi$ is the wrapped difference minus $\pi/2$ in the direction around the loop: $0.4292 = 2 - \pi/2$, and so on. The error of $2\pi$ is shared equally by the four edges, and $J = 4 (\pi/2)^2 = \pi^2$. The result is not congruent to $\psi$: $\varphi_{0,1} - \psi_{0,1} = -\pi/2$ is not a multiple of $2\pi$.

## Correctness

The method is exact as an algorithm for the least squares problem, and that problem is exact for data without residues. The proofs are in proofs/correctness.md.

1. **Normal equations.** $J$ is a convex quadratic, and its gradient is zero exactly when $\Delta \varphi = \rho$ with the Neumann Laplacian. The grid graph is connected, so the kernel of $\Delta$ is the constants, $\sum \rho = 0$ holds automatically, and the solution is unique up to a constant.
2. **The DCT solves the equation.** The cosine $\cos(\pi k (2t+1)/(2n))$ satisfies $c(t-1) + c(t+1) - 2c(t) = (2\cos(\pi k / n) - 2) c(t)$, and its values just outside the grid equal the values on the border, so the dropped terms change nothing. The two-dimensional Laplacian is the sum of the row and column ones, so lines L3 to L6 return the zero mean solution.
3. **Exact without residues.** If no $2 \times 2$ loop of $g$ has a nonzero sum, $g$ is the gradient of an image $\varphi_0$, obtained by summing $g$ along any path, and $J(\varphi_0) = 0$. So the output is $\varphi_0$ up to a constant, and it is congruent to $\psi$. If the true phase also changes by less than $\pi$ between neighbours (Itoh's condition), the output is the true phase up to a constant.
4. **With residues.** The misfit $r = g - D\varphi$ has the same loop sums as $g$, so every loop that encloses a nonzero total charge carries misfit, however far it is from the residues. The error is not confined near the residues. It spreads.

## Complexity

In the real-RAM model, lines L1, L2, L4 and L5 cost $O(mn)$. With a fast DCT, lines L3 and L6 cost $O(mn \log(mn))$, which dominates. The space is $O(mn)$. The reference code computes the DCT by direct sums in $O(mn(m + n))$ time, which is enough for the small test grids. Grid sizes that are not powers of two are handled by fast DCT algorithms built on any fast Fourier transform.

## Properties

- **Exact solver of its model** (theorem). Lines L3 to L6 solve the Neumann Poisson equation without iteration or truncation.
- **Exact without residues** (theorem), and then congruent to the data.
- **Not congruent in general** (theorem for the example, observed in general). With residues the unwrapped phase does not equal the wrapped phase plus multiples of $2\pi$. A congruence step that adds the wrapped difference $W(\psi - \varphi)$ back to $\varphi$ restores congruence.
- **Slope underestimation** (measurement). Where noise or undersampling makes some wrapped differences take the wrong branch, the squared error pulls the slope toward zero. In the test, a ramp of 2.6 rad per pixel with Gaussian noise of standard deviation 0.7 rad has 22 residues on a $10 \times 10$ grid, and the mean slope of the output is 1.08 rad per pixel.
- **Invariant to the wrap count of the input.** Adding $2\pi k(p)$ with integers $k(p)$ to the input does not change the output.
- **Never fails.** There is no path, no cut and no choice; the output is defined for every input.
- **Linear in the slope field.** The map from $g$ to $\varphi$ is linear; all the nonlinearity is in the wrapping of line L1.

## Variants and improvements

- **Weighted least squares** (Ghiglia and Romero 1994). Weights from a quality map, for example the coherence in [SAR interferometry](/sar-interferometry/), lower the influence of bad differences. The weighted Laplacian is no longer diagonal in the DCT basis; it is solved by the [conjugate gradient method](/conjugate-gradient-method/) [preconditioned](/preconditioning/) with the unweighted DCT solver of this page, or by a [multigrid method](/multigrid-method/). A zero weight cuts the edge, which brings back some of the path independence problems of branch cuts.
- **FFT form.** Mirroring the image to $2m \times 2n$ and using the FFT gives the same result; the DCT form avoids the mirror.
- **Minimum $L^p$ norm.** Replacing the square by $|x|^p$ with $p < 2$ concentrates the misfit on fewer edges. For $p = 1$ the problem is a [minimum cost flow problem](/min-cost-flow-problem/) on the dual grid (Costantini 1998), and the result is congruent. The $p = 0$ problem, which counts the edges that disagree with $g$, is NP-hard (Chen and Zebker 2000).
- **Congruence step.** Add $W(\psi - \varphi)$ to the output to get an image congruent to the data, with the least squares solution as a guide for the $2\pi$ multiples.
- **Laplacian based unwrapping** in MRI and [quantitative susceptibility mapping](/quantitative-susceptibility-mapping/) computes $\rho$ from $\operatorname{Im}(e^{-i\psi} \Delta e^{i\psi})$ instead of from wrapped differences and solves the same Poisson equation.

## When to use it

Use the unweighted method as a fast, robust first unwrapping when the data are smooth and nearly free of residues, as a preconditioner, or when a result is needed everywhere without holes. Use it with weights for noisy interferograms. When the exact multiples of $2\pi$ matter, as in topographic [SAR interferometry](/sar-interferometry/), use a congruent method: [Goldstein branch cuts](/goldstein-branch-cut/), minimum cost flow, or the least squares result followed by a congruence step.

## Pitfalls

- **Slopes that are too low.** Many wrong branches shrink the unwrapped range. In the test the slope falls from 2.6 to 1.08 rad per pixel. Check the result against the wrapped data with $W(\psi - \varphi)$.
- **Comparing unwrapped values directly.** The output has zero mean, not the absolute phase. Only differences inside the image are meaningful.
- **Wrong boundary condition.** The FFT without mirroring imposes periodic boundary conditions, which add a jump between opposite borders. Use the DCT-II or a mirrored FFT.
- **Wrong denominator.** The eigenvalues are $2\cos(\pi k/m) + 2\cos(\pi l/n) - 4$, with $k/m$ and not $2k/m$ (that would be the periodic case). A wrong factor gives a smooth but wrong result that is hard to see.
- **Division by zero.** The $(0,0)$ coefficient has a zero eigenvalue; set it to zero, never divide.
- **Weights of zero in the unweighted solver.** Masked pixels must be handled by the weighted method; setting their phase to zero adds false slopes at the mask edge.

## Implementations

The Python code computes the DCT by direct sums, so it needs no helper for the transform. The tests compare the result with the normal equations solved by Gaussian elimination from the shared imgla helper, check the Poisson equation and the zero mean, exact recovery without residues, the invariance to integer wraps, the $2 \times 2$ example with the error of $\pi/2$ on each edge, and the slope underestimation with residues.

## History

Least squares estimates of a phase from measured differences were first used for wavefront sensors in adaptive optics, and Hunt (1979) gave the matrix formulation of the problem. Itoh (1982) analyzed when unwrapping by summing wrapped differences is exact. For wrapped data, Ghiglia and Romero (1994) used the wrapped differences as the slope field, solved the unweighted problem with fast cosine transforms, and solved the weighted problem with preconditioned conjugate gradients. The book of Ghiglia and Pritt (1998) collects these minimum-norm methods together with path-following methods.

## References
