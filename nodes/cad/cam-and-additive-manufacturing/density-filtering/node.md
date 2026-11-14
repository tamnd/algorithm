---
tag: FZQT96
kind: technique
slug: density-filtering
name: Density filtering in topology optimization
aliases:
- sensitivity filtering
- checkerboard control
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Replaces each element density by a weighted average over a radius, with cone weights, and runs the model on the averaged field, so designs lose checkerboards and gain a length scale.
prereqs: [topology-optimization, simp-method]
see_also: [beso-method, homogenization-method, gaussian-filter, mathematical-morphology, convolution, sparse-matrix, automatic-differentiation, kd-tree]
sources:
  - paper: doi:10.1016/S0045-7825(00)00278-4
    title: Tyler E. Bruns and Daniel A. Tortorelli, Topology optimization of non-linear elastic structures and compliant mechanisms, Computer Methods in Applied Mechanics and Engineering 190(26-27), 2001, 3443 to 3459
    locator: the filter applied to the densities with a weighting function that decays linearly with the distance, and the use of the filtered densities in the model
  - paper: doi:10.1002/nme.116
    title: Blaise Bourdin, Filters in topology optimization, International Journal for Numerical Methods in Engineering 50(9), 2001, 2143 to 2158
    locator: the filtered problem, with the density replaced by its convolution with a kernel, and the proof that it has at least one solution
  - paper: doi:10.1080/08905459708945415
    title: Ole Sigmund, On the design of compliant mechanisms using topology optimization, Mechanics of Structures and Machines 25(4), 1997, 493 to 524
    locator: the mesh-independency filter, which averages the sensitivities instead of the densities
  - book: isbn:978-3-540-42992-0
    title: Martin P. Bendsøe and Ole Sigmund, Topology Optimization, Theory, Methods and Applications, Springer, 2003
    locator: the chapter on the minimum compliance problem (checkerboards, mesh dependence and the filters that remove them)
---

## In plain words

A design made of small squares, each solid or empty, can cheat. A pattern of squares that touch only at their corners, like a chessboard, looks stiff to the computer even though it would fall apart. And when the squares get smaller, the computer draws thinner and thinner members, so the answer depends on the grid.

The density filter stops both. The optimizer still chooses a value for every square, but the structure that is analyzed is a blurred copy: each square takes the average of its neighbors within a fixed distance, the near ones counting more. A chessboard blurs to an even gray, which is soft, so the cheat no longer pays. A member thinner than the blur distance turns gray too, so members stay thick, however fine the grid.

## When it applies

**Setting.** A design domain is divided into elements $e$ with centers $c_e$, volumes $v_e$ and design variables $x_e \in [x_{\min}, 1]$, as in [topology optimization](/topology-optimization/). The filter radius $r_{\min} > 0$ is a length, not a number of elements. The weights are the cone

$$H_{ef} = \max\big(0,\; r_{\min} - |c_e - c_f|\big), \qquad D_e = \sum_f H_{ef} v_f,$$

and the filtered densities are

$$\tilde x_e = \frac{1}{D_e} \sum_f H_{ef}\, v_f\, x_f, \qquad \tilde x = W x \text{ with } W = D^{-1} H V.$$

The finite element model, the objective and the constraints are all evaluated at $\tilde x$, and $\tilde x$ is the design that is built. The variables $x$ are only the handles the optimizer turns. This is the density filter of Bruns and Tortorelli (2001). Bourdin (2001) studied the same idea as a convolution and proved that the filtered continuum problem has a solution, which the unfiltered 0/1 problem in general does not.

It applies to any density method where the response is a differentiable function of the element densities: [SIMP](/simp-method/) for stiffness, heat conduction, compliant mechanisms, eigenvalues. It needs a mesh where the neighbors of an element within $r_{\min}$ can be found, and on a regular grid they are a fixed stencil.

## The template

```pseudo id=main
FILTERED-DESIGN(x, r_min, ⟨kernel⟩, ⟨model⟩, ⟨update⟩, ⟨stop⟩)
L1  H_ef ← ⟨kernel⟩(|c_e − c_f|) for the pairs within r_min;  D_e ← Σ_f H_ef v_f
L2  repeat
L3      x̃_e ← Σ_f H_ef v_f x_f / D_e
L4      c, ∂c/∂x̃ ← ⟨model⟩(x̃)                       ▷ e.g. a finite element solve with the SIMP stiffness of x̃
L5      ∂c/∂x_f ← v_f Σ_e H_ef (∂c/∂x̃_e) / D_e       ▷ the transpose of the filter; the same for every constraint
L6      x ← ⟨update⟩(x, ∂c/∂x)
L7  until ⟨stop⟩
L8  return x̃                                        ▷ the physical design is x̃, not x
```

The holes are:

- **Kernel** (L1). The cone $\max(0, r_{\min} - d)$ is the usual choice. A Gaussian, as in the [Gaussian filter](/gaussian-filter/) of image processing, or a constant over the disk, also work. Every proof below needs only $H_{ef} = H_{fe} \ge 0$ and $H_{ee} > 0$.
- **Model** (L4). Any response that is differentiable in $\tilde x$, with its gradient from the adjoint method.
- **Update** (L6). Optimality criteria with a bisection on the volume multiplier, the method of moving asymptotes, or a projected gradient step.
- **Stop** (L7). A bound on the change of $x$ or of the objective, and a maximum count.

**Walk-through.** On a grid of unit squares with $r_{\min} = 1.5$, an element has 9 neighbors with positive weight: itself with 1.5, the 4 edge neighbors at distance 1 with 0.5, and the 4 diagonal ones at $\sqrt 2$ with $1.5 - \sqrt 2 \approx 0.0858$. So $D = 3.843$ inside the grid, 3.172 on an edge and 2.586 in a corner. A single solid element in a void filters to 0.390 at its center and 0.130 at its edge neighbors. A solid bar two elements wide filters to the profile 0.175, 0.825, 0.825, 0.175 across it: its volume is kept, but no element is fully solid. With the neighbors stored as a [sparse matrix](/sparse-matrix/), lines L3 and L5 take $O(n r^2)$ time on a 2D grid with $r$ the radius in elements, and the tests check both against the direct weighted sum over all pairs.

**What is proved.** The statements below are for a grid of equal elements, $v_e = 1$, so $W = D^{-1} H$, and they use the inner product $\langle a, b \rangle_D = \sum_e D_e a_e b_e$. For elements of different volumes only the weights change, as noted under Variations.

1. *A convex combination.* Each row of $W$ has entries $H_{ef} / D_e \ge 0$ that sum to 1. So $\tilde x_e$ is a weighted mean of the $x_f$, and $\min_f x_f \le \tilde x_e \le \max_f x_f$. If every $x_f$ is in $[x_{\min}, 1]$, so is every $\tilde x_e$, and no clipping is needed. A constant design is not changed.
2. *Self-adjoint in the $D$ inner product.* $\langle W x, y \rangle_D = \sum_e D_e \frac{1}{D_e} \sum_f H_{ef} x_f y_e = x^{\mathsf T} H y$. Since $H$ is symmetric, this equals $\langle x, W y \rangle_D$. In the plain inner product the adjoint is $W^{\mathsf T} = H D^{-1} = D W D^{-1}$, which is not $W$ unless $D$ is constant.
3. *The chain rule.* With $c(x) = \hat c(W x)$, $\nabla c = W^{\mathsf T} \nabla \hat c = H D^{-1} \nabla \hat c$, which is line L5. By claim 2 the same statement reads: in the $D$ inner product the gradient is the filter itself applied to the $D$-gradient $D^{-1} \nabla \hat c$. Applying $W$ to the plain gradient, a common error, gives the same numbers only at elements whose whole neighborhood has the same $D$, that is, far enough from the boundary.
4. *The volume.* $\sum_e \tilde x_e = (W^{\mathsf T} \mathbf 1) \cdot x$. The column sums $W^{\mathsf T} \mathbf 1$ are 1 inside the grid, where all $D$ are equal, and not at the boundary. So the volume of $\tilde x$ is not the volume of $x$, and a volume bound on $\tilde x$ needs the derivative $W^{\mathsf T} \mathbf 1$ from line L5.
5. *Checkerboards.* For the pattern $x_e = (-1)^{i + j}$ inside the grid, every neighbor has sign $-$ at distance 1 and $+$ at $\sqrt 2$, so $\tilde x = \lambda x$ with $\lambda = (r - 4(r - 1) + 4(r - \sqrt 2)) / (r + 4(r - 1) + 4(r - \sqrt 2))$ for $1 < r \le 2$. For $r = 1.5$, $\lambda = -0.0408$: the model sees an element checkerboard at 4% of its amplitude, and a checkerboard of 0 and 1 as a uniform gray near $1/2$.

What is measured, on a $10 \times 10$ grid with $r_{\min} = 1.5$: a corner element has column sum 0.918, so a unit of material there counts as 0.918 in the volume, and a solid bottom row of 10 elements filters to a volume of 9.62. On a $20 \times 10$ grid, applying $W$ instead of $W^{\mathsf T}$ to a random gradient is off by up to 11% for $r_{\min} = 1.5$, 36% for 2.5 and 51% for 4, always at the boundary. In the tests, a projected gradient run that tries to match a checkerboard target through the filter lowers the misfit at every step and ends with a filtered field that is nearly flat inside the grid.

## Classic examples

- **[SIMP](/simp-method/).** The density filter is the standard partner of the SIMP model. The page on SIMP uses the older sensitivity filter of Sigmund, which averages $\partial c / \partial x$ weighted by the densities and is not the gradient of any function. The density filter gives the exact gradient of the filtered problem, so any gradient method, and any check by finite differences, applies. The 88 line code of Andreassen and coauthors (2011) offers both filters.
- **[BESO](/beso-method/).** The sensitivity numbers are smoothed with the same cone weights before the elements are ranked. This also gives void elements a number from their solid neighbors, which is what lets material come back.
- **[The homogenization method](/homogenization-method/).** Composite designs have fewer checkerboards than 0/1 models, but the hole sizes are often filtered to fix a length scale for the lattice that is built from them.
- **Projection.** A smooth step $\bar x = P_\beta(\tilde x)$ after the filter, with a steepness $\beta$ raised during the run, pushes the gray band of the filter back to 0 or 1 while the filter keeps the length scale. Guest, Prévost and Belytschko (2004) introduced this Heaviside projection. The chain rule gains one factor: $\nabla c = W^{\mathsf T} \operatorname{diag}(P_\beta'(\tilde x)) \nabla \hat c$.
- **Morphology.** Sigmund (2007) replaced the weighted mean by smooth versions of the minimum and the maximum, the erosion and dilation of [mathematical morphology](/mathematical-morphology/), to get black and white designs with a length scale in the solid or in the void.

## Variations

- **The PDE filter.** Lazarov and Sigmund (2011) replaced the explicit sum by the solution of a Helmholtz type equation $-r^2 \Delta \tilde x + \tilde x = x$ on the mesh. It needs one sparse solve instead of a neighbor search, which is cheaper on unstructured meshes and on parallel computers, and its kernel is close to the cone for a matching $r$.
- **Weights with volumes.** On a mesh with elements of different size, the weights include $v_f$ as in line L3, and the inner product of claim 2 becomes $\sum_e D_e v_e a_e b_e$.
- **Boundary padding.** Extending the domain by $r_{\min}$ with elements of fixed density before filtering gives every design element the same $D$. Then $W = H / D$ is symmetric on the design elements, and the two forms of claim 3 agree. Void padding treats the outside as empty, which makes the edge of the design grayer; solid padding is used next to supports and loads.
- **Convolution by FFT.** On a regular grid the sum of line L3 is a [convolution](/convolution/), which can be done by fast Fourier transform when $r_{\min}$ is large.

## Pitfalls

- **Applying the filter to the gradient.** Line L5 uses the transpose $H D^{-1}$. Using the filter $D^{-1} H$ instead is correct only inside the grid and gives errors of 11% to 51% at the boundary in the cases above, enough to stall a gradient method or fail a finite difference check.
- **Reporting $x$ instead of $\tilde x$.** The model was solved for $\tilde x$. The raw variables can still hold checkerboards that the filter hides, and they are not the design.
- **A radius in elements.** If $r_{\min}$ is fixed in elements, a finer mesh gives thinner members and the length scale is lost. Fix it in units of length.
- **Volume on the wrong field.** The volume of $x$ and of $\tilde x$ differ at the boundary (8% for a corner element above). Put the bound on $\tilde x$, with the derivative of claim 4.
- **Gray boundaries.** The filter turns every solid to void transition into a band about $2 r_{\min}$ wide. Without a projection or a threshold the design never becomes 0/1.
- **Confusing it with checkerboard control in general.** The filter is one way to remove checkerboards; higher order elements, perimeter bounds and slope bounds are others.

## Exercises

1. Show that $W = D^{-1} H$ is similar to the symmetric matrix $D^{-1/2} H D^{-1/2}$, so its eigenvalues are real, and that they lie in $[-1, 1]$ because the rows of $W$ are nonnegative and sum to 1.
2. Compute the checkerboard factor $\lambda$ of claim 5 for $r_{\min} = 2$, where the neighbors at distance 2 have weight 0. Check that it is about $+0.041$, and explain why the sign changed from $r_{\min} = 1.5$.
3. Derive the chain rule for the projected design $\bar x = P_\beta(W x)$ and check it by central differences on a small grid.
4. Sigmund's sensitivity filter maps a gradient $g$ to $\hat g_e = \sum_f H_{ef} x_f g_f / (x_e D_e)$. Show by a two element example that the map $x \mapsto \hat g(x)$, with $g = \nabla \phi(x)$ for $\phi(x) = \frac12 \|x\|^2$, has a Jacobian that is not symmetric, so $\hat g$ is not the gradient of any function.
5. On a $10 \times 10$ grid with $r_{\min} = 1.5$, compute the column sum of an element on an edge (not a corner) and of the element next to it, inward. Explain why one is below 1 and the other above 1, and check that the sum of all column sums is 100.

## References
