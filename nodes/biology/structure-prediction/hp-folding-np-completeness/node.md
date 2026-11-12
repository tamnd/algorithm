---
tag: XJ15FZ
kind: theorem
slug: hp-folding-np-completeness
name: NP-completeness of HP folding
aliases:
- HP folding is NP-complete
area: biology/structure-prediction
level: advanced
summary: Deciding whether an HP sequence has a fold with at least k H-H contacts is NP-complete on the square lattice (Crescenzi et al. 1998) and on the cubic lattice (Berger and Leighton 1998).
prereqs: [hp-model, np-complete, polynomial-time-reduction]
see_also: [protein-structure-prediction, levinthal-paradox, approximation-ratio, certificate, gadget-reduction, strong-np-hardness, pseudoknot-np-hardness, self-avoiding-walk-enumeration]
sources:
  - paper: doi:10.1089/cmb.1998.5.423
    title: Pierluigi Crescenzi, Deborah Goldman, Christos Papadimitriou, Antonio Piccolboni and Mihalis Yannakakis, On the complexity of protein folding, Journal of Computational Biology 5(3), 1998, 423-465
    locator: the NP-completeness of HP folding on the square lattice; an extended abstract is in STOC 1998, pages 597 to 603
  - paper: doi:10.1089/cmb.1998.5.27
    title: Bonnie Berger and Tom Leighton, Protein folding in the hydrophobic-hydrophilic (HP) model is NP-complete, Journal of Computational Biology 5(1), 1998, 27-40
    locator: the NP-completeness on the cubic lattice; an extended abstract is in RECOMB 1998, pages 30 to 39
  - paper: doi:10.1089/cmb.1996.3.53
    title: William E. Hart and Sorin Istrail, Fast protein folding in the hydrophobic-hydrophilic model within three-eighths of optimal, Journal of Computational Biology 3(1), 1996, 53-96
    locator: the approximation algorithms with ratios 1/4 on the square lattice and 3/8 on the cubic lattice
  - paper: doi:10.1007/BF02460703
    title: Ron Unger and John Moult, Finding the lowest free energy conformation of a protein is an NP-hard problem, proof and implications, Bulletin of Mathematical Biology 55(6), 1993, 1183-1198
    locator: the NP-hardness proof for a lattice model with a more general energy
  - paper: doi:10.1007/BF02460704
    title: Aviezri S. Fraenkel, Complexity of protein folding, Bulletin of Mathematical Biology 55(6), 1993, 1199-1210
    locator: the NP-hardness proof for a lattice model with a more general energy
---

The decision version of folding in the [HP model](/hp-model/) is NP-complete on the square lattice and on the cubic lattice: given a string over $\{H, P\}$ and an integer $k$, it is NP-complete to decide whether some self-avoiding fold of the string has at least $k$ contacts between H residues. Crescenzi, Goldman, Papadimitriou, Piccolboni and Yannakakis proved the 2D case and Berger and Leighton the 3D case, both in 1998. The result says that exact [structure prediction](/protein-structure-prediction/), even in the simplest lattice model, has no polynomial-time algorithm unless $\text{P} = \text{NP}$.

## Statement

Fix the dimension $d \in \{2, 3\}$ and the lattice $\mathbb{Z}^d$. A fold of $s = s_0 \cdots s_{n-1}$ is an injective map $x : \{0, \ldots, n-1\} \to \mathbb{Z}^d$ with $\|x_i - x_{i+1}\|_1 = 1$ for each $i < n - 1$. Its number of H-H contacts is

$$C_s(x) = \bigl|\{(i, j) : j \ge i + 2,\ s_i = s_j = H,\ \|x_i - x_j\|_1 = 1\}\bigr|,$$

so its HP energy is $-C_s(x)$.

**HP-FOLD$_d$.** *Input:* a string $s \in \{H, P\}^n$ and an integer $k \ge 0$. *Question:* is there a fold $x$ of $s$ in $\mathbb{Z}^d$ with $C_s(x) \ge k$?

**Theorem.** HP-FOLD$_2$ is [NP-complete](/np-complete/) (Crescenzi et al. 1998). HP-FOLD$_3$ is NP-complete (Berger and Leighton 1998).

So the optimization problem, to find a fold of minimum HP energy, is [NP-hard](/np-hard/) in both dimensions. The input has no large numbers: $k$ is at most $dn$, because each residue has at most $2d$ lattice neighbours and each contact uses two residues. So the problem is NP-complete in the strong sense, and a pseudo-polynomial algorithm does not help.

## In plain words

In the HP model, a protein is a chain of two kinds of beads, oily and not oily. The chain must lie on the squares of a grid without crossing itself, and each pair of oily beads that touch but are not joined scores a point. The question is whether a chain can reach a given score.

If someone shows you a placement, you can check its score quickly, so the problem is in the class of problems with easy checks. The hard part is to find a placement. The two papers show that any problem in that class can be turned into a question about such a chain, with a carefully built pattern of oily and non-oily beads. So a fast exact method for chains would give fast exact methods for many famous hard problems, which most researchers believe do not exist.

## Proof

The proof has two parts. Membership in NP is proved in full. The hardness parts are long gadget constructions, and here they are only sketched.

**Part 1: HP-FOLD$_d$ is in NP.** We give a [certificate](/certificate/) and a [polynomial-time verifier](/polynomial-time-verifier/).

*Certificate.* A word $w = w_1 \cdots w_{n-1}$ over the $2d$ unit vectors of $\mathbb{Z}^d$. Its length is $n - 1$, which is linear in the input length.

*Verifier.* Set $x_0 = 0$ and $x_i = x_{i-1} + w_i$ for $i = 1, \ldots, n - 1$. Each coordinate of each $x_i$ is between $-n$ and $n$, so it fits in $O(\log n)$ bits. Sort the $n$ points in lexicographic order and reject if two consecutive points in the sorted order are equal. For each $i$ with $s_i = H$ and each of the $2d$ unit vectors $u$, find $x_i + u$ in the sorted list by binary search. If it is $x_j$ with $j \ge i + 2$ and $s_j = H$, add 1 to a counter. Accept if and only if the counter is at least $k$.

*Running time.* The positions take $O(dn)$ additions of $O(\log n)$-bit numbers. The sort takes $O(n \log n)$ comparisons and the searches take $O(dn \log n)$ comparisons, each on $O(d \log n)$ bits. The total is polynomial in $n$.

*Correctness.* The points $x_0, \ldots, x_{n-1}$ satisfy $\|x_i - x_{i+1}\|_1 = 1$ by construction. They are distinct if and only if the sort finds no equal neighbours, because equal points are adjacent in a sorted list. So the verifier passes the first test exactly when $x$ is a fold. Each H-H contact $(i, j)$ with $i < j$ is counted exactly once: when the loop is at $i$ and at the vector $u = x_j - x_i$. No other pair is counted, because the loop checks $j \ge i + 2$ and $s_j = H$. So the counter equals $C_s(x)$.

If $(s, k)$ is a yes-instance, some fold $y$ has $C_s(y) \ge k$. The translate $x = y - y_0$ is also a fold with the same contacts, because a translation keeps all distances. Its step word $w_i = x_i - x_{i-1}$ is a certificate that the verifier accepts. Conversely, if the verifier accepts some $w$, then $x$ is a fold with $C_s(x) \ge k$, so the instance is a yes-instance. $\square$

**Part 2: hardness on the cubic lattice (sketch).** Berger and Leighton first define a restricted problem in which the string has exactly $m^3$ H residues and the question is whether they can fill an $m \times m \times m$ cube. A full cube gives the H residues the largest number of lattice contacts among themselves, and this lets them write the restricted problem as a special case of HP-FOLD$_3$ with a suitable $k$. The H residues come in blocks that are separated by P segments, and the P segments act as loops that can leave the cube and come back. They reduce a strongly NP-complete variant of [bin packing](/bin-packing-np-hardness/) to this restricted problem, with gadgets built from H blocks and P loops. The construction has polynomial size, so the reduction is a [polynomial-time reduction](/polynomial-time-reduction/). The details of the gadgets, and the proof that every perfect fold has the intended structure, take most of their paper.

**Part 3: hardness on the square lattice (sketch).** Crescenzi et al. give a [gadget reduction](/gadget-reduction/) from a Hamiltonian cycle problem on a restricted class of planar graphs. From the graph they build, in polynomial time, an HP string and a target $k$ such that a fold with at least $k$ contacts exists if and only if the graph has a Hamiltonian cycle. The square lattice has less room than the cubic one, so the 2D gadgets differ from the 3D ones, and the two proofs are independent.

With Part 1, Parts 2 and 3 give the theorem.

## Consequences

- **Exact prediction is hard in the worst case.** Every energy model that contains the HP model as a special case, with the same lattice, is NP-hard to minimize. This holds for contact models with a 20-letter alphabet and any energy matrix that can express the HP energies.
- **Exponential exact algorithms.** Unless $\text{P} = \text{NP}$, no exact algorithm runs in polynomial time. [Exhaustive enumeration](/self-avoiding-walk-enumeration/) of all folds takes time about $\mu^n$, with $\mu$ about 2.638 in 2D and about 4.684 in 3D.
- **Approximation is the right goal.** The problem has constant-factor approximation algorithms on both lattices, so it is in a better position than problems that cannot be approximated at all. See [approximation ratio](/approximation-ratio/).
- **Folding in nature.** The result does not contradict the fast folding of real proteins. The hard instances are built strings, and natural sequences are selected to have [funnel-shaped landscapes](/energy-landscape/). See [Levinthal's paradox](/levinthal-paradox/).

## Tightness

- **The certificate is short.** A fold has $n - 1$ steps, so the problem is in NP, and NP-completeness is the exact class of the decision problem, not only a lower bound.
- **Two letters are enough.** Hardness holds already for the binary alphabet and for the simplest energy, with one unit for each H-H contact.
- **Dimension one is easy.** On $\mathbb{Z}$, a fold is a straight line, so no two residues with $j \ge i + 2$ are neighbours, and every string has 0 contacts. The problem becomes hard from dimension 2.
- **Upper bounds are easy, optima are not.** The parity bound $2 \min(|\text{EV}|, |\text{OD}|) + 2$ on the square lattice (see [HP model](/hp-model/)) is computed in linear time, but deciding whether a fold reaches a given number is NP-complete.

## History

Unger and Moult (1993) and Fraenkel (1993) proved NP-hardness of finding the lowest energy conformation in lattice models with more general energies, which left the HP model open. Hart and Istrail (1996) gave polynomial-time approximation algorithms for the HP model, with at least 1/4 of the optimal number of contacts on the square lattice and at least 3/8 on the cubic lattice. In 1998, Crescenzi, Goldman, Papadimitriou, Piccolboni and Yannakakis proved NP-completeness on the square lattice, and Berger and Leighton proved it on the cubic lattice. Both papers appeared in the Journal of Computational Biology in 1998, after extended abstracts at STOC 1998 and RECOMB 1998.

## References
