---
tag: M1QQTQ
kind: algorithm
slug: hermite-n-body-integrator
name: Fourth-order Hermite integrator
aliases:
- Hermite predictor-corrector scheme
area: scientific-computing/n-body-and-particle-methods
level: advanced
summary: Predicts positions from the force and its time derivative, then corrects with a Hermite interpolant; the standard integrator of direct N-body codes.
model: real-ram
complexity:
  vars: {N: the number of bodies}
  time: {step: "Θ(N^2)"}
  space: {extra: "Θ(N)"}
properties: {deterministic: true, implicit: false, one_step: true, order: "4", symplectic: false, symmetric: false}
history:
  year: 1991
  people: [Junichiro Makino, Sverre J. Aarseth]
  note: Makino proposed the Hermite scheme with the directly computed force derivative in 1991, and Makino and Aarseth combined it with individual time steps and neighbor schemes in 1992.
prereqs: [direct-n-body-summation, hermite-interpolation, order-of-accuracy]
see_also: [block-time-steps, verlet-integration, wisdom-holman-integrator, kustaanheimo-stiefel-regularization, classical-runge-kutta-4, adaptive-step-size-control, cubic-hermite-spline, symplectic-integrators]
sources:
  - paper: doi:10.1086/169751
    title: "Junichiro Makino, Optimal order and time-step criterion for Aarseth-type N-body integrators, Astrophysical Journal 369, 1991, 200-212"
    locator: the Hermite scheme with the direct computation of the force derivative and the step criterion
  - paper: doi:10.1093/pasj/44.2.141
    title: "Junichiro Makino and Sverre J. Aarseth, On a Hermite integrator with Ahmad-Cohen scheme for gravitational many-body problems, Publications of the Astronomical Society of Japan 44(2), 1992, 141-151"
    locator: the fourth-order Hermite scheme with individual and neighbor time steps
  - book: isbn:9780521432726
    title: Sverre J. Aarseth, Gravitational N-Body Simulations, Tools and Algorithms, Cambridge University Press, 2003
    locator: Section 2.3 (individual time steps and the step criterion), Section 2.5 (Hermite scheme), Appendix H (Hermite integration method)
  - paper: doi:10.1016/j.newast.2006.06.003
    title: "Junichiro Makino, Piet Hut, Murat Kaplan and Hasan Saygin, A time-symmetric block time-step algorithm for N-body simulations, New Astronomy 12(2), 2006, 124-133"
    locator: the time-symmetric form of the Hermite scheme
---

The fourth-order Hermite integrator advances the bodies of an N-body system with the acceleration $\mathbf{a}$ and its time derivative, the jerk $\mathbf{j} = \dot{\mathbf{a}}$, both computed by [direct summation](/direct-n-body-summation/). A step first predicts the positions and velocities by a Taylor series to the jerk, then computes $\mathbf{a}$ and $\mathbf{j}$ at the predicted state, fits a cubic in time through the two values of $\mathbf{a}$ and $\mathbf{j}$ ([Hermite interpolation](/hermite-interpolation/)), and corrects the step with the integral of that cubic. It needs one force evaluation per step, like [leapfrog](/verlet-integration/), but it is fourth order, and it gives the higher derivatives that a step criterion needs. With individual [block time steps](/block-time-steps/) it is the standard integrator of direct codes for star clusters, such as the NBODY codes and GRAPE and GPU codes. It is not [symplectic](/symplectic-integrators/), so its energy error drifts slowly.

## In plain words

To move a body forward in time, you can use how fast it moves and how its speed changes. This method also uses how the pull on it changes from moment to moment. With these, it makes a first guess of where each body will be after a short time.

Then it works out the pulls again at the guessed places, and how fast they change there. Now it knows the pull and its rate of change at the start and at the end of the step. It draws the smoothest curve that fits all four of these, and uses that curve to correct the guess. One new set of pulls per step is enough, and halving the step makes the error about sixteen times smaller.

## The problem

The input is the state of $N$ bodies, masses $m_i$, positions $\mathbf{x}_i$ and velocities $\mathbf{v}_i$, with $G = 1$, a softening parameter $\epsilon \ge 0$ and a time step $h$. The output is an approximation of the state at time $t + h$ of the [gravitational N-body problem](/gravitational-n-body-problem/). The jerk of body $i$ follows from the pair force by the chain rule: with $\mathbf{r}_{ij} = \mathbf{x}_j - \mathbf{x}_i$, $\mathbf{v}_{ij} = \mathbf{v}_j - \mathbf{v}_i$ and $r^2 = |\mathbf{r}_{ij}|^2 + \epsilon^2$,

$$\mathbf{a}_i = G \sum_{j \ne i} m_j \frac{\mathbf{r}_{ij}}{r^3}, \qquad \mathbf{j}_i = G \sum_{j \ne i} m_j \left( \frac{\mathbf{v}_{ij}}{r^3} - \frac{3 (\mathbf{r}_{ij} \cdot \mathbf{v}_{ij})\, \mathbf{r}_{ij}}{r^5} \right).$$

## The algorithm

```pseudo id=main
HERMITE-STEP(x, v, a, j, h)                    ▷ for each body i
L1  x_p ← x + v h + a h²/2 + j h³/6
L2  v_p ← v + a h + j h²/2
L3  (a_1, j_1) ← FORCE-AND-JERK(x_p, v_p)
L4  a⁽²⁾ ← (-6 (a - a_1) - h (4 j + 2 j_1)) / h²
L5  a⁽³⁾ ← (12 (a - a_1) + 6 h (j + j_1)) / h³
L6  x_1 ← x_p + a⁽²⁾ h⁴/24 + a⁽³⁾ h⁵/120
L7  v_1 ← v_p + a⁽²⁾ h³/6 + a⁽³⁾ h⁴/24
L8  return x_1, v_1, a_1, j_1

FORCE-AND-JERK(x, v): for each pair i < j, add with opposite signs
L9      m r_ij / r³                                  to a
L10     m (v_ij / r³ - 3 (r_ij · v_ij) r_ij / r⁵)    to j
```

Lines L1 and L2 are the predictor. Line L3 is the only force evaluation, of cost $\Theta(N^2)$. Lines L4 and L5 compute the second and third derivatives of $\mathbf{a}$ at the start of the step from the cubic through $\mathbf{a}$, $\mathbf{j}$, $\mathbf{a}_1$ and $\mathbf{j}_1$, and lines L6 and L7 add the matching Taylor terms. In closed form, the corrector is

$$\mathbf{v}_1 = \mathbf{v} + \frac{h}{2}(\mathbf{a} + \mathbf{a}_1) + \frac{h^2}{12}(\mathbf{j} - \mathbf{j}_1), \qquad \mathbf{x}_1 = \mathbf{x} + \mathbf{v} h + \frac{h^2}{20}(7\mathbf{a} + 3\mathbf{a}_1) + \frac{h^3}{60}(3\mathbf{j} - 2\mathbf{j}_1).$$

The values $\mathbf{a}^{(2)} + h \mathbf{a}^{(3)}$ and $\mathbf{a}^{(3)}$ at the end of the step feed the step criterion of Aarseth (2003, Section 2.3),

$$h_{\text{new}} = \sqrt{\eta \, \frac{|\mathbf{a}| |\mathbf{a}^{(2)}| + |\mathbf{j}|^2}{|\mathbf{j}| |\mathbf{a}^{(3)}| + |\mathbf{a}^{(2)}|^2}},$$

a rule of thumb with $\eta$ of about $0.01$ to $0.02$.

## Example

Two bodies of mass $1/2$ at $(\mp 0.5, 0, 0)$ with velocities $(0, \mp 0.5, 0)$ move on a circle of radius $0.5$ with period $2\pi$. Take one step of $h = 0.1$ for body 2, which starts at $(0.5, 0)$ with $\mathbf{v} = (0, 0.5)$, $\mathbf{a} = (-0.5, 0)$ and $\mathbf{j} = (0, -0.5)$. The exact state at $t = 0.1$ is $0.5(\cos 0.1, \sin 0.1)$ and $0.5(-\sin 0.1, \cos 0.1)$.

| quantity | position | velocity | position error |
|---|---|---|---|
| predicted (L1, L2) | (0.497500000, 0.049916667) | (-0.050000000, 0.497500000) | $2.1 \times 10^{-6}$ |
| corrected (L6, L7) | (0.497502082, 0.049916708) | (-0.049916771, 0.497502078) | $3.9 \times 10^{-10}$ |
| exact | (0.497502083, 0.049916708) | (-0.049916708, 0.497502083) | |

The force at the predicted point is $\mathbf{a}_1 = (-0.497506, -0.049917)$, close to the exact $-0.5(\cos 0.1, \sin 0.1)$. The corrector reduces the position error by a factor of more than 5000. Over one period of an orbit with eccentricity $0.5$, the position error is $2.2 \times 10^{-6}$ with 400 steps and $1.3 \times 10^{-7}$ with 800 steps, a ratio of 16.8, close to the $2^4 = 16$ of a fourth-order method (measurement with this implementation).

## Correctness

The jerk formula is the time derivative of the pair force (Lemma 1 of the proof file). Lines L4 and L5 give the unique cubic $\mathbf{p}(t)$ that matches $\mathbf{a}$ and $\mathbf{j}$ at $t = 0$ and $\mathbf{a}_1$ and $\mathbf{j}_1$ at $t = h$ (Lemma 2), and lines L6 and L7 integrate it once and twice (Lemma 3). The cubic Hermite interpolant of a smooth function has the error $\frac{1}{24} \mathbf{a}^{(4)}(\xi)\, t^2 (t - h)^2$, whose integral over the step is $O(h^5)$. The predictor errors enter $\mathbf{a}_1$ at order $h^4$ and $\mathbf{j}_1$ at order $h^3$, and they are multiplied by $h$ and $h^2$ in the corrector. So the local error is $O(h^5)$, and the [global error](/global-error/) over a fixed time is $O(h^4)$ (theorem, for a smooth force).

## Complexity

In the [real RAM](/real-ram/) model, one step evaluates the force and the jerk once, with $N(N-1)/2$ pairs of about twice the cost of a pair of the force alone. So a step costs $\Theta(N^2)$, and the extra space is $\Theta(N)$ for the predicted state and the new $\mathbf{a}$ and $\mathbf{j}$. With [block time steps](/block-time-steps/), a step of the bodies of one block of $n$ bodies costs $\Theta(n N)$, plus $\Theta(N)$ for predicting all bodies.

## Properties

- **Fourth order, one force evaluation per step.** The classical [Runge-Kutta method](/classical-runge-kutta-4/) of order 4 needs four.
- **Self-starting.** Only the state and the force at one time are needed, unlike multistep schemes. This is what makes individual time steps simple.
- **Not symplectic and not time-symmetric.** For a fixed step the energy error drifts; for the orbit of eccentricity $0.5$ with 400 steps per orbit, the relative energy error $|E(t) - E(0)| / |E(0)|$ is $1.5 \times 10^{-7}$ after one orbit and $1.5 \times 10^{-6}$ after ten (measurement). The total momentum is conserved up to rounding.
- **Gives the step criterion for free.** The fitted $\mathbf{a}^{(2)}$ and $\mathbf{a}^{(3)}$ are the inputs of the Aarseth criterion.

## Variants and improvements

- **Iterated corrector.** Repeat lines L3 to L7 with the corrected state. With two or more iterations the scheme approaches the implicit time-symmetric Hermite scheme, whose energy error does not drift for periodic orbits (Makino, Hut, Kaplan and Saygin 2006).
- **Individual and block time steps.** Each body has its own step, a power of 2 fraction of a base step; at each time only the bodies of one block are corrected, and all others are only predicted ([block time steps](/block-time-steps/)).
- **Ahmad-Cohen neighbor scheme.** Split the force into the part of near neighbors, corrected with a small step, and the part of distant bodies, with a larger step (Makino and Aarseth 1992).
- **Higher orders.** Sixth- and eighth-order Hermite schemes also use the snap and the crackle of each pair.
- **Regularized pairs.** Close binaries are taken out and integrated with [Kustaanheimo-Stiefel regularization](/kustaanheimo-stiefel-regularization/), and the Hermite scheme moves their center of mass.

## When to use it

Use the Hermite scheme for collisional systems integrated with direct summation: star clusters, galactic nuclei and systems with up to about a million bodies on GPUs, where accuracy per force evaluation matters and steps differ widely between bodies. For collisionless systems with softening and a shared step, use [leapfrog](/verlet-integration/), which is symplectic and cheaper. For planetary systems with one dominant mass, use the [Wisdom-Holman map](/wisdom-holman-integrator/).

## Pitfalls

- **Recomputing the force after the corrector.** The force and the jerk at the corrected state differ from $\mathbf{a}_1$ and $\mathbf{j}_1$ at the predicted state by $O(h^4)$. The scheme keeps $\mathbf{a}_1$ and $\mathbf{j}_1$ for the next step; a second evaluation doubles the cost and is the iterated variant, not the basic scheme.
- **Jerk with the wrong sign.** The relative velocity must be $\mathbf{v}_j - \mathbf{v}_i$ when the relative position is $\mathbf{x}_j - \mathbf{x}_i$. Test the jerk against a finite difference of the acceleration.
- **A step that grows too fast.** A step chosen only from the criterion can double many times in one step at the start; limit the growth, or start with a criterion that uses $\mathbf{a}$ and $\mathbf{j}$ only.
- **Expecting bounded energy errors.** The scheme is not symplectic. For long integrations at a fixed step, the drift grows linearly; use the time-symmetric variant or a symplectic method if that matters.
- **Close encounters.** The step goes to zero as two bodies approach with $\epsilon = 0$. Regularize the pair.

## Implementations

## History

Earlier direct codes of Aarseth used a fourth-order scheme that fitted a polynomial through the forces at four past times, with divided differences. Makino (1991) proposed computing the jerk directly by summation and fitting the cubic with the values at only two times, which gives a self-starting scheme with larger steps for the same accuracy, and a new step criterion. Makino and Aarseth (1992) combined it with individual steps and the Ahmad-Cohen neighbor scheme. The scheme became the standard of the NBODY codes and of the GRAPE special-purpose computers.

## References
