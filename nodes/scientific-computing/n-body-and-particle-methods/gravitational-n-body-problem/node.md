---
tag: HBN91K
kind: problem
slug: gravitational-n-body-problem
name: Gravitational N-body problem
aliases:
- N-body simulation
area: scientific-computing/n-body-and-particle-methods
level: intro
summary: Given the masses, positions and velocities of N bodies that attract by gravity, compute their positions and velocities at later times.
prereqs: [ode-initial-value-problem, hamiltonian-systems]
see_also: [direct-n-body-summation, barnes-hut-algorithm, fast-multipole-method, particle-mesh-method, hermite-n-body-integrator, wisdom-holman-integrator, vlasov-poisson-system, molecular-dynamics]
sources:
  - book: isbn:9780521432726
    title: Sverre J. Aarseth, Gravitational N-Body Simulations, Tools and Algorithms, Cambridge University Press, 2003
    locator: Section 1.2 (historical developments), Section 1.3 (basic concepts)
  - book: isbn:9780691130279
    title: James Binney and Scott Tremaine, Galactic Dynamics, 2nd edition, Princeton University Press, 2008
    locator: Chapter 1 (relaxation time), Chapter 4 (collisionless systems)
  - paper: "Florin Diacu, The solution of the n-body problem, The Mathematical Intelligencer 18, 1996, 66-70"
    locator: the convergent series of Sundman and Wang
---

The gravitational N-body problem asks for the motion of $N$ point masses that attract each other by Newton's law of gravity. It is an [initial value problem](/ode-initial-value-problem/) for $6N$ ordinary differential equations. For $N = 2$ it reduces to the Kepler problem, which has a closed-form solution. For $N \ge 3$ the motion is in general chaotic, and the problem is solved by numerical integration. A solver has two parts: a force method, which computes the accelerations at one instant (for example [direct summation](/direct-n-body-summation/) or a [tree code](/barnes-hut-algorithm/)), and a time integrator, which moves the bodies (for example [leapfrog](/verlet-integration/), the [Hermite scheme](/hermite-n-body-integrator/) or the [Wisdom-Holman map](/wisdom-holman-integrator/)). The problem is the model of star clusters, galaxies, planetary systems and the dark matter of the universe.

## In plain words

You have a number of stars or planets. You know how heavy each one is, where it is and how fast it moves. Each one pulls on every other one, more strongly when they are close. The task is to find where all of them will be later.

With two bodies the answer is a known curve, such as an ellipse. With three or more bodies there is no simple answer, and very small changes at the start lead to large changes later. So computers find the answer step by step: compute all the pulls, move each body a little, and repeat. The two hard parts are to compute the pulls fast when there are many bodies, and to take steps that stay accurate when two bodies come very close.

## Definition

The input is $N$ masses $m_i > 0$, initial positions $\mathbf{x}_i(0) \in \mathbb{R}^3$, initial velocities $\mathbf{v}_i(0)$ and an end time $T$. The gravitational constant is $G$; most codes use units with $G = 1$. The output is $\mathbf{x}_i(t)$ and $\mathbf{v}_i(t)$ for $0 \le t \le T$, the solution of

$$\dot{\mathbf{x}}_i = \mathbf{v}_i, \qquad \dot{\mathbf{v}}_i = G \sum_{j \ne i} m_j \frac{\mathbf{x}_j - \mathbf{x}_i}{|\mathbf{x}_j - \mathbf{x}_i|^3}, \qquad i = 1, \ldots, N.$$

The system is [Hamiltonian](/hamiltonian-systems/), with momenta $\mathbf{p}_i = m_i \mathbf{v}_i$ and

$$H = \sum_i \frac{|\mathbf{p}_i|^2}{2 m_i} - G \sum_{i < j} \frac{m_i m_j}{|\mathbf{x}_i - \mathbf{x}_j|}.$$

The energy $E = H$, the total momentum $\mathbf{P} = \sum_i \mathbf{p}_i$ and the angular momentum $\mathbf{L} = \sum_i \mathbf{x}_i \times \mathbf{p}_i$ are constant, and the center of mass moves on a straight line at constant speed (theorem). A numerical solution is judged by the relative energy error $|E(t) - E(0)| / |E(0)|$ and by how well it keeps $\mathbf{P}$ and $\mathbf{L}$. The solution exists until two or more bodies collide, or until a non-collision singularity occurs, where bodies go to infinity in finite time; Xia proved in 1992 that such solutions exist for $N = 5$.

## Variants

- **Collisional systems.** Star clusters and planetary systems, where close encounters change the orbits and must be followed exactly. These use direct summation, individual or [block time steps](/block-time-steps/) and [regularization](/kustaanheimo-stiefel-regularization/).
- **Collisionless systems.** Galaxies and dark matter, where the bodies of the code are samples of a smooth mass distribution. The force is [softened](/gravitational-softening/), and the limit $N \to \infty$ is the [Vlasov-Poisson system](/vlasov-poisson-system/).
- **Planetary problem.** One mass dominates, and the others are small. The motion is close to Kepler ellipses around the dominant mass, which the [Wisdom-Holman map](/wisdom-holman-integrator/) uses.
- **Restricted three-body problem.** One body has zero mass and moves in the field of two bodies on circular or elliptic orbits.
- **Cosmological problem.** The bodies are in an expanding periodic box; the long-range force is computed with [particle-mesh](/particle-mesh-method/), [P3M](/p3m-method/) or [TreePM](/treepm-method/) and [periodic boundary conditions](/periodic-boundary-conditions/).

## Examples

**Circular two-body orbit.** Take $G = 1$, two bodies of mass $1/2$ at $(\mp 1/2, 0, 0)$ with velocities $(0, \mp 1/2, 0)$. The separation is $r = 1$, the total mass is $M = 1$ and the relative speed is $\sqrt{G M / r} = 1$, so the bodies move on a circle with period $2\pi$. The kinetic energy is $K = 1/8$, the potential energy is $U = -1/4$, and $E = -1/8$. Here $2K + U = 0$ at each instant, which is the virial relation for a bound system on average.

**The figure-eight orbit.** Three equal masses can follow one figure-eight curve, each one a third of a period behind the next. Chenciner and Montgomery proved in 2000 that this periodic solution exists. It is a common test for integrators because it is stable and its period is known to many digits.

**A star cluster.** A Plummer sphere of $N = 10^4$ equal masses in the standard units ($G = 1$, total mass $1$, $E = -1/4$) has a crossing time of a few time units. It evolves by two-body encounters over many crossing times, and after many relaxation times its core collapses.

## Known algorithms

The force part:

- [Direct N-body summation](/direct-n-body-summation/): $\Theta(N^2)$ per evaluation, exact.
- The [Barnes-Hut algorithm](/barnes-hut-algorithm/) and other tree codes: $O(N \log N)$ for non-pathological distributions, with an error set by the [multipole acceptance criterion](/multipole-acceptance-criterion/).
- The [fast multipole method](/fast-multipole-method/): $O(N)$ for a fixed accuracy.
- [Particle-mesh](/particle-mesh-method/), [P3M](/p3m-method/) and [TreePM](/treepm-method/): a mesh and an FFT for the long-range part.

The time part:

- [Leapfrog](/verlet-integration/) with a shared step: symplectic, second order, for collisionless systems.
- The fourth-order [Hermite integrator](/hermite-n-body-integrator/) with [block time steps](/block-time-steps/): the standard for collisional systems.
- The [Wisdom-Holman map](/wisdom-holman-integrator/): a [symplectic](/symplectic-integrators/) splitting for planetary systems.
- [Kustaanheimo-Stiefel regularization](/kustaanheimo-stiefel-regularization/): smooth equations for close pairs.

## Bounds

- **No useful closed form (theorem).** Sundman found in 1912 a convergent power series for the solution of the three-body problem with nonzero angular momentum, and Wang extended it in 1991 to $N > 3$ for solutions without singularities. The series converge so slowly that they are of no use in practice (Diacu 1996).
- **Force cost.** One exact evaluation of all accelerations costs $\Theta(N^2)$ operations by direct summation. The approximate methods reach $O(N \log N)$ or $O(N)$ with a controlled error.
- **Sensitivity (measurement).** In numerical experiments, two nearby solutions of a system of many bodies separate at an exponential rate, with an e-folding time of the order of the crossing time. So a single solution can not be computed accurately for long times, and the results of a simulation are statistical.
- **Relaxation time (estimate).** Two-body encounters change the orbits of a system of $N$ equal stars in about $t_{\mathrm{relax}} \approx \frac{N}{8 \ln N} t_{\mathrm{cross}}$ (Binney and Tremaine, Chapter 1). For $N = 10^5$ this is about 1100 crossing times, and for a galaxy with $N = 10^{11}$ it is about $5 \times 10^8$ crossing times, so galaxies are collisionless.

## Reductions

- **$N = 2$ to the Kepler problem.** The relative position $\mathbf{r} = \mathbf{x}_2 - \mathbf{x}_1$ obeys $\ddot{\mathbf{r}} = -G (m_1 + m_2) \mathbf{r} / |\mathbf{r}|^3$, and the center of mass moves uniformly. The orbit is a conic section.
- **$N \to \infty$ to the Vlasov-Poisson system.** With the total mass fixed and the masses $m_i = M / N$, the distribution of the bodies in phase space tends to a solution of the collisionless Boltzmann equation coupled to the [Poisson equation](/poisson-equation/) for the potential.
- **Softened problem.** Replacing $1/r$ by $1/\sqrt{r^2 + \epsilon^2}$ gives a smooth Hamiltonian system with no collisions, at the cost of a wrong force at distances below about $\epsilon$.

## Applications

Star clusters and the growth of black holes in their cores; the stability of planetary systems over billions of years; the formation of galaxies and of the large-scale structure of the universe; the orbits of spacecraft and asteroids. The same structure, with a different pair force, is the basis of [molecular dynamics](/molecular-dynamics/) and of [smoothed particle hydrodynamics](/smoothed-particle-hydrodynamics/).

## References
