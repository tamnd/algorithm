---
tag: 7MME3S
kind: problem
slug: ab-initio-protein-folding
name: Ab initio protein folding
aliases:
- Ab initio structure prediction
- De novo structure prediction
area: biology/structure-prediction
level: advanced
summary: Predict the fold of a protein from its sequence and an energy function, without a template structure. It is a global minimization over conformations, NP-hard in lattice models.
prereqs: [protein-structure-prediction, energy-function, energy-landscape]
see_also: [fragment-assembly, rosetta, molecular-dynamics, hp-model, hp-folding-np-completeness, comparative-modeling, alphafold, global-optimization]
sources:
  - paper: doi:10.1006/jmbi.1997.0959
    title: Kim T. Simons, Charles Kooperberg, Enoch Huang and David Baker, Assembly of protein tertiary structures from fragments with similar local sequences using simulated annealing and Bayesian scoring functions, Journal of Molecular Biology 268(1), 1997, 209-225
    locator: the fragment assembly method for prediction without templates
  - paper: doi:10.1016/S0022-2836(02)00698-8
    title: Richard Bonneau et al., De novo prediction of three-dimensional structures for major protein families, Journal of Molecular Biology 322(1), 2002, 65-78
    locator: large-scale de novo prediction with Rosetta and the choice of a model by clustering of decoys
  - paper: doi:10.1126/science.1113801
    title: Philip Bradley, Kira M. S. Misura and David Baker, Toward high-resolution de novo structure prediction for small proteins, Science 309(5742), 2005, 1868-1871
    locator: all-atom refinement of de novo models of small proteins
  - paper: doi:10.1126/science.1208351
    title: Kresten Lindorff-Larsen, Stefano Piana, Ron O. Dror and David E. Shaw, How fast-folding proteins fold, Science 334(6055), 2011, 517-520
    locator: the folding of small fast-folding proteins in long all-atom molecular dynamics simulations
  - paper: doi:10.1126/science.1219021
    title: Ken A. Dill and Justin L. MacCallum, The protein-folding problem, 50 years on, Science 338(6110), 2012, 1042-1046
    locator: physics-based and knowledge-based approaches to prediction without templates
  - paper: doi:10.1126/science.1089427
    title: Brian Kuhlman, Gautam Dantas, Gregory C. Ireton, Gabriele Varani, Barry L. Stoddard and David Baker, Design of a novel globular protein fold with atomic-level accuracy, Science 302(5649), 2003, 1364-1368
    locator: the design of Top7 with Rosetta and its crystal structure
---

Ab initio protein folding is the problem of predicting the three-dimensional structure of a protein from its sequence when no protein of known structure can serve as a template. A method searches the conformations of the chain for a minimum of an [energy function](/energy-function/), as the [thermodynamic hypothesis](/thermodynamic-hypothesis/) suggests. It is the hardest part of [protein structure prediction](/protein-structure-prediction/): even in the [HP lattice model](/hp-model/) the exact problem is [NP-hard](/hp-folding-np-completeness/), and all methods for real proteins are heuristics. The best known are [fragment assembly](/fragment-assembly/) in [Rosetta](/rosetta/) and long [molecular dynamics](/molecular-dynamics/) simulations.

## In plain words

Suppose that you must predict the shape of a protein, and no protein of known shape looks like it. You cannot copy a shape. You have only the sequence and a way to score shapes, a formula that says how stable a shape is.

So you search. You start from a stretched chain, change it a little, keep the changes that improve the score, and sometimes keep a worse change so that you do not get stuck. You do this many times, from many starts, and you get a large set of candidate shapes. Then you pick one, often a shape that many separate runs found. Two things can go wrong: the search never reaches the best shape, or the score is wrong and the best shape by the score is not the real one.

## Definition

**Input.** A sequence $s \in \Sigma^n$ over the 20 amino acids, and an [energy function](/energy-function/) $E_s$ on a conformation space $\Omega(s)$. A full-atom model gives $\Omega(s)$ by the backbone [dihedral angles](/dihedral-angle/) and the side-chain angles. A coarse model keeps the backbone and one centroid for each side chain. A lattice model, such as the HP model, uses lattice walks.

**The restriction.** The method must not use the coordinates of a protein that is related to $s$ by evolution. Two readings of this are in use:

- *Physics-based*, or ab initio in the strict sense: only a physical force field and the sequence. [Molecular dynamics](/molecular-dynamics/) folding is the example.
- *De novo*, or template-free: statistics from the database of known structures are allowed, for example short fragments or statistical potentials, but no template for the whole fold. [Fragment assembly](/fragment-assembly/) is the example.

**Output.** One conformation $\hat{X} \in \Omega(s)$, or a short ranked list. In a blind test, $\hat{X}$ is compared with the experimental structure by [RMSD](/rmsd/), [GDT_TS](/gdt-ts/) or [TM-score](/tm-score/). In CASP, targets with no usable template are scored in a separate category of free modelling.

**The three subproblems.** A method has to solve each of these:

1. *Energy.* $E_s$ must have its minimum at or near the native structure.
2. *Search.* The search must find low-energy conformations of $E_s$, a [global optimization](/global-optimization/) over a space whose size grows exponentially with $n$.
3. *Selection.* From the many decoys that the search returns, choose the one to report.

## Variants

- **Lattice folding.** The HP model on the square or cubic lattice. The energy is exact and the search can be exact for short chains, so this variant is used to study the search part alone. See [HP model](/hp-model/).
- **Coarse-grained folding.** One or a few beads for each residue, with a statistical energy. It is the first stage of most de novo methods.
- **Full-atom folding.** All atoms, with a force field and often explicit water. It is the goal of physics-based methods and of the refinement stage of de novo methods.
- **Folding with restraints.** Predicted contacts from [direct coupling analysis](/direct-coupling-analysis/), or sparse data from experiments, are added to the energy as restraints. The search is then much easier.
- **Learned prediction without templates.** A network such as [AlphaFold](/alphafold/) can predict a fold with no template, from a multiple sequence alignment. It does not minimize an explicit energy, so it is not ab initio in the strict sense, but it solves the same blind task.
- **Template-based modelling.** The opposite case, in which a template exists. See [comparative modelling](/comparative-modeling/) and [protein threading](/protein-threading/).

## Examples

**Search in a toy model.** For the HP sequence HPHPPHHPHH on the square lattice, write folds as words of relative turns with the first bond fixed. There are 4067 self-avoiding words, and 6 of them have the minimum energy $-4$. A random fold is optimal with probability $6/4067 \approx 0.00148$, so independent random samples need about 2029 draws for a 95 percent chance to see an optimum, from $\ln 0.05 / \ln(1 - 6/4067)$. The [fragment assembly](/fragment-assembly/) page solves the same instance with Monte Carlo moves that insert short pieces of known structures, and it finds energy $-4$ within its 2000 steps.

**The time scale of physics-based folding.** A molecular dynamics step is about 2 fs, because the fastest bond vibrations limit it. To simulate 1 ms of folding, a program needs $10^{-3} / (2 \times 10^{-15}) = 5 \times 10^{11}$ steps, each with one evaluation of the forces on all atoms of the protein and the water. Lindorff-Larsen, Piana, Dror and Shaw (2011) folded a set of small fast-folding proteins with such simulations on a special-purpose machine.

**Selection by clustering.** Rosetta runs many independent searches and clusters the low-energy decoys by their pairwise RMSD. It reports the centre of a large cluster, because a fold that many runs reach from different starts is more likely to be a broad, deep basin of the energy, and such basins are more often near the native fold than a single low decoy (Bonneau et al. 2002).

## Known algorithms

| method | representation and energy | search | guarantee |
|---|---|---|---|
| exhaustive enumeration | lattice, HP energy | all folds | exact, exponential time |
| [fragment assembly](/fragment-assembly/) (Simons et al. 1997) | backbone with centroids, statistical energy | Monte Carlo fragment insertion with [simulated annealing](/simulated-annealing/) | none |
| [Rosetta](/rosetta/) ab initio protocol | coarse stage, then full atom | fragment insertion, then packing and minimization | none |
| [molecular dynamics](/molecular-dynamics/) | full atom, physical force field | integration of Newton's equations | none for folding; it samples the dynamics |
| replica exchange and other enhanced sampling | full atom | [parallel tempering](/parallel-tempering/) over temperatures | asymptotic sampling only |
| [AlphaFold](/alphafold/) without templates | learned | a forward pass of a network | none |

Bradley, Misura and Baker (2005) showed that all-atom refinement after fragment assembly can reach high accuracy for some small proteins. For larger proteins without templates, the methods that use coevolution or deep learning are now far more accurate than search alone.

## Bounds

- **Hardness.** In the HP model the decision problem is NP-complete on the square and cubic lattices. See [NP-completeness of HP folding](/hp-folding-np-completeness/). Every exact method for an energy that contains the HP energy as a special case needs superpolynomial time unless $\text{P} = \text{NP}$.
- **Size of the space.** The number of conformations grows exponentially with $n$, as [Levinthal's paradox](/levinthal-paradox/) shows. A search can only sample it.
- **No guarantee for heuristics.** [Simulated annealing](/simulated-annealing/) reaches a global minimum with probability tending to 1 only under logarithmic cooling, whose time is exponential in the depth of the traps. See [convergence of simulated annealing](/simulated-annealing-convergence/). The schedules used in practice are much faster and give no such guarantee.
- **Accuracy depends on the energy.** If the native structure is not the minimum of $E_s$, a perfect search returns a wrong answer. No bound links the error of a computable energy to the error of the prediction.

## Reductions

- **To global optimization.** By the thermodynamic hypothesis, ab initio folding is the minimization of $E_s$ over $\Omega(s)$.
- **From HP folding.** The HP model is a special case of a lattice model with a contact energy, so its NP-hardness carries over.
- **To decoy selection.** Given a set of decoys, the remaining task is to rank them. This is the same task as model quality assessment in template-based modelling.
- **With restraints, toward distance geometry.** When enough distances between residues are known, the problem becomes the embedding of a partial distance matrix in 3D, which is much easier than the search over all conformations.

## Applications

- Predict the folds of protein families that have no member of known structure.
- Design: the forward folding of a designed sequence checks that the design has the intended fold as its minimum. The protein Top7 was designed with Rosetta and has a fold not seen in nature.
- Test energy functions: a function that folds small proteins ab initio is likely to rank models well in other tasks.
- Study folding paths: physics-based simulations show the order in which parts of a small protein form.

## References
