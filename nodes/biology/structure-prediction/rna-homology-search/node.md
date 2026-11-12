---
tag: R7KYZT
kind: problem
slug: rna-homology-search
name: RNA structural homology search
aliases:
- Structural RNA search
area: biology/structure-prediction
level: advanced
summary: "Find members of a structured RNA family in a long sequence by scoring each window against a covariance model of the family. Exact search costs O(L(MW + BW^2)) time; filters make it fast."
prereqs: [covariance-model, database-similarity-search]
see_also: [profile-hmm, hmmer, blast, e-value, local-alignment, sliding-window, filtering-technique, banded-alignment]
sources:
  - paper: doi:10.1371/journal.pcbi.0030056
    title: Eric P. Nawrocki and Sean R. Eddy, Query-dependent banding (QDB) for faster RNA similarity searches, PLoS Computational Biology 3(3), 2007, e56
    locator: the cost of CM search with a window W, the subsequence length distributions of the model, the bands with tail loss beta, and the measured average cost with and without bands
  - paper: doi:10.1093/bioinformatics/btt509
    title: Eric P. Nawrocki and Sean R. Eddy, Infernal 1.1, 100-fold faster RNA homology searches, Bioinformatics 29(22), 2013, pages 2933 to 2935
    locator: the filter pipeline of profile HMM stages followed by HMM-banded CM alignment, the E-values from cmcalibrate, and the search times against Infernal 1.0 and an exhaustive search
  - paper: doi:10.1093/nar/22.11.2079
    title: Sean R. Eddy and Richard Durbin, RNA sequence analysis using covariance models, Nucleic Acids Research 22(11), 1994, pages 2079 to 2088
    locator: the covariance model and its use to find tRNA genes by scanning sequences
  - paper: doi:10.1093/nar/gkg006
    title: Sam Griffiths-Jones, Alex Bateman, Mhairi Marshall, Ajay Khanna and Sean R. Eddy, Rfam, an RNA family database, Nucleic Acids Research 31(1), 2003, pages 439 to 441
    locator: families with covariance models, used to annotate sequence databases
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 10, Section 10.3, covariance models and their use for database search (from page 277)
---

RNA structural homology search is the problem of finding all members of a known RNA family in a long sequence, such as a genome, when the family is defined by its consensus secondary structure as well as by its sequence. The family is given as a [covariance model](/covariance-model/), a grammar that scores each base pair together, and the search scores every window of the sequence against it. The exact scan is cubic in the window size for each position, so practical tools such as Infernal put fast [profile HMM](/profile-hmm/) filters and length bands in front of the full model, which gains speed at the price of a small risk to miss real hits.

## In plain words

Many RNA molecules do their work through their shape: parts of the chain fold back and pair with other parts. In a family of such RNAs, the letters often change while the shape stays, because a change on one side of a pair comes with a matching change on the other side.

A search that compares only letters misses these relatives. A structural search uses a model of the family that knows which positions pair. It slides along the genome and asks, at each place, how well a piece of the genome fits both the letters and the pairs of the model.

This exact check is slow. So the tools first run a quick check that looks only at letters, and they keep the slow check for the places that pass it.

## Definition

**Input.**

- A model $G$ of the family: a covariance model with $M$ states, of which $B$ are bifurcation states, built from a consensus structure with $N$ columns. The structure has nested base pairs and no [pseudoknots](/pseudoknot/), and the pair states score all 16 base pairs, so canonical and G-U pairs get the high scores only because they are common in the family.
- A target sequence $x$ of length $L$ over A, C, G and U.
- A largest hit length $W$, usually a little more than the longest expected member, and a score threshold $T$ or an [E-value](/e-value/) threshold.

**Output.** A set of hits $x[i:j)$ with $j - i \le W$. The score of a hit is the best [CYK](/cyk-algorithm/) score of a parse of $x[i:j)$ from the root of $G$, or its inside score, the sum over all parses. The answer holds the hits whose score is at least $T$; when two such hits overlap, the one with the higher score is kept. Each hit comes with its parse, which is an alignment of the hit to the family and a predicted structure for it.

The score depends only on $G$ and the hit, so the problem is a search of all $O(L W)$ windows. It is a [database similarity search](/database-similarity-search/) in which the query is a grammar instead of a sequence or a profile.

## Variants

- **Glocal or local.** A glocal hit aligns the whole model to a part of the target. A local hit may also skip parts of the model, which lets the search find truncated or partial members; the model then gets extra local begin and end moves.
- **CYK or inside.** CYK scores the best parse. The inside algorithm sums over all parses and is the score that Infernal uses for its final E-values.
- **Both strands.** A genome is searched on both strands, which doubles $L$.
- **Sequence only.** A model with no pair states is a profile HMM, and the problem becomes a profile search as in [HMMER](/hmmer/). A single query sequence with no model gives a [BLAST](/blast/) search. Both are fast and both ignore base pairs.
- **Structure only.** Pattern languages that describe stems and loops with lengths and allowed mismatches give a different search problem with no scores from family statistics. This page does not cover them.

## Examples

Take the toy model of the covariance model page: the structure `((...))` with the consensus `GGAAACC`, 25 states and no bifurcation, with integer toy scores. Search the target

`UUGGAAACCUUCUAAAAGUU` ($L = 20$)

with $W = 9$ and $T = 8$. The glocal CYK scores of the best windows are:

| window | bases | score | parse |
|---|---|---|---|
| $x[2:9)$ | `GGAAACC` | 9 | two G-C pairs and the loop `AAA` |
| $x[11:18)$ | `CUAAAAG` | 9 | pairs C-G and U-A, and the loop `AAA` |
| $x[13:20)$ | `AAAAGUU` | 7 | two A-U pairs and a loop with one mismatch |

Two hits reach $T$. The second one shares only three loop bases with the consensus, but both of its pairs are valid, so it scores as high as the consensus itself.

Now use the same scores on the structure `.......`, with no base pairs, which is a profile HMM of the same consensus. Its best window is $x[2:9)$ with score 7, and `CUAAAAG` scores $-1$, below every useful threshold. So a sequence-only model of this family misses the second member, and a structural model finds it.

## Known algorithms

| method | what it does | cost | guarantee |
|---|---|---|---|
| exhaustive CM scan (Eddy and Durbin 1994) | CYK or inside for every end position $j$ and every length $d \le W$ | $O(L (M W + B W^2))$ time, $O(M W + B W^2)$ memory | exact |
| query-dependent banding, QDB (Nawrocki and Eddy 2007) | keeps, for each state $v$, only the lengths in a band $[d_{\min}(v), d_{\max}(v)]$ | worst case as above; observed average about $L N^{1.3}$ against $L N^{2.4}$ without bands | loses parses whose length has model probability below $\beta$ |
| profile HMM filter, then banded CM (Infernal 1.1, 2013) | runs profile HMM stages first and aligns the CM only where they pass, with bands from the HMM alignment | observed about 100 times faster than Infernal 1.0 | heuristic; a hit that fails a filter is lost |

**Exhaustive scan.** CYK on a window needs $\alpha_v(i, j)$ only for $j - i \le W$. Fix the end position $j$ and run over $j$ from left to right; for each $j$ the cells $\alpha_v(j - d, j)$ for $0 \le d \le W$ use cells that end at $j$ or $j - 1$, except the bifurcation states, which use cells that end anywhere in the last $W$ positions. So each $j$ costs $O(M W + B W^2)$ time, and the table keeps the last $W + 1$ columns for the bifurcation children only.

**Query-dependent banding.** For each state $v$, the model defines $\gamma_v(d)$, the probability that the subgraph rooted at $v$ generates a subsequence of length $d$. It can be computed from the model alone, before the search. QDB keeps for each state the band of lengths $d_{\min}(v) \le d \le d_{\max}(v)$ outside of which the tails of $\gamma_v$ have probability less than $\beta$, and fills only those cells. Nawrocki and Eddy used $\beta = 10^{-7}$ and found the search almost as sensitive as without bands. The bands depend on the query model, not on the target, so they are computed once per model. They do not change the worst case, because a model can allow every length.

**Filter pipeline.** Infernal 1.1 first scores the target with a profile HMM built from the CM, which ignores the pairs, in stages of increasing cost and strength. Windows that pass all filter stages go to the CM, and the CM alignment there is banded by the HMM alignment of the window. Nawrocki and Eddy report a search time of 0.44 hours for version 1.1 against 49.31 hours for version 1.0 and 4359 hours for a search with no filters or bands, on their benchmark.

## Bounds

- **Upper bound.** The exhaustive scan is $O(L (M W + B W^2))$ time for every model, and this is the worst case of all the methods above, because bands and filters can be made to pass everything.
- **What drives the cost.** For a model of $N$ columns, $M$ is about $3N$ and $W$ is about $N$, so a scan costs $O(L N^2)$ without bifurcations and up to $O(L N^3)$ with them. The measured exponents of QDB, about 2.4 without bands and 1.3 with them, are averages over the Rfam models of the study and are not bounds.
- **Significance.** A score alone is not a decision. Infernal gives each hit an E-value, the expected number of hits with at least this score in a random target of the same size, from score distributions that the program `cmcalibrate` fits for each model.
- **Loss.** Filters and bands give no guarantee that every hit above $T$ is found. The loss is measured on benchmarks, not proved.

## Reductions

- **From profile search.** A covariance model with no MATP node is a profile HMM, so profile HMM search is the special case with $B = 0$ and no pair states, and its scan costs $O(L M W)$ here, or $O(L M)$ with the HMM recursions that need no length index.
- **To CM alignment.** Each window is a CM alignment problem on a sequence of length at most $W$, so any faster CM alignment gives a faster search.
- **Relation to joint alignment and folding.** When the family has only a few unaligned members, there is no model to search with. Then the members must first be aligned and folded together, the problem of [simultaneous alignment and folding](/simultaneous-alignment-and-folding/), and a model is built from the result.

## Applications

- **Genome annotation.** Rfam keeps a covariance model for each RNA family and uses Infernal to find family members in sequence databases and genomes.
- **Finding new members of a family.** Members whose sequence has drifted but whose structure stays, as in the example above, are found by the structural score where a sequence search misses them.
- **tRNA genes.** Eddy and Durbin used the first covariance models to scan for tRNA genes.

## References
