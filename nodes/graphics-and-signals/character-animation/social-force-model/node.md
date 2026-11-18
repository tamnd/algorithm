---
tag: 4BAJB2
kind: model
slug: social-force-model
name: Social force model
aliases:
- Helbing social force model
area: graphics-and-signals/character-animation
level: core
summary: "Move each pedestrian by a driving force toward its goal plus repulsive forces from other people and walls, integrated as a particle system."
prereqs: [symplectic-euler-method]
see_also: [continuum-crowds, particle-system, boids, reciprocal-velocity-obstacles, optimal-reciprocal-collision-avoidance, velocity-obstacle, molecular-dynamics, cellular-automaton]
sources:
  - paper: doi:10.1103/PhysRevE.51.4282
    title: "Dirk Helbing and Péter Molnár, Social force model for pedestrian dynamics, Physical Review E 51(5), 4282-4286, 1995"
    locator: "the whole paper (the driving term, the repulsion from other people and from borders, the attraction terms, and the simulated lanes and oscillations at bottlenecks; general locator)"
  - paper: doi:10.1038/35035023
    title: "Dirk Helbing, Illés Farkas and Tamás Vicsek, Simulating dynamical features of escape panic, Nature 407, 487-490, 2000"
    locator: "the equation of motion with the driving term, the pair force with repulsion, body force and sliding friction, the wall force, the herding rule, and the constants of the model"
---

The social force model moves pedestrians as particles in the plane. Each person has a goal and a desired speed, and three kinds of force act on the person: a driving force that relaxes the velocity toward the desired velocity, a repulsion from every other person and from every wall that grows fast as they come close, and, when bodies touch, a body force and a sliding friction. Dirk Helbing and Péter Molnár introduced the model in 1995; the form on this page, with the body force and the friction, is the one of Helbing, Farkas and Vicsek (2000). The forces are "social" in the sense that they describe the wish to keep a distance; only the contact forces stand for real forces between bodies. All constants are fitted or tuned values, not laws.

## The machine

The state is a set of $n$ people. Person $i$ has a position $\mathbf x_i$ (in m), a velocity $\mathbf v_i$ (in m/s), a mass $m_i$, a radius $r_i$, a desired speed $v_i^0$ and a goal; $\mathbf e_i$ is the unit vector from $\mathbf x_i$ toward the goal. The equation of motion of Helbing, Farkas and Vicsek is

$$m_i \frac{d\mathbf v_i}{dt} = m_i \frac{v_i^0 \mathbf e_i - \mathbf v_i}{\tau_i} + \sum_{j \ne i} \mathbf f_{ij} + \sum_W \mathbf f_{iW}, \qquad \frac{d\mathbf x_i}{dt} = \mathbf v_i .$$

The first term is the driving force: without other forces, the velocity relaxes to $v_i^0 \mathbf e_i$ with the time constant $\tau_i$. For two people with $d_{ij} = |\mathbf x_i - \mathbf x_j|$, the unit normal $\mathbf n_{ij} = (\mathbf x_i - \mathbf x_j) / d_{ij}$ from $j$ to $i$, the tangent $\mathbf t_{ij} = (-n_{ij}^y, n_{ij}^x)$, the sum of radii $r_{ij} = r_i + r_j$ and $g(z) = \max(z, 0)$, the pair force is

$$\mathbf f_{ij} = \Big(A\, e^{(r_{ij} - d_{ij}) / B} + k\, g(r_{ij} - d_{ij})\Big) \mathbf n_{ij} + \kappa\, g(r_{ij} - d_{ij})\, \big((\mathbf v_j - \mathbf v_i) \cdot \mathbf t_{ij}\big)\, \mathbf t_{ij} .$$

The exponential term is the social repulsion. The term with $k$ is a body force that resists compression, and the term with $\kappa$ is a sliding friction that resists the relative tangential motion; both act only when the bodies overlap, $d_{ij} < r_{ij}$. A wall acts in the same way, with $d_{iW}$ the distance to the wall, $\mathbf n_{iW}$ the normal from the wall to the person, and the friction term $-\kappa\, g(r_i - d_{iW})\, (\mathbf v_i \cdot \mathbf t_{iW})\, \mathbf t_{iW}$.

The constants of the 2000 paper are $A = 2 \cdot 10^3$ N, $B = 0.08$ m, $k = 1.2 \cdot 10^5$ kg/s$^2$, $\kappa = 2.4 \cdot 10^5$ kg/(m s), $\tau = 0.5$ s, $m = 80$ kg and radii from 0.25 m to 0.35 m. The desired speed is about 0.6 m/s for relaxed walking, about 1 m/s for normal walking and up to 1.5 m/s for nervous people. The paper chose $A$ and $B$ to fit a measured flow of about 0.73 persons per second through a door of 1 m. These are fitted and tuned values.

In escape panic the paper also adds herding: the desired direction becomes a normalized mix $(1 - p)\, \mathbf e_i + p\, \langle \mathbf e_j \rangle_i$ of the own direction and the mean direction of the neighbors, with a panic parameter $p \in [0, 1]$. The 1995 model has the same driving term, with repulsive potentials from other people and from borders, attraction to friends or to attractive places, and a weaker effect of what is behind a person than of what is in front of the person.

The code with this page keeps the pair force of the 2000 paper and leaves out the walls, the herding and the attraction. It steps the equations with [symplectic Euler](/symplectic-euler-method/), velocity first, with a time step $\Delta t$:

```pseudo id=main
SOCIAL-FORCE-STEP(X, V, R, goals, v⁰, Δt)
L1  Fᵢ ← m (v⁰ᵢ eᵢ - vᵢ) / τ for every person i      ▷ the driving force
    for every pair i < j
L2      f ← f_ij(xᵢ, xⱼ, vᵢ, vⱼ, rᵢ, rⱼ)              ▷ repulsion, body force, friction
L3      Fᵢ ← Fᵢ + f; Fⱼ ← Fⱼ - f                      ▷ the reaction on j
    for every person i
L4      vᵢ ← vᵢ + Δt Fᵢ / m
L5      xᵢ ← xᵢ + Δt vᵢ
    return X, V
```

The standing assumptions are those of a particle system: people are disks in the plane with no body orientation, the forces add, and every person sees every other person. In the code all people have the same mass.

## What it counts

The model gives the trajectories of all people, and from them the quantities of crowd studies: the flow through a door or a corridor (persons per second), the density (persons per square meter), the speeds, and the time to leave a room. It is a model of collective behavior, and the papers compare its output with observed patterns, not with single trajectories. The fit of $A$ and $B$ to a door flow is a measurement on real crowds; that the simulated crowd shows a pattern is a measurement on the model.

The direct cost of one step is $\Theta(n^2)$ time for all pairs and $\Theta(n)$ space. The repulsion decays by the factor $e$ every $B = 0.08$ m, so implementations cut it off at a distance $d_c$ and find the near pairs with a [uniform grid](/uniform-grid/) or [spatial hashing](/spatial-hashing/), which costs $O(n)$ expected time per step at a bounded density.

## Relation to other models

- A [particle system](/particle-system/) has the same state and update loop but no forces between particles. The social force model adds pair forces, so it is closer to [molecular dynamics](/molecular-dynamics/), with social potentials in place of physical ones.
- [Boids](/boids/) steer each agent by rules on the velocities of its neighbors (separation, alignment, cohesion) for flocks, not by forces with a goal for each agent.
- [Velocity obstacles](/velocity-obstacle/), [reciprocal velocity obstacles](/reciprocal-velocity-obstacles/) and [ORCA](/optimal-reciprocal-collision-avoidance/) choose a new velocity outside the set of velocities that lead to a collision within a time window. They are geometric and predict the motion of others, while social forces react only to the present distance; ORCA proves collision free motion under its assumptions, and the social force model has no such guarantee.
- [Continuum crowds](/continuum-crowds/) replace the people by a density field per group and plan with a potential over the whole space; they avoid local minima of the goal direction, which the social force model, with only a straight line to the goal, does not.
- [Cellular automaton](/cellular-automaton/) models of pedestrians move people between cells of a grid with rules, in discrete time and space.

## Known results in the model

1. **Antisymmetric pair forces (proved).** Exchanging $i$ and $j$ changes the sign of $\mathbf n_{ij}$, $\mathbf t_{ij}$ and $\mathbf v_j - \mathbf v_i$, so $\mathbf f_{ji} = -\mathbf f_{ij}$. So the pair forces of a group sum to zero, and only the driving forces and the walls change its total momentum. Line L3 applies the reaction by this rule. The test checks the rule on random pairs to a relative $10^{-9}$, and the zero sum for 12 people.
2. **Relaxation (proved, with its step limit).** A single person with no other forces has, under symplectic Euler, $\mathbf v_n = v^0 \mathbf e + (\mathbf v_0 - v^0 \mathbf e)(1 - \Delta t / \tau)^n$. The exact solution has $e^{-t/\tau}$ in place of the power. The step converges for $0 < \Delta t < 2 \tau$ and does not overshoot for $\Delta t \le \tau$. The test checks the formula to $10^{-12}$ for 100 steps at $\Delta t = 0.01$ s.
3. **Step limit of the body force (proved for this term alone).** Two overlapping people, with only the body force, are a linear spring $k$ on the reduced mass $m/2$, with $\omega = \sqrt{2k/m} = 54.8$ rad/s. Symplectic Euler is stable for this spring when $\Delta t < 2/\omega = 0.037$ s. The friction and the stiffness $A/B$ of the repulsion add to this, so the code uses $\Delta t = 0.01$ s.
4. **Standing distance (proved).** A person at rest who pushes toward a fixed person feels the driving force $m v^0 / \tau$ and the repulsion. The two balance at $d^* = r_{ij} + B \ln(A \tau / (m v^0))$ if $m v^0 / \tau < A$. For $v^0 = 1$ m/s and $r_{ij} = 0.6$ m, the driving force is 160 N and $d^* = 0.6 + 0.08 \ln 12.5 = 0.802$ m. So with these constants one person alone does not touch another, and contact forces come only when several people push in a row.
5. **Two crossing groups (measured).** In the test, two groups of 5 people walk through each other in opposite directions with $v^0 = 1$ m/s, $\Delta t = 0.01$ s and 2000 steps (seed 4). They pass in 20 s, and the smallest gap between two bodies is about 0.068 m, with no overlap. This is a measurement of one toy, not a bound.
6. **Lanes and oscillations (observed in simulation).** Helbing and Molnár (1995) report that people walking in opposite directions in a corridor form lanes of one walking direction, and that the passing direction at a narrow bottleneck oscillates. Both are self organized patterns of the model, also seen in real crowds.
7. **Panic effects (observed in simulation).** Helbing, Farkas and Vicsek (2000) report that people with a high desired speed jam at a door and leave more slowly than calm people ("faster is slower"), that the crowd forms arches before the exit, and that in a smoke filled room with strong herding the crowd uses the exits badly, while a mix of individual and herding behavior works best. These are measurements on the model, with the constants above.

## References
