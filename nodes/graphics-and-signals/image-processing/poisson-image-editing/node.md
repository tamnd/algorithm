---
tag: 9JM0B6
kind: algorithm
slug: poisson-image-editing
name: Poisson image editing
aliases:
- seamless cloning
- gradient-domain editing
area: graphics-and-signals/image-processing
level: advanced
summary: Paste a region by solving a discrete Poisson equation whose guidance is the source gradient and whose boundary values come from the target.
model: real-ram
complexity:
  vars: {m: the number of pixels in the region, s: the number of sweeps}
  time: {worst: Θ(s m), average: Θ(s m), best: Θ(s m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, iterative: true, linear: true, unique_solution: true, seamless_boundary: true}
history:
  year: 2003
  people: [Patrick Pérez, Michel Gangnet, Andrew Blake]
  note: Pérez, Gangnet and Blake presented guided interpolation by the Poisson equation, seamless cloning, mixed gradients and selection editing at SIGGRAPH 2003.
prereqs: [poisson-equation, gauss-seidel-method, least-squares-problem, digital-image]
see_also: [conjugate-gradient-method, multigrid-method, laplacian-matrix, image-compositing, alpha-blending, image-inpainting, laplacian-pyramid, seam-carving]
sources:
  - paper: doi:10.1145/882262.882269
    title: Patrick Pérez, Michel Gangnet and Andrew Blake, Poisson image editing, ACM Transactions on Graphics 22(3), 2003 (SIGGRAPH 2003)
    locator: pages 313 to 318; Section 2 (guided interpolation, the discrete system (7) and its solvers), Section 3 (seamless cloning, importing and mixing gradients), Section 4 (selection editing)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: the chapter on computational photography (gradient-domain blending)
---

Poisson image editing pastes a region of a source image $g$ into a target image $t$ so that no seam shows. It does not copy the source values. It asks for new values $f$ inside the region $\Omega$ whose differences between neighbors match those of the source as well as possible, while the values just outside $\Omega$ stay those of the target. In the continuous form this is the [Poisson equation](/poisson-equation/) $\Delta f = \Delta g$ in $\Omega$ with Dirichlet boundary values $f = t$ on the boundary of $\Omega$, which is where the name comes from. In discrete form it is a sparse, symmetric, positive definite linear system with one unknown per pixel of $\Omega$, the normal equations of a [least squares problem](/least-squares-problem/) on the pixel differences. Pérez, Gangnet and Blake (2003) solved it with [Gauss-Seidel](/gauss-seidel-method/) sweeps with over-relaxation or with [multigrid](/multigrid-method/); this page uses Gauss-Seidel and SOR, at $\Theta(m)$ per sweep for a region of $m$ pixels. The same machinery gives mixed-gradient cloning, texture flattening, local color and light changes and seamless tiling.

## In plain words

Copying a patch of one photo onto another leaves a visible edge, because the colors and the light do not match. Poisson editing copies the changes between neighboring pixels instead of the pixels themselves: how much brighter each pixel is than the one to its left, or the one above. Inside the patch, those changes come from the source photo. At the edge of the patch, the values must agree with the photo underneath. Usually no set of values can satisfy both exactly, so the method finds the values that come closest. The result keeps the details of the pasted object but takes its overall color and brightness from the new background, so the edge disappears. Finding those values means solving many small equations at once, one per pixel, which a few hundred quick passes over the patch do well.

## The problem

The inputs are a target $t$ and a source $g$, two gray images of $W \times H$ pixels with real values, already aligned so that pixel $p$ of $g$ goes to pixel $p$ of $t$, and a region $\Omega$, a set of $m$ pixels. Pixel centers are at integer coordinates. A color image is handled one channel at a time; the paper works in RGB, and linear or gamma encoded values both work, but the result differs. $N_p$ is the set of 4-neighbors of $p$ inside the image, so $|N_p| = 4$ except at the image border. Every 4-connected part of $\Omega$ must have at least one 4-neighbor outside $\Omega$, so that it touches the target somewhere.

For each ordered pair of neighbors, the guidance is $v_{pq} = g_p - g_q$, the source difference. The output $f$ equals $t$ outside $\Omega$ and, inside, solves the discrete system (7) of the paper: for each $p \in \Omega$,

$$|N_p|\, f_p - \sum_{q \in N_p \cap \Omega} f_q = \sum_{q \in N_p \setminus \Omega} t_q + \sum_{q \in N_p} v_{pq}.$$

The left side is the discrete Laplacian of $f$ with the sign changed, the first sum on the right brings in the boundary values, and the last sum is minus the discrete Laplacian of $g$. Pixels of $\Omega$ on the image border have $|N_p| < 4$, which acts as a zero-flux (Neumann) condition there.

## The algorithm

```pseudo id=main
POISSON-EDIT(t, g, Ω, ω, ε)                    ▷ 0 < ω < 2; ω = 1 is Gauss-Seidel
L1  f ← t                                       ▷ outside Ω, f never changes
L2  for each p ∈ Ω: n_p ← |N_p|;  b_p ← Σ_{q ∈ N_p} v_pq + Σ_{q ∈ N_p ∖ Ω} t_q
L3  repeat
L4      δ ← 0
L5      for each p ∈ Ω in raster order do
L6          x ← (b_p + Σ_{q ∈ N_p ∩ Ω} f_q) / n_p    ▷ solve equation p for f_p
L7          x ← f_p + ω (x − f_p);  δ ← max(δ, |x − f_p|)
L8          f_p ← x
L9  until δ < ε
L10 return f
```

Line L2 builds the right side once. Line L6 solves the equation of pixel $p$ for $f_p$ with the current values of its neighbors, so the new values of the pixels before $p$ in raster order are already used; this is Gauss-Seidel. Line L7 over-relaxes the step by $\omega$: $\omega = 1$ is plain Gauss-Seidel, and $1 < \omega < 2$ is successive over-relaxation (SOR), which is much faster on large regions with a good $\omega$. Line L9 stops when a sweep changes no pixel by more than $\varepsilon$.

For mixed gradients, line L2 uses $v_{pq} = t_p - t_q$ when $|t_p - t_q| > |g_p - g_q|$ and $g_p - g_q$ otherwise, which keeps the stronger of the two structures at each place. The rest is unchanged.

## Example

Take a $4 \times 4$ target and source (row $y = 0$ on top), and let $\Omega$ be the four center pixels:

| | target $t$ | source $g$ |
|---|---|---|
| row 0 | $10, 10, 10, 10$ | $0, 0, 0, 0$ |
| row 1 | $10, \ast, \ast, 30$ | $0, 9, 3, 0$ |
| row 2 | $10, \ast, \ast, 30$ | $0, 3, 9, 0$ |
| row 3 | $30, 30, 30, 30$ | $0, 0, 0, 0$ |

The values marked $\ast$ are 50 and are replaced. At $(1, 1)$, the guidance sum is $4 \cdot 9 - (0 + 0 + 3 + 3) = 30$, and two neighbors are outside with value 10, so line L2 gives $b = 50$. The four equations are

$$4f_{11} - f_{21} - f_{12} = 50, \quad 4f_{21} - f_{11} - f_{22} = 34, \quad 4f_{12} - f_{11} - f_{22} = 34, \quad 4f_{22} - f_{21} - f_{12} = 90,$$

where $f_{xy}$ is the pixel at column $x$ and row $y$. The exact solution is $f_{11} = 24$, $f_{21} = f_{12} = 23$, $f_{22} = 34$: for example $4 \cdot 24 - 23 - 23 = 50$. A plain copy would put $9, 3, 3, 9$ next to borders of 10 and 30. The Poisson result lifts the patch to the level of its surroundings, darker toward the top left where the target is 10 and brighter toward the bottom right where it is 30, and keeps the source pattern of two bright corners and a darker diagonal.

Gauss-Seidel from $f = t$: the first sweep gives $f_{11} = (50 + 50 + 50)/4 = 37.5$, then $f_{21} = (34 + 37.5 + 50)/4 = 30.375$, $f_{12} = 30.375$, and $f_{22} = (90 + 30.375 + 30.375)/4 = 37.6875$. Plain Gauss-Seidel is within $10^{-6}$ of the exact solution after 13 sweeps, SOR with $\omega = 1.2$ after 11, and SOR with $\omega = 1.5$ after 25: on a system this small the best $\omega$ is close to 1.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows three facts.

- **The system is the least squares fit of differences.** Its solution minimizes $\sum (f_p - f_q - v_{pq})^2$ over the pairs of neighbors with at least one pixel in $\Omega$, with $f = t$ outside $\Omega$. The guidance must satisfy $v_{qp} = -v_{pq}$, which holds for source differences and for mixed gradients.
- **The matrix is symmetric positive definite**, because $x^\top A x$ is the sum of $(x_p - x_q)^2$ over the neighbor pairs inside $\Omega$ plus $x_p^2$ over the pairs that cross the boundary. It is singular exactly when a part of $\Omega$ has no neighbor outside, which the implementation rejects.
- **Gauss-Seidel and SOR converge** for $0 < \omega < 2$: each step of line L7 lowers the quadratic $\frac12 x^\top A x - b^\top x$ by $\frac12 \omega(2 - \omega) n_p$ times the square of the Gauss-Seidel step, so the steps go to zero and the iterate goes to the unique solution.

The stopping test of line L9 bounds the last step, not the error; the proof file gives the error in terms of the residual.

## Complexity

- Line L2 visits each pixel of $\Omega$ and its at most four neighbors: $\Theta(m)$.
- One sweep of lines L5 to L8 does $O(1)$ work per pixel: $\Theta(m)$.

With $s$ sweeps the time is $\Theta(sm)$ and the extra space is $\Theta(m)$. The number of sweeps depends on the shape and size of $\Omega$. For a square region of side $k$, the standard model problem analysis gives a Gauss-Seidel rate of about $1 - \pi^2/k^2$ per sweep, so $\Theta(k^2 \log(1/\varepsilon))$ sweeps, and SOR with the best $\omega$ a rate of about $1 - 2\pi/k$, so $\Theta(k \log(1/\varepsilon))$ sweeps. [Conjugate gradients](/conjugate-gradient-method/) also need $O(k \log(1/\varepsilon))$ iterations, and [multigrid](/multigrid-method/) solves the system to a fixed accuracy in $O(m)$ total work. A start better than $f = t$, such as the plain copy of $g$ shifted to the mean of the boundary, saves sweeps.

## Properties

- **Exact boundary.** Outside $\Omega$ the output is the target, and inside, the values join the target with no step, up to the guidance across the boundary.
- **Invariant to a constant offset.** If $g = t + c$ for a constant $c$, the guidance equals the target differences and the output is $t$. More generally, adding a constant to $g$ does not change $f$, so the global brightness of the source does not matter.
- **Linear.** For fixed $\Omega$, the output is linear in the pair $(t, g)$. Mixed gradients make it nonlinear.
- **Harmonic fill with zero guidance.** With $v = 0$, the output inside $\Omega$ is the discrete harmonic interpolation of the boundary values: each pixel is the mean of its neighbors. This is the simplest form of [image inpainting](/image-inpainting/).
- **Color bleeding.** The boundary values spread into the whole region, so a source object placed on a red background turns reddish. This is how the method hides the seam, and also its main artifact.
- **Unique solution.** Under the condition on the parts of $\Omega$, the solution exists and is unique.

## Variants and improvements

- **Mixed gradients.** Keep the stronger of the source and target differences, which lets holes and transparent objects show the background.
- **Texture flattening.** Keep only the source differences at edges, given by an edge detector, and set the others to zero, which gives a flat, cartoon look inside the region.
- **Local illumination and color changes.** Transform the gradient field, for example by a nonlinear compression of its magnitude, or multiply a color channel before solving.
- **Seamless tiling.** Set the boundary values of a rectangle to the average of opposite sides, so the result tiles with no seam.
- **Faster solvers.** Multigrid, conjugate gradients with a preconditioner, or a direct sparse Cholesky factorization for a region reused many times. For a rectangular region a fast sine transform solves the system in $O(m \log m)$.
- **Membrane form and approximations.** With source differences as guidance, $f - g$ is discrete harmonic in $\Omega$ with boundary values $t - g$, so the output is $g$ plus the harmonic fill of the boundary difference. Any fast smooth interpolant of that difference, such as mean value coordinates or a solve on a coarse quadtree, gives an approximation with no large linear system.
- **Gradient-domain compositing of many images.** The same least squares on differences, with guidance taken from several images, blends panoramas and photomontages; [Laplacian pyramid](/laplacian-pyramid/) blending is a cheaper, non-iterative alternative.

## When to use it

Use Poisson editing to paste an object or a texture from one photo into another when the lighting and color differ and the boundary of $\Omega$ runs through smooth areas of both images. It also gives a simple, exact formulation for gradient-domain effects. Do not use it when the background around the object is busy or very different in color from the source background: the boundary values then spread into the object and change its color. [Alpha compositing](/image-compositing/) with a good matte keeps the object colors, and [Laplacian pyramid](/laplacian-pyramid/) blending is faster when a soft transition is enough.

## Pitfalls

- **A part of the region with no boundary.** If a 4-connected part of $\Omega$ has no 4-neighbor outside $\Omega$, for example when $\Omega$ is the whole image, the matrix is singular, and the iteration drifts. Check the region first, or fix one value.
- **Diagonal neighbors in the connectivity check.** The equations use 4-neighbors, so a part of $\Omega$ that touches the outside only at a corner still has no boundary term. The check must use 4-connectivity too.
- **Stopping on the step size.** A small last step does not mean a small error, because Gauss-Seidel moves slowly on large regions. Use the residual $\lVert b - Af \rVert$, which bounds the error by the smallest eigenvalue of $A$, or a fixed relative decrease.
- **ω out of range.** $\omega \ge 2$ or $\omega \le 0$ diverges. The best $\omega$ depends on the region: close to 1 for tiny regions and close to 2 for large ones.
- **Rounding to 8 bits before the end.** The solution can go outside $[0, 255]$, for example where a bright source meets a bright target. Solve in floating point and clamp only the final output.
- **Wrong sign of the guidance.** The right side uses $g_p - g_q$, the difference from the pixel to its neighbor. The other sign gives an inverted copy of the source pattern.

## Implementations

## History

Patrick Pérez, Michel Gangnet and Andrew Blake presented Poisson image editing at SIGGRAPH 2003. They framed the editing tasks as interpolation guided by a vector field, solved the discrete Poisson equation with Gauss-Seidel with over-relaxation or with V-cycle multigrid, and showed seamless cloning, mixed gradients, monochrome transfer, texture flattening, local illumination and color changes, and seamless tiling. The idea of working on gradients and integrating back by a Poisson solve was also used at the same time for high dynamic range compression (Fattal, Lischinski and Werman, 2002) and in later work on photomontage, panorama blending and gradient-domain painting. Image editors added it as a healing or seamless clone tool.

## References
