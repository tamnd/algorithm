---
tag: MWJDAT
kind: definition
slug: sph-smoothing-kernel
name: SPH smoothing kernel
aliases:
- Wendland kernel
- cubic spline kernel
- SPH kernel
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: A compactly supported, normalized radial function W(r, h) that interpolates fields from particles in SPH, such as the cubic spline or Wendland kernels.
prereqs: [kernel-density-estimation]
see_also: [smoothed-particle-hydrodynamics, monaghan-artificial-viscosity, incompressible-sph, weakly-compressible-sph, position-based-fluids, partition-of-unity, b-spline, radial-basis-function-interpolation]
sources:
  - paper: "J. J. Monaghan and J. C. Lattanzio, A refined particle method for astrophysical problems, Astronomy and Astrophysics 149 (1985) 135-143"
    locator: "the cubic spline (M4) kernel"
  - paper: doi:10.1146/annurev.aa.30.090192.002551
    title: "Joseph J. Monaghan, Smoothed particle hydrodynamics, Annual Review of Astronomy and Astrophysics 30 (1992) 543-574"
    locator: "kernel estimates, the cubic spline kernel and the symmetric SPH equations"
  - paper: doi:10.1088/0034-4885/68/8/R01
    title: "Joseph J. Monaghan, Smoothed particle hydrodynamics, Reports on Progress in Physics 68 (2005) 1703-1759"
  - paper: doi:10.1111/j.1365-2966.2012.21439.x
    title: "Walter Dehnen and Hossam Aly, Improving convergence in smoothed particle hydrodynamics simulations without pairing instability, Monthly Notices of the Royal Astronomical Society 425 (2012) 1068-1082"
    locator: "the pairing instability, the Fourier transform condition and the Wendland kernels in SPH"
  - paper: doi:10.1007/BF02123482
    title: "Holger Wendland, Piecewise polynomial, positive definite and compactly supported radial functions of minimal degree, Advances in Computational Mathematics 4 (1995) 389-396"
  - paper: "Matthias Müller, David Charypar and Markus Gross, Particle-based fluid simulation for interactive applications, Symposium on Computer Animation 2003, 154-159"
    locator: "the poly6 and spiky kernels used in graphics"
---

An SPH smoothing kernel is the weight function $W(r, h)$ that [smoothed particle hydrodynamics](/smoothed-particle-hydrodynamics/) uses to turn values carried by particles into a smooth field: the density at a point is the sum of the particle masses, each weighted by $W$ at its distance. It is a bell-shaped radial function with integral 1 that is zero beyond a few smoothing lengths $h$, so each particle interacts only with its neighbors. Graphics fluid solvers ([weakly compressible SPH](/weakly-compressible-sph/), [position-based fluids](/position-based-fluids/)) use the same idea, often with the poly6 and spiky kernels and the support radius called $h$. What the numerical analysis adds is the conditions a kernel must meet for the estimates to be accurate to second order in $h$, and for particles to stay evenly spaced instead of clumping in pairs.

## Definition

Let $d$ be the space dimension. An SPH smoothing kernel is a function $W(r, h) = h^{-d} w(|r|/h)$, with $w \colon [0, \infty) \to \mathbb R$ and smoothing length $h > 0$, such that:

1. **Normalization.** $\int_{\mathbb R^d} W(r, h)\,dr = 1$.
2. **Compact support.** $w(q) = 0$ for $q \ge \kappa$, with a fixed support factor $\kappa$ (here $\kappa = 2$, so $W$ vanishes beyond $2h$).
3. **Symmetry.** $W$ depends only on $|r|$, so $W(-r, h) = W(r, h)$ and $\nabla W(-r, h) = -\nabla W(r, h)$.
4. **Delta limit.** $W(\cdot, h) \to \delta$ as $h \to 0$, which follows from 1 and 2.
5. **Smoothness.** $w$ is at least continuously differentiable, with $w'(0) = 0$, so that $\nabla W$ is continuous. Most kernels in use are also nonnegative and decrease in $q$.

The kernel estimate of a field $A$ and of its gradient at particle $i$ are

$$A_i \approx \sum_j \frac{m_j}{\rho_j} A_j W(x_i - x_j, h), \qquad \nabla A_i \approx \sum_j \frac{m_j}{\rho_j} A_j \nabla_i W(x_i - x_j, h),$$

and the density is $\rho_i = \sum_j m_j W(x_i - x_j, h)$, with $j = i$ included. Conditions 1 and 3 make the continuous estimate $\int A(x')W(x - x', h)\,dx'$ exact for linear $A$ and accurate to $O(h^2)$ for smooth $A$, with leading error $\frac{h^2}{2}\mu_2\nabla^2 A$, where $\mu_2 h^2$ is the second moment $\int r_1^2 W\,dr$ along one axis. The particle sum adds a second error that depends on how the particles are arranged; it does not go to zero as $h \to 0$ with $h/\Delta x$ fixed.

**The cubic spline (M4) kernel** of Monaghan and Lattanzio (1985), with $q = |r|/h$:

$$w(q) = \sigma_d \begin{cases} 1 - \frac32 q^2 + \frac34 q^3, & 0 \le q < 1,\\ \frac14 (2 - q)^3, & 1 \le q < 2,\\ 0, & q \ge 2, \end{cases} \qquad \sigma_1 = \frac23,\ \sigma_2 = \frac{10}{7\pi},\ \sigma_3 = \frac1\pi.$$

It is the cubic [B-spline](/b-spline/) on knots spaced $h$ apart, so it is twice continuously differentiable. Its second moment in 1D is $\int x^2W\,dx = \frac{h^2}3$.

**The Wendland C2 kernel**, from Wendland's (1995) compactly supported functions, written with support $2h$:

$$w(q) = \frac5{8}\bigl(1 - \tfrac q2\bigr)^3\bigl(1 + \tfrac{3q}2\bigr) \text{ in 1D}, \qquad w(q) = \sigma_d\bigl(1 - \tfrac q2\bigr)^4(1 + 2q) \text{ in 2D and 3D},\ \sigma_2 = \frac7{4\pi},\ \sigma_3 = \frac{21}{16\pi},$$

for $q < 2$ and zero beyond. Its 1D second moment is $\frac8{21}h^2$. The normalizations above were checked by numerical integration.

## Examples and non-examples

**A uniform 1D lattice, by hand.** Particles of mass 1 at the integers ($\Delta x = 1$), so the true density is 1. With the cubic spline and $h = 1$, only the particle itself and its two neighbors are inside the support:

$$\rho_i = W(0) + 2W(1) = \tfrac23 + 2 \cdot \tfrac23 \cdot \tfrac14 = 1.$$

The gradient estimate of $A(x) = x$ at $x_i = 0$ is $\sum_j x_j \frac{\partial}{\partial x}W(x - x_j)\big|_{x=0} = -\sum_{j = \pm1} j \cdot \frac{dW}{dr}(1)\,\mathrm{sign}(j) = 2 \cdot \frac23 \cdot \frac34 = 1$, also exact. Other ratios $h/\Delta x$ give small lattice errors:

| $h/\Delta x$ | 1 | 1.2 | 1.5 | 2 |
|---|---|---|---|---|
| $\rho_i$, cubic spline | 1 | 1.00180 | 1.00412 | 1 |
| $\rho_i$, Wendland C2 | 1.01563 | 1.00294 | 1.00309 | 1.00098 |
| gradient of $x$, cubic spline | 1 | 1.02238 | 0.98765 | |

These errors do not shrink when $h$ and $\Delta x$ are refined together. This is the zeroth-order particle error of SPH, and it is why kernel choice and $h/\Delta x$ are rules of thumb ($h/\Delta x$ from about 1.2 to 1.5 for the cubic spline in common use).

**The values at the center in 2D.** $W(0, h) = 0.454728/h^2$ for the cubic spline and $0.557042/h^2$ for Wendland C2. The graphics SPH pages use the first value.

**The graphics kernels.** Müller, Charypar and Gross (2003) use poly6, $W(r) = \frac4{\pi h^8}(h^2 - r^2)^3$ in 2D, for the density, and spiky, $\frac{10}{\pi h^5}(h - r)^3$, for the pressure gradient, both with support $h$. Both meet conditions 1 to 4. Poly6 has a zero gradient at $r \to 0$, so pressure forces from it vanish for close pairs and particles clump; spiky has a nonzero gradient there, which is why it is used for pressure. Spiky has a kink at $r = 0$, so it fails the smoothness condition 5 at the center.

**Non-examples.**
- The Gaussian $W = (\pi h^2)^{-d/2}e^{-|r|^2/h^2}$ meets every condition except compact support. Gingold and Monaghan used it in 1977; with it every pair of particles interacts, so the cost is $N^2$ pairs unless it is cut off, and a cut-off breaks the normalization slightly.
- A top hat, constant inside $|r| < h$ and zero outside, is normalized and compactly supported, but its gradient is zero inside and a delta at the edge. Gradient estimates with it are useless.
- A kernel with a negative region (some higher-order kernels) can give negative densities near voids.

## Related definitions

- **Pairing instability.** With many neighbors per particle, B-spline kernels such as the cubic spline let particles form close pairs. Dehnen and Aly (2012) show that a kernel whose Fourier transform is nonnegative avoids this, and that the Wendland kernels meet this condition while the B-splines do not. So the Wendland kernels allow larger neighbor numbers and better convergence.
- **Kernel density estimation.** The density estimate is a [kernel density estimate](/kernel-density-estimation/) of the mass distribution, with $h$ in the role of the bandwidth.
- **Partition of unity.** The normalized sums $W_{ij}/\sum_k W_{ik}$ (the Shepard correction) form a [partition of unity](/partition-of-unity/) and make the estimate of a constant exact on any particle arrangement.
- **Smoothing length.** The parameter $h$; with variable $h_i$ the pair kernel uses an average of $W(r, h_i)$ and $W(r, h_j)$, or $W(r, \bar h_{ij})$, to keep the forces symmetric.
- **Neighbor search.** Compact support means the neighbors of a particle are found by a [fixed-radius search](/fixed-radius-near-neighbors/) with radius $2h$, usually with a cell list.

## References
