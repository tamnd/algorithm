---
tag: JVQRJ5
kind: model
slug: behler-parrinello-potential
name: Behler-Parrinello neural network potential
aliases:
- high-dimensional neural network potential
area: scientific-computing/molecular-simulation
level: research
summary: Writes the energy as a sum of atomic energies, each a neural network of symmetry functions of the atom's neighborhood, trained on quantum calculations.
model: real-ram
history:
  year: 2007
  people: [Jörg Behler, Michele Parrinello]
  note: Behler and Parrinello wrote the energy of a large system as a sum of atomic neural network outputs in 2007 and fitted it to density functional calculations of silicon. Behler described the atom-centered symmetry functions in detail in 2011.
prereqs: [interatomic-potential, backpropagation]
see_also: [interatomic-potential, embedded-atom-method, born-oppenheimer-molecular-dynamics, molecular-dynamics, gaussian-process, kernel-ridge-regression, automatic-differentiation, activation-function]
sources:
  - paper: doi:10.1103/PhysRevLett.98.146401
    title: Jörg Behler and Michele Parrinello, Generalized neural-network representation of high-dimensional potential-energy surfaces, Physical Review Letters 98(14), 2007, 146401
    locator: the energy as a sum of atomic networks of symmetry functions, and the application to silicon
  - paper: doi:10.1063/1.3553717
    title: Jörg Behler, Atom-centered symmetry functions for constructing high-dimensional neural network potentials, Journal of Chemical Physics 134(7), 2011, 074106
    locator: the cutoff function and the radial and angular symmetry functions
  - paper: doi:10.1021/acs.chemrev.0c00868
    title: Jörg Behler, Four generations of high-dimensional neural network potentials, Chemical Reviews 121(16), 2021, 10037-10072
    locator: the four generations, the training procedure and the treatment of long-range electrostatics
---

The Behler-Parrinello potential is a machine-learned [interatomic potential](/interatomic-potential/). It writes the energy of $N$ atoms as a sum of atomic energies, $U = \sum_i E_i$, and computes each $E_i$ with a small neural network from a fixed-length vector of symmetry functions that describe the neighbors of atom $i$ within a cutoff. The weights of the networks are fitted to energies and forces from quantum calculations, usually density functional theory. The result can be close to the quantum energy surface for configurations like those in the training set, at a cost that grows as $O(N)$, but its accuracy is a measurement on a test set, not a property of the model.

## The machine

**Unknowns.** The positions $r_1, \ldots, r_N$, with $R_{ij} = |r_i - r_j|$ and the angle $\theta_{ijk}$ at atom $i$ between the directions to $j$ and $k$.

**Cutoff function.** With a cutoff radius $R_c$,
$$f_c(R) = \tfrac{1}{2}\left[\cos(\pi R / R_c) + 1\right] \text{ for } R < R_c, \qquad f_c(R) = 0 \text{ otherwise}.$$
It goes to zero with zero slope at $R_c$, so the energy and the forces are continuous.

**Symmetry functions.** Each atom $i$ gets a vector $G_i = (G_i^1, \ldots, G_i^M)$ of functions of its neighborhood that do not change under translation, rotation or exchange of neighbors of the same element. The radial functions are
$$G_i^{\mu} = \sum_{j \ne i} e^{-\eta_\mu (R_{ij} - R_{s,\mu})^2} f_c(R_{ij}),$$
with a width $\eta_\mu$ (in inverse length squared) and a center $R_{s,\mu}$ for each $\mu$; with $\eta = 0$ the function $\sum_j f_c(R_{ij})$ is a smooth count of neighbors. The angular functions are
$$G_i^{\mu} = 2^{1-\zeta} \sum_{j, k} (1 + \lambda \cos\theta_{ijk})^{\zeta}\, e^{-\eta (R_{ij}^2 + R_{ik}^2 + R_{jk}^2)} f_c(R_{ij}) f_c(R_{ik}) f_c(R_{jk}),$$
with $\lambda = \pm 1$ and $\zeta \ge 1$, summed over pairs of neighbors $j, k$ of atom $i$. Papers differ on whether each pair $\{j, k\}$ is counted once or twice, which changes these functions by a factor 2; an implementation must state its choice, and the network must be trained with the same one.

**Atomic networks.** For each element there is one feed-forward network $\mathcal{N}$, the same for every atom of that element. With one hidden layer of $H$ units,
$$E_i = b^{(2)} + \sum_{h=1}^{H} w^{(2)}_h \tanh\Big(b^{(1)}_h + \sum_{\mu} w^{(1)}_{h\mu} G_i^{\mu}\Big),$$
and in practice two hidden layers of 10 to 50 units each are common. The energy is $U = \sum_i E_i$.

**Forces.** By the chain rule, $F_k = -\sum_i \sum_\mu (\partial E_i / \partial G_i^\mu)\, \nabla_k G_i^\mu$. The derivatives $\partial E_i / \partial G_i^\mu$ come from [backpropagation](/backpropagation/) through each network, and $\nabla_k G_i^\mu$ is known in closed form. The forces are the exact gradient of the model energy, so the energy is conserved in molecular dynamics up to the integrator error.

**Parameters, fitted and derived.**

- **Fitted:** all network weights and biases, often thousands per element. They minimize the squared error between the model and the reference energies, often with a weighted squared error of the forces added, on a training set of configurations.
- **Chosen, not fitted:** the cutoff $R_c$, the set of symmetry functions and their $\eta$, $R_s$, $\lambda$ and $\zeta$, and the size of the networks. They are hyperparameters, set by trial and by validation.
- **Derived:** nothing about the energy itself. The structure of the model, a sum of local atomic energies with the right symmetries, is a design choice motivated by the locality of the quantum energy in many materials.

**Standing assumptions.** The energy is a sum of local contributions, so any interaction beyond $R_c$ is missing unless a separate term adds it. The model is only as good as its reference method and its training set.

```pseudo id=main
BP-ENERGY-FORCES(r_1..r_N, network N, radial functions g_1..g_M, R_c)
L1  G_i^μ ← 0 for each atom i and each μ
L2  for each pair i < j with r = |r_ij| < R_c: for each μ: G_i^μ ← G_i^μ + g_μ(r); G_j^μ ← G_j^μ + g_μ(r)
L3  for each atom i: E_i ← N(G_i); a_i ← ∂N/∂G at G_i        ▷ by backpropagation
L4  U ← Σ_i E_i
L5  for each pair i < j with r < R_c:
L6      g ← Σ_μ (a_i^μ + a_j^μ) g_μ'(r)                     ▷ dU/dr for this pair
L7      F_i ← F_i - g r_ij / r; F_j ← F_j + g r_ij / r
L8  return U, (E_i), F
```

The pseudocode and the implementation use radial functions only, as a small toy of the model with given weights; a real potential adds the angular functions, whose forces involve triples, and is trained on quantum data. The structure of the force loop is the same as for the [embedded atom method](/embedded-atom-method/), with the vector $G_i$ in place of the scalar density.

## What it counts

The model gives the energy $U$ and the forces for any configuration of the elements it was trained on, and through [molecular dynamics](/molecular-dynamics/) and Monte Carlo, the properties that follow from them: phase diagrams, melting, defects, diffusion, and reactions that break and form bonds, which a [molecular mechanics force field](/molecular-mechanics-force-field/) cannot describe. The atomic energies $E_i$ themselves are not measurable quantities; only their sum is fitted.

**Cost.** At fixed density each atom has a bounded number of neighbors, so computing all $G_i$, all networks and all forces costs $O(N)$ (more precisely $O(N K^2)$ with $K$ neighbors per atom, because of the angular functions). Per atom this is much more than for a pair potential or EAM, and much less than for density functional theory, whose cost grows about as $N^3$ in standard implementations. This gap is what makes it worth fitting the model.

## Relation to other models

- **[Born-Oppenheimer molecular dynamics](/born-oppenheimer-molecular-dynamics/)** computes the same energy surface from the electrons at each step. The Behler-Parrinello potential is a fit of that surface.
- **[Embedded atom method](/embedded-atom-method/).** Also a sum of atomic energies that depend on the neighborhood, with $F(\sum_j f(R_{ij}))$ in place of a network of many symmetry functions. EAM has a few fitted functions; the network has thousands of weights and needs many more reference data.
- **Kernel methods.** Gaussian approximation potentials and related models use the same decomposition into atomic energies but fit each one by [Gaussian process](/gaussian-process/) regression or [kernel ridge regression](/kernel-ridge-regression/) on descriptors of the neighborhood.
- **Later generations.** Behler's review calls this model the second generation. The third generation adds long-range electrostatics with atomic charges that a second set of networks predicts, and the fourth adds charges that are equilibrated over the whole system, for cases where a charge transfer is not local. Message-passing neural networks learn the descriptors instead of fixing them.

## Known results in the model

**Hand computation of a radial function.** Take $R_c = 4$, $\eta = 0.5$, $R_s = 0$, and an atom with neighbors at distances 1 and 2. Then $f_c(1) = \tfrac12(\cos(\pi/4) + 1) = 0.853553$ and $f_c(2) = \tfrac12(\cos(\pi/2) + 1) = 0.5$, so
$$G = e^{-0.5} \cdot 0.853553 + e^{-2} \cdot 0.5 = 0.517706 + 0.067668 = 0.585374 .$$
With $\eta = 0$ the same neighbors give the smooth count $0.853553 + 0.5 = 1.353553$, less than 2 because the cutoff function weights far neighbors less. The tests check these numbers.

**Exact properties (theorems about the form).**

- **Invariance.** $U$ does not change under translations, rotations and exchanges of atoms of the same element, because each $G_i$ does not and every atom of an element uses the same network. The total force is zero.
- **Extensivity and locality.** Two copies of a system farther apart than $R_c$ have twice the energy of one, and $E_i$ does not change when an atom moves outside the cutoff sphere of atom $i$. The tests check both. The price is that interactions longer than $R_c$, such as Coulomb energies between distant charges, are absent.
- **Radial functions alone are incomplete.** An atom with two neighbors at distance 1 has the same radial functions whether the angle between them is $60°$ or $180°$, so a model with radial functions only gives both the same energy. The angular functions remove this case. Even with angles, a fixed finite set of symmetry functions does not separate every pair of different neighborhoods.
- **Approximation.** A network with one hidden layer and enough units can approximate any continuous function of $G_i$ on a bounded set to any accuracy (the universal approximation theorem). This says nothing about how many data or units are needed, and nothing about the error of the decomposition into atomic energies itself.

**Accuracy (measurements).** Behler and Parrinello fitted their 2007 silicon potential to density functional energies and compared its energies and structural properties with those of the reference method. Errors of later potentials are reported as root mean square errors of energy per atom and of force components on test sets held out from training. Such numbers hold only for configurations like the training set. Outside it, at a new pressure, a new phase or an unseen defect, the network extrapolates without warning, which is why training sets are built by repeated sampling of the configurations that the model itself visits.

## References
