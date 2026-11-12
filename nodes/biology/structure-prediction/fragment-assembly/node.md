---
tag: B7NM52
kind: algorithm
slug: fragment-assembly
name: Fragment assembly
aliases:
- Rosetta fragment assembly
area: biology/structure-prediction
level: advanced
summary: Predicts a protein fold without a template by Monte Carlo moves that copy the backbone angles of short fragments of known structures into the chain, under simulated annealing.
solves: [ab-initio-protein-folding]
model: real-ram
complexity:
  vars: {n: the number of residues, S: the total number of Monte Carlo steps}
  time: {worst: O(S n)}
  space: {extra: O(n)}
properties: {deterministic: false, iterative: true, anytime: true, population: false}
history:
  year: 1997
  people: [Kim T. Simons, Charles Kooperberg, Enoch Huang, David Baker]
  note: Simons, Kooperberg, Huang and Baker introduced the method in 1997 as the search of Rosetta. It became the standard method for template-free prediction until deep learning methods replaced it.
prereqs: [ab-initio-protein-folding, simulated-annealing, hp-model]
see_also: [rosetta, energy-landscape, energy-function, metropolis-hastings, dihedral-angle, protein-secondary-structure, molecular-dynamics, alphafold]
sources:
  - paper: doi:10.1006/jmbi.1997.0959
    title: Kim T. Simons, Charles Kooperberg, Enoch Huang and David Baker, Assembly of protein tertiary structures from fragments with similar local sequences using simulated annealing and Bayesian scoring functions, Journal of Molecular Biology 268(1), 1997, 209-225
    locator: the fragment library, the fragment insertion move, the simulated annealing search and the Bayesian score
  - paper: doi:10.1002/(SICI)1097-0134(19990101)34:1<82::AID-PROT7>3.0.CO;2-A
    title: Kim T. Simons, Ingo Ruczinski, Charles Kooperberg, Brian A. Fox, Chris Bystroff and David Baker, Improved recognition of native-like protein structures using a combination of sequence-dependent and sequence-independent features of proteins, Proteins 34(1), 1999, 82-95
    locator: the terms of the coarse score that guides the assembly
  - paper: doi:10.1016/S0076-6879(04)83004-0
    title: Carol A. Rohl, Charlie E. M. Strauss, Kira M. S. Misura and David Baker, Protein structure prediction using Rosetta, Methods in Enzymology 383, 2004, 66-93
    locator: the stages of the ab initio protocol with 9-residue and 3-residue fragments
  - paper: doi:10.1002/j.1460-2075.1986.tb04287.x
    title: T. Alwyn Jones and Søren Thirup, Using known substructures in protein model building and crystallography, The EMBO Journal 5(4), 1986, 819-822
    locator: the observation that short pieces of known structures fit new structures well
  - paper: doi:10.1016/S0022-2836(02)00698-8
    title: Richard Bonneau et al., De novo prediction of three-dimensional structures for major protein families, Journal of Molecular Biology 322(1), 2002, 65-78
    locator: large-scale use of fragment assembly and the clustering of decoys
---

Fragment assembly predicts the fold of a protein without a template. It builds the backbone from short pieces of proteins of known structure. For each window of 9 or 3 consecutive residues of the target, a library holds fragments from known structures whose local sequence is similar. One Monte Carlo move copies the backbone [dihedral angles](/dihedral-angle/) of one fragment into one window, the new chain is scored with a coarse [energy function](/energy-function/), and the move is accepted by the [Metropolis criterion](/metropolis-criterion/) while the temperature falls, as in [simulated annealing](/simulated-annealing/). Simons, Kooperberg, Huang and Baker introduced it in 1997, and it is the search of the [Rosetta](/rosetta/) ab initio protocol. The name is like that of [genome assembly](/genome-assembly-problem/), which joins overlapping DNA reads into one sequence, but the two problems are different.

## In plain words

Short pieces of protein chains, about nine building blocks long, take only a small number of shapes. A piece with a given local sequence often has the same shape in many unrelated proteins. So a program can guess the shape of each short piece of a new protein from known proteins, even when no known protein has the same overall fold.

Fragment assembly starts with a straight chain. At each step it picks a place on the chain and copies in one of the known shapes for that place. The rest of the chain swings to a new position. A better chain is kept. A worse one is sometimes kept, less often as the run goes on. Long pieces come first, for large changes, and short pieces come at the end, for small corrections. Many runs give many candidate folds, and one of the common ones is the answer.

## The problem

The input is a protein sequence $s$ of length $n$, an energy function $E$ on conformations, and a fragment library. A conformation is given by its backbone torsion angles $(\phi_i, \psi_i, \omega_i)$ for each residue $i$, with fixed bond lengths and angles. The library has, for each window start $j$ and fragment length $k$, a list $F_j$ of $k$-residue angle sequences, taken from known structures whose sequence near the fragment is similar to $s_j \cdots s_{j+k-1}$. The goal is a conformation of low energy, which by the [thermodynamic hypothesis](/thermodynamic-hypothesis/) should be near the native fold. This is the search part of [ab initio protein folding](/ab-initio-protein-folding/).

The implementation on this page uses a toy model with the same structure, so that brute force can check it. The chain lies on the square lattice. Residue 0 is at $(0, 0)$ and residue 1 at $(1, 0)$. Each later residue turns left (L), goes straight (S) or turns right (R) from the direction of the last bond. So a conformation is a word $w \in \{L, S, R\}^{n-2}$, and each letter plays the role of one torsion angle. The energy is the [HP model](/hp-model/) energy, minus the number of contacts between H residues, and a conformation in which two residues are at the same site has energy $+\infty$. A fragment of length $k$ is a word of $k$ letters, and a window starts at $j \in \{0, \ldots, n - 2 - k\}$.

## The algorithm

```pseudo id=main
FRAGMENT-ASSEMBLY(s, stages, T_start, T_end)
L1  w ← the extended chain S S … S of n − 2 letters
L2  E ← SCORE(s, w);  (E*, w*) ← (E, w)
L3  for each stage (k, F, K) in order do            ▷ long fragments first
L4      for t ← 0 to K − 1 do
L5          T ← T_start · (T_end / T_start)^(t / (K − 1))
L6          j ← a uniform window start in 0 … n − 2 − k
L7          f ← a uniform fragment from F_j
L8          w′ ← w with w[j … j + k − 1] replaced by f
L9          E′ ← SCORE(s, w′)                       ▷ +∞ when two residues collide
L10         if E′ ≤ E or random() < exp(−(E′ − E) / T) then
L11             w ← w′;  E ← E′
L12             if E < E* then
L13                 (E*, w*) ← (E, w)
L14 return (E*, w*)
```

SCORE builds the coordinates from the word and counts the contacts with a hash table of the sites. random() is uniform in $[0, 1)$, so line L10 accepts a worse move with probability $e^{-(E' - E)/T}$ and never accepts a collision. Each stage restarts the geometric schedule of line L5, and a stage with $K = 1$ uses $T = T_\text{end}$. The library for a stage is made once before the search. The implementation picks, for window $j$, the distinct fragments of the known words whose HP pattern over the $k + 2$ residues that the $k$ turns involve has the smallest [Hamming distance](/hamming-distance/) to $s_j \cdots s_{j+k+1}$.

## Example

Take the sequence HPHPPHHPHH, so $n = 10$ and a word has 8 letters. The "known structures" are 8 HP strings with a word each, for example (HHPHPPPPHH, LLRLSLLR) and (PHPPHPPHHP, LRRLRRSL). The first stage uses $k = 3$ with the 4 closest fragments for each of the 6 windows, for 1500 steps. For window 0 the target pattern is HPHPP, and the library is LRL, LSL, LLS and LSS. The second stage uses $k = 1$ with all three letters at each of the 8 windows, for 500 steps. Both stages cool from $T = 2.0$ to $T = 0.1$. The first ten steps with the random seed 0:

| step | $T$ | $j$ | $f$ | $w'$ | $E'$ | result |
|---|---|---|---|---|---|---|
| 0 | 2.000 | 3 | LSL | SSSLSLSS | 0 | accept |
| 1 | 1.996 | 4 | RSR | SSSLRSRS | 0 | accept |
| 2 | 1.992 | 2 | SLS | SSSLSSRS | 0 | accept |
| 3 | 1.988 | 1 | SLL | SSLLSSRS | $-1$ | accept, new best |
| 4 | 1.984 | 0 | LLS | LLSLSSRS | $-1$ | accept |
| 5 | 1.980 | 4 | LSL | LLSLLSLS | $+\infty$ | reject, collision |
| 6 | 1.976 | 5 | LLR | LLSLSLLR | $+\infty$ | reject, collision |
| 7 | 1.972 | 5 | SLS | LLSLSSLS | $-1$ | accept |
| 8 | 1.968 | 0 | LLS | LLSLSSLS | $-1$ | accept, no change |
| 9 | 1.964 | 4 | LSL | LLSLLSLS | $+\infty$ | reject, collision |

At step 12 the fragment LRR at window 4 gives LLRRLRRS with $E = -3$. The 3-residue stage stays at $-3$ for the rest of its 1500 steps: 532 of its proposals collide and 521 are accepted. The library of this stage can reach only 567 valid words from the extended chain, and only one of them, LRLLRLLS, is optimal. In the second stage, at step 128 with $T = 0.927$, the letter L at window 0 gives LRLLSSLL with $E = -4$. The run returns $(-4, \text{LRLLSSLL})$. Brute force over all $3^8 = 6561$ words finds the minimum $-4$, reached by 6 words, so this run finds an optimum. The last word of the run, LSLLRSRR with $E = -3$, is worse than the best one, which is why line L13 keeps the best.

## Correctness

Fragment assembly is a heuristic for an [NP-hard](/hp-folding-np-completeness/) problem, so its correctness is a set of invariants, not a guarantee of an optimum.

1. **Every state is valid.** Line L1 starts from the straight chain, which has no collision, and line L10 never accepts $E' = +\infty$. So the current word is always a self-avoiding conformation.
2. **The returned pair is the best visited state.** After each step, $E^*$ is the minimum of the energies of all accepted states and of the start, and $E^* = \text{SCORE}(s, w^*)$.
3. **Equilibrium at a fixed temperature.** If $T$ is constant and each $F_j$ holds all $3^k$ words, the proposal of lines L6 to L8 is symmetric, so the chain satisfies [detailed balance](/detailed-balance/) with the Boltzmann distribution $e^{-E(w)/T}/Z$ on the valid words.
4. **No finite-time guarantee.** With a geometric schedule and a finite number of steps, no bound holds on the gap $E^* - \min E$. The asymptotic result for logarithmic schedules is the [convergence theorem of simulated annealing](/simulated-annealing-convergence/), and it needs a library that connects all valid words.

With a real library, claim 3 fails: the fragments are a small biased set, and the proposal is not symmetric. This bias is the purpose of the method, since it keeps the local structure native-like. The proofs of claims 1 to 3 are below.

## Complexity

Line L9 builds $n$ coordinates and checks the $4$ neighbours of each H residue in the hash table, in $O(n)$ expected time. The other lines of a step take $O(k) \subseteq O(n)$ time. So $S$ steps take $O(S n)$ time, and the search uses $O(n)$ extra space besides the library. Picking a library with $P$ positions in the known words costs $O(n P k)$ distance computations for one fragment length, plus the sort.

In Rosetta the costs are higher by constants, not by order. A move changes the torsions of $k$ residues, and the coordinates of all residues after the window move with them, so a rebuild takes $O(n)$ time. The real cost is the number of steps: one run takes thousands of steps, and a prediction uses many independent runs.

## Properties

- **Randomized.** Different seeds give different decoys. A fixed seed gives the same run.
- **Anytime.** Stop it at any step, and $(E^*, w^*)$ is a valid answer.
- **Local structure is native-like by construction.** Every window of the chain has the angles of some known fragment, until a later move overwrites part of it. So the secondary structure of a decoy is usually plausible even when its fold is wrong.
- **Large moves.** One fragment insertion changes several torsions at once, and the end of the chain far from the window can move a long distance. Early in a run this crosses barriers that single-angle moves cannot cross. Late in a run, when the chain is compact, most such moves collide, which is why the last stage uses short fragments.
- **The move set defines the landscape.** The same energy has different local minima under 9-residue moves, 3-residue moves and 1-letter moves. See [energy landscape](/energy-landscape/).

## Variants and improvements

- **Stages of the score.** Rosetta begins with a score that has only a repulsion term, so that the chain leaves the extended state, and adds terms for secondary structure pairing, burial and compactness in later stages (Rohl et al. 2004).
- **Full-atom refinement.** The low-resolution decoys get side chains and an all-atom energy, and are then refined by small moves and minimization. See [Rosetta](/rosetta/).
- **Selection by clustering.** Many short runs give many decoys. The centre of the largest cluster, by [RMSD](/rmsd/), is reported (Bonneau et al. 2002).
- **Better libraries.** The library can be picked with sequence profiles and predicted [secondary structure](/protein-secondary-structure/), not only with the sequence. With NMR chemical shifts, the library can be picked from the measured shifts.
- **Restraints.** Predicted contacts from [direct coupling analysis](/direct-coupling-analysis/), or sparse experimental distances, can be added to the score, which makes the search much easier.
- **Other samplers.** Replica exchange over temperatures, see [parallel tempering](/parallel-tempering/), in place of one annealing schedule.

## When to use it

Use fragment assembly for a protein, or a domain, with no template, of up to about 100 to 150 residues, when a coarse model is useful. It is also a tool for loops and for parts of a model that a template does not cover. For most targets, a learned method such as [AlphaFold](/alphafold/) is now more accurate. Fragment assembly is still useful as a sampler: to make many different decoys, to check that a designed sequence folds to its target, and to combine with sparse data. If a template exists, use [comparative modelling](/comparative-modeling/) first.

## Pitfalls

- **Leakage in benchmarks.** When the method is tested on a protein of known structure, fragments from that protein and its homologs must not be in the library. Otherwise the test measures copying, not prediction.
- **Windows without fragments.** Each window that a stage can choose needs a nonempty list. A gap in the library freezes those angles.
- **One run is not a prediction.** A single run returns one decoy from one basin. Run many, and select by clustering or by a better energy.
- **Returning the last state.** At a finite temperature the last state can be worse than the best, as in the example. Keep the best.
- **Temperature in the wrong units.** The scale of $T$ must match the scale of the energy differences. For a new score, set the start temperature so that a reasonable fraction of worse moves are accepted.
- **Trust in a low energy.** A coarse score can rank a wrong fold below the native one. A low $E^*$ is evidence about the search, not about the fold.

## Implementations

## History

Jones and Thirup (1986) observed that short pieces of known protein structures fit the chains of new structures well, and used them to build models into electron density maps. Simons, Kooperberg, Huang and Baker (1997) made fragments the move of a Monte Carlo search, with a Bayesian score that came from known structures, and called the program Rosetta. Simons and others (1999) improved the score. Rosetta with fragment assembly did well in the new fold category of the CASP experiments from 1998 on. Bonneau and others (2002) used it to predict structures for many protein families. Rohl, Strauss, Misura and Baker (2004) described the protocol with 9-residue and 3-residue stages that later versions keep.

## References
