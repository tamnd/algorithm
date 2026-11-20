---
tag: VGNNE7
kind: theorem
slug: shadow-hamiltonian
name: Shadow Hamiltonian theorem
aliases:
- modified Hamiltonian of a symplectic integrator
area: scientific-computing/molecular-simulation
level: advanced
summary: "For a symplectic method with a small step h on an analytic Hamiltonian, a modified energy near H is conserved to within e^(-c/h) over times exponentially long in 1/h."
prereqs: [symplectic-integrators, backward-error-analysis]
see_also: [verlet-integration, hamiltonian-systems, molecular-dynamics, rattle-algorithm, respa-multiple-time-step, hamiltonian-monte-carlo, smooth-particle-mesh-ewald, floating-point-model]
sources:
  - paper: doi:10.1007/BF02188219
    title: Giancarlo Benettin and Antonio Giorgilli, On the Hamiltonian interpolation of near-to-the-identity symplectic mappings with application to symplectic integration algorithms, Journal of Statistical Physics 74(5-6), 1994, 1117-1143
    locator: the exponentially small error of the interpolating Hamiltonian
  - paper: doi:10.1137/S0036142997329797
    title: Sebastian Reich, Backward error analysis for numerical integrators, SIAM Journal on Numerical Analysis 36(5), 1999, 1549-1570
    locator: modified equations that keep the geometric structure, with exponential estimates
  - book: isbn:9783540306634
    title: Ernst Hairer, Christian Lubich and Gerhard Wanner, Geometric Numerical Integration, second edition, Springer, 2006
    locator: Section IX.3 (modified equations of symplectic methods), Section IX.7 (exponentially small error estimates) and Theorem IX.8.1 (long-time energy conservation)
  - paper: doi:10.1017/S0962492902000144
    title: Ernst Hairer, Christian Lubich and Gerhard Wanner, Geometric numerical integration illustrated by the Störmer-Verlet method, Acta Numerica 12, 2003, 399-450
    locator: the modified Hamiltonian of the Störmer-Verlet method and its long-time energy behaviour
  - paper: doi:10.1103/PhysRevE.50.2271
    title: Søren Toxvaerd, Hamiltonians for discrete dynamics, Physical Review E 50(3), 1994, 2271-2274
    locator: the conserved Hamiltonian of the discrete Verlet dynamics in molecular dynamics
  - paper: doi:10.1016/j.jcp.2004.12.009
    title: Robert D. Engle, Robert D. Skeel and Matthew Drees, Monitoring energy drift with shadow Hamiltonians, Journal of Computational Physics 206(2), 2005, 432-452
    locator: the use of computed shadow Hamiltonians to measure drift in molecular dynamics
---

The shadow Hamiltonian theorem explains why the energy of a molecular dynamics run with the [Verlet method](/verlet-integration/) does not drift. It has three hypotheses: the method is [symplectic](/symplectic-integrators/), the Hamiltonian $H$ is analytic, and the step $h$ is small. Then there is a modified Hamiltonian $\tilde H = H + h^p H_{p+1} + \cdots$, close to $H$, such that the numerical solution conserves $\tilde H$ up to an error of size $e^{-h_0/h}$ in each step. As long as the solution stays in a bounded region, $H$ itself then oscillates in a band of width $O(h^p)$ for times exponentially long in $1/h$. The theorem is a result of [backward error analysis](/backward-error-analysis/): the method is the exact flow of a nearby system, up to that tiny error. Backward error analysis gives a modified equation for any method; the special fact for symplectic methods is that the modified equation is again Hamiltonian. The theorem is about energy, not about integrators: it says when a method such as RATTLE or RESPA keeps a good energy, and when it does not.

## Statement

**Setting.** Let $H : U \to \mathbb{R}$ be a real analytic Hamiltonian on an open set $U \subset \mathbb{R}^{2d}$, and $y' = J^{-1} \nabla H(y)$ the Hamiltonian system. Let $\Phi_h$ be a one-step method of order $p$ that is symplectic, and whose map is analytic in $h$ and $y$; the Störmer-Verlet method is an example, with $p = 2$. Let $K \subset U$ be compact.

**Theorem (Benettin and Giorgilli, 1994; Hairer, Lubich and Wanner, Theorem IX.8.1).** There are $h_0 > 0$, $C$ and, for each $h \le h_0$, an analytic function $\tilde H_h = H + h^p H_{p+1} + \cdots + h^{N-1} H_N$, with $N$ of order $h_0 / h$, such that for $y \in K$
$$|\tilde H_h(\Phi_h(y)) - \tilde H_h(y)| \le C h \, e^{-h_0/h}, \qquad |\tilde H_h(y) - H(y)| \le C h^p.$$
So if the numerical solution $y_n = \Phi_h^n(y_0)$ stays in $K$, then
$$\tilde H_h(y_n) = \tilde H_h(y_0) + O(n h \, e^{-h_0/h}), \qquad H(y_n) = H(y_0) + O(h^p) \quad \text{for } nh \le e^{h_0/2h}.$$

**Exact case.** For the harmonic oscillator $H = \frac12 (p^2 + x^2)$ and the velocity Verlet method with $0 < h < 2$, the quadratic form $\tilde E = \frac12 p^2 + \frac12 (1 - h^2/4) x^2$ is conserved exactly by every step.

## In plain words

A simulation of moving atoms makes a small error at every step, so you would expect the total energy to wander away over a long run. With the most common method it does not. The energy wobbles a little, but its average stays the same for millions of steps.

The reason is that the method follows the laws of motion of a slightly different system almost perfectly. That other system has its own energy, very close to the true one, and the simulation keeps it almost exactly. The true energy can then only move by the small difference between the two, so it wobbles but cannot drift.

This needs three things: a method of the right kind, smooth forces, and a step that is small against the fastest motion. Without any one of them, a slow drift can come back.

## Proof

**The exact case.** One velocity Verlet step for $x'' = -x$ is $p_{1/2} = p - \frac{h}{2} x$, $x_1 = x + h p_{1/2}$, $p_1 = p_{1/2} - \frac{h}{2} x_1$. In terms of $p_{1/2}$, the two points satisfy $p = p_{1/2} + \frac{h}{2} x$ and $p_1 = p_{1/2} - \frac{h}{2} x_1$. Write $c = 1 - h^2/4$. Then
$$p^2 + c x^2 = p_{1/2}^2 + h p_{1/2} x + x^2, \qquad p_1^2 + c x_1^2 = p_{1/2}^2 - h p_{1/2} x_1 + x_1^2.$$
The difference is $x^2 - x_1^2 + h p_{1/2}(x + x_1) = (x + x_1)(x - x_1 + h p_{1/2}) = 0$, since $x_1 - x = h p_{1/2}$. So $\tilde E$ is conserved. For $0 < h < 2$, $c > 0$, so the level sets of $\tilde E$ are ellipses and the solution is bounded.

**The modified equation is Hamiltonian.** Backward error analysis gives, for any method of order $p$ with smooth coefficients, vector fields $f_j$ such that the flow $\tilde\varphi_{N,h}$ of the truncated modified equation $y' = f(y) + h^p f_{p+1}(y) + \cdots + h^{N-1} f_N(y)$ satisfies $\Phi_h(y) = \tilde\varphi_{N,h}(y) + O(h^{N+1})$. We show by induction that each $f_j = J^{-1} \nabla H_j$ on a simply connected domain. Suppose that $f_1 = f, \ldots, f_N$ are Hamiltonian. Then $\tilde\varphi_{N,h}$ is the flow of a Hamiltonian system, so it is symplectic. The next term is defined by $\Phi_h(y) = \tilde\varphi_{N,h}(y) + h^{N+1} f_{N+1}(y) + O(h^{N+2})$, so
$$\Phi_h'(y) = \tilde\varphi_{N,h}'(y) + h^{N+1} f_{N+1}'(y) + O(h^{N+2}).$$
Insert this into the symplecticity conditions $\Phi_h'^{\mathsf T} J \Phi_h' = J$ and $\tilde\varphi_{N,h}'^{\mathsf T} J \tilde\varphi_{N,h}' = J$, and use $\tilde\varphi_{N,h}' = I + O(h)$. The terms of order $h^{N+1}$ give $f_{N+1}'^{\mathsf T} J + J f_{N+1}' = 0$, which says that the Jacobian of $J f_{N+1}$ is symmetric. By the Poincaré lemma, $J f_{N+1} = \nabla H_{N+1}$ for a function $H_{N+1}$ on a simply connected domain. So every truncation is a Hamiltonian system with the Hamiltonian $\tilde H = H + h^p H_{p+1} + \cdots + h^{N-1} H_N$, and its flow conserves $\tilde H$ exactly.

**The exponential estimate.** This step is cited, not proved here. For analytic $H$ and an analytic method, Cauchy estimates bound the functions $f_j$ on a slightly smaller domain by a constant times $j!$ times a power. Choosing $N$ of order $h_0/h$, which is near the smallest term of the series, gives
$$|\Phi_h(y) - \tilde\varphi_{N,h}(y)| \le C h \, e^{-h_0/h} \quad \text{for } y \in K.$$
This is the theorem of Benettin and Giorgilli (1994), and Section IX.7 of Hairer, Lubich and Wanner gives it in this form.

**The energy statement.** The flow $\tilde\varphi_{N,h}$ conserves $\tilde H$, so
$$\tilde H(\Phi_h(y)) - \tilde H(y) = \tilde H(\Phi_h(y)) - \tilde H(\tilde\varphi_{N,h}(y)),$$
and $\nabla \tilde H$ is bounded on a neighbourhood of $K$, so this difference is at most $C' h e^{-h_0/h}$. Summing over $n$ steps that stay in $K$ gives $|\tilde H(y_n) - \tilde H(y_0)| \le C' n h \, e^{-h_0/h}$. On $K$, $|H - \tilde H| \le C h^p$, because the terms $H_j$ are bounded and $h \le h_0$. For $nh \le e^{h_0/2h}$, the sum is at most $C' e^{-h_0/2h}$, which is smaller than $h^p$ for small $h$, and so $|H(y_n) - H(y_0)| = O(h^p)$. $\square$

The exact case and the Hamiltonian form of the modified equation are proved here in full. The exponential estimate is the cited part.

## Consequences

- **The exact case by hand.** With $h = 0.5$ and the start $(x, p) = (1, 0)$, one step gives $x_1 = 0.875$ and $p_1 = -0.46875$. Then $\tilde E = 0.46875$ before and after, while $H$ falls from $0.5$ to $0.4926758$. In general $H - \frac12 = \frac{h^2}{8}(x^2 - 1)$, so $H$ moves in the band $[\frac12 - \frac{h^2}{8}, \frac12]$ for all time.
- **The second-order term.** For velocity Verlet and $H = \frac12 p^2 + V(q)$ in one dimension, the first correction is $h^2 \bigl(\frac{1}{12} V''(q) p^2 - \frac{1}{24} V'(q)^2\bigr)$. For the pendulum $V = -\cos q$ from $q = 1$, $p = 0$, run to the time 200, the largest error in $H$ is $4.25 \times 10^{-3}$, $1.06 \times 10^{-3}$ and $2.65 \times 10^{-4}$ for $h = 0.2, 0.1, 0.05$, which is order 2. The error in $H + h^2 H_3$ is $2.9 \times 10^{-5}$, $1.8 \times 10^{-6}$ and $1.1 \times 10^{-7}$, which is order 4 (a measurement).
- **No drift in practice.** The same pendulum with $h = 0.1$ for $10^6$ steps has the largest energy error $1.0612 \times 10^{-3}$ in the first $10^4$ steps and the same value in the last $10^4$. The explicit midpoint method, of the same order but not symplectic, has the error $0.087$ in the first $10^4$ steps, and by the end the pendulum has gained so much energy that it turns over the top, with the error $879$ (a measurement).
- **Constrained and split methods.** [RATTLE](/rattle-algorithm/) is symplectic on the constraint manifold, and [RESPA](/respa-multiple-time-step/) is a composition of exact Hamiltonian flows, so both have a modified Hamiltonian when $h$ is small against every time scale of the system.
- **Forces must be gradients.** [Smooth particle mesh Ewald](/smooth-particle-mesh-ewald/) gives forces that are the gradient of an energy, so the theorem can apply. Plain particle mesh Ewald does not, and its runs can drift.
- **Monitoring.** A computed approximation of $\tilde H$ moves much less than $H$, so its drift shows errors such as a loose constraint tolerance that the noise of $H$ would hide (Engle, Skeel and Drees, 2005).
- **Hamiltonian Monte Carlo.** In [HMC](/hamiltonian-monte-carlo/), the acceptance rate depends on the change of $H$ along a Verlet trajectory. Because the change is $O(h^2)$ and does not grow with the length of the trajectory, long trajectories keep a good acceptance rate.

## Tightness

- **The step must be small.** For the harmonic oscillator, $\tilde E$ degenerates as $h \to 2$, and for $h > 2$ velocity Verlet is unstable. In molecular dynamics, the fastest motion sets the limit, and RESPA with an outer step near half a fast period shows resonant growth, even though each step is symplectic.
- **Analyticity.** A force with a cutoff, a switch that is only a few times differentiable, or a table with linear interpolation is not analytic. Then only a finite number of terms of the modified Hamiltonian exist, and the available estimates hold only over times that grow like a power of $1/h$. A force that jumps at the cutoff gives energy errors at each crossing, and these add up to a drift.
- **Rounding.** In floating point, every step adds rounding errors of size about the unit roundoff times $H$. If they behave like independent random errors, $\tilde H$ performs a random walk whose spread grows like the square root of the number of steps, a heuristic estimate.
- **The method must be symplectic and the step fixed.** Changing $h$ from step to step, or using a method that is only accurate, breaks the argument, and the energy then drifts as in the midpoint example. Thermostats and stochastic methods change the dynamics, and the theorem is not about them.
- **The error term cannot be removed.** The series for $\tilde H$ diverges in general, so no method other than an exact solver conserves a modified energy exactly, except in special cases such as linear systems.
- **The region.** The constants depend on the compact set $K$. A trajectory that leaves every compact set, or comes close to a singularity of $H$, such as two atoms that overlap, is not covered.

## History

Toxvaerd (1994) showed in a molecular dynamics setting that the discrete Verlet dynamics has a conserved Hamiltonian close to the true one. In the same year, Benettin and Giorgilli (1994) proved that a symplectic map close to the identity is the time-$h$ map of a Hamiltonian flow up to an exponentially small error, and applied this to symplectic integrators. Reich (1999) and Hairer, Lubich and Wanner developed backward error analysis for structure-preserving methods, and their book gives the long-time energy result as Theorem IX.8.1. Skeel and Hardy (2001) and Engle, Skeel and Drees (2005) gave practical ways to compute shadow Hamiltonians and to use them to measure drift in simulations.

## References
