---
tag: Y79Q7Y
kind: problem
slug: calderon-problem
name: Calderon problem
aliases:
- electrical impedance tomography
- EIT
area: imaging-and-inverse-problems/tomographic-reconstruction
level: advanced
summary: Recover the conductivity inside a body from the map that sends boundary voltages to boundary currents, a severely ill-posed nonlinear problem.
model: real-ram
prereqs: [inverse-problem, poisson-equation, well-posed-problem]
see_also: [d-bar-method, tomographic-reconstruction-problem, degree-of-ill-posedness, gauss-newton-algorithm, finite-element-method, tikhonov-regularization, levenberg-marquardt, diffraction-tomography]
sources:
  - paper: doi:10.1590/S0101-82052006000200002
    title: A. P. Calderon, On an inverse boundary value problem, Computational and Applied Mathematics 25(2-3), 2006
    locator: reprint of the 1980 paper in the Seminar on Numerical Analysis and its Applications to Continuum Physics, Rio de Janeiro, pp. 65 to 73 (the problem, and uniqueness for the linearized problem at a constant conductivity)
  - paper: doi:10.2307/1971291
    title: J. Sylvester and G. Uhlmann, A global uniqueness theorem for an inverse boundary value problem, Annals of Mathematics 125(1), 1987
    locator: the paper starting at p. 153 (uniqueness for smooth conductivities in dimension 3 and higher)
  - paper: doi:10.2307/2118653
    title: A. I. Nachman, Global uniqueness for a two-dimensional inverse boundary value problem, Annals of Mathematics 143(1), 1996
    locator: the paper starting at p. 71 (uniqueness in the plane through a d-bar equation, with a reconstruction method)
  - paper: doi:10.4007/annals.2006.163.265
    title: K. Astala and L. Paivarinta, Calderon's inverse conductivity problem in the plane, Annals of Mathematics 163(1), 2006
    locator: pp. 265 to 299 (uniqueness for bounded measurable conductivities in the plane)
  - paper: doi:10.1080/00036818808839730
    title: G. Alessandrini, Stable determination of conductivity by boundary measurements, Applicable Analysis 27(1-3), 1988
    locator: pp. 153 to 172 (a logarithmic stability estimate under a priori bounds)
  - paper: doi:10.1088/0266-5611/17/5/313
    title: N. Mandache, Exponential instability in an inverse problem for the Schrodinger equation, Inverse Problems 17(5), 2001
    locator: pp. 1435 to 1444 (logarithmic stability is the best possible)
  - book: isbn:9781611972337
    title: J. L. Mueller and S. Siltanen, Linear and Nonlinear Inverse Problems with Practical Applications, SIAM, 2012
    locator: Chapters 12 to 16 (the conductivity problem, its data and reconstruction methods; general locator)
---

The Calderon problem asks for the electrical conductivity $\gamma(x)$ inside a body $\Omega$ when only measurements on the boundary are available. One applies a voltage $\varphi$ on the boundary $\partial\Omega$, the potential $u$ inside solves $\nabla\cdot(\gamma\nabla u) = 0$, and one measures the current $\gamma\,\partial_\nu u$ that flows out through the boundary. The data are the map $\Lambda_\gamma$ from all boundary voltages to the boundary currents, the Dirichlet-to-Neumann map. Calderon posed the problem in 1980. The answer is unique under mild conditions, but the problem is nonlinear and severely ill-posed: the best possible stability is logarithmic, so features deep inside the body leave an exponentially small trace on the data. It is the mathematical model of electrical impedance tomography, an imaging method in medicine and geophysics.

## In plain words

Put electrodes on the skin, push small currents through the body, and measure the voltages at the electrodes. Different tissues let electric current pass with different ease. The question is whether the map of this ease inside the body can be found from these surface measurements alone.

Unlike X-rays, electric current does not move along straight lines. It spreads through the whole body and takes the easiest path. So each measurement mixes up information from everywhere, and a change deep inside changes the surface readings only very little. In theory, complete and exact measurements fix the answer. In practice, small errors in the measurements can hide large changes inside, so the images are blurred, especially far from the electrodes.

## Definition

Let $\Omega \subset \mathbb{R}^n$, $n \ge 2$, be a bounded domain with a Lipschitz boundary, and let $\gamma \in L^\infty(\Omega)$ with $\gamma \ge c > 0$. For $\varphi \in H^{1/2}(\partial\Omega)$ let $u \in H^1(\Omega)$ solve
$$\nabla\cdot(\gamma\nabla u) = 0 \text{ in } \Omega, \qquad u = \varphi \text{ on } \partial\Omega.$$
The solution exists and is unique. The **Dirichlet-to-Neumann map** is $\Lambda_\gamma \varphi = \gamma\,\partial_\nu u|_{\partial\Omega}$, with $\nu$ the outer normal, taken in the weak sense in $H^{-1/2}(\partial\Omega)$. It is linear in $\varphi$, self-adjoint, and its quadratic form is the power that the current dissipates:
$$\langle \Lambda_\gamma\varphi, \varphi\rangle = \int_\Omega \gamma\,|\nabla u|^2\,dx.$$

**The problem.** Given $\Lambda_\gamma$, find $\gamma$. The map $\gamma \mapsto \Lambda_\gamma$ is nonlinear. A related question is uniqueness: does $\Lambda_{\gamma_1} = \Lambda_{\gamma_2}$ imply $\gamma_1 = \gamma_2$?

The equation is a generalization of the Laplace equation, the homogeneous case of the [Poisson equation](/poisson-equation/), with a variable coefficient. Since constants solve it, $\Lambda_\gamma 1 = 0$, and the currents always add up to 0 on the boundary.

## Variants

- **Full or partial data.** The full problem knows $\Lambda_\gamma$ on the whole boundary. In partial data problems, voltages are applied or currents measured on only part of the boundary.
- **Electrode models.** In practice there are finitely many electrodes, and the data are a matrix: the voltages for each pattern of injected currents. Models of the contact between the electrodes and the skin make the forward problem more accurate. The data are then finite, and $\gamma$ must be found from a finite matrix with a regularization method.
- **Admittivity.** With an alternating current of angular frequency $\omega$, the coefficient is complex, $\gamma = \sigma + i\omega\varepsilon$, and both the conductivity $\sigma$ and the permittivity $\varepsilon$ affect the data.
- **Anisotropic conductivity.** If $\gamma$ is a matrix, the problem is not unique: a change of coordinates that is the identity on the boundary changes $\gamma$ but not $\Lambda_\gamma$. The question is then uniqueness up to such changes.
- **The Schrodinger problem.** For $\gamma \in C^2$, the substitution $v = \sqrt{\gamma}\,u$ turns the equation into $-\Delta v + q v = 0$ with $q = \Delta\sqrt{\gamma}/\sqrt{\gamma}$. The data become the Dirichlet-to-Neumann map of the potential $q$, and the problem becomes the inverse problem for the Schrodinger equation at zero energy.
- **The linearized problem.** Near a known conductivity $\gamma_0$, a small change $\delta\gamma$ changes the quadratic form by $\int \delta\gamma\, \nabla u_1 \cdot \nabla u_2$, to first order. Calderon showed that at a constant $\gamma_0$ these integrals determine $\delta\gamma$.

## Examples

**A constant conductivity on the unit disk.** For $\gamma = \gamma_0$ the solutions are harmonic, and $u = r^{|k|} e^{ik\phi}$ in polar coordinates has the boundary value $e^{ik\phi}$. Its normal derivative at $r = 1$ is $|k| e^{ik\phi}$. So $\Lambda_\gamma$ is diagonal in the Fourier basis, with the eigenvalues $\gamma_0 |k|$, $k \in \mathbb{Z}$.

**Two layers.** Let $\gamma = \gamma_1$ on the disk $r < \rho$ and $\gamma_2$ on the ring $\rho < r < 1$. In the ring $u = a r^k + b r^{-k}$, inside $u = c\, r^k$, and the potential and the current are continuous at $r = \rho$. This gives $b = m\, a\, \rho^{2k}$ with $m = (\gamma_2 - \gamma_1)/(\gamma_2 + \gamma_1)$, and the eigenvalues for $k \ge 1$ are
$$\lambda_k = \gamma_2\, k\, \frac{1 - m\rho^{2k}}{1 + m\rho^{2k}}.$$
For $\rho = 0.5$, $\gamma_1 = 2$ and $\gamma_2 = 1$, so $m = -1/3$: $\lambda_1 = 13/11 = 1.1818$ and $\lambda_2 = 98/47 = 2.0851$, against $1$ and $2$ for the constant conductivity 1. The difference $\lambda_k - k$ is about $(2k/3)\, 4^{-k}$: $0.00326$ for $k = 5$, and $6.4 \cdot 10^{-6}$ for $k = 10$. So the inner disk changes the data by an amount that decays exponentially with the frequency $k$. A measurement error of $10^{-3}$ hides everything above $k \approx 5$. This is the severe ill-posedness of the problem in its simplest form.

**A conductivity that only the boundary sees.** For a radial $\gamma$ on the disk, $\Lambda_\gamma$ is diagonal in the Fourier basis, so it is a single sequence of numbers $\lambda_k$. A change of $\gamma$ near the center changes $\lambda_k$ by an amount that decays like $r_0^{2k}$ when the change has support in $r < r_0$, as in the two-layer example.

## Known algorithms

| Method | What it does |
|---|---|
| [D-bar method](/d-bar-method/) | in the plane, computes a scattering transform from $\Lambda_\gamma$ and solves a d-bar equation for each point; a direct method that follows Nachman's uniqueness proof, regularized by a cutoff of the scattering transform |
| Regularized output least squares | minimizes $\|\Lambda_\gamma^{\text{model}} - \text{data}\|^2$ plus a penalty, with a [finite element](/finite-element-method/) forward solver and [Gauss-Newton](/gauss-newton-algorithm/) or [Levenberg-Marquardt](/levenberg-marquardt/) steps; the common method with electrode data |
| One-step linearization | one Gauss-Newton step from a constant conductivity with [Tikhonov regularization](/tikhonov-regularization/); fast and used for time-difference images of the lungs |
| Factorization and other sampling methods | find the shape of inclusions in a known background, not the values of $\gamma$ |
| Statistical methods | a [Bayesian inverse problem](/bayesian-inverse-problem/) with a prior on $\gamma$, sampled or maximized |

## Bounds

- **Uniqueness in dimension 3 and higher.** Sylvester and Uhlmann (1987) proved that $\Lambda_\gamma$ determines $\gamma$ for smooth $\gamma$, with complex geometrical optics solutions of the Schrodinger form. Later work lowered the smoothness.
- **Uniqueness in the plane.** Nachman (1996) proved it for $\gamma \in W^{2,p}$, $p > 1$, with a constructive proof. Astala and Paivarinta (2006) proved it for every $\gamma \in L^\infty$ with $\gamma \ge c > 0$, which is the natural class.
- **The linearized problem.** Calderon (1980) proved injectivity of the derivative of $\gamma \mapsto \Lambda_\gamma$ at a constant conductivity.
- **Stability.** Under a priori bounds on $\gamma$ in a Sobolev norm, Alessandrini (1988) proved a logarithmic estimate: $\|\gamma_1 - \gamma_2\|_{L^\infty} \le C\,|\log \|\Lambda_{\gamma_1} - \Lambda_{\gamma_2}\||^{-\delta}$ for some $\delta > 0$ when the difference of the maps is small. Mandache (2001) proved that no estimate of a better type, such as a Holder estimate, holds in general. So the problem is severely ill-posed, which is consistent with the exponential decay in the two-layer example.
- **Data against resolution.** With $L$ electrodes, the data matrix has at most $L(L-1)/2$ independent entries, because $\Lambda_\gamma$ is self-adjoint and the currents add up to 0. This bounds the number of parameters that can be found, and the logarithmic stability means that the useful number is far smaller.

## Reductions

- **To a Schrodinger problem.** The substitution $v = \sqrt{\gamma}\,u$ reduces the problem for $\gamma \in C^2$ to the inverse problem for $-\Delta + q$, as in the variants. The boundary values of $\gamma$ and of its normal derivative are determined by $\Lambda_\gamma$, so $\Lambda_q$ is known from $\Lambda_\gamma$.
- **To a d-bar equation in the plane.** Nachman's proof writes special solutions $\psi(x, k) \approx e^{ikx}$ with a complex parameter $k$, computes their boundary values and a scattering transform $\mathbf{t}(k)$ from $\Lambda_\gamma$, and gets $\gamma$ from the solution of a $\bar\partial$ equation in $k$. This is the basis of the [D-bar method](/d-bar-method/).
- **To nonlinear least squares.** With finitely many electrodes and a finite element model, the problem is a nonlinear least squares problem in the element values of $\gamma$, which is the input of the regularized iterative methods.
- **Compared with X-ray tomography.** In X-ray tomography the [Radon transform](/radon-transform/) is linear and the problem is mildly ill-posed, with [degree](/degree-of-ill-posedness/) $1/2$. Here the forward map is nonlinear and the stability is logarithmic, which is worse than any power.

## Applications

Electrical impedance tomography is the imaging method that collects this data with electrodes and solves this problem.

- **Medical imaging.** Monitoring of the lungs of patients on a ventilator, where the changes of the conductivity with breath are large and a time-difference image is enough. Studies of breast and brain imaging use it too.
- **Geophysics.** Electrical resistivity surveys find the conductivity of the ground from electrodes on the surface or in boreholes.
- **Industry.** Process tomography watches the mixing of fluids in pipes and tanks, and nondestructive testing looks for cracks.

## References
