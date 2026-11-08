---
tag: GS38D8
kind: concept
slug: symplectic-integrators
name: Symplectic integrators
aliases:
- geometric integrators
- symplectic methods
- canonical integrators
area: numerical/differential-equations
level: advanced
summary: "One-step methods for Hamiltonian systems whose step map is symplectic, like the exact flow. They have no energy drift over long times; Verlet, symplectic Euler and Gauss methods are examples."
prereqs: [hamiltonian-systems, verlet-integration]
see_also: [symplectic-euler-method, gauss-legendre-runge-kutta, implicit-runge-kutta-methods, butcher-tableau, operator-splitting, global-error, stability-region, runge-kutta-methods]
sources:
  - book: isbn:9783540306634
    title: Ernst Hairer, Christian Lubich and Gerhard Wanner, Geometric Numerical Integration, second edition, Springer, 2006
    locator: Chapter VI (symplectic integration; Theorem VI.4.3 for symplectic Runge-Kutta methods, generating functions), Chapter IX (backward error analysis, Theorem IX.8.1 on long-time energy conservation), Chapter X (linear error growth for integrable systems)
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.16 (symplectic integration methods)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 5 (geometric numerical integration)
  - paper: "J. M. Sanz-Serna, Runge-Kutta schemes for Hamiltonian systems, BIT 28 (1988) 877-883"
    locator: the condition b_i a_ij + b_j a_ji = b_i b_j for symplectic Runge-Kutta methods; doi:10.1007/BF01954907
---

A symplectic integrator is a one-step method for a [Hamiltonian system](/hamiltonian-systems/) $y' = J^{-1}\nabla H(y)$, $y = (q, p) \in \mathbb{R}^{2k}$, whose step map $\Phi_h$ is symplectic for every Hamiltonian $H$ and every small $h$, as the exact flow is. In the page notation this is $y' = f(y)$ with $f = J^{-1}\nabla H$. Symplecticity does not make the method more accurate per step, but it changes the long-time behaviour completely: the numerical solution is, up to exponentially small terms, the exact solution of a nearby Hamiltonian system, so energy errors stay bounded over very long times instead of drifting. [Verlet](/verlet-integration/), [symplectic Euler](/symplectic-euler-method/) and the [Gauss-Legendre Runge-Kutta methods](/gauss-legendre-runge-kutta/) are the standard examples.

## In plain words

The motion of planets, molecules and pendulums obeys a hidden geometric rule: if you follow a small patch of possible starting states, the patch moves and bends but keeps its area. Most numerical methods break this rule a little in every step, and the small errors add up in one direction: orbits slowly spiral in or out and the energy creeps.

A symplectic method keeps the area rule exactly at every step. It still makes errors, but they behave like the motion of a slightly different, equally well-behaved physical system. The energy then wobbles around a fixed value instead of creeping, which is why such methods are used for simulations that run for millions of steps.

## The idea

**Symplectic maps.** Let $J = \begin{pmatrix} 0 & I \\ -I & 0 \end{pmatrix}$. A differentiable map $\Phi : \mathbb{R}^{2k} \to \mathbb{R}^{2k}$ is symplectic if its Jacobian satisfies $\Phi'(y)^T J \Phi'(y) = J$ for all $y$. For $k = 1$ this means $\det \Phi' = 1$: area is preserved. Poincaré's theorem says that the exact flow $\varphi_t$ of a Hamiltonian system is symplectic (HLW, Theorem VI.2.4). A numerical method is symplectic if $\Phi_h$ is symplectic whenever it is applied to a Hamiltonian system.

**Which methods are symplectic.**
- *Splitting.* If $H = H_1 + H_2$ and the flows of $H_1$ and $H_2$ can be computed exactly, any composition of them is symplectic, because compositions of symplectic maps are. Symplectic Euler and Störmer-Verlet are the compositions of the kick (flow of $V(q)$) and the drift (flow of $T(p)$).
- *Runge-Kutta methods.* A Runge-Kutta method with tableau $(A, b, c)$ is symplectic if
$$b_i a_{ij} + b_j a_{ji} = b_i b_j \quad \text{for all } i, j = 1, \ldots, s$$
(Sanz-Serna, Lasagni and Suris, 1988; HLW, Theorem VI.4.3). The same condition makes the method conserve all quadratic first integrals.
- *No explicit Runge-Kutta method is symplectic.* With $i = j$ the condition gives $2b_i a_{ii} = b_i^2$. An explicit method has $a_{ii} = 0$, so every $b_i = 0$, which contradicts consistency $\sum_i b_i = 1$.
- *Gauss methods are symplectic.* The $s$-stage Gauss-Legendre collocation method satisfies the condition, for example the implicit midpoint rule ($s = 1$, $a_{11} = \frac12$, $b_1 = 1$): $\frac12 + \frac12 = 1$.

**Linear test.** On the harmonic oscillator $H = (p^2 + q^2)/2$, a Runge-Kutta method gives the step matrix with eigenvalues $R(\pm ih)$, and $\det \Phi_h' = |R(ih)|^2$. So it is symplectic on this problem exactly when $|R(iy)| = 1$, the stability function being unimodular on the imaginary axis. For classical RK4, $|R(iy)|^2 = 1 - y^6/72 + y^8/576 < 1$ for $0 < y < 2\sqrt2$: every step shrinks area and energy.

**Why there is no drift (backward error analysis).** For analytic $H$, a symplectic method of order $p$ is the exact time-$h$ flow of a modified Hamiltonian $\tilde H = H + h^p H_{p+1} + h^{p+1} H_{p+2} + \cdots$, truncated optimally, up to an error $O(h e^{-c/h})$. Hence $\tilde H$ is conserved up to exponentially small errors over exponentially long times, and
$$|H(y_n) - H(y_0)| = O(h^p) \qquad \text{for } nh \le e^{c/(2h)}$$
(HLW, Theorem IX.8.1; an asymptotic result for analytic $H$ and fixed step size). For integrable systems the global error in the angles grows only linearly in time, against quadratically for general methods (HLW, Chapter X).

## Examples

*Kepler problem at equal cost.* With eccentricity $0.5$ and 400 force evaluations per orbit (RK4 with $h = 2\pi/100$, Verlet with $h = 2\pi/400$), the energy errors after 1, 10, 100 and 1000 orbits are (observed):

| orbits | 1 | 10 | 100 | 1000 |
|---|---|---|---|---|
| RK4 | $-1.5 \times 10^{-5}$ | $-1.5 \times 10^{-4}$ | $-1.5 \times 10^{-3}$ | $-1.5 \times 10^{-2}$ |
| Verlet | $1.8 \times 10^{-7}$ | $1.8 \times 10^{-5}$ | $3.3 \times 10^{-4}$ | $1.2 \times 10^{-4}$ |

RK4 is far more accurate per step but drifts linearly in time; the order-2 Verlet method oscillates without drift. Both lose the phase of the orbit over hundreds of orbits.

*Harmonic oscillator.* Symplectic Euler conserves $q^2 + p^2 - hqp$ exactly and Verlet conserves $p^2 + (1 - h^2/4)q^2$ exactly; these are their modified Hamiltonians, and the iterates stay on fixed ellipses for $h < 2$. Explicit Euler multiplies $q^2 + p^2$ by $1 + h^2$ per step.

*Pendulum.* With $h = 0.1$ over $t \in [0, 100]$, symplectic Euler keeps the energy error below $0.051$, while explicit Euler gains $5.07$ in energy and turns a swinging pendulum into a rotating one.

*Non-examples.* Explicit Runge-Kutta methods, linear multistep methods (which are not one-step maps on the phase space), adaptive step-size versions of symplectic methods, and projection onto the energy surface (which conserves energy but not the symplectic structure).

## Where it is used

- **Celestial mechanics:** long-term stability of the solar system, with splitting methods such as Wisdom-Holman that split Keplerian motion from planetary interactions.
- **Molecular dynamics:** Verlet and its constrained versions (SHAKE, RATTLE) over $10^6$ to $10^9$ steps.
- **Accelerator physics and plasma physics:** particle tracking over many turns, the context in which Ruth introduced symplectic methods.
- **Hamiltonian Monte Carlo:** the leapfrog proposal must be volume-preserving and reversible for the acceptance rule to be correct.
- **Wave equations and other Hamiltonian PDEs** after spatial discretization, with leapfrog in time.

## References
