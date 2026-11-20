---
tag: J50KQM
kind: algorithm
slug: p3m-method
name: Particle-particle particle-mesh method
aliases:
- P3M
area: scientific-computing/n-body-and-particle-methods
level: advanced
summary: Splits the force into a short-range part summed directly over near neighbors and a smooth long-range part computed on a mesh by FFT.
model: real-ram
complexity:
  vars: {N: the number of particles, M: the number of mesh points per side, P: the order of the charge assignment, r: the cutoff radius of the short-range part in units of the box}
  time: {best: "Θ(N P^2 + M^2 log M)", average: "Θ(N P^2 + M^2 log M + N^2 r^2)", worst: "Θ(N^2)"}
  space: {extra: "Θ(N + M^2)"}
properties: {deterministic: true}
history:
  year: 1981
  people: [Roger W. Hockney, James W. Eastwood]
  note: Hockney and Eastwood described the P3M algorithm and its optimal influence function in their book Computer Simulation Using Particles, first published in 1981.
prereqs: [particle-mesh-method, ewald-summation, fast-fourier-transform]
see_also: [particle-mesh-ewald, smooth-particle-mesh-ewald, treepm-method, cloud-in-cell-assignment, linked-cell-list, plasma-particle-in-cell, fast-multipole-method, gravitational-softening]
sources:
  - book: isbn:9780852743928
    title: "Roger W. Hockney and James W. Eastwood, Computer Simulation Using Particles, Adam Hilger, 1988"
    locator: Chapter 8, the particle-particle particle-mesh algorithm, the chaining mesh and the optimal influence function
  - paper: doi:10.1063/1.477414
    title: "Markus Deserno and Christian Holm, How to mesh up Ewald sums. I. A theoretical and numerical comparison of various particle mesh routines, Journal of Chemical Physics 109, 1998, 7678"
    locator: the comparison of P3M with particle mesh Ewald and smooth particle mesh Ewald, the optimal influence function and the ik and finite difference derivatives
  - paper: doi:10.1063/1.477415
    title: "Markus Deserno and Christian Holm, How to mesh up Ewald sums. II. An accurate error estimate for the particle-particle-particle-mesh algorithm, Journal of Chemical Physics 109, 1998, 7694"
    locator: the error estimate of P3M from the optimal influence function and its use to choose the parameters
---

The particle-particle particle-mesh method (P3M) computes the forces of $N$ particles that interact by a long-range law, such as gravity or the Coulomb force, in a periodic box. It splits each pair force into a short-range part, which falls off fast and is summed directly over the pairs closer than a cutoff $r_c$, and a smooth long-range part, which is computed for all particles at once on a mesh with the [fast Fourier transform](/fast-fourier-transform/). The mesh part assigns the charges to the mesh, solves the Poisson equation in Fourier space with an *influence function* $G(k)$, and interpolates the field back. Hockney and Eastwood chose $G$ to minimize the force error of the mesh, which makes P3M the most accurate of the mesh versions of [Ewald summation](/ewald-summation/). With a fixed number of neighbours per particle, the work is $O(N + M^2 \log M)$ for $M^2$ mesh points, instead of $O(N^2)$.

## In plain words

Every particle pulls on every other one. Near pulls change quickly with the distance; far pulls change slowly.

So cut each pull into two pieces. The near piece is strong only at short range, and you add it up pair by pair, but only for close pairs. The far piece is smooth, so you can blur the particles onto a regular grid, find the pull of the blurred grid with a fast wave method, and read the pull at each particle back from the grid.

The grid makes small errors, mostly where particles sit between grid points. P3M picks the grid formula that makes these errors as small as possible on average. A finer grid, or a smoother blur, gives smaller errors.

## The problem

The input is $N$ charges $q_i$ at positions $x_i$ in the periodic unit square, a mesh size $M$ (a power of 2), an assignment order $P$, a splitting parameter $\alpha$ and a cutoff $r_c < \frac12$. The output is an approximation of the force on each charge,

$$F_i = \sum_j \sum_{n \in \mathbb{Z}^2}{}' \, q_i q_j \frac{x_i - x_j + n}{|x_i - x_j + n|^2},$$

the force of the 2D Coulomb potential $-q_i q_j \log r$ over all periodic images, defined by Ewald summation; the prime omits $j = i$, $n = 0$. For gravity, replace $q_i q_j$ by $-m_i m_j$, up to the constant.

## The algorithm

The pair force $1/r$ is split as

$$\frac{1}{r} = \underbrace{\frac{e^{-\alpha^2 r^2}}{r}}_{\text{short range}} + \underbrace{\frac{1 - e^{-\alpha^2 r^2}}{r}}_{\text{long range}}.$$

The long-range part is the force between Gaussian clouds of width $1/\alpha$, and its potential has the Fourier coefficients $\hat\phi(k) = \frac{2\pi}{k^2} e^{-k^2/(4\alpha^2)}$. The mesh has $M \times M$ points of spacing $h = 1/M$. The assignment function $W$ is CIC (cloud in cell, $P = 2$) or TSC (triangular shaped cloud, $P = 3$); its Fourier transform is $\hat U(k) = \prod_c \mathrm{sinc}(k_c h / 2)^P$. The optimal influence function is

$$G(k) = \frac{\sum_m \hat U^2(k_m) \, (k \cdot k_m) \, \hat\phi(k_m)}{|k|^2 \big( \sum_m \hat U^2(k_m) \big)^2}, \qquad k_m = k + \frac{2\pi m}{h},$$

where the sums over the alias vectors $m$ run over $|m_c| \le 2$.

```pseudo id=main
P3M(q, x, M, P, α, r_c)
L1  Q_g ← Σ_i q_i W(x_i - x_g) for each mesh point g                    (charge assignment)
L2  ρ̂ ← FFT(Q)
L3  Ê(k) ← -i k G(k) ρ̂(k) for each k, with k_c = 0 at the Nyquist index
L4  E ← inverse FFT(Ê), one transform for each component
L5  F_i ← q_i Σ_g W(x_i - x_g) E_g for each particle                    (interpolation)
L6  for each pair i ≠ j with minimum image distance r < r_c: F_i ← F_i + q_i q_j e^{-α²r²} (x_i - x_j) / r²
L7  return F
```

Lines L1 to L5 are a [particle-mesh](/particle-mesh-method/) solver with the smooth kernel and the optimal $G$. Line L6 finds the close pairs with a chaining mesh, the [cell list](/linked-cell-list/) of Hockney and Eastwood: cells of side at least $r_c$, so that each close pair lies in the same or in adjacent cells. The $G$ table depends only on $M$, $P$ and $\alpha$, and is computed once.

## Example

Take $N = 200$ charges, alternately $+1$ and $-1$, uniform in the unit square (seed 21), with $\alpha = 12$ and $r_c = 0.25$. The short-range sum uses 7632 ordered pairs. The reference is an Ewald sum with $\alpha = 8$, 3 by 3 images and all wave vectors with $|n_c| \le 14$; with $\alpha = 6$ it agrees to $2 \times 10^{-15}$. The relative error of the forces in the 2-norm is:

| mesh | assignment | plain $G = \hat\phi$ | deconvolved $G = \hat\phi / \hat U^2$ | optimal $G$ |
|---|---|---|---|---|
| $16 \times 16$ | CIC | $4.7 \times 10^{-2}$ | $1.8 \times 10^{-2}$ | $1.7 \times 10^{-2}$ |
| $16 \times 16$ | TSC | $6.5 \times 10^{-2}$ | $5.6 \times 10^{-3}$ | $5.5 \times 10^{-3}$ |
| $32 \times 32$ | CIC | $1.3 \times 10^{-2}$ | $3.9 \times 10^{-3}$ | $3.9 \times 10^{-3}$ |
| $32 \times 32$ | TSC | $1.9 \times 10^{-2}$ | $4.4 \times 10^{-4}$ | $4.4 \times 10^{-4}$ |
| $64 \times 64$ | CIC | $3.4 \times 10^{-3}$ | $8.8 \times 10^{-4}$ | $8.8 \times 10^{-4}$ |
| $64 \times 64$ | TSC | $5.0 \times 10^{-3}$ | $4.6 \times 10^{-5}$ | $4.6 \times 10^{-5}$ |

These are measurements. Without correction for the blur of the assignment, the mesh force is too weak at short wavelengths, and the error is 3 to 100 times larger. Here the long-range kernel is smooth on the mesh, so the plain deconvolution is already close to optimal. The optimal $G$ gains more when the kernel is rough on the mesh: with $M = 16$, $\alpha = 24$ and CIC, the errors are $9.3 \times 10^{-2}$ deconvolved and $8.2 \times 10^{-2}$ optimal.

The parameter $\alpha$ moves work between the two parts. On the $32 \times 32$ mesh with CIC and $\alpha r_c = 3$:

| $\alpha$ | $r_c$ | short-range pairs | relative error |
|---|---|---|---|
| 8 | 0.375 | 17418 | $1.7 \times 10^{-3}$ |
| 10 | 0.3 | 11118 | $2.6 \times 10^{-3}$ |
| 12 | 0.25 | 7632 | $3.9 \times 10^{-3}$ |
| 16 | 0.1875 | 4402 | $6.9 \times 10^{-3}$ |
| 20 | 0.15 | 2840 | $1.1 \times 10^{-2}$ |

The sum of all P3M forces is $2.5 \times 10^{-13}$, against a typical force of about 99.

## Correctness

The proof file is partial. It proves that the split is exact and that the long-range part has the Fourier coefficients $\hat\phi(k) S(k)$ (Lemma 1). It proves that the chaining mesh adds the short-range term of every pair closer than $r_c$ once and of no other pair, and that the omitted short-range force is $O(e^{-\alpha^2 r_c^2})$ (Lemma 2). It proves that, for any real even $G$ and the same weights for assignment and interpolation, the mesh forces add up to zero, so the total momentum is conserved and a lone particle feels no force from itself (Lemma 3). It does not prove that the mesh force converges to the long-range force, nor that Hockney and Eastwood's $G$ minimizes the mean square force error; it states the formula and leaves the accuracy to the measurements above and to the error estimate of Deserno and Holm.

## Complexity

The model is the [real RAM](/real-ram/).

- **Mesh part (theorem).** Lines L1 and L5 cost $\Theta(P^2)$ per particle in 2D ($P^3$ in 3D). Line L2 is one FFT and line L4 two, $\Theta(M^2 \log M)$ each. Line L3 is $\Theta(M^2)$, and so is the $G$ table, up to the alias sums.
- **Short-range part.** Line L6 costs $\Theta(N)$ to fill the chaining mesh plus the number of pairs examined. For a uniform distribution, each particle has about $\pi r_c^2 N$ neighbours, so the part costs $\Theta(N^2 r_c^2)$. P3M keeps $r_c^2 N$ bounded by choosing $\alpha$ and the mesh with $N$, which gives $O(N + M^2 \log M)$ with $M^2$ proportional to $N$.
- **Worst case.** If the particles cluster, many pairs fall inside $r_c$ and line L6 costs up to $\Theta(N^2)$. This is the weakness that the [TreePM method](/treepm-method/) and adaptive P3M address.
- **Space.** $\Theta(N + M^2)$.

## Properties

- **Exact split.** The two parts add up to the exact force law; all the error comes from the mesh and from the cutoff.
- **Momentum.** With ik differentiation and the same assignment and interpolation, the total mesh force is zero, and the short-range part obeys Newton's third law. Single pair forces of the mesh are not exactly antisymmetric, and they depend slightly on the positions relative to the mesh.
- **Periodic.** The FFT makes the result periodic, so P3M suits periodic systems: plasmas, molecular dynamics and cosmological boxes. For open boundaries, the mesh must be doubled in each direction and padded with zeros.
- **Tunable.** $M$, $P$, $\alpha$ and $r_c$ trade accuracy against time, and the error estimate of Deserno and Holm predicts the force error before the run.
- **Deterministic.** The result does not depend on the order of the particles, up to rounding.

## Variants and improvements

- **Particle mesh Ewald.** The [particle mesh Ewald](/particle-mesh-ewald/) method of molecular dynamics uses Lagrange interpolation, and [smooth particle mesh Ewald](/smooth-particle-mesh-ewald/) uses B-splines. Deserno and Holm found that P3M with the optimal influence function is the most accurate of these for a given mesh and order.
- **Finite difference gradients.** Instead of ik differentiation (three or two inverse FFTs), the field can be taken from the mesh potential by finite differences, with one inverse FFT; the optimal $G$ changes accordingly.
- **Interlacing.** Averaging the results of two meshes shifted by half a mesh cell cancels the main alias errors.
- **Adaptive P3M.** Refined meshes over dense regions, as in the adaptive P3M codes of cosmology, keep the number of close pairs small when particles cluster.
- **Tree for the short range.** Replacing the direct sum of line L6 by a Barnes-Hut tree gives the [TreePM method](/treepm-method/).

## When to use it

Use P3M for periodic systems with many particles and a long-range force, when the particles are spread fairly evenly: plasma simulation, molecular dynamics with charges, and cosmological simulations at early times. For strongly clustered particles, use TreePM or a fast multipole method. For non-periodic systems, use a [fast multipole method](/fast-multipole-method/), or P3M with a zero padded mesh. For small $N$, direct Ewald summation is simpler.

## Pitfalls

- **No deconvolution.** Using $G = \hat\phi$ ignores the blur of the assignment and makes the short wavelengths too weak; in the example the errors are up to 100 times larger.
- **Cutoff too short for $\alpha$.** The short-range part is cut at $r_c$ with an error of about $e^{-\alpha^2 r_c^2}$. Keep $\alpha r_c$ near 3 or more.
- **Kernel too rough for the mesh.** If $\alpha h$ is not small, the long-range kernel has power beyond the Nyquist frequency, and aliasing dominates the error whatever $G$ is.
- **Different weights for assignment and interpolation.** Then the total force is no longer zero, and a lone particle accelerates by itself.
- **Nyquist modes.** With ik differentiation, the derivative at the Nyquist index must be set to 0, or the field gets an imaginary part and the momentum is lost.

## Implementations

## History

Hockney and Eastwood developed the particle-particle particle-mesh method for plasma and gravitational simulation and described it in their book Computer Simulation Using Particles (1981; second edition 1988), together with the chaining mesh and the optimal influence function. The method was used in cosmological simulations from the 1980s, where adaptive versions refine the mesh over clusters. Deserno and Holm (1998) compared P3M with the particle mesh Ewald methods of molecular dynamics and gave an accurate error estimate for it.

## References
