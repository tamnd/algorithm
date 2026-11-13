---
tag: 1ZBXCP
kind: algorithm
slug: modeller
name: MODELLER
aliases:
- Modeller
area: biology/structure-prediction
level: advanced
summary: Builds a comparative model by turning template distances and angles into probability restraints on the target, then optimizing them with conjugate gradients and annealed molecular dynamics.
solves: [comparative-modeling]
model: real-ram
complexity:
  vars: {a: the number of aligned residues, r: the number of restraints, k: the number of evaluations of the objective}
  time: {worst: "O(a^2 + k r)"}
  space: {extra: "O(a + r)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 1993
  people: [Andrej Sali, Tom L. Blundell]
  note: Sali and Blundell described comparative protein modelling by satisfaction of spatial restraints in 1993; the method became the program MODELLER.
prereqs: [comparative-modeling, rmsd]
see_also: [loop-modeling, side-chain-packing, conjugate-gradient-method, simulated-annealing, molecular-dynamics, energy-function, gradient-descent, maximum-likelihood-estimation]
sources:
  - paper: doi:10.1006/jmbi.1993.1626
    title: Andrej Sali and Tom L. Blundell, Comparative protein modelling by satisfaction of spatial restraints, Journal of Molecular Biology 234(3), 1993, 779-815
    locator: the restraints as probability density functions, the molecular probability density, and its optimization by conjugate gradients and molecular dynamics with simulated annealing
  - paper: doi:10.1146/annurev.biophys.29.1.291
    title: Marc A. Marti-Renom, Ashley C. Stuart, Andras Fiser, Roberto Sanchez, Francisco Melo and Andrej Sali, Comparative protein structure modeling of genes and genomes, Annual Review of Biophysics and Biomolecular Structure 29, 2000, 291-325
    locator: the steps of comparative modeling and the description of modeling by satisfaction of spatial restraints
  - paper: doi:10.1110/ps.9.9.1753
    title: Andras Fiser, Richard Kinh Gian Do and Andrej Sali, Modeling of loops in protein structures, Protein Science 9(9), 2000, 1753-1773
    locator: the loop modeling method of MODELLER
  - paper: doi:10.1002/cpbi.3
    title: Benjamin Webb and Andrej Sali, Comparative protein structure modeling using MODELLER, Current Protocols in Bioinformatics 54, 2016
    locator: the protocol for building and assessing models with the program
---

MODELLER builds a [comparative model](/comparative-modeling/) of a target protein from an alignment with one or more template structures. It does not copy pieces of the template. Instead it reads distances and angles off the template, turns each of them into a probability density for the same feature of the target, and adds stereochemical restraints from a force field. Then it finds the coordinates that make all these restraints most probable, by minimizing the sum of their negative logarithms with conjugate gradients and molecular dynamics with simulated annealing (Sali and Blundell 1993).

## In plain words

Suppose we know the shape of one protein and want the shape of a related one. Where the two sequences line up, the distances between residues are probably about the same in both proteins. So we make a list of rules like "residue 5 and residue 40 should be about 8.1 Å apart". We also add rules that every protein obeys, such as the fixed length of the bonds.

Then we look for positions of all the atoms that obey the rules as well as possible. We start from a rough guess and move the atoms downhill on a score that counts how badly the rules are broken. To avoid getting stuck in a bad spot, we also shake the atoms, first hard and then more gently, and go downhill again. So the rules from several templates and the rules of chemistry act at once.

## The problem

The input is a target sequence of $n$ residues, a template structure $T$, and an alignment $A$, a set of pairs $(i, k)$ that say "target residue $i$ is aligned to template residue $k$". The output is coordinates $x = (x_1, \ldots, x_n)$ for the target. A *restraint* is a probability density $p_\rho$ of a feature $f_\rho(x)$, for example a distance or a dihedral angle. MODELLER treats the restraints as independent, so the molecular probability density is their product, and it maximizes it by minimizing

$$F(x) = -\sum_{\rho \in R} \ln p_\rho\big(f_\rho(x)\big).$$

This page and its implementation use the core case: $C_\alpha$ atoms only and Gaussian distance restraints. A Gaussian restraint with mean $d_0$ and spread $\sigma$ on the distance $d_{ij}(x) = |x_i - x_j|$ contributes $\frac{1}{2}\big((d_{ij}(x) - d_0)/\sigma\big)^2$ to $F$, up to a constant. So

$$F(x) = \sum_{(i, j, d_0, \sigma) \in R} \frac{1}{2} \left( \frac{|x_i - x_j| - d_0}{\sigma} \right)^2.$$

The homology restraints take $d_0$ from the template distance of the aligned residues, and the chain restraints fix consecutive $C_\alpha$ atoms at $3.8$ Å. Costs are in the [real RAM](/real-ram/) model with square roots in $O(1)$.

## The algorithm

```pseudo id=main
MODELLER(T, A, n)                        ▷ template T, alignment A, target of n residues
L1  R ← ∅; for each two aligned pairs (i, k), (j, l) in A with i < j do
L2      if |T_k − T_l| ≤ cutoff and j ≠ i + 1 then
L3          R ← R ∪ {(i, j, |T_k − T_l|, σ)}             ▷ homology restraint
L4  for i ← 1 to n − 1 do R ← R ∪ {(i, i + 1, 3.8 Å, σ_c)}  ▷ stereochemical restraint
L5  x ← the template positions for aligned residues, the others next to a chain neighbour
L6  x ← CONJUGATE-GRADIENTS(F_R, x)
L7  x ← MOLECULAR-DYNAMICS(F_R, x) at a falling temperature    ▷ simulated annealing
L8  x ← CONJUGATE-GRADIENTS(F_R, x)
L9  return x
```

The gradient of one restraint term with respect to $x_i$ is $\frac{d_{ij} - d_0}{\sigma^2} \cdot \frac{x_i - x_j}{d_{ij}}$, and the opposite vector for $x_j$. [Conjugate gradients](/conjugate-gradient-method/) use these gradients with the Polak-Ribiere update and a line search. Molecular dynamics treats $F$ as a potential energy: the atoms move by Newton's law under the force $-\nabla F$, with random velocities at each temperature, and the temperature falls stage by stage as in [simulated annealing](/simulated-annealing/). The real program uses all heavy atoms, restraints on dihedral angles from the template and from statistics of known structures, nonbonded terms from the CHARMM force field, and a *variable target function*: the first passes of conjugate gradients include only restraints between residues close in sequence, and later passes add the longer ones.

## Example

Let the template have four $C_\alpha$ atoms at the corners of a square of side $3.8$ Å, $T_1 = (0, 0, 0)$, $T_2 = (3.8, 0, 0)$, $T_3 = (3.8, 3.8, 0)$, $T_4 = (0, 3.8, 0)$, so the diagonals are $3.8\sqrt{2} \approx 5.37$ Å. The target has five residues, and residue 3 is an insertion:

```text
target    1 2 3 4 5
template  1 2 - 3 4
```

The aligned pairs are $(1, 1), (2, 2), (4, 3), (5, 4)$. Lines L1 to L3 give one homology restraint per pair of aligned target residues that are not chain neighbours: $(1, 4)$ with $d_0 = |T_1 - T_3| = 5.37$, $(1, 5)$ with $3.8$, $(2, 4)$ with $3.8$ and $(2, 5)$ with $5.37$. The pairs $(1, 2)$ and $(4, 5)$ are neighbours, so line L4 covers them, together with $(2, 3)$ and $(3, 4)$.

Line L5 copies residues 1, 2, 4, 5 from the template, which satisfies all their restraints exactly. Residue 3 must be at $3.8$ Å from both $x_2 = (3.8, 0, 0)$ and $x_4 = (3.8, 3.8, 0)$. Those two atoms are $3.8$ Å apart, so the set of exact positions is a circle around the midpoint $(3.8, 1.9, 0)$, of radius $\sqrt{3.8^2 - 1.9^2} \approx 3.29$ Å, in the plane $y = 1.9$. A bad start at the midpoint itself has two chain distances of $1.9$ Å; with $\sigma_c = 0.1$ Å this costs $2 \cdot \frac{1}{2}\big((1.9 - 3.8)/0.1\big)^2 = 361$. By symmetry the force on residue 3 is zero there, but the forces on residues 2 and 4 are not. From this start, conjugate gradients in the implementation reach $F < 10^{-13}$: residues 2 and 4 move a little, residue 3 moves out of the midpoint, and all four chain distances end at $3.8$ Å. With residues 1, 2, 4, 5 at the template, any point of the circle has $F = 0$, so the restraints do not choose one of them; the real program breaks such ties with nonbonded and dihedral terms, which keep the inserted residue away from the rest of the protein.

## Correctness

MODELLER is a heuristic optimizer, so its correctness is about what it optimizes and what it can guarantee.

- **The objective is the right one.** $F$ is the negative logarithm of the product of the restraint densities, plus a constant. A minimum of $F$ is a maximum of the molecular probability density, the most probable structure under the independence assumption.
- **The template is a global minimum when it fits.** If every target residue is aligned and the restraints come from the template, then $F \ge 0$, and $F = 0$ at the template, at each rigid motion of it, and at each mirror image; these are the only zeros when the restrained distances fix the shape. Any structure with $F = 0$ reproduces all restrained template distances.
- **Each minimization step decreases $F$.** The line search accepts a step only if $F$ drops by at least a fixed fraction of the predicted decrease. Since $F \ge 0$, the values of $F$ in conjugate gradients converge.
- **No global guarantee.** $F$ is not convex, so conjugate gradients can stop at a local minimum. The annealing stage is there to escape such minima, but it gives no certificate. The proof file below gives the full arguments for the first three points.

## Complexity

Lines L1 to L3 test each pair of aligned residues once, in $O(a^2)$ time for $a$ aligned residues. With a distance cutoff, each residue has $O(1)$ neighbours within the cutoff in a compact protein, so the number of restraints $r$ is $O(a + n)$ in practice and $O(a^2 + n)$ in the worst case. One evaluation of $F$ and its gradient costs $O(r)$. If the minimizations and the dynamics together evaluate $F$ $k$ times, the total time is $O(a^2 + k r)$ and the extra space is $O(a + r)$. The count $k$ depends on the schedule and on the convergence of the minimizer; there is no bound on it in terms of $n$.

## Properties

- **Not deterministic.** The start positions of unaligned residues and the velocities of the dynamics are random, so runs differ. Practice is to build several models and pick the best by a score.
- **Not exact.** The result is a local minimum of $F$, with no proof that it is the global one.
- **Many templates at once.** Restraints from several templates combine into one density, for example a mixture of Gaussians for one distance, so the model can follow different templates in different regions.
- **Blind to the hand.** Distances are the same in a structure and its mirror image. Dihedral restraints, which change sign under reflection, fix the hand in the real program.

## Variants and improvements

- **Loop refinement.** Fiser, Do and Sali (2000) model loops by optimizing a statistical potential with the same machinery ([loop modeling](/loop-modeling/)).
- **Restraints from other data.** Distance restraints from cross-links, NMR or predicted contacts enter $F$ as more terms.
- **Assessment.** The program scores models with statistical potentials, so the best of several runs can be kept.
- **Side chains.** In the real program side-chain atoms are part of the restraints. A separate [side-chain packing](/side-chain-packing/) step is another choice.

## When to use it

Use MODELLER when you have an alignment with one or more templates of known structure and want a full-atom model that respects stereochemistry. It is at its best at medium to high sequence identity, where the alignment is reliable. At low identity the alignment, not the optimizer, limits the model, and [fold recognition](/protein-fold-recognition/) or deep learning methods such as [AlphaFold](/alphafold/) are the better tools.

## Pitfalls

- **A wrong alignment gives wrong restraints.** A shift of the alignment by one residue makes every restraint of that region wrong, and the optimizer satisfies them faithfully.
- **Distance-only restraints and the mirror image.** A model built from distances alone can come out as the mirror image of the template, with left-handed helices. Use angle or dihedral restraints, or check the hand.
- **Stiff restraints slow the minimizer.** A small $\sigma$ for bonds next to a large $\sigma$ for long distances makes $F$ ill-conditioned. The variable target function and careful step control help.
- **One model is not enough.** A single run can stop in a poor local minimum. Build several models and compare their scores.

## Implementations

## History

Andrej Sali and Tom Blundell described comparative modelling by satisfaction of spatial restraints in 1993. The method turned the template into probability density functions for features of the target and optimized their product, an idea that differed from the earlier assembly of rigid template fragments. It became the program MODELLER, which added loop modeling (Fiser, Do and Sali 2000) and model assessment and stayed one of the most used tools for comparative modeling.

## References
