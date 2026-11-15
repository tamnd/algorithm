---
tag: 1BE9AC
kind: definition
slug: limit-cycle
name: Limit cycle
aliases:
- isolated periodic orbit
area: control/stability
level: core
summary: A periodic orbit of an autonomous system with no other periodic orbit near it. Nearby solutions spiral toward it or away from it, as in the van der Pol oscillator.
prereqs: [equilibrium-point]
see_also: [poincare-bendixson-theorem, describing-function, relay-autotuning, lasalle-invariance-principle, region-of-attraction, lure-problem, phase-noise-analysis, iir-filter]
sources:
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 2.4, Limit Cycles; Section 2.6, Existence of Periodic Orbits; Section 8.4, Stability of Periodic Solutions
  - paper: doi:10.1080/14786442608564127
    title: "B. van der Pol, On relaxation-oscillations, The London, Edinburgh and Dublin Philosophical Magazine and Journal of Science, Series 7, 2(11), 978-992, 1926"
    locator: the equation of the triode oscillator and its periodic solution, for small and for large damping
  - paper: "H. Poincaré, Mémoire sur les courbes définies par une équation différentielle, Journal de Mathématiques Pures et Appliquées, Series 3, volumes 7 and 8 (1881, 1882), and Series 4, volumes 1 and 2 (1885, 1886)"
    locator: the closed trajectories of planar vector fields and the limit cycles (cycles limites)
---

A limit cycle is a closed path in the state space of a system that evolves by a differential equation. A state on the path goes around it again and again with a fixed period, and no other closed path lies near it. Solutions that start near the path spiral toward it, or away from it, as time goes on. Limit cycles are the mathematical form of a self-sustained oscillation: the triode oscillator of van der Pol, an electronic oscillator, a relay feedback loop, a squealing brake, a heartbeat model. The amplitude of a stable limit cycle is set by the system, not by the initial state. This is the difference from a frictionless pendulum or an LC circuit, where every amplitude is possible. A linear system cannot have a limit cycle, so a limit cycle is always a nonlinear effect.

## Definition

**Setting.** $\dot x = f(x)$, with $f : D \to \mathbb{R}^n$ locally Lipschitz on an open set $D \subseteq \mathbb{R}^n$. A solution $x(t)$ is *periodic* with period $T > 0$ if $x(t + T) = x(t)$ for all $t$ and $x$ is not an [equilibrium](/equilibrium-point/). The smallest such $T$ is the period. The set $\gamma = \{x(t) : 0 \le t < T\}$ is a closed curve, the *periodic orbit*.

**Definition.** A periodic orbit $\gamma$ is a *limit cycle* if it is isolated: some neighborhood of $\gamma$ contains no other periodic orbit (Khalil 2002, Section 2.4).

**Stability of a limit cycle.** Let $\operatorname{dist}(x, \gamma)$ be the distance from $x$ to the set $\gamma$. The orbit $\gamma$ is *orbitally stable* if for each $\varepsilon > 0$ there is $\delta > 0$ such that $\operatorname{dist}(x(0), \gamma) < \delta$ implies $\operatorname{dist}(x(t), \gamma) < \varepsilon$ for all $t \ge 0$. It is *asymptotically orbitally stable* if, in addition, $\operatorname{dist}(x(t), \gamma) \to 0$ for all $x(0)$ near $\gamma$ (Khalil 2002, Section 8.4). The distance is to the set, not to one point of it: a solution near $\gamma$ can approach the orbit with a phase shift. Three cases are common:

- a *stable* limit cycle is asymptotically orbitally stable;
- an *unstable* limit cycle is stable in reverse time: nearby solutions move away from it;
- in the plane, a *semistable* limit cycle attracts the solutions on one side and repels the solutions on the other side.

**Floquet multipliers.** Let $f$ be continuously differentiable and let $x^*(t)$ be a periodic solution of period $T$ on $\gamma$. The linearization along it is $\dot \xi = A(t) \xi$ with $A(t) = \partial f / \partial x\,(x^*(t))$, a $T$-periodic matrix. Let $\Phi(t)$ be its state transition matrix with $\Phi(0) = I$. The matrix $\Phi(T)$ is the *monodromy matrix*. It has the eigenvalue $1$ with eigenvector $f(x^*(0))$, because $\dot x^*$ solves the linearized equation. The other $n - 1$ eigenvalues are the *Floquet multipliers* of $\gamma$. They are also the eigenvalues of the derivative of the Poincaré map: on a hypersurface $S$ that crosses $\gamma$ transversally at $p$, the Poincaré map sends a point of $S$ near $p$ to the next point where its solution meets $S$, and $p$ is a fixed point.

- If all $n - 1$ multipliers have modulus less than $1$, $\gamma$ is asymptotically orbitally stable, and the convergence is exponential.
- If one multiplier has modulus greater than $1$, $\gamma$ is not orbitally stable.
- If no multiplier is on the unit circle, $\gamma$ is *hyperbolic*. A hyperbolic periodic orbit is always isolated, so it is a limit cycle, and it persists under small $C^1$ changes of $f$.

In the plane there is one multiplier, and Liouville's formula $\det \Phi(T) = \exp \int_0^T \operatorname{tr} A(t)\, dt$ gives it directly:

$$\mu_1 = \exp\left(\int_0^T \operatorname{div} f(x^*(t))\, dt\right) .$$

A negative integral of the divergence along the orbit means a stable limit cycle.

**A second definition in the plane.** Some books call a periodic orbit a limit cycle if it is the omega-limit set or the alpha-limit set of a point that is not on it. For an analytic planar vector field the two definitions agree. The Poincaré map $P$ of an analytic field is analytic, so the zeros of $P(s) - s$ either are isolated or fill an interval. In the first case the orbit is isolated, and nearby solutions spiral onto it in forward or reverse time. In the second case all nearby orbits are periodic, and no solution can approach $\gamma$.

## Examples and non-examples

- **A stable limit cycle in closed form.** In polar coordinates, $\dot r = r (1 - r^2)$, $\dot \theta = 1$; in Cartesian coordinates $\dot x_1 = x_1 - x_2 - x_1 (x_1^2 + x_2^2)$, $\dot x_2 = x_1 + x_2 - x_2 (x_1^2 + x_2^2)$. The unit circle is a periodic orbit of period $2\pi$. For $r(0) = r_0 > 0$, $r(t) = r_0 / \sqrt{r_0^2 + (1 - r_0^2) e^{-2t}} \to 1$, so every solution other than the origin approaches the circle. Here $\operatorname{div} f = 2 - 4 (x_1^2 + x_2^2)$, which is $-2$ on the circle, so the Floquet multiplier is $e^{-4\pi} \approx 3.4873 \cdot 10^{-6}$. The [invariance principle](/lasalle-invariance-principle/) gives the same convergence with $V = (1 - |x|^2)^2$.
- **An unstable limit cycle.** With $\dot r = -r (1 - r^2)$, $\dot \theta = 1$, the unit circle repels. The origin is asymptotically stable, and its [region of attraction](/region-of-attraction/) is the open unit disc. An unstable limit cycle often bounds a region of attraction in the plane.
- **A semistable limit cycle.** With $\dot r = r (1 - r)^2$, $\dot \theta = 1$, $\dot r > 0$ on both sides of $r = 1$. Solutions inside approach the circle, and solutions outside move away from it. The multiplier is exactly $1$, so the cycle is not hyperbolic. A small change of the equation can split it into two limit cycles or remove it.
- **The van der Pol oscillator.** $\ddot x - \mu (1 - x^2) \dot x + x = 0$ with $\mu > 0$, or $\dot x_1 = x_2$, $\dot x_2 = -x_1 + \mu (1 - x_1^2) x_2$. The damping is negative for $|x| < 1$ and positive for $|x| > 1$, so small oscillations grow and large ones decay. By Liénard's theorem there is exactly one periodic orbit, and it is a stable limit cycle that attracts every solution other than the origin. A simulation with the classical Runge-Kutta method and step $0.0005$ gives these values:

  | $\mu$ | period | peak of $x$ | $\int_0^T \operatorname{div} f\, dt$ |
  |---|---|---|---|
  | 0.1 | 6.28711 | 2.0001 | -0.629 |
  | 1 | 6.66329 | 2.0086 | -7.06 |
  | 5 | 11.61223 | 2.0215 | -85.5 |

  For small $\mu$ the orbit is close to the circle of radius $2$ with period $2\pi$, and the divergence integral is close to $-2\pi\mu$. For large $\mu$ the oscillation becomes a relaxation oscillation, with slow phases and fast jumps, and the period grows like $(3 - 2 \ln 2)\mu$.
- **A limit cycle that is born from an equilibrium.** $\dot r = r (\beta - r^2)$, $\dot \theta = 1$. For $\beta \le 0$ the origin is asymptotically stable and there is no periodic orbit. For $\beta > 0$ the origin is unstable and the circle $r = \sqrt{\beta}$ is a stable limit cycle with multiplier $e^{-4\pi\beta}$. This is a supercritical Hopf bifurcation: the amplitude grows like $\sqrt{\beta}$ from zero.
- **Not a limit cycle: a center.** For the harmonic oscillator $\ddot x + x = 0$, every solution other than the origin is periodic. No periodic orbit is isolated, so none is a limit cycle. The same holds for the closed orbits of a frictionless pendulum and of the Lotka-Volterra equations. The amplitude depends on the initial state, and any small change of the model can destroy the family.
- **Not possible: linear systems.** If $\dot x = A x$ has a periodic solution $x(t)$, then $c\, x(t)$ is a periodic solution for every $c > 0$, so no periodic orbit is isolated.
- **Not possible: gradient systems.** For $\dot x = -\nabla V(x)$, $V$ decreases strictly along every solution that is not an equilibrium, so there is no periodic orbit at all. In the plane the Bendixson and Dulac criteria on the [Poincaré-Bendixson theorem](/poincare-bendixson-theorem/) page rule out periodic orbits in other cases.
- **A relay loop.** A linear plant in feedback with a relay often oscillates in a stable limit cycle. [Relay autotuning](/relay-autotuning/) uses this oscillation to measure the critical gain and period of a process. The [describing function](/describing-function/) method predicts the amplitude and frequency of such cycles. It is an approximation: it assumes that the linear part removes the harmonics, and it can predict a limit cycle that does not exist or miss one that does. The [Lur'e problem](/lure-problem/) asks for conditions that exclude all such oscillations.

## Related definitions

- *Omega-limit set*: the set of points that a solution approaches along a sequence of times that goes to infinity. In the plane the [Poincaré-Bendixson theorem](/poincare-bendixson-theorem/) says when it is a periodic orbit. In dimension 3 and more, bounded solutions can have chaotic limit sets, such as the Lorenz attractor.
- *Orbital stability* and *asymptotic phase*: a solution that approaches a stable hyperbolic limit cycle approaches one particular periodic solution on it, with a fixed time shift. This is why the multipliers measure the stability of the orbit and the phase is free.
- *Hilbert's 16th problem* (second part): find a bound on the number of limit cycles of a planar polynomial vector field in terms of its degree. It is open, even for degree $2$.
- *Limit cycles in digital filters*: a fixed-point [IIR filter](/iir-filter/) can produce a periodic output with zero input because of rounding. These are periodic orbits of a discrete-time quantized map, not of a smooth differential equation, but they have the same name.
- *Oscillators in circuits*: an electronic oscillator is designed to have a stable limit cycle, and the noise of its phase along the cycle is the subject of [phase noise analysis](/phase-noise-analysis/).

## References
