---
tag: 14GKBC
kind: algorithm
slug: direct-n-body-summation
name: Direct N-body summation
aliases:
- particle-particle method
- direct summation
area: scientific-computing/n-body-and-particle-methods
level: intro
summary: Computes the force on each of N particles by summing over all other particles, in O(N^2) time per step and with no approximation error.
model: real-ram
complexity:
  vars: {N: the number of particles}
  time: {worst: "Θ(N^2)"}
  space: {extra: "Θ(N)"}
properties: {deterministic: true}
history:
  year: 1960
  people: [Sebastian von Hoerner, Sverre J. Aarseth]
  note: Von Hoerner published direct numerical integrations of small star clusters in 1960, and Aarseth developed the direct N-body codes of the following decades.
prereqs: [gravitational-n-body-problem]
see_also: [gravitational-softening, barnes-hut-algorithm, fast-multipole-method, hermite-n-body-integrator, particle-mesh-method, p3m-method, verlet-integration, molecular-dynamics]
sources:
  - book: isbn:9780521432726
    title: Sverre J. Aarseth, Gravitational N-Body Simulations, Tools and Algorithms, Cambridge University Press, 2003
    locator: Sections 1.2 and 1.3 (history and basic concepts), Section 3.7 (ring scheme)
  - book: isbn:9780852743928
    title: Roger W. Hockney and James W. Eastwood, Computer Simulation Using Particles, Adam Hilger, 1988
    locator: the particle-particle (PP) method
  - paper: "Sebastian von Hoerner, Die numerische Integration des N-Korper-Problemes fur Sternhaufen. I, Zeitschrift fur Astrophysik 50, 1960, 184-214"
    locator: the first direct integrations of star clusters
---

Direct N-body summation computes the gravitational acceleration of each of $N$ bodies as the sum of the pull of every other body. It visits each of the $N(N-1)/2$ pairs once, and it uses Newton's third law to give the force on both bodies of the pair. The result is exact up to rounding, so it is the reference against which the approximate methods ([Barnes-Hut](/barnes-hut-algorithm/), the [fast multipole method](/fast-multipole-method/), [particle-mesh](/particle-mesh-method/)) are measured. Its cost grows as $N^2$, so it is used for star clusters and planetary systems with up to about a million bodies, and on special hardware or GPUs. It is the force part of a solution of the [gravitational N-body problem](/gravitational-n-body-problem/); an integrator such as [Hermite](/hermite-n-body-integrator/) or [leapfrog](/verlet-integration/) moves the bodies.

## In plain words

Each body pulls on each other body. The pull is stronger for a heavier body and weaker for a body that is far away. To find the total pull on one body, add up the pulls of all the others, one at a time.

Do this for every body and you have the forces. The work is one small calculation for each pair of bodies. A pair pulls with equal strength in opposite directions, so one calculation gives the pull on both bodies of the pair. With a thousand bodies there are about half a million pairs, and doubling the number of bodies makes four times the work. Nothing is left out, so the answer is exact except for rounding.

## The problem

The input is $N$ masses $m_i > 0$ and positions $\mathbf{x}_i \in \mathbb{R}^3$, the gravitational constant $G$ ($G = 1$ in code units) and a softening parameter $\epsilon \ge 0$. The output is the acceleration of each body and the potential energy,

$$\mathbf{a}_i = G \sum_{j \ne i} m_j \frac{\mathbf{x}_j - \mathbf{x}_i}{\left(|\mathbf{x}_j - \mathbf{x}_i|^2 + \epsilon^2\right)^{3/2}}, \qquad U = -G \sum_{i < j} \frac{m_i m_j}{\sqrt{|\mathbf{x}_j - \mathbf{x}_i|^2 + \epsilon^2}}.$$

With $\epsilon = 0$ this is Newtonian gravity, and two bodies must not be at the same point. With $\epsilon > 0$ it is Plummer [gravitational softening](/gravitational-softening/). In both cases $\mathbf{a}_i = -\frac{1}{m_i} \nabla_{\mathbf{x}_i} U$.

## The algorithm

```pseudo id=main
DIRECT-SUM(m, x, epsilon, G)                 ▷ N bodies
L1  for i ← 1 to N do a_i ← 0;  U ← 0
L2  for i ← 1 to N - 1 do
L3      for j ← i + 1 to N do
L4          d ← x_j - x_i
L5          s ← |d|² + epsilon²
L6          w ← G / (s √s)
L7          a_i ← a_i + m_j w d
L8          a_j ← a_j - m_i w d                ▷ Newton's third law
L9          U ← U - G m_i m_j / √s
L10 return a, U
```

Lines L2 and L3 visit each unordered pair $\{i, j\}$ once. Line L6 computes the common factor $G / r^3$ of the pair, with the softened distance $r = \sqrt{s}$. Lines L7 and L8 add the pair to both bodies with opposite signs. One pair costs one square root, one division and about 20 other operations in 3D.

## Example

Take three bodies in the plane $z = 0$, with $G = 1$ and $\epsilon = 0$: $m_1 = 1$ at $(0, 0)$, $m_2 = 2$ at $(3, 0)$ and $m_3 = 3$ at $(0, 4)$. The distances are 3, 4 and 5, so each factor $w = 1 / r^3$ is rational.

| pair | $\mathbf{d} = \mathbf{x}_j - \mathbf{x}_i$ | $w$ | added to $\mathbf{a}_i$ | added to $\mathbf{a}_j$ | added to $U$ |
|---|---|---|---|---|---|
| (1, 2) | (3, 0) | 1/27 | (2/9, 0) | (-1/9, 0) | -2/3 |
| (1, 3) | (0, 4) | 1/64 | (0, 3/16) | (0, -1/16) | -3/4 |
| (2, 3) | (-3, 4) | 1/125 | (-9/125, 12/125) | (6/125, -8/125) | -6/5 |

The sums are $\mathbf{a}_1 = (2/9, 3/16) \approx (0.222222, 0.1875)$, $\mathbf{a}_2 = (-1/9 - 9/125, 12/125) \approx (-0.183111, 0.096)$, $\mathbf{a}_3 = (6/125, -1/16 - 8/125) = (0.048, -0.1265)$ and $U = -157/60 \approx -2.616667$. As a check, $\sum_i m_i \mathbf{a}_i = (2/9 - 2/9 - 18/125 + 18/125, \; 3/16 + 24/125 - 3/16 - 24/125) = (0, 0)$.

## Correctness

Each unordered pair is visited exactly once by lines L2 and L3, and the pair adds the term of $j$ to $\mathbf{a}_i$ and the term of $i$ to $\mathbf{a}_j$. So after line L10 each $\mathbf{a}_i$ holds the sum over all $j \ne i$, and $U$ holds the sum over all pairs. The pair terms of lines L7 and L8 are $m_j w \mathbf{d}$ and $-m_i w \mathbf{d}$, so in exact arithmetic $\sum_i m_i \mathbf{a}_i = 0$, and the total momentum is conserved by any integrator that uses these forces at one common time. The full proof, with the gradient identity, is in the proof file.

## Complexity

In the [real RAM](/real-ram/) model, the loop of lines L2 and L3 runs exactly $N(N-1)/2$ times, and each pass costs $\Theta(1)$ operations in a fixed dimension. So one force evaluation costs $\Theta(N^2)$ in every case, with no dependence on the positions. The extra space is $\Theta(N)$ for the accelerations; no pair list is stored.

For $N = 1000$ there are 499500 pairs. A run of $T$ steps with one force evaluation per step costs $\Theta(N^2 T)$. A force evaluation that reads every mass and position needs $\Omega(N)$ time, and no exact method below $\Theta(N^2)$ is known for this sum with arbitrary real positions in this model. The tree and multipole methods trade a controlled error for $O(N \log N)$ or $O(N)$ time.

## Properties

- **No truncation error.** The only errors are rounding errors. The order of the additions changes the result in the last bits, and the total momentum $\sum m_i \mathbf{v}_i$ is conserved only up to rounding (see the [floating-point model](/floating-point-model/)).
- **Symmetric.** Lines L7 and L8 give equal and opposite pair forces, so there is no spurious net force, unlike tree codes where the forces of $i$ on $j$ and of $j$ on $i$ come from different approximations.
- **Simple to vectorize and to parallelize.** All pairs are independent except for the sums. Each processor can take a block of targets $i$ and loop over all sources $j$; this costs $N(N-1)$ pair evaluations, twice as many, but needs no write conflicts.

## Variants and improvements

- **All targets, all sources.** Loop over all $j \ne i$ for each $i$ without the third law. This doubles the work, but each target is written by one thread only; it is the usual form on GPUs.
- **Ring scheme.** On $P$ processors, each holds $N / P$ bodies, and the blocks of sources travel around a ring of processors, so that each block meets each other block once (Aarseth 2003, Section 3.7).
- **Jerk with the force.** The Hermite integrator also needs the time derivative of each pair force; it is computed in the same loop with a few more operations per pair.
- **Neighbor schemes.** The Ahmad-Cohen scheme computes the force of near neighbors often and the force of distant bodies less often (Aarseth 2003, Section 3.2). It is still direct summation, but with two time scales.
- **Softening.** With $\epsilon > 0$ the same loop gives the Plummer softened force, used for collisionless systems.

## When to use it

Use direct summation when every close encounter matters, as in star clusters, the cores of galaxies with black holes, and planetary systems. Use it as the reference to measure the error of a tree code or an FMM. Use it when $N$ is below a few thousand, because there the tree methods have more overhead than they save. For collisionless systems with millions of bodies, use [Barnes-Hut](/barnes-hut-algorithm/), [FMM](/fast-multipole-method/), [particle-mesh](/particle-mesh-method/) or [TreePM](/treepm-method/) instead.

## Pitfalls

- **Self-interaction.** The pair $j = i$ must be skipped. With $\epsilon > 0$ it gives no force but adds $-G m_i^2 / \epsilon$ to the energy.
- **Coincident bodies with $\epsilon = 0$.** Two bodies at the same point give a division by zero. Real close encounters with $\epsilon = 0$ need [regularization](/kustaanheimo-stiefel-regularization/), not a tiny time step.
- **Counting pairs twice in the energy.** If the loop runs over all ordered pairs, the potential energy must be halved.
- **The cost of the square root.** The square root and the division dominate the cost of a pair. Compute $1/\sqrt{s}$ once and form $w$ from it.
- **Rounding in large sums.** For large $N$, the sum of many small far terms with a few large near terms loses digits. Compensated or pairwise summation reduces this when it matters ([Kahan summation](/kahan-summation/), [pairwise summation](/pairwise-summation/)).

## Implementations

## History

Von Hoerner published direct integrations of small star clusters on a digital computer in 1960. Aarseth wrote the NBODY codes from the 1960s on, with individual time steps, neighbor schemes and regularization, all built around a direct force sum (Aarseth 2003, Section 1.2). Hockney and Eastwood call the method the particle-particle (PP) method and compare it with mesh methods.

## References
