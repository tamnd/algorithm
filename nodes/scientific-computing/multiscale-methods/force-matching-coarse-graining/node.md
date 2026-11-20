---
tag: 3CW63P
kind: algorithm
slug: force-matching-coarse-graining
name: Multiscale coarse-graining by force matching
aliases:
- MS-CG
- force matching
area: scientific-computing/multiscale-methods
level: advanced
summary: Fits coarse-grained forces by least squares to the forces mapped from atomistic simulations onto the coarse sites.
model: real-ram
complexity:
  vars: {T: the number of configurations, N: the number of coarse sites, K: the number of basis functions}
  time: {worst: O(T (N^2 + N K^2) + K^3)}
  space: {extra: O(K^2 + N K)}
properties: {deterministic: true, randomized: false, exact: true, iterative: false}
history:
  year: 2005
  people: [Sergei Izvekov, Gregory A. Voth]
  note: Ercolessi and Adams fitted interatomic potentials to first-principles forces in 1994. Izvekov and Voth used the same least squares fit in 2005 to build coarse-grained models from atomistic runs, and Noid and coworkers gave the statistical mechanics of the method in 2008.
prereqs: [least-squares-problem, molecular-dynamics]
see_also: [iterative-boltzmann-inversion, mori-zwanzig-formalism, dissipative-particle-dynamics, radial-distribution-function, interatomic-potential, embedded-atom-method, tikhonov-regularization, canonical-ensemble]
sources:
  - paper: doi:10.1209/0295-5075/26/8/005
    title: "Furio Ercolessi and James B. Adams, Interatomic potentials from first-principles calculations: the force-matching method, Europhysics Letters 26(8), 1994, 583-588"
    locator: the fit of a potential to forces from first-principles calculations by least squares
  - paper: doi:10.1021/jp044629q
    title: Sergei Izvekov and Gregory A. Voth, A multiscale coarse-graining method for biomolecular systems, The Journal of Physical Chemistry B 109(7), 2005, 2469-2473
    locator: the force matching of coarse-grained sites to mapped atomistic forces
  - paper: doi:10.1063/1.2038787
    title: Sergei Izvekov and Gregory A. Voth, Multiscale coarse graining of liquid-state systems, The Journal of Chemical Physics 123(13), 2005, 134105
    locator: the method for liquids, with the pair force expanded in a basis and fitted by least squares
  - paper: doi:10.1063/1.2938860
    title: "W. G. Noid, Jhih-Wei Chu, Gary S. Ayton, Vinod Krishna, Sergei Izvekov, Gregory A. Voth, Avisek Das and Hans C. Andersen, The multiscale coarse-graining method. I. A rigorous bridge between atomistic and coarse-grained models, The Journal of Chemical Physics 128(24), 2008, 244114"
    locator: the consistency conditions on the map, and the result that force matching approximates the gradient of the many-body potential of mean force
---

Multiscale coarse-graining by force matching (MS-CG) builds a force field for coarse-grained sites, each of which stands for a group of atoms. It runs an atomistic simulation, maps each saved configuration onto the sites, adds up the atomistic forces on the atoms of each site, and then chooses the coarse-grained force field that reproduces these mapped forces best in the least squares sense. With a force field that is linear in its parameters, for example a pair force tabulated on a grid, this is one linear least squares problem. It differs from [iterative Boltzmann inversion](/iterative-boltzmann-inversion/), which matches a structural target and needs a new simulation in every iteration: force matching uses the forces and needs no coarse-grained simulation at all. The [Mori-Zwanzig formalism](/mori-zwanzig-formalism/) explains what both methods leave out: the memory and the noise of the removed atoms.

## In plain words

You have a detailed simulation in which every atom is tracked. You want a simpler model in which each small group of atoms is one ball. Take many snapshots of the detailed run. In each snapshot, put a ball at the center of each group, and add up the forces on the atoms of the group to get the force on the ball.

Now choose a rule for the force between two balls, as a table of numbers against distance. For any table, you can compute the forces that the balls would feel in each snapshot. Pick the table that makes these forces as close as possible to the forces from the detailed run, summed over all balls and all snapshots. Because the forces depend on the table in a simple way, this is a standard fitting problem with one answer.

## The problem

The input is a set of $T$ coarse-grained configurations $R^{(t)}$ of $N$ sites, with site positions $x_i$ in a periodic box, and the reference forces $F^{(t)}_i$ on the sites. The configurations come from an equilibrium atomistic run in the [canonical ensemble](/canonical-ensemble/), mapped onto the sites; for the center of mass map, where each atom belongs to one site, the reference force on a site is the sum of the atomistic forces on its atoms. The model is a pair force $f(r)$ between sites, with $f > 0$ for repulsion, so the coarse-grained force on site $i$ is

$$F_i(R) = \sum_{j \ne i} f(r_{ij})\, e_{ij}, \qquad e_{ij} = \frac{x_i - x_j}{r_{ij}},$$

with the minimum image. The pair force is a combination $f(r) = \sum_{k=1}^K c_k \phi_k(r)$ of $K$ basis functions; here they are hat functions on a uniform grid $r_0 < \dots < r_{K-1} = r_c$, so $c_k$ is the value of $f$ at the node $r_k$ and $f$ is piecewise linear and zero beyond the cutoff $r_c$. The output is the coefficient vector $c$ that minimizes

$$\chi^2(c) = \sum_{t=1}^T \sum_{i=1}^N \lVert F_i(R^{(t)}; c) - F^{(t)}_i \rVert^2 .$$

The pair potential follows as $V(r) = \int_r^{r_c} f(s)\, ds$. Each component of $F_i$ is linear in $c$, so $\chi^2(c) = \lVert A c - F \rVert^2$ for a design matrix $A$ with one row per site, component and configuration, and a vector $F$ of the reference forces. This is a [least squares problem](/least-squares-problem/).

## The algorithm

```pseudo id=main
FORCE-MATCHING(configurations R^(t), reference forces F^(t), basis φ_1..φ_K)
L1  G ← 0 (K by K), b ← 0 (length K)
L2  for each configuration t
L3      build the rows a of A for all sites and components: a_k = Σ_{j≠i} φ_k(r_ij) (e_ij)_α
L4      for each row a with its reference force f
L5          G ← G + a aᵀ, b ← b + a f
L6  set G_pp ← 1 for every p with G_pp = 0     ▷ a basis function that no distance touches gets c_p = 0
L7  return c = G⁻¹ b                            ▷ the normal equations Gc = b
```

Line L3 visits each pair of sites once and adds $\phi_k(r_{ij}) e_{ij}$ to the row of site $i$ and the negative to the row of site $j$; a hat function is nonzero at only two nodes, so each pair touches two columns. Lines L4 and L5 form the normal equations $A^T A c = A^T F$ without storing $A$, so the memory does not grow with $T$. Line L7 solves the $K$ by $K$ system; the implementation uses Gaussian elimination with partial pivoting from the shared dense helper. A [Cholesky decomposition](/cholesky-decomposition/) also works, since $G$ is symmetric positive definite once the unused functions are removed, and a QR factorization of $A$ is better conditioned when $A$ is small enough to store.

## Example

**By hand.** Take two hat functions on $[1, 2]$: $\phi_1(r) = 2 - r$ and $\phi_2(r) = r - 1$, so $f(1) = c_1$ and $f(2) = c_2$. Three configurations each have two sites on the $x$ axis, at distances $1.25$, $1.75$ and $1.5$, and the reference force on the right site is $1.0$, $0.2$ and $0.5$ (repulsive), with the opposite force on the left site. All values are in reduced units. The three rows for the right site are $(0.75, 0.25)$, $(0.25, 0.75)$ and $(0.5, 0.5)$; the left site gives the same rows and forces with the opposite sign, which doubles $G$ and $b$ and does not change $c$. Without the doubling,

$$G = \begin{pmatrix} 0.875 & 0.625 \\ 0.625 & 0.875 \end{pmatrix}, \qquad b = \begin{pmatrix} 1.05 \\ 0.65 \end{pmatrix}, \qquad c = \begin{pmatrix} 41/30 \\ -7/30 \end{pmatrix} = \begin{pmatrix} 1.366667 \\ -0.233333 \end{pmatrix}.$$

The fitted forces at the three distances are $0.966667$, $0.166667$ and $0.566667$, so the residuals are $-1/30$, $-1/30$ and $2/30$, and $\chi^2 = 2 \cdot 6 / 900 = 0.013333$ with both sites. The three data points do not lie on one line, so no $c$ fits them exactly; the least squares line passes below the first two points and above the third. The potential at $r = 1$ is $V(1) = (c_1 + c_2) / 2 = 17/30$.

**Grid refinement.** In the tests, the reference forces come from the smooth pair force $f^*(r) = 3 \cos(3 r) (2.5 - r)$ with $r_c = 2.5$, on 20 configurations of 20 sites in a periodic square of side 6, with no pair closer than $0.85$. The largest error $\max_k |c_k - f^*(r_k)|$ at the nodes is $0.416$, $0.115$, $0.0254$ and $0.00766$ for $K = 6$, $11$, $21$ and $41$ hat functions on $[0.85, 2.5]$: each halving of the grid spacing divides the error by $3.3$ to $4.5$, which is second order, as for the best piecewise linear fit of a smooth function. These are measurements on one data set.

**Noise.** If the reference forces are a force of the basis plus independent Gaussian noise of standard deviation $1$ on each component, the error $\lVert c - c^* \rVert_2$ with $K = 11$ is $0.639$, $0.245$ and $0.134$ for $T = 5$, $20$ and $80$ configurations. It falls about like $T^{-1/2}$. This is the case of real data: the mapped force has a part that the site positions do not determine, and only its mean is fitted.

## Correctness

The proof in the proofs file shows that line L3 builds rows with $a \cdot c = F_{i \alpha}(R; c)$, that lines L4 and L5 give $G = A^T A$ and $b = A^T F$, and that $c$ minimizes $\chi^2$ if and only if $G c = b$, because $\chi^2$ is a convex quadratic with gradient $2 (G c - b)$. A basis function that no distance touches gives a zero row and column, and line L6 sets its coefficient to zero without changing the other equations. If the used columns of $A$ are independent, the minimizer is unique; if the reference forces come from a pair force in the basis, it is that force.

The proof also shows what the fit approximates. If the configurations are samples of a random configuration $R$ and $\bar F(R)$ is the conditional mean of the reference force given $R$, the expected residual splits as $\mathbb{E} \lVert A c - F \rVert^2 = \mathbb{E} \lVert F - \bar F \rVert^2 + \mathbb{E} \lVert A c - \bar F \rVert^2$. So the fit is the least squares projection of $\bar F$ onto the pair forces of the basis. Noid et al. (2008) show that, under their consistency conditions on the map, $\bar F(R)$ is the force $-\nabla_R W(R)$ of the many-body potential of mean force $W$; the proofs file takes this from the paper and does not prove it.

## Complexity

In the [real RAM](/real-ram/) model, line L3 costs $O(N^2)$ per configuration with a loop over all pairs, or $O(N)$ at fixed density with a [linked cell list](/linked-cell-list/). Line L5 costs $O(K^2)$ per row in the worst case, because a row has up to $K$ nonzero entries when a site has neighbors at all distances; there are $2N$ rows per configuration in two dimensions. Line L7 costs $O(K^3)$. The total is $O(T (N^2 + N K^2) + K^3)$, with $O(K^2)$ memory for $G$ and $O(N K)$ for the rows of one configuration. The atomistic simulation that produces the data is not counted, and it costs much more than the fit.

## Properties

- **One linear solve.** For a force field linear in its parameters, the fit is a single least squares problem. There is no iteration and no coarse-grained simulation (theorem: the normal equations give the minimizer).
- **Many-body projection.** The fit is the projection of the many-body mean force onto the chosen basis (theorem, under the consistency conditions of Noid et al. 2008). With only pair forces in the basis, the many-body part of the mean force is lost, and the fitted pair force is the best pair approximation in the force norm, not the potential of mean force between two sites.
- **Structure is not matched.** A force field with the best force residual need not give the right [radial distribution function](/radial-distribution-function/); the error depends on how much of the mean force the basis can represent.
- **State dependence.** The mean force is a free energy gradient, so the fitted force depends on the temperature and the density of the atomistic run.
- **No dynamics.** Force matching fits the conservative part of the coarse-grained force. The friction and the noise of the removed atoms are not fitted.

## Variants and improvements

- **Bonded terms.** Bonds, angles and dihedrals between sites get their own basis functions; the problem stays linear in the coefficients.
- **Regularization.** When $G$ is ill conditioned, for example at distances with few samples, add a penalty $\lambda \lVert c \rVert^2$ or a smoothness penalty ([Tikhonov regularization](/tikhonov-regularization/)), or remove the functions with too few samples. The weight $\lambda$ is a choice.
- **Block averaging.** Solve the normal equations per block of configurations and average the solutions, which also gives an error bar.
- **Nonlinear models.** For an [embedded atom](/embedded-atom-method/) model or a neural network potential, $\chi^2$ is not quadratic and needs an iterative optimizer. This is the form of Ercolessi and Adams (1994), who fitted interatomic potentials to forces from first-principles calculations.
- **Structural and relative entropy methods.** [Iterative Boltzmann inversion](/iterative-boltzmann-inversion/) matches $g(r)$, and relative entropy methods minimize the Kullback-Leibler divergence between the mapped and the coarse-grained distributions. These need coarse-grained simulations but match the structure better when the basis is too small.

## When to use it

Use force matching when the atomistic forces are available and the coarse-grained force field is linear in its parameters, because then one solve gives the answer, and the result does not depend on a starting guess or a convergence criterion. Use [iterative Boltzmann inversion](/iterative-boltzmann-inversion/) when the structure must match closely and a small pair basis cannot represent the mean force. For the dynamics of the coarse model, add friction and noise, as in [dissipative particle dynamics](/dissipative-particle-dynamics/).

## Pitfalls

- **The direction of the pair term.** Writing the site force as $F_i = \sum_j f(r_{ij}) (x_j - x_i) / r_{ij}$ while the reference uses $f > 0$ for repulsion fits $-f$ and gives an attraction where the atoms repel. Use one convention in both: $F_i = \sum_j f(r_{ij}) (x_i - x_j) / r_{ij}$ with $f > 0$ for repulsion.
- **Unsampled distances.** Hat functions below the closest pair distance have no data, and $G$ is singular. Line L6 must set their coefficients to zero (or the grid must start at the smallest sampled distance); the potential there must be extrapolated as a repulsion before it is used.
- **The wrong mapped force.** The reference force on a site is the sum of the forces on its atoms for the center of mass map with each atom in one site. Using the force on the central atom only, or averaging instead of adding, gives a fit of the wrong quantity.
- **Constrained atoms.** With bond constraints in the atomistic run, the constraint forces are part of the force on the atoms. Leaving them out changes the mean force.
- **Reading the pair force as a potential of mean force.** With many-body effects, the fitted pair force is a projection, not $-dw/dr$ with $w = -k_B T \ln g$. The two agree only at low density.
- **Too fine a grid.** With few samples per hat function, noise dominates and the force oscillates. Refine the grid only while the error bars of the coefficients stay small.

## Implementations

## History

Ercolessi and Adams introduced force matching in 1994 to fit interatomic potentials to forces from first-principles calculations of many configurations. Izvekov and Voth turned it into a coarse-graining method in 2005: map an atomistic run onto sites and fit the site forces, first for biomolecular systems and then for liquids, with the pair force expanded in a basis. In 2008 Noid and coworkers gave the method a basis in statistical mechanics, with the consistency conditions on the map and the result that the fit approximates the gradient of the many-body potential of mean force. The method is known as multiscale coarse-graining (MS-CG).

## References
