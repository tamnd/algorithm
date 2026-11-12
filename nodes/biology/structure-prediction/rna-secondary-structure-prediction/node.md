---
tag: ASNGGH
kind: problem
slug: rna-secondary-structure-prediction
name: RNA secondary structure prediction
aliases:
- RNA folding
- RNA secondary structure folding
- MFE structure prediction
area: biology/structure-prediction
level: core
summary: Compute the base-pairing structure of an RNA sequence, usually by minimum free energy.
prereqs: [rna-secondary-structure, nearest-neighbor-model]
see_also: [nussinov-algorithm, zuker-algorithm, mccaskill-algorithm, rna-pseudoknot-prediction, rna-inverse-folding, cyk-algorithm, sankoff-rna-algorithm, covariance-model]
sources:
  - paper: doi:10.1137/0135006
    title: Ruth Nussinov, George Pieczenik, Jerrold R. Griggs and Daniel J. Kleitman, Algorithms for loop matchings, SIAM Journal on Applied Mathematics 35(1), 1978, pages 68 to 82
    locator: the first dynamic program for the largest number of nested base pairs
  - paper: doi:10.1093/nar/9.1.133
    title: Michael Zuker and Patrick Stiegler, Optimal computer folding of large RNA sequences using thermodynamics and auxiliary information, Nucleic Acids Research 9(1), 1981, pages 133 to 148
    locator: minimum free energy folding with loop energies
  - paper: doi:10.1002/bip.360290621
    title: John S. McCaskill, The equilibrium partition function and base pair binding probabilities for RNA secondary structure, Biopolymers 29(6-7), 1990, pages 1105 to 1119
    locator: the partition function and the base pair probabilities
  - paper: doi:10.1093/bioinformatics/btl246
    title: Chuong B. Do, Daniel A. Woods and Serafim Batzoglou, CONTRAfold, RNA secondary structure prediction without physics-based models, Bioinformatics 22(14), 2006, pages e90 to e98
    locator: learned loop scores and the maximum expected accuracy structure
  - paper: doi:10.1137/17m112720x
    title: Karl Bringmann, Fabrizio Grandoni, Barna Saha and Virginia Vassilevska Williams, Truly subcubic algorithms for language edit distance and RNA folding via fast bounded-difference min-plus product, SIAM Journal on Computing 48(2), 2019, pages 481 to 512
    locator: the first truly subcubic algorithm for base pair maximization
  - paper: doi:10.1137/16M1061771
    title: Amir Abboud, Arturs Backurs and Virginia Vassilevska Williams, If the current clique algorithms are optimal, so is Valiant's parser, SIAM Journal on Computing 47(6), 2018, pages 2527 to 2555
    locator: the conditional lower bound for a generalized RNA folding problem from the k-clique problem
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 10, Section 10.2, the Nussinov and Zuker algorithms, and the stochastic context-free grammars of RNA
  - paper: doi:10.1186/1748-7188-6-26
    title: Ronny Lorenz, Stephan H. Bernhart, Christian Höner zu Siederdissen, Hakim Tafer, Christoph Flamm, Peter F. Stadler and Ivo L. Hofacker, ViennaRNA Package 2.0, Algorithms for Molecular Biology 6, 2011, article 26
    locator: RNAfold, the minimum free energy, the partition function and the centroid and maximum expected accuracy structures
---

RNA secondary structure prediction is the problem of computing, from the sequence of an RNA alone, the set of base pairs that it forms. The standard form asks for a [secondary structure](/rna-secondary-structure/) of minimum free energy in the [nearest-neighbor model](/nearest-neighbor-model/), and the [Zuker algorithm](/zuker-algorithm/) solves it in $O(n^3)$ time by interval dynamic programming. The simplest form, the largest number of nested pairs, is solved by the [Nussinov algorithm](/nussinov-algorithm/). Because the energies are a fit and the molecule is not always in its lowest state, many programs also compute the [partition function](/partition-function/) and the probability of each pair with the [McCaskill algorithm](/mccaskill-algorithm/). With [pseudoknots](/pseudoknot/) the problem changes class; see [RNA pseudoknot prediction](/rna-pseudoknot-prediction/).

## In plain words

An RNA is a chain of four kinds of letters. The chain folds back on itself, and some letters stick to matching letters further along, like the two sides of a zipper. Which letters stick together decides the shape, and the shape decides what the RNA does. Experiments to find the shape are slow and costly, so we want to compute it from the letters alone.

The usual rule is that the molecule takes the fold with the lowest energy. Each run of stuck pairs lowers the energy, and each loop raises it. The number of possible folds grows very fast with the length, so we cannot try them one by one. Instead, we solve the problem for each short piece of the chain and build the answers for longer pieces from them.

## Definition

**Input.** A sequence $s = s_1 \cdots s_n$ over $\{A, C, G, U\}$, and a model: a set $\mathcal{B}$ of allowed pairs (usually AU, GC and GU), a hairpin minimum $\theta$ (usually 3), and a score $E(P)$ for each secondary structure $P$ of $s$.

**Output.** A secondary structure $P^*$ of $s$ with

$$E(P^*) = \min \{ E(P) : P \text{ a secondary structure of } s \}.$$

No pseudoknots are allowed in the standard problem. The two main scores are:

- **Pair counting.** $E(P) = -|P|$, or $-\sum_{(i,j) \in P} w(s_i, s_j)$ with a weight per pair type.
- **Loop energy.** $E(P) = \sum_{\ell} \Delta G(\ell)$ over the loops $\ell$ of $P$, with the Turner 2004 parameters of the nearest-neighbor model.

**Cost model.** Time and space on the [word RAM](/word-ram/), with each loop energy a table lookup in $O(1)$ time. Let $n$ be the length of $s$ and $L$ the largest size of an interior loop that the model allows.

## Variants

- **Minimum free energy (MFE).** The standard form above. The output is one structure.
- **Ensemble properties.** Compute the partition function $Z = \sum_P e^{-E(P)/RT}$, the probability of each pair, or samples of structures from the Boltzmann distribution. See the [McCaskill algorithm](/mccaskill-algorithm/).
- **Maximum expected accuracy (MEA).** Find the structure that maximizes the sum of the probabilities of its pairs and of its unpaired bases, with a weight $\gamma$ for pairs. The centroid structure, the pairs with probability above $1/2$, is a special case. CONTRAfold (Do, Woods and Batzoglou, 2006) uses MEA with learned scores.
- **Suboptimal structures.** List all structures within a given energy of the minimum (Wuchty and others, 1999), or a set of different good structures (Zuker 1989).
- **Constrained folding.** Some pairs are forced or forbidden, or the energy gets pseudo-energy terms from chemical probing data.
- **Comparative folding.** Several related sequences share a structure. The [Sankoff algorithm](/sankoff-rna-algorithm/) aligns and folds them at the same time, a [covariance model](/covariance-model/) describes a family, and [simultaneous alignment and folding](/simultaneous-alignment-and-folding/) collects the methods for it.
- **With pseudoknots.** Crossing pairs are allowed in a restricted class. See [RNA pseudoknot prediction](/rna-pseudoknot-prediction/); for arbitrary pseudoknots the problem is NP-hard ([pseudoknot NP-hardness](/pseudoknot-np-hardness/)).
- **Kinetic folding.** The structure that the molecule reaches in a given time, not at equilibrium. See [RNA folding kinetics](/rna-folding-kinetics/).

## Examples

- **Pair counting.** For GGGAAACCC with AU, GC and GU pairs and $\theta = 3$, there are 20 secondary structures, including the empty one. The largest number of pairs is 3, in the single structure (((...))), with the GC pairs $(1, 9)$, $(2, 8)$ and $(3, 7)$ and a hairpin of three A bases. In a small loop model at a Boltzmann factor of $1/2$ per unit of energy, the [McCaskill algorithm](/mccaskill-algorithm/) page gives this structure a probability of about $0.95$.
- **Pairs alone are not enough.** For GCAAAGCAAAGC, the largest number of pairs is 3, in the single structure ((...)(...)), out of 14 structures. The Nussinov score counts its three pairs, but in a loop energy model the multiloop that $(1, 12)$ closes has a penalty, and the pair $(1, 12)$ stacks on no other pair, so the structure with only the two hairpins can have a lower energy. The [Nussinov algorithm](/nussinov-algorithm/) page traces this example.
- **Stacks win.** In the small model of the [Zuker algorithm](/zuker-algorithm/) page, GGAGGAAAACCCC folds into ((.((....)))) with energy $-2$: the stacks of GC pairs pay for a hairpin and a bulge of one base.

## Known algorithms

- **Nussinov algorithm** (Nussinov and others 1978; Nussinov and Jacobson 1980). Largest number of nested pairs, or largest total weight, in $\Theta(n^3)$ time and $\Theta(n^2)$ space, worst case. See [Nussinov algorithm](/nussinov-algorithm/).
- **Zuker algorithm** (Zuker and Stiegler 1981). Minimum free energy in the loop model, in $O(n^3 + n^2 L^2)$ time and $\Theta(n^2)$ space, worst case. With $L$ a constant (often 30), this is $O(n^3)$. Lyngsø, Zuker and Pedersen (1999) do the interior loops in $O(n^3)$ total time without a bound on $L$, for loop energies of the Turner form. Implemented in mfold, RNAfold and RNAstructure. See [Zuker algorithm](/zuker-algorithm/).
- **McCaskill algorithm** (1990). The partition function and all pair probabilities with the same recurrences, with sums of Boltzmann factors in place of minima, in the same time and space. Stochastic sampling (Ding and Lawrence 2003) draws structures from the distribution. See [McCaskill algorithm](/mccaskill-algorithm/).
- **Grammar methods.** A [probabilistic context-free grammar](/probabilistic-context-free-grammar/) for RNA folds with the [CYK algorithm](/cyk-algorithm/) (the most probable parse) and computes pair probabilities with the [inside-outside algorithm](/inside-outside-algorithm/), in $O(n^3)$ time for a grammar of constant size.
- **Faster for pair counting.** Bringmann, Grandoni, Saha and Vassilevska Williams (2019) solve base pair maximization in $O(n^{3 - \varepsilon})$ time for a constant $\varepsilon > 0$, by a fast [min-plus product](/min-plus-matrix-multiplication/) of matrices whose neighbor entries differ by at most a constant. The method does not extend to the full loop energy model.
- **Heuristics for long sequences.** A bound on the span of a pair, as in RNAplfold, gives $O(n W^2)$ time for a span $W$. LinearFold (Huang and others, 2019) uses beam search from $5'$ to $3'$ in time linear in $n$ for a fixed beam, with no guarantee of an optimum.

## Bounds

- **Upper bounds.** $O(n^3)$ worst case time for the loop energy model with a constant bound on interior loops; $O(n^{3 - \varepsilon})$ for pair counting. Space $\Theta(n^2)$ for all the table methods.
- **Lower bounds.** No lower bound above the trivial $\Omega(n)$ is known for the standard problem. Abboud, Backurs and Vassilevska Williams (2018) show that a much faster algorithm for a generalized form of RNA folding, with a large set of pair types, would give a faster algorithm for the $k$-clique problem. This is a conditional bound, not an unconditional one.
- **Output size.** A structure has at most $n/2$ pairs, so its output is $O(n)$, but the number of structures grows exponentially, about $2.29^n$ for $\theta = 3$ (see [RNA secondary structure](/rna-secondary-structure/)). Exhaustive search is not practical even for $n = 40$.

## Reductions

- **To context-free parsing.** Nested structures are the parse trees of a context-free grammar, so the problem is a weighted parsing problem. The Nussinov recurrence is the CYK algorithm for a grammar with rules for a pair, an unpaired base and a split. See [interval dynamic programming](/interval-dp/) for the common form, of which [matrix chain multiplication](/matrix-chain-multiplication/) is another case.
- **From the min-plus product.** The split step of the Nussinov recurrence is a min-plus product of rows and columns of the table, which is why faster products give faster pair counting.
- **To matching, when crossings are allowed.** Without the rule against crossings, the largest set of pairs is a [maximum matching](/maximum-matching/) in the graph of allowed pairs, which is polynomial. With stacking energies and crossings, the problem is NP-hard; see [pseudoknot NP-hardness](/pseudoknot-np-hardness/).
- **Inverse problem.** Finding a sequence that folds into a given structure is [RNA inverse folding](/rna-inverse-folding/). It calls a folding algorithm as a subroutine.

## Applications

- Functional RNAs: transfer RNA, ribosomal RNA, riboswitches, and other non-coding RNAs, whose function depends on their structure.
- Design of RNA molecules, such as aptamers and RNA switches, together with [inverse folding](/rna-inverse-folding/).
- The search for non-coding RNA genes in genomes, where a low folding energy or a conserved structure is a signal; see [RNA homology search](/rna-homology-search/).
- Access of small RNAs and probes to their targets, which depends on the probability that the target bases are unpaired.
- Messenger RNA design for vaccines and gene expression, where a stable structure changes translation and the life of the molecule.

## References
