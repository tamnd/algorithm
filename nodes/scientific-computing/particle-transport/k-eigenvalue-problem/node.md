---
tag: K9VWDE
kind: problem
slug: k-eigenvalue-problem
name: k-eigenvalue problem
aliases:
- criticality eigenvalue problem
area: scientific-computing/particle-transport
level: core
summary: Find the largest eigenvalue k_eff and fundamental mode of the transport equation with the fission source divided by k; k_eff = 1 means critical.
prereqs: [linear-boltzmann-transport-equation, eigenvalue-problem]
see_also: [monte-carlo-criticality, fission-source-entropy, power-iteration, source-iteration, perron-frobenius-theorem, spectral-radius, adjoint-importance-function, arnoldi-iteration]
sources:
  - book: "George I. Bell and Samuel Glasstone, Nuclear Reactor Theory, Van Nostrand Reinhold, 1970"
    locator: the chapters on the time-independent transport equation of a multiplying system, the eigenvalue k and the fundamental mode
  - book: isbn:9780471092452
    title: E. E. Lewis and W. F. Miller, Computational Methods of Neutron Transport, Wiley, 1984 (ANS reprint 1993)
    locator: the chapters on criticality calculations, the power (outer) iteration and its acceleration
  - paper: doi:10.1051/m2an:1999160
    title: Gregoire Allaire and Guillaume Bal, Homogenization of the criticality spectral equation in neutron transport, ESAIM Mathematical Modelling and Numerical Analysis 33(4), 1999, 721-746
    locator: the existence of a simple first eigenvalue with a positive eigenfunction by the Krein-Rutman theorem, under the hypotheses of the paper on the cross sections
  - book: isbn:9780486462936
    title: Jerome Spanier and Ely M. Gelbard, Monte Carlo Principles and Neutron Transport Problems, Addison-Wesley, 1969, Dover reprint 2008
    locator: the chapter on the Monte Carlo solution of eigenvalue problems
---

The k-eigenvalue problem asks for the multiplication factor $k_{\mathrm{eff}}$ of a system that contains fissile material, and for the shape of the neutron population that the system keeps when it runs by itself. It is the [linear Boltzmann transport equation](/linear-boltzmann-transport-equation/) with no external source, in which the fission source is divided by an unknown number $k$ so that a steady solution exists. The largest such $k$ is $k_{\mathrm{eff}}$: the system is critical when $k_{\mathrm{eff}} = 1$, subcritical below 1 and supercritical above 1. Almost every method for it, deterministic or [Monte Carlo](/monte-carlo-criticality/), is a form of [power iteration](/power-iteration/) over fission generations.

## In plain words

In a reactor, a neutron causes a fission, the fission gives a few new neutrons, and some of them cause new fissions. The question is: on average, how many neutrons of the next generation come from one neutron of this generation? That number is $k_{\mathrm{eff}}$. If it is exactly 1, the population stays the same. If it is a little more than 1, the population grows; if it is less than 1, it dies out.

After many generations, the population takes a fixed shape in space and energy, no matter how it started. This shape is the fundamental mode. The problem is to find the number and the shape. Neutrons that leak out of the surface are lost, so a small body has a smaller $k_{\mathrm{eff}}$ than a large body of the same material.

## Definition

**Input.** A bounded body $D$ with vacuum boundary, and for each position $x$ and energy $E$ the total cross section $\Sigma_t$, the scattering kernel $\Sigma_s(E' \to E, \Omega' \cdot \Omega)$, the fission production $\nu\Sigma_f$ and the fission spectrum $\chi(E)$, all in $\mathrm{cm}^{-1}$ except $\chi$, which is a probability density.

**Question.** Write the transport operator and the fission operator as
$$L\psi = \Omega \cdot \nabla\psi + \Sigma_t\psi - \iint \Sigma_s(E' \to E, \Omega' \cdot \Omega)\, \psi(x, \Omega', E')\, d\Omega'\, dE',$$
$$F\psi = \frac{\chi(E)}{4\pi} \iint \nu\Sigma_f(x, E')\, \psi(x, \Omega', E')\, d\Omega'\, dE',$$
with $\psi = 0$ on the incoming part of the boundary. Find the largest real number $k$ and a function $\psi \ge 0$, not zero, with
$$L\psi = \frac{1}{k} F\psi.$$
This $k$ is $k_{\mathrm{eff}}$, and $\psi$ is the fundamental mode, defined up to a constant factor. In operator form, $k_{\mathrm{eff}}$ is the [spectral radius](/spectral-radius/) of $F L^{-1}$, the operator that maps one generation of fission neutrons to the next one. Its eigenfunction $s = F\psi$ is the fission source.

**Existence.** This is a theorem, for hypotheses that the source must state. If the cross sections are bounded, the fission production is positive on a part of the body, and the transport operator couples all positions and energies (no part of the system is cut off from the others), then $F L^{-1}$ is a compact operator that keeps the cone of nonnegative functions, and the Krein-Rutman theorem gives: the spectral radius $k_{\mathrm{eff}}$ is a simple eigenvalue, it has a positive eigenfunction, and every other eigenvalue has a smaller absolute value. Allaire and Bal (1999) use this result in this form. In a discretized problem the same role is played by the [Perron-Frobenius theorem](/perron-frobenius-theorem/) for a nonnegative irreducible matrix.

## Variants

- **The one-speed and multigroup problems.** One energy group, or a [multigroup approximation](/multigroup-approximation/) in which $F$ maps the fission rate of all groups into the groups of the fission spectrum.
- **The diffusion problem.** $-\nabla \cdot D \nabla\phi + \Sigma_a\phi = (1/k)\nu\Sigma_f\phi$ with $\phi = 0$ on the boundary or on an extrapolated boundary, from the [diffusion approximation of transport](/diffusion-approximation-of-transport/).
- **The adjoint problem.** $L^+\psi^+ = (1/k)F^+\psi^+$ has the same $k_{\mathrm{eff}}$. Its fundamental mode is the [importance](/adjoint-importance-function/) of a neutron for the population many generations later, and it weights the first-order perturbation formula for the reactivity $\rho = (k - 1)/k$.
- **Other eigenvalues.** The $\alpha$-eigenvalue problem looks for solutions $e^{\alpha t}\psi$ of the time-dependent equation; the $c$-eigenvalue problem scales the number of secondaries per collision; search problems scale a size or a concentration until $k_{\mathrm{eff}} = 1$.
- **Higher modes.** The second eigenvalue $k_2$ and its mode. The dominance ratio $k_2 / k_{\mathrm{eff}}$ sets the speed of power iteration.
- **The subcritical source problem.** With $k_{\mathrm{eff}} < 1$ and an external source $q$, the problem $L\psi = F\psi + q$ has a unique solution, and the total population is about the source strength divided by $1 - k_{\mathrm{eff}}$ (a rule that is exact in the fundamental mode approximation).

## Examples

**Infinite medium, one group.** With no leakage and no space dependence, the balance of one generation is production over absorption: $k_\infty = \nu\Sigma_f / \Sigma_a$. For $\Sigma_t = 1$, $\Sigma_s = 0.9$ and $\nu\Sigma_f = 0.12\ \mathrm{cm}^{-1}$, $\Sigma_a = 0.1$ and $k_\infty = 1.2$. Each neutron has $1/(1 - 0.9) = 10$ collisions on average before it is absorbed.

**A bare slab in diffusion theory.** Take the same material in a slab of width $L = 20$ cm with isotropic scattering, so $D = 1/(3\Sigma_t) = 1/3$ cm. The fundamental mode with $\phi = 0$ at both faces is $\cos(\pi x / L)$ about the center, the buckling is $B^2 = (\pi/L)^2 = 0.024674\ \mathrm{cm}^{-2}$, and
$$k = \frac{\nu\Sigma_f}{\Sigma_a + D B^2} = \frac{0.12}{0.1 + 0.008225} = 1.108804.$$
The second mode $\sin(2\pi x / L)$ has $B^2 = (2\pi/L)^2$ and $k_2 = 0.902943$, so the dominance ratio is $0.8143$. With the extrapolated width $L + 2 \cdot 0.7104/\Sigma_t = 21.4208$ cm, diffusion gives $k = 1.119718$.

**The same slab in transport theory.** A discrete ordinates solve with diamond differences gives $k_{\mathrm{eff}} = 1.120009$ with 80 cells and $S_8$, and $1.120062$ with 320 cells and $S_{16}$ (measurements on this one problem). The first odd mode gives $k_2 = 0.93637$, a dominance ratio of $0.8360$. Diffusion with a zero flux at the true faces is 1% low because it puts the flux to zero too early; the extrapolated boundary removes most of the error. All values are below $k_\infty = 1.2$, because the slab leaks.

**Large bodies converge slowly.** In diffusion theory the dominance ratio of the bare slab is $0.8143$ for $L = 20$ cm, $0.9625$ for $L = 50$ cm and $0.9903$ for $L = 100$ cm. Power iteration reduces the error in the shape by about this factor per generation, so the 100 cm slab needs about 240 generations for each factor of 10.

**A two-region fission matrix by hand.** Let $A_{ij}$ be the expected number of fission neutrons born in region $i$ per fission neutron born in region $j$, with
$$A = \begin{pmatrix} 1.0 & 0.2 \\ 0.3 & 0.5 \end{pmatrix}.$$
The characteristic polynomial is $\lambda^2 - 1.5\lambda + 0.44$, so the eigenvalues are $1.1$ and $0.4$. The fundamental mode is $(2/3, 1/3)$, since $1.0 \cdot 2/3 + 0.2 \cdot 1/3 = 0.7333 = 1.1 \cdot 2/3$. Power iteration from $(1, 0)$, with $k_n$ the total of $A x$ over the total of $x$, gives $k_n = 1.3, 1.161538, 1.121192, 1.107561, 1.102731, 1.100990, \ldots$. The errors $0.2, 0.0615, 0.0212, 0.0076, 0.0027, 0.0010$ fall by a factor that tends to the dominance ratio $0.4/1.1 = 0.3636$.

## Known algorithms

- **Power iteration** (outer iteration): $s^{(n+1)} = F L^{-1} s^{(n)} / k^{(n)}$, with $k^{(n+1)}$ from the ratio of the totals of two fission sources. Each step needs one fixed source solve $L\psi = s/k$, which a deterministic code does by [source iteration](/source-iteration/) and [transport sweeps](/transport-sweep/), with [diffusion synthetic acceleration](/diffusion-synthetic-acceleration/) for the inner iterations.
- **[Monte Carlo criticality](/monte-carlo-criticality/)**: power iteration with a random fission bank, with inactive cycles to converge the source and the [fission source entropy](/fission-source-entropy/) as a check.
- **Shifted and accelerated power iteration.** The Wielandt shift, Chebyshev extrapolation and coarse mesh finite difference acceleration lower the effective dominance ratio.
- **Krylov and Newton methods.** [Arnoldi iteration](/arnoldi-iteration/) on $F L^{-1}$ gives several modes at once; Jacobian-free Newton-Krylov methods solve for $(\psi, k)$ together with a normalization condition.
- **[Inverse iteration](/inverse-iteration/)** with a shift is used for the diffusion problem, where $L$ is a sparse matrix.

## Bounds

- **Rate of power iteration.** A theorem: if $k_{\mathrm{eff}}$ is simple and every other eigenvalue satisfies $|k_i| \le k_2 < k_{\mathrm{eff}}$, the error of the source shape after $n$ steps is $O((k_2/k_{\mathrm{eff}})^n)$, and the error of $k$ is of the same order.
- **Leakage lowers $k$.** A theorem for a homogeneous one-group body: integrate the balance $L\phi = (1/k)\nu\Sigma_f\phi$ over the body; it gives $k = \nu\Sigma_f \int\phi / (\Sigma_a \int\phi + \text{leakage})$, which is below $k_\infty$ when the leakage is positive. More generally, by the positivity of $L^{-1}$, a body that contains a second body of the same material has the larger $k_{\mathrm{eff}}$ of the two.
- **Monte Carlo cost.** The error of a Monte Carlo estimate of $k$ falls like $N^{-1/2}$ in the number of neutron histories, but the estimates of successive generations are correlated, and the source needs a number of generations of order $1/\ln(k_{\mathrm{eff}}/k_2)$ per factor $e$ to converge.

## Reductions

- **To a matrix eigenvalue problem.** Any discretization in space, angle and energy gives a generalized [eigenvalue problem](/eigenvalue-problem/) $A\psi = (1/k)B\psi$, or the standard problem for $B A^{-1}$. The largest eigenvalue of a nonnegative matrix is the subject of the Perron-Frobenius theorem.
- **To a fixed source problem.** Each power step is a fixed source solve of the transport equation with the source $s/k$.
- **From the fission matrix.** Collapsing the transport to the expected number of next-generation fissions in region $i$ from a fission in region $j$ gives a finite matrix whose largest eigenvalue approaches $k_{\mathrm{eff}}$ as the regions get small.

## Applications

- Reactor design: the core loading, the control rod worth and the burnup of the fuel are all set by $k_{\mathrm{eff}}$ and the fundamental mode.
- Criticality safety: storage, transport and processing of fissile material must keep $k_{\mathrm{eff}}$ below 1 with a margin, and the margin is set by validated calculations.
- Kinetics: the adjoint fundamental mode weights the delayed neutron fractions and the prompt neutron lifetime.
- Subcritical systems: accelerator-driven systems and source-driven experiments measure how far $k_{\mathrm{eff}}$ is below 1.

## References
