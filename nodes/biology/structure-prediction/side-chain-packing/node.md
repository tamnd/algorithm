---
tag: MMD1MC
kind: problem
slug: side-chain-packing
name: Side-chain packing
aliases:
- Rotamer packing
- Side-chain placement
- Side-chain positioning
area: biology/structure-prediction
level: advanced
summary: Choose a rotamer for each side chain on a fixed backbone so that a sum of self and pair energies is least. NP-hard in general; polynomial on graphs of bounded treewidth by tree decomposition.
prereqs: [rotamer, np-hard]
see_also: [dead-end-elimination, protein-design, comparative-modeling, variable-elimination, tree-decomposition, map-inference, three-coloring, binary-integer-programming]
sources:
  - paper: doi:10.1093/protein/15.10.779
    title: Niles A. Pierce and Erik Winfree, Protein design is NP-hard, Protein Engineering 15(10), 2002, 779-782
    locator: the NP-hardness of minimizing a pairwise energy over discrete rotamers on a fixed backbone
  - paper: doi:10.1002/prot.22488
    title: Georgii G. Krivov, Maxim V. Shapovalov and Roland L. Dunbrack Jr., Improved prediction of protein side-chain conformations with SCWRL4, Proteins 77(4), 2009, 778-795
    locator: the abstract (tree decomposition for the combinatorial problem, and the accuracy on 379 proteins)
  - paper: doi:10.1110/ps.03154503
    title: Adrian A. Canutescu, Andrew A. Shelenkov and Roland L. Dunbrack Jr., A graph-theory algorithm for rapid protein side-chain prediction, Protein Science 12(9), 2003, 2001-2014
    locator: the interaction graph, its connected and biconnected components (SCWRL3)
  - paper: doi:10.1007/11415770_32
    title: Jinbo Xu, Rapid protein side-chain packing via tree decomposition, RECOMB 2005, Lecture Notes in Computer Science 3500, 423-439
    locator: the tree decomposition algorithm and its cost in the treewidth
  - paper: doi:10.1093/bioinformatics/bti144
    title: Carleton L. Kingsford, Bernard Chazelle and Mona Singh, Solving and analyzing side-chain positioning problems using linear and integer programming, Bioinformatics 21(7), 2005, 1028-1039
    locator: the integer program for side-chain positioning and its linear relaxation
---

Side-chain packing is the problem of choosing one [rotamer](/rotamer/) for each side chain of a protein whose backbone is fixed, so that a sum of self energies and pairwise energies is least. It is the last step of most [comparative models](/comparative-modeling/) and the inner problem of [protein design](/protein-design/). With arbitrary pairwise energies it is [NP-hard](/np-hard/) (Pierce and Winfree 2002), but the interaction graph of a real protein is sparse, so exact methods based on [dead-end elimination](/dead-end-elimination/) and [tree decomposition](/tree-decomposition/) solve typical instances fast.

## In plain words

A protein has a backbone and, on each residue, a side chain that can point in a few standard ways. The backbone is given. For each side chain we must pick one of its standard shapes, so that the side chains fit together without bumping into each other and make good contacts.

Each shape has a cost on its own (how well it fits the backbone) and a cost with each neighbour shape (a clash costs a lot). The task is to pick one shape per side chain so that the total cost is lowest. Picking the best shape for each side chain alone does not work, because two good shapes can clash. The number of combinations grows very fast, so the methods use the fact that each side chain touches only a few others.

## Definition

**Model.** The backbone is a fixed full-atom structure of $n$ residues. Residue $i$ has a finite set $R_i$ of rotamers from a rotamer library, with $|R_i| \le p$. The energy is pairwise decomposable:

$$E(x) = \sum_{i=1}^{n} E_i(x_i) + \sum_{1 \le i < j \le n} E_{ij}(x_i, x_j), \qquad x \in R_1 \times \cdots \times R_n.$$

$E_i(r)$ holds the interaction of rotamer $r$ with the backbone (and often $-\ln$ of its library probability), and $E_{ij}(r, s)$ the interaction of two side chains. The *interaction graph* has the residues as vertices and an edge $\{i, j\}$ when $E_{ij}$ is not identically zero. Costs below are in the [real RAM](/real-ram/) model, with one step per energy lookup or addition.

**Problem.** Given $R_1, \ldots, R_n$, $E_i$ and $E_{ij}$, find an assignment $x^*$ of least energy, the global minimum energy conformation (GMEC).

**Decision version.** Given also a number $K$, decide whether some $x$ has $E(x) \le K$.

The quality of a packing on a real protein is measured against the crystal structure, often as the fraction of residues whose angle $\chi_1$ (or $\chi_1$ and $\chi_2$) is within $40°$ of the observed angle. That measure depends on the energy, not only on the optimizer.

## Variants

- **Continuous packing.** The angles $\chi$ are real numbers, not library values. Methods sample extra rotamers around each library value or minimize locally after the discrete search.
- **Design.** $R_i$ holds rotamers of several amino acid types, so the packing also chooses the sequence. This is [protein design](/protein-design/) on a fixed backbone; the combinatorial problem has the same form.
- **Flexible backbone.** The backbone may move a little. The energy is then no longer a fixed table, and the problem leaves this definition.
- **Suboptimal packings.** List all assignments within an energy gap of the GMEC, for example for ensembles.

## Examples

**A chain of three residues.** Each of residues 1, 2, 3 has two rotamers, a and b. The self energies are $E_1 = (0, 2)$, $E_2 = (1, 0)$, $E_3 = (0, 1)$. The pair energies are $E_{12}(a, b) = 3$ and $E_{23}(b, a) = 2$, and all other pair energies are 0. The eight energies are:

| $x$ | aaa | aab | aba | abb | baa | bab | bba | bbb |
|---|---|---|---|---|---|---|---|---|
| $E(x)$ | 1 | 2 | 5 | 4 | 3 | 4 | 4 | 3 |

The GMEC is aaa with energy 1. The greedy choice of the best self energy at each residue gives aba, with energy 5, because rotamer b of residue 2 clashes with both neighbours.

The interaction graph is a path, so variable elimination solves it exactly. Eliminate residue 1: $m_1(x_2) = \min_r [E_1(r) + E_{12}(r, x_2)]$ gives $m_1(a) = 0$ and $m_1(b) = 2$. Eliminate residue 2: $m_2(x_3) = \min_s [E_2(s) + m_1(s) + E_{23}(s, x_3)]$ gives $m_2(a) = \min(1, 4) = 1$ and $m_2(b) = \min(1, 2) = 1$, both with $s = a$. Eliminate residue 3: $\min(0 + 1, 1 + 1) = 1$ with $x_3 = a$. Going back gives $x_2 = a$ and $x_1 = a$.

**A non-example of easy structure.** The interaction graph of a protein with $n$ residues and a contact cutoff of about 10 Å has about $n$ times a small constant edges, not $n^2/2$. A random dense instance with the same $n$ is much harder than any protein of that size, so a benchmark on random dense instances says little about protein packing.

## Known algorithms

- **Brute force.** Try all $\prod_i |R_i| \le p^n$ assignments, in $O(n^2 p^n)$ time. It is the reference for tests.
- **[Dead-end elimination](/dead-end-elimination/)** (Desmet et al. 1992, Goldstein 1994). Remove rotamers that provably cannot be in any GMEC, then search the rest exactly. It has no polynomial bound.
- **Graph decomposition.** Split the interaction graph into connected components, then into biconnected components, and solve each part with the separating residues fixed (SCWRL3, Canutescu, Shelenkov and Dunbrack 2003). SCWRL4 (Krivov, Shapovalov and Dunbrack 2009) uses a tree decomposition for the combinatorial step.
- **Tree decomposition dynamic programming** (Xu 2005). With a tree decomposition of width $w$, a dynamic program over the bags finds the GMEC in $O(n p^{w+1})$ time. [Variable elimination](/variable-elimination/) along an order of induced width $w$ has the same cost and is the method of the implementation of this page.
- **Integer programming** (Kingsford, Chazelle and Singh 2005). One 0/1 variable per rotamer and one per pair of rotamers, with constraints that pick one rotamer per residue and tie the pair variables to them. Kingsford et al. found that the linear relaxation is often integral on their protein instances, so a linear program then gives a certified optimum.
- **Heuristics.** Monte Carlo with [simulated annealing](/simulated-annealing/) over rotamer swaps, as in Rosetta, and message passing for [MAP inference](/map-inference/). They are fast and flexible but give no certificate of optimality.

## Bounds

**Theorem.** The decision version is NP-complete, already with $p = 3$, self energies 0 and pair energies in $\{0, 1\}$.

*Proof.* The problem is in NP: an assignment is a certificate, and its energy takes $O(n^2)$ additions. For hardness, reduce from [graph 3-coloring](/three-coloring/). Given a graph $G = (V, F)$, make one residue per vertex with three rotamers, the colours. Set $E_i = 0$, and for each edge $\{i, j\} \in F$ set $E_{ij}(r, s) = 1$ if $r = s$ and 0 otherwise. Then $E(x)$ is the number of edges whose two ends get the same colour, so $E(x) \le 0$ for some $x$ if and only if $G$ has a proper 3-coloring. The construction takes polynomial time. $\square$

Pierce and Winfree (2002) proved NP-hardness for the same minimization in its protein design form, with an arbitrary rigid backbone, rotamer library and pairwise energy. On the upper side, given a tree decomposition of width $w$ of the interaction graph, the problem is solvable in $O(n p^{w+1})$ time. So it is polynomial for interaction graphs of bounded [treewidth](/treewidth/), and in $O(n p^2)$ time on trees ($w = 1$). No method can be expected to avoid exponential time on all instances unless P = NP.

The accuracy numbers of the tools are measurements, not bounds. Krivov et al. (2009) report that SCWRL4 predicts 86% of $\chi_1$ angles and 75% of $\chi_{1+2}$ angles within $40°$ of the X-ray structures on a test set of 379 proteins.

## Reductions

- **To MAP inference.** Set $P(x) \propto \exp(-E(x))$. Then the GMEC is the most probable assignment of a pairwise [Markov random field](/markov-random-field/), and min-sum message passing is max-product in the log domain.
- **To weighted constraint satisfaction.** Each residue is a variable, each table a soft constraint, and the GMEC is an optimal solution.
- **To 0/1 integer programming.** As in the list above. This form adds side constraints easily, for example a fixed number of residues of one type in design.
- **From graph coloring.** The reduction of the theorem.

## Applications

- **Comparative modeling.** After the backbone is copied from a template, the side chains of the target are packed onto it, for example with SCWRL. [MODELLER](/modeller/) instead treats the side chains as part of its restraint optimization.
- **Protein design.** With all amino acid types in the rotamer sets, packing chooses the sequence too ([protein design](/protein-design/)).
- **Docking and mutation scans.** Repacking the side chains near an interface or a mutation estimates its effect on the energy.

## References
