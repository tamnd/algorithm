---
tag: 7F8PW8
kind: algorithm
slug: quasicontinuum-method
name: Quasicontinuum method
aliases:
- QC method
area: scientific-computing/multiscale-methods
level: advanced
summary: Keeps full atomistic detail near defects and a Cauchy-Born continuum elsewhere, with the positions of all atoms interpolated from a few representative atoms.
model: real-ram
complexity:
  vars: {N: the number of atoms, n: the number of representative atoms, I: the number of Newton iterations}
  time: {worst: O(I (N + n^3))}
  space: {extra: O(N + n^2)}
properties: {deterministic: true, randomized: false, exact: false, iterative: true}
history:
  year: 1996
  people: [Ellad B. Tadmor, Michael Ortiz, Rob Phillips]
  note: Tadmor, Ortiz and Phillips gave the method in 1996. Shenoy and coauthors gave the adaptive form with local and nonlocal representative atoms and a correction of the ghost forces in 1999.
prereqs: [cauchy-born-rule, finite-element-method, newton-raphson-method]
see_also: [interatomic-potential, embedded-atom-method, lennard-jones-potential, deformation-gradient, multiscale-modeling, heterogeneous-multiscale-method, fe2-method, peridynamics]
sources:
  - paper: doi:10.1080/01418619608243000
    title: Ellad B. Tadmor, Michael Ortiz and Rob Phillips, Quasicontinuum analysis of defects in solids, Philosophical Magazine A 73(6), 1996, 1529-1563
    locator: the representative atoms, the finite element interpolation of the atom positions and the Cauchy-Born energy of the elements
  - paper: doi:10.1016/S0022-5096(98)00051-9
    title: "V. B. Shenoy, R. Miller, E. B. Tadmor, D. Rodney, R. Phillips and M. Ortiz, An adaptive finite element approach to atomic-scale mechanics: the quasicontinuum method, Journal of the Mechanics and Physics of Solids 47(3), 1999, 611-642"
    locator: the local and nonlocal representative atoms, the ghost forces at the interface and their correction, and the adaptive mesh
  - paper: doi:10.1088/0965-0393/17/5/053001
    title: Ronald E. Miller and Ellad B. Tadmor, A unified framework and performance benchmark of fourteen multiscale atomistic/continuum coupling methods, Modelling and Simulation in Materials Science and Engineering 17(5), 2009, 053001
    locator: the energy-based and force-based couplings in one framework, and the benchmark of their errors and costs
  - paper: doi:10.1051/m2an:2007058
    title: Matthew Dobson and Mitchell Luskin, Analysis of a force-based quasicontinuum approximation, ESAIM Mathematical Modelling and Numerical Analysis 42(1), 2008, 113-139
    locator: the force-based coupling, which has no ghost forces and no energy
  - paper: doi:10.1017/S0962492913000068
    title: Mitchell Luskin and Christoph Ortner, Atomistic-to-continuum coupling, Acta Numerica 22, 2013, 397-508
    locator: the numerical analysis of the couplings, the consistency error of the energy-based coupling and the patch test
  - book: isbn:9780521856980
    title: "Ellad B. Tadmor and Ronald E. Miller, Modeling Materials: Continuum, Atomistic and Multiscale Techniques, Cambridge University Press, 2011"
    locator: chapter 12 (atomistic-continuum coupling, static methods)
---

The quasicontinuum (QC) method computes the equilibrium of a crystal with a defect, such as a crack tip, a dislocation core or a weak bond, at a fraction of the cost of full atomistics. It keeps every atom near the defect, where the strain changes from atom to atom. Far from the defect, where the strain is smooth, it keeps only a few representative atoms (repatoms) and interpolates the positions of all other atoms on a finite element mesh. The energy of the far region comes from the [Cauchy-Born rule](/cauchy-born-rule/): each element deforms uniformly, so its energy is the number of atoms in it times the energy per atom of the uniformly deformed lattice. The unknowns are the repatom positions, and the method minimizes the approximate energy (energy-based QC) or sets the approximate forces to zero (force-based QC). The difficulty is the interface between the two regions, where the energy-based form makes spurious ghost forces.

## In plain words

Think of a long chain of beads joined by springs, with one weak spring in the middle. Near the weak spring the beads move in a complex way, so you follow each bead. Far from it the beads only spread out evenly, so you follow one bead in four or one in ten and place the others evenly between them. For the far part you do not add the springs one by one. You take the energy of one bead in an evenly stretched chain and multiply by the number of beads.

The two descriptions meet at a border. If you only add up energies, the beads at the border feel small false forces, because the near part and the far part count the long springs across the border in different ways. These forces are the ghost forces. One fix is to balance the forces directly instead of the energy.

## The problem

The input is a crystal of $N$ atoms with reference sites $X_i$ and a potential energy $E(y)$ of the positions $y$ (here a pair potential $\varphi$ with a cutoff), boundary conditions, and a defect. The output is an approximation of the local minimizer $y^*$ of $E$, with about the same accuracy near the defect, but with only $n \ll N$ unknowns. The page uses a chain: atoms $0, \dots, N - 1$ at $X_i = i a$, nearest neighbor bonds $(i, i+1)$ and second neighbor bonds $(i, i+2)$, with energy

$$E(y) = \sum_{i} s_{i,i+1}\, \varphi(y_{i+1} - y_i) + \sum_i \varphi(y_{i+2} - y_i),$$

where $s_b$ is a scale factor of the bond ($s_b = 1$ except at the defect). The two atoms at each end are fixed at $y_i = \bar F a i$, which applies a mean stretch $\bar F$.

The QC method chooses a sorted set $R$ of repatoms with positions $z$, and a subset $A \subset R$ of nonlocal repatoms. The positions of all atoms follow by linear interpolation, $y = T z$: an atom $i$ between neighboring repatoms $p < i < q$ gets $y_i = ((q - i) z_p + (i - p) z_q) / (q - p)$. Each pair of neighboring repatoms forms an element $e = (p, q)$ with $n_e = q - p$ lattice spacings and the deformation gradient $F_e = (z_q - z_p) / (n_e a)$. The Cauchy-Born energy per atom is $W(F) = \varphi(F a) + \varphi(2 F a)$ for the chain with second neighbors.

The energy-based approximation is the sum of the energies of the atoms: half of each bond for a nonlocal atom, $W(F_e)$ for a local atom inside an element, and the mean of $W$ over the two elements for a local repatom. Collected bond by bond and element by element, this is

$$E_{\mathrm{QCE}}(z) = \sum_b c_b\, s_b\, \varphi(y_j - y_i) + \sum_e w_e\, W(F_e), \quad c_b = \tfrac12\, \#(b \cap A), \quad w_e = n_e - \tfrac12\, \#(e \cap A),$$

where $\#(b \cap A)$ is the number of ends of bond $b$ in $A$. Bonds with $c_b = 0$ drop out, and elements inside the atomistic region have $n_e = 1$ and $w_e = 0$.

## The algorithm

```pseudo id=main
QUASICONTINUUM(φ, R, A, z, fixed, tol)
L1  build T with y = T z: an atom between repatoms p < i < q gets y_i = ((q - i) z_p + (i - p) z_q) / (q - p)
L2  c_b ← (number of ends of bond b in A) / 2, w_e ← n_e - (number of ends of element e in A) / 2
L3  repeat
L4      y ← T z
L5      g ← T^T ∇_y Σ_b c_b s_b φ(y_j - y_i) + ∇_z Σ_e w_e W(F_e)         ▷ F_e = (z_q - z_p) / (n_e a)
L6      K ← the Hessian of the same energy, restricted to the free repatoms
L7      solve K δ = -g on the free repatoms
L8      z_free ← z_free + δ
L9  until max |g_free| < tol
L10 return z, y
```

Line L1 builds the interpolation, which is the finite element interpolation with linear elements in one dimension. Line L2 fixes the weights once. Lines L4 to L8 are a Newton iteration on $E_{\mathrm{QCE}}$. The gradient of line L5 has two parts: the bond forces of the atomistic part, pulled back to the repatoms by $T^{\mathsf T}$ (an interpolated atom passes its force to its two repatoms in the ratio of the weights), and the element forces $\pm w_e W'(F_e) / (n_e a)$ with $W'(F) = a \varphi'(F a) + 2 a \varphi'(2 F a)$. The Hessian of line L6 adds $c_b s_b \varphi''$ for each bond, pulled back by $T$ on both sides, and $w_e W''(F_e) / (n_e a)^2$ for each element. The fixed repatoms carry the boundary conditions.

The force-based form (QCF) changes lines L5 and L6. For a nonlocal repatom, the residual is minus the exact atomistic force $-\partial E / \partial y_i$ at $y = T z$, with all bonds of atom $i$. For a local repatom, it is the gradient of the pure local energy $\sum_e n_e W(F_e)$. These forces are not the gradient of any energy, so $K$ is the Jacobian of the residual and is not symmetric.

## Example

**Ghost forces by hand.** Take a long chain at the uniform state $y_i = i a$, with all atoms as repatoms, the atoms $i \le 0$ nonlocal and the atoms $i \ge 1$ local. Collect the terms of $E_{\mathrm{QCE}}$ by the function they contain. The nearest neighbor bond $(i, i+1)$ appears with weight $c_b + w_e$, which is $1$ for every $i$: $(1, 0)$ for $i \le -1$, $(\frac12, \frac12)$ for $i = 0$ and $(0, 1)$ for $i \ge 1$. So with nearest neighbors only, $E_{\mathrm{QCE}} = E$ and there are no ghost forces. The second neighbor terms do not match. The true bonds $\varphi(y_{i+2} - y_i)$ have the weights $c_i = 1$ for $i \le -2$, $\frac12$ for $i = -1$ and $0$, and $0$ for $i \ge 1$, while the elements add $w_i \varphi(2 (y_{i+1} - y_i))$ with $w_i = 0$ for $i \le -1$, $\frac12$ for $i = 0$ and $1$ for $i \ge 1$. At the uniform state the derivative of each term is $\pm \varphi'(2a)$, so the force on atom $k$ is

$$f_k = -\frac{\partial E_{\mathrm{QCE}}}{\partial y_k} = \varphi'(2a)\, \bigl(c_k - c_{k-2} + 2 w_k - 2 w_{k-1}\bigr).$$

This gives $f_{-1} = -\frac12 \varphi'(2a)$, $f_0 = \frac12 \varphi'(2a)$, $f_1 = \frac12 \varphi'(2a)$, $f_2 = -\frac12 \varphi'(2a)$, and $f_k = 0$ for all other $k$. For the Lennard-Jones potential $\varphi(r) = 4\epsilon ((\sigma / r)^{12} - (\sigma / r)^6)$ in reduced units, the chain with second neighbors has its equilibrium spacing at $\varphi'(a) + 2 \varphi'(2a) = 0$, which is $a = (2 (1 + 2^{-12}) / (1 + 2^{-6}))^{1/6} \sigma = 1.11961\, \sigma$. There $\varphi'(2a) = 0.083673\, \epsilon / \sigma$, so the ghost forces are $\pm 0.041837\, \epsilon / \sigma$ on the four atoms next to the interface, while the exact forces are zero. The force-based residual is zero at this state.

**A weak bond.** Take $N = 81$ Lennard-Jones atoms with $a = 1.11961\, \sigma$, the bond $(40, 41)$ scaled by $s = 0.5$, and the two end atoms on each side fixed at a mean stretch $\bar F = 1.02$. The full atomistic minimizer, by Newton's method on all 77 free atoms, has the energy $-80.947593\, \epsilon$ and opens the weak bond to $1.174750\, \sigma$, against a mean spacing of $1.142003\, \sigma$. For QC, the atoms 0 to 3, 32 to 49 and 77 to 80 are nonlocal, and the local region has a repatom at every fourth atom, which gives $n = 40$ repatoms in place of 81 atoms. From the uniformly stretched start, the free gradient of $E_{\mathrm{QCE}}$ falls in the Newton steps as

| step | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $\max \lvert g \rvert$ ($\epsilon / \sigma$) | $4.66 \times 10^{-1}$ | $9.76 \times 10^{-2}$ | $8.54 \times 10^{-3}$ | $8.67 \times 10^{-5}$ | $9.23 \times 10^{-9}$ | $6.5 \times 10^{-13}$ |

which is quadratic convergence. The QCE energy is $-80.947681\, \epsilon$. The largest error in the atom positions is $9.5 \times 10^{-4}\, \sigma$ for QCE, at atom 4, next to the interface near the fixed end, where the ghost forces act. QCF reaches the same residuals in the same number of steps, and its largest error is $2.2 \times 10^{-10}\, \sigma$. With a nonlocal region of only two atoms on each side of the weak bond (32 repatoms), the QCF error grows to $2.6 \times 10^{-8}\, \sigma$, because the strain field of the defect then reaches the local region. These numbers are measurements on this chain.

## Correctness

The proof in the proofs file has four parts. First, $E_{\mathrm{QCE}}$ with the weights of line L2 is exactly the sum of the atom energies defined above, by a count of the bonds and elements that each atom touches. Second, if every atom is a nonlocal repatom, $c_b = 1$ for every bond and $w_e = 0$ for every element, so QC is full atomistics. Third, the patch test: at a uniform state $y = F X$, the force-based residual is zero at every free repatom whose neighbors exist, because the atomistic forces cancel by symmetry and each local repatom gets $\pm W'(F) / a$ from its two elements. The energy-based form fails the patch test when the potential reaches beyond nearest neighbors, with the ghost forces of the example. Fourth, Newton's method converges to the minimizer of $E_{\mathrm{QCE}}$ (or to the zero of the QCF residual) quadratically from a start close enough, when $K$ is nonsingular there, which is the standard result for [Newton's method](/newton-raphson-method/). The proof does not bound the error of QC against full atomistics. Such bounds are theorems of the numerical analysis literature (see Luskin and Ortner 2013) under stability hypotheses.

## Complexity

In the [real RAM](/real-ram/) model, one iteration computes $y = T z$ in $O(N)$, the atomistic part in $O(|A|)$ (a bounded number of bonds per nonlocal atom), the element part in $O(n)$, and the Newton step. The implementation solves with dense Gaussian elimination, $O(n^3)$, so the cost is $O(I (N + n^3))$ for $I$ Newton steps. The Hessian couples only repatoms within the cutoff of each other, so in one dimension it is banded and a banded solve takes $O(n)$; in two and three dimensions sparse solvers apply as for finite elements. A production code never forms $y$ for all atoms: it needs only the positions of the atoms near the nonlocal repatoms, so the cost of an iteration scales with $n$ and not with $N$. The memory is $O(N + n^2)$ here and $O(n)$ with sparse storage.

## Properties

- **Exact limit.** With every atom a nonlocal repatom, QC is full atomistics (Correctness, part two).
- **Ghost forces (theorem, for this chain).** QCE has nonzero forces at the uniform state when the potential reaches beyond nearest neighbors. With nearest neighbors only, there are none.
- **Energy or forces.** QCE has an energy, a symmetric Hessian and a variational structure. QCF has no ghost forces but no energy, so a minimizer, a line search or an energy barrier is not defined for it, and its Jacobian is not symmetric.
- **Local errors.** In the example, the QCE error sits at the interface, not at the defect. The QCF error depends on the size of the nonlocal region around the defect.
- **Uniform elements.** Each element has one deformation gradient. The Cauchy-Born rule assumes a simple lattice; complex lattices need the inner shifts of the [Cauchy-Born](/cauchy-born-rule/) page.

## Variants and improvements

- **Ghost force correction.** Shenoy and coauthors (1999) compute the ghost forces at the reference state and add their negative as a fixed load. This removes the ghost forces at the reference state, but not at other states.
- **Force-based QC.** QCF zeroes the forces without an energy; Dobson and Luskin (2008) analyze it. It passes the patch test, as in the example.
- **Consistent energies.** Several energy-based couplings change the energy of the atoms near the interface so that the uniform state has no ghost forces. Miller and Tadmor (2009) compare fourteen coupling methods, energy-based and force-based, in one framework on one benchmark.
- **Adaptive meshes.** The mesh is refined to full atomistic resolution where the strain changes fast, for example ahead of a moving dislocation, and coarsened elsewhere.
- **Finite temperature and dynamics.** Extensions use free energies in place of the energy in the local region, or couple to molecular dynamics; see the chapters on dynamics in Tadmor and Miller (2011).

## When to use it

Use QC for a static or slowly loaded problem in a crystal with a few localized defects in a large region of smooth deformation: nanoindentation, a crack tip, the core of a dislocation, a grain boundary. Use full [molecular dynamics](/molecular-dynamics/) when the defects move fast or fill the volume, or when temperature matters. Use the [heterogeneous multiscale method](/heterogeneous-multiscale-method/) or the [FE2 method](/fe2-method/) when the continuum constitutive law itself is the unknown everywhere, not near one defect. Use [peridynamics](/peridynamics/) when many cracks grow and the fine scale is not a lattice.

## Pitfalls

- **Full weights on interface bonds.** If line L2 gives weight $1$ to every bond that touches $A$ and $w_e = n_e$ to every element, the bonds across the interface are counted twice. The right weights are $c_b = \frac12 \#(b \cap A)$ and $w_e = n_e - \frac12 \#(e \cap A)$, which give the sum of the atom energies.
- **A symmetric solver for QCF.** The QCF Jacobian is not symmetric, so Cholesky or conjugate gradients in line L7 can fail. Use an LU solve (Gaussian elimination with pivoting) or GMRES for QCF.
- **A nonlocal region that is too small.** The strain must be close to uniform in each local element. With two nonlocal atoms on each side of the weak bond, the QCF error in the example is a hundred times larger than with eight. Refine where the strain changes.
- **Error checks only at the defect.** The QCE error in the example is largest at an interface far from the defect. Compare with full atomistics over the whole chain on a small problem.
- **An interpolated atom in a nonlocal bond.** Bonds of nonlocal atoms that reach into a coarse element use interpolated positions. Refine the mesh to full resolution within one cutoff of the nonlocal region.
- **Large strains.** The local energy $W(F)$ loses convexity where the lattice becomes unstable, and the Cauchy-Born rule then fails; see the [Cauchy-Born rule](/cauchy-born-rule/).

## Implementations

## History

Tadmor, Ortiz and Phillips introduced the quasicontinuum method in 1996 for the analysis of defects in solids, with the finite element interpolation of atom positions and Cauchy-Born energies for the elements. Shenoy, Miller, Tadmor, Rodney, Phillips and Ortiz gave in 1999 the adaptive formulation with local and nonlocal repatoms, identified the ghost forces at the interface and proposed a correction by fixed forces. Over the next decade many coupling methods followed. Miller and Tadmor (2009) put fourteen of them in one framework and benchmark, and a numerical analysis of consistency and stability grew from work such as Dobson and Luskin (2008), reviewed by Luskin and Ortner (2013).

## References
