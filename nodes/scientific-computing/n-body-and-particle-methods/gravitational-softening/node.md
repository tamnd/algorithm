---
tag: 4YEZ3N
kind: technique
slug: gravitational-softening
name: Gravitational softening
aliases:
- Plummer softening
- softening length
area: scientific-computing/n-body-and-particle-methods
level: core
summary: "Replaces the pair potential -G m / r by -G m / sqrt(r^2 + epsilon^2), so the force stays finite in close encounters; epsilon sets the smallest resolved scale."
prereqs: [gravitational-n-body-problem]
see_also: [direct-n-body-summation, barnes-hut-algorithm, treepm-method, particle-mesh-method, vlasov-poisson-system, smoothed-particle-hydrodynamics, kustaanheimo-stiefel-regularization, block-time-steps]
sources:
  - book: isbn:9780521432726
    title: Sverre J. Aarseth, Gravitational N-Body Simulations, Tools and Algorithms, Cambridge University Press, 2003
    locator: Chapter 6 (tree codes), Section 6.2 (basic formulation)
  - paper: doi:10.1046/j.1365-8711.2001.04237.x
    title: "Walter Dehnen, Towards optimal softening in three-dimensional N-body codes - I. Minimizing the force error, Monthly Notices of the Royal Astronomical Society 324(2), 2001, 273-291"
    locator: the bias and noise parts of the force error and the optimal softening as a function of N
  - paper: doi:10.1086/191344
    title: "Lars Hernquist and Neal Katz, TREESPH: a unification of SPH with the hierarchical tree method, Astrophysical Journal Supplement Series 70, 1989, 419-446"
    locator: the spline kernel softening
  - paper: doi:10.1111/j.1365-2966.2005.09655.x
    title: "Volker Springel, The cosmological simulation code GADGET-2, Monthly Notices of the Royal Astronomical Society 364(4), 2005, 1105-1134"
    locator: the spline softening of the gravitational force
---

Gravitational softening changes the pair force of an N-body code at short distances, so that the force stays finite when two bodies come close. The usual form, due to Plummer's model of a star cluster, replaces the Newtonian pair potential $-G m / r$ by

$$\phi(r) = -\frac{G m}{\sqrt{r^2 + \epsilon^2}}, \qquad \mathbf{F} = -G m_i m_j \frac{\mathbf{r}}{(r^2 + \epsilon^2)^{3/2}},$$

where $\mathbf{r}$ points from body $j$ to body $i$ and $\epsilon > 0$ is the softening parameter. The force is the gradient of the potential, so the softened system is still Hamiltonian and still conserves energy and momentum. Softening is used in collisionless simulations, where each body of the code is a sample of a smooth mass distribution of stars or dark matter, and the close encounters of the samples are an error of the method, not physics. It is not used in collisional simulations of star clusters and planets, which treat close encounters by [regularization](/kustaanheimo-stiefel-regularization/).

## In plain words

In a computer model of a galaxy, each body stands for a large cloud of stars, not for one star. When two such bodies pass close to each other, true gravity gives them a very strong kick, and the computer must take tiny steps to follow it. Real clouds of stars do not kick each other like that.

Softening changes the pull between two very close bodies so that it becomes weak instead of very strong. Far away, the pull is almost the same as before. One number sets the distance below which the pull is weakened. A small number keeps more detail but gives more random kicks; a large number gives smoother results but blurs small structures.

## When it applies

- The bodies of the code are tracers of a smooth density, as in galaxies, dark matter halos and cosmology. The [Vlasov-Poisson system](/vlasov-poisson-system/) is the target, and two-body encounters are noise.
- The time step must stay bounded. With $\epsilon > 0$ the largest acceleration from one body of mass $m$ is $\frac{2}{3\sqrt{3}} G m / \epsilon^2 \approx 0.385\, G m / \epsilon^2$, so a shared step of order $\sqrt{\epsilon^3 / (G m)}$ resolves every pair passage (heuristic).
- The force method has its own short-range resolution, such as a tree code or a [TreePM](/treepm-method/) code; softening sets this scale in a controlled way.

It does not apply to systems where close encounters are real, such as binaries, star clusters and planetary systems.

## The template

1. Choose $\epsilon$ for the problem. Smaller $\epsilon$ resolves smaller structures but increases the two-body noise; larger $\epsilon$ smooths the noise but biases the force below a few $\epsilon$.
2. Replace each pair potential by the softened one, $\phi(r) = -G m / \sqrt{r^2 + \epsilon^2}$ for the Plummer form, or by a kernel with compact support (below). Use the gradient of the same potential as the force, so that energy is conserved.
3. Use the same softening in the far-field approximation of the force method, or show that the difference is below the force error of the method. For a tree code, the softened monopole of a far cell differs from the Newtonian one by a relative amount of about $\frac{3}{2} \epsilon^2 / d^2$.
4. Choose the time step from $\epsilon$ and the local density, and report the relative energy error $|E(t) - E(0)| / |E(0)|$ with the softened potential energy $U = -G \sum_{i<j} m_i m_j / \sqrt{r_{ij}^2 + \epsilon^2}$.

## Classic examples

**The Plummer force against Newton.** The ratio of the Plummer pair force to the Newtonian one is $r^3 / (r^2 + \epsilon^2)^{3/2}$.

| $r / \epsilon$ | 0.5 | 0.7071 | 1 | 2 | 5 | 10 |
|---|---|---|---|---|---|---|
| force ratio | 0.0894 | 0.1925 | 0.3536 | 0.7155 | 0.9428 | 0.9852 |

The softened force is largest at $r = \epsilon / \sqrt{2}$ and goes to zero linearly as $r \to 0$. The relative error at large $r$ is about $\frac{3}{2} \epsilon^2 / r^2$, so it is still 1.5 percent at $r = 10\epsilon$. The Plummer potential of a point mass is the exact potential of a Plummer sphere of mass $m$ and scale $\epsilon$, with density $\rho(r) = \frac{3 m \epsilon^2}{4 \pi (r^2 + \epsilon^2)^{5/2}}$, so the softened problem is the problem of bodies that are small spheres that pass through each other.

**Tree codes for galaxies.** Collisionless tree codes such as [Barnes-Hut](/barnes-hut-algorithm/) use a softened monopole for each accepted cell and a softened pair force for each nearby body (Aarseth 2003, Chapter 6).

**Spline softening.** TREESPH (Hernquist and Katz 1989) and GADGET-2 (Springel 2005) soften gravity with the cubic spline kernel of [smoothed particle hydrodynamics](/smoothed-particle-hydrodynamics/). Each body is a spline mass distribution of finite radius, so the force is exactly Newtonian beyond that radius, unlike the Plummer force, which is wrong at every distance.

## Variations

- **Kernels with compact support.** A smooth mass distribution with a finite radius $h$, such as the spline, gives exactly the Newtonian force at $r \ge h$. Codes quote the Plummer-equivalent $\epsilon$, the one with the same potential at $r = 0$.
- **Optimal softening.** Dehnen (2001) splits the force error into a bias, which grows with $\epsilon$, and a noise, which falls with $\epsilon$. Their sum has a minimum at an $\epsilon$ that depends on the mass distribution and becomes smaller as $N$ grows (measurement and asymptotic analysis).
- **Adaptive softening.** Each body gets its own $\epsilon_i$, from the local density, as for the smoothing length of SPH. The pair force then uses a symmetric combination, such as the mean or the maximum of $\epsilon_i$ and $\epsilon_j$, to keep Newton's third law. A force that is not the gradient of one potential no longer conserves energy, and extra terms are needed to restore it.
- **Comoving softening.** In cosmology $\epsilon$ is fixed in comoving coordinates at early times and in physical coordinates later.
- **Softening by type.** Codes with stars, gas and dark matter use a different $\epsilon$ for each type of body.

## Pitfalls

- **Results below the softening scale.** Structures smaller than about $2\epsilon$ to $3\epsilon$ are not resolved, and the density profiles of halos are wrong inside this radius.
- **Too small for the time step.** If $\epsilon$ is small and the step is not, close pairs gain energy at each step, and the energy error grows. Choose $h$ from $\epsilon$, or use adaptive [block time steps](/block-time-steps/).
- **Two-body relaxation still happens.** Softening reduces the effect of close encounters only; the distant encounters still relax the system on a time scale of the order of $N / \ln N$ crossing times.
- **Mixing potentials.** The energy must use the same softened potential as the force. A Newtonian $U$ with a softened force shows an energy error that is not an error of the integrator.
- **Not physics for collisional systems.** Softening a binary or a planetary system changes its orbits. Use [regularization](/kustaanheimo-stiefel-regularization/) instead.

## Exercises

1. Show that the Plummer potential $-G m / \sqrt{r^2 + \epsilon^2}$ solves the [Poisson equation](/poisson-equation/) $\nabla^2 \phi = 4 \pi G \rho$ with $\rho(r) = \frac{3 m \epsilon^2}{4 \pi (r^2 + \epsilon^2)^{5/2}}$, and that this density has total mass $m$.
2. Show that the magnitude of the Plummer pair force is largest at $r = \epsilon / \sqrt{2}$, with the value $\frac{2}{3\sqrt{3}} G m_i m_j / \epsilon^2$.
3. Show that the relative force error at $r \gg \epsilon$ is $\frac{3}{2} \epsilon^2 / r^2 + O(\epsilon^4 / r^4)$, and find the radius where the exact error is 1 percent. (Answer: $r \approx 12.2\,\epsilon$.)
4. Two bodies of mass $m$ start at rest at distance $D$ and fall toward each other with the Plummer potential. Show that they pass through each other with the finite relative speed $v = \sqrt{4 G m (1/\epsilon - 1/\sqrt{D^2 + \epsilon^2})}$.

## References
