---
tag: QC6JDQ
kind: concept
slug: hamiltonian-dynamics
name: Hamiltonian dynamics
aliases:
- Hamiltonian flow
- leapfrog integration
area: randomized/markov-chain-monte-carlo
level: advanced
summary: The flow dq/dt = ∂H/∂p, dp/dt = −∂H/∂q with H = −log π(q) + |p|²/2. It keeps H and volume and is reversible. Leapfrog keeps the last two exactly, so it can drive HMC.
prereqs: [hamiltonian-systems, verlet-integration]
see_also: [hamiltonian-monte-carlo, no-u-turn-sampler, symplectic-integrators, symplectic-euler-method, metropolis-adjusted-langevin-algorithm, detailed-balance]
sources:
  - book: isbn:9781420079418
    title: Steve Brooks, Andrew Gelman, Galin L. Jones and Xiao-Li Meng (editors), Handbook of Markov Chain Monte Carlo, Chapman and Hall/CRC, 2011
    locator: Chapter 5, Radford M. Neal, MCMC using Hamiltonian dynamics, pages 113 to 162 (the three properties of the flow, and the leapfrog method)
  - book: isbn:9783540306634
    title: Ernst Hairer, Christian Lubich and Gerhard Wanner, Geometric Numerical Integration, second edition, Springer, 2006
    locator: the chapters on symplectic integration, symmetric methods and backward error analysis (the modified Hamiltonian and long-time energy behaviour)
  - book: isbn:9780521772907
    title: Benedict Leimkuhler and Sebastian Reich, Simulating Hamiltonian Dynamics, Cambridge University Press, 2004
    locator: the chapters on symplectic and reversible integrators (the Störmer-Verlet method)
  - paper: doi:10.1103/PhysRev.159.98
    title: Loup Verlet, Computer experiments on classical fluids. I. Thermodynamical properties of Lennard-Jones molecules, Physical Review 159(1), 1967
    locator: pages 98 to 103 (the Verlet integration scheme for molecular dynamics)
---

Hamiltonian dynamics is the system of differential equations

$$\frac{dq}{dt} = \frac{\partial H}{\partial p} = M^{-1}p, \qquad \frac{dp}{dt} = -\frac{\partial H}{\partial q} = -\nabla U(q), \qquad H(q, p) = U(q) + \tfrac12 p^\top M^{-1}p,$$

on the pairs of a position $q \in \mathbb{R}^d$ and a momentum $p \in \mathbb{R}^d$. In MCMC the potential energy is $U(q) = -\log\tilde\pi(q)$ for the unnormalized target $\tilde\pi$, and $M$ is a positive definite "mass matrix" that the user chooses. The exact flow $\Phi_t$ has three properties: it keeps $H$ constant, it keeps volume in $(q, p)$ space, and it is reversible when the momentum is flipped. So it moves far through the state space while it keeps the joint density $e^{-H}$. The flow cannot be computed exactly, but the leapfrog method keeps volume and reversibility exactly and keeps $H$ to within $O(\varepsilon^2)$. That is the combination that [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/) needs.

## In plain words

Think of the target density as a landscape, where likely places are valleys. Put a ball at your current point and give it a random push. The ball rolls: it speeds up going downhill and slows going uphill, and its total energy stays the same.

After some time the ball is far from where it started, but it is still at a place that is about as likely as before. This is much better than a random step, which goes in a random direction. The computer cannot follow the ball exactly, so it moves it in small steps. One particular step rule, called leapfrog, keeps the properties that matter for sampling, and makes only a small error in the energy.

## The idea

Write $z = (q, p)$, $J = \begin{pmatrix}0 & I\\ -I & 0\end{pmatrix}$, so the equations are $\dot z = J\nabla H(z)$. Let $\Phi_t$ be the solution map for time $t$ and $F(q, p) = (q, -p)$ the momentum flip. In what follows $U$ is twice continuously differentiable, so solutions exist and are unique locally.

**Energy is conserved.** Along a solution,

$$\frac{d}{dt}H(q, p) = \nabla_q H \cdot \dot q + \nabla_p H \cdot \dot p = \nabla_q H \cdot \nabla_p H - \nabla_p H \cdot \nabla_q H = 0.$$

So $H(\Phi_t(z)) = H(z)$, and the density $e^{-H}$ has the same value at the start and at the end.

**Volume is preserved (Liouville).** The vector field $J\nabla H$ has divergence $\sum_i \partial^2H/\partial q_i\partial p_i - \sum_i \partial^2H/\partial p_i\partial q_i = 0$. A flow of a divergence-free field has Jacobian determinant 1: if $D(t) = \det D\Phi_t$, then $\dot D(t) = \operatorname{div}(J\nabla H)(\Phi_t)\,D(t) = 0$ and $D(0) = 1$. The flow is also symplectic, $D\Phi_t^\top J\,D\Phi_t = J$, which is stronger than volume preservation when $d \ge 2$.

**The flow is reversible.** Because $H(q, -p) = H(q, p)$, if $(q(t), p(t))$ is a solution, so is $(q(-t), -p(-t))$. In maps, $F \circ \Phi_t \circ F = \Phi_t^{-1}$, so $F \circ \Phi_t$ is an involution: applying it twice returns the start.

These three facts give a $\pi$-invariant move. The map $G = F \circ \Phi_t$ is a bijection with Jacobian $\pm 1$ and $G = G^{-1}$, and it keeps $e^{-H}$. So if $(q, p)$ has density proportional to $e^{-H(q, p)} = \tilde\pi(q)\,e^{-p^\top M^{-1}p/2}$, then so does $G(q, p)$, and the $q$-marginal is $\pi$. The [HMC](/hamiltonian-monte-carlo/) page turns this into a Markov chain.

**The leapfrog method.** One step of size $\varepsilon$ is

$$p_{1/2} = p - \tfrac{\varepsilon}{2}\nabla U(q), \qquad q' = q + \varepsilon M^{-1}p_{1/2}, \qquad p' = p_{1/2} - \tfrac{\varepsilon}{2}\nabla U(q').$$

It is the [Störmer-Verlet method](/verlet-integration/), written for positions and momenta. Let $\Psi_\varepsilon$ be this map.

- *Volume.* Each of the three substeps is a shear: it changes $p$ by a function of $q$ only, or $q$ by a function of $p$ only. A shear has a block triangular Jacobian with identity blocks on the diagonal, so its determinant is 1, and so is the determinant of the composition. Each shear is also symplectic, so $\Psi_\varepsilon$ is symplectic.
- *Reversibility.* Start at $F(q', p') = (q', -p')$ and take a leapfrog step. The first half step gives $-p' + \frac\varepsilon2\nabla U(q') = -p_{1/2}$. The full position step gives $q' - \varepsilon M^{-1}p_{1/2} = q$. The last half step gives $-p_{1/2} + \frac\varepsilon2\nabla U(q) = -p$. So $\Psi_\varepsilon(F(\Psi_\varepsilon(z))) = F(z)$, which is $F \circ \Psi_\varepsilon \circ F = \Psi_\varepsilon^{-1}$, the same identity as for the exact flow. By induction it holds for $L$ steps, $\Psi_\varepsilon^L$.
- *Energy.* The method is not exact, so $H$ changes. The local error is $O(\varepsilon^3)$, and for a fixed time $L\varepsilon$ the global error in $(q, p)$ and in $H$ is $O(\varepsilon^2)$. Backward error analysis gives more: for analytic $H$, leapfrog conserves a modified energy $\tilde H_\varepsilon = H + O(\varepsilon^2)$ up to an exponentially small error over exponentially long times (Hairer, Lubich and Wanner). So the energy error stays $O(\varepsilon^2)$ and does not drift.

Volume preservation and reversibility are what make the Metropolis correction of HMC simple: the acceptance probability is just $\min(1, e^{-H(z') + H(z)})$, with no Jacobian. The energy error only decides how often proposals are rejected.

**Why not Euler's method.** The explicit Euler step $q' = q + \varepsilon M^{-1}p$, $p' = p - \varepsilon\nabla U(q)$ is neither volume preserving nor reversible. The symplectic Euler method, which updates $p$ and then uses the new $p$ to update $q$, keeps volume but is not reversible. Leapfrog is the symmetric composition of the two halves, and the symmetry gives reversibility.

## Examples

**The harmonic oscillator.** Take $d = 1$, $M = 1$ and $U(q) = q^2/2$, so the target is $\mathcal{N}(0, 1)$ and the exact flow is a rotation: $q(t) = q_0\cos t + p_0\sin t$. One leapfrog step is the linear map

$$\begin{pmatrix}q'\\ p'\end{pmatrix} = \begin{pmatrix}1 - \varepsilon^2/2 & \varepsilon\\ -\varepsilon(1 - \varepsilon^2/4) & 1 - \varepsilon^2/2\end{pmatrix}\begin{pmatrix}q\\ p\end{pmatrix}.$$

Its determinant is $(1 - \varepsilon^2/2)^2 + \varepsilon^2(1 - \varepsilon^2/4) = 1$, and its trace is $2 - \varepsilon^2$, so the method is stable exactly when $\varepsilon < 2$. For $\varepsilon \ge 2$ the energy grows without bound from almost every start. A direct check shows that the step keeps

$$\tilde H_\varepsilon(q, p) = \frac{p^2}{2} + \Big(1 - \frac{\varepsilon^2}{4}\Big)\frac{q^2}{2}$$

exactly. So the points stay on an ellipse close to the circle $H = $ constant.

With $\varepsilon = 1/2$ from $(q, p) = (1, 0)$: $p_{1/2} = -1/4$, $q' = 1 - 1/8 = 7/8$, and $p' = -1/4 - 7/32 = -15/32$. Then $H = 1009/2048 = 0.4927$, compared with $H = 1/2$ at the start, and $\tilde H_\varepsilon = 15/32$ at both points. Along the whole orbit from $(1, 0)$, $H = \tilde H_\varepsilon + \varepsilon^2q^2/8$ moves between its two extremes, and the largest error $|H - 1/2|$ is exactly $\varepsilon^2/8$:

| step size $\varepsilon$ | largest leapfrog energy error in time 20 | $\varepsilon^2/8$ | explicit Euler, $H$ at time 20 (exact value 0.5) |
|---|---|---|---|
| 0.5 | 0.03125 | 0.03125 | 3762 |
| 0.25 | 0.00781 | 0.00781 | 63.9 |
| 0.125 | 0.00195 | 0.00195 | 5.98 |

Halving $\varepsilon$ divides the leapfrog error by 4, as $O(\varepsilon^2)$ says, and the error does not grow with time. Euler multiplies $H$ by $1 + \varepsilon^2$ at every step, so $H$ grows like $(1 + \varepsilon^2)^{20/\varepsilon}$.

**A quartic potential.** For $U(q) = q^4/4$ from $(1, 0)$, the largest energy error in time 20 is $0.00335$, $0.000834$ and $0.000208$ for $\varepsilon = 0.2$, $0.1$ and $0.05$: again a factor of 4 for each halving. Taking 10 leapfrog steps with $\varepsilon = 0.3$ from $(1, 0.3)$, flipping $p$, taking 10 more steps and flipping again returns $(1, 0.3)$ up to rounding.

## Where it is used

- **[Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/).** Draw a fresh Gaussian momentum, run $L$ leapfrog steps, flip the momentum, and accept with probability $\min(1, e^{-\Delta H})$.
- **[The No-U-Turn sampler](/no-u-turn-sampler/).** Builds the leapfrog trajectory forward and backward in time and stops when it starts to turn back.
- **[Langevin methods](/metropolis-adjusted-langevin-algorithm/).** HMC with one leapfrog step is the same as MALA with step size $\varepsilon^2$.
- **Molecular dynamics.** Verlet (1967) used the same scheme to simulate fluids, and the [symplectic integrators](/symplectic-integrators/) of numerical analysis grew from it.

## References
