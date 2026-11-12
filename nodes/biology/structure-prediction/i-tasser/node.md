---
tag: KNTH85
kind: algorithm
slug: i-tasser
name: I-TASSER
aliases:
- Iterative threading assembly refinement
area: biology/structure-prediction
level: research
summary: Builds full-length protein models from threading templates by fragment reassembly with replica-exchange Monte Carlo, SPICKER clustering, and a second round of refinement from the cluster centroids.
solves: [protein-structure-prediction]
model: real-ram
complexity:
  vars: {s: the number of Monte Carlo sweeps, r: the number of replicas, n: the number of residues, d: the number of decoys}
  time: {worst: "O(s r n + d^2 n)"}
  space: {extra: "O(r n + d^2)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2008
  people: [Yang Zhang]
  note: Zhang described the I-TASSER server in 2008, building on the TASSER method of Zhang and Skolnick; Roy, Kucukural and Zhang published the full protocol in 2010.
prereqs: [protein-threading, parallel-tempering]
see_also: [protein-fold-recognition, comparative-modeling, fragment-assembly, rosetta, tm-score, metropolis-criterion, hierarchical-clustering-problem, alphafold]
sources:
  - paper: doi:10.1186/1471-2105-9-40
    title: Yang Zhang, I-TASSER server for protein 3D structure prediction, BMC Bioinformatics 9, 2008, 40
    locator: the steps of the method, threading, fragment assembly, clustering and the second iteration
  - paper: doi:10.1038/nprot.2010.5
    title: Ambrish Roy, Alper Kucukural and Yang Zhang, I-TASSER, a unified platform for automated protein structure and function prediction, Nature Protocols 5(4), 2010, 725-738
    locator: the protocol, LOMETS threading, replica-exchange Monte Carlo assembly, SPICKER clustering, the second simulation, and the C-score
  - paper: doi:10.1002/jcc.20011
    title: Yang Zhang and Jeffrey Skolnick, SPICKER, a clustering approach to identify near-native protein folds, Journal of Computational Chemistry 25(6), 2004, 865-871
    locator: the clustering of decoys by the number of structural neighbours within a cutoff
  - paper: doi:10.1093/nar/gkm251
    title: Sitao Wu and Yang Zhang, LOMETS, a local meta-threading-server for protein structure prediction, Nucleic Acids Research 35(10), 2007, 3375-3382
    locator: the meta-threading step that gives the templates
  - paper: doi:10.1103/PhysRevLett.57.2607
    title: Robert H. Swendsen and Jian-Sheng Wang, Replica Monte Carlo simulation of spin glasses, Physical Review Letters 57(21), 1986, 2607-2609
    locator: the idea of running copies of a system at several temperatures and exchanging information between them
  - paper: doi:10.1038/nmeth.3213
    title: Jianyi Yang, Renxiang Yan, Ambrish Roy, Dong Xu, Jonathan Poisson and Yang Zhang, The I-TASSER Suite, protein structure and function prediction, Nature Methods 12(1), 2015, 7-8
    locator: the standalone package of the method
---

I-TASSER (Iterative Threading ASSEmbly Refinement) predicts the structure of a protein by combining templates from [threading](/protein-threading/) with physics-like simulation. It threads the query through a library of known structures, cuts the well-aligned parts of the best templates into fragments, and reassembles them into full-length chains by [replica-exchange Monte Carlo](/parallel-tempering/) on a reduced model of the protein. The regions with no template are built from scratch in the same simulation. It then clusters the decoys with SPICKER, takes the cluster centroids, and runs a second round of simulation from them with extra restraints. The result is a set of full-length models with a confidence score (Zhang 2008; Roy, Kucukural and Zhang 2010).

## In plain words

Suppose you must draw a city map, and you have pieces of old maps of similar cities. Some pieces fit well, some do not, and some parts of the city appear on no old map. You copy the good pieces, guess the missing parts, and then shake the whole drawing many times, keeping changes that make it more consistent.

I-TASSER does this for proteins. It finds known structures that the new sequence may resemble, copies the parts that line up, and joins and fills them by random moves that are scored by an energy. Many runs at different "temperatures" swap their states, so the search does not get stuck. In the end it groups all the shapes it found and takes the biggest group as the answer, since shapes that the search finds again and again are more likely to be right.

## The problem

The input is a protein sequence $a$ of length $n$. The output is a set of three-dimensional models, each with a confidence score. The method solves [protein structure prediction](/protein-structure-prediction/) in its template-based form: it needs at least weak templates, and it is most accurate when [fold recognition](/protein-fold-recognition/) finds good ones. Accuracy is judged by comparing the models to the experimental structure, for example with [TM-score](/tm-score/).

Inside, the method uses two general tools that this page defines precisely and that the implementation tests:

- **Replica-exchange Monte Carlo.** Given an energy $E$ on states, a symmetric proposal of local moves, and temperatures $T_1 < \cdots < T_R$, sample each replica $r$ from the Boltzmann distribution $\pi_r(x) \propto e^{-E(x)/T_r}$.
- **SPICKER clustering.** Given decoys $x_1, \ldots, x_d$, a distance (the RMSD of the $C_\alpha$ atoms) and a cutoff $\delta$, repeatedly pick the decoy with the most neighbours within $\delta$ among the decoys left, and remove it with its neighbours as one cluster.

Costs are in the [real RAM](/real-ram/) model, with one local Monte Carlo move costing $O(n)$ and one RMSD costing $O(n)$.

## The algorithm

```pseudo id=main
I-TASSER(a, T)                           ▷ T: templates of a from threading (LOMETS)
L1  S ← start chains from the aligned fragments of T; unaligned regions built ab initio
L2  D ← REMC(E, S)                       ▷ E: template, contact and statistical terms
L3  C ← SPICKER(D, δ)                    ▷ clusters, largest first
L4  E' ← E plus restraints from the centroids of C and from structural analogs of them
L5  D' ← REMC(E', centroids of C)
L6  m ← the lowest-energy decoy of the largest cluster of D'
L7  return m and the other models, each with a C-score

REMC(E, S)                               ▷ temperatures T_1 < ... < T_R
L8  for sweep ← 1 to N do
L9      for each replica r do a Metropolis move at temperature T_r
L10     pick r at random; swap the states of r and r + 1 with probability min(1, exp((1/T_r − 1/T_{r+1})(E_r − E_{r+1})))
L11 return the states of the low-temperature replicas along the run

SPICKER(D, δ)
L12 while D ≠ ∅ do
L13     c ← the decoy of D with the most neighbours in D within distance δ
L14     output c and its neighbours as one cluster; remove them from D
```

The Metropolis move of line L9 proposes a local change of the chain, such as moving a fragment, and accepts it with probability $\min(1, e^{-\Delta E / T_r})$ ([Metropolis criterion](/metropolis-criterion/)). The swap of line L10 lets a state found at a high temperature, where barriers are easy to cross, move down to the low temperatures, where it is refined. In the real program, the reduced model has one or a few points per residue on a lattice, the energy combines restraints from the templates, predicted contacts, hydrogen bonds and statistical terms, and the second round also removes steric clashes. Full-atom models are built from the final reduced models. The C-score combines the threading Z-scores of the templates with the size and the tightness of the cluster.

## Example

**One swap.** Let replica 1 be at $T_1 = 1$ with energy $E_1 = -3$, and replica 2 at $T_2 = 2$ with $E_2 = -5$. The exponent of line L10 is $(1 - 0.5)(-3 - (-5)) = 1 > 0$, so the swap is always accepted: the better state moves to the colder replica. In the opposite case, $E_1 = -5$ and $E_2 = -3$, the exponent is $0.5 \cdot (-2) = -1$, and the swap happens with probability $e^{-1} \approx 0.37$.

**SPICKER on eight decoys.** Let the decoys be points on a line, $x = (1.0, 1.4, 2.1, 2.3, 2.6, 5.0, 5.3, 9.0)$, numbered 0 to 7, with the distance $|x_i - x_j|$ and the cutoff $\delta = 0.8$. Each decoy counts itself as a neighbour.

| decoy | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| position | 1.0 | 1.4 | 2.1 | 2.3 | 2.6 | 5.0 | 5.3 | 9.0 |
| neighbours | 2 | 3 | 4 | 3 | 3 | 2 | 2 | 1 |

Round 1 picks decoy 2 with 4 neighbours, and the first cluster is $\{1, 2, 3, 4\}$. Among the decoys left, $\{0, 5, 6, 7\}$, decoy 0 has lost its neighbour 1, so the counts are 1, 2, 2, 1. Round 2 picks decoy 5 (the tie with 6 goes to the lower number), with cluster $\{5, 6\}$. Then $\{0\}$ and $\{7\}$ are single clusters. The largest cluster, around position 2.1, is the region the search visited most often, and line L6 takes the best decoy in it.

## Correctness

I-TASSER is a heuristic, so the claims are about its two tools, not about the final model.

- **Replica-exchange sampling is exact in the limit.** With a symmetric proposal, the Metropolis move at $T_r$ satisfies detailed balance for $\pi_r$, and the swap move of line L10 satisfies detailed balance for the product $\pi_1 \times \cdots \times \pi_R$. So the joint chain has this product as a stationary distribution, and if the chain is irreducible and aperiodic, the states of replica $r$ follow $\pi_r$ in the long run. The test of the implementation compares the visited states of each replica with the exact Boltzmann distribution of a small landscape.
- **SPICKER returns a partition.** Each round removes at least the chosen decoy, so the loop ends after at most $d$ rounds, and each decoy belongs to exactly one cluster. Each center has the most neighbours among the decoys left in its round.
- **The largest cluster is a sound choice, not a proof.** At low temperature, the stationary distribution puts most weight on low free energy, which is a wide basin of low energy, not only a deep point. A large cluster marks such a basin. Whether this basin is the native fold depends on the energy and the templates.

The full proofs of the first two points are in the proof file below.

## Complexity

One sweep of lines L9 and L10 makes $R$ local moves, $O(n)$ each with an energy that is updated locally, so $N$ sweeps cost $O(N R n)$, written $O(s r n)$ in the front matter. SPICKER computes all $d^2$ pairwise distances, $O(n)$ each with a fixed superposition, and stores the neighbour lists, $O(d^2)$ space in the worst case; the rounds cost $O(d^2)$ in total. The whole method takes $O(s r n + d^2 n)$ time plus the threading step, which is a library search. In practice the threading and the simulations dominate, and a run on one protein can take many hours.

## Properties

- **Randomized.** Different seeds give different decoys and possibly different models.
- **Template-dependent.** The accuracy follows the quality of the threading templates. Without good templates the method falls back to fragment-based ab initio folding, which works only for small proteins.
- **Consensus by density.** The choice of the largest cluster turns the many runs into a vote, which is more robust than taking the single lowest-energy decoy.
- **Confidence.** The C-score correlates with the TM-score of the model to the native structure, so a user can judge a model without the native structure.

## Variants and improvements

- **TASSER.** The earlier method of Zhang and Skolnick, on which I-TASSER builds, with the same idea of template fragment assembly on a lattice model.
- **Adaptive clustering cutoff.** SPICKER chooses its cutoff from the spread of the decoys, so that clustering works both for tight and for diverse decoy sets.
- **Function prediction.** The I-TASSER platform also compares the final models with proteins of known function to predict ligand-binding sites and function.
- **Contact and distance restraints.** Later versions add predicted contacts, and then distances from deep learning, to the energy of the simulation.

## When to use it

Use I-TASSER when the query has templates of medium or weak quality, and a full-length model with an estimate of its accuracy is needed. With a close homolog, plain [comparative modeling](/comparative-modeling/) is faster and as accurate. For most single-chain proteins today, deep learning methods such as [AlphaFold](/alphafold/) give more accurate models, but I-TASSER remains a template-based pipeline with interpretable steps and a built-in confidence score.

## Pitfalls

- **Asymmetric proposals.** If a move is more likely in one direction than in the other, the plain Metropolis rule samples the wrong distribution. Use the Hastings correction or symmetric moves.
- **Too few replicas.** If neighbouring temperatures are far apart, swaps are almost never accepted and the replicas behave like independent runs.
- **Clustering correlated samples.** Consecutive states of one Monte Carlo run are almost the same, so they inflate the cluster of the current basin. Thin the samples, as in the implementation, and use many runs.
- **Reading the C-score as accuracy.** It is a predictor of accuracy trained on benchmark data, not a measurement of it.

## Implementations

## History

Zhang and Skolnick developed TASSER, which assembled template fragments on a lattice model, and SPICKER (2004) to pick the model from the decoys. Zhang (2008) described the I-TASSER server, which added iterations of threading and assembly, and the method was ranked as the top server in the CASP7 and CASP8 experiments, as Roy, Kucukural and Zhang (2010) report. The 2010 protocol paper gave the full pipeline with function prediction, and the I-TASSER Suite of 2015 made it available as a standalone package. Replica exchange itself goes back to the replica Monte Carlo method of Swendsen and Wang (1986).

## References
