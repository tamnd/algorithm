---
tag: C0K6PX
kind: problem
slug: rna-inverse-folding
name: RNA inverse folding
aliases:
- RNA design
- Inverse RNA folding
- RNA sequence design
- RNAinverse
area: biology/structure-prediction
level: advanced
summary: Find an RNA sequence whose minimum free energy structure is a given target structure.
prereqs: [rna-secondary-structure-prediction, nussinov-algorithm]
see_also: [zuker-algorithm, mccaskill-algorithm, nearest-neighbor-model, local-search, hill-climbing, simulated-annealing, genetic-algorithm, rna-folding-kinetics]
sources:
  - paper: doi:10.1007/BF00818163
    title: Ivo L. Hofacker, Walter Fontana, Peter F. Stadler, L. Sebastian Bonhoeffer, Manfred Tacker and Peter Schuster, Fast folding and comparison of RNA secondary structures, Monatshefte für Chemie 125(2), 1994, pages 167 to 188
    locator: the inverse folding problem and the adaptive walk of RNAinverse
  - paper: doi:10.1093/bioinformatics/btl194
    title: Anke Busch and Rolf Backofen, INFO-RNA, a fast approach to inverse RNA folding, Bioinformatics 22(15), 2006, pages 1823 to 1831
    locator: a start sequence of minimum energy for the target by dynamic programming, then stochastic local search
  - paper: doi:10.1089/cmb.2019.0420
    title: Édouard Bonnet, Paweł Rzążewski and Florian Sikora, Designing RNA secondary structures is hard, Journal of Computational Biology 27(3), 2020, pages 302 to 316
    locator: NP-completeness of design in the Watson-Crick base pair model when some positions have given bases
  - paper: doi:10.1007/s00453-016-0196-x
    title: Jozef Haleš, Alice Héliou, Ján Maňuch, Yann Ponty and Ladislav Stacho, Combinatorial RNA design, designability and structure-approximating algorithm in Watson-Crick and Nussinov-Jacobson energy models, Algorithmica 79(3), 2017, pages 835 to 856
    locator: classes of designable and non-designable structures in base pair models, the linear-time tests, and the structure-approximating algorithm
  - paper: doi:10.1186/1748-7188-6-26
    title: Ronny Lorenz, Stephan H. Bernhart, Christian Höner zu Siederdissen, Hakim Tafer, Christoph Flamm, Peter F. Stadler and Ivo L. Hofacker, ViennaRNA Package 2.0, Algorithms for Molecular Biology 6, 2011, article 26
    locator: RNAinverse in the current Vienna RNA package, with minimum free energy and partition function objectives
---

RNA inverse folding is the reverse of [RNA secondary structure prediction](/rna-secondary-structure-prediction/): given a target [secondary structure](/rna-secondary-structure/), find a sequence that folds into it. In the standard form the target must be the unique minimum free energy structure of the sequence. The problem was posed with the RNAinverse program of Hofacker and others (1994), which solves it by an adaptive walk over sequences and calls a folding algorithm at each step. It is the basic task of the design of RNA molecules. In the Watson-Crick base pair model with some positions fixed to given bases it is NP-complete (Bonnet, Rzążewski and Sikora 2020), and some targets have no design at all.

## In plain words

Folding takes a string of letters and computes its shape. Design goes the other way: we have a shape that we want, and we look for a string that takes it. Many strings can form the wanted pairs, but most of them also have other shapes that are as good or better, and the molecule would then fold wrong.

So a good design must make the wanted shape the clear winner. The usual methods start with a random string that can form the wanted pairs, fold it, compare the result with the target, and change a few letters at a time, keeping the changes that bring the fold closer to the target. Exact search is possible only for short strings, because the number of strings grows very fast with the length.

## Definition

**Input.** A target structure $T$ on $n$ positions, given in dot-bracket notation, and an energy model: allowed pairs, a hairpin minimum $\theta$, and an energy $E(s, P)$ for each sequence $s$ and secondary structure $P$ of $s$.

**Output.** A sequence $s \in \{A, C, G, U\}^n$ such that $T$ is a secondary structure of $s$ and

$$E(s, T) < E(s, P) \quad \text{for every other secondary structure } P \ne T \text{ of } s,$$

or the answer that no such $s$ exists. Such an $s$ is a **design** for $T$, and $T$ is **designable** if it has one.

**The models.**

- **Turner model.** The [nearest-neighbor model](/nearest-neighbor-model/) with the Turner 2004 parameters, AU, GC and GU pairs, $\theta = 3$, no pseudoknots. This is the model of RNAinverse and of most design programs.
- **Base pair models.** $E(s, P) = -|P|$, so the optimal structures are those with the most pairs, as in the [Nussinov algorithm](/nussinov-algorithm/). The Watson-Crick model allows only AU and CG pairs; the Nussinov-Jacobson model gives weights to AU, GC and GU pairs. The code on this page uses AU, GC and GU pairs, $\theta = 3$ and $-1$ per pair.

**Checking a design.** For a given $s$, a design can be checked in polynomial time: compute the optimum with the folding algorithm, compute the number of optimal structures with an unambiguous form of the same recurrence, and test that the count is 1 and that $T$ is optimal. In the base pair model the code does this in $O(n^3)$ time.

**Cost model.** The number of calls of the folding algorithm, each $O(n^3)$ time on the [word RAM](/word-ram/), and the total time.

## Variants

- **Probabilistic design.** Maximize the probability of $T$ in the Boltzmann ensemble of $s$, $e^{-E(s, T)/RT} / Z(s)$, computed with the [McCaskill algorithm](/mccaskill-algorithm/). This rewards a large gap to the other structures.
- **Ensemble defect.** Minimize the expected number of positions whose pairing state differs from $T$, from the pair probabilities.
- **Constraints on the sequence.** Some positions have given bases, the GC content lies in a range, or some motifs are forbidden. With fixed positions, design is NP-complete in the Watson-Crick model.
- **Several targets.** Find a sequence with two given good structures, such as a riboswitch, often with a given barrier between them; see [RNA folding kinetics](/rna-folding-kinetics/).
- **Pseudoknots and complexes.** Targets with crossing pairs, or with several strands that bind each other.
- **Structure approximation.** Change the target a little, for example by adding at most one pair to each helix, so that it becomes designable (Haleš and others 2017).

## Examples

All examples use the base pair model of the code: AU, GC and GU pairs, $\theta = 3$, energy $-1$ per pair, positions numbered from 1. The target is $T = $ ((....)).., with the pairs $(1, 8)$ and $(2, 7)$, and $n = 10$.

- **A design.** GGAAAACCAA has at most 2 pairs, and the only structure with 2 pairs is $T$, so it is a design.
- **Not a design: ties.** GGGAAACCAA can form $T$, but it has 3 optimal structures: ((....)).., (.(...)).. and .((...)).., because the third G can take the place of either of the first two. The cost of the code is 2, the number of other optima.
- **Not a design: a wobble pair.** GGAAAAUCAA also has 3 optima: ((....)).., (.(...)).. and .((...)).., because the U at position 7 can pair with the A at position 3 as well as with the second G, and then either G pairs with the C at position 8.
- **A search.** The adaptive walk of the code, with random seed 1, finds the design CUAGAUAGAU, with the CG pair $(1, 8)$ and the UA pair $(2, 7)$.
- **All small targets are designable here.** A full search over all $4^n$ sequences shows that every secondary structure with $n \le 10$ has a design in this model. The tests check this for $n \le 8$. In other base pair models and for larger $n$, Haleš and others (2017) give targets that have no design.

## Known algorithms

- **Adaptive walk (RNAinverse; Hofacker and others 1994).** Start with a random sequence that can form the pairs of $T$. Mutate one unpaired base, or one pair to another allowed pair, and keep the mutant if its folded structure is not farther from $T$. RNAinverse measures the distance between the minimum free energy structure and $T$, and works on the substructures of $T$ from the inside out. Each step costs one call of the folding algorithm. There is no bound on the number of steps, and the walk can fail on a designable target.
- **INFO-RNA (Busch and Backofen 2006).** Start from a sequence that minimizes $E(s, T)$, found by dynamic programming over $T$, and then improve it by stochastic [local search](/local-search/). The good start makes the search shorter.
- **Other heuristics.** [Simulated annealing](/simulated-annealing/), [genetic algorithms](/genetic-algorithm/) and [hill climbing](/hill-climbing/) on the probability of $T$ or on the ensemble defect, and constraint programming and integer programming for exact or nearly exact search on short targets.
- **Complete search.** Only sequences that can form every pair of $T$ need a test, so for $p$ pairs and $u$ unpaired positions a complete search tests at most $6^p\, 4^u$ sequences, each in $O(n^3)$ time. The code uses it for short targets as an exact baseline.
- **Linear-time tests in base pair models.** Haleš and others (2017) characterize designable structures in base pair models for restricted alphabets, and for the four letters when no base is unpaired, and give $\Theta(n)$ time tests and constructions for large classes of structures.

## Bounds

- **Hardness.** In the Watson-Crick model, with AU and CG pairs and energy $-1$ per pair, deciding whether a target has a design is NP-complete when some positions must have given bases (Bonnet, Rzążewski and Sikora 2020). They left the case without fixed positions open. No hardness proof is known for the Turner model.
- **Membership.** The decision problem is in NP for the base pair models and for the Turner model, because a design is checked in polynomial time.
- **Search space.** Up to $6^p 4^u \le 4^n$ sequences, so the complete search is exponential in $n$ in the worst case.
- **Heuristics.** For the adaptive walk and the other heuristics, no useful worst case bound on the number of folding calls is known; their cost is reported as observed time on benchmark sets of targets.

## Reductions

- **Calls folding.** Every method evaluates candidates with a folding algorithm: the [Zuker algorithm](/zuker-algorithm/) for the minimum free energy, the McCaskill algorithm for probabilities, or the Nussinov algorithm in base pair models.
- **From NP-complete problems.** Bonnet, Rzążewski and Sikora prove hardness by a polynomial reduction to design with fixed bases, which they use to build gadgets in the sequence.
- **To local search.** The heuristics are [local search](/local-search/) over the graph of sequences in which neighbors differ in one base or one pair, with the cost from a folding call.

## Applications

- Synthetic biology: riboswitches, ribozymes, aptamers and RNA parts that sense or control gene expression.
- RNA nanotechnology, where many strands must form a given shape.
- Messenger RNA and vaccine design, with the target structure and the codons as constraints.
- Studies of the map from sequences to structures, such as neutral networks of sequences with the same structure.

## References
