---
tag: PDJW2G
kind: algorithm
slug: boids
name: Boids
aliases:
- Reynolds flocking
area: robotics/multi-robot-systems
level: intro
summary: Reynolds's flocking rules of separation, alignment and cohesion, applied by each agent to its nearby agents, which give lifelike flocks without a leader.
model: real-ram
complexity:
  vars: {r: the number of boids, k: the number of steps}
  time: {per_step: O(r^2), total: O(k r^2)}
  space: {extra: O(r)}
properties: {deterministic: true, randomized: false, online: true}
history:
  year: 1987
  people: [Craig W. Reynolds]
  note: Reynolds introduced the boids at SIGGRAPH 1987 as a model of flocks, herds and schools for computer animation, with the rules of collision avoidance, velocity matching and flock centering.
prereqs: [multi-robot-system]
see_also: [swarm-robotics, laplacian-consensus-protocol, swarm-intelligence, particle-swarm-optimization, fixed-radius-near-neighbors, uniform-grid, reciprocal-velocity-obstacles, symplectic-euler-method]
sources:
  - paper: doi:10.1145/37402.37406
    title: Craig W. Reynolds, Flocks, herds, and schools, a distributed behavioral model, Computer Graphics 21(4), Proceedings of SIGGRAPH 1987
    locator: pages 25 to 34 (the three behaviors, the local neighborhood, and the prioritized acceleration allocation)
  - paper: doi:10.1103/PhysRevLett.75.1226
    title: Tamas Vicsek, Andras Czirok, Eshel Ben-Jacob, Inon Cohen and Ofer Shochet, Novel type of phase transition in a system of self-driven particles, Physical Review Letters 75(6), 1995
    locator: pages 1226 to 1229 (constant speed particles that take the mean heading of their neighbors plus noise)
  - paper: doi:10.1109/TAC.2003.812781
    title: Ali Jadbabaie, Jie Lin and A. Stephen Morse, Coordination of groups of mobile autonomous agents using nearest neighbor rules, IEEE Transactions on Automatic Control 48(6), 2003
    locator: pages 988 to 1001 (agreement of headings in the Vicsek model)
  - paper: doi:10.1109/TAC.2005.864190
    title: Reza Olfati-Saber, Flocking for multi-agent dynamic systems, algorithms and theory, IEEE Transactions on Automatic Control 51(3), 2006
    locator: pages 401 to 420 (flocking algorithms with potential functions and proofs of cohesion, velocity agreement and collision avoidance)
---

Boids are the flocking model of Craig Reynolds (1987). Each agent, a boid, sees only the boids within a radius $R$ and steers by three rules: **separation**, move away from boids that are too close; **alignment**, turn toward the mean velocity of the neighbors; and **cohesion**, move toward the mean position of the neighbors. The weighted sum of the three rules is the acceleration of the boid, and all boids update at the same time. No boid leads and none knows the whole flock, but the group moves as one flock, turns together, and parts and joins around obstacles. The rules are heuristics: they often give a flock, but they do not guarantee one. They are the classic example of local rules that give a global pattern in [swarm robotics](/swarm-robotics/).

## In plain words

Think of a bird in a large flock. It cannot see the whole flock, only the birds near it.

It follows three simple habits. If a neighbor is too close, it moves away so that they do not hit. It tries to fly in the same direction and at the same speed as its neighbors. And it moves a little toward the middle of its neighbors, so that it does not fall behind alone.

Every bird does the same thing at the same time. Nobody gives orders, and nobody has a plan of the flock. Still, the group soon flies together in one direction, and it bends and turns like a real flock. If the birds see too few neighbors, the flock can split into smaller groups.

## The problem

**The model.** There are $r$ boids with positions $p_i$ and velocities $v_i$ in the plane. Boid $i$ sees the set $N_i = \{ j \ne i : \lVert p_j - p_i \rVert \le R \}$. Time runs in steps of length $h$, and in each step all boids read the same snapshot and then move. The parameters are the weights $w_s, w_a, w_c$, a separation radius $R_s \le R$, a limit $A$ on the acceleration, and limits $s_{\min}$ and $s_{\max}$ on the speed.

**Input.** The start positions and velocities, the parameters, and the number $k$ of steps.

**Output.** The positions and velocities after $k$ steps. There is no exact goal; the usual measures are the order parameter $\left\lVert \frac1r \sum_i v_i / \lVert v_i \rVert \right\rVert$, which is 1 when all boids head the same way, the number of groups, and the smallest distance between two boids.

**How it differs from close pages.** The [Laplacian consensus protocol](/laplacian-consensus-protocol/) is the alignment rule alone on a fixed graph, and it has a proof. Boids add cohesion, separation and limits, and the graph changes with the positions, so the analysis of the consensus protocol does not carry over. [Particle swarm optimization](/particle-swarm-optimization/) borrows the image of a flock to search for the minimum of a function, which is a different task.

## The algorithm

```pseudo id=main
BOIDS(p, v, k)
L1  for step = 1 to k do
L2      for each boid i, in parallel, do
L3          N_i ← { j ≠ i : ‖p_j - p_i‖ ≤ R }
L4          s_i ← Σ_{j ∈ N_i, ‖p_i - p_j‖ ≤ R_s} (p_i - p_j) / ‖p_i - p_j‖²     ▷ separation
L5          a_i ← mean_{j ∈ N_i} v_j - v_i                               ▷ alignment
L6          c_i ← mean_{j ∈ N_i} p_j - p_i                               ▷ cohesion
L7          u_i ← limit(w_s s_i + w_a a_i + w_c c_i, A)                ▷ or prioritized allocation
L8          v_i ← v_i + h u_i, scaled to a speed in [s_min, s_max]
L9          p_i ← p_i + h v_i
L10 return p, v
```

A boid with no neighbors gets $u_i = 0$ and flies straight. Line L4 pushes harder the closer a neighbor is, with the inverse square of the distance as in many implementations; other strengths work too. Line L7 either scales the sum down to the norm $A$, or uses Reynolds's prioritized acceleration allocation: the requests of separation, alignment and cohesion are taken in this order until their norms use up the budget $A$, so that avoiding a collision wins over keeping up with the flock. Line L9 uses the new velocity, which is the [symplectic Euler method](/symplectic-euler-method/). Reynolds's paper calls the three rules collision avoidance, velocity matching and flock centering. The implementation uses a full disk as the neighborhood, with no limit on the angle of view.

## Example

**One boid by hand.** Let $R = 1$, $R_s = 0.5$, $w_s = 1.5$, $w_a = w_c = 1$, $h = 0.1$ and no limits. Boid 1 is at $(0, 0)$ with velocity $(1, 0)$. Boid 2 is at $(0.5, 0)$ with velocity $(0, 1)$, boid 3 at $(0, 0.8)$ with velocity $(1, 1)$, and boid 4 is far away at $(3, 3)$.

- Neighbors (line L3): boids 2 and 3, at distances $0.5$ and $0.8$.
- Separation (line L4): only boid 2 is within $R_s$, so $s_1 = (0 - 0.5, 0) / 0.25 = (-2, 0)$.
- Alignment (line L5): the mean velocity of the neighbors is $(0.5, 1)$, so $a_1 = (-0.5, 1)$.
- Cohesion (line L6): the mean position is $(0.25, 0.4)$, so $c_1 = (0.25, 0.4)$.
- Steering (line L7): $u_1 = 1.5 (-2, 0) + (-0.5, 1) + (0.25, 0.4) = (-3.25, 1.4)$.
- Motion: $v_1 = (1, 0) + 0.1 (-3.25, 1.4) = (0.675, 0.14)$, and $p_1 = (0.0675, 0.014)$.

The boid slows down, because boid 2 is close in front of it, and turns toward boid 3. With the limit $A = 2$, the plain sum is scaled to about $(-1.837, 0.791)$. The prioritized allocation instead spends the whole budget on separation, because its request $(-3, 0)$ has norm 3, and gives $(-2, 0)$.

**A flock forms, or splits.** The implementation places 20 boids at random in a square of side 2.5 with speed 1 and random headings (seed 8), with $R_s = 0.4$, $A = 2$, speeds in $[0.5, 1]$ and $h = 0.1$. At the start the order parameter is $0.147$. With $R = 2$ it is $0.98$ after 100 steps and stays near that value; after 600 steps there is one group, and no two boids are closer than $0.327$. With $R = 1.5$ and the same start, the boids form two groups that fly in different directions, and the order parameter stays near $0.49$. These numbers are measurements of one run, not guarantees.

## Correctness

There is no specification to prove: the rules are heuristics. The [proof](proofs/correctness/) shows what holds for the step itself. The new states do not depend on the order of the boids, and the step commutes with rotations, reflections and translations, so the boids need no common compass. On a complete graph without separation and without limits, the step is linear. Then the mean velocity never changes, alignment alone is a consensus step that brings all velocities to the mean, cohesion alone makes the boids oscillate about the center without settling, and both together, for a small enough step $h$, make the flock contract to one point that moves with the mean velocity. Separation, a radius smaller than the flock, and the limits make the step nonlinear and the graph time-varying, and then the flock can split, as in the example.

## Complexity

- **Per step.** Line L3 checks all pairs, which takes $O(r^2)$ time in the [real RAM](/real-ram/) model. Lines L4 to L9 take $O(|N_i|)$ time for boid $i$, so $O(r + m)$ for all boids, where $m$ is the number of pairs within distance $R$.
- **With a grid.** A [uniform grid](/uniform-grid/) or [spatial hashing](/spatial-hashing/) with cells of side $R$ finds the neighbors by [fixed-radius near neighbors](/fixed-radius-near-neighbors/) search, in expected time $O(r + m)$ per step when the boids are spread out, which makes the step linear in the size of the neighbor graph.
- **Steps.** There is no bound on the number of steps until a flock forms, because a flock need not form.
- **Space.** $O(r)$ for the states and the new states.

## Properties

- **Local and leaderless.** Each boid uses only its own state and its neighbors.
- **Synchronous.** All boids read one snapshot; updating boids one by one gives a different, order-dependent model.
- **Equivariant.** Relabeling, translations and rotations of the start give the same motion, relabeled, moved or rotated.
- **Heuristic.** No guarantee of a single flock, of alignment, or of no collisions.
- **Deterministic.** The rules have no noise; the Vicsek model adds noise to the headings.

## Variants and improvements

- **Vicsek model.** Vicsek et al. (1995) kept only alignment, with constant speed and a random error in the heading, and found a transition from disorder to order as the density grows or the noise falls. Jadbabaie, Lin and Morse (2003) proved agreement of the headings for the noise-free model when the neighbor graph is connected often enough.
- **Provable flocking.** Olfati-Saber (2006) replaced cohesion and separation by the gradient of a pair potential with a preferred distance and added velocity consensus, and proved that the flock keeps its shape, agrees on velocity and avoids collisions under stated conditions.
- **Field of view and obstacles.** Many implementations let a boid see only in front of it and add rules for obstacles, goals and leaders, which is common in games and films.
- **Robots.** On real robots, separation is replaced by a collision avoidance method with guarantees, such as [reciprocal velocity obstacles](/reciprocal-velocity-obstacles/) or [ORCA](/optimal-reciprocal-collision-avoidance/), and the boids rules give the preferred velocity.

## When to use it

Use boids for animation, games and simulations of crowds, birds and fish, where a lifelike group motion matters more than a guarantee, and as a simple baseline for the motion of a robot swarm. Use the [Laplacian consensus protocol](/laplacian-consensus-protocol/) or provable flocking laws when the group must agree or stay together for sure, and a collision avoidance method with guarantees when robots must not touch.

## Pitfalls

- **Splitting.** With a small neighbor radius the flock breaks into groups that never meet again, because boids that see no one fly straight.
- **Weights.** Too much cohesion makes the flock oscillate and clump, too much separation makes it spread out, and good weights depend on the radius, the speed and the step.
- **Large steps.** The explicit step can overshoot when $h$ times the weights is large, as for the consensus step; the linear analysis gives the bound in the simplest case.
- **Collisions.** Separation is a soft rule. Boids can still pass through each other when they meet at high speed or when the acceleration limit is low.
- **Quadratic cost.** Checking all pairs is slow for large flocks; use a grid for the neighbor search.
- **Snapshot.** Updating each boid in place, so that later boids see the new states of earlier ones, makes the result depend on the order.

## Implementations

## History

Craig Reynolds presented the boids at SIGGRAPH in 1987, with the three behaviors, a local neighborhood, and the prioritized allocation of acceleration, as a way to animate flocks without a script for each bird. Vicsek et al. (1995) studied the alignment rule with noise as a model in statistical physics. Jadbabaie, Lin and Morse (2003) gave the first proof of heading agreement for the Vicsek rule, and Olfati-Saber (2006) gave flocking algorithms with proofs, which links the boids to consensus and to multi-robot control.

## References
