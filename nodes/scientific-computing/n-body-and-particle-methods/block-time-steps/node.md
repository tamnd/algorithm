---
tag: 23X3JT
kind: technique
slug: block-time-steps
name: Block time steps
aliases:
- hierarchical time steps
- individual time steps
area: scientific-computing/n-body-and-particle-methods
level: advanced
summary: Gives each particle a power-of-two fraction of a base step chosen from its own acceleration, so dense regions get small steps without slowing the rest.
prereqs: [hermite-n-body-integrator, adaptive-step-size-control]
see_also: [respa-multiple-time-step, direct-n-body-summation, verlet-integration, symplectic-integrators, kustaanheimo-stiefel-regularization, barnes-hut-algorithm, gravitational-softening, wisdom-holman-integrator]
sources:
  - book: isbn:9780521432726
    title: Sverre J. Aarseth, Gravitational N-Body Simulations, Tools and Algorithms, Cambridge University Press, 2003
    locator: Section 2.3 (individual time-steps), Section 2.6 (block time-steps), Section 2.7 (time-symmetric method)
  - paper: doi:10.1093/pasj/44.2.141
    title: "Junichiro Makino and Sverre J. Aarseth, On a Hermite integrator with Ahmad-Cohen scheme for gravitational many-body problems, Publications of the Astronomical Society of Japan 44(2), 1992, 141-151"
    locator: the Hermite scheme with individual time steps
  - paper: doi:10.1016/j.newast.2006.06.003
    title: "Junichiro Makino, Piet Hut, Murat Kaplan and Hasan Saygin, A time-symmetric block time-step algorithm for N-body simulations, New Astronomy 12(2), 2006, 124-133"
    locator: the time-symmetric choice of block steps and the random walk of the energy error
  - paper: doi:10.1111/j.1365-2966.2005.09655.x
    title: "Volker Springel, The cosmological simulation code GADGET-2, Monthly Notices of the Royal Astronomical Society 364(4), 2005, 1105-1134"
    locator: the power-of-two hierarchy of individual time steps for leapfrog
---

Block time steps let each body of an N-body code advance with its own time step, but restrict the steps to powers of 2 of a base step $h_0$, $h_k = h_0 / 2^k$, and keep the time of each body a multiple of its step. Then the bodies fall into blocks that are due at the same time, and the force of a whole block is computed in one pass. In a star cluster the steps of bodies differ by factors of $10^4$ or more, between the dense core or a binary and the outer halo, so a shared step would spend almost all of its work on bodies that do not need it. The technique is used with the [Hermite integrator](/hermite-n-body-integrator/) in direct codes, and with [leapfrog](/verlet-integration/) in tree codes for galaxies and cosmology.

## In plain words

Some bodies move fast, close to other bodies, and need very short steps. Others move slowly far out and could take long steps. Giving all of them the shortest step wastes most of the work.

So give each body its own step, but only from a fixed list: a base step, half of it, a quarter, an eighth, and so on. A body is moved only when its own step is over. Because all steps come from the same halving list, many bodies are due at the same moment, and they can be moved together. A body may move to a shorter step at any time, but to a longer step only at a moment when the longer step fits.

## When it applies

- The steps that the bodies need differ by large factors, as in star clusters, galactic nuclei and halos with dense centers.
- The force on one body can be computed alone, as in [direct summation](/direct-n-body-summation/) or a tree code, and the positions of the other bodies can be predicted cheaply to any time.
- The integrator is a one-step method that can start at any time with any step, such as the Hermite scheme or leapfrog.

It does not apply as such when the force of all bodies is computed together on a mesh, as in [particle-mesh](/particle-mesh-method/) codes; there the [RESPA](/respa-multiple-time-step/) splitting of the force is the analogue.

## The template

1. **Choose the base step** $h_0$ and the largest level $K$. The steps are $h_k = h_0 / 2^k$ for $0 \le k \le K$.
2. **Quantize the wanted step.** For each body, compute the wanted step $h^*_i$ from a criterion (for example the Aarseth criterion of the Hermite scheme), and give it the largest $h_k \le h^*_i$.
3. **Keep the times aligned.** Each body has a time $t_i$ that is a multiple of its step $h_i$. A step may be halved at any update. A step may be doubled only when $t_i$ is a multiple of $2 h_i$, and by one factor of 2 per update.
4. **Find the next block.** The next time is $t = \min_i (t_i + h_i)$, and the block is the set of bodies with $t_i + h_i = t$. Because of step 3, the block is exactly the set of bodies whose step divides $t$.
5. **Predict all bodies** to time $t$ with a cheap Taylor series (positions and velocities from $\mathbf{a}$ and $\mathbf{j}$), at cost $O(N)$.
6. **Compute the force** on the bodies of the block from the predicted state, at cost $O(n N)$ for a block of $n$ bodies by direct summation, and **correct** them.
7. **Set the new steps** of the block from the criterion with the rules of step 3, and go to step 4.

## Classic examples

**A hand example.** Take $h_0 = 1$ and three bodies whose wanted steps are $0.3$, $0.12$ and $0.05$. They get $h = 1/4$, $1/16$ and $1/32$. Over the interval $[0, 1/4]$ the block times are the multiples of $1/32$:

| time | 1/32 | 2/32 | 3/32 | 4/32 | 5/32 | 6/32 | 7/32 | 8/32 |
|---|---|---|---|---|---|---|---|---|
| block | 3 | 2, 3 | 3 | 2, 3 | 3 | 2, 3 | 3 | 1, 2, 3 |

So 13 body updates are needed instead of $3 \times 8 = 24$ with a shared step of $1/32$. If body 2 at time $3/16$ wants a step of $1/8$, it must wait: $3/16$ is not a multiple of $1/8$, so it keeps $1/16$ and doubles at time $1/4$.

**The Hermite scheme in direct codes.** The NBODY codes and the GRAPE and GPU codes use the Hermite scheme with block steps and the Aarseth criterion (Aarseth 2003, Sections 2.5 and 2.6). The force pipeline of the hardware computes the force on all bodies of a block in parallel.

**Leapfrog in tree codes.** GADGET-2 uses a hierarchy of power-of-two steps for a kick-drift-kick leapfrog, with steps from the acceleration and the [softening](/gravitational-softening/) parameter (Springel 2005).

## Variations

- **Individual steps without quantization.** In Aarseth's earlier codes each body had an arbitrary step, and only one body was due at a time; this needs a prediction of all bodies per update and gives no blocks, so it is slower on vector and parallel hardware.
- **Time-symmetric block steps.** Choose the steps so that the step from $t$ to $t + h$ is the same as the step that the criterion would give backwards from $t + h$. The step of a body can still change only by a factor of 2 at a time. With this choice the energy error of the Hermite scheme behaves as a random walk instead of a linear drift (Makino, Hut, Kaplan and Saygin 2006).
- **Neighbor schemes.** The Ahmad-Cohen scheme gives each body two steps, a short one for the force of its neighbors and a long one for the rest (Aarseth 2003, Chapter 3).
- **Hierarchical splitting of the Hamiltonian.** Split the bodies by their steps and the Hamiltonian into the parts of each level, as in RESPA, which gives a symplectic integrator with power-of-two steps.

## Pitfalls

- **Lost symmetry and conservation.** Body $i$ is corrected with the force of body $j$ at a predicted position, while $j$ may be updated later with a force from $i$ at another time. So the pair forces are not equal and opposite, and the total momentum is not conserved exactly. The method is not symplectic and not time-symmetric, even with leapfrog as the base integrator.
- **Doubling at the wrong time.** Doubling a step when $t_i$ is not a multiple of $2 h_i$ breaks the alignment, and later blocks no longer match.
- **Too few levels.** If the wanted step is below $h_K$, the body takes a step that is too long. Add levels, or regularize the close pair with [Kustaanheimo-Stiefel regularization](/kustaanheimo-stiefel-regularization/).
- **Sudden encounters.** A body with a long step does not notice a fast body that comes close before its next update. Codes limit the ratio of the steps of neighbors, or wake bodies up early.
- **Prediction error.** Inactive bodies are only predicted, with a low-order series; if their steps are too long, the predicted positions spoil the force on the active bodies.

## Exercises

1. Show that, with the rules of step 3, the block at each block time $t$ is exactly the set of bodies whose step divides $t$. (Hint: each body has $t_i < t \le t_i + h_i$, and $t_i$ is a multiple of $h_i$.) Conclude that the bodies with the smallest step are in every block.
2. A cluster has $N_k$ bodies at level $k$, for $k = 0, \ldots, K$. Show that the number of body updates per base step is $\sum_k N_k 2^k$, compared with $N 2^K$ for a shared step, and compute the gain for $N_0 = 900$, $N_3 = 90$ and $N_6 = 10$. (Answer: 2260 against 64000.)
3. Show that a body at time $t_i$ with step $h_k$ that wants a step of $2 h_k$ waits at most one step of $h_k$.
4. In the cluster of Exercise 2, count the body predictions per base step ($64 \times 1000$) and the pair forces per base step ($2260 \times 999$), and explain why the prediction is not the bottleneck.

## References
