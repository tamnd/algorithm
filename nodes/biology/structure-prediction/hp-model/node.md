---
tag: HVWK9P
kind: model
slug: hp-model
name: HP lattice model
aliases:
- Hydrophobic-polar model
- HP model
area: biology/structure-prediction
level: advanced
summary: "Lattice model of folding: a chain of H and P residues is a self-avoiding walk on the square or cubic lattice, and the energy is minus the number of H-H contacts (Dill 1985, Lau and Dill 1989)."
history:
  year: 1985
  people: [Ken A. Dill, Kit Fun Lau]
  note: Dill proposed the model in 1985, and Lau and Dill studied it by exhaustive enumeration of short chains in 1989.
prereqs: [hydrophobic-effect, self-avoiding-walk-enumeration]
see_also: [hp-folding-np-completeness, protein-structure-prediction, energy-landscape, fragment-assembly, ising-model, bipartite-graph, approximation-ratio, nearest-neighbor-model]
sources:
  - paper: doi:10.1021/bi00327a032
    title: Ken A. Dill, Theory for the folding and stability of globular proteins, Biochemistry 24(6), 1985, 1501-1509
    locator: the lattice theory of folding with hydrophobic and polar residues
  - paper: doi:10.1021/ma00200a030
    title: Kit Fun Lau and Ken A. Dill, A lattice statistical mechanics model of the conformational and sequence spaces of proteins, Macromolecules 22(10), 1989, 3986-3997
    locator: the HP model with the energy of minus one for each H-H contact, and the exhaustive enumeration of short chains
  - paper: doi:10.1002/pro.5560040401
    title: Ken A. Dill et al., Principles of protein folding, a perspective from simple exact models, Protein Science 4(4), 1995, 561-602
    locator: the review of lattice models, exact enumeration, unique ground states and the folding funnel
  - paper: doi:10.1089/cmb.1996.3.53
    title: William E. Hart and Sorin Istrail, Fast protein folding in the hydrophobic-hydrophilic model within three-eighths of optimal, Journal of Computational Biology 3(1), 1996, 53-96
    locator: the parity argument, the upper bound on the number of contacts, and the approximation algorithms on the square and cubic lattices
  - paper: doi:10.1089/cmb.1998.5.27
    title: Bonnie Berger and Tom Leighton, Protein folding in the hydrophobic-hydrophilic (HP) model is NP-complete, Journal of Computational Biology 5(1), 1998, 27-40
    locator: the NP-completeness on the cubic lattice
  - paper: doi:10.1089/cmb.1998.5.423
    title: Pierluigi Crescenzi, Deborah Goldman, Christos Papadimitriou, Antonio Piccolboni and Mihalis Yannakakis, On the complexity of protein folding, Journal of Computational Biology 5(3), 1998, 423-465
    locator: the NP-completeness on the square lattice
  - paper: doi:10.1021/ma00145a039
    title: Sanzo Miyazawa and Robert L. Jernigan, Estimation of effective interresidue contact energies from protein crystal structures, quasi-chemical approximation, Macromolecules 18(3), 1985, 534-552
    locator: the table of contact energies between the 20 residue types
---

The HP model is a lattice model of protein folding in which each residue is either hydrophobic (H) or polar (P), a fold is a self-avoiding walk on the square or the cubic lattice, and the energy of a fold is minus the number of contacts between H residues that are not chain neighbours. Ken Dill proposed it in 1985 to isolate the [hydrophobic effect](/hydrophobic-effect/), and Lau and Dill (1989) studied it by exhaustive enumeration. It is the standard exact model of folding in computer science: its optimization problem is [NP-complete](/hp-folding-np-completeness/) in 2D and 3D, and it has constant-factor approximation algorithms.

## The machine

**Sequence.** A string $s = s_0 s_1 \cdots s_{n-1} \in \{H, P\}^n$, where $n$ is the number of residues.

**Lattice.** The square lattice $\mathbb{Z}^2$ or the cubic lattice $\mathbb{Z}^3$, with $d$ the dimension. Two sites are neighbours when their $\ell_1$ distance is 1, so each site has $2d$ neighbours.

**Fold.** A fold is an injective map $x : \{0, \ldots, n-1\} \to \mathbb{Z}^d$ with $\|x_i - x_{i+1}\|_1 = 1$ for $0 \le i < n - 1$. It is a [self-avoiding walk](/self-avoiding-walk-enumeration/) of $n - 1$ steps. Residues $i$ and $i + 1$ are joined by a chain bond.

**Contact and energy.** A pair $(i, j)$ with $j \ge i + 2$ is a *contact* of the fold $x$ when $\|x_i - x_j\|_1 = 1$. It is an *H-H contact* when also $s_i = s_j = H$. The energy of the fold is

$$E_s(x) = -\,\bigl|\{(i, j) : j \ge i + 2,\ s_i = s_j = H,\ \|x_i - x_j\|_1 = 1\}\bigr|.$$

So an H-H contact has energy $-1$, and H-P and P-P contacts have energy 0.

**The question.** Find $E^\ast(s) = \min_x E_s(x)$ and a fold that reaches it. A fold of minimum energy is a *native* fold of $s$ in the model. The decision version asks, for given $s$ and $k$, whether some fold has at least $k$ H-H contacts.

**Symmetry.** A translation of $\mathbb{Z}^d$, or a rotation or reflection of the lattice, maps folds to folds and keeps all distances, so it keeps the energy. The point group has 8 elements in 2D and 48 in 3D. Two folds are counted as the same structure when one of these maps takes one to the other.

## What it counts

The cost measure of the model is the number of H-H contacts, and the size of the search is the number $c_m$ of self-avoiding walks of $m = n - 1$ steps.

| steps $m$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| square, $c_m$ | 4 | 12 | 36 | 100 | 284 | 780 | 2172 | 5916 | 16268 | 44100 | 120292 | 324932 | 881500 |
| cubic, $c_m$ | 6 | 30 | 150 | 726 | 3534 | 16926 | 81390 | | | | | | |

The counts grow as $\mu^{m + o(m)}$, with the connective constant $\mu$ about 2.638 on the square lattice and about 4.684 on the cubic lattice.

**Lemma 1 (parity).** On $\mathbb{Z}^2$ and $\mathbb{Z}^3$, every contact $(i, j)$ has $j - i$ odd. In particular $j \ge i + 3$.

*Proof.* Colour each site by the parity of the sum of its coordinates. A step of the walk changes one coordinate by 1, so it changes the colour. By induction on $i$, the colour of $x_i$ is the colour of $x_0$ when $i$ is even and the other colour when $i$ is odd. Two neighbour sites have different colours. So if $x_i$ and $x_j$ are neighbours, $i$ and $j$ have different parities, and $j - i$ is odd. The smallest odd number that is at least 2 is 3. $\square$

So the cubic and square lattices are [bipartite](/bipartite-graph/), and an H residue at an even position can touch only H residues at odd positions. The triangular and face-centred cubic lattices are not bipartite, and this restriction does not hold there.

**Lemma 2 (upper bound).** Let $\text{EV}$ and $\text{OD}$ be the sets of H residues at even and at odd positions. On the square lattice, every fold has at most $2 \min(|\text{EV}|, |\text{OD}|) + 2$ H-H contacts. On the cubic lattice the bound is $4 \min(|\text{EV}|, |\text{OD}|) + 2$.

*Proof.* Each site has $2d$ neighbours. A residue $i$ with $0 < i < n - 1$ uses two of them for its chain bonds, so it has at most $2d - 2$ contacts. An end residue uses one, so it has at most $2d - 1$ contacts. By Lemma 1, each H-H contact has exactly one residue in $\text{EV}$. So the number of H-H contacts is at most the sum of the contact counts of the residues of $\text{EV}$, which is at most $(2d - 2)|\text{EV}| + e$, where $e \le 2$ is the number of end residues in $\text{EV}$. The same argument holds for $\text{OD}$. Take the smaller of the two bounds and put $d = 2$ or $d = 3$. $\square$

This is the bound that Hart and Istrail (1996) compare their folds against.

**Example.** Take $s = $ HPHPPHHPHH, with $n = 10$. The H residues are at positions 0, 2, 5, 6, 8 and 9, so $\text{EV} = \{0, 2, 6, 8\}$ and $\text{OD} = \{5, 9\}$. Lemma 2 gives at most $2 \cdot 2 + 2 = 6$ contacts on the square lattice. Exhaustive search over all 16,268 walks of 9 steps gives the exact optimum: 4 contacts, so $E^\ast = -4$. One optimal fold is

$$x = (0,0), (1,0), (1,1), (2,1), (2,2), (1,2), (0,2), (-1,2), (-1,1), (0,1),$$

with the H-H contacts $(0, 9)$, $(2, 9)$, $(6, 9)$ and $(2, 5)$. Each has one even and one odd position, as Lemma 1 says. The 24 optimal walks form 3 folds up to symmetry. The energies of all 16,268 walks are distributed as follows:

| energy | 0 | $-1$ | $-2$ | $-3$ | $-4$ |
|---|---|---|---|---|---|
| walks | 9292 | 5792 | 1024 | 136 | 24 |

On the cubic lattice the same sequence also has $E^\ast = -4$, but with 53 optimal folds up to symmetry, because the extra dimension gives more ways to make the same contacts.

## Relation to other models

- **Self-avoiding walks.** With $s = P^n$ every fold has energy 0, and the model is the counting of self-avoiding walks, a classic model of a polymer in a good solvent. See [self-avoiding walk enumeration](/self-avoiding-walk-enumeration/).
- **Contact energies.** The HP model is the two-letter case of a contact model with a matrix of energies $\varepsilon_{ab}$ between residue types $a$ and $b$. The 20-letter version uses statistical contact energies, for example those of Miyazawa and Jernigan (1985). Variants of the HP model also give an energy to H-P contacts.
- **Other lattices.** The triangular, face-centred cubic and other lattices remove the parity restriction. Models with a side-chain site for each residue are closer to real proteins.
- **Ising model.** The [Ising model](/ising-model/) has a fixed graph and variable spins. The HP model is the reverse: the labels H and P are fixed, and the graph of contacts is the variable. This is why the transfer matrix and the exact solutions of spin models do not apply.
- **RNA models.** In the RNA [nearest neighbor model](/nearest-neighbor-model/), a secondary structure is a set of nested pairs, and dynamic programming finds the optimum in polynomial time. A lattice fold has no such nested structure, so no decomposition of this kind is known.
- **Full models.** Off-lattice models, the [energy functions](/energy-function/) of [Rosetta](/rosetta/) and force fields for [molecular dynamics](/molecular-dynamics/) describe real proteins. The HP model keeps only chain connectivity, excluded volume and the hydrophobic effect, so its results are about principles, not about particular proteins.

## Known results in the model

**Hardness.**

- The decision version is NP-complete on the square lattice (Crescenzi, Goldman, Papadimitriou, Piccolboni and Yannakakis 1998) and on the cubic lattice (Berger and Leighton 1998). See [NP-completeness of HP folding](/hp-folding-np-completeness/).

**Approximation.**

- Hart and Istrail (1996) gave polynomial-time algorithms that fold each sequence with at least 1/4 of the optimal number of contacts on the square lattice and 3/8 on the cubic lattice. They compare with the bound of Lemma 2, not with the unknown optimum. Later work improved the ratio on the square lattice. See [approximation ratio](/approximation-ratio/).

**Exact search.**

- Exhaustive search over all folds is exact. With the symmetries removed, it visits about $c_{n-1}/8$ walks in 2D and $c_{n-1}/48$ in 3D, with $O(d)$ work per node of the search tree. The implementation on this site folds a chain of 14 residues on the square lattice, over $c_{13} = 881{,}500$ walks, in a few seconds of Python.
- In 2D, among the 1,024 sequences of length 10, 944 have $E^\ast < 0$. Only 6 of these have a single optimal fold up to symmetry: HHPHPPHPPH, HHPPHPPHPH, HPHPPHPPHH, HPPHPPHPHH and HPPHPPHPPH with $E^\ast = -4$, and PHPPHHPPHP with $E^\ast = -3$. The sequence HHPPHPPHPPHH, of length 12, has a single optimal fold with $E^\ast = -5$. So a unique native state, which the [thermodynamic hypothesis](/thermodynamic-hypothesis/) needs, is a rare property of a sequence even in this model.

**Heuristics.**

- Monte Carlo search, [simulated annealing](/simulated-annealing/), genetic algorithms and chain growth methods find good folds of chains far longer than exact search can handle, with no guarantee. The [fragment assembly](/fragment-assembly/) page uses a lattice chain of this kind as its toy model.

**Landscapes.**

- Exact enumeration of all folds of short chains gives the full [energy landscape](/energy-landscape/): the density of states, the number of local minima, and the barriers between them. Dill et al. (1995) review what these exact models show about funnels and about the collapse of the chain.

## References
