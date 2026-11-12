---
tag: EM1WEQ
kind: problem
slug: ancestral-recombination-graph-inference
name: Ancestral recombination graph inference
aliases:
- ARG inference
area: biology/phylogenetics
level: research
summary: Infer an ancestral recombination graph consistent with sampled sequences.
prereqs: [ancestral-recombination-graph, four-gamete-condition]
see_also: [perfect-phylogeny, gusfield-perfect-phylogeny, phylogenetic-network, spr-distance, activity-selection, zero-one-bfs, importance-sampling, np-hard]
sources:
  - paper: doi:10.1093/genetics/111.1.147
    title: R. R. Hudson and N. L. Kaplan, Statistical properties of the number of recombination events in the history of a sample of DNA sequences, Genetics 111(1), 1985, 147-164
    locator: the lower bound R_M from pairs of sites that fail the four-gamete test, and its procedure on intervals
  - paper: doi:10.1093/genetics/163.1.375
    title: S. R. Myers and R. C. Griffiths, Bounds on the minimum number of recombination events in a sample history, Genetics 163(1), 2003, 375-394
    locator: the haplotype bound R_h, and the composition of local bounds along the sequence by dynamic programming
  - paper: doi:10.1089/106652701300099119
    title: L. Wang, K. Zhang and L. Zhang, Perfect phylogenetic networks with recombination, Journal of Computational Biology 8(1), 2001, 69-78
    locator: NP-hardness of the minimum number of recombinations, and the networks whose recombination cycles are disjoint
  - paper: doi:10.1142/S0219720004000521
    title: D. Gusfield, S. Eddhu and C. Langley, Optimal, efficient reconstruction of phylogenetic networks with constrained recombination, Journal of Bioinformatics and Computational Biology 2(1), 2004, 173-213
    locator: the complete polynomial-time algorithm for galled trees, and the proof that a galled tree, when one exists, has the least number of recombinations
  - paper: doi:10.1016/j.jcss.2004.12.009
    title: D. Gusfield, Optimal, efficient reconstruction of root-unknown phylogenetic networks with constrained and structured recombination, Journal of Computer and System Sciences 70(3), 2005, 381-398
    locator: the galled tree algorithm when the ancestral sequence is not known
  - paper: doi:10.1089/cmb.1996.3.479
    title: R. C. Griffiths and P. Marjoram, Ancestral inference from samples of DNA sequences with recombination, Journal of Computational Biology 3(4), 1996, 479-502
    locator: likelihood inference over ancestral recombination graphs by importance sampling
  - paper: doi:10.1089/cmb.2005.12.147
    title: Y. S. Song and J. Hein, Constructing minimal ancestral recombination graphs, Journal of Computational Biology 12(2), 2005, 147-169
    locator: exact minimum histories by a search over the marginal trees along the sequence
  - paper: doi:10.1007/11557067_20
    title: R. B. Lyngsø, Y. S. Song and J. Hein, Minimum recombination histories by branch and bound, Algorithms in Bioinformatics (WABI 2005), Lecture Notes in Computer Science 3692, 2005, 239-250
    locator: the backward search over ancestral states with coalescence, mutation and recombination steps, pruned by lower bounds
  - paper: doi:10.1093/bioinformatics/bti1033
    title: Y. S. Song, Y. Wu and D. Gusfield, Efficient computation of close lower and upper bounds on the minimum number of recombinations in biological sequence evolution, Bioinformatics 21(suppl 1), 2005, i413-i422
    locator: the HapBound lower bound by integer programming and the SHRUB upper bound by a constructed history
  - paper: doi:10.1371/journal.pgen.1004342
    title: M. D. Rasmussen, M. J. Hubisz, I. Gronau and A. Siepel, Genome-wide inference of ancestral recombination graphs, PLoS Genetics 10(5), 2014, e1004342
    locator: ARGweaver, sampling of ARGs under the sequentially Markov coalescent by Markov chain Monte Carlo
  - paper: doi:10.1038/s41588-019-0483-y
    title: J. Kelleher, Y. Wong, A. W. Wohns, C. Fadil, P. K. Albers and G. McVean, Inferring whole-genome histories in large population datasets, Nature Genetics 51(9), 2019, 1330-1338
    locator: tsinfer, a heuristic that infers a tree sequence from many genomes by ancestor matching
  - paper: doi:10.1038/s41588-019-0484-x
    title: L. Speidel, M. Forest, S. Shi and S. R. Myers, A method for genome-wide genealogy estimation for thousands of samples, Nature Genetics 51(9), 2019, 1321-1329
    locator: Relate, which builds one tree per region from a hidden Markov model of copying and then fits branch lengths
---

ARG inference asks for an [ancestral recombination graph](/ancestral-recombination-graph/) that explains a set of sampled sequences. In its combinatorial form the input is a binary matrix, one row per sequence and one column per site in order along the sequence, under the infinite-sites model: each site mutates once in the whole history. The goal is a graph with the least number of recombination nodes, $R_{\min}$. When $R_{\min} = 0$ the data fit a [perfect phylogeny](/perfect-phylogeny/), which the [four-gamete test](/four-gamete-condition/) detects. In general the problem is [NP-hard](/np-hard/) (Wang, Zhang and Zhang 2001), so practical methods compute lower bounds such as $R_M$ of Hudson and Kaplan (1985), exact values for small data, or networks of a restricted shape. In statistical form the goal is a distribution over graphs, or a good estimate, under the coalescent with recombination.

## In plain words

We have the DNA of a few people at a few places along a chromosome. Each place changed once in the past. If no piece of DNA ever came from two parents, one family tree would explain every place. Recombination breaks this: the left part of a chromosome may follow one family tree and the right part another. We want a history that explains the data with as few recombination events as possible. A quick test shows that some recombination is needed. Look at two places. If all four pairs of letters occur, then no single tree explains them, so some event must lie between them. Counting such pairs carefully gives a lower bound. Finding the true least number is hard in general, but small cases can be searched, and some special shapes of history are fast to find.

## Definition

Let $M$ be an $n \times m$ matrix with entries 0 and 1. Row $i$ is a sequence and column $j$ is a site, and the sites are in order along the sequence. Under the infinite-sites model, each site mutates once. In the *rooted* version the ancestral state of every site is 0, so the root sequence is $0 \cdots 0$.

An *ARG for* $M$ is an ancestral recombination graph on $n$ samples, with breakpoints only between sites, and with each site $j$ marked on one edge that is a branch of the marginal tree at $j$. The marked edge carries the change from 0 to 1. The sequence of each sample is read from the marks: sample $i$ has a 1 at site $j$ exactly when its path at site $j$ goes through the edge marked $j$. The ARG *explains* $M$ when this gives row $i$ for every $i$.

**The problem.** Given $M$, find an ARG that explains $M$ with the least number of recombination nodes. This number is $R_{\min}(M)$. The decision version asks whether $R_{\min}(M) \le k$.

**Incompatible pairs.** Sites $i$ and $j$ are *incompatible* if the rows of $M$, with the root row $0 \cdots 0$ added in the rooted version, show all four of $00, 01, 10, 11$ at $i$ and $j$. On a single tree with one mutation per site this is impossible. So every ARG that explains $M$ has a recombination with a breakpoint between $i$ and $j$.

## Variants

- **Root unknown.** No root row is added, and the ancestral state of each site is free. The four-gamete test then uses the rows only. Gusfield (2005) solved the galled tree case for this version as well.
- **Galled trees.** The recombination cycles of the network must be disjoint. Wang, Zhang and Zhang (2001) introduced this case. Gusfield, Eddhu and Langley (2004) showed that their algorithm was incomplete, and gave a complete polynomial-time algorithm. They also proved that when a galled tree exists, it has the least number of recombinations over all networks for the data.
- **Bounds only.** Compute a lower bound such as $R_M$ or $R_h$, and an upper bound from a constructed history, such as SHRUB (Song, Wu and Gusfield 2005). When the two meet, $R_{\min}$ is known.
- **Finite sites.** Allow recurrent or back mutation, and minimize a weighted count of recombinations and extra mutations.
- **Statistical inference.** Sample ARGs from the posterior under the coalescent with recombination (Griffiths and Marjoram 1996, by [importance sampling](/importance-sampling/); ARGweaver, Rasmussen et al. 2014), or build one good estimate for many genomes quickly (tsinfer, Kelleher et al. 2019; Relate, Speidel et al. 2019). These methods do not minimize $R$.
- **Unknown phase.** The input gives genotypes, not haplotypes, so each row is the sum of two unknown sequences.

## Examples

**Three gametes and the root.** The rooted matrix with rows $01$, $10$ and $11$ has $R_{\min} = 1$. With the root row $00$, the two sites show all four gametes. One recombination suffices: a sequence takes site 1 from the ancestor of $10$ and site 2 from the ancestor of $01$. Without the row $11$, the rows $01$ and $10$ fit a tree with two branches, and $R_{\min} = 0$.

**The matrix of Gusfield, Eddhu and Langley.** Their Figure 1 uses seven sequences on five sites, with root $00000$:

| row | a | b | c | d | e | f | g |
| --- | --- | --- | --- | --- | --- | --- | --- |
| sequence | 00010 | 10010 | 00100 | 10100 | 01100 | 01101 | 00101 |

With the root row, the incompatible pairs are sites $(1, 3)$, $(1, 4)$ and $(2, 5)$. The intervals $[1, 3]$, $[1, 4]$ and $[2, 5]$ all contain the gap between sites 2 and 3, so one breakpoint hits all of them and $R_M = 1$. The rows are all different, so with the root there are 8 distinct haplotypes on 5 sites. A tree with 5 sites shows at most 6, so $R_h \ge 8 - 5 - 1 = 2$. The exact search of this page's implementation finds a history with 2 recombinations, so $R_{\min} = 2$, and the haplotype bound is tight here while $R_M$ is not.

## Known algorithms

| method | what it gives | time | source |
| --- | --- | --- | --- |
| four-gamete test on all pairs | whether $R_{\min} = 0$ | $O(n m^2)$, or $O(nm)$ by Gusfield's method | [perfect phylogeny](/gusfield-perfect-phylogeny/) |
| incompatible intervals, then a greedy stab | lower bound $R_M$ | $O(n m^2)$ | Hudson and Kaplan 1985 |
| distinct haplotypes on site sets, then dynamic programming | lower bound $R_h$ | exponential in the size of the site sets, $O(m^2)$ for the composition | Myers and Griffiths 2003 |
| integer programming over local bounds | lower bound HapBound | exponential in the worst case | Song, Wu and Gusfield 2005 |
| a constructed history | upper bound SHRUB | polynomial per step | Song, Wu and Gusfield 2005 |
| search backward over ancestral states | exact $R_{\min}$ | exponential | Lyngsø, Song and Hein 2005 |
| decomposition into galls | a galled tree, if one exists, which is optimal | $O(nm + n^3)$ | Gusfield, Eddhu and Langley 2004 |
| Markov chain Monte Carlo under the sequentially Markov coalescent | samples of ARGs | many sweeps, each about linear in the number of sites | Rasmussen et al. 2014 |

**Hudson and Kaplan.** List the incompatible pairs $(i, j)$ with $i < j$ as intervals of sites. A breakpoint in gap $g$, between sites $g$ and $g + 1$, hits $[i, j]$ when $i \le g < j$. $R_M$ is the least number of gaps that hit every interval. Hudson and Kaplan first drop each interval that contains another one, then count from the left the intervals that do not overlap the last one counted. This is the same as the greedy stab by right end, the dual of [activity selection](/activity-selection/): it gives the least number of stabbing gaps, which equals the largest number of intervals with no gap in common.

**The haplotype bound.** If $S$ is a set of sites in an interval and $h_S$ is the number of distinct rows of $M$ restricted to $S$, then a part of the sequence with no breakpoint shows at most $|S| + 1$ distinct haplotypes on $S$, because each mutation adds one. Each recombination adds at most one more. So $B(a, b) = \max_S (h_S - |S| - 1)$ is a lower bound on the breakpoints inside $[a, b]$. Myers and Griffiths combine local bounds along the sequence with $R[b] = \max_{a < b} (R[a] + B(a, b))$, since intervals that share only an end site have no gap in common. With $B = 1$ on incompatible pairs, this gives $R_M$ again, so $R_M \le R_h$.

**Exact search.** Go backward in time from the samples. A state is a list of partial sequences, with a mark for sites that are not ancestral. Three steps are allowed: merge two sequences that agree wherever both are ancestral, at no cost; set a 1 back to 0 when only one sequence has a 1 at that site, at no cost, since that is the one mutation; and split a sequence at a gap into a left part and a right part, at cost 1. $R_{\min}$ is the cost of the cheapest way to reach one sequence. This page's implementation runs a [0-1 breadth-first search](/zero-one-bfs/) over the states. Lyngsø, Song and Hein use branch and bound with the lower bounds above to cut the search.

## Bounds

- **Chain of bounds.** $R_M \le R_h \le R_{\min}$. The tests of this page check this chain on random matrices with up to 4 rows and 4 columns against the exact search.
- **Tightness.** Both bounds can be strict. On the matrix above, $R_M = 1 < R_h = R_{\min} = 2$. The rooted matrix with rows $1101$, $1100$, $0011$ and $0111$ has $R_M = R_h = 1$, but the exact search gives $R_{\min} = 2$.
- **Zero.** $R_{\min} = 0$ if and only if no pair of sites is incompatible, by the four-gamete theorem.
- **Rooted against unrooted.** Adding the root row can only add incompatible pairs, so the rooted values are at least the unrooted ones.
- **Hardness.** Computing $R_{\min}$ is NP-hard (Wang, Zhang and Zhang 2001). The galled tree case is polynomial.

## Reductions

- **Perfect phylogeny.** $R_{\min}(M) = 0$ is the [perfect phylogeny](/perfect-phylogeny/) problem for binary characters, solved in $O(nm)$ time by [Gusfield's algorithm](/gusfield-perfect-phylogeny/).
- **Interval stabbing.** $R_M$ is a minimum stabbing set of the incompatible intervals by gaps.
- **Tree distances.** One recombination changes the marginal tree by at most one rooted [SPR move](/spr-distance/): the recombining lineage is pruned from the tree on one side and regrafted where its other parent joins. So if two blocks of sites each fix a binary tree, $R_{\min}$ is at least the rSPR distance between those trees. An ARG is a [phylogenetic network](/phylogenetic-network/) with times, and the network view leads to the hybridization number as a related lower bound.
- **Galled trees.** Build the incompatibility graph, with one vertex per site and one edge per incompatible pair. In a galled tree, each connected component with more than one site is explained by one gall, so the problem splits into one small problem per component.

## Applications

- **Recombination rates and hotspots.** Lower bounds such as $R_M$ and $R_h$ count events in each region of a sample, which shows where recombination is frequent.
- **Association mapping.** The marginal trees of an inferred ARG group the samples by shared ancestry at each position, which helps to locate the sites that affect a trait.
- **Population history.** Inferred tree sequences for many genomes give the times of common ancestors along the genome, which inform estimates of population size and of mixing between populations.
- **Testing a tree model.** Before a single tree is built for a region, $R_M > 0$ shows that one tree cannot fit it.

## References
