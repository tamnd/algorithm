---
tag: KH1G6R
kind: concept
slug: horizontal-gene-transfer
name: Horizontal gene transfer
aliases:
- lateral gene transfer
- HGT
- LGT
area: biology/phylogenetics
level: advanced
summary: Genetic material moves between lineages outside parent-to-offspring descent, so gene trees of the moved genes disagree with the species tree.
prereqs: [phylogenetic-tree, tree-reconciliation]
see_also: [duplication-loss-model, lca-reconciliation, phylogenetic-network, spr-distance, maximum-agreement-forest, incomplete-lineage-sorting, species-tree-estimation, np-hard]
sources:
  - paper: doi:10.1038/35012500
    title: Howard Ochman, Jeffrey G. Lawrence and Eduardo A. Groisman, Lateral gene transfer and the nature of bacterial innovation, Nature 405(6784), 2000
    locator: pp. 299-304 (mechanisms of transfer in bacteria and its role in their evolution)
  - paper: doi:10.1126/science.284.5423.2124
    title: W. Ford Doolittle, Phylogenetic classification and the universal tree, Science 284(5423), 1999
    locator: pp. 2124-2128 (transfer as a challenge to a single tree of life)
  - paper: doi:10.1186/1471-2148-6-15
    title: Robert G. Beiko and Nicholas Hamilton, Phylogenetic identification of lateral genetic transfer events, BMC Evolutionary Biology 6, 2006
    locator: article 15 (transfers inferred as subtree prune and regraft moves between gene and species trees)
  - paper: doi:10.1109/TCBB.2010.14
    title: Ali Tofigh, Michael Hallett and Jens Lagergren, Simultaneous identification of duplications and lateral gene transfers, IEEE/ACM Transactions on Computational Biology and Bioinformatics 8(2), 2011
    locator: pp. 517-535 (reconciliation with duplications and transfers, polynomial without time consistency)
  - paper: doi:10.1093/bioinformatics/bts225
    title: Mukul S. Bansal, Eric J. Alm and Manolis Kellis, Efficient algorithms for the reconciliation problem with gene duplication, horizontal transfer and loss, Bioinformatics 28(12), 2012
    locator: pp. i283-i291 (DTL reconciliation in O(mn) time)
  - paper: doi:10.1089/cmb.2009.0240
    title: Yaniv Ovadia, Daniel Fielder, Chris Conow and Ran Libeskind-Hadas, The cophylogeny reconstruction problem is NP-complete, Journal of Computational Biology 18(1), 2011
    locator: pp. 59-65 (NP-completeness with time-consistent transfers)
---

Horizontal gene transfer (HGT) is the movement of genetic material from one organism to another that is not its offspring, often across species. In bacteria and archaea it happens through uptake of free DNA, through viruses that carry DNA between cells, and through direct cell-to-cell transfer of plasmids. A transferred gene then has a history that leaves the species tree: its gene tree puts the receiving species next to the donor. In algorithms, HGT is the transfer event of duplication-transfer-loss [reconciliation](/tree-reconciliation/), and it is the main reason to describe the history of microbes by a [phylogenetic network](/phylogenetic-network/) instead of a tree.

## In plain words

Most genes go from parents to children. Some genes jump sideways, from one species into another one that lives at the same time. Bacteria do this often, for example to pass on genes that protect them from medicines.

When a gene jumps, the family tree of that gene does not match the family tree of the species anymore. The species that got the gene now looks like a close relative of the species that gave it.

To find such jumps, we compare the tree of each gene with the tree of the species and look for the smallest set of jumps, copies and losses that explains the difference. Jumps must also make sense in time, because both species must be alive at the moment of the jump.

## The idea

**A transfer as an event.** A transfer copies a gene from a donor lineage into a recipient lineage that exists at the same time. In the gene tree it shows as a node with one child that stays in the donor and one child that continues in the recipient. If the recipient already had a copy of the gene and loses it, the transfer replaces it. Otherwise the recipient gains a new copy.

**A transfer as a tree rearrangement.** If the gene has one copy per species and its history has only transfers, each transfer cuts the recipient subtree out of the species tree and regrafts it next to the donor. That is one [subtree prune and regraft](/subtree-prune-and-regraft/) move. So the number of transfers is at least the rooted [SPR distance](/spr-distance/) between the gene tree and the species tree, which equals one less than the size of a [maximum agreement forest](/maximum-agreement-forest/). Beiko and Hamilton (2006) used this view to infer transfers.

**Transfers in reconciliation.** In duplication-transfer-loss (DTL) reconciliation, each gene node is a speciation, a duplication or a transfer, and each event has a cost. Without time constraints, the best reconciliation comes from a dynamic program over pairs of gene and species nodes: Tofigh, Hallett and Lagergren (2011) gave a polynomial algorithm, and Bansal, Alm and Kellis (2012) solved it in $O(mn)$ time for a gene tree with $n$ nodes and a species tree with $m$ nodes.

**Time consistency.** Each transfer needs the donor and the recipient to be alive at the same time. On a species tree without node dates, one transfer alone always fits some order of the speciations, but two transfers can need opposite orders. Requiring that all transfers fit one order in time makes the reconciliation problem NP-hard (Ovadia et al. 2011). With known node dates, transfers are allowed only between edges that overlap in time, and a dynamic program over time slices stays polynomial.

**Other signals.** A recently transferred gene often differs from the rest of its new genome in GC content and codon usage. These compositional methods need no tree, but the signal fades as the gene adapts to its new genome.

## Examples

**A single transfer.** Species tree $((a, b), c)$, gene tree $((a_1, c_1), b_1)$. One transfer from the lineage of $a$ into $c$ explains the gene tree, while a story with only duplications and losses needs one duplication and three losses. Which story wins depends on the costs.

**Two transfers with no consistent dating.** Take the species tree $((a, b), (c, d))$ with inner nodes $u = ab$ and $v = cd$. A transfer from the edge above $a$ into the edge above $v$ needs a time after the split at $u$ and before the split at $v$, so it needs $u$ to be older than $v$. A transfer from the edge above $c$ into the edge above $u$ needs $v$ to be older than $u$. Each transfer alone is possible, but no dating of the species tree allows both. An undated DTL algorithm can return both, and a time-consistent method must replace one of them.

**Ecology.** Genes for antibiotic resistance on plasmids spread between unrelated bacterial species, so their gene trees follow the plasmid and not the species.

## Where it is used

- **Microbial phylogenomics.** Gene families of bacteria and archaea are reconciled under DTL to count gains, losses and transfers on each branch, and to find genes that keep the vertical signal.
- **Species tree estimation.** Transfers add discordance on top of [incomplete lineage sorting](/incomplete-lineage-sorting/). Methods for [species tree estimation](/species-tree-estimation/) are tested for robustness to transfer, and genes with signs of transfer are often left out.
- **The tree of life.** Frequent transfer among microbes led Doolittle (1999) to question whether one tree describes their history. Networks and forests of gene trees are the alternatives.
- **Origin of organelles.** Genes moved from the ancestors of mitochondria and chloroplasts into the nuclear genome. Reconciliation places these transfers on the tree.
- **Cophylogeny.** Host switches of parasites follow the same mathematics as transfers, so the same algorithms and hardness results hold.

## References
