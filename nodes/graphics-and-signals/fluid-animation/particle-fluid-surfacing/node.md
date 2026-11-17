---
tag: 96G5QA
kind: problem
slug: particle-fluid-surfacing
name: Surface reconstruction from fluid particles
aliases:
- particle fluid surfacing
area: graphics-and-signals/fluid-animation
level: advanced
summary: Build a smooth liquid surface from the particles of a FLIP or SPH simulation, by a blended implicit function or anisotropic kernels, then polygonize it.
prereqs: [implicit-surface, marching-cubes]
see_also: [smoothed-particle-hydrodynamics, fluid-implicit-particle, surface-reconstruction, level-set-method, particle-level-set, principal-component-analysis, spatial-hashing, fluid-simulation-for-animation]
sources:
  - paper: doi:10.1145/357306.357310
    title: James F. Blinn, A generalization of algebraic surface drawing, ACM Transactions on Graphics 1(3), 235-256, 1982
    locator: the whole paper (the blobby model, a sum of Gaussian functions around the atoms and its level set)
  - paper: doi:10.1145/1073204.1073298
    title: Yongning Zhu and Robert Bridson, Animating sand as a fluid, ACM Transactions on Graphics 24(3), 965-972, 2005
    locator: the section on surface reconstruction from the particles (the distance to a sphere around the weighted mean of the nearby particles)
  - paper: doi:10.1145/2421636.2421641
    title: Jihun Yu and Greg Turk, Reconstructing surfaces of particle-based fluids using anisotropic kernels, ACM Transactions on Graphics 32(1), 2013
    locator: the whole paper (the smoothing of the kernel centers and the anisotropic kernels from weighted PCA)
  - paper: "Jihun Yu and Greg Turk, Reconstructing surfaces of particle-based fluids using anisotropic kernels, Eurographics/ACM SIGGRAPH Symposium on Computer Animation, 2010"
    title: Reconstructing surfaces of particle-based fluids using anisotropic kernels (symposium version)
    locator: Section 4, Equations 4 to 16 (the isotropic field, the smoothing of the centers, the weighted covariance and the anisotropy matrix, with the constants of their examples)
---

A particle fluid simulation, such as [SPH](/smoothed-particle-hydrodynamics/) or [FLIP](/fluid-implicit-particle/), gives a cloud of points, but a renderer needs a surface.
Particle fluid surfacing is the problem of building that surface: a closed, smooth surface that wraps the particles, is flat where the liquid is flat, keeps thin sheets and drops, and does not flicker from frame to frame.
The usual approach defines a scalar field from the particles, takes a level set of it as an [implicit surface](/implicit-surface/), and turns that into triangles with [marching cubes](/marching-cubes/).
The methods differ in the field: a sum of blobs (Blinn 1982), the distance to a sphere around a weighted mean of nearby particles (Zhu and Bridson 2005), or a sum of stretched kernels from the local shape of the particle cloud (Yu and Turk).
No field is correct in a formal sense, because the particles do not fix a unique surface; the radii, thresholds and weights are tuning.

## In plain words

A fluid simulation often follows the water as many small balls.
To show the water, the computer must wrap a smooth skin around the balls.
If the skin follows each ball closely, the water looks like a pile of beads.
If it smooths too much, small drops and thin sheets of water vanish, and the water looks thick.
The methods build a "how much water is near here" value for every point in space, and the skin is where that value crosses a chosen level.
Better methods look at how the balls near a point are spread out, and stretch the skin flat along a flat surface.

## Definition

**Input.** The particle positions $x_i \in \mathbb{R}^3$, $i = 1, \dots, n$, usually with a radius $r_i$ or a smoothing length $h_i$, and sometimes masses and densities, at one time step.
A sequence of such frames for an animation.

**Output.** A closed surface, usually a triangle mesh, that bounds a region containing the particles.
In most methods it is the level set $\{x : \phi(x) = 0\}$ of a field $\phi$ that is negative inside, sampled on a grid of spacing $\Delta$ and extracted by marching cubes.

**Goals.** These are wanted, not proved, and they pull against each other:

- **Smooth.** No bumps of the size of the particle spacing on a flat surface.
- **Faithful.** Thin sheets, thin streams and single drops stay, and the surface lies close to the outer particles.
- **Volume.** The enclosed volume is close to the volume of the fluid that the simulation represents.
- **Coherent in time.** Small motions of the particles give small changes of the surface, so it does not flicker.
- **Fast.** The cost is near linear in $n$ and in the number of grid cells near the surface.

**Cost model.** Neighbor search with a [spatial hash](/spatial-hashing/) or a uniform grid, a field evaluation per grid point with a bounded number of neighbors, and linear time marching cubes over the grid.

## Variants

- **Mesh or image.** Most methods build a mesh for an offline renderer. Screen space methods instead render the particles as spheres into a depth image and smooth the depth image, which is fast but gives a surface only for one view.
- **Isotropic or anisotropic kernels.** The field uses the same round kernel for every particle, or a stretched kernel per particle from the local shape of the cloud.
- **Per frame or tracked.** The field is built from each frame alone, or it carries information across frames to keep the surface steady.
- **With a level set.** In grid fluid solvers, the surface is often a [level set](/level-set-method/) carried with the flow and corrected by particles, as in the [particle level set](/particle-level-set/) method; then the particles help the surface rather than define it.
- **General point clouds.** [Surface reconstruction](/surface-reconstruction/) from scanned points is the same kind of problem, but scans give points on the surface only, often with normals, while fluid particles fill the volume.

## Examples

The examples use particles on a cubic lattice of spacing 1 and were computed by a short script.
The blobby field is $\phi = T - \sum_i e^{-a|x - x_i|^2}$ with $T = 0.5$ and $a = \ln 2/0.25$, so one particle alone gives a sphere of radius 0.5.
The Zhu-Bridson field is $\phi = |x - \bar x| - r$ with $r = 0.5$, the weighted mean $\bar x = \sum_i w_i x_i / \sum_i w_i$ and the weights $w_i = \max(0, 1 - |x - x_i|^2/R^2)^3$; one particle alone also gives a sphere of radius 0.5.

**A flat surface.** A block of $7 \times 7 \times 3$ particles has a flat top layer at $z = 2$.
The table gives the height of the surface above the top layer, sampled on an $11 \times 11$ grid over one lattice cell in the middle (measured).

| field | parameters | lowest height | highest height | bump (highest minus lowest) |
|---|---|---|---|---|
| blobby | $T = 0.5$, single radius 0.5 | 0.504 | 0.580 | 0.075 |
| Zhu-Bridson | $R = 1.5$ | 0.4999 | 0.5000 | 0.0001 |
| Zhu-Bridson | $R = 2$ | 0.430 | 0.443 | 0.012 |
| Zhu-Bridson | $R = 3$ | 0.048 | 0.049 | 0.001 |

The blobby surface has bumps of 7.5 percent of the particle spacing over each particle; Yu and Turk describe such bumps as a defect of round kernels.
The Zhu-Bridson surface is much flatter, but with a large $R$ the weighted mean is pulled into the block, and the surface sinks toward the top layer, so the liquid loses volume.

**Two particles.** Two particles at the distance $d$ apart; the table gives the radius of the neck of the surface at the midpoint, or 0 if the two parts are not joined (measured).

| $d$ | blobby neck | Zhu-Bridson neck ($R = 2$) |
|---|---|---|
| 1.0 | 0.500 | 0.500 |
| 1.2 | 0.375 | 0.500 |
| 1.5 | 0 (separate) | 0.500 |
| 2.0 | 0 (separate) | 0.500 |

The blobs of two close particles merge into a fat neck, as wide as one particle.
The Zhu-Bridson field joins any two particles closer than $2R$ with a neck of radius $r$, because at the midpoint the weighted mean is the midpoint itself.
So it can make thin bridges of liquid between drops that should be apart.

## Known algorithms

- **Blobby spheres (Blinn 1982).** $\phi(x) = T - \sum_i b_i e^{-a_i|x - x_i|^2}$. Simple and smooth, but bumpy on flat surfaces and fat where particles are close. Blinn made it for molecules; fluid codes use it with kernels of finite support, often the SPH density or a color field.
- **Weighted mean of the neighbors (Zhu and Bridson 2005).** $\phi(x) = |x - \bar x(x)| - \bar r(x)$, with $\bar x$ and $\bar r$ the weighted means of the nearby positions and radii. Exact for one particle and much flatter on flat surfaces, but the surface sinks into the liquid when $R$ is large and bridges gaps between drops (both measured in the examples). They also smooth the sampled field afterward. Adams and others (2007) improved it by tracking the distance from each particle to the surface over time.
- **Anisotropic kernels (Yu and Turk).** First move each kernel center by one step of Laplacian smoothing, $\bar x_i = (1 - \lambda)x_i + \lambda\sum_j w_{ij}x_j/\sum_j w_{ij}$, with $\lambda$ between 0.9 and 1 in their examples. Then compute the weighted covariance $C_i$ of the neighbors of each particle, a weighted [principal component analysis](/principal-component-analysis/), and stretch the kernel of particle $i$ by $G_i = h_i^{-1}R\tilde\Sigma^{-1}R^{\mathsf T}$, where $C_i = R\Sigma R^{\mathsf T}$ and $\tilde\Sigma$ caps the ratio of the eigenvalues and falls back to a round kernel when the particle has few neighbors. The field is $\phi(x) = \sum_j (m_j/\rho_j) W(x - \bar x_j, G_j)$ with $W(r, G) = \sigma\lvert G\rvert P(\lvert Gr\rvert)$. Near a flat surface the kernels become flat disks, so the surface is flat and edges stay sharp. Their constants ($k_r = 4$, $k_s = 1400$, $k_n = 0.5$, $N_\varepsilon = 25$ in the 2010 version) are tuning.
- **Screen space smoothing.** Render the particles as spheres into a depth buffer, smooth the depth with a filter that keeps the edges, and shade the result. No mesh is built.
- **Polygonization.** Every field method above ends with [marching cubes](/marching-cubes/) or a variant such as [dual contouring](/dual-contouring/) on a grid that covers the surface.

## Bounds

There are no lower bounds or guarantees of quality: the goals above are not formal, and different fields give different surfaces from the same particles.
What can be shown is narrow:

- **One particle (proved).** The blobby field gives the sphere of radius $(\ln(b/T)/a)^{1/2}$, and the Zhu-Bridson field gives the sphere of radius $r$, because $\bar x = x_1$.
- **Cost (proved).** With a bounded number of neighbors within the kernel radius, one field value costs $O(1)$ after a spatial hash is built in $O(n)$ expected time. On a grid with $g$ cells in a band around the surface, the field costs $O(g)$ and marching cubes $O(g)$. The weighted PCA of Yu and Turk adds an $O(1)$ eigenproblem of size $3 \times 3$ per particle, so it is $O(n)$ as well.
- **Grid resolution (measured).** Features thinner than the grid spacing $\Delta$ can vanish or break into pieces, so $\Delta$ is usually a fraction of the particle spacing, and the grid cost grows as $\Delta^{-2}$ for a band around the surface.
- **Volume (measured).** No method above keeps the volume of the particles; the table of flat surfaces shows a shift of the surface of up to 0.45 particle spacings with the choice of $R$.

## Reductions

- **To isosurface extraction.** Once the field is fixed, the problem is the extraction of a level set from a scalar field, solved by [marching cubes](/marching-cubes/) or [marching squares](/marching-squares/) in 2D.
- **From SPH density.** The SPH density estimate itself is a field of the blobby kind, with the [SPH kernel](/sph-smoothing-kernel/) in place of the Gaussian, so a level set of the density is one surfacing method.
- **To point cloud reconstruction.** Taking only the particles near the surface, with normals from the gradient of the density, turns it into [surface reconstruction](/surface-reconstruction/) from oriented points, for example by [Poisson surface reconstruction](/poisson-surface-reconstruction/).

## Applications

- Rendering the liquids of SPH, PBF, FLIP and APIC simulations in film and games.
- Building the free surface for the boundary condition of a hybrid solver, where the particles carry the liquid and the grid needs to know which cells are full.
- Foam, spray and bubbles, which are often drawn as particles while the main body of the liquid is a surface.

## References
