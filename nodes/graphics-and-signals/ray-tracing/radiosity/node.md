---
tag: E000CC
kind: algorithm
slug: radiosity
name: Radiosity
aliases:
- progressive radiosity
- hierarchical radiosity
area: graphics-and-signals/ray-tracing
level: advanced
summary: A finite element method for diffuse light. Split the surfaces into patches, compute the form factors between them, and solve the linear system B = E + ρFB for the radiosity of each patch.
solves: [global-illumination]
model: real-ram
complexity:
  vars: {n: the number of patches, q: the quadrature points per side of a patch, ε: the tolerance, ρ: the largest reflectance}
  time: {form_factors: "O(n² q²)", sweep: Θ(n²), solve: "O(n² log(1/ε) / log(1/ρ))"}
  space: {total: Θ(n²)}
properties: {deterministic: true, randomized: false, recursive: false, exact: false}
history:
  year: 1984
  people: [Cindy M. Goral, Kenneth E. Torrance, Donald P. Greenberg, Bennett Battaile]
  note: Goral, Torrance, Greenberg and Battaile brought the radiative heat exchange method of thermal engineering to computer graphics at SIGGRAPH 1984.
prereqs: [rendering-equation, lambertian-reflectance, jacobi-method, gauss-seidel-method]
see_also: [diagonally-dominant-matrix, neumann-series, spectral-radius, successive-over-relaxation, gaussian-elimination, instant-radiosity, photon-mapping, path-tracing]
sources:
  - paper: doi:10.1145/964965.808601
    title: Cindy M. Goral, Kenneth E. Torrance, Donald P. Greenberg and Bennett Battaile, Modeling the interaction of light between diffuse surfaces, Computer Graphics (SIGGRAPH '84 Proceedings) 18(3), 1984, 213 to 222
    locator: the radiosity equation for diffuse patches and the form factors between them
  - paper: doi:10.1145/54852.378487
    title: Michael F. Cohen, Shenchang Eric Chen, John R. Wallace and Donald P. Greenberg, A progressive refinement approach to fast radiosity image generation, Computer Graphics (SIGGRAPH '88 Proceedings) 22(4), 1988, 75 to 84
    locator: shooting the unshot radiosity of the brightest patch, and the ambient term for display
  - book: isbn:9780121782702
    title: Michael F. Cohen and John R. Wallace, Radiosity and Realistic Image Synthesis, Academic Press Professional, 1993
    locator: the chapters on the radiosity equation, form factors, and the solution of the linear system
  - book: isbn:9781568813073
    title: Philip Dutré, Kavita Bala and Philippe Bekaert, Advanced Global Illumination, second edition, AK Peters, 2006
    locator: Chapter 6, Stochastic Radiosity, Section 6.1, Classic Radiosity
---

Radiosity computes [global illumination](/global-illumination/) in a scene where every surface is a [Lambertian reflector](/lambertian-reflectance/). It splits the surfaces into $n$ small patches and assumes that each patch has a constant *radiosity* $B_i$, the light power that leaves it per unit area. The light that leaves patch $i$ is its own emission $E_i$ plus the fraction $\rho_i$ of the light that arrives from all the other patches. The share of the light from patch $i$ that reaches patch $j$ is a purely geometric number, the *form factor* $F_{ij}$. So the radiosities solve the linear system

$$B_i = E_i + \rho_i \sum_{j=1}^{n} F_{ij} B_j, \qquad i = 1, \dots, n.$$

The matrix $I - \rho F$ is strictly diagonally dominant when each $\rho_i < 1$, so the [Jacobi method](/jacobi-method/) and the [Gauss-Seidel method](/gauss-seidel-method/) converge. The answer does not depend on the camera, so one solution serves every view.

## In plain words

Think of a room with white walls and one lamp. The lamp lights the walls, the walls light each other, and the light keeps bouncing.

Radiosity cuts every wall, the floor and the ceiling into small tiles. It gives each tile one brightness. For each pair of tiles it computes how much one tile sees of the other. A tile that is near and faces you counts a lot. A small tile far away at a steep angle counts little.

Then it writes down one rule for each tile: its brightness is its own glow plus part of the light that comes from all the other tiles. It solves these rules together. A simple way is to start from the glow alone and apply the rules again and again. Each round adds one more bounce of light. Because each tile reflects less light than it gets, the rounds settle down.

## The problem

The scene is a set of surfaces with emitted radiosity $E(x)$ and diffuse reflectance $\rho(x) < 1$. For Lambertian surfaces the [rendering equation](/rendering-equation/) becomes an equation for the radiosity $B(x) = \pi L(x)$:

$$B(x) = E(x) + \rho(x) \int_{S} B(y)\, \frac{\cos\theta_x \cos\theta_y}{\pi\, |x - y|^2}\, V(x, y)\, dA(y),$$

where $\theta_x$ and $\theta_y$ are the angles between the normals and the line $xy$, and $V(x, y)$ is 1 if $x$ and $y$ see each other and 0 if not. Split $S$ into patches $P_1, \dots, P_n$ with areas $A_i$, and take $B$, $E$ and $\rho$ constant on each patch. Average the equation over patch $i$. Then the patch radiosities solve the system above with

$$F_{ij} = \frac{1}{A_i} \int_{P_i} \int_{P_j} \frac{\cos\theta_x \cos\theta_y}{\pi\, |x - y|^2}\, V(x, y)\, dA(y)\, dA(x).$$

The input is the patches, $E_i$ and $\rho_i$. The output is $B_1, \dots, B_n$. For a colour image, solve one system for each colour band.

## The algorithm

```pseudo id=main
RADIOSITY(patches, E, ρ, ε)
L1  for each pair of patches i, j do F_ij ← the form factor from i to j
L2  B ← E
L3  repeat
L4      δ ← 0
L5      for i ← 1 to n do
L6          b ← E_i + ρ_i Σ_j F_ij B_j
L7          δ ← max(δ, |b − B_i|);  B_i ← b
L8  until δ < ε
L9  return B
```

Line L1 is most of the work. The form factor has two classic properties that give checks for the code:

- **Reciprocity.** $A_i F_{ij} = A_j F_{ji}$, because the integrand is symmetric in $x$ and $y$.
- **Row sums.** In a closed scene $\sum_j F_{ij} = 1$, because the patches cover the whole hemisphere above each point. In an open scene the sum is at most 1.

For a point $x$ and a polygon $P_j$ in full view, the inner integral has a closed form, Lambert's formula:

$$F_{dx \to P_j} = \frac{1}{2\pi} \left| \sum_{k} \gamma_k\, n_x \cdot \frac{a_k \times a_{k+1}}{|a_k \times a_{k+1}|} \right|,$$

where $a_k$ are the vectors from $x$ to the vertices of $P_j$ and $\gamma_k$ is the angle between $a_k$ and $a_{k+1}$. The implementation integrates this over patch $i$ with [Gauss-Legendre quadrature](/gauss-legendre-quadrature/). Renderers with occlusion use the hemicube of Cohen and Greenberg (1985), which projects the scene onto the five faces of a half cube with a z-buffer, or ray casting.

Lines L2 to L8 are Gauss-Seidel iteration: each new $B_i$ is used at once in the next rows. Jacobi iteration computes all new values from the old ones. Each sweep of either one adds about one more bounce of light, as the terms of the [Neumann series](/neumann-series/) $B = \sum_{k \ge 0} (\rho F)^k E$ show.

**Progressive refinement.** Cohen, Chen, Wallace and Greenberg (1988) reversed the order. Each patch keeps an unshot radiosity $\Delta B_i$, at first $E_i$. Each step picks the patch $i$ with the most unshot power $A_i \Delta B_i$ and shoots it to all the patches:

$$B_j \mathrel{+}= \rho_j F_{ji} \Delta B_i, \qquad \Delta B_j \mathrel{+}= \rho_j F_{ji} \Delta B_i, \qquad \text{then } \Delta B_i \leftarrow 0,$$

with $F_{ji} = F_{ij} A_i / A_j$ from reciprocity. A step needs only one row of form factors, from patch $i$, so the method needs $\Theta(n)$ memory, and a useful image appears after a few steps.

## Example

**Zones of a sphere, solved exactly.** Inside a sphere, the form factor from any point to a region is the area of the region divided by the area of the sphere, because $\cos\theta_x = \cos\theta_y = |x - y|/(2R)$. Cut the inside of the unit sphere by the planes $z = 0$ and $z = 1/2$ into three zones. By Archimedes, a zone of height $\Delta z$ has the area $2\pi \Delta z$, so $F_{ij} = \Delta z_j / 2$ for each $i$:

$$\Delta z = (1, \tfrac12, \tfrac12), \qquad F_{ij} = (\tfrac12, \tfrac14, \tfrac14) \text{ for each row } i.$$

Each row sums to 1, and $A_i F_{ij} = \pi \Delta z_i \Delta z_j$ is symmetric. A concave zone sees itself, so $F_{ii} > 0$. Let the bottom zone emit, $E = (1, 0, 0)$, with $\rho = (\frac12, \frac12, \frac14)$. Each zone receives the same irradiance $H = \sum_j F_{ij} B_j$, so $B_i = E_i + \rho_i H$, and the exact solve with fractions gives

$$H = \tfrac89, \qquad B = \left(\tfrac{13}{9}, \tfrac49, \tfrac29\right) \approx (1.444444, 0.444444, 0.222222).$$

The iterates in exact arithmetic, from $B = E$:

| sweep | Jacobi $B$ | Gauss-Seidel $B$ |
|---|---|---|
| 1 | (1.250000, 0.250000, 0.125000) | (1.250000, 0.312500, 0.175781) |
| 2 | (1.359375, 0.359375, 0.179688) | (1.373535, 0.404419, 0.207954) |
| 3 | (1.407227, 0.407227, 0.203613) | (1.419930, 0.431529, 0.217459) |

After the first sweep the Jacobi error shrinks by the factor $7/16$ at each sweep. This is the [spectral radius](/spectral-radius/) of $\rho F$. All the rows of $F$ are the same row $f$, so $\rho F$ has rank 1 and its only nonzero eigenvalue is $\sum_j f_j \rho_j = \frac14 + \frac18 + \frac1{16} = \frac{7}{16}$. The bound of the correctness section is $\max_i \rho_i = \frac12$. In floating point to the tolerance $10^{-12}$, Jacobi takes 33 sweeps, Gauss-Seidel 26 and progressive refinement 69 shots.

**A cube room.** Split each inner face of the unit cube into 2 by 2 squares, 24 patches in all. The ceiling emits $E = 1$. The walls have $\rho = 0.7$, and the floor and ceiling have $\rho = 0.3$. Lambert's formula with 8 by 8 Gauss-Legendre points gives the form factors. Each row sums to 1 within $1.4 \times 10^{-15}$, and reciprocity holds within a relative $6 \times 10^{-11}$. The form factor between two unit squares at distance 1 is 0.199825, and between two that share an edge at a right angle it is 0.200044, as the closed forms give. To the tolerance $10^{-10}$, Jacobi takes 37 sweeps, Gauss-Seidel 21 and progressive refinement 448 shots, and all three agree with Gaussian elimination. The solution is 1.086131 on the ceiling, 0.366818 on the upper halves of the walls, 0.219012 on the lower halves and 0.127238 on the floor.

## Correctness

**The system has one solution.** The matrix $I - \rho F$ has the diagonal $1 - \rho_i F_{ii}$, and the off-diagonal entries of row $i$ sum in absolute value to $\rho_i \sum_{j \ne i} F_{ij} \le \rho_i (1 - F_{ii})$. The difference is at least $1 - \rho_i > 0$, so the matrix is strictly [diagonally dominant](/diagonally-dominant-matrix/) by rows and so nonsingular.

**The iterations converge.** Let $e = B^{(k)} - B$. For Jacobi, $e^{(k+1)} = \rho F e^{(k)}$, and each row of $\rho F$ is nonnegative with the sum at most $\rho_{\max} = \max_i \rho_i < 1$, so $\|e^{(k+1)}\|_\infty \le \rho_{\max} \|e^{(k)}\|_\infty$. For Gauss-Seidel the same bound follows row by row, because each updated error is a weighted mean of errors that are already bounded by $\|e^{(k)}\|_\infty$, with the weights summing to at most $\rho_{\max}$. So both converge geometrically, and at least as fast as $\rho_{\max}^k$.

**Progressive refinement converges to the same answer.** The invariant $B_j = E_j + \rho_j \sum_k F_{jk} (B_k - \Delta B_k)$ holds at the start and after each shot, by reciprocity. Each shot removes the unshot power $A_i \Delta B_i$ and adds at most $\rho_{\max} A_i \Delta B_i$, and the chosen patch has at least $1/n$ of the total. So the total unshot power falls at least by the factor $1 - (1 - \rho_{\max})/n$ at each shot, and $\Delta B \to 0$.

The proofs, and the form factors of the sphere zones, are in the proof file.

## Complexity

With $n$ patches there are $n^2$ form factors. With $q^2$ quadrature points on patch $i$ and Lambert's formula for patch $j$, they cost $O(n^2 q^2)$ without occlusion, and a visibility test multiplies this by the cost of a ray cast or a hemicube render. One Jacobi or Gauss-Seidel sweep costs $\Theta(n^2)$. The error falls at least by $\rho_{\max}$ per sweep, so $\log(1/\varepsilon)/\log(1/\rho_{\max})$ sweeps reach the tolerance $\varepsilon$ relative to $\|E\|_\infty$. The full matrix needs $\Theta(n^2)$ memory, which limited classic radiosity to a few thousand patches.

Progressive refinement costs $\Theta(n)$ per shot plus one row of form factors, and $\Theta(n)$ memory. Hierarchical radiosity (Hanrahan, Salzman and Aupperle 1991) links patches at different levels of a subdivision tree according to an error estimate. For $k$ input surfaces it needs $O(k^2 + n)$ links instead of $n^2$ form factors.

## Properties

- **View independent.** The solution holds for every camera. It was used for walkthroughs of buildings.
- **Diffuse only.** Glossy and specular surfaces do not fit the model with one value per patch. Extensions exist but are costly.
- **Discretization error.** The answer is piecewise constant. Shadows and other sharp changes need fine meshes or a mesh that follows the discontinuities.
- **Deterministic.** There is no noise. The error is the mesh error plus the form factor error plus the solver error.
- **Energy is conserved.** With exact form factors the reflected power in each bounce is at most $\rho_{\max}$ times the power before.

## Variants and improvements

- **Progressive refinement radiosity.** Shoot from the brightest patch first. Add an ambient term from the total unshot power for display, so the early images are not too dark.
- **Hierarchical radiosity.** Subdivide patches adaptively and link each pair at the coarsest level where the form factor is accurate enough. This is the same idea as the Barnes-Hut and fast multipole methods for n-body problems.
- **Wavelet and higher order bases.** Use basis functions that are not constant on each patch, for smoother answers on coarse meshes.
- **Stochastic radiosity.** Estimate the form factors or the whole iteration with random rays, as in Chapter 6 of Dutré, Bala and Bekaert. This avoids storing the matrix.
- **Over-relaxation.** [Successive over-relaxation](/successive-over-relaxation/) speeds up Gauss-Seidel for high reflectances.
- **Instant radiosity.** Despite the name, [instant radiosity](/instant-radiosity/) is a different method. It places virtual point lights at the vertices of light paths and does not solve a patch system.

## When to use it

Use radiosity for diffuse interiors where you need the light once and many views of it, as in architectural walkthroughs and baked light maps for games. Use it when a deterministic, noise-free answer matters more than glossy effects. For general materials, use [path tracing](/path-tracing/), [photon mapping](/photon-mapping/) or another Monte Carlo method.

## Pitfalls

- **Form factors that break reciprocity.** A point-to-patch estimate from the center of patch $i$ is wrong for near patches, and it breaks $A_i F_{ij} = A_j F_{ji}$. Progressive refinement uses $F_{ij} A_i / A_j$ for $F_{ji}$, so it then solves a slightly different system than Gauss-Seidel.
- **Missing self form factors.** A curved concave patch sees itself, so $F_{ii} > 0$. Planar patches have $F_{ii} = 0$.
- **Row sums above 1.** With approximate form factors a row can sum to more than 1. Then the diagonal dominance can fail when $\rho$ is near 1. Normalize the rows, or check them.
- **Light leaks.** If a wall meets the floor and the mesh does not split the floor at the wall, the floor patch gets light from both sides of the wall.
- **A reflectance of 1.** With $\rho_i = 1$ in a closed room, the system is singular and the iterations do not converge.
- **Visible patches.** Constant patches show as blocks. Interpolate the radiosity to the vertices for display, or use a finer mesh.

## Implementations

## History

The method comes from radiative heat transfer between surfaces in thermal engineering, where form factors are called view factors. Goral, Torrance, Greenberg and Battaile brought it to computer graphics in 1984, with form factors from contour integrals and an empty box as the test scene. Cohen and Greenberg introduced the hemicube in 1985, which made form factors with occlusion practical. Cohen, Chen, Wallace and Greenberg introduced progressive refinement in 1988, so a user saw a useful image after a few steps. Hanrahan, Salzman and Aupperle introduced hierarchical radiosity in 1991. The book of Cohen and Wallace of 1993 collected the field. Later, Monte Carlo methods such as path tracing replaced radiosity for most uses, but the radiosity equation remains a standard test case and the basis of light baking.

## References
