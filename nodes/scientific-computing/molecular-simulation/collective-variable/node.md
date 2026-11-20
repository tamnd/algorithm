---
tag: 9F91J7
kind: concept
slug: collective-variable
name: Collective variable
aliases:
- reaction coordinate
area: scientific-computing/molecular-simulation
level: core
summary: "A low-dimensional function of the atomic positions, such as a distance or torsion, used to describe a slow process and to bias or analyse it."
prereqs: [canonical-ensemble]
see_also: [metadynamics, umbrella-sampling, weighted-histogram-analysis-method, principal-component-analysis, diffusion-maps, string-method, transition-path-sampling, mori-zwanzig-formalism]
sources:
  - book: isbn:9781848162471
    title: Tony Lelièvre, Mathias Rousset and Gabriel Stoltz, Free Energy Computations, A Mathematical Perspective, Imperial College Press, 2010
    locator: the definition of the free energy associated with a reaction coordinate, the marginal density and the mean force
  - paper: doi:10.1073/pnas.202427399
    title: Alessandro Laio and Michele Parrinello, Escaping free-energy minima, Proceedings of the National Academy of Sciences of the USA 99(20), 2002, 12562-12566
    locator: the choice of a few collective variables that describe the slow process and the bias placed on them
  - paper: doi:10.1002/wcms.66
    title: Johannes Kästner, Umbrella sampling, Wiley Interdisciplinary Reviews, Computational Molecular Science 1(6), 2011, 932-942
    locator: the reaction coordinate along which the windows are placed and the free energy profile along it
  - book: isbn:9783540384472
    title: Christophe Chipot and Andrew Pohorille (eds.), Free Energy Calculations, Theory and Applications in Chemistry and Biology, Springer Series in Chemical Physics 86, Springer, 2007
    locator: the treatment of free energies along an order parameter and the methods that bias it
---

A collective variable (CV) is a function $s(x)$ that maps the $3N$ atomic coordinates $x$ of a system to a few numbers, such as a distance between two atoms, a torsion angle, a number of contacts or the distance from a reference structure. It is chosen so that its value tells apart the states of interest, for example bound and unbound, folded and unfolded, reactant and product, and so that it changes slowly while everything else changes fast. Free energy methods work with the CV: [umbrella sampling](/umbrella-sampling/) places windows along it, [metadynamics](/metadynamics/) puts its bias on it, and the [weighted histogram analysis method](/weighted-histogram-analysis-method/) builds the free energy profile along it. The term reaction coordinate is often used as a synonym; in a stricter sense it means a CV that describes the progress of a reaction exactly, such as the committor.

## In plain words

A protein has thousands of atoms, and each of them moves all the time. To talk about what the protein does, such as folding or opening, we need a few numbers that sum up its shape, like the distance between its two ends.

Such a number is a collective variable. A good one changes clearly when the important event happens, and changes slowly, while the many other motions just jiggle around it.

With a good collective variable, we can draw a curve of how likely each value is, and push the system along it to see rare events. With a bad one, the important motion stays hidden, and the curve can mislead.

## The idea

**The free energy along a CV.** Let $x \in \mathbb R^n$ have the [canonical](/canonical-ensemble/) density $e^{-\beta U(x)} / Z$ with $\beta = 1/(k_B T)$, and let $s : \mathbb R^n \to \mathbb R^d$ with $d$ small. The marginal density of $s$ is
$$p(z) = \frac{1}{Z} \int \delta(s(x) - z)\, e^{-\beta U(x)}\,dx,$$
and the free energy profile, or potential of mean force, is $F(z) = -k_B T \ln p(z)$, up to a constant. Differences $F(z_2) - F(z_1)$ give the relative probability of two values, and the minima of $F$ are the states as seen through $s$. Every bias that depends on $x$ only through $s(x)$ changes $p(z)$ by an explicit factor, $p_{\text{biased}}(z) \propto p(z)\, e^{-\beta w(z)}$, which is why biasing methods can remove the bias exactly.

**$F$ depends on the choice of variable, not only on the physics.** If $\tilde s = g(s)$ for a smooth increasing $g$ in one dimension, the densities are related by $\tilde p(g(z))\, g'(z) = p(z)$, so
$$\tilde F(g(z)) = F(z) + k_B T \ln g'(z).$$
So the depth of a minimum and the height of a barrier in $F$ depend on how the CV is parametrized; only quantities such as the probability of a state, an integral of $e^{-\beta F}$ over a region, do not. The same effect gives the volume terms of distances and angles: $F$ contains an entropy part that comes from the volume of the set $\{x : s(x) = z\}$, not from $U$.

**The mean force.** Where $s$ is smooth with $\nabla s \ne 0$, $F'(z)$ is a conditional average over the set $s(x) = z$ of a local quantity built from $\nabla U$, $\nabla s$ and the curvature of $s$ (the co-area formula; see Lelièvre, Rousset and Stoltz 2010). Constrained molecular dynamics at fixed $s$, as in the blue moon ensemble, and the adaptive biasing force method estimate this mean force and integrate it to get $F$.

**What makes a CV good.** A good CV (a) takes clearly different values in the states of interest, (b) is slow compared with all motions orthogonal to it, so that at fixed $s$ the rest of the system relaxes quickly, and (c) is smooth, so that its gradient gives a well-defined biasing force. Condition (b) is the hard one. In terms of dynamics, the best one-dimensional CV for a transition from $A$ to $B$ is the committor $q(x)$, the probability that a trajectory started at $x$ reaches $B$ before $A$: it is the ideal reaction coordinate, but it is not known in advance, and computing it needs methods such as [transition path sampling](/transition-path-sampling/).

**Common CVs.**
- Distances, angles and torsions between atoms or centres of mass. Torsions are periodic, and the bias and the histogram must use the period.
- Coordination numbers, smooth counts of the neighbours within a cutoff, for example $\sum_j (1 - (r_{ij}/r_0)^6) / (1 - (r_{ij}/r_0)^{12})$, used for bonds that break and form.
- The root mean square deviation from a reference structure, and the number of native contacts.
- Path CVs, which measure the progress along a path between two structures and the distance from it, close in spirit to the [string method](/string-method/).
- Learned CVs: the slowest modes found by [principal component analysis](/principal-component-analysis/), [diffusion maps](/diffusion-maps/) or other data analysis of trajectories.

## Examples

**The volume term of a distance.** Two particles in three dimensions with no interaction between them, in a large box. The relative vector has a uniform density, so the density of its length $r$ is proportional to the area $4\pi r^2$ of the sphere, and $F(r) = -2 k_B T \ln r + \text{const}$. So $F(2) - F(1) = -2 k_B T \ln 2 = -1.386\, k_B T$: a larger distance has a lower free energy with no force at all. For a real pair potential $u(r)$ the profile is $F(r) = u(r) - 2 k_B T \ln r + \text{const}$ at low density, and a bound state must be judged against this volume term.

**Changing the variable.** For the same pair, take $\tilde s = r^3$ instead of $r$. Then $g'(r) = 3r^2$, and $\tilde F(r^3) = F(r) + k_B T \ln(3 r^2) = \text{const}$: in the variable $r^3$ the profile is flat. The two profiles describe the same system; neither is wrong.

**A double well with $s = x$.** For $U(x) = 8(x^2 - 1)^2$ in one dimension with $s = x$, $F = U$ up to a constant, with a barrier of $8\, k_B T$. This is the test case of the [umbrella sampling](/umbrella-sampling/), WHAM and [metadynamics](/metadynamics/) pages, where the computed profiles are compared with $U$.

**A hidden slow motion.** Take $U(x, y) = 8(x^2 - 1)^2 + 8(y^2 - 1)^2$ in two dimensions and the CV $s = x$. The density is a product, so $F(x) = 8(x^2 - 1)^2$ up to a constant, exactly. But a biased run along $x$ does not help the motion in $y$, which has its own barrier of $8\, k_B T$: each window stays in the $y$-well where it started. In this separable case the profile along $x$ is still right, because the $y$-well does not change $F(x)$. If the two wells in $y$ had different shapes for different $x$, each window would report the free energy of its own $y$-well, and the profile would depend on where the windows started. This is the most common failure of CV-based methods, and it is invisible in the profile itself.

## Where it is used

- **Free energy profiles.** Umbrella sampling with WHAM or MBAR, thermodynamic integration of the mean force, and constrained dynamics all compute $F$ along a CV, for example the free energy of a ligand as a function of its distance from a binding site.
- **Enhanced sampling.** Metadynamics, adaptive biasing force and related methods put a time-dependent bias on the CVs to cross barriers.
- **Rare events and rates.** Transition path sampling, [forward flux sampling](/forward-flux-sampling/) and the string method use CVs or order parameters to define the states and to measure progress, and the committor tests whether a CV is a good reaction coordinate.
- **Coarse-grained dynamics.** The [Mori-Zwanzig formalism](/mori-zwanzig-formalism/) gives an exact equation for the dynamics of a CV, with memory and noise, and its Markovian limit is a Langevin equation on $F$.
- **Analysis of simulations.** Projecting a trajectory on a few CVs is the standard way to see states and transitions in high-dimensional data.

## References
