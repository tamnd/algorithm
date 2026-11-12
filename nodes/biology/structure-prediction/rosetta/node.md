---
tag: 2J2HZZ
kind: algorithm
slug: rosetta
name: Rosetta
aliases:
- Rosetta software suite
area: biology/structure-prediction
level: advanced
summary: A software suite for macromolecular modelling. Its ab initio protocol folds a chain by fragment assembly under a coarse score, then packs side chains and refines under an all-atom energy.
solves: [ab-initio-protein-folding]
model: real-ram
complexity:
  vars: {n: the number of residues, S: the total number of Monte Carlo steps in both phases}
  time: {worst: O(S n + n^3 + 4^n)}
  space: {extra: O(n)}
properties: {deterministic: false, iterative: true, exact: false}
history:
  year: 1997
  people: [David Baker, Kim T. Simons, Carol A. Rohl, Brian Kuhlman, Andrew Leaver-Fay]
  note: The Baker laboratory wrote Rosetta for de novo structure prediction in 1997. It grew into a suite for prediction, design and docking, and Rosetta3 (2011) rewrote it as a library of modules.
prereqs: [fragment-assembly, energy-function]
see_also: [ab-initio-protein-folding, side-chain-packing, rotamer, protein-design, loop-modeling, dead-end-elimination, alphafold, molecular-dynamics]
sources:
  - paper: doi:10.1016/S0076-6879(04)83004-0
    title: Carol A. Rohl, Charlie E. M. Strauss, Kira M. S. Misura and David Baker, Protein structure prediction using Rosetta, Methods in Enzymology 383, 2004, 66-93
    locator: the low-resolution stages with fragments, the high-resolution refinement and the selection of models
  - paper: doi:10.1016/B978-0-12-381270-4.00019-6
    title: Andrew Leaver-Fay et al., Rosetta3, an object-oriented software suite for the simulation and design of macromolecules, Methods in Enzymology 487, 2011, 545-574
    locator: the architecture of the suite, with poses, score functions, movers and the packer
  - paper: doi:10.1021/acs.jctc.7b00125
    title: Rebecca F. Alford et al., The Rosetta all-atom energy function for macromolecular modeling and design, Journal of Chemical Theory and Computation 13(6), 2017, 3031-3048
    locator: the terms and weights of the all-atom energy function
  - paper: doi:10.1126/science.1113801
    title: Philip Bradley, Kira M. S. Misura and David Baker, Toward high-resolution de novo structure prediction for small proteins, Science 309(5742), 2005, 1868-1871
    locator: all-atom refinement that reaches near-atomic accuracy for some small proteins
  - paper: doi:10.1126/science.1089427
    title: Brian Kuhlman, Gautam Dantas, Gregory C. Ireton, Gabriele Varani, Barry L. Stoddard and David Baker, Design of a novel globular protein fold with atomic-level accuracy, Science 302(5649), 2003, 1364-1368
    locator: the design of Top7, which alternates sequence design and structure prediction with Rosetta
  - paper: doi:10.1006/jmbi.1997.0959
    title: Kim T. Simons, Charles Kooperberg, Enoch Huang and David Baker, Assembly of protein tertiary structures from fragments with similar local sequences using simulated annealing and Bayesian scoring functions, Journal of Molecular Biology 268(1), 1997, 209-225
    locator: the first version of the method, fragment assembly with a Bayesian score
---

Rosetta is a software suite for modelling proteins and other macromolecules, written in the laboratory of David Baker and developed by many groups. Its ab initio protocol predicts a fold in two phases. A low-resolution phase represents each side chain by one centroid and folds the backbone by [fragment assembly](/fragment-assembly/), with 9-residue and then 3-residue fragments, under a coarse statistical score. A high-resolution phase adds all side-chain atoms, chooses a [rotamer](/rotamer/) for each side chain by [side-chain packing](/side-chain-packing/), and refines the structure by Monte Carlo moves and minimization under an all-atom [energy function](/energy-function/). Many independent runs give many decoys, and the protocol reports low-energy decoys or the centres of large clusters. The same parts, the score functions, the packer and the Monte Carlo movers, serve design, docking and loop modelling.

## In plain words

Rosetta folds a protein in two passes, first rough and then fine. In the rough pass, each building block of the chain is a backbone with one ball for its side group. The program bends the backbone by copying in the shapes of short pieces of known proteins, and keeps the changes that a simple score likes.

In the fine pass, every atom is present. The program chooses a shape for each side group so that the groups fit together without overlap. Then it makes small changes to the backbone and to the side groups, and keeps those that a detailed score likes. At the end it stops at a shape where no single small change helps. It repeats the whole process many times and picks the best results.

## The problem

The input is a protein sequence $s$ of length $n$, fragment libraries for the windows of the chain, a coarse score $E_\text{cen}$ on backbones with centroids, and an all-atom energy $E_\text{fa}$ on backbones with side chains. The output is a full-atom structure of low $E_\text{fa}$, a prediction for [ab initio protein folding](/ab-initio-protein-folding/). In Rosetta a structure is a pose: the backbone torsions, a rotamer for each side chain, and the coordinates that follow from them.

The implementation on this page keeps the two-phase structure on the square lattice, so that brute force can check it.

- **Backbone.** Residue 0 is at $(0, 0)$ and residue 1 at $(1, 0)$. A word $w \in \{L, S, R\}^{n-2}$ places residues 2 to $n - 1$ by a left turn, a straight step or a right turn, as on the [fragment assembly](/fragment-assembly/) page.
- **Centroid score.** $E_\text{cen}(w)$ is the [HP model](/hp-model/) energy of the backbone beads, minus the number of H-H contacts, and $+\infty$ when two beads share a site.
- **Full-atom model.** Each residue $i$ also has a side-chain bead on one of the 4 lattice neighbours of its backbone bead. Its rotamer $r_i \in \{0, 1, 2, 3\}$ is a turn from the direction of the bond into residue $i$: forward, left, back or right. So the side chains move with the backbone. $E_\text{fa}(w, r)$ is minus the number of pairs of H side-chain beads at distance 1, and $+\infty$ when any two of the $2n$ beads share a site.

## The algorithm

```pseudo id=main
ROSETTA(s, stages, R)
L1  w ← the extended chain S S … S
L2  for each centroid stage (k, F, K) in order do              ▷ long fragments first
L3      w ← the best word of K fragment insertion steps from w under E_cen
L4  r ← PACK(s, w)                                             ▷ rotamers for all side chains
L5  if r = NIL then w ← the extended chain;  r ← PACK(s, w)
L6  E ← E_fa(w, r);  best ← (E, w, r)
L7  for t ← 0 to R − 1 do                                      ▷ refinement, T falls geometrically
L8      with probability 1/2: (w′, r′) ← (w with one random letter replaced, r)
L9      otherwise: (w′, r′) ← (w, r with one random rotamer replaced)
L10     E′ ← E_fa(w′, r′)                                      ▷ +∞ on a clash
L11     if E′ ≤ E or random() < exp(−(E′ − E) / T_t) then (w, r, E) ← (w′, r′, E′)
L12         if E < best.E then best ← (E, w, r)
L13 (E, w, r) ← best
L14 repeat
L15     scan the single moves of (w, r): one letter or one rotamer changed
L16     if a move (w′, r′) has E_fa(w′, r′) < E then (w, r, E) ← the first such move
L17 until no move improves;  return (E, w, r)
```

Line L3 is the loop of [fragment assembly](/fragment-assembly/) with the Metropolis criterion and a falling temperature, and it returns the best word that it visits. PACK first finds a clash-free rotamer vector by [backtracking](/backtracking/) over the residues in order, or returns NIL when none exists. It then runs rotamer trials: it visits the residues in order and gives each the rotamer of lowest $E_\text{fa}$ with the others fixed, until a full pass changes nothing. The extended chain can always be packed, for example with every side chain on the left, so line L5 always gives a rotamer vector. Lines L14 to L17 are a first-improvement [local search](/local-search/), the analogue of the final minimization of Rosetta.

## Example

Take HHPPHH, with $n = 6$. The centroid phase has a stage of 300 steps with all 27 words of 3 letters at each window, and a stage of 200 steps with single letters, both cooling from $T = 2.0$ to $0.5$. The refinement has 1500 steps and cools from $T = 1.0$ to $0.1$. With the random seed 0:

1. **Centroid phase.** Both stages end with the word SLLS, a U shape in which residue 0 touches residue 5 and residue 1 touches residue 4. Its centroid score is $-2$.
2. **Packing.** PACK gives the rotamers $(2, 3, 0, 0, 3, 0)$. The side chains of the H residues 0, 1, 4 and 5 are at $(-1, 0)$, $(1, -1)$, $(1, 2)$ and $(-1, 1)$, and only the first and the last touch, so $E_\text{fa} = -1$. A search over all rotamer vectors for this backbone finds $-2$. Rotamer trials are a local search and can stop short of the best packing.
3. **Refinement.** At step 157, with $T = 0.786$, the run reaches $E_\text{fa} = -2$ with SRLL. At step 269, with $T = 0.662$, it reaches $-3$ with the backbone LRRL and the rotamers $(3, 3, 0, 1, 0, 3)$. The run ends at a state with $E_\text{fa} = -2$, so line L13 goes back to the best state.
4. **Descent.** No single move improves LRRL with these rotamers, and the protocol returns $(-3, \text{LRRL}, (3, 3, 0, 1, 0, 3))$.

In the result, the backbone beads are at $(0, 0), (1, 0), (1, 1), (2, 1), (2, 0), (3, 0)$, and the side chains of the four H residues lie in a row at $(0, -1), (1, -1), (2, -1), (3, -1)$, with 3 contacts. Brute force over all $3^4 \cdot 4 \cdot 3^5 = 78\,732$ pairs of a word and a rotamer vector in which no side chain points back along its bond finds the minimum $-3$, so this run is optimal. The backbone LRRL has the centroid score $-1$, worse than SLLS. The coarse score and the fine score disagree, which is why the high-resolution phase must be able to change the backbone.

The protocol is a heuristic. For PHHPPPH the brute-force minimum is $-2$, and with the same settings 3 of the seeds 0 to 9 reach it while the other 7 stop at $-1$.

## Correctness

Rosetta gives no guarantee of an optimum, and the problem is [NP-hard](/hp-folding-np-completeness/) already for its centroid part. What the protocol guarantees is about the validity of its output:

1. **The output is valid and its energy is exact.** The returned structure has no clash, and the returned $E$ equals $E_\text{fa}(w, r)$.
2. **PACK is complete for validity.** It returns NIL exactly when the backbone has no clash-free rotamer vector, because the backtracking tries every vector in order. Otherwise its output is clash-free, and no change of one rotamer lowers its energy.
3. **The descent terminates.** The energy is an integer at least $-\lfloor 3n/2 \rfloor$, because each side-chain bead has at most 3 neighbouring side-chain beads, and each round of lines L14 to L16 lowers it by at least 1.
4. **The output is a local minimum.** No single move of line L15 lowers $E_\text{fa}$ of the returned structure, and its energy is at most the energy of each state that the refinement visited.

The proofs are below.

## Complexity

One Monte Carlo step, in line L3 or in lines L8 to L12, rebuilds the chain and scores it with a hash table of the sites in $O(n)$ expected time. So $S$ steps in both phases take $O(S n)$ time. The rotamer trials and the final descent each change the energy at most $\lfloor 3n/2 \rfloor$ times, and each round scores $O(n)$ candidates at $O(n)$ each, so each takes $O(n^3)$ time. The backtracking of PACK can, in the worst case, try $O(4^n)$ partial vectors, which gives the exponential term. Each residue has at most 4 sites for its side chain, so a clash-free vector is a matching that covers all residues in a [bipartite graph](/bipartite-matching/) between residues and free sites, and the [Hopcroft-Karp algorithm](/hopcroft-karp/) finds one in polynomial time. The extra space is $O(n)$.

In Rosetta the costs are in the energy function and in the number of runs. Its packer chooses among hundreds of rotamers for each residue by simulated annealing over a table of precomputed pair energies. A prediction typically uses thousands to hundreds of thousands of independent runs, which is why Rosetta was also run on volunteer computers in the Rosetta@home project.

## Properties

- **Two resolutions.** The coarse phase searches a smooth [energy landscape](/energy-landscape/) quickly. The fine phase decides between similar folds. The example shows that the two scores can disagree.
- **Randomized.** Each run gives one decoy. A fixed seed repeats a run.
- **Valid output.** Every returned structure is clash-free, whatever the libraries and the temperatures.
- **Local optimality, not global.** The output is a local minimum for the single moves, and it can be far from the global minimum.
- **Modular.** In Rosetta, a protocol is a sequence of movers that change a pose, scored by a weighted sum of energy terms. The same parts serve many protocols.

## Variants and improvements

- **Relax.** Full-atom refinement alternates repacking, small and shear moves of backbone torsions, and quasi-Newton minimization, such as [L-BFGS](/limited-memory-bfgs/), with a repulsion weight that rises during the run. Bradley, Misura and Baker (2005) reached near-atomic accuracy for some small proteins this way.
- **Design.** Fix the backbone and let the packer choose both the amino acid and the rotamer at each position. Alternating design and structure prediction produced Top7, a protein with a new fold (Kuhlman et al. 2003). See [protein design](/protein-design/).
- **Docking, loops and comparative modelling.** The same movers dock two proteins, rebuild [loops](/loop-modeling/) between fixed ends, and refine models built from templates, see [comparative modelling](/comparative-modeling/).
- **Restraints.** Contacts from [direct coupling analysis](/direct-coupling-analysis/), or sparse experimental data, are added to the score as restraints.
- **Score functions.** The all-atom energy has changed over the years. Alford et al. (2017) describe the version of 2015, which mixes physical terms such as Lennard-Jones and solvation with statistical terms for torsions and rotamers.
- **Deep learning.** The Baker laboratory later built networks that predict structures directly, in the line of [AlphaFold](/alphafold/), and Rosetta now often refines their models or uses their predicted distances as restraints.

## When to use it

Use Rosetta when the task needs an explicit energy model with many atoms: the design of new proteins, binders and enzymes, the refinement of a model, docking, the effects of mutations, and modelling with sparse experimental data. For the prediction of a natural protein from its sequence, a learned predictor such as [AlphaFold](/alphafold/) is now more accurate and faster, and the ab initio protocol of Rosetta is mostly of use for small proteins or as a sampler of alternative folds. For the dynamics of a structure, use [molecular dynamics](/molecular-dynamics/).

## Pitfalls

- **One run is one sample.** A single trajectory says little. Run many and compare the low-energy decoys.
- **The lowest energy is not always the native fold.** A decoy can score below the native structure. Clustering, and agreement between independent runs, are better evidence than one low energy.
- **Coarse and fine scores disagree.** A backbone that the centroid phase prefers can be wrong at full atom, as in the example. Do not discard all decoys with poor centroid scores before refinement.
- **Packing is a local search too.** Rotamer trials, and the packer of Rosetta, can miss the best packing. Repeated packing, or an exact method such as [dead-end elimination](/dead-end-elimination/) on small cases, helps to check it.
- **Energy units.** The Rosetta energy is in its own units, which are only roughly kcal/mol. Compare energies within one score function, not across versions.
- **Fragments from homologs.** In a benchmark, exclude fragments from the target and its homologs, or the test measures copying.

## Implementations

## History

Simons, Kooperberg, Huang and Baker (1997) introduced fragment assembly with a Bayesian score, the first version of Rosetta. Rosetta was among the most successful methods for targets without templates in the CASP experiments of the following years. Rohl, Strauss, Misura and Baker (2004) described the two-phase ab initio protocol. Kuhlman and others (2003) designed Top7 with it, and Bradley, Misura and Baker (2005) showed high-resolution prediction for small proteins. Leaver-Fay and many others (2011) rewrote the suite as Rosetta3, with modules for poses, score functions, packers and movers, and Alford and others (2017) described its all-atom energy function. The development is shared by the many laboratories of the RosettaCommons.

## References
