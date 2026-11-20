---
tag: BKG2W0
kind: algorithm
slug: treepm-method
name: TreePM method
aliases:
- tree particle-mesh method
area: scientific-computing/n-body-and-particle-methods
level: advanced
summary: Splits gravity into a long-range part solved on a mesh by FFT and a short-range part summed with a Barnes-Hut tree; GADGET-2 and other cosmological codes use it.
model: real-ram
complexity:
  vars: {N: the number of particles, M: the number of mesh points per side}
  time: {best: "Θ(N log N + M^2 log M)", average: "Θ(N log N + M^2 log M)", worst: "Θ(N^2)"}
  space: {extra: "Θ(N + M^2)"}
properties: {deterministic: true}
history:
  year: 2002
  people: [Jasjeet S. Bagla]
  note: Bagla described the TreePM code, which splits the force in Fourier space and computes the short-range part with a tree, in the Journal of Astrophysics and Astronomy in 2002.
prereqs: [p3m-method, barnes-hut-algorithm]
see_also: [particle-mesh-method, fast-multipole-method, ewald-summation, multipole-acceptance-criterion, gravitational-softening, hashed-oct-tree, quadtree, adaptive-mesh-refinement]
sources:
  - paper: doi:10.1007/BF02702282
    title: "J. S. Bagla, TreePM: A code for cosmological N-body simulations, Journal of Astrophysics and Astronomy 23, 2002, 185-196"
    locator: the split of the force with a Gaussian filter, the short-range force from the tree with a cutoff, and the errors of the method
  - paper: url:https://ui.adsabs.harvard.edu/abs/1995ApJS...98..355X
    title: "Guohong Xu, A new parallel N-body gravity solver: TPM, The Astrophysical Journal Supplement Series 98, 1995, 355-366"
    locator: the TPM method, which uses a tree in the dense regions and a particle-mesh solver for the rest
  - paper: doi:10.1111/j.1365-2966.2005.09655.x
    title: "Volker Springel, The cosmological simulation code GADGET-2, Monthly Notices of the Royal Astronomical Society 364, 2005, 1105-1134"
    locator: the TreePM force computation of GADGET-2, with the long-range force on a mesh and the short-range force from the tree
---

The TreePM method computes the gravitational forces of $N$ particles in a periodic box. Like the [P3M method](/p3m-method/), it splits each pair force into a long-range part and a short-range part. The long-range part is smooth, and a [particle-mesh](/particle-mesh-method/) solver computes it for all particles at once with the [fast Fourier transform](/fast-fourier-transform/). The short-range part is zero beyond a cutoff of a few mesh cells, and TreePM computes it with a [Barnes-Hut](/barnes-hut-algorithm/) tree instead of a sum over all close pairs. The tree treats a far group of particles as one mass, so the work stays near $O(N \log N)$ when the particles cluster, which is where P3M slows down to $O(N^2)$. Bagla described the method in 2002, and GADGET-2 and other cosmological codes use it.

## In plain words

Gravity pulls every particle toward every other one. TreePM cuts each pull into a near piece and a far piece.

The far piece changes slowly over space. So you spread the particles onto a regular grid, find the far pull of the whole grid with a fast wave method, and read it back at each particle.

The near piece is strong only close to a particle. To add it up, you put the particles in a tree of nested squares. For each particle, you walk the tree. You skip the squares that are out of range. You treat a small square that is far enough away as one heavy point at its center of mass. You open the other squares and look inside. A dense cluster then costs little more than an empty region.

## The problem

The input is $N$ masses $m_i > 0$ at positions $x_i$ in the periodic unit square, a mesh size $M$ (a power of 2), a split scale $r_s$, a cutoff factor $c$ with $c \, r_s \le \frac12$, and an opening angle $\theta \ge 0$. The output is an approximation of the force on each particle,

$$F_i = -\sum_j \sum_{n \in \mathbb{Z}^2}{}' \, m_i m_j \frac{x_i - x_j + n}{|x_i - x_j + n|^2},$$

the force of the 2D gravitational potential $m_i m_j \log r$ over all periodic images, defined by [Ewald summation](/ewald-summation/); the prime omits $j = i$, $n = 0$. Cosmological codes use the 3D law and add [gravitational softening](/gravitational-softening/); the method is the same.

## The algorithm

The potential is split in Fourier space. With $\hat\phi(k) = 2\pi / k^2$,

$$\hat\phi(k) = \underbrace{\hat\phi(k) \, e^{-k^2 r_s^2}}_{\text{long range}} + \underbrace{\hat\phi(k) \big(1 - e^{-k^2 r_s^2}\big)}_{\text{short range}}.$$

This is the Gaussian split of Ewald summation with $\alpha = 1 / (2 r_s)$. In real space, the short-range pair force is the Newtonian force times $e^{-r^2 / (4 r_s^2)}$; in 3D the factor is $\mathrm{erfc}\big(\frac{r}{2 r_s}\big) + \frac{r}{r_s \sqrt\pi} e^{-r^2 / (4 r_s^2)}$. Both factors fall off like a Gaussian, so the short-range force is cut at $r_{\text{cut}} = c \, r_s$. Write $f_s(z) = -m_i m_j \frac{z}{|z|^2} e^{-|z|^2 / (4 r_s^2)}$ for the short-range force of a mass $m_j$ at displacement $z$.

```pseudo id=main
TREEPM(m, x, M, r_s, c, θ)
L1  F^long ← particle-mesh forces with the filter e^{-k² r_s²} (TSC assignment, deconvolution, FFT, ik derivative, TSC interpolation)
L2  build a quadtree of the particles; each node stores its total mass and its center of mass
L3  for each particle i: walk the tree from the root with a stack, and F_i^short ← 0
L4      skip a node if its minimum image distance from x_i is at least r_cut = c r_s
L5      if the node is a leaf: add f_s(x_i - x_j) for each j ≠ i in it with |x_i - x_j| < r_cut
L6      else if its side s < θ d, with d the distance to its center of mass: add f_s for its total mass at that center; else push its children
L7  return F^long + F^short
```

Line L1 is a particle-mesh solver whose kernel is smooth on the mesh, because $e^{-k^2 r_s^2}$ is small at the Nyquist wave number when $r_s$ is a mesh cell or more. Lines L2 to L6 are the Barnes-Hut algorithm with two changes: the pair force has the factor $e^{-r^2/(4 r_s^2)}$, and the nodes out of range are skipped. Line L6 is the simple [opening criterion](/multipole-acceptance-criterion/) $s < \theta d$. The code uses monopoles only, which is enough because all masses are positive.

## Example

Take $N = 200$ particles of mass $1/200$: 100 in a Gaussian cluster of width 0.03 around $(0.3, 0.6)$ and 100 uniform in the unit square (seed 7). The mesh is $32 \times 32$ and $c = 6$. The reference is an Ewald sum. The table gives the relative error of the forces in the 2-norm, and the number of particle and node interactions of the short-range walk:

| $r_s$ in mesh cells | $\theta = 0$ | $\theta = 0.3$ | $\theta = 0.5$ | $\theta = 0.7$ | $\theta = 1$ |
|---|---|---|---|---|---|
| 0.75 | $3.4 \times 10^{-3}$, 11376 | $3.4 \times 10^{-3}$, 10867 | $5.5 \times 10^{-3}$, 8929 | $1.1 \times 10^{-2}$, 7175 | $2.4 \times 10^{-2}$, 5516 |
| 1.25 | $7.6 \times 10^{-4}$, 14304 | $9.0 \times 10^{-4}$, 13134 | $3.3 \times 10^{-3}$, 11088 | $7.3 \times 10^{-3}$, 9320 | $1.8 \times 10^{-2}$, 7278 |
| 2 | $1.6 \times 10^{-4}$, 21518 | $5.5 \times 10^{-4}$, 18460 | $2.4 \times 10^{-3}$, 16125 | $5.8 \times 10^{-3}$, 13619 | $1.5 \times 10^{-2}$, 9443 |
| 2.5 | $7.4 \times 10^{-5}$, 29944 | $5.7 \times 10^{-4}$, 23563 | $2.3 \times 10^{-3}$, 20172 | $5.7 \times 10^{-3}$, 15708 | $1.5 \times 10^{-2}$, 10161 |

These are measurements. The column $\theta = 0$ is the exact cut-off sum, so its error is the error of the mesh and of the cutoff; it falls fast as $r_s$ grows, because the filter is smaller at the Nyquist wave number. A larger $r_s$ puts more particles in range and needs more interactions. A larger $\theta$ saves interactions and adds the error of the tree, which soon dominates. The direct sum needs 39800 ordered pairs.

For 200 uniform particles (seed 21) with $\theta = 0.5$ and $r_s = 1.25$ cells, the errors are $4.1 \times 10^{-3}$, $5.6 \times 10^{-4}$ and $5.3 \times 10^{-4}$ on meshes of 16, 32 and 64 points per side, with 21060, 6808 and 1728 interactions. A finer mesh shrinks $r_s$ and moves the work from the tree to the mesh. For two unit masses at distance 0.02, TreePM gives the force 49.904 and Ewald summation 49.937.

## Correctness

The proof file is partial. It proves that the Fourier split is exact and is the Ewald split with $\alpha = 1/(2 r_s)$ (Lemma 1). It proves that the pruning of line L4 never drops a particle in range (Lemma 2), and that with $\theta = 0$ the walk adds the short-range force of every pair closer than $r_{\text{cut}}$ exactly once (Lemma 3). The omitted part beyond the cutoff is $O(e^{-c^2/4})$ (Lemma 4). A node accepted at line L6 with $\theta < 1/\sqrt2$ has an error of $O(\theta^2)$ relative to its force, because the dipole term vanishes about the center of mass (Lemma 5). With $\theta = 0$, the total force is zero. The proof does not bound the error of the mesh part; the example measures it.

## Complexity

The model is the [real RAM](/real-ram/).

- **Mesh part (theorem).** Line L1 costs $\Theta(N)$ for the assignment and the interpolation and $\Theta(M^2 \log M)$ for the FFTs.
- **Tree build.** Line L2 costs $\Theta(N \cdot D)$ for a tree of depth $D$. The depth is about $\log_4 N$ for evenly spread particles, and the code caps it at 40.
- **Walk (typical, not a theorem).** Each walk visits the nodes on the paths toward the region within $r_{\text{cut}}$, and inside that region about $1/\theta^2$ nodes per level. For a fixed $\theta > 0$ and a fixed number of mesh cells in $r_{\text{cut}}$, this is $O(\log N)$ nodes per particle, so the time is $O(N \log N + M^2 \log M)$ even with clusters. With $\theta = 0$, a cluster of $K$ particles within $r_{\text{cut}}$ costs $\Theta(K^2)$, as in P3M.
- **Worst case.** If many particles sit at the same point, a leaf at the depth cap holds them all, and line L5 costs $\Theta(N^2)$.
- **Space.** $\Theta(N + M^2)$.

## Properties

- **Exact split.** The two parts add up to the exact force law. The errors come from the mesh, the cutoff and the tree, and the three are set by $r_s / h$, $c$ and $\theta$.
- **Insensitive to clustering.** The short-range work grows like $\log N$ per particle in a cluster, not like the number of neighbours.
- **No Newton's third law for $\theta > 0$.** The force of a node on a particle and the force of that particle's node on the node's particles are different approximations. In the example, with $r_s = 1.25$ cells, the total force is 0.09 times the root mean square force for $\theta = 0.5$, and $6 \times 10^{-15}$ times it for $\theta = 0$.
- **Periodic.** The mesh makes the long-range part periodic, and the short-range part uses the minimum image. Both suit cosmological boxes.
- **Deterministic.** The result depends on the particles, not on their order, up to rounding.

## Variants and improvements

- **TPM.** The TPM method of Xu (1995) splits space, not the force: it uses a tree for the particles in dense regions and a particle-mesh solver for the rest.
- **3D and softening.** Production codes work in 3D with the erfc factor above, and add [softening](/gravitational-softening/) to the short-range force.
- **Better trees.** Higher multipoles, the relative opening criterion and the [hashed oct-tree](/hashed-oct-tree/) improve the short-range part; a [fast multipole method](/fast-multipole-method/) can replace the tree.
- **Zoom meshes.** A second, finer mesh over a high-resolution region adds an intermediate scale to the split.
- **Individual time steps.** The long-range force changes slowly, so codes compute it less often than the short-range force of fast particles.

## When to use it

Use TreePM for large periodic gravitational simulations in which the particles cluster strongly, as in cosmology at late times. If the particles stay fairly even, [P3M](/p3m-method/) or a pure mesh method is simpler. For a non-periodic system, use a [Barnes-Hut tree](/barnes-hut-algorithm/) or a fast multipole method alone. For small $N$, direct summation with Ewald sums is simpler.

## Pitfalls

- **Cutoff past half the box.** The short-range part uses only the minimum image, so $c \, r_s$ must stay below $\frac12$, or the nearest images beyond the cutoff are missed; the code raises an error.
- **Split scale too small.** If $r_s$ is below about one mesh cell, the long-range kernel is not smooth on the mesh, and aliasing dominates the error whatever $\theta$ is.
- **Split scale too large.** A large $r_s$ puts many particles in range and makes the tree do most of the work.
- **Opening angle too large.** In the example, $\theta = 1$ gives errors near $2 \times 10^{-2}$ for every $r_s$. Choose $\theta$ for the target error, not for speed alone.
- **No deconvolution.** As in P3M, the mesh force must be divided by the transform of the assignment and interpolation windows, or the short wavelengths are too weak.

## Implementations

## History

Hockney and Eastwood's P3M method of the 1980s already split the force into a mesh part and a short-range part. Xu (1995) combined a tree with a particle-mesh solver in the TPM method, but split the box into dense and sparse regions. Bagla (2002) described TreePM, which splits the force with a Gaussian filter in Fourier space and uses the tree for the short-range part everywhere. Springel's GADGET-2 (2005) used the same TreePM scheme for large cosmological simulations, and many later codes follow it.

## References
