---
tag: HS0YNY
kind: model
slug: duplication-loss-model
name: Duplication-loss model
aliases:
- DL model
- gene evolution model
area: biology/phylogenetics
level: advanced
summary: A gene family grows by duplications and shrinks by losses, as a birth-death process run along each branch of a dated species tree.
history:
  year: 2003
  people: [Lars Arvestad, Ann-Charlotte Berglund, Jens Lagergren, Bengt Sennblad]
  note: Arvestad and coauthors used a birth-death process of genes inside a species tree for Bayesian reconciliation and orthology analysis in 2003.
prereqs: [birth-death-process, tree-reconciliation]
see_also: [lca-reconciliation, horizontal-gene-transfer, incomplete-lineage-sorting, multispecies-coalescent, metropolis-hastings, bayesian-phylogenetic-inference, phylogenetic-likelihood]
sources:
  - paper: doi:10.1093/bioinformatics/btg1000
    title: Lars Arvestad, Ann-Charlotte Berglund, Jens Lagergren and Bengt Sennblad, Bayesian gene/species tree reconciliation and orthology analysis using MCMC, Bioinformatics 19(Suppl. 1), 2003
    locator: pp. i7-i15 (the birth-death model of genes in a species tree, and MCMC over gene trees and reconciliations)
  - paper: doi:10.1145/1502793.1502796
    title: Lars Arvestad, Jens Lagergren and Bengt Sennblad, The gene evolution model and computing its associated probabilities, Journal of the ACM 56(2), 2009
    locator: pp. 1-44 (the gene evolution model and dynamic programs for the probability of a gene tree given a species tree)
  - paper: doi:10.1109/TCBB.2011.64
    title: Jean-Philippe Doyon, Sylvie Hamel and Cedric Chauve, An efficient method for exploring the space of gene tree/species tree reconciliations in a probabilistic framework, IEEE/ACM Transactions on Computational Biology and Bioinformatics 9(1), 2012
    locator: pp. 26-39 (the most probable reconciliation under the duplication-loss model, and its difference from the most parsimonious one)
  - paper: doi:10.1101/gr.123901.111
    title: Matthew D. Rasmussen and Manolis Kellis, Unified modeling of gene duplication, loss, and coalescence using a locus tree, Genome Research 22(4), 2012
    locator: pp. 755-765 (duplication and loss combined with the multispecies coalescent)
  - paper: doi:10.1214/aoms/1177730285
    title: David G. Kendall, On the generalized birth-and-death process, Annals of Mathematical Statistics 19(1), 1948
    locator: pp. 1-15 (the distribution of the population size of a linear birth-death process)
---

The duplication-loss model is a probabilistic model of how a gene family evolves inside a species tree. Along each branch of a dated species tree, each gene copy duplicates at rate $\lambda$ and is lost at rate $\mu$, independently of the other copies, so the number of copies follows a linear [birth-death process](/birth-death-process/). At each speciation, every copy passes into both daughter species. The model gives a probability to each gene tree with its [reconciliation](/tree-reconciliation/), and it is the basis of Bayesian methods that infer gene trees, duplications and orthologs together (Arvestad et al. 2003; 2009).

## The machine

**The input.** A rooted binary species tree $S$ with a time on each node, and a stem edge above its root. The rates $\lambda \ge 0$ (duplication) and $\mu \ge 0$ (loss).

**The process.**

1. Start with one gene copy at the top of the stem edge.
2. On each species edge, run a birth-death process for the edge's time span. Each copy waits an exponential time with rate $\lambda + \mu$. With probability $\lambda / (\lambda + \mu)$ it duplicates into two copies in the same species, and otherwise it is lost.
3. At each species node, each copy that reaches the node splits into one copy for each daughter edge. This is a speciation event of the gene tree.
4. At the leaves of $S$, the surviving copies are the genes of the family.

The full history is a gene tree with all copies, including the lost ones, a map of its nodes to points of $S$, and the times of all events. The observed gene tree keeps only the lineages with at least one surviving descendant, as in the reconstructed process of the birth-death page.

**The extension to sequences.** In the gene evolution model of Arvestad, Lagergren and Sennblad (2009), each gene edge also gets a rate from a relaxed clock, and the sequences evolve along the gene tree under a [substitution model](/substitution-model/). Then the [phylogenetic likelihood](/phylogenetic-likelihood/) of the sequences and the duplication-loss probability of the gene tree enter one posterior.

## What it counts

- **The probability of a gene tree with its reconciliation.** The density of the observed gene tree, its event times, and its map into $S$, given $S$, $\lambda$ and $\mu$.
- **The probability of a gene tree alone.** The sum, or integral, over all reconciliations and event times.
- **The size of the gene family in each species.** The number of copies at a leaf of $S$. One copy at the root of an edge of length $t$ gives a count with the Kendall distribution of a birth-death process over time $t$.
- **The expected numbers of duplications and losses on each branch**, which compare with the counts of a parsimony reconciliation.

## Relation to other models

- **Birth-death process.** On a single edge, the model is the linear birth-death process with births as duplications and deaths as losses. A speciation node does not change the number of copies on each side. So, by the semigroup property of the birth-death generating function, the number of copies at one leaf at depth $T$ below the stem has the same law as a birth-death process run for time $T$ from one copy. The counts at different leaves are dependent, since they share ancestral branches.
- **Parsimony reconciliation.** The [LCA mapping](/lca-reconciliation/) gives the reconciliation with the fewest duplications and losses. Under the duplication-loss model, the most probable reconciliation can differ from it, because the probability depends on branch lengths and on where on a branch each event falls (Doyon, Hamel and Chauve 2012).
- **Multispecies coalescent.** The DL model explains all discordance between a gene tree and the species tree by duplications and losses. The [multispecies coalescent](/multispecies-coalescent/) explains it by [incomplete lineage sorting](/incomplete-lineage-sorting/). The DLCoal model of Rasmussen and Kellis (2012) combines both: a locus tree evolves by duplication and loss in the species tree, and the gene tree evolves by coalescence inside the locus tree.
- **Transfers.** Adding a rate of transfer from one living species lineage to another gives a duplication-transfer-loss model, the probabilistic form of DTL reconciliation with [horizontal gene transfer](/horizontal-gene-transfer/).

## Known results in the model

- **The probability of a gene tree in polynomial time.** Arvestad, Lagergren and Sennblad (2009) gave dynamic programs that sum over all reconciliations and integrate over the event times. Discretizing time on each species edge makes the sums finite, and the work is polynomial in the sizes of the gene tree, the species tree and the time grid.
- **Joint Bayesian inference.** MCMC over gene trees, reconciliations, rates and edge times gives posterior probabilities of orthology and of duplications (Arvestad et al. 2003). It uses the sequences and the species tree together, which gives more accurate gene trees than sequence data alone.
- **Most probable and most parsimonious maps differ.** The most probable reconciliation can be found by dynamic programming over the gene tree and the time grid, and it is not always the LCA mapping (Doyon, Hamel and Chauve 2012).
- **Copy number.** The number of copies in a leaf species starting from one copy at depth $T$ is $0$ with probability $\alpha$ and $k \ge 1$ with probability $(1 - \alpha)(1 - \beta)\beta^{k - 1}$, where $\alpha$ and $\beta$ are Kendall's functions of $\lambda$, $\mu$ and $T$. If $\lambda = \mu$, the expected number of copies stays $1$, but the probability that the family is absent tends to $1$ as $T$ grows.
- **Identifiability of the rates.** For a known $T$, the pair $(\alpha, \beta)$ determines $\lambda$ and $\mu$: the ratio $\alpha / \beta$ equals $\mu / \lambda$, and then $\beta$ fixes $\lambda - \mu$. So copy numbers of many independent families with shared rates identify both rates.

## References
